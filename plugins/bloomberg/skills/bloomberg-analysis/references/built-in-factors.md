# bqfactor Built-in Factors — Complete Reference

All factors are created with `factor = bqf.category.name(bq)` where `bq = bql.Service()`.

## Import
```python
import bqfactor.factors as bqf
import bql
bq = bql.Service()
```

## Simple Factors (25 total)

### Value (6)
| Factor | Function | Underlying BQL |
|--------|----------|----------------|
| P/E Ratio | `bqf.simple.price_earnings(bq)` | `pe_ratio()` |
| P/B Ratio | `bqf.simple.price_book(bq)` | `cur_mkt_cap / book_val_per_sh` |
| Earnings Yield | `bqf.simple.earnings_yield(bq)` | `1 / pe_ratio()` |
| Forward Earnings Yield | `bqf.simple.earnings_yield_forward(bq)` | `1 / pe_ratio(fpt=BT)` |
| FCF Yield | `bqf.simple.fcf_yield(bq)` | `cf_free_cash_flow / cur_mkt_cap` |
| Dividend Yield | `bqf.simple.dividend_yield(bq)` | `is_div_per_shr / px_last` |

### Growth (4)
| Factor | Function | Underlying BQL |
|--------|----------|----------------|
| EPS Growth | `bqf.simple.eps_growth(bq)` | `eps_growth()` or `is_eps` YoY % |
| Sales Growth | `bqf.simple.sales_growth(bq)` | `sales_rev_turn` YoY % |
| EBITDA Growth | `bqf.simple.ebitda_growth(bq)` | `ebitda` YoY % |
| FCF Growth | `bqf.simple.fcf_growth(bq)` | `cf_free_cash_flow` YoY % |

### Quality / Profitability (8)
| Factor | Function | Underlying BQL |
|--------|----------|----------------|
| Gross Margin | `bqf.simple.gross_margin(bq)` | `gross_margin()` |
| Gross Profit | `bqf.simple.gross_profit(bq)` | `gross_profit()` |
| Net Margin | `bqf.simple.net_margin(bq)` | `prof_margin()` |
| ROA | `bqf.simple.roa(bq)` | `return_on_asset()` |
| ROE | `bqf.simple.roe(bq)` | `return_com_eqy()` |
| Asset Turnover | `bqf.simple.asset_turnover(bq)` | `asset_turnover()` |
| Net Income | `bqf.simple.net_income(bq)` | `net_income()` |
| EBITDA | `bqf.simple.ebitda(bq)` | `ebitda()` |

### Leverage (5)
| Factor | Function | Underlying BQL |
|--------|----------|----------------|
| LT Debt | `bqf.simple.lt_debt(bq)` | `bs_lt_borrow()` |
| LT Debt / EV | `bqf.simple.lt_debt_to_enterprise_value(bq)` | `lt_debt / enterprise_value` |
| LT Debt / Assets | `bqf.simple.lt_debt_total_assets(bq)` | `lt_debt_to_tot_asset()` |
| ST Debt | `bqf.simple.st_debt(bq)` | `bs_st_borrow()` |
| Total Equity | `bqf.simple.total_equity(bq)` | `total_equity()` |

### Momentum (2)
| Factor | Function | Underlying BQL |
|--------|----------|----------------|
| Price Momentum | `bqf.simple.price_momentum(bq)` | 12-1 month total return |
| EPS Surprise | `bqf.simple.eps_surprise(bq)` | `eps_surprise()` |

## Composite Factors (5 total)

| Factor | Function | Components |
|--------|----------|------------|
| Value Composite | `bqf.composite.value_composite(bq)` | Avg Z-score: P/E, P/B, FCF yield, earnings yield, div yield |
| Growth Composite | `bqf.composite.growth_composite(bq)` | Avg Z-score: EPS growth, sales growth, EBITDA growth |
| Profitability Composite | `bqf.composite.profitability_composite(bq)` | Avg Z-score: ROE, ROA, gross margin, net margin |
| Leverage Composite | `bqf.composite.leverage_composite(bq)` | Avg Z-score: LT debt/EV, LT debt/assets, ST debt |
| Momentum Composite | `bqf.composite.momentum_composite(bq)` | Avg Z-score: price momentum, EPS surprise |

## Factor Transformations

```python
factor = bqf.simple.price_earnings(bq)

# Cross-sectional transformations
factor.groupzscore()          # Z-score across universe at each date
factor.grouprank()            # Rank 1..N across universe (ascending)
factor.grouprank(order='desc') # Rank descending
factor.winsorize()            # Clip outliers at 2 std deviations
factor.normalize()            # Normalize to [0,1] range
factor.lag(n=1)               # Lag by n rebalancing periods
```

## Combining Factors

```python
import bql
bq = bql.Service()
import bqfactor.factors as bqf

# Z-score average (equal weight composite)
pe_z = bqf.simple.price_earnings(bq).groupzscore()
mom_z = bqf.simple.price_momentum(bq).groupzscore()
composite = bq.func.avg(pe_z, mom_z)

# Weighted average
composite = pe_z * 0.6 + mom_z * 0.4

# Rank-based composite (more robust to outliers)
pe_rank = bqf.simple.price_earnings(bq).grouprank()
mom_rank = bqf.simple.price_momentum(bq).grouprank()
composite = bq.func.avg(pe_rank, mom_rank)

# Multi-factor composite using built-in composites
value = bqf.composite.value_composite(bq)
quality = bqf.composite.profitability_composite(bq)
momentum = bqf.composite.momentum_composite(bq)
vqm = bq.func.avg(value.groupzscore(), quality.groupzscore(), momentum.groupzscore())
```

## Custom Factor Construction

```python
# Custom momentum: 6-month return
prev_6m = bq.func.range(start='-6M', end='0D')
px_6m = bq.data.px_last(dates=prev_6m, fill='prev')
momentum_6m = px_6m.pct_chg()

# Custom quality: FCF / Revenue
fcf = bq.data.cf_free_cash_flow(fpt='LTM')
rev = bq.data.sales_rev_turn(fpt='LTM')
fcf_margin = fcf / rev

# Custom leverage: Net Debt / EBITDA
net_debt = bq.data.short_and_long_term_debt() - bq.data.bs_cash_near_cash_item()
ebitda = bq.data.ebitda(fpt='LTM')
net_leverage = net_debt / ebitda

# CDE (Consumer Data Engine) factor
cde_factor = bq.data.cde_sales_yoy_growth()   # requires Bloomberg Second Measure subscription
```
