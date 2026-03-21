"""
chart_utils.py — Shared utilities for MMF Analytics charts.
Provides DB loading, data processing, Datawrapper helpers, and matplotlib fallback.
"""

import os
import sys
import sqlite3
import argparse
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

DEFAULT_DB = os.environ.get(
    "MMF_DB_PATH",
    "/sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db"
)
DEFAULT_OUT = "/tmp/mmf_charts"
DEFAULT_DAYS = 365

DW_API_TOKEN = "EIZmveiKHi0Yv5me8ZVzUeEqAeEmrO7h38MV6ApweA6N0JoXfws7vGkxmGFZhSrO"
DW_SOURCE    = "SEC EDGAR N-MFP2 Filings"
DW_BYLINE    = "SBC Treasury Analytics"

TICKERS = ["FRGXX", "GOFXX", "MVRXX", "BGSXX"]

FUND_COLORS = {
    "FRGXX": "#1f77b4",
    "GOFXX": "#ff7f0e",
    "MVRXX": "#2ca02c",
    "BGSXX": "#d62728",
}

BUCKET_ORDER  = ["<=1d", "2-7d", "8-30d", "31-90d", "91-180d", "180+d"]
BUCKET_COLORS = {
    "<=1d":    "#1a9850",
    "2-7d":    "#66bd63",
    "8-30d":   "#fee08b",
    "31-90d":  "#fdae61",
    "91-180d": "#f46d43",
    "180+d":   "#d73027",
}

CAT_MAP = {
    "U.S. Government Agency Debt": "Agency Debt",
    "U.S. Government Agency Debt (if categorized as coupon-paying notes)": "Agency Debt",
    "U.S. Government Agency Debt (if categorized as no-coupon discount notes)": "Agency Debt",
    "U.S. Treasury Debt": "Treasury Debt",
    "U.S. Government Agency Repurchase Agreement": "Agency Repo",
    "U.S. Government Agency Repurchase Agreement, collateralized only by U.S. Government Agency securities, U.S. Treasuries, and cash": "Agency Repo",
    "U.S. Treasury Repurchase Agreement": "Treasury Repo",
    "U.S. Treasury Repurchase Agreement, if collateralized only by U.S. Treasuries (including Strips) and cash": "Treasury Repo",
    "Other Repurchase Agreement": "Other Repo",
    "Other Repurchase Agreement, if any collateral falls outside Treasury, Government Agency and cash": "Other Repo",
    "Other Instrument": "Other",
    "Variable Rate Demand Note": "VRDN",
}

CAT_COLORS = {
    "Agency Debt":   "#1f77b4",
    "Treasury Debt": "#aec7e8",
    "Agency Repo":   "#ff7f0e",
    "Treasury Repo": "#ffbb78",
    "Other Repo":    "#2ca02c",
    "VRDN":          "#98df8a",
    "Other":         "#d62728",
}

# ── CLI Helpers ───────────────────────────────────────────────────────────────

def base_parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--db",  default=DEFAULT_DB,  help="Path to mmf_holdings.db")
    p.add_argument("--out", default=DEFAULT_OUT, help="Directory to save PNGs")
    p.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Lookback days (default 365)")
    return p


def ensure_out(out_dir: str) -> Path:
    p = Path(out_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def report_png(path: str):
    """Print PNG path in the format Claude uses to detect and display images."""
    print(f"PNG:{path}")

# ── Data Loading ──────────────────────────────────────────────────────────────

def load_data(db_path: str, days: int = 365):
    """
    Load and pre-process series_info and holdings for the last `days` days.
    Returns (series, holdings, cutoff, latest_per_ticker).
    """
    cutoff = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    con = sqlite3.connect(db_path)

    series = pd.read_sql(
        "SELECT * FROM series_info WHERE report_date >= ? ORDER BY ticker, report_date",
        con, params=(cutoff,)
    )
    series["report_date"] = pd.to_datetime(series["report_date"])
    series["aum_B"]       = series["net_asset_of_series"] / 1e9
    series["cash_pct"]    = series["cash"] / series["net_asset_of_series"] * 100

    holdings = pd.read_sql(
        """SELECT h.*, s.net_asset_of_series
           FROM holdings h
           JOIN series_info s ON h.ticker = s.ticker AND h.report_date = s.report_date
           WHERE h.report_date >= ?
           ORDER BY h.ticker, h.report_date""",
        con, params=(cutoff,)
    )
    holdings["report_date"] = pd.to_datetime(holdings["report_date"])
    holdings["simple_cat"]  = holdings["investment_category"].map(CAT_MAP).fillna(
        holdings["investment_category"]
    )

    # WAL maturity bucket
    holdings["wal_date"] = pd.to_datetime(holdings["maturity_date_wal"], errors="coerce")
    holdings["wal_days"] = (holdings["wal_date"] - holdings["report_date"]).dt.days
    holdings["mat_bucket"] = holdings["wal_days"].apply(_assign_bucket)

    latest_per_ticker = series.groupby("ticker")["report_date"].max().to_dict()

    con.close()
    return series, holdings, cutoff, latest_per_ticker


def _assign_bucket(days):
    if pd.isna(days): return "180+d"
    if days <= 1:     return "<=1d"
    if days <= 7:     return "2-7d"
    if days <= 30:    return "8-30d"
    if days <= 90:    return "31-90d"
    if days <= 180:   return "91-180d"
    return "180+d"

# ── Matplotlib Style ──────────────────────────────────────────────────────────

def apply_clean_style(ax):
    """Clean, no-grid, no-background matplotlib style."""
    ax.set_facecolor("white")
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_edgecolor("#dddddd")


def save_fig(fig, out_dir: Path, filename: str) -> str:
    path = str(out_dir / filename)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return path

# ── Datawrapper ───────────────────────────────────────────────────────────────

def get_dw():
    """Return initialized Datawrapper client, or None if unavailable."""
    try:
        from datawrapper import Datawrapper
        return Datawrapper(access_token=DW_API_TOKEN)
    except Exception:
        return None


def dw_publish_and_export(dw, chart_id: str, out_dir: Path, filename: str) -> str | None:
    """Publish a DW chart and export its PNG. Returns local path or None."""
    try:
        dw.publish_chart(chart_id)
        png_bytes = dw.export_chart(
            chart_id,
            unit="px",
            mode="rgb",
            width=900,
            zoom=2,
            plain=False,
            output="png",
        )
        path = str(out_dir / filename)
        with open(path, "wb") as f:
            f.write(png_bytes)
        return path
    except Exception as e:
        print(f"[DW export error] {e}", file=sys.stderr)
        return None


def dw_line_chart(dw, title: str, data: pd.DataFrame, intro: str,
                  custom_colors: dict, out_dir: Path, filename: str) -> str | None:
    """Create, publish, export a DW line chart. Returns PNG path or None."""
    try:
        chart = dw.create_chart(title=title, chart_type="d3-lines", data=data)
        cid = chart["id"]
        dw.update_description(cid, intro=intro, source_name=DW_SOURCE, byline=DW_BYLINE)
        if custom_colors:
            dw.update_metadata(cid, {"visualize": {"custom-colors": custom_colors}})
        return dw_publish_and_export(dw, cid, out_dir, filename)
    except Exception as e:
        print(f"[DW line chart error] {e}", file=sys.stderr)
        return None


def dw_bar_chart(dw, title: str, data: pd.DataFrame, intro: str,
                 custom_colors: dict, out_dir: Path, filename: str,
                 chart_type: str = "column-chart") -> str | None:
    """Create, publish, export a DW bar/column chart. Returns PNG path or None."""
    try:
        chart = dw.create_chart(title=title, chart_type=chart_type, data=data)
        cid = chart["id"]
        dw.update_description(cid, intro=intro, source_name=DW_SOURCE, byline=DW_BYLINE)
        if custom_colors:
            dw.update_metadata(cid, {"visualize": {"custom-colors": custom_colors}})
        return dw_publish_and_export(dw, cid, out_dir, filename)
    except Exception as e:
        print(f"[DW bar chart error] {e}", file=sys.stderr)
        return None


def dw_stacked_bar(dw, title: str, data: pd.DataFrame, intro: str,
                   custom_colors: dict, out_dir: Path, filename: str) -> str | None:
    """Create, publish, export a DW stacked bar chart. Returns PNG path or None."""
    try:
        chart = dw.create_chart(title=title, chart_type="d3-bars-stacked", data=data)
        cid = chart["id"]
        dw.update_description(cid, intro=intro, source_name=DW_SOURCE, byline=DW_BYLINE)
        if custom_colors:
            dw.update_metadata(cid, {"visualize": {"custom-colors": custom_colors}})
        return dw_publish_and_export(dw, cid, out_dir, filename)
    except Exception as e:
        print(f"[DW stacked bar error] {e}", file=sys.stderr)
        return None
