"""Universal BQL runner using bqnt-3 (Bloomberg's standard Python environment).

This script uses bql.Service() which is available on every Bloomberg terminal at:
    C:\blp\bqnt\environments\bqnt-3\python.exe

Usage:
    "C:\blp\bqnt\environments\bqnt-3\python.exe" bql_bqnt.py query.bql
    "C:\blp\bqnt\environments\bqnt-3\python.exe" bql_bqnt.py query.bql --json
    "C:\blp\bqnt\environments\bqnt-3\python.exe" bql_bqnt.py query.bql --output results.csv
    "C:\blp\bqnt\environments\bqnt-3\python.exe" bql_bqnt.py query.bql --timeout 120
"""
import sys
import os

# CRITICAL: Remove the script's directory from sys.path to avoid importing
# polars_bloomberg or other packages from the skill's scripts/ folder.
# bqnt-3 has its own self-contained environment.
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p) != _script_dir]

import argparse
import json
import time
import warnings

# Suppress the combined_df deprecation warning
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

# Fix encoding on Windows
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

import bql
import pandas as pd


def main():
    p = argparse.ArgumentParser(description="Run BQL via bql.Service() (bqnt-3)")
    p.add_argument("file", nargs="?", help="Path to .bql file containing the query")
    p.add_argument("--inline", help="BQL query string (for use from Python, not shell)")
    p.add_argument("--output", help="Save result to CSV")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--timeout", type=int, default=60, help="Timeout in seconds (default: 60)")
    args = p.parse_args()

    # Get query from file or inline
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            query = f.read().strip()
    elif args.inline:
        query = args.inline.strip()
    else:
        print("Provide a .bql file path or --inline query", file=sys.stderr)
        sys.exit(1)

    # Strip comment lines
    lines = [l for l in query.splitlines()
             if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("--")]
    query = " ".join(lines)

    print(f"BQL: {query[:200]}{'...' if len(query) > 200 else ''}", file=sys.stderr)

    start = time.time()
    bq = bql.Service()
    response = bq.execute(query)
    df = bql.combined_df(response)
    elapsed = time.time() - start

    # Reset multi-index to flat columns for clean output
    if isinstance(df.index, pd.MultiIndex) or df.index.name:
        df = df.reset_index()

    # bql.combined_df() creates separate rows per field with NaN for the others.
    # Collapse them: group by ID and take first non-null value for each column.
    if "ID" in df.columns and len(df) > 0:
        data_cols = [c for c in df.columns if c != "ID"]
        collapsed = df.groupby("ID", sort=False)[data_cols].first().reset_index()
        if len(collapsed) < len(df):
            df = collapsed

    print(f"Returned {len(df)} rows in {elapsed:.1f}s", file=sys.stderr)

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"Saved to {args.output}", file=sys.stderr)

    if args.json:
        print(json.dumps(df.to_dict(orient="records"), default=str, indent=2))
    elif not args.output:
        # Print as table
        with pd.option_context("display.max_rows", 50, "display.max_columns", 20, "display.width", 200):
            print(df)


if __name__ == "__main__":
    main()
