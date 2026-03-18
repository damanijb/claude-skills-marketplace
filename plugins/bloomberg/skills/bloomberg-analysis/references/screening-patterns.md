# BQL Screening Patterns Cookbook

## Equity Screens

```python
from polars_bloomberg import BQuery

with BQuery() as bq:
    # Value screen: low P/E + high margin
    result = bq.bql(
        "for(filter(members('SPX Index'),"
        "    pe_ratio<15 and gross_margin>40 and oper_margin>15))"
        "get(name, pe_ratio, gross_margin, oper_margin, cur_mkt_cap/1B)"
    )

    # Growth screen: revenue + EPS growth
    result = bq.bql(
        "for(filter(members('SPX Index'),"
        "    sales_5yr_avg_gr>10 and eps_growth>15 and oper_margin>20))"
        "get(name, sales_5yr_avg_gr, eps_growth, oper_margin, cur_mkt_cap/1B)"
    )

    # Quality screen: high ROE, low leverage
    result = bq.bql(
        "for(filter(members('SPX Index'),"
        "    return_com_eqy>20 and tot_debt_to_ebitda<2 and free_cash_flow_margin>10))"
        "get(name, return_com_eqy, tot_debt_to_ebitda, free_cash_flow_margin)"
    )

    # Momentum screen: price above 200-day MA
    result = bq.bql(
        "for(filter(members('SPX Index'),"
        "    px_last > avg(px_last(dates=range(-1Y,0D)))))"
        "get(name, px_last, day_to_day_total_return, cur_mkt_cap/1B)"
    )

    # Dividend screen
    result = bq.bql(
        "for(filter(members('INDU Index'),"
        "    is_div_per_shr > 0 and pe_ratio < 20 and return_com_eqy > 15))"
        "get(name, is_div_per_shr, pe_ratio, return_com_eqy)"
    )

    # Tech sector screen
    result = bq.bql(
        "for(filter(members('SPX Index'),"
        "    gics_sector_name=='Information Technology' and cur_mkt_cap>50B))"
        "get(name, cur_mkt_cap/1B, pe_ratio, ev_to_ebitda, sales_rev_turn/1B)"
    )

    # Large-cap global screen (requires mode=cached)
    result = bq.bql(
        "for(filter(equitiesUniv(['active','primary']),"
        "    cur_mkt_cap(currency=usd)>100B and return_com_eqy>20))"
        "get(name, cur_mkt_cap/1B, return_com_eqy, gics_sector_name)"
        "with(mode=cached)"
    )

    # SPX companies with keyword in description
    result = bq.bql(
        "for(filter(members('SPX Index'), contains(CIE_DES, 'artificial intelligence')))"
        "get(name, id)"
    )

    # Top 10 by market cap
    result = bq.bql(
        "for(top(members('SPX Index'), 10, CUR_MKT_CAP))"
        "get(name, cur_mkt_cap/1B, pe_ratio, ev_to_ebitda)"
    )

    # Peer comparison
    result = bq.bql(
        "for(union(['AAPL US Equity'], peers('AAPL US Equity', type=BLOOMBERG_BEST_FIT)))"
        "get(name, px_last, pe_ratio, ev_to_ebitda, gross_margin, oper_margin)"
    )
```

## Fixed Income Screens

```python
with BQuery() as bq:
    # Investment-grade bonds
    result = bq.bql(
        "for(filter(bondsUniv('Active'),"
        "    in(BB_composite, ['AAA','AA+','AA','AA-','A+','A','A-'])))"
        "get(sum(Group(amt_outstanding(currency=USD)))/1M)"
    )

    # High-yield: yield > 8%
    result = bq.bql(
        "for(filter(bondsUniv('Active'),"
        "    yield()>=8 and rating(source=BBG) in ['BB+','BB','BB-','B+','B','B-']))"
        "get(name, yield(yield_type=YTW), spread(spread_type='OAS'),"
        "    maturity_years, amt_outstanding/1M)"
    )

    # AAPL bonds maturing in 5-10 years
    result = bq.bql(
        "for(filter(bonds('AAPL US Equity'), BETWEEN(MATURITY, 5Y, 10Y)))"
        "get(ID, name, maturity, yield(yield_type=YTW), spread(spread_type='OAS'))"
    )

    # SSA EUR bonds outstanding
    result = bq.bql(
        "GET(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B)) as #AMT_EUR_Billion)"
        "FOR(FILTER(BONDSUNIV('ACTIVE'), MARKET_CLASSIFICATION=='SSA' AND Crncy==EUR))"
    )

    # EUR corporate maturity schedule by year
    result = bq.bql(
        "GET(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B, YEAR(MATURITY))))"
        "FOR(FILTER(BONDSUNIV('ACTIVE'), MARKET_CLASSIFICATION=='Corporate' AND Crncy==EUR))"
    )

    # Senior bonds, IG rated
    result = bq.bql(
        "for(filter(bondsUniv(Active),"
        "    RTG_SP>'BBB-' AND IN(PAYMENT_RANK, ['Sr Preferred','Sr Non Preferred'])))"
        "get(count(group(ID)))"
    )
```

## Sector / Group Analysis

```python
with BQuery() as bq:
    # Sector averages
    result = bq.bql(
        "for(members('INDU Index'))"
        "get(groupAvg(pe_ratio, gics_sector_name), groupAvg(ev_to_ebitda, gics_sector_name))"
    )

    # Z-scores vs index
    result = bq.bql(
        "for(members('SPX Index'))"
        "get(groupZscore(day_to_day_total_return(fill=prev)))"
    )

    # Sector count
    result = bq.bql(
        "for(members('SPX Index'))"
        "get(count(group(id, gics_sector_name)))"
    )

    # Market cap by country
    result = bq.bql(
        "for(filter(equitiesUniv(['active','primary']), cur_mkt_cap(currency=usd)>1B))"
        "get(sum(group(cur_mkt_cap(currency=usd)/1B, cntry_of_risk)))"
        "with(mode=cached)"
    )
```

## CDS Screens

```python
with BQuery() as bq:
    # 5Y CDS spreads for INDU members
    result = bq.bql(
        "get(long_comp_name as #name, cds_spread(pricing_source='CBGN').value as #spread)"
        "for(cds(members(['INDU Index']), tenor=5Y))"
    )

    # Implied vs market CDS spread
    result = bq.bql(
        "let(#Implied = RSK_BB_IMPLIED_CDS_SPREAD(dates=-1d,fill=prev).value;"
        "    #5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value,"
        "               cds(tenor=5Y), mapby=lineage).value;"
        "    #Spread = #Implied - #5Y;)"
        "get(name, #Implied, #5Y, #Spread)"
        "for(filter(members(['SPX Index']), #Implied*#5Y!=na))"
    )
```

## Fund Screens

```python
with BQuery() as bq:
    # Active US large-cap equity funds
    result = bq.bql(
        "for(filter(fundsUniv(['Primary','Active']),"
        "    FUND_GEO_FOCUS=='United States' AND FUND_MKT_CAP_FOCUS=='Large-Cap'))"
        "get(name, fund_total_assets/1B, fund_benchmark_prim, fund_mgmt_style)"
    )

    # ETFs with replication data
    result = bq.bql(
        "for(filter(fundsUniv(['Primary','Active']), FUND_TYP=='ETF'))"
        "get(name, replication_strategy, index_weighting_methodology, fund_total_assets/1B)"
    )
```
