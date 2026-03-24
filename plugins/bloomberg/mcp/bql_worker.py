"""BQL Worker — runs a single BQL query via bql.Service() and prints JSON to stdout.

Called by the Node.js MCP server as a subprocess.
Usage: python bql_worker.py <query_json>

The query_json is a JSON object: {"query": "get(px_last) for('AAPL US Equity')", "timeout": 60}
"""
import sys
import os
import json
import warnings

# Isolate from other Python environments
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p) != _script_dir]

warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import bql
import pandas as pd


def run_query(query: str) -> list[dict]:
    bq = bql.Service()
    response = bq.execute(query)
    df = bql.combined_df(response)

    if isinstance(df.index, pd.MultiIndex) or df.index.name:
        df = df.reset_index()

    # Collapse duplicate rows from combined_df's per-field expansion.
    # combined_df creates separate rows per field (name gets one row, px_last another)
    # with NaT in DATE for non-price fields. Only collapse when this pattern is detected.
    # Do NOT collapse time-series data (where DATE varies across rows for the same ID).
    if "ID" in df.columns and "DATE" in df.columns and len(df) > 0:
        n_unique_ids = df["ID"].nunique()
        n_unique_dates = df["DATE"].nunique()
        has_nat_dates = df["DATE"].isna().any()
        # Only collapse if: many rows per ID AND dates are mostly NaT (per-field expansion)
        # Skip if: dates are mostly populated (time-series data)
        if has_nat_dates and n_unique_dates <= 2 and len(df) > n_unique_ids:
            data_cols = [c for c in df.columns if c != "ID"]
            collapsed = df.groupby("ID", sort=False)[data_cols].first().reset_index()
            if len(collapsed) < len(df):
                df = collapsed

    return json.loads(df.to_json(orient="records", date_format="iso", default_handler=str))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)

    try:
        req = json.loads(sys.argv[1])
        query = req.get("query", "").strip()
        if not query:
            print(json.dumps({"error": "Empty query"}))
            sys.exit(1)

        results = run_query(query)
        print(json.dumps({"data": results, "count": len(results)}))
    except Exception as e:
        error_msg = str(e)
        hints = []
        if "YIELD" in error_msg.upper():
            hints.append("Use yield_type=YTW (not type=ytw)")
        if "DURATION" in error_msg.upper():
            hints.append("Use duration_type=modified (not type=modified)")
        if "BONDSUNIV" in error_msg.upper():
            hints.append("bondsuniv must be lowercase: bondsuniv(Active)")
        if "rating" in error_msg.lower() and "String Vectors" in error_msg:
            hints.append("Use rating(source=SP).source_scale <= 4, not >= 'AA-'")

        print(json.dumps({"error": error_msg, "hints": hints}))
        sys.exit(1)


if __name__ == "__main__":
    main()
