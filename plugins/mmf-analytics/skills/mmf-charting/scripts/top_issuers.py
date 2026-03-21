#!/usr/bin/env python3
"""
top_issuers.py — Top 10 issuers by % of NAV for one or all funds (latest date).

Usage:
    python3 top_issuers.py [--db PATH] [--out DIR] [--days N] [--ticker FRGXX]

Prints PNG:<path> for each chart saved.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from chart_utils import (
    base_parser, ensure_out, report_png, load_data,
    apply_clean_style, save_fig, get_dw, dw_bar_chart,
    FUND_COLORS, TICKERS,
)


def build_top10(h, ticker, nav, lat_date) -> pd.DataFrame:
    lat_h = h[(h["ticker"] == ticker) & (h["report_date"] == lat_date)].copy()
    top10 = (
        lat_h.groupby("name_of_issuer")["value_excl_sponsor"]
        .sum().reset_index()
        .sort_values("value_excl_sponsor", ascending=False)
        .head(10)
    )
    top10["pct_nav"] = top10["value_excl_sponsor"] / nav * 100
    return top10


def chart_top10_dw(ticker, top10, lat_date, out_dir, dw):
    df = top10[["name_of_issuer", "pct_nav"]].rename(
        columns={"name_of_issuer": "Issuer", "pct_nav": "% of NAV"}
    ).sort_values("% of NAV", ascending=False)

    top5_pct = df["% of NAV"].head(5).sum()
    return dw_bar_chart(
        dw=dw,
        title=f"{ticker} — Top 10 Issuers ({lat_date.strftime('%b %Y')})",
        data=df,
        intro=f"Top 5 issuers represent {top5_pct:.1f}% of NAV.",
        custom_colors={"% of NAV": FUND_COLORS[ticker]},
        out_dir=out_dir,
        filename=f"{ticker}_top_issuers.png",
        chart_type="d3-bars",
    )


def chart_top10_mpl(ticker, top10, lat_date, out_dir):
    matplotlib.rcParams["font.size"] = 10
    t10 = top10.sort_values("pct_nav", ascending=True)
    top5_pct = top10.sort_values("pct_nav", ascending=False).head(5)["pct_nav"].sum()

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("white")
    apply_clean_style(ax)

    bars = ax.barh(t10["name_of_issuer"], t10["pct_nav"],
                   color=FUND_COLORS[ticker], edgecolor="white", linewidth=0.5, height=0.6)
    for bar, val in zip(bars, t10["pct_nav"]):
        ax.text(val + 0.15, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=10, fontweight="bold", color="#333333")

    ax.text(0.98, 0.02, f"Top 5 issuers: {top5_pct:.1f}% of NAV",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=9, color="#555555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f5f5f5", edgecolor="#cccccc"))

    ax.set_title(f"{ticker} — Top 10 Issuers ({lat_date.strftime('%b %Y')})",
                 fontweight="bold", fontsize=13)
    ax.set_xlabel("% of Net Assets", fontsize=11)
    ax.tick_params(axis="y", labelsize=9.5)
    ax.set_xlim(0, t10["pct_nav"].max() * 1.22)
    plt.tight_layout()
    return save_fig(fig, out_dir, f"{ticker}_top_issuers.png")


def run_fund(ticker, holdings, series, latest_per_ticker, out_dir, dw):
    lat_date = latest_per_ticker.get(ticker)
    if lat_date is None:
        return None
    s_row = series[(series["ticker"] == ticker) & (series["report_date"] == lat_date)]
    if s_row.empty:
        return None
    nav = s_row["net_asset_of_series"].iloc[0]
    top10 = build_top10(holdings, ticker, nav, lat_date)

    if dw:
        path = chart_top10_dw(ticker, top10, lat_date, out_dir, dw)
        if path:
            return path

    return chart_top10_mpl(ticker, top10, lat_date, out_dir)


def main():
    p = base_parser("Top 10 issuer charts (% of NAV, latest month)")
    p.add_argument("--ticker", default=None,
                   help="Single fund ticker. Default: all 4.")
    args = p.parse_args()
    out_dir = ensure_out(args.out)

    print(f"Loading data from {args.db}...")
    series, holdings, _, latest_per_ticker = load_data(args.db, args.days)

    tickers_to_run = [args.ticker] if args.ticker else TICKERS
    dw = get_dw()

    paths = []
    for ticker in tickers_to_run:
        print(f"  Top issuers: {ticker}...")
        path = run_fund(ticker, holdings, series, latest_per_ticker, out_dir, dw)
        if path:
            paths.append(path)

    for pp in paths:
        report_png(pp)

    print(f"\n✓ {len(paths)} top-issuer chart(s) saved to {args.out}")


if __name__ == "__main__":
    main()
