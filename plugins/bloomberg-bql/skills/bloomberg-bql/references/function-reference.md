# BQL Function Reference — Complete Catalog

## Arithmetic
```
abs(pe_ratio)           ceil(px_last)        floor(px_last)
round(is_eps, 2)        sqrt(x)              square(x)
pow(2, 10) / 2^10       mod(100, 7)          sign(is_eps)
ln(x)                   log(x)               exp(x)
negation(x) / -x
normal_dist(groupZscore(pe_ratio))
normal_inv(0.025 + normal_dist(groupZscore(pe_ratio)))
```

## Statistical (within a time series or list)
```
sum(px_volume(dates=range(-1W,0D)))
avg(px_last(dates=range(-3m,0d)))
wAvg(px_last, px_volume)           # weighted average
min(day_to_day_total_return(dates=range(-1y,0d)))
max(day_to_day_total_return(dates=range(-1y,0d)))
median(day_to_day_total_return(dates=range(-1y,0d)))
product(1+dropna(day_to_day_total_return(dates=range(-1m,0d))))-1
std(day_to_day_total_return(dates=range(-1y,0d)))
var(px_last)
skew(day_to_day_total_return(dates=range(-1y,0d)))
kurt(day_to_day_total_return(dates=range(-1y,0d)))
corr(dropna(px_volume), dropna(day_to_day_total_return))
rsq([1,2,3,4,5], is_eps(ae=a,fpt=a,fpo=range(-4,0)))
slope(dropna(px_volume), dropna(day_to_day_total_return))
intercept(dropna(px_volume), dropna(day_to_day_total_return))
zScore(dropna(day_to_day_total_return(dates=range(-1m,0d))))
rank(px_last(dates=range(-6m,0d)))
quantile(px_last(dates=range(-1Y,0D)), 0.25)
cut(day_to_day_total_return, 10)           # split into 10 quantile bins
winsorize(dropna(day_to_day_total_return), threshold_type=STD, lower_limit=2.0, upper_limit=2.0)
compoundGrowthRate(px_last)                # CAGR
```

## Cross-Security Grouping (operates across securities, not within one series)
```
groupAvg(pe_ratio, gics_sector_name)      # avg by sector
groupMedian(pe_ratio, gics_sector_name)   # median by sector
groupMin(pe_ratio)                        # min across universe
groupMax(sales_rev_turn)                  # max across universe
groupSum(eqy_sh_out)                      # total across universe
groupCount(interest_income)               # count non-null
groupStd(day_to_day_total_return(fill=prev))
groupWAvg(pe_ratio, id.weights)           # portfolio weighted avg
groupZscore(day_to_day_total_return(fill=prev))
groupRank(bs_cash_near_cash_item)
groupSort(ev_to_ebitda)
groupCut(day_to_day_total_return(fill=prev), n=100)  # percentile rank
groupWinsorize(day_to_day_total_return(fill=prev))
group(is_eps, gics_sector_name)           # group for further stat ops
ungroup(skew(group(is_eps, gics_sector_name)))  # project back to securities

# Aggregation patterns
SUM(GROUP(amt_outstanding(currency=USD)/1B))
AVG(GROUP(pe_ratio))
WAVG(GROUP(PE_RATIO), GROUP(id().weights))
SUM(GROUP(AMT_Outstanding, YEAR(MATURITY)))   # maturity schedule heatmap
AVG(GROUP(SPREAD(spread_type='OAS'), BICS_LEVEL_1_SECTOR_NAME))
```

## Time Series
```
cumProd(1+dropNA(day_to_day_total_return(dates=range(-3M,0d))))-1  # cumulative return
cumSum(dropNA(px_volume(dates=range(-6m,0d))))
cumAvg(dropNA(is_eps(fpt=a,fpo=1Y,dates=range(-3m,0d))))
cumMax(dropNA(px_last(dates=range(-1y,0d))))
cumMin(dropNA(px_last(dates=range(-1y,0d))))
diff(eqy_sh_out)                          # period-over-period change
pct_chg(cur_mkt_cap(dates=range(2018-01-01,today)))/100
pct_diff(cur_mkt_cap, step=7)/100         # change with step
net_chg(cur_mkt_cap)
rolling(avg(px_last(-1m,0d)), iterationdates=range(-1y,0d))  # rolling window
```

## Date Functions
```
today()
year(today())              # extract year
month(maturity)            # extract month (1-12)
dayofweek(date)            # 1=Mon … 7=Sun
dayofmonth(date)           # 1-31
range(-30d, 0d)            # date range
range(2020-01-01, 2023-12-31)
date(year(today())-1, 12, 20)   # construct date
startOfMonth               startOfQuarter       startOfYear
endOfMonth                 endOfQuarter         endOfYear
WTD  MTD  QTD  YTD        # period-to-date shortcuts
```

## String Functions
```
name + ' - ' + gics_sector_name           # concat / +
left(is_eps(fpt=a,fpo=0).period, 4)
right(is_eps(fpo=range(1Q,4Q),fpt=q).period, 2)
len(name)
replace(name, toscalar(len(name)-2), 3, 'incorporated')
toLower(name)              toUpper(name)
startsWith(gics_sector_name, 'consumer')
contains(CIE_DES, "gold")
```

## Filtering & Conditionals
```
filter(members('SPX Index'), pe_ratio<20 and cur_mkt_cap>10B)
top(members('INDU Index'), 10, CUR_MKT_CAP)
bottom(members('INDU Index'), 5, PE_RATIO)
if(pe_ratio>20, 'overvalued', 'undervalued')
matches(day_to_day_total_return, px_volume>35M)   # filter parallel series
between(px_last, 100, 200)
in(gics_sector_name, ['Financials', 'Technology'])
not(gics_sector_name=='Energy')
and / or / xor
all(day_to_day_total_return(dates=range(2018-08-13,2018-08-17))>0)
any(day_to_day_total_return(dates=range(2018-08-20,2018-08-24))<0)
```

## Data Handling
```
dropNA(expr)                              # remove NaN rows
dropNA(expr, remove_id=true)             # also remove the security
zNAV(day_to_day_total_return)            # replace NaN with 0
replaceNonNumeric(day_to_day_total_return, 0)   # replace NaN/inf
avail(is_eps(fpt=ltm,fpo=3Y), is_eps(fpt=a,fpo=3Y))  # first non-null
first(dropna(px_last(dates=range(-3m,0d))), 10)
last(dropNA(is_eps), 8)
sort(dropna(px_last), order=desc)
value(day_to_day_total_return, relativeIndex)    # evaluate in private universe, project to global
toscalar(len(name)-2)                    # convert series to scalar
```

## Metadata / Sub-field Access
```
day_to_day_total_return().date           # date column from time series
is_eps(fpt=a,fpo=0).period              # period string from fundamentals
rating().BASE_RATING                    # rating string without watch indicator
#rating().WATCH                         # watch status
#rating().EFFECTIVE_DATE                # when rating became effective
TRADE_DATA(#dates).I_SPREAD             # I-spread from TRACE data
TRADE_DATA(#dates).volume               # volume from TRACE data
PRICE(SPREAD=125).WAL                   # WAL from YT custom analytics
PRICE(SPREAD=125).ASSUMPTIONS           # prepayment assumptions
id().weights                            # portfolio security weights
id().positions                          # portfolio security positions
cds_spread().value                      # scalar value from data item
spread(st=I).VALUE                      # alternative .value syntax
```
