#!/usr/bin/env python3
"""
heatmap_chart.py — Cross-fund metric heatmap for latest reporting month.

Rows = funds, Columns = metrics. Each cell shows the raw value;
color encodes relative standing within each column (green = favorable, red = unfavorable).

Usage:
    python3 heatmap_chart.py [--db PATH] [--out DIR] [--days N]

Prints PNG:<path> for the saved chart.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from chart_utils import (
    base_parser, ensure_out, report_png, load_data,
    save_fig, FUND_COLORS, TICKERS,
)

# (col, display_label, fmt, higher_is_better)
#   higher_is_better=True  → highest value gets greenest cell
#   higher_is_better=False → lowest value gets greenest cell
#   higher_is_better=None  → neutral gradient (blue), no directional judgment
METRICS = [
    ("aum_B",                  "AUM\n($B)",          "${:.1f}B",  None),
    ("avg_portfolio_maturity",  "WAM\n(days)",        "{:.0f}d",   False),
    ("avg_life_maturity",       "WAL\n(days)",        "{:.0f}d",   False),
    ("cash_pct",                "Cash\n% NAV",        "{:.2f}%",   None),
    ("daily_liq_pct",           "Daily\nLiq %",       "{:.1f}%",   True),
    ("weekly_liq_pct",          "Weekly\nLiq %",      "{:.1f}%",   True),
    ("top1_pct",                "Top Issuer\n% NAV",  "{:.1f}%",   False),
    ("hhi",                     "HHI\nConcentration", "{:.0f}",    False),
]

# Regulatory reference lines (shown as annotation, not color)
REG_MINS = {"daily_liq_pct": 10.0, "weekly_liq_pct": 30.0}


def build_heatmap_table(series, holdings, latest_per_ticker):
    rows = []
    for ticker in TICKERS:
        lat_date = latest_per_ticker.get(ticker)
        if lat_date is None:
            continue
        s_row = series[(series["ticker"] == ticker) & (series["report_date"] == lat_date)]
        h_rows = holdings[(holdings["ticker"] == ticker) & (holdings["report_date"] == lat_date)]
        if s_row.empty or h_rows.empty:
            continue

        nav = s_row["net_asset_of_series"].iloc[0]
        daily_pct  = h_rows.loc[h_rows["daily_liquid"]  == "Y", "value_excl_sponsor"].sum() / nav * 100
        weekly_pct = h_rows.loc[h_rows["weekly_liquid"] == "Y", "value_excl_sponsor"].sum() / nav * 100

        # Top issuer % of NAV
        issuer_pcts = h_rows.groupby("name_of_issuer")["value_excl_sponsor"].sum() / nav * 100
        top1_pct = issuer_pcts.max() if len(issuer_pcts) > 0 else np.nan

        # HHI
        hhi = (issuer_pcts ** 2).sum() if len(issuer_pcts) > 0 else np.nan

        rows.append({
            "ticker":                 ticker,
            "aum_B":                  s_row["aum_B"].iloc[0],
            "avg_portfolio_maturity": s_row["avg_portfolio_maturity"].iloc[0],
            "avg_life_maturity":      s_row["avg_life_maturity"].iloc[0],
            "cash_pct":               s_row["cash_pct"].iloc[0],
            "daily_liq_pct":          daily_pct,
            "weekly_liq_pct":         weekly_pct,
            "top1_pct":               top1_pct,
            "hhi":                    hhi,
            "report_date":            lat_date,
        })
    return pd.DataFrame(rows)


def col_color(vals, higher_is_better):
    """
    Map a column of values to RGBA colors.
    - higher_is_better=True:  green↑, red↓
    - higher_is_better=False: green↓, red↑
    - higher_is_better=None:  neutral steel-blue gradient
    """
    arr = np.array(vals, dtype=float)
    finite = arr[~np.isnan(arr)]
    if len(finite) == 0 or finite.max() == finite.min():
        # All same → neutral mid
        return [matplotlib.cm.Blues(0.5)] * len(arr)

    normed = (arr - finite.min()) / (finite.max() - finite.min())  # 0=min, 1=max

    colors = []
    for n in normed:
        if np.isnan(n):
            colors.append((0.9, 0.9, 0.9, 1.0))
            continue
        if higher_is_better is None:
            # Neutral: light blue gradient
            colors.append(matplotlib.cm.Blues(0.3 + 0.5 * n))
        elif higher_is_better:
            # green for high, red for low
            colors.append(matplotlib.cm.RdYlGn(0.15 + 0.7 * n))
        else:
            # green for low, red for high  (invert)
            colors.append(matplotlib.cm.RdYlGn(0.15 + 0.7 * (1 - n)))
    return colors


def make_heatmap(tbl, out_dir):
    matplotlib.rcParams["font.size"] = 11

    report_date = tbl["report_date"].iloc[0].strftime("%b %Y")
    n_funds   = len(TICKERS)
    n_metrics = len(METRICS)

    cell_w, cell_h = 2.0, 1.1
    left_pad = 1.2   # room for ticker labels
    top_pad  = 1.4   # room for metric headers
    fig_w = left_pad + n_metrics * cell_w + 0.4
    fig_h = top_pad  + n_funds   * cell_h + 0.6

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    # ── Title ────────────────────────────────────────────────────────────────
    ax.text(fig_w / 2, fig_h - 0.22,
            f"MMF Fund Comparison Heatmap — {report_date}",
            ha="center", va="top", fontsize=14, fontweight="bold", color="#1a1a1a")

    # ── Column headers ────────────────────────────────────────────────────────
    for j, (col, label, fmt, hib) in enumerate(METRICS):
        cx = left_pad + j * cell_w + cell_w / 2
        cy = fig_h - top_pad + 0.1

        # Direction badge
        if hib is True:
            badge, badge_color = "↑ better", "#2ca02c"
        elif hib is False:
            badge, badge_color = "↓ better", "#d62728"
        else:
            badge, badge_color = "neutral", "#888888"

        ax.text(cx, cy, label, ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", color="#222222",
                multialignment="center")
        ax.text(cx, cy - 0.30, badge, ha="center", va="bottom",
                fontsize=7, color=badge_color, style="italic")

        # Regulatory min label
        if col in REG_MINS:
            ax.text(cx, cy - 0.52, f"min {REG_MINS[col]:.0f}%",
                    ha="center", va="bottom", fontsize=6.5, color="#cc0000")

    # ── Compute per-column colors ─────────────────────────────────────────────
    col_colors = {}
    for col, label, fmt, hib in METRICS:
        vals = [tbl.loc[tbl["ticker"] == t, col].values[0]
                if t in tbl["ticker"].values else np.nan
                for t in TICKERS]
        col_colors[col] = col_color(vals, hib)

    # ── Rows ──────────────────────────────────────────────────────────────────
    for i, ticker in enumerate(TICKERS):
        row_y = fig_h - top_pad - (i + 1) * cell_h

        # Ticker label
        ax.text(left_pad - 0.12, row_y + cell_h / 2,
                ticker, ha="right", va="center",
                fontsize=12, fontweight="bold",
                color=FUND_COLORS[ticker])

        for j, (col, label, fmt, hib) in enumerate(METRICS):
            cx = left_pad + j * cell_w
            cy = row_y

            val = tbl.loc[tbl["ticker"] == ticker, col].values[0] \
                  if ticker in tbl["ticker"].values else np.nan
            bg  = col_colors[col][i]

            # Cell background
            rect = FancyBboxPatch(
                (cx + 0.06, cy + 0.06),
                cell_w - 0.12, cell_h - 0.12,
                boxstyle="round,pad=0.04",
                facecolor=bg, edgecolor="white", linewidth=1.5,
                zorder=2
            )
            ax.add_patch(rect)

            # Cell value
            if not np.isnan(val):
                # Pick text color based on cell brightness
                r, g, b, _ = bg
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                txt_color = "#1a1a1a" if lum > 0.55 else "white"

                ax.text(cx + cell_w / 2, cy + cell_h / 2,
                        fmt.format(val),
                        ha="center", va="center",
                        fontsize=10.5, fontweight="bold",
                        color=txt_color, zorder=3)

                # Flag if below regulatory minimum
                if col in REG_MINS and val < REG_MINS[col]:
                    ax.text(cx + cell_w - 0.14, cy + 0.12, "⚠",
                            ha="center", va="bottom",
                            fontsize=8, color="#cc0000", zorder=4)
            else:
                ax.text(cx + cell_w / 2, cy + cell_h / 2, "N/A",
                        ha="center", va="center",
                        fontsize=9, color="#aaaaaa", zorder=3)

    # ── Grid lines between rows/cols ─────────────────────────────────────────
    for j in range(n_metrics + 1):
        lx = left_pad + j * cell_w
        ax.plot([lx, lx],
                [fig_h - top_pad, fig_h - top_pad - n_funds * cell_h],
                color="#dddddd", linewidth=0.5, zorder=1)
    for i in range(n_funds + 1):
        ly = fig_h - top_pad - i * cell_h
        ax.plot([left_pad, left_pad + n_metrics * cell_w],
                [ly, ly], color="#dddddd", linewidth=0.5, zorder=1)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_y = 0.18
    ax.text(left_pad, legend_y,
            "Color scale: per-column relative ranking    "
            "⚠ = below regulatory minimum",
            ha="left", va="bottom", fontsize=7.5, color="#666666", style="italic")

    plt.tight_layout(pad=0.3)
    path = save_fig(fig, out_dir, "heatmap_comparison.png")
    return path


def main():
    p = base_parser("Cross-fund metric heatmap for latest reporting month")
    args = p.parse_args()
    out_dir = ensure_out(args.out)

    print(f"Loading data from {args.db}...")
    series, holdings, _, latest_per_ticker = load_data(args.db, args.days)
    tbl = build_heatmap_table(series, holdings, latest_per_ticker)

    print(f"Building heatmap for {tbl['report_date'].iloc[0].strftime('%b %Y')}...")
    path = make_heatmap(tbl, out_dir)
    report_png(path)
    print(f"\n✓ Heatmap saved to {path}")


if __name__ == "__main__":
    main()
