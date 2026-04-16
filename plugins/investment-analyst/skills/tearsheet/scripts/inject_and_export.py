#!/usr/bin/env python3
"""
inject_and_export.py — SBC Tearsheet Automation
================================================
Attaches to a running Excel instance via Windows COM, injects narrative and
economic context into an open tearsheet template, triggers a Bloomberg data
refresh, exports the workbook as a PDF to the quarterly archive folder, and
saves the template.

Requirements:
    pip install pywin32

Usage:
    python inject_and_export.py \
        --workbook "Citibank.xlsx" \
        --narrative "Citigroup reported revenues of $24.6B..." \
        --economic-context "Economic Update — US Banks..." \
        --issuer "Citibank" \
        --quarter "1Q26" \
        --year "2026"

Fiscal offset example (Canadian banks, Toyota, Visa, etc.):
    python inject_and_export.py \
        --workbook "Bank of Montreal.xlsx" \
        --narrative "..." \
        --issuer "Bank of Montreal" \
        --quarter "2Q26" \
        --year "2026" \
        --fiscal-label "2Q26" \
        --calendar-label "1Q26"
"""

import argparse
import os
import sys
import time


# ---------------------------------------------------------------------------
# COM helpers
# ---------------------------------------------------------------------------

def get_excel_app():
    """Attach to the running Excel instance. Exits if Excel is not open."""
    try:
        import win32com.client
        xl = win32com.client.GetActiveObject("Excel.Application")
        return xl
    except ImportError:
        print(
            "ERROR: pywin32 is not installed.\n"
            "       Run: pip install pywin32",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception:
        print(
            "ERROR: Could not connect to Excel.\n"
            "       Make sure the tearsheet workbook is open in Excel with Bloomberg running.",
            file=sys.stderr,
        )
        sys.exit(1)


def find_workbook(xl, workbook_name: str):
    """
    Find an open workbook by filename (case-insensitive, .xlsx suffix optional).
    Lists all open workbooks in the error message to help diagnose mismatches.
    """
    target = workbook_name.lower().removesuffix(".xlsx").strip()
    for wb in xl.Workbooks:
        candidate = wb.Name.lower().removesuffix(".xlsx").strip()
        if candidate == target or target in candidate:
            return wb

    open_books = [wb.Name for wb in xl.Workbooks]
    print(
        f"ERROR: Workbook '{workbook_name}' not found in open Excel instances.\n"
        f"       Open workbooks: {open_books}\n"
        f"       Open the correct template and try again.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Sheet operations
# ---------------------------------------------------------------------------

def inject_narrative(wb, narrative_text: str):
    """
    Inject the earnings narrative into the Analysis sheet.

    The Analysis sheet layout:
      Row 1  — Dynamic header formula: ="Analysis / Q"&RIGHT(...)  (do NOT clear)
      Row 2+ — Narrative body (clear and replace)

    We find the first non-formula cell after row 1 and write the text there,
    preserving any formulas in row 1.
    """
    try:
        ws = wb.Sheets("Analysis")
    except Exception:
        print("ERROR: 'Analysis' sheet not found in workbook.", file=sys.stderr)
        sys.exit(1)

    # Determine how many rows are in use so we know what to clear.
    used_rows = ws.UsedRange.Rows.Count

    # Clear rows 2 onward (preserve row 1 formula/header).
    if used_rows > 1:
        clear_range = ws.Range(ws.Cells(2, 1), ws.Cells(used_rows + 5, 50))
        clear_range.ClearContents()

    # Write narrative starting at A2.
    cell = ws.Cells(2, 1)
    cell.Value = narrative_text
    cell.WrapText = True
    cell.VerticalAlignment = -4160   # xlTop
    cell.HorizontalAlignment = -4131 # xlLeft

    # Auto-fit row height so the full text is visible.
    ws.Rows(2).AutoFit()

    char_count = len(narrative_text)
    print(f"  ✓ Narrative injected into Analysis sheet ({char_count:,} chars)")


def update_economic_section(wb, economic_context: str):
    """
    Update the economic context section on the Front Page sheet.

    The Front Page has a cell (or merged cell) containing text like
    "Economic Update / US" or "= 'Economic Update / ' & ...".
    We search for the row containing "Economic Update", then write
    the context into the cell immediately below that heading.
    """
    try:
        ws = wb.Sheets("Front Page")
    except Exception:
        print(
            "  WARNING: 'Front Page' sheet not found — skipping economic context update.",
            file=sys.stderr,
        )
        return

    # Search used range for the "Economic Update" anchor cell.
    found_row, found_col = None, None
    used = ws.UsedRange
    for r in range(1, min(used.Rows.Count + 1, 40)):
        for c in range(1, min(used.Columns.Count + 1, 40)):
            cell = ws.Cells(r, c)
            try:
                val = str(cell.Value or "")
                text_val = str(cell.Text or "")
            except Exception:
                continue
            if "Economic Update" in val or "Economic Update" in text_val:
                found_row, found_col = r, c
                break
        if found_row:
            break

    if found_row is None:
        # Fallback: write to a known safe location (A15) and warn.
        print(
            "  WARNING: 'Economic Update' anchor not found on Front Page.\n"
            "           Writing economic context to cell A15 as fallback.",
            file=sys.stderr,
        )
        target = ws.Cells(15, 1)
    else:
        # Write into the cell two rows below the heading (leaves one blank row gap).
        target = ws.Cells(found_row + 2, found_col)

    # Unmerge if merged, then write.
    try:
        target.MergeArea.UnMerge()
    except Exception:
        pass

    target.Value = economic_context
    target.WrapText = True
    target.VerticalAlignment = -4160
    target.HorizontalAlignment = -4131

    print("  ✓ Economic context updated on Front Page")


# ---------------------------------------------------------------------------
# Bloomberg refresh
# ---------------------------------------------------------------------------

def trigger_bloomberg_refresh(xl, wb, wait_seconds: int = 4):
    """
    Force a full recalculation so Bloomberg BDP/BDH formulas re-query.
    Waits briefly between two Calculate() calls to allow async BDP responses.
    """
    try:
        xl.Calculate()
        time.sleep(wait_seconds)
        xl.Calculate()
        print("  ✓ Bloomberg refresh triggered")
    except Exception as e:
        print(f"  WARNING: Bloomberg refresh may not have completed: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# PDF export
# ---------------------------------------------------------------------------

def build_pdf_filename(issuer: str, quarter: str, fiscal_label: str = None,
                        calendar_label: str = None) -> str:
    """
    Build the PDF filename following SBC naming conventions.

    Standard:       Citibank 1Q26.pdf
    Fiscal offset:  Bank of Montreal 2Q26 (Calendar 1Q26).pdf
    """
    if fiscal_label and calendar_label and fiscal_label != calendar_label:
        return f"{issuer} {fiscal_label} (Calendar {calendar_label}).pdf"
    return f"{issuer} {quarter}.pdf"


def export_pdf(wb, issuer: str, quarter: str, year: str,
               fiscal_label: str = None, calendar_label: str = None) -> str:
    """
    Export all sheets as a PDF to the quarterly archive folder.
    Creates the folder if it doesn't exist.
    Returns the full path to the exported PDF.
    """
    # Build archive directory path.
    # Quarter folder uses the calendar quarter (e.g., "1Q26"), not the fiscal label.
    archive_dir = os.path.join(
        "T:\\", "Data", "Shared", "Credit analysis",
        "Quarterly Tearsheets", year, quarter
    )
    os.makedirs(archive_dir, exist_ok=True)

    filename = build_pdf_filename(issuer, quarter, fiscal_label, calendar_label)
    output_path = os.path.join(archive_dir, filename)

    try:
        wb.ExportAsFixedFormat(
            Type=0,                     # xlTypePDF
            Filename=output_path,
            Quality=0,                  # xlQualityStandard
            IncludeDocProperties=True,
            IgnorePrintAreas=False,
            OpenAfterPublish=False,
        )
        print(f"  ✓ PDF exported: {output_path}")
        return output_path

    except Exception as e:
        print(f"  ERROR: PDF export failed: {e}", file=sys.stderr)
        print(
            "  Tip: Check that the workbook's print areas are set correctly\n"
            "       and that the T: drive is accessible.",
            file=sys.stderr,
        )
        sys.exit(1)


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_workbook(wb):
    """Save the Excel template in place."""
    try:
        wb.Save()
        print(f"  ✓ Workbook saved: {wb.Name}")
    except Exception as e:
        print(f"  WARNING: Could not auto-save workbook: {e}", file=sys.stderr)
        print("           Please save manually (Ctrl+S).", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SBC Tearsheet — Excel injection & PDF export via Windows COM"
    )
    parser.add_argument("--workbook", required=True,
                        help="Workbook filename, e.g. 'Citibank.xlsx'")
    parser.add_argument("--narrative", required=True,
                        help="Earnings narrative text to inject into Analysis sheet")
    parser.add_argument("--economic-context", default="",
                        help="Economic context block for Front Page")
    parser.add_argument("--issuer", required=True,
                        help="Issuer name for PDF filename, e.g. 'Citibank'")
    parser.add_argument("--quarter", required=True,
                        help="Calendar quarter label, e.g. '1Q26'")
    parser.add_argument("--year", required=True,
                        help="Calendar year, e.g. '2026'")
    parser.add_argument("--fiscal-label", default=None,
                        help="Fiscal quarter label if different from calendar (e.g. '2Q26')")
    parser.add_argument("--calendar-label", default=None,
                        help="Calendar quarter label for dual-label naming (e.g. '1Q26')")
    parser.add_argument("--no-refresh", action="store_true",
                        help="Skip Bloomberg data refresh")
    parser.add_argument("--no-save", action="store_true",
                        help="Skip saving the workbook after export")
    args = parser.parse_args()

    sep = "=" * 52
    print(f"\n{sep}")
    print(f"  SBC Tearsheet Update: {args.issuer} {args.quarter}")
    print(f"{sep}\n")

    # 1. Connect to Excel.
    xl = get_excel_app()
    wb = find_workbook(xl, args.workbook)
    print(f"  ✓ Connected to workbook: {wb.Name}\n")

    # 2. Inject narrative.
    inject_narrative(wb, args.narrative)

    # 3. Update economic section.
    if args.economic_context:
        update_economic_section(wb, args.economic_context)
    else:
        print("  — Economic context not provided, skipping Front Page update")

    # 4. Bloomberg refresh.
    if not args.no_refresh:
        trigger_bloomberg_refresh(xl, wb)
    else:
        print("  — Bloomberg refresh skipped (--no-refresh)")

    # 5. Export PDF.
    pdf_path = export_pdf(
        wb,
        issuer=args.issuer,
        quarter=args.quarter,
        year=args.year,
        fiscal_label=args.fiscal_label,
        calendar_label=args.calendar_label,
    )

    # 6. Save workbook.
    if not args.no_save:
        save_workbook(wb)
    else:
        print("  — Workbook save skipped (--no-save)")

    print(f"\n{sep}")
    print(f"  ✓ COMPLETE")
    print(f"    PDF: {pdf_path}")
    print(f"{sep}\n")


if __name__ == "__main__":
    main()
