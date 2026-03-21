#!/usr/bin/env python3
"""
extract_metrics.py — Extract key fund metrics from mmf_holdings.db to JSON.

Used by build_presentation.js to populate slide callouts and stat boxes.

Usage:
    python3 extract_metrics.py [--db PATH] [--out PATH]

Output JSON structure:
{
  "report_date": "January 2025",
  "report_month": "January",
  "report_year": "2025",
  "funds": {
    "FRGXX": {
      "aum_B": 123.4, "wam": 30.0, "wal": 45.0,
      "yield_7d_pct": 4.52, "daily_liq": 42.1, "weekly_liq": 68.3,
      "hhi": 812, "top_issuer": "US TREASURY", "top_issuer_pct": 18.2,
      "report_date": "2025-01-31"
    },
    ...
  },
  "cross_fund": { "total_aum_B": 500.0 }
}
"""

import sys
import json
import sqlite3
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chart_utils import DEFAULT_DB, TICKERS


def main():
    p = argparse.ArgumentParser(description="Extract MMF metrics to JSON")
    p.add_argument("--db", default=DEFAULT_DB, help="Path to mmf_holdings.db")
    p.add_argument("--out", default=None, help="Output JSON file (default: stdout)")
    args = p.parse_args()

    con = sqlite3.connect(args.db)

    series = pd.read_sql(
        "SELECT * FROM series_info ORDER BY ticker, report_date", con
    )
    series["report_date"] = pd.to_datetime(series["report_date"])
    series["aum_B"] = series["net_asset_of_series"] / 1e9

    holdings = pd.read_sql("SELECT * FROM holdings", con)
    holdings["report_date"] = pd.to_datetime(holdings["report_date"])
    con.close()

    latest_per_ticker = series.groupby("ticker")["report_date"].max().to_dict()
    overall_latest = max(latest_per_ticker.values())

    funds = {}
    for ticker in TICKERS:
        lat = latest_per_ticker.get(ticker)
        if lat is None:
            continue

        s = series[(series["ticker"] == ticker) & (series["report_date"] == lat)]
        h = holdings[(holdings["ticker"] == ticker) & (holdings["report_date"] == lat)]

        if s.empty:
            continue

        nav = float(s["net_asset_of_series"].iloc[0] or 0)
        aum_b = nav / 1e9
        wam   = float(s["avg_portfolio_maturity"].iloc[0] or 0)
        wal   = float(s["avg_life_maturity"].iloc[0] or 0)
        # seven_day_gross_yield is stored as a decimal (e.g. 0.0452 = 4.52%)
        raw_yield = float(s["seven_day_gross_yield"].iloc[0] or 0)
        yield_pct = raw_yield * 100 if raw_yield < 0.5 else raw_yield  # guard

        daily_liq = weekly_liq = hhi = top1_pct = 0.0
        top_issuer = "N/A"
        if not h.empty and nav > 0:
            daily_liq  = float(h.loc[h["daily_liquid"]  == "Y", "value_excl_sponsor"].sum() / nav * 100)
            weekly_liq = float(h.loc[h["weekly_liquid"] == "Y", "value_excl_sponsor"].sum() / nav * 100)
            issuer_pcts = h.groupby("name_of_issuer")["value_excl_sponsor"].sum() / nav * 100
            hhi         = float((issuer_pcts ** 2).sum())
            top1_pct    = float(issuer_pcts.max())
            top_issuer  = str(issuer_pcts.idxmax())

        funds[ticker] = {
            "aum_B":          round(aum_b, 2),
            "wam":            round(wam, 1),
            "wal":            round(wal, 1),
            "yield_7d_pct":   round(yield_pct, 2),
            "daily_liq":      round(daily_liq, 1),
            "weekly_liq":     round(weekly_liq, 1),
            "hhi":            round(hhi, 0),
            "top_issuer":     top_issuer,
            "top_issuer_pct": round(top1_pct, 1),
            "report_date":    lat.strftime("%Y-%m-%d"),
        }

    total_aum = sum(v["aum_B"] for v in funds.values())

    result = {
        "report_date":  overall_latest.strftime("%B %Y"),
        "report_month": overall_latest.strftime("%B"),
        "report_year":  overall_latest.strftime("%Y"),
        "funds":        funds,
        "cross_fund":   {"total_aum_B": round(total_aum, 1)},
    }

    # NaN is not valid JSON — walk the dict and replace with None
    import math
    def clean_nans(obj):
        if isinstance(obj, float) and math.isnan(obj):
            return None
        if isinstance(obj, dict):
            return {k: clean_nans(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [clean_nans(v) for v in obj]
        return obj
    result = clean_nans(result)
    output = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output)
        print(f"Metrics written to {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
