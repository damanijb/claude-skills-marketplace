"""Seaborn/Matplotlib chart renderer — generates static PNG charts as base64 HTML img tags.

All chart functions return an HTML string: <img src="data:image/png;base64,...">
Style: white background, no gridlines, minimal axis labels, brand colors.
"""

import io
import base64
from typing import List, Optional, Tuple, Union

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# San Bernardino County ATC brand palette — vibrant, high-contrast
BRAND_COLORS = [
    '#003366',  # County Navy (primary)
    '#FFB703',  # County Gold (accent)
    '#E97007',  # County Orange
    '#0693E3',  # Cyan Blue
    '#00D084',  # Green Cyan
    '#9B51E0',  # Vivid Purple
    '#7CC6DD',  # Secondary Blue
    '#C00000',  # Red
]

DOUGHNUT_COLORS = [
    '#003366', '#0693E3', '#7CC6DD', '#FFB703',
    '#E97007', '#00D084', '#9B51E0', '#C00000',
    '#3b5ea1', '#f59e42', '#2ea87e', '#7c3aed',
]

DPI = 150
FONT_FAMILY = 'Segoe UI'


def _setup_style():
    """Configure matplotlib/seaborn for clean, minimal charts."""
    if HAS_SEABORN:
        sns.set_style("white")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': [FONT_FAMILY, 'Helvetica Neue', 'Arial', 'sans-serif'],
        'font.size': 10,
        'axes.edgecolor': '#cccccc',
        'axes.linewidth': 0.5,
        'xtick.color': '#666666',
        'ytick.color': '#666666',
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.grid': False,
    })


def _to_bytes(fig, tight: bool = True) -> io.BytesIO:
    """Render figure to PNG BytesIO (for ReportLab)."""
    buf = io.BytesIO()
    if tight:
        fig.savefig(buf, format='png', dpi=DPI, bbox_inches='tight',
                    facecolor='white', edgecolor='none', pad_inches=0.15)
    else:
        fig.savefig(buf, format='png', dpi=DPI,
                    facecolor='white', edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    return buf


def _to_base64(fig, tight: bool = True) -> str:
    """Render figure to base64-encoded PNG data URI, then close figure."""
    buf = io.BytesIO()
    if tight:
        fig.savefig(buf, format='png', dpi=DPI, bbox_inches='tight',
                    facecolor='white', edgecolor='none', pad_inches=0.15)
    else:
        fig.savefig(buf, format='png', dpi=DPI,
                    facecolor='white', edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{b64}" style="width:100%; height:auto;">'


def _despine(ax):
    """Remove top and right spines."""
    if HAS_SEABORN:
        sns.despine(ax=ax)
    else:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


def _simplify_date_label(label: str) -> str:
    """Convert date labels like '2024-01-01' to shorter forms."""
    if len(label) == 10 and label[4] == '-':
        # YYYY-MM-DD → Mon 'YY  or just 'YY for Jan
        parts = label.split('-')
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        try:
            m = int(parts[1]) - 1
            return f"{months[m]} '{parts[0][2:]}"
        except (ValueError, IndexError):
            pass
    return label


def _thin_x_labels(ax, labels, max_labels=8):
    """Show at most max_labels evenly spaced x-tick labels; never rotate."""
    n = len(labels)
    if n == 0:
        return
    # Simplify date-format labels
    simple = [_simplify_date_label(l) for l in labels]

    if n <= max_labels:
        ax.set_xticks(range(n))
        ax.set_xticklabels(simple, fontsize=8, rotation=0, ha='center')
        return
    # Show evenly spaced ticks — never rotate
    step = max(1, n // (max_labels - 1))
    visible = set(range(0, n, step))
    visible.add(n - 1)
    show_indices = sorted(visible)
    ax.set_xticks(show_indices)
    ax.set_xticklabels([simple[i] for i in show_indices], fontsize=8, rotation=0, ha='center')


def _auto_y_range(ax, values_list):
    """Set y-axis to data range with 5% padding instead of starting at 0."""
    all_vals = []
    for vals in values_list:
        all_vals.extend(v for v in vals if v is not None)
    if not all_vals:
        return
    lo, hi = min(all_vals), max(all_vals)
    spread = hi - lo
    if spread < 1e-10:
        spread = abs(lo) * 0.1 or 1.0
    pad = spread * 0.08
    ax.set_ylim(lo - pad, hi + pad)


def render_line_chart(
    series_list: List[List[float]],
    labels: List[str],
    series_names: Optional[List[str]] = None,
    title: str = '',
    y_label: str = '',
    colors: Optional[List[str]] = None,
    annotate_last: bool = True,
    fill_first: bool = False,
    figsize: Tuple[float, float] = (7, 3.5),
    point_markers: bool = False,
    y_auto_range: bool = True,
) -> str:
    """Render a line chart. series_list is a list of y-value lists."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)

    colors = colors or BRAND_COLORS
    series_names = series_names or [f'Series {i+1}' for i in range(len(series_list))]

    x = np.arange(len(labels))
    # Only fill for single-series charts
    do_fill = fill_first and len(series_list) == 1

    for i, values in enumerate(series_list):
        color = colors[i % len(colors)]
        marker = 'o' if point_markers else None
        markersize = 4 if point_markers else None
        ax.plot(x, values, color=color, linewidth=2.2, label=series_names[i],
                marker=marker, markersize=markersize, zorder=3)
        if do_fill and i == 0:
            ax.fill_between(x, values, alpha=0.06, color=color)

    # Annotate last values with vertical staggering to avoid overlap
    if annotate_last:
        endpoints = []
        for i, values in enumerate(series_list):
            if len(values) > 0:
                endpoints.append((values[-1], i, colors[i % len(colors)]))
        # Sort by value so we can stagger
        endpoints.sort(key=lambda t: t[0])
        prev_y = None
        for val, idx, color in endpoints:
            fmt = f'{val:.1f}' if abs(val) < 1000 else f'{val:,.0f}'
            # Stagger if too close to previous annotation
            y_offset = 0
            if prev_y is not None and abs(val - prev_y) < (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.04:
                y_offset = 10
            prev_y = val
            ax.annotate(fmt, xy=(x[-1], val),
                        xytext=(8, y_offset), textcoords='offset points',
                        fontsize=9, fontweight='bold', color=color,
                        va='center',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                                  edgecolor='none', alpha=0.8))

    if y_auto_range:
        _auto_y_range(ax, series_list)
    _thin_x_labels(ax, labels)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    if len(series_list) > 1:
        ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
                  edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _to_base64(fig)


def render_area_chart(
    series_list: List[List[float]],
    labels: List[str],
    series_names: Optional[List[str]] = None,
    title: str = '',
    y_label: str = '',
    colors: Optional[List[str]] = None,
    annotate_last: bool = True,
    figsize: Tuple[float, float] = (7, 3.5),
    y_auto_range: bool = True,
) -> str:
    """Line chart with subtle fill_between for each series."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)

    colors = colors or BRAND_COLORS
    series_names = series_names or [f'Series {i+1}' for i in range(len(series_list))]

    x = np.arange(len(labels))
    for i, values in enumerate(series_list):
        color = colors[i % len(colors)]
        ax.plot(x, values, color=color, linewidth=2.2, label=series_names[i], zorder=3)
        # Very subtle fill — only for single-series area charts
        if len(series_list) == 1:
            if y_auto_range and values:
                fill_base = min(values)
            else:
                fill_base = 0
            ax.fill_between(x, fill_base, values, alpha=0.06, color=color)
        if annotate_last and len(values) > 0:
            last_val = values[-1]
            fmt = f'{last_val:.1f}' if abs(last_val) < 1000 else f'{last_val:,.0f}'
            ax.annotate(fmt, xy=(x[-1], last_val),
                        xytext=(8, 0), textcoords='offset points',
                        fontsize=9, fontweight='bold', color=color, va='center',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                                  edgecolor='none', alpha=0.8))

    if y_auto_range:
        _auto_y_range(ax, series_list)
    _thin_x_labels(ax, labels)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    if len(series_list) > 1:
        ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
                  edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _to_base64(fig)


def render_bar_chart(
    categories: List[str],
    values: List[float],
    title: str = '',
    y_label: str = '',
    colors: Optional[Union[str, List[str]]] = None,
    horizontal: bool = False,
    data_labels: bool = True,
    data_label_fmt: str = '{:.1f}',
    figsize: Tuple[float, float] = (7, 3.5),
    bar_width: float = 0.65,
) -> str:
    """Render a single-series bar chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)

    if colors is None:
        colors = BRAND_COLORS[0]
    if isinstance(colors, list) and len(colors) == len(categories):
        bar_colors = colors
    else:
        bar_colors = colors if isinstance(colors, str) else colors[0]

    # Auto-suppress data labels when too many bars (>12)
    if data_labels and len(categories) > 12:
        data_labels = False

    x = np.arange(len(categories))
    if horizontal:
        bars = ax.barh(x, values, height=bar_width, color=bar_colors,
                       edgecolor='none', zorder=3)
        ax.set_yticks(x)
        ax.set_yticklabels(categories, fontsize=9)
        if data_labels:
            for bar, val in zip(bars, values):
                fmt = data_label_fmt.format(val)
                ax.text(bar.get_width() + max(abs(v) for v in values) * 0.02,
                        bar.get_y() + bar.get_height() / 2,
                        fmt, va='center', fontsize=8, fontweight='bold', color='#555')
        if y_label:
            ax.set_xlabel(y_label, fontsize=9, color='#666')
    else:
        bars = ax.bar(x, values, width=bar_width, color=bar_colors,
                      edgecolor='none', zorder=3, clip_on=False)
        _thin_x_labels(ax, categories)
        if data_labels:
            for bar, val in zip(bars, values):
                fmt = data_label_fmt.format(val)
                y_pos = bar.get_height() if val >= 0 else bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                        fmt, ha='center', va='bottom', fontsize=7,
                        fontweight='bold', color='#555')
        if y_label:
            ax.set_ylabel(y_label, fontsize=9, color='#666')

    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    if not horizontal:
        ax.set_xlim(-0.5, len(categories) - 0.5)

    return _to_base64(fig)


def render_grouped_bar(
    categories: List[str],
    groups: List[List[float]],
    group_labels: List[str],
    colors: Optional[List[str]] = None,
    title: str = '',
    y_label: str = '',
    data_labels: bool = False,
    figsize: Tuple[float, float] = (7, 3.5),
) -> str:
    """Render a grouped bar chart. groups[i] = values for group i."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)

    colors = colors or BRAND_COLORS
    n_groups = len(groups)
    bar_width = 0.7 / n_groups
    x = np.arange(len(categories))

    for i, (vals, label) in enumerate(zip(groups, group_labels)):
        offset = (i - n_groups / 2 + 0.5) * bar_width
        color = colors[i % len(colors)]
        bars = ax.bar(x + offset, vals, width=bar_width, label=label,
                      color=color, edgecolor='none', zorder=3)
        if data_labels:
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        f'{val:.2f}', ha='center', va='bottom', fontsize=7,
                        fontweight='bold', color='#555')

    _thin_x_labels(ax, categories)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _to_base64(fig)


def render_stacked_bar(
    categories: List[str],
    groups: List[List[float]],
    group_labels: List[str],
    colors: Optional[List[str]] = None,
    title: str = '',
    y_label: str = '',
    figsize: Tuple[float, float] = (7, 3.5),
) -> str:
    """Render a stacked bar chart. groups[i] = values for stack layer i."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)

    colors = colors or BRAND_COLORS
    x = np.arange(len(categories))
    bottom = np.zeros(len(categories))

    for i, (vals, label) in enumerate(zip(groups, group_labels)):
        color = colors[i % len(colors)]
        vals_arr = np.array(vals)
        ax.bar(x, vals_arr, width=0.6, bottom=bottom, label=label,
               color=color, edgecolor='none', zorder=3)
        bottom += vals_arr

    _thin_x_labels(ax, categories)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _to_base64(fig)


def render_doughnut(
    labels: List[str],
    values: List[float],
    colors: Optional[List[str]] = None,
    center_text: Optional[str] = None,
    title: str = '',
    figsize: Tuple[float, float] = (5, 5),
    show_pct_labels: bool = True,
    pct_threshold: float = 3.0,
) -> str:
    """Render a doughnut (ring) chart using matplotlib pie with wedgeprops."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)

    colors = colors or DOUGHNUT_COLORS
    chart_colors = [colors[i % len(colors)] for i in range(len(values))]

    def autopct_func(pct):
        if show_pct_labels and pct >= pct_threshold:
            return f'{pct:.1f}%'
        return ''

    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=chart_colors, autopct=autopct_func,
        startangle=90, pctdistance=0.82,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight('bold')
        at.set_color('#555')

    if center_text:
        ax.text(0, 0, center_text, ha='center', va='center',
                fontsize=18, fontweight='bold', color='#2d3748')

    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8)

    ax.set_aspect('equal')

    return _to_base64(fig)


def render_dual_axis(
    series1: List[float],
    series2: List[float],
    labels: List[str],
    name1: str = 'Series 1',
    name2: str = 'Series 2',
    y1_label: str = '',
    y2_label: str = '',
    color1: str = '#003366',
    color2: str = '#7CC6DD',
    title: str = '',
    figsize: Tuple[float, float] = (7, 3.5),
) -> str:
    """Line on left axis, bar on right axis."""
    _setup_style()
    fig, ax1 = plt.subplots(figsize=figsize)
    ax2 = ax1.twinx()

    x = np.arange(len(labels))

    # Bar on right axis (draw first so line is on top)
    ax2.bar(x, series2, width=0.5, color=color2, alpha=0.35,
            edgecolor='none', label=name2, zorder=2)
    # Line on left axis
    ax1.plot(x, series1, color=color1, linewidth=2.5, label=name1,
             zorder=3, marker=None)

    _thin_x_labels(ax1, labels)
    if y1_label:
        ax1.set_ylabel(y1_label, fontsize=9, color='#666')
    if y2_label:
        ax2.set_ylabel(y2_label, fontsize=9, color='#666')
    if title:
        ax1.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, frameon=True,
               fancybox=True, framealpha=0.9, edgecolor='#ddd', loc='best')

    _despine(ax1)
    ax2.spines['top'].set_visible(False)
    ax1.tick_params(axis='both', which='both', length=0)
    ax2.tick_params(axis='both', which='both', length=0)

    return _to_base64(fig)


def render_horizontal_bar(
    categories: List[str],
    values: List[float],
    colors: Optional[List[str]] = None,
    title: str = '',
    data_label_fmt: str = '{:.2f}',
    figsize: Tuple[float, float] = (6, 4),
) -> str:
    """Horizontal bar chart — one bar per category, each with its own color."""
    return render_bar_chart(
        categories=categories,
        values=values,
        title=title,
        colors=colors,
        horizontal=True,
        data_labels=True,
        data_label_fmt=data_label_fmt,
        figsize=figsize,
    )


# ── Figure-returning variants (for PDF builder) ─────────────────────────
# These return the raw matplotlib Figure instead of an HTML string.

def _build_line_chart_fig(
    series_list, labels, series_names=None, title='', y_label='',
    colors=None, annotate_last=True, fill_first=False,
    figsize=(7, 3.5), point_markers=False, y_auto_range=True,
):
    """Build a line chart Figure (shared logic)."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or BRAND_COLORS
    series_names = series_names or [f'Series {i+1}' for i in range(len(series_list))]
    x = np.arange(len(labels))
    do_fill = fill_first and len(series_list) == 1

    for i, values in enumerate(series_list):
        color = colors[i % len(colors)]
        marker = 'o' if point_markers else None
        markersize = 4 if point_markers else None
        ax.plot(x, values, color=color, linewidth=2.2, label=series_names[i],
                marker=marker, markersize=markersize, zorder=3)
        if do_fill and i == 0:
            ax.fill_between(x, values, alpha=0.06, color=color)

    if y_auto_range:
        _auto_y_range(ax, series_list)
    _thin_x_labels(ax, labels)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    if len(series_list) > 1:
        ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
                  edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_line_chart_figure(**kwargs):
    """Return matplotlib Figure for a line chart."""
    return _build_line_chart_fig(**kwargs)


def render_bar_chart_figure(
    categories, values, title='', y_label='', colors=None,
    horizontal=False, data_labels=True, data_label_fmt='{:.1f}',
    figsize=(7, 3.5), bar_width=0.65,
):
    """Return matplotlib Figure for a bar chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    if colors is None:
        colors = BRAND_COLORS[0]
    if isinstance(colors, list) and len(colors) == len(categories):
        bar_colors = colors
    else:
        bar_colors = colors if isinstance(colors, str) else colors[0]

    if data_labels and len(categories) > 12:
        data_labels = False

    x = np.arange(len(categories))
    if horizontal:
        bars = ax.barh(x, values, height=bar_width, color=bar_colors, edgecolor='none', zorder=3)
        ax.set_yticks(x)
        ax.set_yticklabels(categories, fontsize=9)
    else:
        bars = ax.bar(x, values, width=bar_width, color=bar_colors,
                      edgecolor='none', zorder=3, clip_on=False)
        _thin_x_labels(ax, categories)
        if data_labels:
            for bar, val in zip(bars, values):
                fmt = data_label_fmt.format(val)
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        fmt, ha='center', va='bottom', fontsize=7,
                        fontweight='bold', color='#555')
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    if not horizontal:
        ax.set_xlim(-0.5, len(categories) - 0.5)
    return fig


def render_grouped_bar_figure(
    categories, groups, group_labels, colors=None,
    title='', y_label='', data_labels=False, figsize=(7, 3.5),
):
    """Return matplotlib Figure for a grouped bar chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or BRAND_COLORS
    n_groups = len(groups)
    bar_width = 0.7 / n_groups
    x = np.arange(len(categories))
    for i, (vals, label) in enumerate(zip(groups, group_labels)):
        offset = (i - n_groups / 2 + 0.5) * bar_width
        color = colors[i % len(colors)]
        ax.bar(x + offset, vals, width=bar_width, label=label,
               color=color, edgecolor='none', zorder=3)
    _thin_x_labels(ax, categories)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_stacked_bar_figure(
    categories, groups, group_labels, colors=None,
    title='', y_label='', figsize=(7, 3.5),
):
    """Return matplotlib Figure for a stacked bar chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or BRAND_COLORS
    x = np.arange(len(categories))
    bottom = np.zeros(len(categories))
    for i, (vals, label) in enumerate(zip(groups, group_labels)):
        color = colors[i % len(colors)]
        vals_arr = np.array(vals)
        ax.bar(x, vals_arr, width=0.6, bottom=bottom, label=label,
               color=color, edgecolor='none', zorder=3)
        bottom += vals_arr
    _thin_x_labels(ax, categories)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_doughnut_figure(
    labels, values, colors=None, center_text=None,
    title='', figsize=(5, 5), show_pct_labels=True, pct_threshold=3.0,
):
    """Return matplotlib Figure for a doughnut chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or DOUGHNUT_COLORS
    chart_colors = [colors[i % len(colors)] for i in range(len(values))]

    def autopct_func(pct):
        if show_pct_labels and pct >= pct_threshold:
            return f'{pct:.1f}%'
        return ''

    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=chart_colors, autopct=autopct_func,
        startangle=90, pctdistance=0.82,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight('bold')
        at.set_color('#555')
    if center_text:
        ax.text(0, 0, center_text, ha='center', va='center',
                fontsize=18, fontweight='bold', color='#2d3748')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8)
    ax.set_aspect('equal')
    return fig


# ── Economic Trend Charts (v2.0 — NEW) ──────────────────────────────────
# All economic charts: 4.5" × 3.0", DPI 200, endpoint annotations,
# despined, no gridlines, month abbreviation labels.

ECON_DPI = 200
ECON_FIGSIZE = (4.5, 3.0)


def _econ_endpoint_annotation(ax, x_pos, value, color, fmt='{:.2f}%'):
    """Add an endpoint annotation at the last data point."""
    label = fmt.format(value)
    ax.annotate(label, xy=(x_pos, value),
                xytext=(8, 0), textcoords='offset points',
                fontsize=9, fontweight='bold', color=color, va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor='none', alpha=0.85))


def _save_econ_chart(fig, output_path=None):
    """Save economic chart to file or return base64 string."""
    if output_path:
        fig.savefig(output_path, format='png', dpi=ECON_DPI,
                    bbox_inches='tight', facecolor='white',
                    edgecolor='none', pad_inches=0.15)
        plt.close(fig)
        return output_path
    else:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=ECON_DPI, bbox_inches='tight',
                    facecolor='white', edgecolor='none', pad_inches=0.15)
        plt.close(fig)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode('utf-8')
        return f'<img src="data:image/png;base64,{b64}" style="width:100%; height:auto;">'


def render_fed_funds_history(
    labels: List[str],
    values: List[float],
    title: str = 'Federal Funds Rate',
    output_path: Optional[str] = None,
) -> str:
    """Fed Funds Rate history — line + area fill chart.

    Spec: #003366 line (linewidth 2.5), #E2E8F0 area fill (alpha 0.3).
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    x = np.arange(len(labels))

    ax.plot(x, values, color='#003366', linewidth=2.5, zorder=3)
    ax.fill_between(x, values, alpha=0.3, color='#E2E8F0')

    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#003366')

    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Rate (%)', fontsize=9, color='#666')
    ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _save_econ_chart(fig, output_path)


def render_inflation_trend(
    labels: List[str],
    values: List[float],
    fed_target: float = 2.0,
    title: str = 'CPI Inflation (Year-over-Year)',
    output_path: Optional[str] = None,
) -> str:
    """CPI Year-over-Year trend — line chart with Fed 2% target reference.

    Spec: #E97007 line (linewidth 2.5), dashed #70AD47 reference at 2%.
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    x = np.arange(len(labels))

    ax.plot(x, values, color='#E97007', linewidth=2.5, zorder=3)

    # Fed target reference line
    ax.axhline(y=fed_target, color='#70AD47', linestyle='--', linewidth=1.2,
               alpha=0.7, zorder=2)
    ax.text(len(labels) * 0.02, fed_target + 0.08, f'Fed Target: {fed_target}%',
            fontsize=7, color='#70AD47', va='bottom')

    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#E97007')

    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Year-over-Year Change (%)', fontsize=9, color='#666')
    ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _save_econ_chart(fig, output_path)


def render_unemployment_trend(
    labels: List[str],
    values: List[float],
    title: str = 'Unemployment Rate',
    output_path: Optional[str] = None,
) -> str:
    """Unemployment rate trend — line chart.

    Spec: #003366 line (linewidth 2.5), auto y-range (don't start at 0).
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    x = np.arange(len(labels))

    ax.plot(x, values, color='#003366', linewidth=2.5, zorder=3)

    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#003366')

    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Rate (%)', fontsize=9, color='#666')
    ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _save_econ_chart(fig, output_path)


def render_credit_spread_trend(
    labels: List[str],
    values: List[float],
    title: str = 'AA Corporate Credit Spread',
    output_path: Optional[str] = None,
) -> str:
    """AA Credit Spread history — line + area fill.

    Spec: #C00000 line (linewidth 2.5), #FADBD8 area fill (alpha 0.3).
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    x = np.arange(len(labels))

    ax.plot(x, values, color='#C00000', linewidth=2.5, zorder=3)
    ax.fill_between(x, values, alpha=0.3, color='#FADBD8')

    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#C00000')

    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Spread (percentage points)', fontsize=9, color='#666')
    ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    # Subtle context footnote
    ax.text(0.98, 0.02, 'Tighter = more confidence',
            transform=ax.transAxes, fontsize=6, color='#999',
            ha='right', va='bottom', style='italic')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _save_econ_chart(fig, output_path)


def render_yield_curve_comparison(
    tenors: List[str],
    current_values: List[float],
    prior_values: List[float],
    current_label: str = 'Current',
    prior_label: str = '1 Year Ago',
    title: str = 'Treasury Yield Curve',
    output_path: Optional[str] = None,
) -> str:
    """Yield Curve Comparison — dual line chart (current vs 12-month-ago).

    Spec: #003366 current (solid, linewidth 2.5, marker 'o'),
          #FFB703 prior (dashed, linewidth 1.5, marker 's').
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    x = np.arange(len(tenors))

    # Current curve (solid, bold)
    ax.plot(x, current_values, color='#003366', linewidth=2.5, marker='o',
            markersize=5, label=current_label, zorder=3)
    # Prior year curve (dashed, lighter)
    ax.plot(x, prior_values, color='#FFB703', linewidth=1.5, marker='s',
            markersize=4, linestyle='--', label=prior_label, zorder=2)

    # Annotate current curve endpoints
    if current_values:
        # First point
        ax.annotate(f'{current_values[0]:.2f}%', xy=(x[0], current_values[0]),
                    xytext=(-8, 10), textcoords='offset points',
                    fontsize=7, fontweight='bold', color='#003366', ha='right')
        # Last point
        ax.annotate(f'{current_values[-1]:.2f}%', xy=(x[-1], current_values[-1]),
                    xytext=(8, 0), textcoords='offset points',
                    fontsize=7, fontweight='bold', color='#003366', va='center')

    _auto_y_range(ax, [current_values, prior_values])
    ax.set_xticks(x)
    ax.set_xticklabels(tenors, fontsize=8)
    ax.set_ylabel('Yield (%)', fontsize=9, color='#666')
    ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _save_econ_chart(fig, output_path)


def render_economic_trend(
    labels: List[str],
    values: List[float],
    title: str = '',
    y_label: str = '',
    line_color: str = '#003366',
    fill_color: Optional[str] = None,
    fill_alpha: float = 0.3,
    reference_line: Optional[dict] = None,
    output_path: Optional[str] = None,
) -> str:
    """Generic economic trend chart — configurable line + optional area fill.

    This is a catch-all for economic trend charts that don't have a
    specialized renderer. Uses the same 4.5" × 3.0" size and DPI 200.

    Args:
        labels: x-axis labels (month abbreviations)
        values: y-axis values
        title: chart title
        y_label: y-axis label
        line_color: line color hex
        fill_color: optional area fill color (None = no fill)
        fill_alpha: area fill transparency
        reference_line: optional dict with 'value' and 'label' keys
        output_path: optional file path to save PNG
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    x = np.arange(len(labels))

    ax.plot(x, values, color=line_color, linewidth=2.5, zorder=3)
    if fill_color:
        ax.fill_between(x, values, alpha=fill_alpha, color=fill_color)

    if reference_line:
        ref_val = reference_line.get("value", 0)
        ref_label = reference_line.get("label", "")
        ax.axhline(y=ref_val, color='#70AD47', linestyle='--',
                   linewidth=1.2, alpha=0.7, zorder=2)
        if ref_label:
            ax.text(len(labels) * 0.02, ref_val + 0.05, ref_label,
                    fontsize=7, color='#70AD47', va='bottom')

    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], line_color)

    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, color='#666')
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)

    return _save_econ_chart(fig, output_path)


# ── Figure-returning variants for economic charts ────────────────────────

def render_fed_funds_history_figure(**kwargs):
    """Return matplotlib Figure for Fed Funds chart (for PPTX embedding)."""
    kwargs.pop('output_path', None)
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    labels = kwargs.get('labels', [])
    values = kwargs.get('values', [])
    x = np.arange(len(labels))
    ax.plot(x, values, color='#003366', linewidth=2.5, zorder=3)
    ax.fill_between(x, values, alpha=0.3, color='#E2E8F0')
    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#003366')
    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Rate (%)', fontsize=9, color='#666')
    ax.set_title(kwargs.get('title', 'Federal Funds Rate'),
                 fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_inflation_trend_figure(**kwargs):
    """Return matplotlib Figure for CPI YoY chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    labels = kwargs.get('labels', [])
    values = kwargs.get('values', [])
    fed_target = kwargs.get('fed_target', 2.0)
    x = np.arange(len(labels))
    ax.plot(x, values, color='#E97007', linewidth=2.5, zorder=3)
    ax.axhline(y=fed_target, color='#70AD47', linestyle='--',
               linewidth=1.2, alpha=0.7, zorder=2)
    ax.text(len(labels) * 0.02, fed_target + 0.08, f'Fed Target: {fed_target}%',
            fontsize=7, color='#70AD47', va='bottom')
    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#E97007')
    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Year-over-Year Change (%)', fontsize=9, color='#666')
    ax.set_title(kwargs.get('title', 'CPI Inflation (Year-over-Year)'),
                 fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_unemployment_trend_figure(**kwargs):
    """Return matplotlib Figure for Unemployment chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    labels = kwargs.get('labels', [])
    values = kwargs.get('values', [])
    x = np.arange(len(labels))
    ax.plot(x, values, color='#003366', linewidth=2.5, zorder=3)
    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#003366')
    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Rate (%)', fontsize=9, color='#666')
    ax.set_title(kwargs.get('title', 'Unemployment Rate'),
                 fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_credit_spread_trend_figure(**kwargs):
    """Return matplotlib Figure for BBB Spread chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    labels = kwargs.get('labels', [])
    values = kwargs.get('values', [])
    x = np.arange(len(labels))
    ax.plot(x, values, color='#C00000', linewidth=2.5, zorder=3)
    ax.fill_between(x, values, alpha=0.3, color='#FADBD8')
    if values:
        _econ_endpoint_annotation(ax, x[-1], values[-1], '#C00000')
    _auto_y_range(ax, [values])
    _thin_x_labels(ax, labels, max_labels=12)
    ax.set_ylabel('Spread (percentage points)', fontsize=9, color='#666')
    ax.set_title(kwargs.get('title', 'AA Corporate Credit Spread'),
                 fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.text(0.98, 0.02, 'Tighter = more confidence',
            transform=ax.transAxes, fontsize=6, color='#999',
            ha='right', va='bottom', style='italic')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig


def render_yield_curve_comparison_figure(**kwargs):
    """Return matplotlib Figure for Yield Curve Comparison chart."""
    _setup_style()
    fig, ax = plt.subplots(figsize=ECON_FIGSIZE)
    tenors = kwargs.get('tenors', kwargs.get('labels', []))
    current_values = kwargs.get('current_values', kwargs.get('current', []))
    prior_values = kwargs.get('prior_values', kwargs.get('prior', []))
    current_label = kwargs.get('current_label', 'Current')
    prior_label = kwargs.get('prior_label', '1 Year Ago')
    x = np.arange(len(tenors))
    ax.plot(x, current_values, color='#003366', linewidth=2.5, marker='o',
            markersize=5, label=current_label, zorder=3)
    ax.plot(x, prior_values, color='#FFB703', linewidth=1.5, marker='s',
            markersize=4, linestyle='--', label=prior_label, zorder=2)
    if current_values:
        ax.annotate(f'{current_values[0]:.2f}%', xy=(x[0], current_values[0]),
                    xytext=(-8, 10), textcoords='offset points',
                    fontsize=7, fontweight='bold', color='#003366', ha='right')
        ax.annotate(f'{current_values[-1]:.2f}%', xy=(x[-1], current_values[-1]),
                    xytext=(8, 0), textcoords='offset points',
                    fontsize=7, fontweight='bold', color='#003366', va='center')
    _auto_y_range(ax, [current_values, prior_values])
    ax.set_xticks(x)
    ax.set_xticklabels(tenors, fontsize=8)
    ax.set_ylabel('Yield (%)', fontsize=9, color='#666')
    ax.set_title(kwargs.get('title', 'Treasury Yield Curve'),
                 fontsize=11, fontweight='bold', color='#333', pad=8, loc='left')
    ax.legend(fontsize=8, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor='#ddd', loc='best')
    _despine(ax)
    ax.tick_params(axis='both', which='both', length=0)
    return fig
