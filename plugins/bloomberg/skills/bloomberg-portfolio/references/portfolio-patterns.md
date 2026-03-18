# Portfolio BQL Patterns Cookbook

## Holdings & Weights

```python
from polars_bloomberg import BQuery

with BQuery() as bq:
    # Full holdings snapshot
    result = bq.bql(
        "get(name, px_last, gics_sector_name, cur_mkt_cap/1B, id().weights)"
        "for(members('PORT_ID', type=PORT))"
    )

    # Filter to equity only
    result = bq.bql(
        "get(name, px_last, pe_ratio, gics_sector_name, id().weights)"
        "for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))"
    )

    # Fixed income holdings
    result = bq.bql(
        "get(name, yield(yield_type=YTW), spread(spread_type='OAS'),"
        "    duration(duration_type=MODIFIED), maturity, rating(source=BBG), id().weights)"
        "for(members('FI_PORT_ID', type=PORT))"
    )

    # Drifting weight portfolio
    result = bq.bql(
        "get(name, id().positions)"
        "for(members('PORT_ID', type=PORT))"
    )
```

## Sector / Country / Rating Allocation

```python
with BQuery() as bq:
    # Equity sector weights
    result = bq.bql(
        "get(sum(group(id().weights, gics_sector_name)))"
        "for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))"
    )

    # BICS sector allocation
    result = bq.bql(
        "get(sum(group(id().weights, bics_level_1_sector_name)))"
        "for(members('PORT_ID', type=PORT))"
    )

    # Country allocation
    result = bq.bql(
        "get(sum(group(id().weights, cntry_of_risk)))"
        "for(members('PORT_ID', type=PORT))"
    )

    # FI rating allocation
    result = bq.bql(
        "get(sum(group(id().weights, rating(source=BBG))))"
        "for(members('FI_PORT_ID', type=PORT))"
    )

    # FI currency allocation
    result = bq.bql(
        "get(sum(group(amt_outstanding(currency=USD)/1M, crncy)))"
        "for(members('FI_PORT_ID', type=PORT))"
    )

    # Bond maturity schedule by year
    result = bq.bql(
        "GET(SUM(GROUP(AMT_Outstanding(CURRENCY=USD)/1B, YEAR(MATURITY))))"
        "FOR(members('FI_PORT_ID', type=PORT))"
    )

    # Bond maturity schedule by quarter
    result = bq.bql(
        "GET(SUM(GROUP(AMT_Outstanding(CURRENCY=USD)/1B,"
        "    year(MATURITY)*100+month(MATURITY))))"
        "FOR(members('FI_PORT_ID', type=PORT))"
    )
```

## Weighted Analytics

```python
with BQuery() as bq:
    # Portfolio weighted P/E
    result = bq.bql(
        "get(WAVG(GROUP(PE_RATIO), GROUP(id().weights)))"
        "for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))"
    )

    # Weighted P/E by sector
    result = bq.bql(
        "get(WAVG(GROUP(PE_RATIO), Group(id().weights)),"
        "    groupAvg(ev_to_ebitda, gics_sector_name))"
        "for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))"
    )

    # FI portfolio OAS by sector
    result = bq.bql(
        "get(AVG(GROUP(SPREAD(spread_type='OAS'), BICS_LEVEL_1_SECTOR_NAME)))"
        "for(members('FI_PORT_ID', type=PORT))"
    )

    # Duration-weighted OAS
    result = bq.bql(
        "get(wavg(group(spread(spread_type='OAS'), bics_level_1_sector_name),"
        "         group(duration(duration_type=MODIFIED), bics_level_1_sector_name)))"
        "for(members('FI_PORT_ID', type=PORT))"
    )

    # Portfolio weighted market cap
    result = bq.bql(
        "get(groupWAvg(cur_mkt_cap/1B, id.weights))"
        "for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))"
    )
```

## Total Return

```python
with BQuery() as bq:
    # 3-month total return per holding
    result = bq.bql(
        "get(TOTAL_RETURN(Calc_Interval=Range(-3M,0D), display_returns='Percent'))"
        "for(members('PORT_ID', type=PORT))"
    )

    # YTD total return
    result = bq.bql(
        "get(TOTAL_RETURN(Calc_Interval=YTD, display_returns='Percent'))"
        "for(members('PORT_ID', type=PORT))"
    )

    # Monthly total return series
    result = bq.bql(
        "get(total_return(return_type=TOTAL, calc_interval=MTD,"
        "    dates=range(-1y,0d), fill=prev))"
        "for(members('PORT_ID', type=PORT))"
    )

    # FI bond zero-coupon total return
    result = bq.bql(
        "get(TOTAL_RETURN(Calc_Interval=Range(-12M,0D),"
        "    Reinvestment_Type='Fixed', Reinvestment_Rate=0, display_returns='Percent'))"
        "for(members('FI_PORT_ID', type=PORT))"
    )

    # Portfolio vs benchmark cumulative return
    result = bq.bql(
        "let(#R = return_series(calc_interval=range(-2Y,0d), per=M);"
        "    #Cum = cumProd(dropna(#R)+1)-1;)"
        "get(#Cum)"
        "for(union([members('PORT_ID', type=PORT)], ['SPX Index']))"
    )
```

## Risk Analytics

```python
with BQuery() as bq:
    # Portfolio annualized volatility
    result = bq.bql(
        "get(sqrt(252)*std(day_to_day_total_return(dates=range(-1y,0d))))"
        "for(members('PORT_ID', type=PORT))"
    )

    # Max drawdown proxy
    result = bq.bql(
        "get(min(cumProd(1+dropNA(day_to_day_total_return(dates=range(-1Y,0d))))-1))"
        "for(members('PORT_ID', type=PORT))"
    )

    # 52-week cumulative return per holding
    result = bq.bql(
        "get(cumProd(1+dropNA(day_to_day_total_return(dates=range(-1Y,0d))))-1)"
        "for(members('PORT_ID', type=PORT))"
    )

    # Key rate durations for FI portfolio
    result = bq.bql(
        "get(KRD(TENOR=2Y), KRD(TENOR=5Y), KRD(TENOR=10Y), KRD(TENOR=30Y),"
        "    DV01, DURATION(DURATION_TYPE=MODIFIED))"
        "for(members('FI_PORT_ID', type=PORT))"
    )
```

## Entity Translation

```python
with BQuery() as bq:
    # Map bonds to equity tickers
    result = bq.bql(
        "for(translateSymbols(members('FI_PORT', type=PORT),"
        "    targetidtype='fundamentalticker'))"
        "get(name, pe_ratio, ev_to_ebitda, tot_debt_to_ebitda, gics_sector_name)"
    )

    # Map bonds to issuer
    result = bq.bql(
        "for(translateSymbols(members('FI_PORT', type=PORT),"
        "    instrumentidtype=Corp))"
        "get(name, gics_sector_name, cur_mkt_cap/1B)"
    )

    # Get issuer details from bond ISIN
    result = bq.bql(
        "for(issuerOf(['AZ791428 Corp']))"
        "get(name, gics_sector_name, cur_mkt_cap/1B, tot_debt_to_ebitda)"
    )

    # Fund holdings (ETF x-ray)
    result = bq.bql(
        "get(name, px_last, gics_sector_name, cur_mkt_cap/1B)"
        "for(holdings('HYG US Equity'))"
    )

    # Fund holdings historical
    result = bq.bql(
        "get(name, px_last, gics_sector_name)"
        "for(holdings('HYG US Equity', dates=-1y))"
    )
```

## Peer & Benchmark Comparison

```python
with BQuery() as bq:
    # Portfolio vs benchmark comparison
    result = bq.bql(
        "get(sum(group(id().weights, gics_sector_name)))"
        "for(union("
        "    [members('PORT_ID', type=PORT)],"
        "    [members('SPX Index')]"
        "))"
    )

    # Active weight by sector
    # (calculate portfolio weight - index weight in Python after fetching both)

    # Holdings overlap: portfolio vs ETF
    result = bq.bql(
        "for(intersect("
        "    members('PORT_ID', type=PORT),"
        "    holdings('QQQ US Equity')"
        "))"
        "get(name, cur_mkt_cap/1B)"
    )
```
