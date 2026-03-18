# bqviz — Complete API Reference

## Import
```python
import bqviz
from bqviz.base_plots import BarPlot, HistPlot, KDEPlot, LinePlot, OverUnderPlot
from bqviz.compound_plots import ComparisonPlot, MultiComparisonPlot
from bqviz.grid_plots import GridPlot, MultiGridPlot
from bqviz.interactive_plots import InteractiveLinePlot, InteractiveScatterPlot
from bqviz.specialized_plots import CorrelationPlot, CumulativeLinePlot, DrawdownPlot, QSpreadPlot
```

All plots accept **pandas DataFrames**. Available in `bqnt-3` environment.

## Bloomberg Color Palette (BB_CLRS)
```python
BB_CLRS = ['#007575', '#D20000', '#1E6AB4', '#89A4C5', '#626262',
           '#E8821C', '#7B3F8F', '#00A878', '#FF6B6B', '#4ECDC4']
```

## Common Parameters (most plots)
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | pandas DataFrame | required | Data to plot |
| `title` | str | `''` | Plot title |
| `fig_style` | str | `'general'` | BQV_FIGSTYLE reference |
| `colors` | list[str] | BB_CLRS | Hex color list |
| `hline` | list[num] | None | Horizontal reference lines |
| `legend` | str/None | `'default'` | `'default'`, `'outside'`, or None |
| `tick_format` | str | None | Y-axis format e.g. `'.2f'`, `'0.1%'` |
| `num_ticks` | int | None | Number of Y-axis ticks |
| `y_label` | str | None | Y-axis label |
| `x_label` | str | None | X-axis label |
| `y_min` | float | None | Y-axis minimum |
| `y_max` | float | None | Y-axis maximum |
| `is_subplot` | bool | False | True when used inside GridPlot |

## Base Plots

### LinePlot
```python
LinePlot(df, title='', fig_style='general', colors=BB_CLRS, hline=None,
         legend='default', tick_format=None, num_ticks=None,
         convert_dates=False, y_label=None, x_label=None, is_subplot=False)
```
Use for: time series, price histories, multi-line comparisons, yield curves.

### BarPlot
```python
BarPlot(df, title='', fig_style='general', bar_type='grouped', colors=BB_CLRS,
        normalized=False, num_ticks=None, color_mode='column',
        y_label=None, x_label=None, is_subplot=False, orientation='vertical')
# bar_type: 'grouped' or 'stacked'
# color_mode: 'column' or 'index'
# orientation: 'vertical' or 'horizontal'
```
Use for: sector comparisons, grouped metrics, stacked allocations.

### HistPlot
```python
HistPlot(df, bins=10, normalized=False, title='', fig_style='general',
         colors=BB_CLRS, cols=2, tick_format=None, y_label=None, x_label=None,
         is_subplot=False)
```
Use for: return distributions, factor score distributions.

### KDEPlot
```python
KDEPlot(df, title='KDE', fig_style='general', colors=BB_CLRS,
        legend='default', bandwidth=0.018, tick_format=None, num_ticks=None,
        y_label=None, x_label=None, is_subplot=False)
```
Use for: smooth density estimates, comparing distributions.

### OverUnderPlot
```python
OverUnderPlot(df, title='', fig_style='general', colors=None, hline=None,
              y_min=None, y_max=None, tick_format=None, legend=None,
              convert_dates=False, line=False, y_label=None, x_label=None,
              is_subplot=False)
```
Use for: P&L, excess returns, any series that flips sign.

## Compound Plots

### ComparisonPlot
```python
ComparisonPlot(df, title='', colors=BB_CLRS, hline=None, legend='default',
               y_min=None, y_max=None, tick_format=None, num_ticks=None)
# df must have exactly 2 columns: portfolio vs benchmark
```

### MultiComparisonPlot
```python
MultiComparisonPlot(df1, df2, titles=['', ''], colors=BB_CLRS, hline=None,
                    legend='default', y_min=None, y_max=None, align='vertical',
                    tick_format=None, num_ticks=None, is_subplot=False)
# df1 and df2 must have same columns
# align: 'vertical' or 'horizontal'
```

## Grid Plots

### GridPlot
```python
GridPlot(df, plots=LinePlot, cols=3, colors=BB_CLRS, widths=None,
         tick_format=None, convert_dates=False, heights=None)
# plots: single class or list of classes (one per column)
```

### MultiGridPlot
```python
MultiGridPlot(df, plots, colors=BB_CLRS, legend='default', widths=None,
              tick_format=None, heights=None)
# plots: list of (PlotClass, title_str, [column_names]) tuples
```

## Interactive Plots

### InteractiveLinePlot
```python
InteractiveLinePlot(df, title='', colors=BB_CLRS, hide_controls=False,
                    tick_format=None, legend='default', y_min=None, y_max=None,
                    num_ticks=None, y_label=None, x_label=None, is_subplot=False)
```

### InteractiveScatterPlot
```python
InteractiveScatterPlot(df, color_field=None, scheme='Blues', reg_line=True,
                       indexes=False, num_ticks=None, is_subplot=False,
                       enable_selection=True, title='', fig_style='general',
                       colors=BB_CLRS)
# scheme: any Colorbrewer scheme string
```

## Specialized Plots

### CorrelationPlot
```python
CorrelationPlot(df, tick_format='.2f')
# df: correlation matrix (pass df.corr())
# range: -1 to 1 heatmap
```

### CumulativeLinePlot
```python
CumulativeLinePlot(df, tick_format=None)
fig.push(new_df)  # update with new data (live streaming)
```

### DrawdownPlot
```python
DrawdownPlot(df, legend=None, title=None, inverted=True, colors=['red'],
             tick_format=None)
# inverted=True: flip so drawdowns show as negative bars
```

### QSpreadPlot
```python
QSpreadPlot(df, line=True, colors=None)
# range: -1 to 1 (quantile spread)
# line=True: overlay trend line
```

## Local Documentation
```
C:\blp\bqnt\environments\bqnt-3\Doc\html\bqviz\
  index.html            -- overview
  api_ref_summary.html  -- all class signatures
  bqviz_gallery.html    -- visual gallery
  _stubs\               -- individual class stubs
```
