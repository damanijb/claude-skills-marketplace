---
name: bloomberg-portfolio
description: Portfolio construction and analysis using Bloomberg data — portfolio BQL queries (members with type=PORT), portfolio weighted metrics, risk management, and portfolio optimization. Use this skill for portfolio holdings analysis, risk decomposition, rebalancing analysis, sector/credit allocation, and building Bloomberg portfolio analytics workflows.
---

# Bloomberg Portfolio Analysis

## Portfolio Data Retrieval

```python
from polars_bloomberg import BQuery

with BQuery() as bq:
    # Holdings snapshot
    result = bq.bql(
        "get(name, px_last, gics_sector_name, cur_mkt_cap/1B)"
        "for(members('U17911388-100', type=PORT))"
    )
    df = result.combine()

    # Equity portfolio: weighted P/E by sector
    result = bq.bql(
        "get(WAVG(GROUP(PE_RATIO), GROUP(id().weights)),"
        "    groupAvg(ev_to_ebitda, gics_sector_name))"
        "for(filter(members('U17911388-100', type=PORT), SECURITY_TYP=='Common Stock'))"
    )

    # FI portfolio: weight by credit rating
    result = bq.bql(
        "get(sum(group(id().weights, credit_rating)))"
        "for(members('U17911388-181', type=PORT))"
    )

    # FI portfolio OAS by sector
    result = bq.bql(
        "get(AVG(GROUP(SPREAD(spread_type='OAS'), BICS_LEVEL_1_SECTOR_NAME)))"
        "for(members('U17911388-181', type=PORT))"
    )

    # Drifting weight portfolio (use positions not weights)
    result = bq.bql("get(id().positions) for(members('PORT_ID', type=PORT))")

    # Map FI holdings -> equity fundamentals
    result = bq.bql(
        "for(translateSymbols("
        "    filter(members('U17911388-181', type=PORT), SECURITY_TYP=='Common Stock'),"
        "    targetidtype='fundamentalticker'))"
        "get(AVG(GROUP(PE_RATIO)))"
    )
```

---

## Portfolio Weight vs Position

| Scenario | Field | Notes |
|----------|-------|-------|
| Fixed Weight portfolio | `id().weights` | Fixed weight percentages |
| Shares/Par portfolio | `id().weights` | Weight based on shares/par value |
| Drifting Weight portfolio | `id().positions` | Current positions (weight drifts with price) |

---

## Risk Management Patterns

```python
with BQuery() as bq:
    # Annualized volatility (252-day) across index members
    result = bq.bql(
        "get(sqrt(252)*std(day_to_day_total_return(dates=range(-1y,0d))))"
        "for(members('SPX Index'))"
    )

    # Cumulative 1-year return
    result = bq.bql(
        "get(cumProd(1+dropNA(day_to_day_total_return(dates=range(-1Y,0d))))-1)"
        "for(members('SPX Index'))"
    )

    # Portfolio Z-score vs peers
    result = bq.bql(
        "for(members('SPX Index'))"
        "get(groupZscore(day_to_day_total_return(fill=prev)))"
    )

    # Rolling 1-month average price
    result = bq.bql(
        "for('AAPL US Equity')"
        "get(rolling(avg(px_last(-1m,0d)), iterationdates=range(-1y,0d)))"
    )

    # Bond portfolio key rate durations
    result = bq.bql(
        "get(KRD(TENOR=2Y), KRD(TENOR=5Y), KRD(TENOR=10Y), KRD(TENOR=30Y),"
        "    DV01, DURATION(DURATION_TYPE=MODIFIED))"
        "for(members('FI_PORT_ID', type=PORT))"
    )
```

---

## Sector / Allocation Analysis

```python
with BQuery() as bq:
    # Equity sector weights
    result = bq.bql(
        "get(sum(group(id().weights, gics_sector_name)))"
        "for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))"
    )

    # Bond maturity schedule by year
    result = bq.bql(
        "GET(SUM(GROUP(AMT_Outstanding(CURRENCY=USD)/1B, YEAR(MATURITY))))"
        "FOR(members('PORT_ID', type=PORT))"
    )

    # Country exposure
    result = bq.bql(
        "get(sum(group(id().weights, cntry_of_risk)))"
        "for(members('PORT_ID', type=PORT))"
    )

    # Duration-weighted OAS by sector
    result = bq.bql(
        "get(wavg(group(spread(spread_type='OAS'), bics_level_1_sector_name),"
        "         group(duration(duration_type=MODIFIED), bics_level_1_sector_name)))"
        "for(members('FI_PORT_ID', type=PORT))"
    )
```

---

## Total Return Analysis

```python
with BQuery() as bq:
    # 3-month total return per holding
    result = bq.bql(
        "get(TOTAL_RETURN(Calc_Interval=Range(-3M,0D), display_returns='Percent'))"
        "for(members('PORT_ID', type=PORT))"
    )

    # Monthly total return series
    result = bq.bql(
        "get(total_return(return_type=TOTAL, calc_interval=MTD,"
        "    dates=range(-1y,0d), fill=prev))"
        "for(members('PORT_ID', type=PORT))"
    )

    # Portfolio vs benchmark cumulative return
    result = bq.bql(
        "let(#R = return_series(calc_interval=range(-2Y,0d), per=M);"
        "    #Cum = cumProd(dropna(#R)+1)-1;)"
        "get(#Cum)"
        "for(union([members('PORT_ID', type=PORT)], ['SPX Index']))"
    )
```

---

## Portfolio Construction with bqfactor

```python
import bqfactor
import bqfactor.reports as bqr
import bqfactor.analytics as bqa
import bqfactor.weighting_functions as bqw
import bql

bq = bql.Service()

# Universe: your portfolio + benchmark
portfolio = bq.univ.members('U17911388-100', type='PORT')
benchmark = bq.univ.members('SPX Index')
universe = bq.univ.union(portfolio, benchmark)

time_horizon = bq.func.range('2023-01-01', '2024-12-31', frq='M')
context = bqfactor.create_analysis_context(universe, time_horizon, bq, currency='USD')

# Market-cap weighted long-only portfolio
def mktcap_weight(bq, factor):
    mktcap = bq.data.cur_mkt_cap(fill='prev')
    return mktcap / mktcap.groupsum()

portfolio_weights = bqr.LongOnlyPortfolioWeights(mktcap_weight)
portfolio_returns = bqr.PortfolioReturns(portfolio_weights)

analytics = [
    bqa.AnnualizedTotalReturn(),
    bqa.SharpeRatio(),
    bqa.MaxDrawdown(),
    bqa.TrackingError(),
    bqa.InformationRatio(),
    bqa.Beta(),
    bqa.Volatility(),
]

reports = {
    'weights': portfolio_weights,
    'returns': portfolio_returns,
    'analytics': bqr.StartToEndAnalyticReport(portfolio_returns, analytics),
    'rolling_sharpe': bqr.RollingAnalyticReport(
        portfolio_returns, analytics=[bqa.SharpeRatio()], window=12
    ),
}

mktcap_factor = bq.data.cur_mkt_cap(fill='prev')
results = context.report(mktcap_factor, reports)
```

---

## Entity Translation

```python
with BQuery() as bq:
    # Bond holdings -> equity parent for fundamental analysis
    result = bq.bql(
        "for(translateSymbols(members('FI_PORT', type=PORT),"
        "    targetidtype='fundamentalticker'))"
        "get(name, pe_ratio, ev_to_ebitda, tot_debt_to_ebitda)"
    )

    # Get issuer from bond
    result = bq.bql(
        "for(issuerOf(['AZ791428 Corp']))"
        "get(name, gics_sector_name, cur_mkt_cap/1B)"
    )

    # Fund holdings analysis
    result = bq.bql(
        "get(name, px_last, gics_sector_name, cur_mkt_cap/1B)"
        "for(holdings('HYG US Equity'))"
    )
```

---

## References
- `references/portfolio-patterns.md` — portfolio BQL cookbook with 30+ patterns
- `references/risk-management.md` — volatility, correlation, and hedging patterns
