---
name: bloomberg-analysis
description: Quantitative analysis with Bloomberg data — equity screening, factor construction, and backtesting using bqfactor. Use this skill for building custom or built-in factors, weighting portfolios, running backtests, generating IC/return reports, and computing analytics (Sharpe, IR, MaxDrawdown). Also covers BQL screening patterns for multi-criteria security selection.
---

# Bloomberg Analysis — Screening & Factor Research

## BQL Screening Patterns

```python
from polars_bloomberg import BQuery

with BQuery() as bq:
    # Multi-criteria equity screen
    result = bq.bql(
        "for(filter(members('SPX Index'),"
        "    pe_ratio<15 and gross_margin>40 and oper_margin>15))"
        "get(name, pe_ratio, gross_margin, oper_margin, cur_mkt_cap/1B)"
    )
    df = result.combine()

    # Sector averages + z-scores
    result = bq.bql(
        "for(members('SPX Index'))"
        "get(groupAvg(pe_ratio, gics_sector_name),"
        "    groupZscore(day_to_day_total_return(fill=prev)))"
    )

    # Large-cap universe screen (mode=cached for large universes)
    result = bq.bql(
        "for(filter(equitiesUniv(['active','primary']),"
        "    cur_mkt_cap(currency=usd)>100B))"
        "get(count(group(id))) with(mode=cached)"
    )

    # FI screen: high-yield bonds yield > 8%
    result = bq.bql(
        "for(filter(bondsUniv('Active'),"
        "    yield()>=8 and rating(source=BBG) in ['BB+','BB','BB-','B+','B','B-']))"
        "get(name, yield(yield_type=YTW), spread(spread_type='OAS'),"
        "    maturity_years, amt_outstanding/1M)"
    )
```

---

## bqfactor — Factor Analysis & Backtesting

### 5-Step Workflow

```python
import bqfactor
import bqfactor.factors as bqf
import bqfactor.reports as bqr
import bqfactor.analytics as bqa
import bqfactor.weighting_functions as bqw
import bql

bq = bql.Service()

# Step 1: Create analysis context
universe = bq.univ.members('SPX Index')
time_horizon = bq.func.range('2020-01-01', '2023-12-31', frq='M')
context = bqfactor.create_analysis_context(universe, time_horizon, bq, currency='USD')

# Step 2: Create factors
# Built-in simple factor
pe_factor = bqf.simple.price_earnings(bq)

# Built-in composite factor
value_composite = bqf.composite.value_composite(bq)

# Custom BQL-based factor
prev_month = bq.func.range(start='-1M', end='0D')
px_series = bq.data.px_last(dates=prev_month, fill='prev')
momentum = px_series.pct_chg()

# Combine factors: Z-score average
pe_z = pe_factor.groupzscore()
mom_z = momentum.groupzscore()
composite_factor = bq.func.avg(pe_z, mom_z)

# Explore factor data (BQuant notebook only)
context.explore(momentum)

# Step 3: Weighting function
# Built-in: long top quintile, short bottom quintile
weighting_fn = bqw.top_bottom_quantile

# Custom weighting function
def long_top_ten(bq, factor):
    rank = bq.func.grouprank(factor, order='desc')
    top10 = bq.func.if_(rank <= 10, 1, 0)
    return top10 / top10.groupsum()

weighting_fn = long_top_ten

# Step 4: Reports dictionary
portfolio_weights = bqr.LongShortPortfolioWeights(weighting_fn)
portfolio_returns = bqr.PortfolioReturns(portfolio_weights)
analytics = [bqa.SharpeRatio(), bqa.MaxDrawdown(), bqa.InformationRatio(), bqa.AnnualizedTotalReturn()]
monthly_analytics = bqr.PeriodicAnalyticReport(
    port_returns=portfolio_returns, analytics=analytics, period='M'
)
ic_history = bqr.ICHistory()
quantile_returns = bqr.QuantileReturns(weighting_fn)

reports = {
    'portfolio_weights': portfolio_weights,
    'portfolio_returns': portfolio_returns,
    'monthly_analytics': monthly_analytics,
    'ic_history': ic_history,
    'quantile_returns': quantile_returns,
}

# Step 5: Run backtest
results = context.report(composite_factor, reports)

# Visualize (BQuant notebook)
results.plot()

# Extract as DataFrames
weights_df = results['portfolio_weights']
returns_df = results['portfolio_returns']
ic_df = results['ic_history']
```

---

## Built-in Factors

### Simple Factors (25)
```python
import bqfactor.factors as bqf
bq = bql.Service()

# Value
pe_factor         = bqf.simple.price_earnings(bq)           # P/E ratio
pb_factor         = bqf.simple.price_book(bq)               # P/B ratio
ey_factor         = bqf.simple.earnings_yield(bq)           # E/P (inverse P/E)
ey_fwd_factor     = bqf.simple.earnings_yield_forward(bq)   # forward E/P
fcf_yield         = bqf.simple.fcf_yield(bq)                # FCF / market cap
div_yield         = bqf.simple.dividend_yield(bq)           # dividend yield

# Growth
eps_growth        = bqf.simple.eps_growth(bq)               # EPS growth
sales_growth      = bqf.simple.sales_growth(bq)             # revenue growth
ebitda_growth     = bqf.simple.ebitda_growth(bq)            # EBITDA growth
fcf_growth        = bqf.simple.fcf_growth(bq)               # FCF growth

# Quality / Profitability
gross_margin      = bqf.simple.gross_margin(bq)             # gross margin
gross_profit      = bqf.simple.gross_profit(bq)             # gross profit
net_margin        = bqf.simple.net_margin(bq)               # net income margin
roa               = bqf.simple.roa(bq)                      # return on assets
roe               = bqf.simple.roe(bq)                      # return on equity
asset_turnover    = bqf.simple.asset_turnover(bq)           # revenue / assets
net_income        = bqf.simple.net_income(bq)               # net income
ebitda            = bqf.simple.ebitda(bq)                   # EBITDA

# Leverage
lt_debt           = bqf.simple.lt_debt(bq)                  # long-term debt
lt_debt_to_ev     = bqf.simple.lt_debt_to_enterprise_value(bq)
lt_debt_to_assets = bqf.simple.lt_debt_total_assets(bq)
st_debt           = bqf.simple.st_debt(bq)                  # short-term debt
total_equity      = bqf.simple.total_equity(bq)             # total equity

# Momentum
price_momentum    = bqf.simple.price_momentum(bq)           # 12-1 month momentum
eps_surprise      = bqf.simple.eps_surprise(bq)             # earnings surprise
```

### Composite Factors (5)
```python
bqf.composite.value_composite(bq)         # blended value score
bqf.composite.growth_composite(bq)        # blended growth score
bqf.composite.profitability_composite(bq) # blended profitability score
bqf.composite.leverage_composite(bq)      # blended leverage score
bqf.composite.momentum_composite(bq)      # blended momentum score
```

---

## Factor Transformations
```python
factor = bqf.simple.price_earnings(bq)

factor.groupzscore()      # Z-score across universe
factor.grouprank()        # rank across universe
factor.winsorize()        # winsorize outliers
factor.normalize()        # normalize to [0,1]
factor.lag(n=1)           # lag by n periods
```

---

## Report Types

| Report | Description |
|--------|-------------|
| `LongOnlyPortfolioWeights(wfn)` | Long-only portfolio weights |
| `LongShortPortfolioWeights(wfn)` | Long-short portfolio weights |
| `QuantilePortfolioWeights(wfn)` | Weights by quantile bucket |
| `PortfolioReturns(port_weights)` | Portfolio return series |
| `FactorPortfolioReturns(wfn)` | Return attribution to factors |
| `ExcessReturns(port_returns)` | Returns vs benchmark |
| `ICHistory()` | Information coefficient over time |
| `QuantileReturns(wfn)` | Returns by quantile |
| `ExposureReport(factors)` | Factor exposure analysis |
| `TurnoverReport(wfn)` | Portfolio turnover |
| `TransactionCostsReport(wfn)` | Simulated transaction costs |
| `TradingPnlReport(wfn)` | P&L from trading |
| `ProfitLossContributionReport(wfn)` | Per-security P&L contribution |
| `ReturnsComparison(port_returns)` | Multi-portfolio comparison |
| `ReturnsDataFrame(port_returns)` | Raw returns DataFrame |
| `RiskFreeRate()` | Risk-free rate series |
| `SecurityReturns()` | Individual security returns |
| `PeriodicAnalyticReport(port_returns, analytics, period)` | Analytics over periods |
| `RollingAnalyticReport(port_returns, analytics, window)` | Rolling window analytics |
| `StartToEndAnalyticReport(port_returns, analytics)` | Single-period analytics |
| `TrailingAnalyticReport(port_returns, analytics, period)` | Trailing period analytics |

---

## Analytics

```python
import bqfactor.analytics as bqa

analytics = [
    bqa.SharpeRatio(),
    bqa.InformationRatio(),
    bqa.MaxDrawdown(),
    bqa.AnnualizedTotalReturn(),
    bqa.TotalReturn(),
    bqa.MeanReturn(),
    bqa.Volatility(),
    bqa.TrackingError(),
    bqa.Beta(),
    bqa.CustomAnalytic(name='Win Rate', func=lambda r: (r > 0).mean()),
]
```

---

## Weighting Functions

```python
import bqfactor.weighting_functions as bqw

# Built-in
bqw.top_bottom_quantile   # long top quintile, short bottom quintile
bqw.top_quantile          # long only top quintile
bqw.market_cap_weight     # market-cap weighted

# Custom template
def my_weighting(bq, factor):
    rank = bq.func.grouprank(factor, order='desc')
    top_n = bq.func.if_(rank <= 20, 1, 0)
    return top_n / top_n.groupsum()

# Beta-neutralized
config = bqfactor.create_rebalancing_config(
    weight_transformation=bqw.beta_neutralize(bq, factor)
)

# Establish leverage
config = bqfactor.create_rebalancing_config(
    weight_transformation=bqw.establish_leverage(bq, factor, leverage=1.5)
)
```

---

## References
- `references/bqfactor-guide.md` — full bqfactor API reference
- `references/built-in-factors.md` — all 25 simple + 5 composite factors
- `references/screening-patterns.md` — BQL screening cookbook
- `references/sample-notebooks.md` — Bloomberg sample notebook catalog (50+ examples)
