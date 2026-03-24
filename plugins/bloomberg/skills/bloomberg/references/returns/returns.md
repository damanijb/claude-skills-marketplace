# BQL Returns Analysis

## BQL Syntax
False
bbg://screens/LPHP CURR:0:1 591037  |  Help!A1
Required Parameters  |  Description  |  let()  |  (Optional) lab expressions for later reuse in your query
Universe  |  The security universe including ticker(s), isin(s), cusip(s) or larger universes such as index members or the bonds universe.
get()  |  DataItem(Parameters) to be retrieved
Data Item(s)  |  The data fields such as TOTAL_RETURN. You can find a current list of available fields via the BQL Builder on the Bloomberg Ribbon in Excel.
for()  |  Security, wrapped in single quotes '
with()  |  (Optional) global parameters that are applied to all applicable data items.
The FOR clause in BQL() can take several inputs, e.g.
Single security  |  - Eg... for(['IBM US Equity'])
List of securities  |  - Eg... for(['VOD LN Equity','IBM US Equity'])
Debt Chains  |  - Eg… for(bonds(['CBA AU Equity']))
Index/Port members:  |  - Eg... for(members(['LEGATRUU Index']))
let()  |  let(#Spread_Chg =pct_chg(spread(dates=range(-3m,0d)));)
get()  |  Get(#Spread_Chg)
for()  |  for(bonds('NAB AU Equity'))
with()  |  with(fill=prev)

## Total Return Analysis
In BQL, we have two different data fields for pulling the total return of a fixed income instrument, see the below comparison for pulling the two fields across different instruments and asset classes :
BOND TOTAL RETURN
Data Items  |  Behaviour  |  Parameters
TOTAL_RETURN  |  Pulls the total return (with distributions reinvested) for the entire holding period  |  Calc_Interval=Range(), Reinvestment_Type, Reinvestment_Rate, Side, Display_Returns
RETURN_SERIES  |  Pulls the period-over-period total return (with distributions reinvested) at the specified periodicity  |  Calc_interval=Range(), Per
*Parameters in bold are mandatory
TOTAL RETURN Mandatory Parameters  |  Options
Calc_interval  |  Calc_Interval=Range()  |  Calculation interval for total return
TOTAL RETURN Optional Parameters  |  Options
Side  |  Bid, Mid, or Ask  |  Side of pricing used in the calculation
Reinvestment_Rate  |  Rate at which to invest the distributions
Reinvestment_Type  |  None, Fixed, Mmkt  |  Coupon reinvested at security's price (None); Reinvested at a specific rate (Fixed)
Display_Returns  |  Asset_class_default, Decimal, Percent  |  Select how to display returns (percent vs decimal)
Note: To specify no reinvestment of the coupon, set Reinvestment_Type=Fixed, and Reinvestment_Rate=0. Options in bold are default values.
EQUITY / INDEX / FUND TOTAL RETURN
Data Items  |  Behaviour  |  Parameters
TOTAL_RETURN  |  Pulls the total return (with distributions reinvested) for the entire holding period  |  Calc_Interval, Calc_Interval=Range(), Display_Returns
RETURN_SERIES  |  Pulls the period-over-period total return (with distributions reinvested) at the specified periodicity  |  Calc_Interval, Calc_interval=Range(), Per
Note: Equity, Index, and Fund returns are reinvested in the security per market convention, and thus do not take the reinvestment_type / reinvestment_rate overrides.
Pulling the total return of a bond:
Bond:  |  EC527035 Corp
Decimal  |  Return Horizon:  |  3M
Percent  |  Display Returns:  |  Percent
Asset_Class_Default
=BQL(''EC527035 Corp'',''TOTAL_RETURN(Calc_Interval=Range(-3M,0D),display_returns='Percent')'')  |  #N/A Requesting Data...
Pulling the total return of a bond:
Bond:  |  EC527035 Corp
Return Horizon:  |  11M
=BQL(''EC527035 Corp'',''TOTAL_RETURN(Calc_Interval=Range(-11M,0D))'')  |  #N/A Requesting Data...
Pulling the total return of a bond:
Bond:  |  EC527035 Corp
Return Horizon:  |  1M
Reinvestment Rate:  |  3
Reinvestment Type:  |  Fixed
=BQL(''EC527035 Corp'',''TOTAL_RETURN(Calc_Interval=Range(-1M,0D),Reinvestment_Type='Fixed',Reinvestment_Rate=3)'')  |  #N/A Requesting Data...
Pulling the total return of a bond:
Bond:  |  EC527035 Corp
Return Horizon:  |  12M
Reinvestment Rate:  |  0
Reinvestment Type:  |  Fixed
Display Returns:  |  Percent
=BQL(''EC527035 Corp'',''TOTAL_RETURN(Calc_Interval=Range(-12M,0D),Reinvestment_Type='Fixed',Reinvestment_Rate=0,display_returns='Percent')'')  |  #N/A Requesting Data...

## Cross-Asset Returns
In BQL, we have two different data fields for pulling the total return of a fixed income instrument, see the below comparison for pulling the two fields across different instruments and asset classes :
BOND TOTAL RETURN
Data Items  |  Behaviour  |  Parameters
TOTAL_RETURN  |  Pulls the total return (with distributions reinvested) for the entire holding period  |  Calc_Interval=Range(), Reinvestment_Type, Reinvestment_Rate, Side, Display_Returns
RETURN_SERIES  |  Pulls the period-over-period total return (with distributions reinvested) at the specified periodicity  |  Calc_interval=Range(), Per
*Parameters in bold are mandatory
TOTAL RETURN Mandatory Parameters  |  Options
Calc_interval  |  Calc_Interval=Range()  |  Calculation interval for total return
TOTAL RETURN Optional Parameters  |  Options
Side  |  Bid, Mid, or Ask  |  Side of pricing used in the calculation
Reinvestment_Rate  |  Rate at which to invest the distributions
Reinvestment_Type  |  None, Fixed, Mmkt  |  Coupon reinvested at security's price (None); Reinvested at a specific rate (Fixed)
Display_Returns  |  Asset_class_default, Decimal, Percent  |  Select how to display returns (percent vs decimal)
Note: To specify no reinvestment of the coupon, set Reinvestment_Type=Fixed, and Reinvestment_Rate=0. Options in bold are default values.
EQUITY / INDEX / FUND TOTAL RETURN
Data Items  |  Behaviour  |  Parameters
TOTAL_RETURN  |  Pulls the total return (with distributions reinvested) for the entire holding period  |  Calc_Interval, Calc_Interval=Range(), Display_Returns
RETURN_SERIES  |  Pulls the period-over-period total return (with distributions reinvested) at the specified periodicity  |  Calc_Interval, Calc_interval=Range(), Per
Note: Equity, Index, and Fund returns are reinvested in the security per market convention, and thus do not take the reinvestment_type / reinvestment_rate overrides.
Inflation Index  |  CPI YOY Index
Equity Index  |  SPX Index
Bond Index  |  LUACTRUU Index
Correlation Horizon  |  1Y
Series Length:  |  20Y
Periodicity:  |  Q
Let()  |  let(#returns = return_series(Calc_interval=range(-1Y,0d));
#returns_fi = value(#returns,['LUACTRUU Index']);
#returns_eq = value(#returns,['SPX Index']);
#correl = corr(#returns_fi,#returns_eq);
#cpi = px_last;)  |  #N/A Requesting Data...  |  #Corr  |  #Inflation
2022-03-02 00:00:00  |  0.014382119237961549  |  7.47988
2021-12-02 00:00:00  |  0.040889457444442  |  6.809
2021-09-02 00:00:00  |  0.0611843182379674  |  5.25127
2021-06-02 00:00:00  |  0.14927710947095382  |  4.9927
2021-03-02 00:00:00  |  0.15968363916188208  |  1.67621
get()  |  get(rolling(#correl,range(-20Y,0d,frq=Q)) as #Corr,rolling(#cpi,range(-20Y,0d,frq=Q)) as #Inflation)  |  2020-12-02 00:00:00  |  0.13809569352649662  |  1.17453
2020-09-02 00:00:00  |  0.13367821006625105  |  1.30964
for()  |  for('CPI YOY Index')  |  2020-06-02 00:00:00  |  0.09674161248489886  |  0.11793
with()  |  with(fill=prev,currency=USD)  |  2020-03-02 00:00:00  |  -0.2925262215293283  |  2.33488
2019-12-02 00:00:00  |  -0.32610306950638246  |  2.05128
2019-09-02 00:00:00  |  -0.29007525588685024  |  1.74979
2019-06-02 00:00:00  |  -0.24132327970947895  |  1.79023
2019-03-02 00:00:00  |  -0.2178185279889749  |  1.52014
2018-12-02 00:00:00  |  -0.11071840849354472  |  2.1766
2018-09-02 00:00:00  |  -0.13122762040203892  |  2.69918
2018-06-02 00:00:00  |  -0.12395208155466719  |  2.80101
2018-03-02 00:00:00  |  -0.11246791430708121  |  2.2118
2017-12-02 00:00:00  |  -0.2868001073596406  |  2.20259
2017-09-02 00:00:00  |  -0.14845034295653797  |  1.93897
2017-06-02 00:00:00  |  -0.21465001177537157  |  1.87488
2017-03-02 00:00:00  |  -0.22208221907169473  |  2.73796
2016-12-02 00:00:00  |  -0.22658739134143252  |  1.69254
2016-09-02 00:00:00  |  -0.33616454356258485  |  1.06288
2016-06-02 00:00:00  |  -0.31594935548774833  |  1.01933
2016-03-02 00:00:00  |  -0.2399509951461916  |  1.0178
2015-12-02 00:00:00  |  -0.2855567802101585  |  0.5018
2015-09-02 00:00:00  |  -0.2504089124806136  |  0.19507
2015-06-02 00:00:00  |  -0.24791333974558602  |  -0.03993
2015-03-02 00:00:00  |  -0.42607162513852465  |  -0.02513
2014-12-02 00:00:00  |  -0.3503114302554383  |  1.32236
2014-09-02 00:00:00  |  -0.23691840616073756  |  1.69961
2014-06-02 00:00:00  |  -0.057935060342755945  |  2.12711
2014-03-02 00:00:00  |  -0.03684213399417009  |  1.12635
2013-12-02 00:00:00  |  -0.07779962894856816  |  1.23708
2013-09-02 00:00:00  |  -0.20128786824447478  |  1.51837
2013-06-02 00:00:00  |  -0.510104950737624  |  1.36197
2013-03-02 00:00:00  |  -0.49104159699503414  |  1.97793
2012-12-02 00:00:00  |  -0.5033410429789681  |  1.76413
2012-09-02 00:00:00  |  -0.519103800555244  |  1.69238
2012-06-02 00:00:00  |  -0.5139094976606747  |  1.70425
2012-03-02 00:00:00  |  -0.5330859196362551  |  2.87109
2011-12-02 00:00:00  |  -0.4731821841460973  |  3.39438
2011-09-02 00:00:00  |  -0.38711439720285146  |  3.77121
2011-06-02 00:00:00  |  -0.3877213825416219  |  3.56865
2011-03-02 00:00:00  |  -0.3626515136728962  |  2.10759
2010-12-02 00:00:00  |  -0.40161694132020836  |  1.14316
2010-09-02 00:00:00  |  -0.4236006504159172  |  1.1481
2010-06-02 00:00:00  |  -0.3385166429238293  |  2.02098
2010-03-02 00:00:00  |  -0.22227772379761077  |  2.14333
2009-12-02 00:00:00  |  -0.22960678209076305  |  1.8383
2009-09-02 00:00:00  |  -0.18529077757972015  |  -1.48435
2009-06-02 00:00:00  |  -0.20744571374012302  |  -1.28144
2009-03-02 00:00:00  |  -0.26841870580064964  |  0.23619
2008-12-02 00:00:00  |  -0.2818248213256749  |  1.06958
2008-09-02 00:00:00  |  -0.494878763036081  |  5.37185
2008-06-02 00:00:00  |  -0.44108110764073294  |  4.17554
2008-03-02 00:00:00  |  -0.4029494042007136  |  4.02656
2007-12-02 00:00:00  |  -0.3510371354739516  |  4.3062
