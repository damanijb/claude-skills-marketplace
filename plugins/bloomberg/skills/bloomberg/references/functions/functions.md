# BQL Functions Reference

## Arithmetic Functions
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Arithmetic Functions  |  abs()  |  Return absolute value of a number  |  for(members('INDU Index'))
get(groupavg(abs(pe_ratio-groupavg(pe_ratio))))  |  Returns the metric of PE_RATIO dispersion using abs.
Arithmetic Functions  |  ceil()  |  Round up to a whole number  |  for(members('INDU Index'))
get(ceil(px_last))  |  Returns the price rounded up to nearest dollar.
Arithmetic Functions  |  exp()  |  Return e raised to a value  |  for('AAPL US Equity')
get(exp(1))  |  Returns e^1 power.
Arithmetic Functions  |  floor()  |  Round down to a whole number  |  for(members('INDU Index'))
get(floor(px_last))  |  Returns the price rounded down to nearest dollar.
Arithmetic Functions  |  ln()  |  Calculate the natural log  |  for('AAPL US Equity')
get(ln(2.718282))  |  Applies natural logarithm to e and returns 1.
Arithmetic Functions  |  log()  |  Calculate the base 10 log  |  for('AAPL US Equity')
get(log(1000))  |  Applies base 10 logarithm to 1000 and returns 3.
Arithmetic Functions  |  round()  |  Round to a given precision  |  for(members('INDU Index'))
get(round(is_eps, 2))  |  Rounds data to two digits.
Arithmetic Functions  |  sign()  |  Get the sign of an integer  |  for(members('SPX Index'))
get(sign(is_eps))  |  Returns -1 for negative eps and +1 for positive eps.
Arithmetic Functions  |  sqrt()  |  Calculate the square root  |  for('AAPL US Equity')
get(sqrt(12321))  |  Takes sqrt of 12321 and returns 111.
Arithmetic Functions  |  square()  |  Calculate the square  |  for('AAPL US Equity')
get(square(11))  |  Squares 11 to return 121.
Arithmetic Functions  |  mod()  |  Calculate the modulo  |  for('AAPL US Equity')
get(mod(100,7))  |  Returns modulo (remainder) of 100/7.
Arithmetic Functions  |  negation() , -  |  Return negative of the value  |  for('AAPL US Equity')
get(-px_last)  |  Returns px_last * -1.
Arithmetic Functions  |  pow() , ^  |  Raise the value to the nth power  |  for('AAPL US Equity')
get(2^10)  |  Returns 2^10 = 1024.
Arithmetic Functions  |  normal_dist()  |  Calculate normal/cumulative normal distribution  |  for(members('SPX Index'))
get(normal_dist(groupZscore(pe_ratio)))  |  Returns the expected probability that each security's pe_ratio is greater than or equal to a randomly selected one
Arithmetic Functions  |  normal_inv()  |  Calculates inverse normal/cumulative normal distribution  |  for(members('SPX Index'))
get(normal_inv(0.025+normal_dist(groupZscore(pe_ratio))))  |  Returns the equivalent z-score derived from the expected probability that each security's pe_ratio is greater than or equal to a randomly selected one if it was increased by  2.5%

## Statistical Functions
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Statistical Functions  |  sum()  |  Calculate the sum of all values  |  for('AAPL US Equity')
get(sum(px_volume(dates=range(-1W, 0D))))  |  Returns the total 1-week traded volume.
Statistical Functions  |  count()  |  Count all non-null values  |  get(count(px_last(dates=range(-1y,0d))))
for('AAPL US Equity')  |  Counts number of closing prices over last year.
Statistical Functions  |  avg()  |  Calculate the average value  |  for('AAPL US Equity')
get(avg(px_last(dates=range(-3m,0d))))  |  Returns the average price over last 3 months.
Statistical Functions  |  wAvg()  |  Calculate the weighted average  |  for('AAPL US Equity')
get(wAvg(px_last,px_volume))
with(dates=range(-1y,0y),frq=d)  |  Returns the 1 year volume weighted average price (VWAP) - using close prices only for simplicity.
Statistical Functions  |  min()  |  Return the lowest value  |  for('AAPL US Equity')
get(min(day_to_day_total_return(dates=range(-1y,0d))))  |  Returns the minimum daily return over the course of a year.
Statistical Functions  |  max()  |  Return the highest value  |  for('AAPL US Equity')
get(max(day_to_day_total_return(dates=range(-1y,0d))))  |  Returns the max daily return over the course of a year.
Statistical Functions  |  median()  |  Return the median value  |  for('AAPL US Equity')
get(median(day_to_day_total_return(dates=range(-1y,0d))))  |  Returns the median daily return over the course of a year.
Statistical Functions  |  product()  |  Calculate the product  |  for(members('INDU Index'))
get(product(1+dropna(day_to_day_total_return(dates=range(-1m,0d))))-1)  |  Returns the total return over a month by taking product of data series.
Statistical Functions  |  corr()  |  Calculate the correlation  |  for(members('INDU Index',dates=0d))
get(corr(dropna(px_volume),dropna(day_to_day_total_return)))
with(dates=range(-1m,-1d))  |  Returns the correlation coefficient of daily volume vs daily total return over period of 1 year for each member of index.
Statistical Functions  |  rsq()  |  Calculate the r-squared  |  for(members('INDU Index'))
get(rsq([1,2,3,4,5,6,7,8,9,10],is_eps(ae=a,fpt=a,fpo=range(-9Y,0Y))))  |  Returns R-Squared value of last ten years annual earnings (a measure of stability).
Statistical Functions  |  std()  |  Calculate the standard deviation  |  for('INDU Index')
get(sqrt(260)*std(day_to_day_total_return(dates=range(-1y,0d))))  |  Returns the annualized vol of the index over the course of a year using daily returns.
Statistical Functions  |  var()  |  Calculate the variance  |  for(members('INDU Index'))
get(sqrt(var(px_last))==std(px_last))
with(dates=range(-2m,0d))  |  Returns TRUE showing the standard deviation squared of a data series is its variance.
Statistical Functions  |  skew()  |  Calculate the skewness  |  for('INDU Index')
get(skew(day_to_day_total_return(dates=range(-1y,0d))))  |  Returns the skew of daily returns over a year.
Statistical Functions  |  kurt()  |  Calculate the kurtosis  |  for('AAPL US Equity')
get(kurt(day_to_day_total_return(dates=range(-1y,0d))))  |  Returns the kurtosis of daily returns over a year.
Statistical Functions  |  zScore()  |  Calculate the z-scores  |  for('AAPL US Equity')
get(zScore(dropna(day_to_day_total_return(dates=range(-1m,0d)))))  |  Returns the Z-Score of data-point relative to its data series.
Statistical Functions  |  winsorize()  |  Applies a limit to outliers  |  for('AAPL US Equity'
get(winsorize(dropna(day_to_day_total_return(dates=range(-1m,0d))),threshold_type=STD, lower_limit=2.0, upper_limit=2.0))  |  Generates the daily returns of Apple, limiting each value to 2 standard deviations away from the mean
Statistical Functions  |  compoundGrowthRate()  |  Return the geometric average growth rate  |  for('AAPL US Equity')
get(compoundGrowthRate(px_last))
with(dates=range(-20y,0y,frq=y),fill=prev)  |  Returns the yearly average growth rate of Apple's stock price over the last 20 years.
Statistical Functions  |  cut()  |  Calculate quantile rank  |  for('AAPL US Equity')
get(dropna(matches(day_to_day_total_return, cut(day_to_day_total_return,10)==10)))
with(dates=range(-6m,0d))  |  Splits returns into 10 deciles and shows only data that is >90th percentile.
Statistical Functions  |  rank()  |  Rank values descending/ascending  |  for('M US Equity')
get(rank(px_last(dates=range(-6m,0d))))  |  Ranks each price highest to lowest for last 6 months.
Statistical Functions  |  quantile()  |  Return the value corresponding to a quantile  |  for(['IBM US Equity'])
get(quantile(px_last(dates=range(-1Y, 0D)), 0.25))  |  Returns the price representing the top of the 1st quartile
Statistical Functions  |  slope()  |  Return the slope linear regression  |  for(members('INDU Index',dates=0d))
get(slope(dropna(px_volume),dropna(day_to_day_total_return)))
with(dates=range(-1m,-1d))  |  Returns the slope of the linear regression between daily volume vs daily total return over period of 1 year for each member of index.
Statistical Functions  |  intercept()  |  Return the intercept of a linear regression  |  for(members('INDU Index',dates=0d))
get(intercept(dropna(px_volume),dropna(day_to_day_total_return)))
with(dates=range(-1m,-1d))  |  Returns the intercept of the linear regression between daily volume vs daily total return over period of 1 year for each member of index.

## Grouping Data
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Grouping Data  |  group()  |  Group data for statistical analysis across security boundaries  |  for(members('SPX Index'))
get(group(is_eps, gics_sector_name))  |  Groups all of the data by GICS Sector and applies functions across all the data as opposed to within each.
Grouping Data  |  ungroup()  |  Projects grouped data back onto the original security list  |  for(members(['SPX Index']))
get(ungroup(skew(group(is_eps, gics_sector_name))))  |  For each member of S&P Index, returns the skew of the EPS observations for the sector to which the security belongs.
Grouping Data  |  groupAvg()  |  Return average of values across securities (with optional grouping)  |  for(members('SPX Index'))
get(groupAvg(is_eps, gics_sector_name))  |  For each member of S&P Index, returns the average EPS for the sector to which the security belongs.
Grouping Data  |  groupCount()  |  Count non-NaN values across securities (with optional grouping)  |  for(members('SPX Index'))
get(groupCount(interest_income))  |  For each member of S&P Index, returns the count of members of SPX with interest income data available.
Grouping Data  |  groupMax()  |  Return maximum of values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupMax(sales_rev_turn))  |  For each member of INDU Index, returns max LTM revenue for members of INDU.
Grouping Data  |  groupMedian()  |  Return median of values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupMedian(pe_ratio, gics_sector_name))  |  For each member of INDU Index, returns the median pe_ratio for the sector to which the security belongs.
Grouping Data  |  groupMin()  |  Return minimum of values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupMin(pe_ratio))  |  For each member of INDU Index, returns smallest PE_RATIO for members of INDU.
Grouping Data  |  groupRank()  |  Rank values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupRank(bs_cash_near_cash_item))  |  Ranks each member of the INDU by amount of cash on hand.
Grouping Data  |  groupStd()  |  Return the standard deviation of values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupStd(day_to_day_total_return(fill=prev)))  |  For each member of INDU Index, returns standard deviation of dow members' last daily returns.
Grouping Data  |  groupSum()  |  Add values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupSum(eqy_sh_out))  |  For each member of INDU Index, returns total shares outstanding for INDU.
Grouping Data  |  groupWAvg()  |  Average values across securities using weights (with optional grouping)  |  for(members('INDU Index'))
get(groupWAvg(pe_ratio,id.weights))  |  For each member of INDU Index, returns weighted average PE Ratio for INDU.
Grouping Data  |  groupZscore()  |  Return the z-score of values across securities (with optional grouping)  |  for(members('INDU Index'))
get(groupZscore(day_to_day_total_return(fill=prev)))  |  For each member of INDU Index, returns z-score of dow members' last daily returns.
Grouping Data  |  groupcut()  |  Returns the quantile for each security (with optional grouping)  |  for(members('INDU Index'))
get(groupCut(day_to_day_total_return(fill=prev), n=100))  |  For each member of INDU Index, returns percentile of dow members' last daily returns.
Grouping Data  |  groupwinsorize()  |  Limits outlying data quantile across securities (optionally within groups)  |  for(members('INDU Index'))
get(groupWinsorize(day_to_day_total_return(fill=prev)))  |  For each member of INDU Index, returns dow members' last daily returns, limiting outliers

## Time Series Manipulation
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Time Series Manipulation  |  cumAvg()  |  Calculate the cumulative mean  |  for('AAPL US Equity')
get(cumAvg(dropNA(is_eps(fpt=a,fpo=1Y,dates=range(-3m,0d)))))  |  Returns the cumulative average consensus estimate for EPS for this coming fiscal year.
Time Series Manipulation  |  cumMax()  |  Return the cumulative maximum  |  for('AAPL US Equity')
get(cumMax(dropNA(px_last(dates=range(-1y,0d)))))  |  Returns the cumulative maximum price over last year.
Time Series Manipulation  |  cumMin()  |  Return the cumulative minumum  |  for('GE US Equity')
get(cumMin(dropNA(px_last(dates=range(-1y,0d)))))  |  Returns the cumulative minimum price over last year.
Time Series Manipulation  |  cumProd()  |  Calculate the cumulative product  |  for('AAPL US Equity')
get(cumProd(1+dropNA(day_to_day_total_return(dates=range(-3M,0d))))-1)  |  Calculates a data series of cumulative daily return.
Time Series Manipulation  |  cumSum()  |  Calculate the cumulative sum  |  for('AAPL US Equity')
get(cumSum(dropNA(px_volume(dates=range(-6m,0d)))))  |  Calculates a data series of cumulative daily volume.
Time Series Manipulation  |  diff()  |  Subtract value from prior in series  |  for('AAPL US Equity')
get(dropNA(if(diff(eqy_sh_out)==0,nan,diff(eqy_sh_out))))
with(dates=range(-2y,0d))  |  Calculates any changes in shares outstanding over course of 2 years.
Time Series Manipulation  |  net_chg()  |  Calculate the net change  |  for('GE US Equity')
get(net_chg(dropNA(cur_mkt_cap(dates=range(2018-01-01,today))))/100)  |  Calculates year-to-date net dollar change in market cap.
Time Series Manipulation  |  pct_chg()  |  Calculate the percent change  |  for('GE US Equity')
get(pct_chg(dropNA(cur_mkt_cap(dates=range(2018-01-01,today))))/100)  |  Calculates year-to-date percent change in market cap.
Time Series Manipulation  |  pct_diff()  |  Calculate the percent difference  |  for('GE US Equity')
get(pct_diff(dropNA(cur_mkt_cap(dates=range(2018-01-01,today))), step=7)/100)  |  Calculates 7 day percent change in price since beginning of the calendar year.
Time Series Manipulation  |  rolling()  |  Evaluates an expression for a series of dates  |  for('AAPL US Equity')
get(rolling(avg(px_last(-1m,0d)),iterationdates=range(-1y,0d)))  |  Returns a 1 month moving average price for Apple's Stock going back daily for 1 year.

## Date Manipulation
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Date Manipulation  |  today()  |  Returns today's date  |  for('AAPL US Equity')
get(today())  |  Returns today's date and time.
Date Manipulation  |  year()  |  Returns the year  |  for('AAPL US Equity')
get(year(today()))  |  Returns the current year.
Date Manipulation  |  month()  |  Returns the month  |  for('SPX Index')
get(groupavg(day_to_day_total_return,month(day_to_day_total_return().date)))
with(dates=range(-9y,0d),per=m)  |  Returns the avg monthly return of SPX by month over the past 9 years.
Date Manipulation  |  dayofweek()  |  Returns the weekday as a number 1-7  |  for('SPX Index')
get(avg(dropNA(if(dayOfWeek(day_to_day_total_return().date)==3, day_to_day_total_return,nan))))
with(dates=range(-5y,0d))  |  Returns the average Tuesday return for the SPX going back 5 years.
Date Manipulation  |  dayofmonth()  |  Returns the day of the month  |  for('INTC US Equity')
get(dropNA(if(dayOfMonth(px_volume().date)==1,px_volume,nan)))
with(dates=range(-3y,0d),fill=prev)  |  Shows total daily volume on the first day of the month going back 3 years.
Date Manipulation  |  range()  |  Creates a range of dates or numbers  |  for('IBM US Equity')
get(px_last(dates=range(-30d,0d)))  |  Returns 30 days of prices for IBM
Date Manipulation  |  date()  |  Returns a date from its numeric components  |  for(cds('VOD LN Equity'))
get(px_last(dates = date(year(today())-1,12,20)))  |  Returns Vodafone's CDS spread as of December IMM date last year
Date Manipulation  |  startOfMonth  |  Returns the first day of the current month  |  for('VOD LN Equity')
get(px_last(dates=startOfMonth-1d))  |  Returns Vodafone's closing price last month
Date Manipulation  |  startOfQuarter  |  Returns the first day of the current quarter  |  for('VOD LN Equity')
get(px_last(dates=startOfQuarter-1d))  |  Returns Vodafone's closing price last quarter
Date Manipulation  |  startOfYear  |  Returns the first day of the current year  |  for('VOD LN Equity')
get(px_last(dates=startOfYear-1d))  |  Returns Vodafone's closing price last year
Date Manipulation  |  endOfMonth  |  Returns the last day of the current month  |  for('US Country')
get(calendar(type=ECONOMIC_RELEASES, dates=range(0d,endOfMonth)))  |  Returns US economic releases until the end of the month
Date Manipulation  |  endOfQuarter  |  Returns the last day of the current quarter  |  for('US Country')
get(calendar(type=ECONOMIC_RELEASES, dates=range(0d,endOfQuarter)))  |  Returns US economic releases until the end of the Quarter
Date Manipulation  |  endOfYear  |  Returns the last day of the current year  |  for('US Country')
get(calendar(type=ECONOMIC_RELEASES, dates=range(0d,endOfYear)))  |  Returns US economic releases until the end of the Year
Date Manipulation  |  WTD  |  Returns dates from 1st day of the current week to today  |  for('MSFT US Equity')
get(px_last(dates=wtd))  |  Microsoft's price series week-to-date
Date Manipulation  |  MTD  |  Returns dates from 1st day of the current month to today  |  for('MSFT US Equity')
get(px_last(dates=mtd))  |  Microsoft's price series month-to-date
Date Manipulation  |  QTD  |  Returns dates from 1st day of the current quarter to today  |  for('MSFT US Equity')
get(px_last(dates=qtd))  |  Microsoft's price series quarter-to-date
Date Manipulation  |  YTD  |  Returns dates from 1st day of the current year to today  |  for('MSFT US Equity')
get(px_last(dates=ytd))  |  Microsoft's price series year-to-date
5) S&P500 daily price chart over the last calendar year:
for('SPX Index') get(px_last(dates=range(-2cy, -1cy, frq=d)))

## Filtering and Conditionals
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Filtering and Conditionals  |  filter()  |  Screen a subset from a universe using a predicate  |  for(filter(members('INDU Index'),px_last>200))
get(px_last)  |  Returns the last price for each stock in the Dow where the price of the stock is higher than $200.
Filtering and Conditionals  |  top()  |  Sorts a universe from largest to smallest and returns the first entries  |  for(top(members('INDU Index'),10,CUR_MKT_CAP))
get(cur_mkt_cap/1M)  |  Returns the top ten stocks in the Dow by market cap; sorted from highest to lowest
Filtering and Conditionals  |  bottom()  |  Sorts a universe from smallest to largest and returns the first entries  |  for(bottom(members('INDU Index'),10,CUR_MKT_CAP))
get(cur_mkt_cap/1M)  |  Returns the bottom ten stocks in the Dow by market cap; sorted from lowest to highest
Filtering and Conditionals  |  if()  |  Evaluate predicate to decide output  |  for(members('INDU Index'))
get(if(pe_ratio>20,"overvalued","undervalued"))  |  Tags securities as undervalued/overvalued based on current LTM PE.
Filtering and Conditionals  |  and() , and  |  True if both of two are true  |  for(members('INDU Index'))
get(pe_ratio<20 and px_last>100)  |  Returns True for securities in the DOW that have a PE < 20 and a Price > 100.
Filtering and Conditionals  |  equals() , ==  |  True if values are the same  |  for(members('INDU Index'))
get(gics_sector_name=='Financials')  |  Returns True for each security only if it is in in the 'Financials' GICS Sector.
Filtering and Conditionals  |  greaterThan() , >  |  True if greater than  |  for(members('INDU Index'))
get(px_last>200)  |  Returns True for securities in the DOW that have a Price > 200.
Filtering and Conditionals  |  greaterThanOrEquals() , >=  |  True if greater than or equal  |  for(members('INDU Index'))
get(px_last>=200)  |  Returns True for securities in the DOW that have a Price >= 200.
Filtering and Conditionals  |  in() , in  |  True if the value is in a list  |  for(members('INDU Index'))
get(gics_sector_name in ['Financials','Consumer Discretionary'])  |  Returns True if anything in second parameter appears in each data item of first parameter.
Filtering and Conditionals  |  lessThan() , <  |  True if less than  |  for(members('INDU Index'))
get(px_last<200)  |  Returns True for securities in the DOW that have a Price < 200.
Filtering and Conditionals  |  lessThanOrEquals() , <=  |  True if less than or equal  |  for(members('INDU Index'))
get(px_last<=200)  |  Returns True for securities in the DOW that have a Price <=200.
Filtering and Conditionals  |  not()  |  True if condition is false  |  for(members('INDU Index'))
get(not(gics_sector_name=='Energy'))  |  Returns True for each security only if it is NOT in in the 'Energy' GICS Sector.
Filtering and Conditionals  |  notEquals() , !=  |  True if values are different  |  for(members('INDU Index'))
get(gics_sector_name!='Financials')  |  Returns True for each security only if it is NOT in in the 'Financials' GICS Sector.
Filtering and Conditionals  |  or() , or  |  True if at least one of two is true  |  for(members('INDU Index'))
get(pe_ratio<20 or px_last>100)  |  Returns True for securities in the DOW that have a PE < 20 OR a Price > 100.
Filtering and Conditionals  |  xor() , xor  |  True if one is true & one is false  |  for(members('INDU Index'))
get (gics_sector_name=='Financials' xor sales_rev_turn>100B)  |  Returns True if either GICS Sector is Financials or Revenue >100B, but NOT both.
Filtering and Conditionals  |  all()  |  True if all in a series are true  |  for('AAPL US Equity')
get(all(day_to_day_total_return(dates=range(2018-08-13,2018-08-17))>0))  |  Returns True since Apple's daily returns for that week were all greater than zero.
Filtering and Conditionals  |  any()  |  True if any in a series is true  |  for('AAPL US Equity')
get(any(day_to_day_total_return(dates=range(2018-08-20,2018-08-24))<0))  |  Returns True since at least one of Apple's daily returns for that week was less than zero.
Filtering and Conditionals  |  between()  |  True if value is in inclusive range  |  for(members('INDU Index'))
get(between(px_last,100,200))  |  Returns TRUE for members of the Dow with a price between the inclusive range of $100 and $200.
Filtering and Conditionals  |  matches()  |  Find values that meet criteria  |  for('AAPL US Equity')
get(matches(day_to_day_total_return,px_volume>35M))
with(dates=range(2018-08-01,2018-08-31))  |  Returns the return of Apple's stock on days with volume higher than 35 million shares traded.

## Security Universes
Category  |  Function  |  Description  |  Example Query  |  Example Query Result
Security Universes  |  equitiesUniv()  |  All equities  |  for(filter(equitiesUniv(['active','primary']), cur_mkt_cap(currency=usd)>100B))
get(count(group(id)))
with(mode=cached)  |  Counts the number of equities in the entire universe that have a market cap higher than $100 Billion.
Security Universes  |  fundsUniv()  |  All funds  |  for(filter(fundsUniv(['Primary','Active']),mgr_country_name=='Argentina' and fund_geo_focus=='U.S.'))
get(name)
with(mode=cached)  |  Gets the names of funds that are managed in Argentina but focus on U.S. companies.
Security Universes  |  bondsUniv()  |  All bonds  |  for(filter(bondsUniv('active'),amt_outstanding(currency=usd)>100B))
get(crncy)  |  Displays the currency for all of the bonds in the bonds universe with an amount outstanding more than $100 Billion.
Security Universes  |  debtUniv()  |  All bonds, loans, munis or preferreds  |  for(filter(debtUniv('ACTIVE'), yield()>=14 and crncy()=='USD' and callable()==FALSE and maturity()>=5Y))
get(name)  |  Return the yield of all active, non-callable debt securities available on Bloomberg issued in USD, with a yield greater than 14%, and maturing more than five years from now
Security Universes  |  municipalsUniv()  |  All munis  |  for(filter(municipalsUniv(ACTIVE), defaulted()==TRUE and amt_outstanding(currency=USD)>100M))
get(id)  |  Return a list of all active municipal bonds available on Bloomberg with an amount outstanding over $100M that have defaulted
Security Universes  |  loansUniv()  |  All loans  |  for(loansUniv('active'))
get(count(group(id)))  |  Counts the size of the active loans universe.
Security Universes  |  mortgagesUniv()  |  All mortgages  |  for(filter(mortgagesUniv(ACTIVE), mtg_deal_typ()=='CMO' and callable()=='Y' and mtg_factor()<=0.1 and mtg_delinquencies_pct()<3 and px_ask()<100 and issue_dt()>2010-07-31))
get(name)  |  Return a list of active MBS available on Bloomberg that were issued after July 21, 2010 and are selling below par, with collateral below cleanup percentage and low delinquency rates
Security Universes  |  preferredsUniv()  |  All preferreds  |  for(filter(preferredsUniv(ACTIVE), callable()==Y and cpn()>6))
get(id)  |  Return all active US preferreds available on Bloomberg that are callable and have a coupon greater than 6%
Security Universes  |  countries()  |  All countries  |  for(countries(['g8']))
get(cpi)  |  Return CPI for all G8 countries
