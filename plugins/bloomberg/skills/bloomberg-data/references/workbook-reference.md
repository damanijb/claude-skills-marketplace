# Bloomberg Reference Workbooks — BQL Patterns

Content extracted from 13 Bloomberg reference workbooks (C:\blp\data).

---

## Workbook Index

| File | Topic |
|------|-------|
| 2085678.xlsx | BQL Quick Start & Equity Fundamentals |
| 2088954.xlsx | BQL for Funds |
| 2089580.xlsx | BQL Functions Complete Reference |
| 2090418.xlsx | BQL for Portfolios (Equity & FI) |
| 2096050.xlsx | Total Return & Cross-Asset Returns |
| 2097527.xlsx | CDS (Single Names & Indices) |
| 2098648.xlsx | Fixed Income Structured Products (FISP) |
| 2098844.xlsx | Fixed Income Full Reference |
| 2139460.xlsx | YAS Custom Analytics |
| 2142562.xlsx | Credit Ratings (rating() Data Model) |
| 2148204.xlsx | Market Sizing & Issuance Analysis |
| 2168185.xlsm | Agency CMBS Analytics |
| 2171225.xlsm | TRACE Trades & Spreads (MBS) |

---

## BQL Quick Start — Fundamentals (2085678)

```
# Single EPS
=BQL("IBM US Equity","IS_EPS")

# Annual EPS, specific offset
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=A", "FA_PERIOD_OFFSET=0")

# Last 5 years annual EPS
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=A", "FA_PERIOD_OFFSET=RANGE(-4,0)")

# Historical + forecast EPS
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=A", "FA_PERIOD_OFFSET=RANGE(-5,2)")

# Calendarized EPS 2010-2018
=BQL("ORCL US Equity","IS_EPS", "FA_PERIOD_TYPE=BA", "FA_PERIOD_REFERENCE=RANGE(2010,2018)")

# Quarterly EPS range
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=Q", "FA_PERIOD_REFERENCE=RANGE(2017Q1,2018Q4)")

# NTM EPS
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=BT", "FA_PERIOD_OFFSET=1")

# NTM EPS time series (estimates evolution)
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=BT", "FA_PERIOD_OFFSET=1","DATES=RANGE(2017-01-01,2017-06-01)")

# Point-in-time EPS as of date
=BQL("IBM US Equity","IS_EPS", "FA_PERIOD_TYPE=A", "FA_PERIOD_OFFSET=RANGE(-5,2)", "DATES=2015-06-01")

# Average PE ratio over 5 years
=BQL("IBM US Equity","AVG(DROPNA(PE_RATIO(DATES=RANGE(-5Y,0D), FA_PERIOD_TYPE=LTM)))")
```

### Custom Ratio Expressions (Piotroski-style scoring)
```
IF(ASSET_TURNOVER(FPO=0,FPT=A)>ASSET_TURNOVER(FPO=-1,FPT=A),1,0)   # Asset turnover improving
IF(CF_CASH_FROM_OPER(FPO=0,FPT=A)>0,1,0)                            # Positive cash from ops
IF(CUR_RATIO(FPO=0,FPT=A)>CUR_RATIO(FPO=-1,FPT=A),1,0)             # Improving current ratio
IF(CF_CASH_FROM_OPER(FPO=0,FPT=A)>NET_INCOME(FPO=0,FPT=A),1,0)     # Earnings quality
IF(LT_DEBT_TO_TOT_ASSET(FPO=0,FPT=A)>LT_DEBT_TO_TOT_ASSET(FPO=-1,FPT=A),1,0)  # LT debt ratio
IF(RETURN_ON_ASSET(FPO=0,FPT=A)>RETURN_ON_ASSET(FPO=-1,FPT=A),1,0) # ROA improving
```

---

## Funds Analysis (2088954)

### Risk/Return Metrics
```
# Sharpe ratio for a period
=BQL("SPY US Equity","Sharpe_ratio(calc_interval=range(2018-01-01, 2018-06-30))")

# Rolling 1Y Sharpe (monthly, on specific date)
=BQL("EUE IM Equity","Rolling(Sharpe_ratio(calc_interval='1Y'), iterationdates=range(2018-02-05, 2018-02-05))")

# Rolling monthly Sharpe over 1 year
=BQL("SPY US Equity","Rolling(Sharpe_ratio(1Y, ann_factor=252), range(-1Y,0d, frq=m))")

# Sharpe with custom risk-free rate
rolling(SHARPE_RATIO(Calc_Interval=1y,TR_Base=Price_If_Available,Ann_Factor=252,RISK_FREE_TICKER=['USGG3M Index']),iterationdates=range(2018-01-01,2018-06-01))

# BQL query version
get(rolling(SHARPE_RATIO(Calc_Interval=1y,TR_Base=Price_If_Available,RISK_FREE_TICKER=['USGG3M Index']), iterationdates=range(2018-01-01,2018-06-01)) for(['SPY US Equity'])
```

### Fund Comparison Sheet Metrics
```
# Total return at various horizons (as-of a date)
PX_LAST(FILL=PREV, CURRENCY=USD, START=2026-03-02, END=2026-03-02)
rolling(TOTAL_RETURN(CALC_INTERVAL=1M,CURRENCY=USD), iterationdates=range(2026-03-02,2026-03-02))
rolling(TOTAL_RETURN(CALC_INTERVAL=6M,CURRENCY=USD), iterationdates=range(2026-03-02,2026-03-02))
rolling(TOTAL_RETURN(CALC_INTERVAL=1Y,CURRENCY=USD), iterationdates=range(2026-03-02,2026-03-02))
ANN_TOTAL_RETURN(CALC_INTERVAL=RANGE(2018-01-01,2018-06-08),CURRENCY=USD)
rolling(SHARPE_RATIO(CALC_INTERVAL=1Y,CURRENCY=USD,PER=W), iterationdates=range(2026-03-02,2026-03-02))
```

### Fund Screening & Top N by Assets
```
# Filter fund universe
FILTER(Fundsuniv(['Active','Primary']),FUND_TYP=='Open-End Fund' AND FUND_STRATEGY=='Macro')

# Top 10 funds by AUM
let(
    #FundData=FUND_TOTAL_ASSETS(CURRENCY=USD, fill=prev);
)
get(GROUPSORT(#FundData,Order=DESC) as #FUND_ASSETS_USD)
for(filter(FILTER(Fundsuniv(['Active','Primary']),FUND_TYP=='Open-End Fund' AND FUND_STRATEGY=='Macro'),
    ungroup(rank(group(#FundData),Order=DESC))<=10))

# ETF count by strategy
get(count(group(ID, FUND_STRATEGY))) for(filter(FundsUniv(['Primary','Active']), FUND_TYP=='ETF'))
```

### ETF Fund Flows by Strategy
```
let(
    #DailyFundFlows = FUND_FLOW(START=2017-01-01, END=2024-01-01, CURRENCY=USD)/10^9;
    #AggregatedFundFlows = SUM(GROUP(#DailyFundFlows,FUND_STRATEGY));
    #SortedFundFlows = GROUPSORT(#AggregatedFundFlows);
)
get(#SortedFundFlows)
for(filter(FundsUniv(['Active','Primary']), FUND_TYP=='ETF'))
with(MODE=CACHED)
```

### Risk/Return Field Reference
| Field | Description | Key Params |
|-------|-------------|------------|
| `TOTAL_RETURN` | Holding period return | `Calc_Interval`, `Currency` |
| `ANN_TOT_RETURN` | Annualized holding period return | `Calc_Interval`, `Currency` |
| `RETURN_SERIES` | Period-over-period returns time series | `Calc_Interval`, `Per` |
| `SHARPE_RATIO` | Return / Std Dev of returns | `Calc_Interval`, `Ann_Factor`, `Risk_Free_Ticker` |
| `SORTINO_RATIO` | Return / Downside volatility | `Calc_Interval`, `Ann_Factor`, `Target_Return` |
| `DOWNSIDE_VOLATILITY` | Std dev of returns below target | `Calc_Interval`, `Per` |

### Fund Fields Reference
| Field | Description |
|-------|-------------|
| `FUND_NET_ASSET_VAL` | Net Asset Value (NAV) |
| `FUND_TOTAL_ASSETS` | Fund total assets (AUM) |
| `FUND_MANAGEMENT_CO` | Management company |
| `FUND_BENCHMARK_PRIM` | Primary benchmark ticker |
| `FUND_OBJECTIVE_LONG` | Fund objective (Bloomberg classification) |
| `FUND_RTG_CLASS_FOCUS` | Rating class focus (HY, IG) |
| `FUND_MKT_CAP_FOCUS` | Market cap focus (Large/Mid/Small-cap) |
| `FUND_STRATEGY` | Investment strategy |
| `FUND_MGMT_STYLE` | Active/Passive |
| `FUND_GEO_FOCUS` | Geographic focus |
| `FUND_ASSET_CLASS_FOCUS` | Asset class focus |
| `FUND_INDUSTRY_FOCUS` | Industry focus |
| `FUND_LEVERAGE_TYPE` | Leverage type |
| `FUND_DOMICILE_TYP` | Domicile type |
| `FUND_MATURITY_BAND_FOCUS` | Maturity band focus |
| `MGR_COUNTRY_NAME` | Manager country |

---

## BQL Functions Reference (2089580)

### Arithmetic
```
for(members('INDU Index')) get(groupavg(abs(pe_ratio-groupavg(pe_ratio))))  # MAD dispersion
for('AAPL US Equity') get(ceil(px_last))
for('AAPL US Equity') get(floor(px_last))
for('AAPL US Equity') get(exp(1))
for('AAPL US Equity') get(ln(2.718282))
for('AAPL US Equity') get(log(1000))
for(members('INDU Index')) get(round(is_eps, 2))
for(members('SPX Index')) get(sign(is_eps))
for('AAPL US Equity') get(sqrt(12321))
for('AAPL US Equity') get(square(11))
for('AAPL US Equity') get(mod(100,7))
for('AAPL US Equity') get(-px_last)
for('AAPL US Equity') get(2^10)
for(members('SPX Index')) get(normal_dist(groupZscore(pe_ratio)))
for(members('SPX Index')) get(normal_inv(0.025+normal_dist(groupZscore(pe_ratio))))
```

### Statistical
```
for('AAPL US Equity') get(sum(px_volume(dates=range(-1W, 0D))))
for('AAPL US Equity') get(count(px_last(dates=range(-1y,0d))))
for('AAPL US Equity') get(avg(px_last(dates=range(-3m,0d))))
for('AAPL US Equity') get(wAvg(px_last,px_volume)) with(dates=range(-1y,0y),frq=d)
for('AAPL US Equity') get(min(day_to_day_total_return(dates=range(-1y,0d))))
for('AAPL US Equity') get(max(day_to_day_total_return(dates=range(-1y,0d))))
for('AAPL US Equity') get(median(day_to_day_total_return(dates=range(-1y,0d))))
for(members('INDU Index')) get(product(1+dropna(day_to_day_total_return(dates=range(-1m,0d))))-1)
for(members('INDU Index',dates=0d)) get(corr(dropna(px_volume),dropna(day_to_day_total_return))) with(dates=range(-1m,-1d))
for(members('INDU Index')) get(rsq([1,2,3,4,5,6,7,8,9,10],is_eps(ae=a,fpt=a,fpo=range(-9Y,0Y))))
for('INDU Index') get(sqrt(260)*std(day_to_day_total_return(dates=range(-1y,0d))))
for('INDU Index') get(skew(day_to_day_total_return(dates=range(-1y,0d))))
for('AAPL US Equity') get(kurt(day_to_day_total_return(dates=range(-1y,0d))))
for('AAPL US Equity') get(zScore(dropna(day_to_day_total_return(dates=range(-1m,0d)))))
for('AAPL US Equity') get(winsorize(dropna(day_to_day_total_return(dates=range(-1m,0d))),threshold_type=STD, lower_limit=2.0, upper_limit=2.0))
for('AAPL US Equity') get(compoundGrowthRate(px_last)) with(dates=range(-20y,0y,frq=y),fill=prev)
for('AAPL US Equity') get(dropna(matches(day_to_day_total_return, cut(day_to_day_total_return,10)==10))) with(dates=range(-6m,0d))
for('M US Equity') get(rank(px_last(dates=range(-6m,0d))))
for(['IBM US Equity']) get(quantile(px_last(dates=range(-1Y, 0D)), 0.25))
for(members('INDU Index',dates=0d)) get(slope(dropna(px_volume),dropna(day_to_day_total_return))) with(dates=range(-1m,-1d))
for(members('INDU Index',dates=0d)) get(intercept(dropna(px_volume),dropna(day_to_day_total_return))) with(dates=range(-1m,-1d))
```

### Grouping Functions
```
for(members('SPX Index')) get(group(is_eps, gics_sector_name))
for(members(['SPX Index'])) get(ungroup(skew(group(is_eps, gics_sector_name))))
for(members('SPX Index')) get(groupAvg(is_eps, gics_sector_name))
for(members('SPX Index')) get(groupCount(interest_income))
for(members('INDU Index')) get(groupMax(sales_rev_turn))
for(members('INDU Index')) get(groupMedian(pe_ratio, gics_sector_name))
for(members('INDU Index')) get(groupMin(pe_ratio))
for(members('INDU Index')) get(groupRank(bs_cash_near_cash_item))
for(members('INDU Index')) get(groupStd(day_to_day_total_return(fill=prev)))
for(members('INDU Index')) get(groupSum(eqy_sh_out))
for(members('INDU Index')) get(groupWAvg(pe_ratio,id.weights))
for(members('INDU Index')) get(groupZscore(day_to_day_total_return(fill=prev)))
for(members('INDU Index')) get(groupCut(day_to_day_total_return(fill=prev), n=100))
for(members('INDU Index')) get(groupWinsorize(day_to_day_total_return(fill=prev)))
for(members('INDU Index')) get(groupSort(ev_to_ebitda))
```

### Time Series Manipulation
```
for('AAPL US Equity') get(cumAvg(dropNA(is_eps(fpt=a,fpo=1Y,dates=range(-3m,0d)))))
for('AAPL US Equity') get(cumMax(dropNA(px_last(dates=range(-1y,0d)))))
for('GE US Equity') get(cumMin(dropNA(px_last(dates=range(-1y,0d)))))
for('AAPL US Equity') get(cumProd(1+dropNA(day_to_day_total_return(dates=range(-3M,0d))))-1)
for('AAPL US Equity') get(cumSum(dropNA(px_volume(dates=range(-6m,0d)))))
for('AAPL US Equity') get(dropNA(if(diff(eqy_sh_out)==0,nan,diff(eqy_sh_out)))) with(dates=range(-2y,0d))
for('GE US Equity') get(net_chg(dropNA(cur_mkt_cap(dates=range(2018-01-01,today))))/100)
for('GE US Equity') get(pct_chg(dropNA(cur_mkt_cap(dates=range(2018-01-01,today))))/100)
for('GE US Equity') get(pct_diff(dropNA(cur_mkt_cap(dates=range(2018-01-01,today))), step=7)/100)
for('AAPL US Equity') get(rolling(avg(px_last(-1m,0d)),iterationdates=range(-1y,0d)))
```

### Date Functions
```
for('AAPL US Equity') get(today())
for('AAPL US Equity') get(year(today()))
for('SPX Index') get(groupavg(day_to_day_total_return,month(day_to_day_total_return().date))) with(dates=range(-9y,0d),per=m)
for('SPX Index') get(avg(dropNA(if(dayOfWeek(day_to_day_total_return().date)==3, day_to_day_total_return,nan)))) with(dates=range(-5y,0d))
for('INTC US Equity') get(dropNA(if(dayOfMonth(px_volume().date)==1,px_volume,nan))) with(dates=range(-3y,0d),fill=prev)
for(cds('VOD LN Equity')) get(px_last(dates = date(year(today())-1,12,20)))
for('VOD LN Equity') get(px_last(dates=startOfMonth-1d))
for('VOD LN Equity') get(px_last(dates=startOfQuarter-1d))
for('VOD LN Equity') get(px_last(dates=startOfYear-1d))
for('US Country') get(calendar(type=ECONOMIC_RELEASES, dates=range(0d,endOfMonth)))
for('MSFT US Equity') get(px_last(dates=wtd))
for('MSFT US Equity') get(px_last(dates=mtd))
for('MSFT US Equity') get(px_last(dates=qtd))
for('MSFT US Equity') get(px_last(dates=ytd))
for('SPX Index') get(px_last(dates=range(-2cy, -1cy, frq=d)))   # calendar year range
```

### String Functions
```
for('AAPL US Equity') get(name + ' - ' + gics_sector_name)
for(members('INDU Index')) get(left(is_eps(fpt=a,fpo=0).period,4))
for('AAPL US Equity') get(name,len(name))
for('AAPL US Equity') get(replace(name,toscalar(len(name)-2),3,'incorporated'))
for('AAPL US Equity') get(right(is_eps(fpo=range(1Q,4Q),fpt=q).period,2))
for(members('INDU Index')) get(gics_sector_name,startsWith(gics_sector_name,'consumer'))
for('AAPL US Equity') get(toLower(name))
for('AAPL US Equity') get(toUpper(name))
for(filter(members('SPX Index'), contains(CIE_DES, "gold"))) get(id)
```

### Filtering & Conditionals
```
for(filter(members('INDU Index'),px_last>200)) get(px_last)
for(top(members('INDU Index'),10,CUR_MKT_CAP)) get(cur_mkt_cap/1M)
for(bottom(members('INDU Index'),10,CUR_MKT_CAP)) get(cur_mkt_cap/1M)
for(members('INDU Index')) get(if(pe_ratio>20,"overvalued","undervalued"))
for(members('INDU Index')) get(pe_ratio<20 and px_last>100)
for(members('INDU Index')) get(gics_sector_name in ['Financials','Consumer Discretionary'])
for(members('INDU Index')) get(not(gics_sector_name=='Energy'))
for(members('INDU Index')) get(gics_sector_name!='Financials')
for(members('INDU Index')) get(pe_ratio<20 or px_last>100)
for(members('INDU Index')) get(gics_sector_name=='Financials' xor sales_rev_turn>100B)
for('AAPL US Equity') get(all(day_to_day_total_return(dates=range(2018-08-13,2018-08-17))>0))
for('AAPL US Equity') get(any(day_to_day_total_return(dates=range(2018-08-20,2018-08-24))<0))
for(members('INDU Index')) get(between(px_last,100,200))
for('AAPL US Equity') get(matches(day_to_day_total_return,px_volume>35M)) with(dates=range(2018-08-01,2018-08-31))
```

### Data Handling
```
for(members('SPX Index')) get(avail(is_eps(fpt=ltm,fpo=3Y),is_eps(fpt=a,fpo=3Y)))
for('IBM US Equity') get(dropNA(px_last(dates=range(-100d,0d))))
for('MSFT US Equity') get(zNAV(day_to_day_total_return(dates=range(-100d,0d))))
for('AAPL US Equity') get(product(1+replaceNonNumeric(day_to_day_total_return,0))-1) with(dates=range(-1m,0d))
for('TSLA US Equity') get(first(dropna(px_last(dates=range(-3m,0d))),10))
for('AAPL US Equity') get(last(dropNA(is_eps,8)) with(fpt=a,fpr=2017-09-30,dates=range(2017-07-01,2017-09-30),ae=e))
for('M US Equity') get(sort(dropna(px_last(dates=range(-6m,0d))),order=desc))
for(members('INDU Index')) get(groupSort(ev_to_ebitda))
for('AAPL US Equity') get(corr(day_to_day_total_return,value(day_to_day_total_return,relativeindex))) with(dates=range(-12m,0d))
```

### Security Universes
```
# Large-cap equities (use mode=cached)
for(filter(equitiesUniv(['active','primary']), cur_mkt_cap(currency=usd)>100B))
get(count(group(id))) with(mode=cached)

# Fund universe
for(filter(fundsUniv(['Primary','Active']),mgr_country_name=='Argentina' and fund_geo_focus=='U.S.'))
get(name) with(mode=cached)

# Bond universe filters
for(filter(bondsUniv('active'),amt_outstanding(currency=usd)>100B)) get(crncy)
for(filter(debtUniv('ACTIVE'), yield()>=14 and crncy()=='USD' and callable()==FALSE and maturity()>=5Y)) get(name)
for(filter(municipalsUniv(ACTIVE), defaulted()==TRUE and amt_outstanding(currency=USD)>100M)) get(id)
for(loansUniv('active')) get(count(group(id)))
for(filter(mortgagesUniv(ACTIVE), mtg_deal_typ()=='CMO' and callable()=='Y' and mtg_factor()<=0.1 and mtg_delinquencies_pct()<3 and px_ask()<100 and issue_dt()>2010-07-31))
for(filter(preferredsUniv(ACTIVE), callable()==Y and cpn()>6)) get(id)
for(countries(['g8'])) get(cpi)
```

### Security Chains & Related Entities
```
for(members('INDU Index')) get(px_last)
for(peers('TSLA US Equity', type=BLOOMBERG_BEST_FIT)) get(id)
for(segments(['AAPL US Equity'])) get(segment_name, sales_rev_turn)
for(bonds(members('INDU Index'))) get(count(group(id)))
for(loans('MSFT US Equity')) get(cpn_typ)
for(mortgages(['MS US Equity'])) get(id)
for(preferreds(['GE US Equity'])) get(id)
for(debt(['GE US Equity'])) get(id)
for(options('AAPL US Equity')) get(sum(group(open_int)))
for(futures(['CLA Comdty'])) get(id)
for(curveMembers('YCGT0025 Index')) get(rate)

# Related entities
for(fundamentalTicker(members('SHSZ300 index'))) get(is_eps)
for(relativeIndex(['AAPL US Equity','VOD LN Equity'])) get(id)
for(translateSymbols(members('SHSZ300 index'), targetidtype='fundamentalticker')) get(is_eps)
for(issuerOf(['AZ791428 Corp'])) get(name)
for(parent(['FIAT GR Equity'])) get(name)
for(equitypricingticker(['FIAT GR Equity'])) get(name)
for(esgTicker(['FIAT GR Equity'])) get(name)
for(cds('TSLA US Equity')) get(cds_spread)

# User screens / axed universe
for(screenResults(SRCH, '@COCO')) get(name)
for(filter(axedUniv(ASK), crncy()==EUR)) get(name)

# Set operations
for(union(members(['INDU Index']), ['PEP US Equity', 'T US Equity', 'LOW US Equity'])) get(px_last)
for(intersect(members(['SX5E Index']), members(['CAC Index']))) get(id)
for(setDiff(members(['LEGATRUU Index']), members(['LEGASTAT Index']))) get(id)
for(list(['IBM US Equity', 'AAPL US Equity', 'VOD LN Equity'])) get(px_volume)
for(top(members(['SPX INDEX']), 5, num_of_employees)) get(id)
for(bottom(members(['SPX INDEX']), 5, pe_ratio)) get(id)
```

---

## Portfolio Analysis (2090418)

### Equity Portfolio
```
# All holdings
get(NAME) for(members('U17911388-100',type=PORT))

# Multiple portfolios combined
get(NAME) for(Members(symbols=['U17911388-167','U17911388-100'],type=PORT))

# Translate to fundamental tickers
get(NAME) for(translateSymbols(Members('U17911388-100',type=PORT), targetidtype='fundamentalticker'))

# Common stock only, translated
get(NAME) for(translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker'))

# Average PE ratio
get(AVG(GROUP(PE_RATIO))) for(translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker'))

# Weighted average PE ratio
get(WAVG(GROUP(PE_RATIO),Group(id().weights))) for(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'))

# Sector average PE
get(AVG(GROUP(PE_RATIO,GICS_SECTOR_NAME))) for(translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker'))

# Portfolio vs benchmark
get(AVG(Group(PE_RATIO))) for(UNION(members('INDU Index'),members('U17911388-100',type=PORT)))

# Holdings not in SPX (off-benchmark)
get(NAME) for(SETDIFF(members('U17911388-100',type=PORT),translatesymbols(members('SPX Index'),targetidtype='fundamentalticker')))
```

### FI Portfolio
```
# Holdings list
get(LONG_COMP_NAME) for(members('U17911388-100',type=PORT))

# Count by credit rating
get(COUNT(GROUP(id,CREDIT_RATING))) for(Members('U17911388-100',type=PORT))

# Sum of weights by credit rating (Fixed Weight portfolios)
get(sum(group(id().weights, credit_rating))) for(members('U17911388-181',type=PORT))

# Sum of positions by credit rating (Drifting Weight portfolios)
get(sum(group(id().positions, credit_rating))) for(members('U17911388-181',type=PORT))

# Multi-category grouping (credit rating x maturity year)
get(count(group(id, [credit_rating,YEAR(MATURITY)]))) for(filter(members('U17911388-181',type=PORT),MATURITY<2050-01-01))

# Sector average OAS
get(AVG(GROUP(SPREAD(spread_type='OAS'),BICS_LEVEL_1_SECTOR_NAME))) for(members('U17911388-181',type=PORT))

# Median current ratio for FI index translated to equity
get(MEDIAN(GROUP(DROPNA(CUR_RATIO,remove_id=true)))) for(translateSymbols(Members('LBEASTAT Index'), targetIdType='FUNDAMENTALTICKER',instrumentidtype=Corp)) with(mode=cached)

# Net debt/EBITDA for FI portfolio
get(MEDIAN(GROUP(dropna(NET_DEBT_TO_EBITDA,remove_id=true)))) for(translateSymbols(Members('U1838317-300',type=PORT), targetIdType='FUNDAMENTALTICKER',instrumentidtype=Corp))
```

---

## Total Return Analysis (2096050)

### Bond Total Return vs Return Series
```
# Holding period total return (3M)
=BQL("EC527035 Corp","TOTAL_RETURN(Calc_Interval=Range(-3M,0D),display_returns='Percent')")

# Total return (11M, decimal)
=BQL("EC527035 Corp","TOTAL_RETURN(Calc_Interval=Range(-11M,0D))")

# With fixed reinvestment rate
=BQL("EC527035 Corp","TOTAL_RETURN(Calc_Interval=Range(-1M,0D),Reinvestment_Type='Fixed',Reinvestment_Rate=3)")

# Zero-coupon (no reinvestment) total return
=BQL("EC527035 Corp","TOTAL_RETURN(Calc_Interval=Range(-12M,0D),Reinvestment_Type='Fixed',Reinvestment_Rate=0,display_returns='Percent')")

# Return series with spread and yield (daily)
let(
    #returns = return_series(Calc_interval=range(2022-02-01,2022-02-06),per=D);
    #Spread = spread(st=z,dates=range(2022-02-01,2022-02-06),per=D);
    #Yield = yield(yt=YTW, dates=range(2022-02-01,2022-02-06),per=D);
)
get(#returns,#Spread,#Yield) for('ZS584499 Corp')

# Cumulative returns (monthly)
let(
    #Returns = return_series(calc_interval=range(-2Y,0d),per=M);
    #Cumulative_Returns = cumprod(dropna(#Returns)+1)-1;
)
get(#Cumulative_Returns) for('BACR0 Index')
```

### Cross-Asset Return Correlation
```
let(
    #returns = return_series(Calc_interval=range(-1Y,0d));
    #returns_fi = value(#returns,['LUACTRUU Index']);
    #returns_eq = value(#returns,['SPX Index']);
    #correl = corr(#returns_fi,#returns_eq);
    #cpi = px_last;
)
get(rolling(#correl,range(-20Y,0d,frq=Q)) as #Corr,rolling(#cpi,range(-20Y,0d,frq=Q)) as #Inflation)
for('CPI YOY Index')
```

### Returns Heatmap (Portfolio/Index)
```
# Weighted average total return by rating bucket
let(#Returns = total_return(calc_interval=range(2026-03-12-3M,2026-03-12),reinvestment_type='Fixed');)
get(wavg(group(#Returns),group(id().weights)))
for(members('I02885JP Index',dates=2026-03-12))
```

---

## CDS Analysis (2097527)

### Single Names
```
# Get CDS ticker IDs
get(id()) for(cds('JPM US Equity', tenor=2Y))
get(id()) for(cds('JPM US Equity', tenor=5Y))
get(id()) for(cds('GM US Equity', tenor=3Y))

# CDS spreads (various tenors and sources)
get(cds_spread) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread(pricing_source=CBBT)) for(cds('JPM US Equity', tenor=2Y))
get(cds_spread(pricing_source=CBIN)) for(cds('JPM US Equity', tenor=10Y))
get(cds_spread(dates=-1m)) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread(dates=range(-1m,0d))) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread(dates=range(2021-01-01,2024-01-01))) for(cds('JPM US Equity'))
get(cds_spread(fill=prev, dates=range(2021-01-01,2024-01-01))) for(cds('JPM US Equity'))

# Custom list (bonds and equities mixed)
get(name, px_last(pricing_source=CBIN).value as #spread)
for(CDS(['ibm us equity','vod ln equity','EI798988 Corp','ZB310991 Corp']))

# CDS term structure (let + value + mapby=lineage)
let(
    #3Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=3Y),mapby=lineage).value;
    #5Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=5Y),mapby=lineage).value;
    #7Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=7Y),mapby=lineage).value;
    #10Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=10Y),mapby=lineage).value;
)
get(name, #3Y, #5Y, #7Y, #10Y) for(members('INDU Index'))

# Implied CDS vs market spread for banking sector
let(
    #Implied_CDS = RSK_BB_IMPLIED_CDS_SPREAD(dates=-1d,fill=prev).value;
    #5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, CDS(tenor=5Y),mapby=lineage);
    #Spread = #Implied_CDS-#5Y;
)
get(name, #Implied_CDS, #5Y, #Spread)
for(filter(members(['SPX Index']),Classification_Name(BICS,3)=='Banking' and #Implied_CDS*#5Y!=na))

# CDS 1-year spread change by sector
let(
    #spread=dropna(cds_spread(pricing_source='CBGN',dates=range(2020-03-01,2020-12-31)));
    #pct_chg=pct_chg(#spread);
)
get(groupsort(avg(group(#pct_chg, industry_sector))) as #credit_per_chg)
for(CDS(members(['SPX Index']), tenor=5Y))
```

### CDS Pricing Sources
| Source | Description |
|--------|-------------|
| CBBT | Composite Bloomberg Bond Trader |
| CBIL | BBG CDS Intra LN |
| CBIN | BBG CDS Intra NY |
| CBIT | BBG CDS Intra TK |
| CBGL | BBG CDS 5:15PM LN |
| CBGN | BBG CDS 5:15PM NY |
| CBGT | BBG CDS 5:15PM TK |

### CDS Index Membership
```
# Count members in CDS index
get(count(group(id) as #count)) for(members(['ITRXEXE Curncy']))

# Historical membership (6 months ago)
get(id) for(members('ITRXEXE Curncy', dates=-6m))

# Reference + market data for index members
get(name, crncy, seniority, cds_tenor, credit_rating_grade_indicator as #rating,
    classification_name as #sector, px_last().value as #spread, probability_of_default_cds().value as #1y_def_prob)
for(members(['ITRXESE Curncy']))

# Filter by sector
get(name, px_last().value as #spread)
for(filter(members(['ITRXEXE Curncy']), classification_name==Energy))

# Compare series (added/removed constituents)
get(name) for(setdiff(members('CDX IG CDSI S43 5Y Corp'),members('CDX IG CDSI S42 5Y Corp')))
get(name) for(setdiff(members('CDX IG CDSI S42 5Y Corp'),members('CDX IG CDSI S43 5Y Corp')))

# CDS index tickers reference
# ITRXEXE Curncy  = MARKIT ITRX EUR XOVER
# ITRXESE Curncy  = MARKIT ITRX EUR SNR FIN
# IBOXUMAE Curncy = MARKIT CDX.NA.IG
# IBOXHYAE Index  = MARKIT CDX.NA.HY
```

---

## Fixed Income Structured Products (2098648 & 2171225)

### FISP Analytics
```
# Yield types for securitized
get(yield(yield_type='CONVENTION')) for('3137H8QV6')
get(yield(yield_type='YTW')) for('3137H8QV6')
get(yield(yield_type='YTM')) for('3137H8QV6')
get(yield(yield_type='YTC')) for('3137H8QV6')

# With side and pricing source
get(yield(yield_type='EFFECTIVE', side='BID', PRICING_SOURCE='BVAL')) for('3137H8QV6')

# Historical yield
get(yield(yield_type='I', dates=range(-3m,0d), fill=prev)) for('3137H8QV6')

# Spread types for securitized
get(spread(spread_type='Z')) for('3137H8QV6')
get(spread(spread_type='I')) for('3137H8QV6')
get(spread(spread_type='OAS')) for('3137H8QV6')
get(spread(spread_type='N')) for('3137H8QV6')
get(spread(spread_type='E')) for('3137H8QV6')
get(spread(spread_type='J')) for('3137H8QV6')
get(spread(spread_type='A')) for('3137H8QV6')
get(spread(spread_type='P')) for('3137H8QV6')
get(spread(spread_type='R')) for('3137H8QV6')
get(spread(spread_type='ZV_OAS')) for('3137H8QV6')

# Duration types
get(duration(duration_type='SPREAD')) for('3137H8QV6')
get(duration(duration_type='EFFECTIVE')) for('3137H8QV6')
get(duration(duration_type='MODIFIED')) for('3137H8QV6')
get(duration(duration_type='MACAULAY')) for('3137H8QV6')

# Convexity
get(convexity(dates=range(-3m,0d),fill=prev)) for('3137H8QV6')

# Key rate durations for securitized
get(KEY_RATE_DUR_6MO) for('FHR 5100 AB Mtge')
get(KEY_RATE_DUR_1YR) for('FHR 5100 AB Mtge')
get(KEY_RATE_DUR_2YR) for('FHR 5100 AB Mtge')
get(KEY_RATE_DUR_5YR) for('FHR 5100 AB Mtge')
get(KEY_RATE_DUR_10YR) for('FHR 5100 AB Mtge')
get(KEY_RATE_DUR_30YR) for('FHR 5100 AB Mtge')
```

### Spread Type Definitions
| Type | Description |
|------|-------------|
| Z | Cash flow spread to spot sovereign curve |
| I | Conventional yield spread to interpolated sovereign |
| OAS | Option-adjusted spread (Monte Carlo) |
| N | Yield spread to swap curve (nominal maturities) |
| E | SOFR Futures curve spread (post Apr 2023) |
| J | Yield spread to sovereign curve (nominal maturities) |
| A | Spread to sovereign bond with closest nominal maturity to WAL |
| P | Spread to risk-free rate swap curve (actual maturities) |
| R | Cash flow spread to risk-free rate spot curve (SOFR/SONIA/SARON) |
| ZV_OAS | Zero-volatility OAS (0% vol assumption) |

### Securitized Screening
```
# Active MBS universe
mortgagesuniv('active')

# Count from saved SRCH screen
get(count(group(id))) for(screenresults(SRCH, screen_name='@IABS'))

# Average I-spread of US Auto ABS by rating
get(groupsort(avg(group(spread(spread_type=I), rtg_sp)), order=desc) as #Average_I_Spread)
for(filter(mortgagesuniv(Active), structured_prod_class_ast_subcl=='CARS'
    AND maturity <= 3Y AND crncy=='USD'))

# Top 20 auto ABS monitor by spread change
let(
    #I_spread = spread(spread_type=I, fill=prev).value;
    #1W_I_spread_change = net_chg(spread(spread_type=I, dates=range(-1w,0d), fill=prev)).value;
    #rank = grouprank(#1W_I_spread_change);
    #Name = groupsort(name, sortby=#1W_I_spread_change, order=desc);
    #Delinquencies_Pct = mtg_delinquencies_pct;
)
get(#Name, #I_spread, #1W_I_spread_change, #Delinquencies_Pct)
for(filter(filter(mortgagesuniv(Active), structured_prod_class_ast_subcl=='CARS'
    AND maturity <= 3Y and rtg_sp>'BB+' AND mtg_wal>=0.5), #rank<=20))
```

### Expanded FISP Fields
| Field | Domain | Description |
|-------|--------|-------------|
| `EXTENDED_CASH_FLOW` | Cash Flow | Extended cashflows |
| `MTG_CASH_FLOW` | Cash Flow | Projected cashflows |
| `HIST_CASH_FLOW` | Historical | Historical cashflows |
| `PROJ_PREPAYMENT_SPEEDS_IN_CPR` | Cash Flow | Projected CPR |
| `CDR_VECTOR_PROJ_BY_CREDIT_MOD` | Cash Flow | CDR vector by credit model |

### CLO / ABS Market Analysis
```
# Total outstanding UK RMBS by next call date
get(sum(group(amt_outstanding/1B, year(NXT_CALL_DT))) as #Amt_Out_GBP_Blns)
for(filter(mortgagesuniv('active'), MTG_DEAL_TYP=='CMO' and CRNCY=='GBP' AND NEXT_CALL_DT!=NA))

# CLO issuance USD vs EUR (last 5 years)
get(sum(group(MTG_ORIG_AMT,[crncy, year(issue_dt)]))/1B as #Issuance)
for(filter(mortgagesuniv('all'), MTG_DEAL_TYP=='CLO' AND ISSUE_DT>=2016-01-01 and IN(CRNCY, ['USD', 'EUR'])))

# CLO top tranche average spread by year
get(avg(group(BASIC_SPREAD, year(ISSUE_DT))) as #Avg_Coupon)
for(filter(mortgagesuniv('all'), MTG_DEAL_TYP=='CLO' AND CRNCY=='EUR' AND TRANCHE_NUM==1 and ISSUE_DT>=2017-01-01))
```

---

## Fixed Income Full Reference (2098844)

### Pricing Source Comparison
```
# Compare yield across multiple pricing sources
let(
    #Company_Name=long_comp_name();
    #amt_outstanding_millions=amt_outstanding().value/1000000;
    #YIELDUCIB=dropNA((yield(pricing_source=UCIB).value), remove_ID=TRUE);
    #YIELDTRAC=dropNA((yield(pricing_source=TRAC).value), remove_ID=TRUE);
    #YIELDFRNK=dropNA((yield(pricing_source=FRNK).value), remove_ID=TRUE);
    #YIELDBGN=dropNA((yield(pricing_source=BGN).value), remove_ID=TRUE);
    #YIELDBVAL=dropNA((yield(pricing_source=BVAL).value), remove_ID=TRUE);
    #AVERAGE=dropNA(avg(yield(pricing_source=UCIB).value, yield(pricing_source=TRAC).value,
        yield(pricing_source=FRNK).value, yield(pricing_source=BGN).value, yield(pricing_source=BVAL).value));
)
get(groupsort(#YIELDBMRK) as #SortedYIELD, #AVERAGE, #YIELDUCIB, ...)
for([CUSIP1, CUSIP2, ...])
```

### Repo & Forward Pricing (NEW)
```
# Forward yield given forward price
get(REPO_FORWARD_YLD(FORWARD_PRICE=98.164000,TERM_DATE=2026-03-16,REPO_RATE=2.1220,SETTLE_DATE=2026-03-13) as #forward_yield)
for(['XS3181537526'])

# Forward price given settle price and repo rate
get(REPO_FORWARD_PRICE(SETTLE_DATE=2026-03-13,SETTLE_PRICE=98.869,REPO_RATE=2.122,TERM_DAYS=3) as #forward_price)
for(['YJ649939 Corp'])
```

### Government Bond Spline Analytics (GOVY)
```
# Spline-fitted yields (exponential vs cubic)
get(yield(interpolation_type=exponential_spline) as #exp_yield,
    yield(interpolation_type=cubic_spline) as #cubic_yield)
for('BV688282 Corp')

# Cross-currency spline spreads
get(spread(interpolation_type=cubic_spline) as #cubic_spread,
    spread(interpolation_type=exponential_spline) as #exp_spread)
for('912810UB Govt')

# Roll-down analysis
get(roll_down(interpolation_type=exponential_spline) as #exp_roll_down,
    roll_down(interpolation_type=cubic_spline) as #cubic_roll_down)
for('91282CLC Govt')
# time_horizon param: 1M, 3M, 6M, 1Y
```

### Historical Risk Measures (Back to 2018)
```
# Historical modified duration
get(duration(duration_type=MODIFIED, dates=range(-1w,0d), fill=prev)) for('EJ222340 Corp')
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MODIFIED, DATES=RANGE(-10D,0D))")

# Historical risk (DV01 x 100)
get(risk(dates=-6m, fill=prev)) for(bond_id)
=BQL("DD103619 Corp","RISK(DATES=RANGE(-5Y,0D))")

# Historical convexity
=BQL("DD103619 Corp","CONVEXITY(DATES=RANGE(-5Y,0D))")

# Key rate durations (treasury and swap curve)
=BQL("DD103619 Corp","KRD(DATES=RANGE(-5Y,0D))")   # par treasury curve
=BQL("DD103619 Corp","S_KRD(DATES=RANGE(-5Y,0D))")  # par swap curve
# Available KRD tenors: 6M, 2Y, 5Y, 10Y, 20Y, 30Y

# Option-adjusted sovereign measures
=BQL("DD103619 Corp","SPREAD(SPREAD_TYPE=OAS_SOVEREIGN)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=OAD_SOVEREIGN)")
=BQL("DD103619 Corp","CONVEXITY(CONVEXITY_TYPE=OAC_SOVEREIGN)")
```

### Expanded Returns (Return Types + 1D/MTD/QTD/YTD)
```
# 1D total return
get(total_return(return_type=TOTAL, calc_interval=1D, fill=prev)) for('EJ222340 Corp')

# MTD return series over last week
get(total_return(return_type=TOTAL, calc_interval=MTD, dates=range(-1w,0d), fill=prev) as #1d_tot_ret)

# Top/bottom 10 performers in index (MTD)
let(
    #MTD_Return=total_return(return_type=TOTAL,calc_interval=MTD).value;
    #BestReturns=grouprank(#MTD_Return).value;
    #WorstReturns=grouprank(#MTD_Return, order=Asc).value;
)
get(groupsort(Name,#MTD_Return) as #Bond,#MTD_Return)
for(filter(members('LUACTRUU Index'), #BestReturns<=10 OR #WorstReturns<=10))

# Sector returns dashboard (weighted avg by BCLASS sector)
let(
    #TotalReturn=total_return(calc_interval=MTD,return_type=TOTAL);
    #Weights=id().weights;
    #Sector=classification_name(BCLASS,3);
    #WavgReturn=wavg(group(#TotalReturn,#Sector),group(#Weights,#Sector));
)
get(#WavgReturn) for(members('LUACTRUU Index'))
```
### Return Type Reference
| Return Type | Description |
|-------------|-------------|
| `TOTAL` | Total return (price + income) |
| `PRICE` | Price return only |
| `CPN` | Coupon income return |
| `PAYDOWN` | Paydown/amortization return |

### Bond Cashflows
```
# Projected cashflow schedule
=BQL("EC527035 Corp", "cashflows")

# Cashflows with custom settle date
=BQL("EC527035 Corp", "cashflows(settle_dt=2002-02-28) as #cashflows")

# workout_date codes: 1=Maturity, 2=Next Call, 4=Next Put, 15=Worst, 28=Avg Life, 65=Next Fix (floaters)
```

### Issuer Curve Analysis
```
# Median yield of IBM fixed USD bonds by maturity year
get(MEDIAN(GROUP(YIELD,YEAR(MATURITY))) as #Yld)
for(FILTER(Bonds(['IBM US Equity']),CPN_TYP=='FIXED' AND CRNCY==USD))

# Multi-issuer curve by credit rating
get(MEDIAN(GROUP(YIELD,RATING(SOURCE=BBG))) as #Yld)
for(FILTER(Bonds(['IBM US Equity','MSFT US Equity','ORCL US Equity','HPQ US Equity','INTC US Equity']),CPN_TYP=='FIXED' AND CRNCY==USD))

# Aggregate yield curve with maturity bucketing
let(
    #mat = (maturity-today())/365;
    #matbucket = IF(#mat <= 0.25,0.25,IF(#mat <= 0.5,0.5,IF(#mat <= 0.75,0.75,ceil(#mat))));
    #AvgMat = avg(group(#mat().value,#matbucket));
    #AvgYield = AVG(group(YIELD,#matbucket));
)
get(dropna(groupsort(#AvgYield().value, sortby=#AvgMat, order=asc),True) as #Yld)
for(FILTER(members(['LUACTRUU Index']),CPN_TYP=='FIXED' AND CRNCY==USD AND year(maturity)<2050))
```

### FI Screening Patterns
```
# IG Sr Non/Preferred count
get(count(group(ID)))
for(filter(bondsuniv(Active), RTG_SP>'BBB-' AND IN(PAYMENT_RANK,['Sr Preferred','Sr Non Preferred'])))

# EUR/GBP bonds issued YTD
get(sum(Group(amt_issued(currency=EUR)/1M,[CRNCY,PAYMENT_RANK])) as #amt_out)
for(filter(bondsuniv(active),in(CRNCY,['EUR','GBP']) AND ISSUE_DT>2023-01-01))

# Disney bullet bonds (non-callable/putable/perpetual)
for(filter(bondsuniv('active'), ticker=='DIS' AND NOT(IN(mty_typ,['PERPETUAL','CALLABLE','PUTABLE']))))

# USD large deals in 2020 (non-government)
get(NAME, AMT_ISSUED().value/10^9 as #USD_Bln_Issued)
for(filter(bondsUniv('Active'),MATURITY>10Y AND CRNCY=='USD' AND CNTRY_OF_RISK=='US'
    AND AMT_ISSUED>5*10^9 AND BICS_LEVEL_1_SECTOR_NAME!='Government' and year(issue_dt)==2020))

# Sustainability bonds from @GREEN screen
for(screenresults(type=srch, screen_name='@GREEN'))

# IBM investment grade bonds OAS (filtered)
get(avg(group(SPREAD(Spread_type='OAS'))))
for(filter(bonds(['IBM US Equity']), in(CRNCY,[USD]) AND AMT_OUTSTANDING>=300000000
    AND CPN_TYP==FIXED AND ISSUE_DT>=2013-01-01 AND MATURITY>=10y AND MATURITY<=30y
    AND Not(payment_rank in ['Jr Subordinated','Subordinated'])))
```

### Historical FI Screening (Point-in-Time)
```
# Russian energy bond spreads before/after conflict
let(#mty = bins(maturity_years,[3,5,10,20],['0-3','03-05','05-10','10-20','20+']);
    #Z_spread = spread(spread_type='Z');
    #avg_spread_by_mty = avg(group(#Z_spread,#mty));
    #count = count(group(#Z_spread,#mty));)
get(#count,#avg_spread_by_mty)
for(filter(bondsuniv('Active'),CNTRY_OF_RISK=='RU' and CLASSIFICATION_NAME('BCLASS',3)=='Energy'))
with(dates=2022-04-01,mode=cached)

# LIBOR vs SOFR floating rate debt
let(#AMT_OUT= sum(group(amt_outstanding/1m,reset_index));)
get(#AMT_OUT)
for(filter(filter(bondsuniv('Active'),CRNCY=='USD' AND FLOATER=='Y'),
    RESET_INDEX=='US0003M Index' OR RESET_INDEX=='SOFRRATE Index'))

# US leveraged loan by rating bucket
let(
    #rtg_bucket = if(bb_composite==NR,'NR',if(bb_composite<='CCC+','CCC+ or worse',if(bb_composite<='BB+','BB','BBB or Greater')));
    #amt_out = sum(group(amt_outstanding/1b,#rtg_bucket));
)
get(#amt_out)
for(filter(loansuniv('Active'),loan_typ=='TERM' AND CRNCY=='USD' AND CNTRY_OF_RISK=='US'))
```

---

## Notes on Excel BQL vs Python BQL

The workbooks use Excel `=BQL()` syntax. In Python (polars-bloomberg or bql.Service):
- `=BQL("security","field","params")` → `bq.bdp([security], [field])` or `bq.bql("get(field(params)) for(security)")`
- `=BQL.Query("get(...) for(...)")` → `bq.bql("get(...) for(...)")`
- `showquery=True` → displays the underlying BQL query syntax
- All BQL query patterns in `get()...for()...with()` format work directly in Python
