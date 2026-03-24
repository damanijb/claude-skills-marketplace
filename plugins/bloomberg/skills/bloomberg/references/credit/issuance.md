# BQL Issuance, Market Sizing & Issuer Analysis

## BQL Syntax
False
bbg://screens/LPHP CURR:0:1 591037  |  Help!A1
Required Parameters  |  Description  |  let()  |  (Optional) lab expressions for later reuse in your query
Universe  |  The security universe including ticker(s), isin(s), cusip(s) or larger universes such as index members or the bonds universe.
get()  |  DataItem(Parameters) to be retrieved
Data Item(s)  |  The data fields such as Axes(). You can find a current list of available fields via the BQL Builder on the Bloomberg Ribbon in Excel.
for()  |  Security, wrapped in single quotes '
with()  |  (Optional) global parameters that are applied to all applicable data items.
The FOR clause in BQL() can take several inputs, e.g.
Single security  |  - Eg... for(['IBM US Equity'])
List of securities  |  - Eg... for(['VOD LN Equity','IBM US Equity'])
Debt Chains  |  - Eg… for(bonds(['CBA AU Equity']))
Index/Port members  |  - Eg... for(members(['LEGATRUU Index']))
Entire bonds universe  |  - Eg... for(bondsuniv('all'))
let()  |  let(#Spread_Chg =pct_chg(spread(dates=range(-3m,0d)));)
get()  |  Get(#Spread_Chg)
for()  |  for(members('BACR0 Index'))
with()  |  with(fill=prev)

## Market Sizing
Market Size Overview by Sectors
Using BQL we can aggregate total market size for each of the 4 market segments,alone with displaying the  top issuers based on input as of dates.
Data shown are aggregated in Billions in currency of choice.
IG/HY definition are based on selected agency rating at issuance for each bonds.
Group By  |  Level 3 Bclassification  |    |  As of Date 1  |  2026-03-12 00:00:00
Normalize Crncy (Bln)  |  EUR  |  As of Date 2  |  2019-12-01 00:00:00
Rating Agency  |  SP  |  
RTG_SP_INITIAL  |  BB+  |  GET(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B))as#AMT_ISSUED_EUR_Billion)
CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,classification_level=3)  |  GET(groupsort(dropna(matches(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B,CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,classification_level=3) )),grouprank(SUM(GROUP(AMT_Outstanding(CURRENCY=EUR)/1B,CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,classification_level=3) )))<=10),true))as#AMT_ISSUED_EUR_Billion)
GET(groupsort(dropna(matches(SUM(GROUP(AMT_ISSUED(CURRENCY=EUR)/1B,ISSUER)),GROUPRANK(SUM(GROUP(AMT_ISSUED(CURRENCY=EUR)/1B,ISSUER)))<=10),true))as#Top_Issuer_EUR_Billion)
MARKET_CLASSIFICATION=='SSA'  |  SSA  |  FOR(FILTER(BONDSUNIV('ACTIVE'), MARKET_CLASSIFICATION=='SSA' AND (Crncy==EUR  )))
CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)=='Financial Institutions' AND MARKET_CLASSIFICATION!='SSA'  |  Financials  |  FOR(FILTER(BONDSUNIV('ACTIVE'), CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)=='Financial Institutions' AND MARKET_CLASSIFICATION!='SSA'  AND (Crncy==EUR  )))
CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions'  |  Corporate IG  |  FOR(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL>'BB+' and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )))
Corporate HY  |  FOR(FILTER(BONDSUNIV('ACTIVE'),,RTG_SP_INITIAL<='BB+' and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )))
with(dates=2026-03-12)  |  with(dates=2019-12-01)
Segment 1  |  Corporate IG  |    |  Segment 2  |  Financials  |  
Corporate IG  |  Financials
Corporate IG as of 2026-03-12  |  Financials as of  2026-03-12
Issuance Amount  |  Top 10 Issuer  |  Issuance Amount  |  Top 10 Issuer
Total (Billion):  |  #N/A Requesting Data...  |  As of
 2026-03-12  |  Total (Billion):  |  #N/A Requesting Data...
#N/A Requesting Data...  |  #N/A Requesting Data...  |  #N/A Requesting Data...  |  #N/A Requesting Data...
Others  |  #VALUE!  |  Others  |  #VALUE!
Corporate IG as of 2019-12-01
Total (Billion):  |  #N/A Requesting Data...  |  As of
 2019-12-01  |  Total (Billion):  |  #N/A Requesting Data...  |  Financials as of 2019-12-01
#N/A Requesting Data...  |  #N/A Requesting Data...  |  #N/A Requesting Data...  |  #N/A Requesting Data...
Others  |  #VALUE!  |  Others  |  #VALUE!

## Issuance Trends
Issuance Trends by Group with CDS index
BQL can aggregate issuance amount by selected group metrics and display it together with CDS index performance.
CDS Index will only be displayed when USD or EUR is selected as Issuance Currency.
Requesting Data...
ITRXEBE CBBT CURNCY  |  BICS_LEVEL_1_SECTOR_NAME  |  Issue Start  |  2021  |  Group By  |  BICS Sector
Corporate IG Issuance with CDS Index Price  |  Issue End  |  2023  |  Measurement  |  SUM
RTG_SP_INITIAL  |  BB+  |  Market Type  |  Corporate IG  |  Metrics  |  Amount Issued
amt_issued(currency=EUR)/1B  |  Currency Conversion  |  EUR  |  Rating Agency  |  SP
GET(SUM(GROUP(amt_issued(currency=EUR)/1B,year(issue_dt)*100+month(issue_dt)))as#AMT_ISSUED_EUR_Billion)
GET(SUM(GROUP(amt_issued(currency=EUR)/1B,[BICS_LEVEL_1_SECTOR_NAME,year(issue_dt)*100+month(issue_dt)]))as#AMT_ISSUED_EUR_Billion)
SSA  |  FOR(FILTER(BONDSUNIV('ACTIVE'), MARKET_CLASSIFICATION=='SSA' AND (Crncy==EUR  ) and year(issue_dt)>=2021 and year(issue_dt)<=2023))
Financials' exclude SSA  |  FOR(FILTER(BONDSUNIV('ACTIVE'), CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)=='Financial Institutions' AND MARKET_CLASSIFICATION!='SSA' AND MARKET_CLASSIFICATION!='SSA' AND (Crncy==EUR  )  and year(issue_dt)>=2021 and year(issue_dt)<=2023))
Corporate IG  |  FOR(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL>'BB+' and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  ) and year(issue_dt)>=2021 and year(issue_dt)<=2023))
Corporate HY  |  FOR(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL<='BB+' and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )  and year(issue_dt)>=2021 and year(issue_dt)<=2023))
FOR(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL>'BB+' and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  ) and year(issue_dt)>=2021 and year(issue_dt)<=2023))
#N/A Requesting Data...  |  #N/A Requesting Data...  |  EUR/Billion  |  Total  |  #N/A Requesting Data...
#N/A Requesting Data...

## Issuance & Maturity Heatmap
Market Segment Issue and Maturity Schedule
Each market segment bonds can be grouped by year/month to see the history of issuance and schedule of maturity.
Values can be selected either in total amount or total number of bonds.
Normalize Crncy (Bln)  |  EUR  |  Saved Search Name  |  Corporate IG
RTG_SP_INITIAL  |  BB+  |  Start Year  |  2015  |  Rating Agency  |  SP
Measurement  |  SUM
let(#Sum=sum(group(amt_issued()/1b,year(security_pricing_date)*100+month(security_pricing_date)));
#Count=Count(group(ID,year(SECURITY_PRICING_DATE)*100+month(SECURITY_PRICING_DATE)));)  |  let(#amt=amt_outstanding(dates=range(2015-01-01,today));
#mty_amt=last(dropna(if(#amt+0>0,#amt,na)));
#Sum=sum(group(amt_issued()/1b,year(maturity)*100+month(maturity)));
#Count=Count(group(ID,year(maturity)*100+month(maturity)));)
get(DROPNA(#SUM,TRUE))
Government  |  BICS_LEVEL_1_SECTOR_NAME=='Government' AND (Crncy==EUR  )
SSA  |  MARKET_CLASSIFICATION=='SSA' AND (Crncy==EUR  )
Financials' exclude SSA  |  CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)=='Financial Institutions' AND MARKET_CLASSIFICATION!='SSA' AND MARKET_CLASSIFICATION!='SSA' AND (Crncy==EUR  )
Corporate IG  |  RTG_SP_INITIAL>'BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )
Corporate HY  |  RTG_SP_INITIAL<='BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )
for(filter(bondsuniv('all'), security_pricing_date>=2015-01-01 and RTG_SP_INITIAL>'BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )))
for(filter(bondsuniv('all'), maturity>=2015-01-01 and year(maturity)<=year(today) and RTG_SP_INITIAL>'BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' AND (Crncy==EUR  )))
WITH(Currency=EUR)
Issuance Schedule  |  Updating Data…..
#N/A Requesting Data...  |  #N/A Requesting Data...
Month/Year (Bln)  |  2026  |  2025  |  2024  |  2023  |  2022  |  2021  |  2020  |  2019  |  2018
01
02
03
04
05
06
07
08
09
10
11
12
Maturity Schedule
Month/Year (Bln)  |  2026  |  2025  |  2024  |  2023  |  2022  |  2021  |  2020  |  2019  |  2018
01  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
02  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
03  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
04  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
05  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
06  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
07  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
08  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
09  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
10  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
11  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
12  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0
Net Issuance
Month/Year (Bln)  |  2026  |  2025  |  2024  |  2023  |  2022  |  2021  |  2020  |  2019  |  2018
01
02
03
04
05
06
07
08
09
10
11
12

## Issuer Financials vs Market
Issuer Key Stats
BQL helps to map bond segments back to corresponding issuer group. This sheet aggregates issuer level financial stats by issuer rating ( Currency for Financial Issuer).
Target company ID ( both Equity/FI ticker accepted) can be entered to check targted category for comparison.
Market Type  |  IG Corporates  |  Segment Type  |  RATING
Stats  |  MEDIAN  |  Normalize Crncy  |  EUR
RTG_SP_INITIAL  |  Financial Period  |  A  |  Adjusted  |  Y  |  Corporate Issuer
BB+  |  Credit_Rating_Agency  |  SP
Target Issuer  |  ZL509538 Corp  |  is  |  #N/A Requesting Data...
fundamentalticker(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL>'BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' and (Crncy==EUR  ) ))
fundamentalticker(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL<='BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' and (Crncy==EUR  ) ))
fundamentalticker(FILTER(BONDSUNIV('ACTIVE'),RTG_SP_INITIAL>'BB+'  and CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=1)=='Corporate' and  MARKET_CLASSIFICATION!='SSA' AND CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)!='Financial Institutions' and (Crncy==EUR  ) ))
adjusted=Y, FPT=A,RATING_SOURCE=SP,MODE=CACHED
get(MEDIAN(group(DROPNA(TOT_DEBT_TO_EBITDA,TRUE),RATING )))
Leverage & Coverage  |  #N/A Requesting Data...
TOT_DEBT_TO_EBITDA  |  MEDIAN(group(DROPNA(TOT_DEBT_TO_EBITDA,TRUE),RATING )).VALUE  |  Total Debt / EBITDA
NET_DEBT_TO_EBITDA  |  MEDIAN(group(DROPNA(NET_DEBT_TO_EBITDA,TRUE),RATING )).VALUE  |  Net Debt / EBITDA
TOT_DEBT_TO_TOT_CAP  |  MEDIAN(group(DROPNA(TOT_DEBT_TO_TOT_CAP,TRUE),RATING )).VALUE  |  Total Debt to Total Capital
TOT_DEBT_TO_TOT_EQY  |  MEDIAN(group(DROPNA(TOT_DEBT_TO_TOT_EQY,TRUE),RATING )).VALUE  |  Total Debt to Total Equity
EBITDA_TO_TOT_INT_EXP  |  MEDIAN(group(DROPNA(EBITDA_TO_TOT_INT_EXP,TRUE),RATING )).VALUE  |  EBITDA / Interest
Profitability
SALES_5YR_AVG_GR  |  MEDIAN(group(DROPNA(SALES_5YR_AVG_GR,TRUE),RATING )).VALUE  |  Sales 5Yr Avg. Growth  |  #N/A Requesting Data...
GROSS_MARGIN  |  MEDIAN(group(DROPNA(GROSS_MARGIN,TRUE),RATING )).VALUE  |  Gross Margin
OPER_MARGIN  |  MEDIAN(group(DROPNA(OPER_MARGIN,TRUE),RATING )).VALUE  |  Operating Margin
EBITDA_TO_REVENUE  |  MEDIAN(group(DROPNA(EBITDA_TO_REVENUE,TRUE),RATING )).VALUE  |  EBITDA Margin
RETURN_COM_EQY  |  MEDIAN(group(DROPNA(RETURN_COM_EQY,TRUE),RATING )).VALUE  |  Return on Equity
Liquidity & Cash Flow
FREE_CASH_FLOW_MARGIN  |  MEDIAN(group(DROPNA(FREE_CASH_FLOW_MARGIN,TRUE),RATING )).VALUE  |  FCF Margin  |  #N/A Requesting Data...
FCF_TO_TOTAL_DEBT  |  MEDIAN(group(DROPNA(FCF_TO_TOTAL_DEBT,TRUE),RATING )).VALUE  |  Free Cash Flow to Total Debt
CUR_RATIO  |  MEDIAN(group(DROPNA(CUR_RATIO,TRUE),RATING )).VALUE  |  Current Ratio
CASH_RATIO  |  MEDIAN(group(DROPNA(CASH_RATIO,TRUE),RATING )).VALUE  |  Cash Ratio
CASH_CONVERSION_CYCLE  |  MEDIAN(group(DROPNA(CASH_CONVERSION_CYCLE,TRUE),RATING )).VALUE  |  Cash Conversion Cycle
Efficiency & Other
INVENT_TO_WORKING_CAPITAL  |  MEDIAN(group(DROPNA(INVENT_TO_WORKING_CAPITAL,True),RATING )).VALUE  |  Inventories to Working Capital  |  #N/A Requesting Data...
ASSET_TURNOVER  |  MEDIAN(group(DROPNA(ASSET_TURNOVER,TRUE),RATING )).VALUE  |  Asset  Turnover
CAP_EXPEND_TO_SALES  |  MEDIAN(group(DROPNA(CAP_EXPEND_TO_SALES,TRUE),RATING )).VALUE  |  Capital Expenditure to Sales
ALTMAN_Z_SCORE  |  MEDIAN(group(DROPNA(ALTMAN_Z_SCORE,TRUE),RATING )).VALUE  |  Altman's Z-Score
Financial Period  |  A  |  Adjusted  |  Y
Stats  |  MEDIAN  |  Currency  |  EUR
Segment Type  |  CRNCY  |  Financial Issuer
Credit_Rating_Agency  |  SP
Fundamentalticker(FILTER(BONDSUNIV('ACTIVE'), CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS,CLASSIFICATION_LEVEL=2)=='Financial Institutions' AND MARKET_CLASSIFICATION!='SSA' and (Crncy==EUR  ) ))
adjusted=Y, FPT=A,rating_source=SP,MODE=CACHED  |  Target Issuer  |  DBK GY Equity  |  is  |  #N/A Requesting Data...
#N/A Requesting Data...
BS_TOT_ASSET(CURRENCY=EUR)/1B  |  MEDIAN(group(DROPNA(BS_TOT_ASSET(CURRENCY=EUR)/1B,TRUE),CRNCY )).VALUE  |  Macro, Size & Market Metrics  |  Assets (Bln)
CUR_MKT_CAP(CURRENCY=EUR)/1B  |  MEDIAN(group(DROPNA(CUR_MKT_CAP(CURRENCY=EUR)/1B,TRUE),CRNCY )).VALUE  |  Market Cap (Bln)
PX_TO_TANG_BV_PER_SH  |  MEDIAN(group(DROPNA(PX_TO_TANG_BV_PER_SH,TRUE),CRNCY )).VALUE  |  Price / Tangible Book
RETURN_ON_ASSET  |  MEDIAN(group(DROPNA(RETURN_ON_ASSET,TRUE),CRNCY )).VALUE  |  Profitability  |  Return on Assets
RETURN_COM_EQY  |  MEDIAN(group(DROPNA(RETURN_COM_EQY,TRUE),CRNCY )).VALUE  |  Return on Equity
SALES_5YR_AVG_GR  |  MEDIAN(group(DROPNA(SALES_5YR_AVG_GR,TRUE),CRNCY )).VALUE  |  Sales 5Yr Avg. Growth
NET_INT_MARGIN  |  MEDIAN(group(DROPNA(NET_INT_MARGIN,TRUE),CRNCY )).VALUE  |  Net Interest Margin
EFF_RATIO  |  MEDIAN(group(DROPNA(EFF_RATIO,TRUE),CRNCY )).VALUE  |  Efficiency Ratio
TOT_LOAN_TO_TOT_DPST  |  MEDIAN(group(DROPNA(TOT_LOAN_TO_TOT_DPST,TRUE),CRNCY )).VALUE  |  Liquidity  |  Total Loans / Total Deposits
TOT_LOAN_TO_TOT_ASSET  |  MEDIAN(group(DROPNA(TOT_LOAN_TO_TOT_ASSET,TRUE),CRNCY )).VALUE  |  Total Loans / Total Assets
BS_LIQUID_ASSETS/BS_TOT_ASSET  |  MEDIAN(group(DROPNA(BS_LIQUID_ASSETS/BS_TOT_ASSET,TRUE),CRNCY )).VALUE  |  Liquid Assets / Total Assets
DEPOSITS_TO_FUNDING  |  MEDIAN(group(DROPNA(DEPOSITS_TO_FUNDING,TRUE),CRNCY )).VALUE  |  Deposits / Funding
GROWTH_IN_TOT_DPST  |  MEDIAN(group(DROPNA(GROWTH_IN_TOT_DPST,TRUE),CRNCY )).VALUE  |  1Yr Deposit Growth
TEXAS_RATIO  |  MEDIAN(group(DROPNA(TEXAS_RATIO,TRUE),CRNCY )).VALUE  |  Credit Quality  |  Texas Ratio
RSRV_FOR_LOAN_LOSS_TO_TOT_LOAN  |  MEDIAN(group(DROPNA(RSRV_FOR_LOAN_LOSS_TO_TOT_LOAN,TRUE),CRNCY )).VALUE  |  Reserve for Loan Losses / Total Loans
NPLS_TO_TOTAL_LOANS  |  MEDIAN(group(DROPNA(NPLS_TO_TOTAL_LOANS,TRUE),CRNCY )).VALUE  |  NPL's / Total Loans
RESERVE_LOAN_LOSSES_TO_NPLS  |  MEDIAN(group(DROPNA(RESERVE_LOAN_LOSSES_TO_NPLS,TRUE),CRNCY )).VALUE  |  Loan Loss Reserve / NPL's
IS_PROV_FOR_LOAN_LOSS/PRETAX_PRE_PROVISION_PROFIT  |  MEDIAN(group(DROPNA(IS_PROV_FOR_LOAN_LOSS/PRETAX_PRE_PROVISION_PROFIT,TRUE),CRNCY )).VALUE  |  Loan Loss Prov. / Pre-Prov. Pre-Tax Profit
BS_TIER1_COM_EQUITY_RATIO  |  MEDIAN(group(DROPNA(BS_TIER1_COM_EQUITY_RATIO,TRUE),CRNCY )).VALUE  |  Capital  |  Tier 1 Common Equity Ratio
BS_TIER1_CAP_RATIO  |  MEDIAN(group(DROPNA(BS_TIER1_CAP_RATIO,TRUE),CRNCY )).VALUE  |  Tier 1 Risk-Based Capital Ratio
BS_TOT_CAP_TO_RISK_BASE_CAP  |  MEDIAN(group(DROPNA(BS_TOT_CAP_TO_RISK_BASE_CAP,TRUE),CRNCY )).VALUE  |  Total Risk-Based Capital Ratio
BS_LEV_RATIO_TO_TANG_CAP  |  MEDIAN(group(DROPNA(BS_LEV_RATIO_TO_TANG_CAP,TRUE),CRNCY )).VALUE  |  Leverage Ratio

## Issuer Financials
Individual Issuer Financial Stats Dashboard  |  HEIA NA Equity Price vs CDS  |  #N/A Requesting Data...
This tab displays detailed issuer level information ranging from financial stats, debt (maturity) profile, issuer curve to peer analysis.
GICS_SECTOR_NAME  |  #N/A Requesting Data...
GICS_INDUSTRY_NAME  |  PX_LAST  |  Issuer Ticker  |  HEIA NA Equity  |  Share Price  |  #N/A Requesting Data...
GICS_SUB_INDUSTRY_NAME  |  EQY_SH_OUT/1m  |  Financial Period Type  |  A  |  *Shares Out(M)
COMPANY_TEL_NUMBER  |  CUR_MKT_CAP/1m  |  Converting Currency  |  EUR  |  =Market Capitalization
COMPANY_WEB_ADDRESS  |  CASH_AND_ST_INVESTMENTS/1m  |  -Cash and Equivalents
COUNTRY_FULL_NAME  |  SHORT_AND_LONG_TERM_DEBT/1m  |  #N/A Requesting Data...  |  +Total Debt
PRIMARY_EXCHANGE_NAME  |  BS_PFD_EQY/1m  |  #N/A Requesting Data...  |  +Preferred Equity
MINORITY_NONCONTROLLING_INTEREST/1m  |  +Total Minority Interest
ENTERPRISE_VALUE/1M  |  =Enterprise Value
#N/A Requesting Data...
SALES_REV_TURN()/1M  |  Total Revenue
SALES_GROWTH/100  |  PoP Growth
GROSS_PROFIT/1M  |  Gross Profit
GROSS_PROFIT/SALES_REV_TURN  |  Margin
EBITDA/1M  |  EBITDA
EBITDA/SALES_REV_TURN  |  Margin
EBIT/1M  |  EBIT
EBIT/SALES_REV_TURN  |  Margin
Net_Income/1m  |  Net Income
Net_income/sales_rev_turn  |  Margin
IS_DIL_EPS_BEF_XO  |  Diluted EPS Excl. Extra Items
EPS_GROWTH  |  PoP Growth
CF_CASH_FROM_OPER/1M  |  Cash from Operations
CFO_SEQUENTIAL_GROWTH/100  |  PoP Growth
CAPITAL_EXPEND/1M  |  Capital Expenditures
TOT_CAP_EXPEND_GROWTH/100  |  PoP Growth
CF_FREE_CASH_FLOW/1M  |  Free Cash Flow
FREE_CASH_FLOW_1_YEAR_GROWTH/100  |  PoP Growth
#N/A Requesting Data...
EV_TO_SALES  |  Enterprise Value/Tot Rev
EV_TO_EBITDA  |  Enterprise Value/EBITDA
EV_TO_EBIT  |  Enterprise Value/EBIT
IS_DIL_EPS_BEF_XO  |  Diluted EPS Before Extraordinary Items
#N/A Requesting Data...
Debt Profile
#N/A Requesting Data...
HEIA NA Equity Bonds Maturity Schedule (Bn)  |  Company Ticker  |  CREDIT_FAMILY
GET(SUM(GROUP(AMT_OUTSTANDING(CURRENCY=EUR)/1B,YEAR(MATURITY))))
FOR(BONDS('HEIA NA Equity',ISSUEDBY=CREDIT_FAMILY))  |  CAST  |  Millions  |  Count
Total Debt  |  #N/A Requesting Data...  |  #N/A Requesting Data...
Total Loans  |  -  |  -
Total Bonds  |  #N/A Requesting Data...  |  #N/A Requesting Data...
Total Secured Bonds  |  0  |  0
1st lien  |  1st Lien Bonds  |  -  |  -
2nd lien  |  2nd Lien Bonds  |  -  |  -
Secured  |  Secured Bonds  |  -  |  -
Total Unsecured Bonds  |  0  |  0
Sr Unsecured  |  Senior Unsecured Bonds/Notes  |  -  |  -
Unsecured  |  Unsecured Bonds  |  -  |  -
Total Subordinated Bonds  |  0  |  0
Sr Subordinated  |  Sr Subordinated Bonds/Notes  |  -  |  -
Subordinated  |  Subordinated Bonds/Notes  |  -  |  -
Jr Subordinated  |  Jr Subordinated Bonds/Notes  |  -  |  -
Preferred Shares  |  #N/A Requesting Data...
Issuer Curves /Interpolation
for(filter(bonds('HEIA NA Equity'),crncy==EUR))
get(GROUPSORT(MATURITY_YEARS,ORDER=ASC) AS#MATURITY_YEARS,spread(st=I).VALUE AS#I_Spread )
spread(st=I)  |  Filter  |  crncy==EUR  |  Regressing Point  |  Regresion Result  |  #N/A Requesting Data...
X Metric  |  MATURITY_YEARS  |  1Y  |  #N/A Requesting Data...  |  1
Y Metric  |  I_Spread  |  2Y  |  #N/A Requesting Data...  |  2
Regression Method  |  NELSON_SIEGEL  |  3Y  |  #N/A Requesting Data...  |  3
5Y  |  #N/A Requesting Data...  |  5
7Y  |  #N/A Requesting Data...  |  7
10Y  |  #N/A Requesting Data...  |  10
15Y  |  #N/A Requesting Data...  |  15
20Y  |  #N/A Requesting Data...  |  20
25Y  |  #N/A Requesting Data...  |  25
Peers Comparison (Peers from EQRV <GO> )
Bloomberg_Best_Fit  |  Name  |  Total Debt/EBITDA  |  Interest Coverage  |  Total Debt/Total Capital  |  Price/Book
Long_comp_name  |  TOT_DEBT_TO_EBITDA().value  |  INTEREST_COVERAGE_RATIO().value  |  TOT_DEBT_TO_TOT_CAP().value  |  PX_TO_BOOK_RATIO().value
#N/A

## Issuer Debt Analysis
Issuer Analysis on Issuance
BQL offers New Issuance Analytics for bonds. This tab displays new issuance data and calculated post issuance performance for target Ticker.
Ticker  |  HEIANA
let(#band=MID;
#IPT_TYPE = ISSUANCE_PRICING(STAGE=IPT, BAND=#band).PRICING_TYPE;
#GUID_TYPE=ISSUANCE_PRICING(STAGE=GUIDANCE, BAND=#band).PRICING_TYPE;
#REV_TYPE=ISSUANCE_PRICING(STAGE=REVISED_GUIDANCE, BAND=#band).PRICING_TYPE;
#FIN_GUID_TYPE=ISSUANCE_PRICING(STAGE=FINAL_GUIDANCE, BAND=#band).PRICING_TYPE;
#PRICING_TYPE = if(#IPT_TYPE!=na, #IPT_TYPE, if(#GUID_TYPE!=na, #GUID_TYPE, if(#REV_TYPE!=na, #REV_TYPE, if(#FIN_GUID_TYPE!=na, #FIN_GUID_TYPE, "-"))));)
Get()  |  get(name,yield().value as#YIELD,
duration().value AS#DURATION,cpn_type,cpn, MATURITY,  (maturity-issue_dt)/365.25 as #MTY_TO_ISSUE, (maturity-today)/365.25 AS #MTY_YEARS, ANNOUNCE_DT, SECURITY_PRICING_DATE, amt_issued().value/1m AS#AMT_ISSUE_M,BB_COMPOSITE,  CRNCY, ISSUANCE_PRICING(STAGE=IPT, BAND=#band) AS#IPT,
ISSUANCE_PRICING(STAGE=GUIDANCE, BAND=#band) AS#GUIDANCE, ISSUANCE_PRICING(STAGE=REVISED_GUIDANCE, BAND=#band)AS#REV_GDN, ISSUANCE_PRICING(STAGE=FINAL_GUIDANCE, BAND=#band)AS#FINAL_GDN,
#IPT_TYPE,
BENCHMARK_FOR_PRICING,
ISSUANCE_PRICING(STAGE=PRICED)AS#PRICED,
ISSUANCE_PRICING(STAGE=PRICED).PRICING_TYPE AS #PRICED_PRICING_TYPE,
NEW_ISSUE_COMPRESSION,
ISSUE_PX,
net_chg(dropna(PX_LAST(fill=prev,dates=RANGE(PERIDSCALAR(ISSUE_DATE()),PERIDSCALAR(ISSUE_DATE()+7d))))).VALUE as#1W_BPS_CHG,
net_chg(dropna(PX_LAST(fill=prev,dates=RANGE(PERIDSCALAR(ISSUE_DATE()),PERIDSCALAR(ISSUE_DATE()+14d))))).VALUE as#2W_BPS_CHG,
(px_last().value-issue_px().value)as#2ND_Mkt_PERF
)
For()  |  for(filter(bondsuniv('active'),ticker==HEIANA and (Crncy==EUR  ) and (Payment_Rank=='Sr Unsecured'  )))
Descriptive Data  |  New Issuance Data  |  Post-Issue Performance  |  Primary Market Data(BDP)
N/A REQUESTING DATA...  |  ACTIVE_BOOKRUNNERS  |  BOOK_SIZE  |  COVER_RATIO_FOR_INITIAL_ISSUANCE
#N/A Requesting Data...  |  ACTIVE_BOOKRUNNERS  |  BOOK_SIZE  |  COVER_RATIO_FOR_INITIAL_ISSUANCE

## Comparable Analysis
Sector Analysis on Active Past Issuance
Based on input ticker from tab "Issuer Primary Stats", comparable bonds can be identified based on industry/rating/issuance date range criteria.
Same BCLASS LEVEL  |  3  |  #N/A Requesting Data...
Rating Range  |  BBB+  |  AA
date range  |  2024-12-02 00:00:00  |  2026-03-12 00:00:00
Market Issuance Stats
AVG COMPRESSION  |  #N/A
AVG 1W PERFORMANCE  |  #N/A
AVG 2W PERFORMANCE  |  #N/A
GET(AVG(GROUP(NEW_ISSUE_COMPRESSION)))
GET(AVG(GROUP(net_chg(dropna(PX_LAST(fill=prev,dates=RANGE(PERIDSCALAR(ISSUE_DATE()),PERIDSCALAR(ISSUE_DATE()+7d))))))))
GET(AVG(GROUP(net_chg(dropna(PX_LAST(fill=prev,dates=RANGE(PERIDSCALAR(ISSUE_DATE()),PERIDSCALAR(ISSUE_DATE()+14d))))))))
for(filter(bondsuniv('active'),CLASSIFICATION_NAME(CLASSIFICATION_LEVEL=3)=='#N/A Requesting Data...' AND BB_COMPOSITE >='BBB+' AND BB_COMPOSITE<='AA' AND SECURITY_PRICING_DATE>=2024-12-02 AND SECURITY_PRICING_DATE<=2026-03-12 and (Crncy==EUR  ) and (Payment_Rank=='Sr Unsecured'  )))
Descriptive Data  |  New Issuance Data  |  Post-Issue Performance  |  Primary Market Data(BDP)
N/A  |  ACTIVE_BOOKRUNNERS  |  BOOK_SIZE  |  COVER_RATIO_FOR_INITIAL_ISSUANCE  |  COVER_RATIO_FOR_INITIAL_ISSUANCE
#N/A  |  ACTIVE_BOOKRUNNERS  |  BOOK_SIZE  |  COVER_RATIO_FOR_INITIAL_ISSUANCE  |  COVER_RATIO_FOR_INITIAL_ISSUANCE
