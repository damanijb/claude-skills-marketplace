"""
Chart generation engine for Bloomberg data.

Supports matplotlib (static PNG) and altair (interactive HTML) charts.
Professional financial color palette with minimal chrome.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

# Professional muted palette for financial charts
PALETTE = [
    "#1e3a5f",  # primary — navy
    "#3b6fa0",  # secondary — steel blue
    "#c05746",  # accent — burnt sienna
    "#5b8c5a",  # tertiary — sage
    "#9b7a3c",  # fourth — gold
    "#6b5b8a",  # fifth — purple
]

_CHART_DIR = Path(tempfile.gettempdir()) / "bloomberg_charts"


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


def _timestamp_name(prefix: str, ext: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.{ext}"


def _records_to_dataframe(data_json: list[dict]) -> Any:
    """Convert JSON records to a pandas DataFrame."""
    import pandas as pd

    df = pd.DataFrame(data_json)
    for col in df.columns:
        if any(hint in col.lower() for hint in ("date", "time", "dt")):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
    return df


def _auto_detect_columns(
    df: Any,
    x_col: str | None,
    y_cols: list[str] | None,
) -> tuple[str, list[str]]:
    """Auto-detect date column for x and numeric columns for y."""
    import pandas as pd

    if x_col and y_cols:
        return x_col, y_cols

    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    if not x_col:
        x_col = date_cols[0] if date_cols else (df.columns[0] if len(df.columns) > 0 else "index")

    if not y_cols:
        y_cols = [c for c in numeric_cols if c != x_col]
        if not y_cols and numeric_cols:
            y_cols = numeric_cols[:3]

    return x_col, y_cols or []


# ======================================================================
# matplotlib renderers
# ======================================================================

def _mpl_setup():
    """Configure matplotlib with professional defaults."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Helvetica Neue", "Arial", "sans-serif"],
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#d1d5db",
        "axes.labelcolor": "#374151",
        "xtick.color": "#6b7280",
        "ytick.color": "#6b7280",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "figure.dpi": 150,
    })
    return plt


def _mpl_timeseries(df, x_col, y_cols, title, **kwargs):
    plt = _mpl_setup()
    import matplotlib.dates as mdates
    from matplotlib.ticker import FuncFormatter

    fig, ax = plt.subplots(figsize=(10, 5.5))

    for i, col in enumerate(y_cols):
        ax.plot(df[x_col], df[col], color=PALETTE[i % len(PALETTE)], linewidth=1.8, label=col)
        last_val = df[col].dropna().iloc[-1] if not df[col].dropna().empty else None
        if last_val is not None:
            last_x = df.loc[df[col].notna(), x_col].iloc[-1]
            ax.annotate(
                f"{last_val:,.2f}", xy=(last_x, last_val),
                xytext=(8, 0), textcoords="offset points",
                fontsize=10, fontweight="600", color=PALETTE[i % len(PALETTE)], va="center",
            )

    ax.set_title(title, fontsize=16, fontweight="600", loc="left", pad=20)
    try:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    except Exception:
        pass
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.2f}"))
    if len(y_cols) > 1:
        ax.legend(frameon=False, fontsize=10, loc="upper left")
    fig.text(0.12, 0.01, "Source: Bloomberg", fontsize=8, color="#9ca3af")
    plt.tight_layout()
    return fig


def _mpl_bar(df, x_col, y_cols, title, **kwargs):
    plt = _mpl_setup()

    value_col = y_cols[0] if y_cols else df.select_dtypes("number").columns[0]
    df_sorted = df.sort_values(value_col, ascending=True).tail(20)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df_sorted[x_col].astype(str), df_sorted[value_col], color=PALETTE[0], height=0.65)

    max_val = df_sorted[value_col].max()
    for bar in bars:
        w = bar.get_width()
        ax.text(
            w + max_val * 0.015, bar.get_y() + bar.get_height() / 2,
            f"{w:,.2f}", va="center", fontsize=9, color="#374151",
        )

    ax.set_title(title, fontsize=16, fontweight="600", loc="left", pad=20)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(left=False, labelsize=10)
    fig.text(0.12, 0.01, "Source: Bloomberg", fontsize=8, color="#9ca3af")
    plt.tight_layout()
    return fig


def _mpl_scatter(df, x_col, y_cols, title, **kwargs):
    plt = _mpl_setup()

    y_col = y_cols[0] if y_cols else df.select_dtypes("number").columns[1]
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.scatter(df[x_col], df[y_col], s=50, color=PALETTE[0], alpha=0.7, edgecolors="none")
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_ylabel(y_col, fontsize=11)
    ax.set_title(title, fontsize=16, fontweight="600", loc="left", pad=20)
    fig.text(0.12, 0.01, "Source: Bloomberg", fontsize=8, color="#9ca3af")
    plt.tight_layout()
    return fig


def _mpl_heatmap(df, x_col, y_cols, title, **kwargs):
    plt = _mpl_setup()
    import numpy as np

    numeric = df.select_dtypes("number")
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(numeric.values, cmap="RdYlBu_r", aspect="auto")
    ax.set_xticks(range(len(numeric.columns)))
    ax.set_yticks(range(len(numeric.index)))
    ax.set_xticklabels(numeric.columns, fontsize=9, rotation=45, ha="right")
    ax.set_yticklabels(numeric.index, fontsize=9)
    for i in range(numeric.shape[0]):
        for j in range(numeric.shape[1]):
            val = numeric.values[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8)
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(title, fontsize=16, fontweight="600", loc="left", pad=16)
    fig.text(0.12, 0.01, "Source: Bloomberg", fontsize=8, color="#9ca3af")
    plt.tight_layout()
    return fig


def _mpl_multipanel(df, x_col, y_cols, title, **kwargs):
    plt = _mpl_setup()
    import matplotlib.dates as mdates
    from matplotlib.ticker import FuncFormatter

    n_panels = min(len(y_cols), 4)
    fig, axes = plt.subplots(n_panels, 1, figsize=(10, 3 * n_panels + 1), sharex=True)
    if n_panels == 1:
        axes = [axes]

    for i, col in enumerate(y_cols[:n_panels]):
        axes[i].plot(df[x_col], df[col], color=PALETTE[i % len(PALETTE)], linewidth=1.8)
        axes[i].set_ylabel(col, fontsize=10)
        axes[i].spines[["top", "right"]].set_visible(False)

    axes[0].set_title(title, fontsize=16, fontweight="600", loc="left", pad=16)
    try:
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    except Exception:
        pass
    fig.text(0.12, 0.01, "Source: Bloomberg", fontsize=8, color="#9ca3af")
    plt.tight_layout()
    return fig


_MPL_RENDERERS = {
    "timeseries": _mpl_timeseries,
    "bar": _mpl_bar,
    "scatter": _mpl_scatter,
    "heatmap": _mpl_heatmap,
    "multipanel": _mpl_multipanel,
}


# ======================================================================
# Altair renderers
# ======================================================================

def _altair_timeseries(df, x_col, y_cols, title, **kwargs):
    import altair as alt
    import pandas as pd

    palette = PALETTE[: len(y_cols)]

    if len(y_cols) > 1:
        df_long = df.melt(id_vars=[x_col], value_vars=y_cols, var_name="series", value_name="value")
        color_enc = alt.Color("series:N", scale=alt.Scale(range=palette), legend=alt.Legend(title=None, orient="top"))
    else:
        df_long = df[[x_col, y_cols[0]]].rename(columns={y_cols[0]: "value"})
        df_long["series"] = y_cols[0]
        color_enc = alt.value(PALETTE[0])

    x_type = "T" if pd.api.types.is_datetime64_any_dtype(df[x_col]) else "Q"

    line = (
        alt.Chart(df_long)
        .mark_line(strokeWidth=2)
        .encode(
            x=alt.X(f"{x_col}:{x_type}", title=None),
            y=alt.Y("value:Q", title="Value"),
            color=color_enc,
        )
    )

    chart = (
        line
        .properties(title=alt.Title(title, subtitle="Source: Bloomberg"), width=700, height=380)
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domainColor="#d1d5db", labelColor="#6b7280", titleColor="#374151")
        .configure_title(anchor="start", fontSize=16, fontWeight="bold", subtitleColor="#6b7280")
    )
    return chart


def _altair_bar(df, x_col, y_cols, title, **kwargs):
    import altair as alt

    value_col = y_cols[0] if y_cols else df.select_dtypes("number").columns[0]
    df_sorted = df.sort_values(value_col, ascending=False).head(20)

    chart = (
        alt.Chart(df_sorted)
        .mark_bar(color=PALETTE[0], cornerRadiusEnd=3)
        .encode(
            x=alt.X(f"{value_col}:Q", title=value_col),
            y=alt.Y(f"{x_col}:N", title=None, sort=alt.EncodingSortField(field=value_col, order="descending")),
            tooltip=[alt.Tooltip(f"{x_col}:N"), alt.Tooltip(f"{value_col}:Q", format=",.2f")],
        )
        .properties(title=alt.Title(title, subtitle="Source: Bloomberg"), width=600, height=alt.Step(22))
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domainColor="#d1d5db", labelColor="#6b7280", titleColor="#374151")
        .configure_title(anchor="start", fontSize=16, fontWeight="bold", subtitleColor="#6b7280")
    )
    return chart


def _altair_scatter(df, x_col, y_cols, title, **kwargs):
    import altair as alt

    y_col = y_cols[0] if y_cols else df.select_dtypes("number").columns[1]

    chart = (
        alt.Chart(df)
        .mark_circle(opacity=0.7, color=PALETTE[0])
        .encode(
            x=alt.X(f"{x_col}:Q", title=x_col),
            y=alt.Y(f"{y_col}:Q", title=y_col),
            tooltip=list(df.columns[:5]),
        )
        .properties(title=alt.Title(title, subtitle="Source: Bloomberg"), width=700, height=420)
        .interactive()
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domainColor="#d1d5db", labelColor="#6b7280", titleColor="#374151")
        .configure_title(anchor="start", fontSize=16, fontWeight="bold", subtitleColor="#6b7280")
    )
    return chart


def _altair_facet(df, x_col, y_cols, title, **kwargs):
    import altair as alt
    import pandas as pd

    value_col = y_cols[0] if y_cols else df.select_dtypes("number").columns[0]
    cat_cols = [c for c in df.columns if c not in [x_col, value_col] and df[c].dtype == "object"]
    facet_col = cat_cols[0] if cat_cols else df.columns[0]

    x_type = "T" if pd.api.types.is_datetime64_any_dtype(df[x_col]) else "Q"

    chart = (
        alt.Chart(df)
        .mark_line(strokeWidth=1.5, color=PALETTE[0])
        .encode(
            x=alt.X(f"{x_col}:{x_type}", title=None),
            y=alt.Y(f"{value_col}:Q", title=None),
        )
        .properties(width=180, height=120)
        .facet(facet=alt.Facet(f"{facet_col}:N", title=None), columns=3)
        .resolve_scale(y="independent")
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False, domainColor="#d1d5db", labelColor="#6b7280")
        .properties(title=alt.Title(title, subtitle="Source: Bloomberg"))
        .configure_title(anchor="start", fontSize=16, fontWeight="bold", subtitleColor="#6b7280")
    )
    return chart


_ALTAIR_RENDERERS = {
    "timeseries": _altair_timeseries,
    "bar": _altair_bar,
    "scatter": _altair_scatter,
    "facet": _altair_facet,
}


# ======================================================================
# Public API
# ======================================================================

def generate_chart(
    chart_type: str,
    library: str,
    data_json: list[dict],
    title: str = "Bloomberg Data",
    x_col: str | None = None,
    y_cols: list[str] | None = None,
) -> dict[str, Any]:
    """Generate a chart and save to temp directory."""
    chart_dir = _ensure_chart_dir()
    df = _records_to_dataframe(data_json)
    x_col, y_cols = _auto_detect_columns(df, x_col, y_cols)

    if library == "matplotlib":
        renderer = _MPL_RENDERERS.get(chart_type)
        if not renderer:
            avail = ", ".join(_MPL_RENDERERS.keys())
            return {"error": f"Unknown chart type '{chart_type}' for matplotlib. Available: {avail}"}

        fig = renderer(df, x_col, y_cols, title)
        out_path = chart_dir / _timestamp_name(chart_type, "png")
        fig.savefig(str(out_path), dpi=200, bbox_inches="tight")
        import matplotlib.pyplot as plt
        plt.close(fig)

        return {"file_path": str(out_path), "chart_type": chart_type, "library": "matplotlib"}

    elif library == "altair":
        renderer = _ALTAIR_RENDERERS.get(chart_type)
        if not renderer:
            avail = ", ".join(_ALTAIR_RENDERERS.keys())
            return {"error": f"Unknown chart type '{chart_type}' for altair. Available: {avail}"}

        chart = renderer(df, x_col, y_cols, title)
        out_path = chart_dir / _timestamp_name(chart_type, "html")
        chart.save(str(out_path))

        return {"file_path": str(out_path), "chart_type": chart_type, "library": "altair"}

    else:
        return {"error": f"Unknown library '{library}'. Use 'matplotlib' or 'altair'."}
