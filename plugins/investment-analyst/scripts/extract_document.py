#!/usr/bin/env python3
"""
Local PDF extraction for SBC Treasury credit analysis pipeline.

Replaces PageIndex MCP with a local pymupdf4llm-based extractor that:
  1. Converts a PDF to page-tagged markdown
  2. Applies section filtering based on document type
  3. Writes targeted output suitable for a writer agent's context window

Designed to be called by source-collector agents after Chrome MCP downloads
the PDF. Intentionally deterministic — no LLM calls, no network, just parse
and filter.

Usage:
    python extract_document.py \
        --input /path/to/downloaded.pdf \
        --output /path/to/out.md \
        --type {press_release|supplement|filing|transcript} \
        [--max-pages 200]

Exit codes:
    0  success
    2  input file not found or not a PDF
    3  extraction library missing (pip install pymupdf4llm)
    4  extraction produced empty output (corrupt/image-only PDF)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Section filters
# ---------------------------------------------------------------------------
# Each filter is a list of (regex, keep_until_next_h1) tuples applied to the
# page-tagged markdown. A hit on the heading regex keeps everything from that
# heading until the next heading at the same-or-higher level (or end-of-doc).
#
# These patterns reflect what the writer agent actually needs for a bank
# tearsheet. For corporate issuers, the FILING and SUPPLEMENT filters are
# the same universe (MD&A, statements, segments, guidance).
# ---------------------------------------------------------------------------

PRESS_RELEASE_KEEP_ALL = True  # Press releases are short; keep everything.

SUPPLEMENT_SECTIONS: list[str] = [
    # US banks
    r"(?i)financial\s+highlights",
    r"(?i)consolidated\s+(results|summary)",
    r"(?i)segment\s+(results|performance|detail)",
    r"(?i)(credit|loan)\s+(quality|trends|metrics)",
    r"(?i)(net\s+charge[-\s]?offs?|npl|non[-\s]performing)",
    r"(?i)(capital|cet1|tier\s*1|risk[-\s]weighted)",
    r"(?i)liquidity\s+(coverage|profile|lcr)",
    r"(?i)(net\s+interest\s+income|nii|nim)",
    # EU / Canadian banks variants
    r"(?i)common\s+equity\s+tier\s*1",
    r"(?i)cost\s+of\s+risk",
    # Corporates
    r"(?i)(revenue|sales)\s+by\s+(segment|geography)",
    r"(?i)operating\s+(income|margin)",
    r"(?i)free\s+cash\s+flow",
    r"(?i)(outlook|guidance|forward[-\s]looking)",
]

FILING_SECTIONS: list[str] = [
    # 10-Q / 10-Q items
    r"(?i)management['\u2019]s\s+discussion\s+and\s+analysis",
    r"(?i)md&a",
    r"(?i)consolidated\s+(balance\s+sheet|statement)",
    r"(?i)condensed\s+consolidated",
    r"(?i)statements?\s+of\s+(operations|income|earnings|cash\s+flows)",
    r"(?i)(note\s+\d+\s*[\.\-:\u2014]\s*)?loans?\s+and\s+(allowance|lease)",
    r"(?i)(note\s+\d+\s*[\.\-:\u2014]\s*)?regulatory\s+capital",
    r"(?i)(note\s+\d+\s*[\.\-:\u2014]\s*)?allowance\s+for\s+credit\s+losses",
    r"(?i)(note\s+\d+\s*[\.\-:\u2014]\s*)?segment",
    r"(?i)risk\s+factors",  # Only kept if changed from prior period
]

TRANSCRIPT_SECTIONS: list[str] = [
    r"(?i)prepared\s+remarks",
    r"(?i)(chief\s+executive|ceo|chief\s+financial|cfo).{0,60}(opening|comment)",
    r"(?i)questions?\s+and\s+answers?",
    r"(?i)q\s*&\s*a",
    r"(?i)(outlook|guidance|forward[-\s]looking)",
    # Transcript headers often use speaker names; we fall back to keeping the
    # whole thing if no matches — transcripts are small enough to tolerate.
]


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_markdown(pdf_path: Path) -> str:
    """Convert PDF to page-tagged markdown via pymupdf4llm.

    Raises:
        ImportError: if pymupdf4llm is not installed.
        RuntimeError: if extraction yields empty output.
    """
    try:
        import pymupdf4llm  # type: ignore[import-untyped]
    except ImportError as e:
        raise ImportError(
            "pymupdf4llm not installed. Run: pip install pymupdf4llm --break-system-packages"
        ) from e

    # page_chunks=True gives us a list of per-page markdown blocks with metadata.
    # We wrap each page with a "## Page N" header so the writer agent can cite
    # pages when quoting numbers.
    chunks = pymupdf4llm.to_markdown(
        str(pdf_path),
        page_chunks=True,
        write_images=False,      # Charts/logos as images — skip; we want text
        extract_words=False,
        show_progress=False,
    )

    if not chunks:
        raise RuntimeError("Extraction yielded zero pages — PDF may be image-only")

    parts: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        if isinstance(chunk, dict):
            text = chunk.get("text", "")
        else:
            text = str(chunk)
        text = text.strip()
        if not text:
            continue
        parts.append(f"\n\n---\n\n## Page {i}\n\n{text}")

    combined = "\n".join(parts).strip()
    if not combined:
        raise RuntimeError("Extraction yielded empty text — PDF may be image-only")
    return combined


# ---------------------------------------------------------------------------
# Section filtering
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$", re.MULTILINE)
_PAGE_RE = re.compile(r"^## Page \d+\s*$", re.MULTILINE)


def filter_sections(markdown: str, patterns: Iterable[str]) -> str:
    """Keep only sections whose headings match one of the patterns.

    Page markers (## Page N) are always kept so the writer can cite pages.
    If no headings match any pattern, return the full document (fail-open)
    rather than returning nothing — better to give the writer too much than
    give it nothing.
    """
    compiled = [re.compile(p) for p in patterns]

    # Find every heading's position.
    headings: list[tuple[int, int, str]] = []  # (start, level, title)
    for m in _HEADING_RE.finditer(markdown):
        level = len(m.group(1))
        title = m.group(2)
        # Skip page markers — those are structural, not content headings.
        if _PAGE_RE.match(m.group(0)):
            continue
        headings.append((m.start(), level, title))

    if not headings:
        return markdown  # No structure detected; pass through.

    # Determine which headings to keep.
    keep_ranges: list[tuple[int, int]] = []  # (start_offset, end_offset)
    for idx, (start, level, title) in enumerate(headings):
        if not any(p.search(title) for p in compiled):
            continue
        # Find end: next heading at same-or-higher level.
        end = len(markdown)
        for j in range(idx + 1, len(headings)):
            next_start, next_level, _ = headings[j]
            if next_level <= level:
                end = next_start
                break
        keep_ranges.append((start, end))

    if not keep_ranges:
        # No pattern matched — fail open, return full document with a warning
        # so the writer knows filtering was attempted but found nothing.
        return (
            "<!-- section filter: no matching headings found; full document preserved -->\n\n"
            + markdown
        )

    # Merge overlapping ranges.
    keep_ranges.sort()
    merged: list[list[int]] = [list(keep_ranges[0])]
    for s, e in keep_ranges[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])

    # Collect kept text, preserving all page markers even outside kept ranges
    # so the writer can see document-wide pagination.
    page_markers = [(m.start(), m.end()) for m in _PAGE_RE.finditer(markdown)]

    kept_parts: list[str] = []
    last = 0
    for s, e in merged:
        # Include any page markers that fall between `last` and `s`
        for pstart, pend in page_markers:
            if last <= pstart < s:
                kept_parts.append(markdown[pstart:pend])
        kept_parts.append(markdown[s:e].rstrip())
        last = e
    # Trailing page markers
    for pstart, pend in page_markers:
        if pstart >= last:
            kept_parts.append(markdown[pstart:pend])

    return "\n\n".join(p for p in kept_parts if p.strip())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

TYPE_FILTERS = {
    "press_release": None,  # keep everything
    "supplement": SUPPLEMENT_SECTIONS,
    "filing": FILING_SECTIONS,
    "transcript": TRANSCRIPT_SECTIONS,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to input PDF")
    parser.add_argument("--output", required=True, help="Path to output markdown file")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(TYPE_FILTERS.keys()),
        help="Document type — drives section filtering",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=250,
        help="Refuse to process PDFs with more than this many pages (safety rail)",
    )
    args = parser.parse_args()

    pdf = Path(args.input)
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        print(f"ERROR: input not found or not a PDF: {pdf}", file=sys.stderr)
        return 2

    # Page-count guardrail before the expensive extraction step.
    try:
        import fitz  # PyMuPDF; bundled with pymupdf4llm
        doc = fitz.open(str(pdf))
        page_count = doc.page_count
        doc.close()
        if page_count > args.max_pages:
            print(
                f"ERROR: PDF has {page_count} pages (limit {args.max_pages}). "
                "Raise --max-pages if this is expected.",
                file=sys.stderr,
            )
            return 2
    except ImportError:
        # fitz is a dependency of pymupdf4llm; if it's missing, we'll fail
        # below with the clearer pymupdf4llm message.
        page_count = None

    try:
        md = extract_markdown(pdf)
    except ImportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 4

    patterns = TYPE_FILTERS[args.type]
    filtered = md if patterns is None else filter_sections(md, patterns)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    header = (
        f"<!-- Source: {pdf.name} | Type: {args.type} | "
        f"Pages: {page_count if page_count else 'unknown'} | "
        f"Extracted chars: {len(filtered):,} -->\n\n"
    )
    out.write_text(header + filtered, encoding="utf-8")

    print(
        f"OK: {args.type} extracted from {pdf.name}\n"
        f"  Input pages: {page_count if page_count else 'unknown'}\n"
        f"  Output chars: {len(filtered):,} (pre-filter: {len(md):,})\n"
        f"  Output path: {out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
