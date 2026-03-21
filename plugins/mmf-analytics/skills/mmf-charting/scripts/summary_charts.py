#!/usr/bin/env python3
"""
summary_charts.py — Latest-month vs. prior-month grouped bar charts for all 4 funds.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SCRIPTS_DIR = "/sessions/jolly-sharp-faraday/mnt/.local-plugins/marketplaces/local-desktop-app-uploads/mmf-analytics/skills/mmf-charting/scripts"
sys.path.insert(0, SCRIPTS_DIR)
from chart_utils import (
    base_parser, ensure_out, report_png, load_data,
    apply_clean_style, save_fig,
    FUND_COLORS, TICKERS,
)

METRICS = [
    ("aum_B",                  "AUM ($B)",        None,  "${:.2f}B"),
    ("avg_portfolio_maturity",  "WAM (days)",      None,  "{:.0f}d"),
    ("avg_life_maturity",       "WAL (days)",      None,  "{:.0f}d"),
    ("cash_pct",                "Cash % of NAV",   None,  "{:.2f}%"),
    ("daily_liq_pct",           "Daily Liquid %",  10,    "{:.1f}%"),
    ("weekly_liq_pct",          "Weekly Liquid %", 30,    "{:.1f}%"),
]


def get_prior_date(series, ticker, latest_date):
    dates = sorted(series[series["ticker"] == ticker]["report_date"].unique())
    prior = [d for d in dates if d < latest_date]
    return prior[-1] if prior else None


def build_snapshot(series, holdings, ticker, date):
    if date is None:
        return None
    s_row = series[(series["ticker"] == ticker) & (series["report_date"] == date)]
    h_rows = holdings[(holdings["ticker"] == ticker) & (holdings["report_date"] == date)]
    if s_row.empty or h_rows.empty:
        return None
    nav = s_row["net_asset_of_series"].iloc[0]
    daily_pct  = h_rows.loc[h_rows["daily_liquid"]  == "Y", "value_excl_sponsor"].sum() / nav * 100
    weekly_pct = h_rows.loc[h_rows["weekly_liquid"] == "Y", "value_excl_sponsor"].sum() / nav * 100
    return {
        "ticker":                 ticker,
        "aum_B":                  s_row["aum_B"].iloc[0],
        "avg_portfolio_maturity": s_row["avg_portfolio_maturity"].iloc[0],
        "avg_life_maturity":      s_row["avg_life_maturity"].iloc[0],
        "cash_pct":               s_row["cash_pct"].iloc[0],
        "daily_liq_pct":          daily_pct,
        "weekly_liq_pct":         weekly_pct,
        "report_date":            date,
    }


def build_both_periods(series, holdings, latest_per_ticker):
    cur_rows, prv_rows = [], []
    for ticker in TICKERS:
        lat_date = latest_per_ticker.get(ticker)
        prv_date = get_prior_date(series, ticker, lat_date)
        cur = build_snapshot(series, holdings, ticker, lat_date)
        prv = build_snapshot(series, holdings, ticker, prv_date)
        if cur: cur_rows.append(cur)
        if prv: prv_rows.append(prv)
    return pd.DataFrame(cur_rows), pd.DataFrame(prv_rows)


def make_mpl_charts(cur, prv, out_dir):
    matplotlib.rcParams["font.size"] = 10

    cur_label = cur["report_date"].iloc[0].strftime("%b %Y") if not cur.empty else "Current"
    prv_label = prv["report_date"].iloc[0].strftime("%b %Y") if not prv.empty else "Prior"

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.patch.set_facecolor("white")
    fig.suptitle(f"MMF Summary — {prv_label} vs. {cur_label}",
                 fontsize=15, fontweight="bold", y=1.01)

    n = len(TICKERS)
    bar_w = 0.38
    x = np.arange(n)

    for idx, (col, label, reg_min, fmt) in enumerate(METRICS):
        ax = axes[idx // 3][idx % 3]
        apply_clean_style(ax)

        cur_vals = [cur.loc[cur["ticker"] == t, col].values[0]
                    if t in cur["ticker"].values else np.nan for t in TICKERS]
        prv_vals = [prv.loc[prv["ticker"] == t, col].values[0]
                    if not prv.empty and t in prv["ticker"].values else np.nan for t in TICKERS]

        all_vals = [v for v in cur_vals + prv_vals if not np.isnan(v)]
        max_val  = max(all_vals) if all_vals else 1

        # Prior month bars (faded, left)
        for i, (val, ticker) in enumerate(zip(prv_vals, TICKERS)):
            if np.isnan(val): continue
            ax.bar(x[i] - bar_w / 2, val, width=bar_w,
                   color=FUND_COLORS[ticker], alpha=0.3,
                   edgecolor="white", linewidth=0.5)
            ax.text(x[i] - bar_w / 2, val + max_val * 0.013,
                    fmt.format(val), ha="center", va="bottom",
                    fontsize=7.5, color="#777777")

        # Current month bars (solid, right)
        for i, (val, ticker) in enumerate(zip(cur_vals, TICKERS)):
            if np.isnan(val): continue
            ax.bar(x[i] + bar_w / 2, val, width=bar_w,
                   color=FUND_COLORS[ticker], alpha=1.0,
                   edgecolor="white", linewidth=0.5)
            ax.text(x[i] + bar_w / 2, val + max_val * 0.013,
                    fmt.format(val), ha="center", va="bottom",
                    fontsize=7.5, fontweight="bold", color="#222222")

        # Change arrows
        for i, (cv, pv) in enumerate(zip(cur_vals, prv_vals)):
            if np.isnan(cv) or np.isnan(pv) or cv == pv: continue
            arrow = "▲" if cv > pv else "▼"
            color = "#2ca02c" if cv > pv else "#d62728"
            top = max(cv, pv) + max_val * 0.085
            ax.text(x[i], top, arrow, ha="center", va="bottom",
                    fontsize=9, color=color)

        if reg_min is not None:
            ax.axhline(reg_min, color="red", linestyle="--", linewidth=1.2, alpha=0.8)
            ax.text(n - 0.5, reg_min + max_val * 0.025,
                    f"{reg_min}% min", color="red", fontsize=7.5,
                    va="bottom", ha="right")

        ax.set_title(label, fontsize=11, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(TICKERS, fontsize=9)
        ax.set_ylabel(label, fontsize=9)
        ax.set_ylim(0, max_val * 1.30 if max_val > 0 else 1)

    legend_patches = [
        mpatches.Patch(facecolor="#888888", alpha=0.3, label=f"{prv_label} (prior)"),
        mpatches.Patch(facecolor="#888888", alpha=1.0, label=f"{cur_label} (current)"),
    ]
    fig.legend(handles=legend_patches, loc="upper right",
               bbox_to_anchor=(1.0, 1.01), fontsize=9, framealpha=0.9)

    plt.tight_layout()
    path = save_fig(fig, out_dir, "summary_all_metrics.png")
    return [path]


def main():
    p = base_parser("Latest vs. prior month grouped bar charts for all 4 MMFs")
    args = p.parse_args()
    out_dir = ensure_out(args.out)

    print(f"Loading data from {args.db}...")
    series, holdings, _, latest_per_ticker = load_data(args.db, args.days)
    cur, prv = build_both_periods(series, holdings, latest_per_ticker)

    if not cur.empty and not prv.empty:
        print(f"Current: {cur['report_date'].iloc[0].strftime('%b %Y')} | "
              f"Prior: {prv['report_date'].iloc[0].strftime('%b %Y')}")

    paths = make_mpl_charts(cur, prv, out_dir)
    for pp in paths:
        report_png(pp)
    print(f"\n✓ {len(paths)} summary chart(s) saved to {args.out}")


if __name__ == "__main__":
    main()
