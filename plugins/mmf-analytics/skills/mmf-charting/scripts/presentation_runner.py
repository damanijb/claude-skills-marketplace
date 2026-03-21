#!/usr/bin/env python3
"""
presentation_runner.py — Generate the full MMF meeting presentation.

Steps:
  1. [Optional] Fetch latest SEC EDGAR N-MFP2 filings and rebuild the DB
  2. Generate all analytics charts (cross-fund, summary, heatmap, per-fund, issuers)
  3. Extract key metrics to JSON
  4. Build PPTX with pptxgenjs

Usage:
    python3 presentation_runner.py [--db PATH] [--out PPTX_PATH] [--fetch] [--charts-dir DIR]

Prints: PPTX:<path> on completion for Claude to detect and link.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

WORKSPACE   = "/sessions/jolly-sharp-faraday/mnt/MMF_holdings"
DEFAULT_DB  = os.environ.get("MMF_DB_PATH", f"{WORKSPACE}/mmf_holdings.db")
SCRIPTS_DIR = Path(__file__).parent
NODE_BIN    = "node"
NPM_BIN     = "npm"


def run(cmd, cwd=None, check=True):
    """Run a subprocess command, streaming output."""
    print(f"\n▶ {' '.join(str(c) for c in cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=cwd, text=True)
    if check and result.returncode != 0:
        print(f"  [WARNING] command exited with code {result.returncode}", file=sys.stderr)
    return result.returncode


def step_fetch(db_path: str):
    """Pull latest N-MFP2 filings from SEC EDGAR and rebuild the DB."""
    print("\n" + "="*60)
    print("  STEP 1: Fetching latest SEC EDGAR data")
    print("="*60)
    # Run fetch script from WORKSPACE so relative paths (data/) work correctly
    rc = run([sys.executable, f"{WORKSPACE}/fetch_nmfp_holdings.py"], cwd=WORKSPACE)
    if rc == 0:
        print("\n  Rebuilding SQLite database from CSVs...")
        run([sys.executable, f"{WORKSPACE}/build_db.py"], cwd=WORKSPACE)
    else:
        print("  [WARN] Fetch step had issues — proceeding with existing DB data.")


def step_charts(db_path: str, charts_dir: str, days: int):
    """Generate all PNG charts."""
    print("\n" + "="*60)
    print("  STEP 2: Generating analytics charts")
    print("="*60)
    scripts = [
        "cross_fund_charts.py",
        "summary_charts.py",
        "heatmap_chart.py",
        "top_issuers.py",
        "fund_deep_dive.py",  # generates per-ticker charts
    ]
    for script in scripts:
        run([sys.executable, str(SCRIPTS_DIR / script),
             "--db", db_path, "--out", charts_dir, "--days", str(days)])


def step_metrics(db_path: str, metrics_path: str):
    """Extract key metrics to JSON."""
    print("\n" + "="*60)
    print("  STEP 3: Extracting metrics to JSON")
    print("="*60)
    run([sys.executable, str(SCRIPTS_DIR / "extract_metrics.py"),
         "--db", db_path, "--out", metrics_path])


def step_pptx(charts_dir: str, metrics_path: str, out_path: str):
    """Build PPTX using pptxgenjs."""
    print("\n" + "="*60)
    print("  STEP 4: Building PowerPoint presentation")
    print("="*60)
    js_script = str(SCRIPTS_DIR / "build_presentation.js")
    run([NODE_BIN, js_script,
         "--charts-dir", charts_dir,
         "--metrics",    metrics_path,
         "--out",        out_path])


def main():
    p = argparse.ArgumentParser(description="Generate MMF meeting presentation")
    p.add_argument("--db",         default=DEFAULT_DB,
                   help="Path to mmf_holdings.db")
    p.add_argument("--out",        default=f"{WORKSPACE}/MMF_Investment_Review.pptx",
                   help="Output PPTX path")
    p.add_argument("--charts-dir", default="/tmp/mmf_charts",
                   help="Directory for intermediate chart PNGs")
    p.add_argument("--days",       type=int, default=365,
                   help="Lookback days for time-series charts")
    p.add_argument("--fetch",      action="store_true",
                   help="Pull latest data from SEC EDGAR before charting")
    p.add_argument("--no-charts",  action="store_true",
                   help="Skip chart regeneration (use existing PNGs)")
    args = p.parse_args()

    Path(args.charts_dir).mkdir(parents=True, exist_ok=True)
    metrics_path = str(Path(args.charts_dir) / "metrics.json")

    # ── Steps ──────────────────────────────────────────────────────────────
    if args.fetch:
        step_fetch(args.db)

    if not args.no_charts:
        step_charts(args.db, args.charts_dir, args.days)

    step_metrics(args.db, metrics_path)
    step_pptx(args.charts_dir, metrics_path, args.out)

    # ── Done ───────────────────────────────────────────────────────────────
    if Path(args.out).exists():
        print(f"\n{'='*60}")
        print(f"  ✓ Presentation complete!")
        print(f"  File: {args.out}")
        print(f"{'='*60}")
        print(f"\nPPTX:{args.out}")
    else:
        print(f"\n[ERROR] Expected output not found: {args.out}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
