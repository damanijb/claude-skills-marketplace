#!/usr/bin/env python3
"""
fund_deep_dive.py — Full per-fund analysis: composition, maturity, AUM flow, liquidity, HHI.
Produces 5 charts per fund (or for a specific fund via --ticker).

Usage:
    python3 fund_deep_dive.py [--db PATH] [--out DIR] [--days N] [--ticker FRGXX]

Prints PNG:<path> for each chart saved.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from chart_utils import (
    base_parser, ensure_out, report_png, load_data,
    apply_clean_style, save_fig, get_dw, dw_stacked_bar, dw_line_chart,
    FUND_COLORS, TICKERS, BUCKET_ORDER, BUCKET_COLORS, CAT_COLORS,
)


# ── DW Helpers ─────────────────────────────────────────────────────────────────

def build_stacked_pivot(df_grouped, date_col, cat_col, val_col, index_dates):
    """Build a stacked-bar DataFrame: rows=dates, cols=categories, values=pct."""
    pivot = df_grouped.pivot_table(
        index=date_col, columns=cat_col, values=val_col, aggfunc="sum"
    ).fillna(0)
    # Normalise to 100%
    pivot = pivot.div(pivot.sum(axis=1), axis=0) * 100
    pivot.index = pd.to_datetime(pivot.index).strftime("%Y-%m-%d")
    return pivot.reset_index().rename(columns={date_col: "Date"})


# ── Chart Builders ─────────────────────────────────────────────────────────────

def chart_composition(h, ticker, out_dir, dw):
    """(A) Portfolio composition by category — stacked bar."""
    comp = (
        h.groupby(["report_date", "simple_cat"])["value_excl_sponsor"]
        .sum().reset_index()
    )
    totals = comp.groupby("report_date")["value_excl_sponsor"].sum().rename("total")
    comp = comp.join(totals, on="report_date")
    comp["pct"] = comp["value_excl_sponsor"] / comp["total"] * 100

    if dw:
        pivot = (
            comp.pivot_table(index="report_date", columns="simple_cat", values="pct")
            .fillna(0)
        )
        pivot.index = pivot.index.strftime("%Y-%m-%d")
        pivot = pivot.reset_index().rename(columns={"report_date": "Date"})
        path = dw_stacked_bar(
            dw=dw,
            title=f"{ticker} — Portfolio Composition by Category",
            data=pivot,
            intro="% of portfolio in each investment category over the past 12 months.",
            custom_colors=CAT_COLORS,
            out_dir=out_dir,
            filename=f"{ticker}_composition.png",
        )
        if path:
            return path

    # Matplotlib fallback
    months = sorted(comp["report_date"].unique())
    x_pos = np.arange(len(months))
    month_labels = [pd.Timestamp(m).strftime("%b %Y") for m in months]
    all_cats = sorted(comp["simple_cat"].dropna().unique())

    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor("white")
    apply_clean_style(ax)
    bottom = np.zeros(len(months))

    for cat in all_cats:
        sub = comp[comp["simple_cat"] == cat].set_index("report_date")
        vals = np.array([sub.loc[m, "pct"] if m in sub.index else 0.0 for m in months])
        color = CAT_COLORS.get(cat, "#999999")
        bars = ax.bar(x_pos, vals, bottom=bottom, label=cat, color=color,
                      width=0.75, edgecolor="white", linewidth=0.4)
        for bar, val, bot in zip(bars, vals, bottom):
            if val > 7:
                ax.text(bar.get_x() + bar.get_width() / 2, bot + val / 2,
                        f"{val:.0f}%", ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold")
        bottom += vals

    ax.set_title(f"{ticker} — Portfolio Composition by Category", fontweight="bold", fontsize=13)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(month_labels, rotation=35, ha="right", fontsize=8.5)
    ax.set_ylabel("% of Portfolio", fontsize=10)
    ax.set_ylim(0, 108)
    ax.legend(fontsize=8, loc="upper right", ncol=2, framealpha=0.9)
    plt.tight_layout()
    return save_fig(fig, out_dir, f"{ticker}_composition.png")


def chart_maturity_buckets(h, ticker, out_dir, dw):
    """(C) Maturity bucket distribution — stacked bar."""
    bkt = (
        h.groupby(["report_date", "mat_bucket"])["value_excl_sponsor"]
        .sum().reset_index()
    )
    totals = bkt.groupby("report_date")["value_excl_sponsor"].sum().rename("total")
    bkt = bkt.join(totals, on="report_date")
    bkt["pct"] = bkt["value_excl_sponsor"] / bkt["total"] * 100

    if dw:
        pivot = (
            bkt.pivot_table(index="report_date", columns="mat_bucket", values="pct")
            .fillna(0)
            .reindex(columns=BUCKET_ORDER, fill_value=0)
        )
        pivot.index = pivot.index.strftime("%Y-%m-%d")
        pivot = pivot.reset_index().rename(columns={"report_date": "Date"})
        path = dw_stacked_bar(
            dw=dw,
            title=f"{ticker} — Maturity Bucket Distribution (WAL)",
            data=pivot,
            intro="% of portfolio by WAL maturity bucket over the past 12 months.",
            custom_colors=BUCKET_COLORS,
            out_dir=out_dir,
            filename=f"{ticker}_maturity_buckets.png",
        )
        if path:
            return path

    # Matplotlib fallback
    months = sorted(bkt["report_date"].unique())
    x_pos = np.arange(len(months))
    month_labels = [pd.Timestamp(m).strftime("%b %Y") for m in months]

    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor("white")
    apply_clean_style(ax)
    bottom = np.zeros(len(months))

    for bkt_name in BUCKET_ORDER:
        sub = bkt[bkt["mat_bucket"] == bkt_name].set_index("report_date")
        vals = np.array([sub.loc[m, "pct"] if m in sub.index else 0.0 for m in months])
        bars = ax.bar(x_pos, vals, bottom=bottom, label=bkt_name,
                      color=BUCKET_COLORS[bkt_name], width=0.75, edgecolor="white", linewidth=0.4)
        for bar, val, bot in zip(bars, vals, bottom):
            if val > 7:
                ax.text(bar.get_x() + bar.get_width() / 2, bot + val / 2,
                        f"{val:.0f}%", ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold")
        bottom += vals

    ax.set_title(f"{ticker} — Maturity Bucket Distribution (WAL)", fontweight="bold", fontsize=13)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(month_labels, rotation=35, ha="right", fontsize=8.5)
    ax.set_ylabel("% of Portfolio", fontsize=10)
    ax.set_ylim(0, 108)
    ax.legend(fontsize=8, loc="upper right", ncol=3, framealpha=0.9)
    plt.tight_layout()
    return save_fig(fig, out_dir, f"{ticker}_maturity_buckets.png")


def chart_aum_flow(s, ticker, out_dir, dw):
    """(B) AUM trend with MoM change bars."""
    s2 = s.sort_values("report_date").copy().reset_index(drop=True)
    s2["mom_change"] = s2["aum_B"].diff()

    if dw:
        df_dw = s2[["report_date", "aum_B"]].copy()
        df_dw["report_date"] = df_dw["report_date"].dt.strftime("%Y-%m-%d")
        df_dw = df_dw.rename(columns={"report_date": "Date", "aum_B": "AUM ($B)"})
        path = dw_line_chart(
            dw=dw,
            title=f"{ticker} — AUM Trend",
            data=df_dw,
            intro="Monthly AUM in billions over the past 12 months.",
            custom_colors={"AUM ($B)": FUND_COLORS[ticker]},
            out_dir=out_dir,
            filename=f"{ticker}_aum_flow.png",
        )
        if path:
            return path

    # Matplotlib fallback — dual-axis
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")
    apply_clean_style(ax)
    ax2 = ax.twinx()
    ax2.set_facecolor("white")
    ax2.grid(False)

    bar_cols = ["#2ca02c" if v >= 0 else "#d62728" for v in s2["mom_change"].fillna(0)]
    ax.bar(s2["report_date"], s2["mom_change"].fillna(0),
           color=bar_cols, width=20, alpha=0.75, label="MoM Change ($B)")
    ax2.plot(s2["report_date"], s2["aum_B"],
             color=FUND_COLORS[ticker], linewidth=2.5, marker="o", markersize=5, label="AUM ($B)")

    for _, row in s2.dropna(subset=["aum_B"]).iterrows():
        ax2.annotate(f"${row['aum_B']:.1f}B",
                     xy=(row["report_date"], row["aum_B"]),
                     xytext=(0, 7), textcoords="offset points",
                     fontsize=7.5, color=FUND_COLORS[ticker], ha="center")

    ax.set_title(f"{ticker} — AUM & Monthly Flow", fontweight="bold", fontsize=13)
    ax.set_ylabel("MoM Change ($B)", fontsize=10)
    ax2.set_ylabel("AUM ($B)", color=FUND_COLORS[ticker], fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha="right", fontsize=8.5)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="upper left")
    plt.tight_layout()
    return save_fig(fig, out_dir, f"{ticker}_aum_flow.png")


def chart_liquidity(h, ticker, out_dir, dw):
    """(D) Daily and weekly liquidity ratios with regulatory minimums."""
    liq = h.copy()
    liq["daily_val"]  = liq["value_excl_sponsor"].where(liq["daily_liquid"]  == "Y", 0)
    liq["weekly_val"] = liq["value_excl_sponsor"].where(liq["weekly_liquid"] == "Y", 0)
    agg = liq.groupby("report_date").agg(
        daily_sum=("daily_val",  "sum"),
        weekly_sum=("weekly_val", "sum"),
        nav=("net_asset_of_series", "first")
    ).reset_index()
    agg["daily_pct"]  = agg["daily_sum"]  / agg["nav"] * 100
    agg["weekly_pct"] = agg["weekly_sum"] / agg["nav"] * 100

    if dw:
        df_dw = agg[["report_date", "daily_pct", "weekly_pct"]].copy()
        df_dw["report_date"] = df_dw["report_date"].dt.strftime("%Y-%m-%d")
        df_dw = df_dw.rename(columns={
            "report_date": "Date",
            "daily_pct":   "Daily Liquid %",
            "weekly_pct":  "Weekly Liquid %",
        })
        path = dw_line_chart(
            dw=dw,
            title=f"{ticker} — Liquidity Ratios",
            data=df_dw,
            intro="Daily and weekly liquidity as % of NAV. Regulatory minimums: 10% daily, 30% weekly.",
            custom_colors={"Daily Liquid %": "#2ca02c", "Weekly Liquid %": "#1f77b4"},
            out_dir=out_dir,
            filename=f"{ticker}_liquidity.png",
        )
        if path:
            return path

    # Matplotlib fallback
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")
    apply_clean_style(ax)

    ax.plot(agg["report_date"], agg["daily_pct"],
            color="#2ca02c", marker="o", markersize=5, linewidth=2.5, label="Daily Liquid %")
    ax.plot(agg["report_date"], agg["weekly_pct"],
            color="#1f77b4", marker="s", markersize=5, linewidth=2.5, label="Weekly Liquid %")

    for _, row in agg.iterrows():
        ax.text(row["report_date"], row["daily_pct"]  + 0.8, f"{row['daily_pct']:.0f}",
                ha="center", fontsize=6.5, color="#2ca02c")
        ax.text(row["report_date"], row["weekly_pct"] + 0.8, f"{row['weekly_pct']:.0f}",
                ha="center", fontsize=6.5, color="#1f77b4")

    ax.axhline(10, color="#ff7f0e", linestyle="--", linewidth=1.5, alpha=0.9, label="10% daily min")
    ax.axhline(30, color="#d62728", linestyle="--", linewidth=1.5, alpha=0.9, label="30% weekly min")

    ax.set_title(f"{ticker} — Liquidity Ratios", fontweight="bold", fontsize=13)
    ax.set_ylabel("% of Net Assets", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha="right")
    ax.legend(fontsize=9, loc="lower right")
    ax.set_ylim(0, max(agg["weekly_pct"].max() * 1.18, 45))
    plt.tight_layout()
    return save_fig(fig, out_dir, f"{ticker}_liquidity.png")


def chart_hhi(h, ticker, out_dir, dw):
    """(F) Issuer concentration (HHI) over time."""
    months = sorted(h["report_date"].unique())
    hhi_rows = []
    for dt in months:
        m = h[h["report_date"] == dt]
        nav = m["net_asset_of_series"].iloc[0] if len(m) > 0 else None
        if nav and nav > 0:
            issuer_pct = m.groupby("name_of_issuer")["value_excl_sponsor"].sum() / nav * 100
            hhi = (issuer_pct ** 2).sum()
            hhi_rows.append({"report_date": dt, "HHI": hhi})
    hhi_df = pd.DataFrame(hhi_rows)

    if dw:
        df_dw = hhi_df.copy()
        df_dw["report_date"] = pd.to_datetime(df_dw["report_date"]).dt.strftime("%Y-%m-%d")
        df_dw = df_dw.rename(columns={"report_date": "Date"})
        path = dw_line_chart(
            dw=dw,
            title=f"{ticker} — Issuer Concentration (HHI)",
            data=df_dw,
            intro="Herfindahl-Hirschman Index: <1500 competitive, 1500-2500 moderate, >2500 concentrated.",
            custom_colors={"HHI": FUND_COLORS[ticker]},
            out_dir=out_dir,
            filename=f"{ticker}_hhi.png",
        )
        if path:
            return path

    # Matplotlib fallback
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")
    apply_clean_style(ax)

    hhi_df["report_date"] = pd.to_datetime(hhi_df["report_date"])
    ax.fill_between(hhi_df["report_date"], hhi_df["HHI"], alpha=0.12, color=FUND_COLORS[ticker])
    ax.plot(hhi_df["report_date"], hhi_df["HHI"],
            color=FUND_COLORS[ticker], linewidth=2.5, marker="o", markersize=5)

    for _, row in hhi_df.iterrows():
        ax.text(row["report_date"], row["HHI"] + 30, f"{row['HHI']:.0f}",
                ha="center", fontsize=6.5, color=FUND_COLORS[ticker])

    ax.axhline(1500, color="#ff7f0e", linestyle="--", linewidth=1.5, label="Moderate (1500)")
    ax.axhline(2500, color="#d62728", linestyle="--", linewidth=1.5, label="High (2500)")
    ax.axhspan(0,    1500, alpha=0.03, color="green")
    ax.axhspan(1500, 2500, alpha=0.03, color="orange")
    ax.axhspan(2500, 6000, alpha=0.03, color="red")

    ax.set_title(f"{ticker} — Issuer Concentration (HHI)", fontweight="bold", fontsize=13)
    ax.set_ylabel("HHI", fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha="right")
    ax.legend(fontsize=9)
    ax.set_ylim(0, max(hhi_df["HHI"].max() * 1.25, 3000))
    plt.tight_layout()
    return save_fig(fig, out_dir, f"{ticker}_hhi.png")


def run_fund(ticker, series, holdings, latest_per_ticker, out_dir, dw):
    """Run all 5 deep-dive charts for one fund. Returns list of PNG paths."""
    s = series[series["ticker"] == ticker].sort_values("report_date")
    h = holdings[holdings["ticker"] == ticker].copy()
    if s.empty or h.empty:
        print(f"No data found for {ticker}", file=sys.stderr)
        return []

    print(f"\n── {ticker} ──")
    paths = []

    print("  Composition chart...")
    p = chart_composition(h, ticker, out_dir, dw)
    if p: paths.append(p)

    print("  Maturity buckets chart...")
    p = chart_maturity_buckets(h, ticker, out_dir, dw)
    if p: paths.append(p)

    print("  AUM flow chart...")
    p = chart_aum_flow(s, ticker, out_dir, dw)
    if p: paths.append(p)

    print("  Liquidity chart...")
    p = chart_liquidity(h, ticker, out_dir, dw)
    if p: paths.append(p)

    print("  HHI concentration chart...")
    p = chart_hhi(h, ticker, out_dir, dw)
    if p: paths.append(p)

    return paths


def main():
    p = base_parser("Per-fund deep dive: composition, maturity, flow, liquidity, HHI")
    p.add_argument("--ticker", default=None,
                   help="Single fund ticker (FRGXX/GOFXX/MVRXX/BGSXX). Default: all 4.")
    args = p.parse_args()
    out_dir = ensure_out(args.out)

    print(f"Loading data from {args.db}...")
    series, holdings, _, latest_per_ticker = load_data(args.db, args.days)

    tickers_to_run = [args.ticker] if args.ticker else TICKERS
    dw = get_dw()
    if dw:
        print("Datawrapper available.")

    all_paths = []
    for ticker in tickers_to_run:
        paths = run_fund(ticker, series, holdings, latest_per_ticker, out_dir, dw)
        all_paths.extend(paths)

    for pp in all_paths:
        report_png(pp)

    print(f"\n✓ {len(all_paths)} deep-dive chart(s) saved to {args.out}")


if __name__ == "__main__":
    main()
