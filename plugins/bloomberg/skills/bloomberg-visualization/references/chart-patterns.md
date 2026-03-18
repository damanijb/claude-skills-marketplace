# Bloomberg Chart Patterns Cookbook

## Time Series Charts

```python
from polars_bloomberg import BQuery
from bqviz.base_plots import LinePlot, OverUnderPlot
from bqviz.specialized_plots import CumulativeLinePlot, DrawdownPlot
import pandas as pd

# 1-year daily price chart (single stock)
with BQuery() as bq:
    result = bq.bql(
        "get(px_last(dates=range(-1Y,0D))) for('AAPL US Equity') with(frq=d, fill=prev)"
    )
    df = result.combine().to_pandas().set_index('DATE')[['px_last']]
    df.columns = ['AAPL']
fig = LinePlot(df, title='AAPL 1-Year Price', tick_format='.0f', y_label='USD')
fig.show()

# Multi-stock comparison
with BQuery() as bq:
    result = bq.bql(
        "get(px_last(dates=range(-1Y,0D)))"
        "for(['AAPL US Equity', 'MSFT US Equity', 'GOOGL US Equity'])"
        "with(frq=d, fill=prev)"
    )
    df_long = result.combine()
df_wide = (
    df_long.to_pandas()
    .pivot(index='DATE', columns='ID', values='px_last')
    .sort_index()
)
fig = LinePlot(df_wide, title='Tech Stock Comparison', legend='outside')

# Cumulative return chart
with BQuery() as bq:
    result = bq.bql(
        "get(cumProd(1+dropNA(day_to_day_total_return(dates=range(-1Y,0d))))-1)"
        "for(['AAPL US Equity', 'SPY US Equity'])"
        "with(frq=d, fill=prev)"
    )
    df_long = result.combine()
df_cum = df_long.to_pandas().pivot(index='DATE', columns='ID', values='cumProd...')
fig = CumulativeLinePlot(df_cum, title='Cumulative Return vs SPY')

# Daily P&L (over/under zero)
with BQuery() as bq:
    result = bq.bql(
        "get(day_to_day_total_return(dates=range(-6M,0d)))"
        "for('AAPL US Equity') with(frq=d, fill=prev)"
    )
    df = result.combine().to_pandas().set_index('DATE')[['day_to_day_total_return']]
fig = OverUnderPlot(df, title='Daily Returns', tick_format='.2%', hline=[0])
```

## Distribution Charts

```python
from bqviz.base_plots import HistPlot, KDEPlot

# Return histogram
with BQuery() as bq:
    result = bq.bql(
        "get(day_to_day_total_return(dates=range(-2Y,0d)))"
        "for('SPY US Equity') with(frq=d, fill=prev)"
    )
    df = result.combine().to_pandas().set_index('DATE')[['day_to_day_total_return']]
fig = HistPlot(df, bins=50, normalized=True, title='SPY Daily Return Distribution')

# Compare return distributions across assets
with BQuery() as bq:
    result = bq.bql(
        "get(day_to_day_total_return(dates=range(-1Y,0d)))"
        "for(['AAPL US Equity', 'MSFT US Equity']) with(frq=d, fill=prev)"
    )
    df_long = result.combine()
df_wide = df_long.to_pandas().pivot(index='DATE', columns='ID', values='day_to_day_total_return')
fig = KDEPlot(df_wide, title='Return Density Comparison', bandwidth=0.005)
```

## Bar Charts (Cross-Sectional)

```python
from bqviz.base_plots import BarPlot

# Sector P/E ratios
with BQuery() as bq:
    result = bq.bql(
        "for(members('INDU Index'))"
        "get(groupAvg(pe_ratio, gics_sector_name))"
    )
    df = result.combine().to_pandas().set_index('gics_sector_name')[['groupAvg(pe_ratio,...)']]
fig = BarPlot(df, title='DJIA Average P/E by Sector', orientation='horizontal')

# Credit rating distribution (stacked)
with BQuery() as bq:
    result = bq.bql(
        "for(filter(bondsUniv('Active'), MARKET_CLASSIFICATION=='Corporate' AND Crncy==USD))"
        "get(count(group(id, rating(source=BBG))))"
    )
# pivot to get rating as columns, then stacked bar
fig = BarPlot(df_ratings, bar_type='stacked', title='IG Bond Count by Rating')
```

## Correlation Matrix

```python
from bqviz.specialized_plots import CorrelationPlot

# Index member correlation heatmap
with BQuery() as bq:
    result = bq.bql(
        "get(day_to_day_total_return(dates=range(-1Y,0d)))"
        "for(top(members('INDU Index'), 20, CUR_MKT_CAP))"
        "with(frq=d, fill=prev)"
    )
    df_long = result.combine()
df_wide = df_long.to_pandas().pivot(index='DATE', columns='ID', values='day_to_day_total_return')
corr_matrix = df_wide.corr()
fig = CorrelationPlot(corr_matrix, title='DJIA Top-20 Return Correlations')
```

## Drawdown Chart

```python
from bqviz.specialized_plots import DrawdownPlot

with BQuery() as bq:
    result = bq.bql(
        "get(day_to_day_total_return(dates=range(-3Y,0d)))"
        "for('SPY US Equity') with(frq=d, fill=prev)"
    )
    df = result.combine().to_pandas().set_index('DATE')[['day_to_day_total_return']]
fig = DrawdownPlot(df, title='SPY Drawdown (3Y)', inverted=True)
```

## Grid Layouts

```python
from bqviz.grid_plots import GridPlot, MultiGridPlot
from bqviz.base_plots import LinePlot, BarPlot, HistPlot

# SPX sector grid (one panel per sector)
with BQuery() as bq:
    result = bq.bql(
        "get(groupAvg(px_last(dates=range(-1Y,0d)), gics_sector_name))"
        "for(members('SPX Index')) with(frq=m, fill=prev)"
    )
    df_wide = result.combine().to_pandas().pivot(...)

fig = GridPlot(df_wide, plots=LinePlot, cols=3, title='Sector Price Trends')

# Multi-metric dashboard
fig = MultiGridPlot(
    df_combined,
    plots=[
        (LinePlot,  'Price History',      ['PX_LAST']),
        (BarPlot,   'Monthly Volume',     ['PX_VOLUME']),
        (HistPlot,  'Return Distribution',['DAY_TO_DAY_TOTAL_RETURN']),
        (OverUnderPlot, 'Daily P&L',      ['DAY_TO_DAY_TOTAL_RETURN']),
    ],
)
```

## Interactive Charts (BQuant Notebooks)

```python
from bqviz.interactive_plots import InteractiveLinePlot, InteractiveScatterPlot

# Zoomable price chart
fig = InteractiveLinePlot(price_df, title='Interactive Price Chart', hide_controls=False)

# Scatter: P/E vs ROE colored by sector
with BQuery() as bq:
    result = bq.bql(
        "get(pe_ratio, return_com_eqy, gics_sector_name, name)"
        "for(filter(members('SPX Index'), pe_ratio<50 and return_com_eqy>0))"
    )
    df = result.combine().to_pandas().set_index('ID')
    df.columns = ['PE', 'ROE', 'Sector', 'Name']
fig = InteractiveScatterPlot(df[['PE','ROE']], color_field='Sector', reg_line=True,
                              title='P/E vs ROE by Sector')
```

## bqfactor Results Visualization

```python
# After running context.report(factor, reports)
from bqviz.specialized_plots import CumulativeLinePlot, DrawdownPlot, CorrelationPlot
from bqviz.base_plots import LinePlot, BarPlot

returns_df = results['portfolio_returns']   # pandas DataFrame from bqfactor

# Cumulative return of strategy
fig = CumulativeLinePlot(returns_df, title='Strategy Cumulative Return')

# Drawdown profile
fig = DrawdownPlot(returns_df, title='Strategy Drawdown', inverted=True)

# IC over time
ic_df = results['ic_history']
fig = BarPlot(ic_df, title='Information Coefficient History', bar_type='grouped')

# Quantile returns
quantile_df = results['quantile_returns']
fig = BarPlot(quantile_df, title='Quantile Portfolio Returns')
```

## Yield Curve / Fixed Income Charts

```python
# Yield curve evolution
with BQuery() as bq:
    result = bq.bql(
        "get(yield(yield_type=YTW, dates=range(-1Y,0D)))"
        "for(curveMembers('YCGT0025 Index'))"
        "with(frq=m, fill=prev)"
    )
    df = result.combine()
# pivot on security (tenor), index=date
df_curve = df.to_pandas().pivot(index='DATE', columns='ID', values='yield(yield_type=YTW)')
fig = LinePlot(df_curve, title='Treasury Yield Curve Evolution', y_label='Yield (%)')

# Credit spread heatmap
with BQuery() as bq:
    result = bq.bql(
        "get(AVG(GROUP(SPREAD(spread_type='OAS'), BICS_LEVEL_1_SECTOR_NAME)))"
        "for(filter(bondsUniv('Active'), MARKET_CLASSIFICATION=='Corporate' AND Crncy==USD))"
    )
    df = result.combine().to_pandas()
fig = BarPlot(df.set_index('BICS_LEVEL_1_SECTOR_NAME'), title='OAS by Sector (bps)', orientation='horizontal')
```
