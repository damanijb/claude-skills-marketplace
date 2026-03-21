#!/usr/bin/env python3
"""
cross_fund_charts.py — Four line charts comparing all 4 MMF funds over 12 months.
Charts: AUM ($B), Cash % of NAV, WAM (days), WAL (days)

Usage:
    python3 cross_fund_charts.py [--db PATH] [--out DIR] [--days N]

Prints PNG:<path> for each chart saved.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Allow running as script or import
sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from chart_utils import (
    base_parser, ensure_out, report_png, load_data,
    apply_clean_style, save_fig, get_dw, dw_line_chart,
    FUND_COLORS, TICKERS,
)

PANELS = [
    ("aum_B",                 "AUM ($B)",      "AUM Over Time"),
    ("cash_pct",              "Cash % NAV",    "Cash as % of NAV"),
    ("avg_portfolio_maturity","WAM (days)",    "Weighted Avg Maturity (WAM)"),
    ("avg_life_maturity",     "WAL (days)",    "Weighted Avg Life (WAL)"),
]


def build_line_df(series: pd.DataFrame, col: str) -> pd.DataFrame:
    """Pivot series data into a date × ticker DataFrame for Datawrapper."""
    pivot = series.pivot_table(index="report_date", columns="ticker", values=col)
    pivot.index = pivot.index.strftime("%Y-%m-%d")
    pivot = pivot.rename_axis("Date").reset_index()
    # Keep only our 4 tickers (column order matters for DW colors)
    for t in TICKERS:
        if t not in pivot.columns:
            pivot[t] = float("nan")
    return pivot[["Date"] + TICKERS]


def make_dw_charts(series, out_dir, dw):
    paths = []
    for col, ylabel, title in PANELS:
        df = build_line_df(series, col)
        path = dw_line_chart(
            dw=dw,
            title=f"MMF — {title} (12 Months)",
            data=df,
            intro=f"{ylabel} for FRGXX, GOFXX, MVRXX, BGSXX over the past 12 months.",
            custom_colors=FUND_COLORS,
            out_dir=out_dir,
            filename=f"cross_fund_{col}.png",
        )
        if path:
            paths.append(path)
    return paths


def make_mpl_charts(series, out_dir):
    """Fallback: matplotlib clean charts, one per metric."""
    matplotlib.rcParams["font.size"] = 10
    paths = []

    for col, ylabel, title in PANELS:
        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor("white")
        apply_clean_style(ax)

        for ticker in TICKERS:
            df = series[series["ticker"] == ticker].sort_values("report_date")
            if df[col].isna().all():
                continue
            ax.plot(df["report_date"], df[col],
                    color=FUND_COLORS[ticker], marker="o", markersize=4,
                    linewidth=2, label=ticker)
            last = df.dropna(subset=[col]).iloc[-1]
            ax.annotate(f"{last[col]:.1f}",
                        xy=(last["report_date"], last[col]),
                        xytext=(5, 4), textcoords="offset points",
                        fontsize=7.5, color=FUND_COLORS[ticker], fontweight="bold")

        ax.set_title(f"MMF — {title} (12 Months)", fontsize=13, fontweight="bold", pad=12)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
        ax.legend(fontsize=9, loc="best", framealpha=0.9)
        plt.tight_layout()

        path = save_fig(fig, out_dir, f"cross_fund_{col}.png")
        paths.append(path)

    return paths


def main():
    p = base_parser("Cross-fund comparison: AUM, Cash%, WAM, WAL for all 4 MMFs")
    args = p.parse_args()
    out_dir = ensure_out(args.out)

    print(f"Loading data from {args.db}...")
    series, _, _, _ = load_data(args.db, args.days)

    paths = []
    dw = get_dw()
    if dw:
        print("Using Datawrapper...")
        paths = make_dw_charts(series, out_dir, dw)

    if not paths:
        print("Using matplotlib fallback...")
        paths = make_mpl_charts(series, out_dir)

    for p_path in paths:
        report_png(p_path)

    print(f"\n✓ {len(paths)} cross-fund chart(s) saved to {args.out}")


if __name__ == "__main__":
    main()
