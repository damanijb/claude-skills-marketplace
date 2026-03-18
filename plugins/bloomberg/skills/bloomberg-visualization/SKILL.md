---
name: bloomberg-visualization
description: Visualize Bloomberg financial data using bqviz (15 Bloomberg-branded plot types) in BQuant notebooks, or matplotlib/plotly patterns for standalone scripts. Use this skill for creating charts, plots, and dashboards from Bloomberg data including line plots, bar charts, histograms, correlation matrices, drawdown plots, and interactive visualizations.
---

# Bloomberg Visualization

## bqviz — Bloomberg Visualization Library

All bqviz plots accept **pandas DataFrames** and return BQuant-compatible figure objects.
Available in `bqnt-3` conda environment: `import bqviz`

---

## Plot Type Selection Guide

| Plot | Class | Use Case |
|------|-------|----------|
| Line | `LinePlot` | Price history, index performance, yield curves |
| Bar | `BarPlot` | Grouped/stacked comparisons, sector breakdowns |
| Histogram | `HistPlot` | Return distributions, factor score distributions |
| KDE | `KDEPlot` | Smooth return distributions, density comparisons |
| Over/Under | `OverUnderPlot` | P&L, excess returns (green/red around zero) |
| Comparison | `ComparisonPlot` | Portfolio vs benchmark (2 series) |
| Multi-Comparison | `MultiComparisonPlot` | Each column of df1 vs df2 |
| Grid | `GridPlot` | Multi-security grid of same plot type |
| Multi-Grid | `MultiGridPlot` | Custom grid with different plot types per panel |
| Interactive Line | `InteractiveLinePlot` | Zoomable time series with control widgets |
| Interactive Scatter | `InteractiveScatterPlot` | X/Y scatter with color axis and regression line |
| Correlation | `CorrelationPlot` | Correlation matrix heatmap (-1 to 1) |
| Cumulative Line | `CumulativeLinePlot` | Cumulative sum/return series |
| Drawdown | `DrawdownPlot` | Maximum drawdown visualization |
| Q-Spread | `QSpreadPlot` | Quantile spread plot (-1 to 1 range) |

---

## Base Plots

```python
from bqviz.base_plots import BarPlot, HistPlot, KDEPlot, LinePlot, OverUnderPlot

# LinePlot: time series or any column-indexed DataFrame
fig = LinePlot(
    df,                      # pandas DataFrame (index=dates, columns=series names)
    title='AAPL Price History',
    colors=['#1f4296', '#e74c3c'],   # hex colors; defaults to Bloomberg palette
    hline=[100, 200],        # horizontal reference lines
    legend='default',        # 'default', 'outside', or None
    tick_format='.2f',
    y_label='Price (USD)',
    x_label='Date',
)
fig.show()

# BarPlot: grouped or stacked
fig = BarPlot(
    df,
    title='Sector P/E Ratios',
    bar_type='grouped',      # 'grouped' or 'stacked'
    color_mode='column',     # 'column' or 'index'
    orientation='vertical',  # 'vertical' or 'horizontal'
)

# HistPlot: distribution of values
fig = HistPlot(df, bins=30, normalized=False, title='Daily Returns Distribution')

# KDEPlot: kernel density estimate
fig = KDEPlot(df, bandwidth=0.018, title='Return Density')

# OverUnderPlot: positive=green, negative=red
fig = OverUnderPlot(df, title='Daily P&L', hline=[0])
```

---

## Compound Plots

```python
from bqviz.compound_plots import ComparisonPlot, MultiComparisonPlot

# ComparisonPlot: portfolio vs benchmark (exactly 2 columns)
fig = ComparisonPlot(df, title='Portfolio vs SPX', colors=['#1f4296', '#e74c3c'])

# MultiComparisonPlot: each column of df1 vs same column of df2
fig = MultiComparisonPlot(df1, df2, titles=['Portfolio', 'Benchmark'], align='vertical')
```

---

## Grid Plots

```python
from bqviz.grid_plots import GridPlot, MultiGridPlot

# GridPlot: one plot per column, all same type
fig = GridPlot(df, plots=LinePlot, cols=3)

# MultiGridPlot: custom plot per panel
fig = MultiGridPlot(
    df,
    plots=[
        (LinePlot,  'Price History',    ['PX_LAST']),
        (BarPlot,   'Volume',           ['PX_VOLUME']),
        (HistPlot,  'Return Dist',      ['DAY_TO_DAY_TOTAL_RETURN']),
    ],
    legend='default',
)
```

---

## Interactive Plots (BQuant notebooks)

```python
from bqviz.interactive_plots import InteractiveLinePlot, InteractiveScatterPlot

# Interactive line with zoom/pan controls
fig = InteractiveLinePlot(df, title='Interactive Price Chart', hide_controls=False, legend='outside')

# Interactive scatter with regression line and color axis
fig = InteractiveScatterPlot(
    df,
    color_field='GICS_SECTOR_NAME',
    scheme='Blues',          # Colorbrewer scheme
    reg_line=True,
    enable_selection=True,
)
```

---

## Specialized Plots

```python
from bqviz.specialized_plots import (
    CorrelationPlot, CumulativeLinePlot, DrawdownPlot, QSpreadPlot
)

# CorrelationPlot: -1 to 1 heatmap
fig = CorrelationPlot(df.corr(), tick_format='.2f')

# CumulativeLinePlot: running cumulative sum
fig = CumulativeLinePlot(returns_df)
fig.push(new_returns_df)     # update live

# DrawdownPlot: show drawdowns
fig = DrawdownPlot(returns_df, inverted=True, colors=['red'])

# QSpreadPlot: -1 to 1 quantile spread
fig = QSpreadPlot(ic_series_df, line=True)
```

---

## Common Data Prep Patterns

```python
from polars_bloomberg import BQuery
import pandas as pd

# Time series -> wide pandas for multi-line plot
with BQuery() as bq:
    result = bq.bql(
        "get(px_last(dates=range(-1Y,0D))) for(['AAPL US Equity','MSFT US Equity'])"
        " with(frq=d, fill=prev)"
    )
    df_polars = result.combine()

df_wide = (
    df_polars
    .pivot(on='ID', index='DATE', values='px_last')
    .sort('DATE')
    .to_pandas()
    .set_index('DATE')
)
fig = LinePlot(df_wide, title='1Y Price Comparison')

# Returns distribution
returns_df = df_wide.pct_change().dropna()
fig = HistPlot(returns_df, bins=50, normalized=True, title='Return Distributions')

# Correlation matrix
fig = CorrelationPlot(returns_df.corr(), title='Return Correlations')

# bqfactor results -> visualization
# results['portfolio_returns'] is a pandas DataFrame
fig = CumulativeLinePlot(results['portfolio_returns'], title='Cumulative Portfolio Return')
fig = DrawdownPlot(results['portfolio_returns'], title='Drawdown Analysis')
```

---

## Matplotlib Patterns (standalone scripts)

For scripts outside BQuant (polars-bloomberg sbc environment):

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

with BQuery() as bq:
    result = bq.bql(
        "get(px_last(dates=range(-1Y,0D))) for('AAPL US Equity') with(frq=d, fill=prev)"
    )
    df = result.combine().to_pandas()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['DATE'], df['px_last'])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.set_title('AAPL 1-Year Price')
plt.tight_layout()
plt.savefig('aapl_price.png', dpi=150)
```

---

## Bloomberg Color Palette
```python
# Bloomberg visualization colors (BB_CLRS default in bqviz)
BB_CLRS = ['#007575', '#D20000', '#1E6AB4', '#89A4C5', '#626262',
           '#E8821C', '#7B3F8F', '#00A878', '#FF6B6B', '#4ECDC4']
```

---

## References
- `references/bqviz-reference.md` — complete bqviz API for all 15 plot classes with all parameters
- `references/chart-patterns.md` — cookbook: BQL data -> chart patterns by use case
