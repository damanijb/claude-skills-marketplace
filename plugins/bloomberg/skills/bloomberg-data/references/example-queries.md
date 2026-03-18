# BQL Example Queries by Asset Class

All examples can be run via:
```python
from polars_bloomberg import BQuery
with BQuery() as bq:
    result = bq.bql("QUERY_HERE")
    df = result.combine()
```

---

## Equity — Fundamentals

```
# Single field
get(IS_EPS) for('IBM US Equity')

# Annual EPS, last 5 periods
get(is_eps(fpt=A, fpo=range(-4,0))) for('AAPL US Equity')

# Calendarized annual EPS range
get(IS_EPS(fpt=BA, fpr=range(2010,2018))) for('ORCL US Equity')

# LTM P/E average over 5 years
get(AVG(DROPNA(PE_RATIO(DATES=RANGE(-5Y,0D), fpt=LTM)))) for('IBM US Equity')

# Custom ratio: FCF yield
get(cf_free_cash_flow / cur_mkt_cap * 100) for('AAPL US Equity')
```

## Equity — Screening

```
# Dow Jones stocks above $200
for(filter(members('INDU Index'), px_last>200)) get(name, px_last, pe_ratio)

# Top 10 SPX by market cap
for(top(members('SPX Index'), 10, CUR_MKT_CAP)) get(name, cur_mkt_cap/1B, pe_ratio, ev_to_ebitda)

# Large-cap universe screen
for(filter(equitiesUniv(['active','primary']), cur_mkt_cap(currency=usd)>100B))
get(count(group(id))) with(mode=cached)

# SPX gold-related companies
for(filter(members('SPX Index'), contains(CIE_DES, "gold"))) get(name, id)

# Screen by multiple criteria
for(filter(members('SPX Index'), pe_ratio<15 and gross_margin>40 and oper_margin>15))
get(name, pe_ratio, gross_margin, oper_margin, cur_mkt_cap/1B)
```

## Equity — Sector / Peer Analysis

```
# Sector averages
for(members('INDU Index')) get(groupAvg(pe_ratio, gics_sector_name), groupAvg(ev_to_ebitda, gics_sector_name))

# Z-scores vs peers
for(members('SPX Index')) get(groupZscore(day_to_day_total_return(fill=prev)))

# Portfolio weighted P/E
for(filter(members('U17911388-100', type=PORT), SECURITY_TYP=='Common Stock'))
get(groupWAvg(pe_ratio, id.weights))

# Peer comparison: AAPL vs Bloomberg best-fit peers
for(union(['AAPL US Equity'], peers('AAPL US Equity', type=BLOOMBERG_BEST_FIT)))
get(name, px_last, pe_ratio, ev_to_ebitda, gross_margin, oper_margin)
```

## Equity — Time Series

```
# 1-year daily prices
get(px_last(dates=range(-1Y,0D))) for('AAPL US Equity') with(frq=d, fill=prev)

# Cumulative return
get(cumProd(1+dropNA(day_to_day_total_return(dates=range(-3M,0d))))-1) for('AAPL US Equity')

# Rolling 1-month average price
for('AAPL US Equity') get(rolling(avg(px_last(-1m,0d)), iterationdates=range(-1y,0d)))

# Annualised volatility (252-day)
get(sqrt(252)*std(day_to_day_total_return(dates=range(-1y,0d)))) for('AAPL US Equity')

# Monthly returns
let(#R = return_series(calc_interval=range(-2Y,0d), per=M);
    #Cum = cumProd(dropna(#R)+1)-1;)
get(#Cum) for('BACR0 Index')
```

---

## Fixed Income — Basic

```
# Bond reference data
get(name, issue_dt, id_isin, crncy, cpn, payment_rank) for('EH469710 Corp')

# Current YTW, OAS, modified duration
get(yield(yield_type=YTW), spread(spread_type='OAS'), duration(duration_type=MODIFIED))
for('DD103619 Corp')

# Historical composite rating
get(BB_COMPOSITE) for('25468PBW5 Corp') with(dates=2021-06-24)

# Point-in-time rating
get(rating(source=SP, type=ISSUE, dates=2020-04-19)) for(['US25468PBW59 Corp'])
```

## Fixed Income — Screening

```
# IG bonds by rating
for(filter(bondsUniv('Active'),
    in(BB_composite, ['AAA','AA+','AA','AA-','A+','A','A-'])))
get(sum(Group(amt_outstanding(currency=USD)))/1M)

# Investment-grade senior bonds
for(filter(bondsUniv(Active),
    RTG_SP>'BBB-' AND IN(PAYMENT_RANK, ['Sr Preferred','Sr Non Preferred'])))
get(count(group(ID)))

# AAPL bonds maturing in 5-10 years
for(filter(bonds('AAPL US Equity'), BETWEEN(MATURITY, 5Y, 10Y))) get(ID)

# High-yield screen with yield > 8%
for(filter(bondsUniv('Active'),
    yield()>=8 and rating(source=BBG) in ['BB+','BB','BB-','B+','B','B-']))
get(name, yield(yield_type=YTW), spread(spread_type='OAS'), maturity_years, amt_outstanding/1M)
```

## Fixed Income — Market Sizing

```
# EUR SSA outstanding
GET(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B)) as #AMT_EUR_Billion)
FOR(FILTER(BONDSUNIV('ACTIVE'), MARKET_CLASSIFICATION=='SSA' AND Crncy==EUR))

# Issuance by quarter (heatmap)
get(SUM(GROUP(amt_issued(currency=EUR)/1B, year(issue_dt)*100+month(issue_dt))))
for(filter(bondsuniv('active'),
    RTG_SP_INITIAL>'BB+' AND
    CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS, CLASSIFICATION_LEVEL=1)=='Corporate'))

# Maturity schedule by year
GET(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B, YEAR(MATURITY))))
FOR(FILTER(BONDSUNIV('ACTIVE'), MARKET_CLASSIFICATION=='Corporate' AND Crncy==EUR))
```

## Fixed Income — YAS Custom Analytics

```
# Price from yield
get(PRICE(YIELD=5, DATES=2023-09-11)) for(['US25468PBW59'])

# Price from OAS
get(PRICE(SPREAD=250, SPREAD_TYPE='OAS', DATES=2023-09-01)) for(['US25468PBW59'])

# Yield from price
get(YIELD(PRICE=115) as #yield) for(['US25468PBW59'])

# OAS given price
get(SPREAD(SPREAD_TYPE='OAS', PRICE=103, DATES=2023-09-01) as #spread) for(['US25468PBW59'])

# Cross-currency spread
get(SPREAD(CURRENCY=EUR) as #XCCY_spread) for(['US25468PBW59'])

# Duration and DV01 given price
get(DURATION(DURATION_TYPE=MODIFIED, PRICE=110, DATES=2023-09-01),
    DV01(PRICE=90, DATES=2023-09-01)) for(['US25468PBW59'])
```

## Fixed Income — Total Return

```
# 3-month total return
get(TOTAL_RETURN(Calc_Interval=Range(-3M,0D), display_returns='Percent')) for('EC527035 Corp')

# Zero-coupon reinvestment assumption
get(TOTAL_RETURN(Calc_Interval=Range(-12M,0D),
    Reinvestment_Type='Fixed', Reinvestment_Rate=0, display_returns='Percent')) for('EC527035 Corp')

# MTD return series
get(total_return(return_type=TOTAL, calc_interval=MTD, dates=range(-1w,0d), fill=prev)) for('EJ222340 Corp')
```

---

## Portfolio Analysis

```
# Holdings list
get(name, px_last, gics_sector_name) for(members('U17911388-100', type=PORT))

# Equity portfolio weighted P/E by sector
get(WAVG(GROUP(PE_RATIO), Group(id().weights)),
    groupAvg(ev_to_ebitda, gics_sector_name))
for(filter(Members('U17911388-100', type=PORT), SECURITY_TYP=='Common Stock'))

# FI portfolio: weight by credit rating
get(sum(group(id().weights, credit_rating))) for(members('U17911388-181', type=PORT))

# FI portfolio OAS by sector
get(AVG(GROUP(SPREAD(spread_type='OAS'), BICS_LEVEL_1_SECTOR_NAME)))
for(members('U17911388-181', type=PORT))

# Map FI holdings to equity for fundamental analysis
for(translateSymbols(filter(Members('U17911388-181', type=PORT), SECURITY_TYP=='Common Stock'),
    targetidtype='fundamentalticker'))
get(AVG(GROUP(PE_RATIO)))
```

---

## CDS

```
# 5Y CDS spread
get(cds_spread(pricing_source=CBIN)) for(cds('JPM US Equity'))

# 10Y CDS time series
get(cds_spread(pricing_source=CBIN, dates=range(-2w,0d), fill=prev))
for(cds('JPM US Equity', tenor=10Y))

# CDS for all INDU members
get(long_comp_name as #name, cds_spread(pricing_source='CBGN').value as #spread)
for(cds(members(['INDU Index']), tenor=5Y))

# CDS term structure via let()
let(#3Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=3Y), mapby=lineage).value;
    #5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=5Y), mapby=lineage).value;)
get(name, #3Y, #5Y) for(members('INDU Index'))

# Implied CDS vs market CDS spread
let(#Implied = RSK_BB_IMPLIED_CDS_SPREAD(dates=-1d,fill=prev).value;
    #5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=5Y), mapby=lineage).value;
    #Spread = #Implied - #5Y;)
get(name, #Implied, #5Y, #Spread)
for(filter(members(['SPX Index']), #Implied*#5Y!=na))

# CDS index membership count
get(count(group(id) as #count)) for(members(['ITRXEXE Curncy']))
```

---

## Credit Ratings

```
# Current rating
get(RATING()) for(['US25468PBW59 Corp'])

# Bloomberg composite, issuer level
get(RATING(SOURCE=BBG, type=ISSUER) as #BBG_Issuer) for(['EI240093 Corp'])

# Historical S&P rating with metadata
let(#rating = RATING(SOURCE=SP, TYPE='ISSUE', DATES=2020-04-19);)
get(#rating().BASE_RATING, #rating().WATCH, #rating().EFFECTIVE_DATE)
for(['US25468PBW59 Corp'])

# Rating time series
get(rating(source=SP, dates=range(2020-01-01, 2023-01-01))) for(['US25468PBW59 Corp'])
```

---

## MBS / Securitized

```
# Agency CMO screen
for(filter(mortgagesUniv(ACTIVE),
    mtg_deal_typ()=='CMO' AND mtg_factor>0.1 AND px_ask<105))
get(name, yield(yield_type=YTW), spread(spread_type='OAS'), mtg_wal, mtg_factor)

# TRACE trades
get(dropna(TRADE_DATA(SOURCE=TRACE, SCENARIO=PX, WORKOUT=TO_WORST,
    VIEW=MTGE_ANALYTICS, dates=range(2024-09-01,2024-09-30))))
for('AMCAR 2024-1 a3 Mtge')

# Weighted avg I-spread for AAA auto ABS (TRACE)
get(wavg(group(matches(TRADE_DATA(#dates), TRADE_DATA(#dates).I_SPREAD <= 300))))
for(filter(mortgagesuniv(all), STRUCTURED_PROD_ASSET_CLASS==AUTO AND RTG_SP==AAA))
with(source=TRACE, scenario=PX, workout=TO_WORST)
```

---

## Funds

```
# Active equity funds focused on US large-cap
for(filter(fundsUniv(['Primary','Active']),
    FUND_GEO_FOCUS=='United States' AND FUND_MKT_CAP_FOCUS=='Large-Cap'))
get(name, fund_total_assets/1B, fund_benchmark_prim, fund_mgmt_style)

# ETF replication strategies
for(filter(fundsUniv(['Primary','Active']), FUND_TYP=='ETF'))
get(name, replication_strategy, index_weighting_methodology, fund_total_assets/1B)

# Fund holdings
get(name, px_last, gics_sector_name) for(holdings('HYG US Equity'))
```
