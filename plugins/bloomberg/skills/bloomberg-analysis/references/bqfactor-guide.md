# bqfactor — Complete API Reference

## Installation / Import
```python
import bqfactor
import bqfactor.factors as bqf
import bqfactor.factors.simple as bqfs      # simple factors
import bqfactor.factors.composite as bqfc   # composite factors
import bqfactor.reports as bqr
import bqfactor.analytics as bqa
import bqfactor.weighting_functions as bqw
import bql

bq = bql.Service()
```

## Analysis Context

```python
# Create analysis context (required first step)
context = bqfactor.create_analysis_context(
    universe=bq.univ.members('SPX Index'),
    time_horizon=bq.func.range('2020-01-01', '2023-12-31', frq='M'),
    bq=bq,
    currency='USD'    # optional: normalize to currency
)

# Filter universe
from bqfactor.filters import is_active
filtered_universe = bq.univ.filter(
    bq.univ.members('SPX Index'),
    is_active(bq)
)
context = bqfactor.create_analysis_context(filtered_universe, time_horizon, bq)
```

## Factor Explorer
```python
# Explore factor data (BQuant notebook only)
context.explore(factor)

# Evaluate weighting function
context.evaluate(weighting_fn(bq, factor))

# Run reports
results = context.report(factor, reports_dict)
results.plot()                          # visualize in notebook
weights_df = results['report_name']    # extract pandas DataFrame
```

## Simple Factors (bqfactor.factors.simple)

| Function | Description |
|----------|-------------|
| `price_earnings(bq)` | P/E ratio |
| `price_book(bq)` | P/B ratio |
| `earnings_yield(bq)` | E/P (inverse P/E) |
| `earnings_yield_forward(bq)` | Forward E/P |
| `fcf_yield(bq)` | Free Cash Flow Yield |
| `dividend_yield(bq)` | Dividend Yield |
| `eps_growth(bq)` | EPS growth |
| `sales_growth(bq)` | Revenue growth |
| `ebitda_growth(bq)` | EBITDA growth |
| `fcf_growth(bq)` | Free Cash Flow growth |
| `gross_margin(bq)` | Gross Margin % |
| `gross_profit(bq)` | Gross Profit |
| `net_margin(bq)` | Net Income Margin % |
| `roa(bq)` | Return on Assets |
| `roe(bq)` | Return on Equity |
| `asset_turnover(bq)` | Revenue / Total Assets |
| `net_income(bq)` | Net Income |
| `ebitda(bq)` | EBITDA |
| `lt_debt(bq)` | Long-term Debt |
| `lt_debt_to_enterprise_value(bq)` | LT Debt / EV |
| `lt_debt_total_assets(bq)` | LT Debt / Total Assets |
| `st_debt(bq)` | Short-term Debt |
| `total_equity(bq)` | Total Equity |
| `price_momentum(bq)` | 12-1 month price momentum |
| `eps_surprise(bq)` | Earnings surprise |

## Composite Factors (bqfactor.factors.composite)

| Function | Description |
|----------|-------------|
| `value_composite(bq)` | Blended value score (P/E, P/B, FCF yield, div yield) |
| `growth_composite(bq)` | Blended growth score (EPS, sales, EBITDA growth) |
| `profitability_composite(bq)` | Blended profitability (ROE, ROA, gross/net margin) |
| `leverage_composite(bq)` | Blended leverage (LT debt, ST debt, debt/assets) |
| `momentum_composite(bq)` | Blended momentum (price momentum, EPS surprise) |

## Reports (bqfactor.reports)

### Portfolio Weight Reports
```python
bqr.LongOnlyPortfolioWeights(weighting_fn)
bqr.LongShortPortfolioWeights(weighting_fn)
bqr.QuantilePortfolioWeights(weighting_fn, n_quantiles=5)
```

### Return Reports
```python
bqr.PortfolioReturns(portfolio_weights)
bqr.FactorPortfolioReturns(weighting_fn)
bqr.ExcessReturns(portfolio_returns, benchmark_returns)
bqr.QuantileReturns(weighting_fn)
bqr.ReturnsComparison([portfolio_returns_1, portfolio_returns_2])
bqr.ReturnsDataFrame(portfolio_returns)
bqr.SecurityReturns()
bqr.RiskFreeRate()
```

### Analytics Reports
```python
bqr.PeriodicAnalyticReport(port_returns, analytics, period='M')   # M, Q, Y
bqr.RollingAnalyticReport(port_returns, analytics, window=12)
bqr.StartToEndAnalyticReport(port_returns, analytics)
bqr.TrailingAnalyticReport(port_returns, analytics, period='1Y')
```

### Diagnostic Reports
```python
bqr.ICHistory()                           # Information Coefficient history
bqr.ExposureReport(factors)               # Factor exposure
bqr.TurnoverReport(weighting_fn)          # Turnover
bqr.TransactionCostsReport(weighting_fn, cost_bps=10)
bqr.TradingPnlReport(weighting_fn)
bqr.ProfitLossContributionReport(weighting_fn)
```

## Analytics (bqfactor.analytics)

```python
bqa.SharpeRatio()
bqa.InformationRatio()
bqa.MaxDrawdown()
bqa.AnnualizedTotalReturn()
bqa.TotalReturn()
bqa.MeanReturn()
bqa.Volatility()
bqa.TrackingError()
bqa.Beta()
bqa.CustomAnalytic(name='My Metric', func=lambda returns: returns.mean())
```

## Weighting Functions (bqfactor.weighting_functions)

```python
bqw.top_bottom_quantile    # long top quintile, short bottom quintile
bqw.top_quantile           # long only top quintile
bqw.market_cap_weight      # market-cap weighted
bqw.beta_neutralize(bq, factor)
bqw.establish_leverage(bq, factor, leverage=1.5)
```

## Local Documentation
```
C:\blp\bqnt\environments\bqnt-3\Doc\html\bqservices\bqfactor\
  Library_Overview.html
  Tutorials\
    Step_1_Create_an_Analysis_Context.html
    Step_2_Create_the_Factors.html
    Step_3_Weighting_Function.html
    Step_4_Create_the_Reports_Dictionary.html
    Step_5_Run_the_Backtest.html
  API_Reference\
    Working_with_Factors\Built-in_Factors\Simple_Factors\
    Working_with_Factors\Built-in_Factors\Composite_Factors\
    Reporting\Portfolio_Reports\
    Reporting\Portfolio_Analytics\
    Strategy_Backtesting\
```
