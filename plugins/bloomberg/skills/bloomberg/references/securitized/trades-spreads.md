# BQL TRACE Trades & Spreads

## BQL Syntax
False
bbg://screens/LPHP CURR:0:1 591037  |  Help!A1
Required Parameters  |  Description  |  let()  |  (Optional) lab expressions for later reuse in your query
Universe  |  The security universe including ticker(s), isin(s), cusip(s) or larger universes such as index members or the bonds universe.
get()  |  DataItem(Parameters) to be retrieved
Data Item(s)  |  The data fields such as trade_data(). You can find a current list of available fields via the BQL Builder on the Bloomberg Ribbon in Excel.
for()  |  Security, wrapped in single quotes '
with()  |  (Optional) global parameters that are applied to all applicable data items.
The FOR clause in BQL() can take several inputs, e.g.
Single security  |  - Eg... for(['FN MA4732 Mtge'])
List of securities  |  - Eg... for(['FN MA4732 Mtge', 'BMARK 2024-V5 A3 Mtge', 'TAOT 2024-A A3 Mtge'])
Debt Chains  |  - Eg… for(mortgages(['FN MA4732 Mtge']))
Index/Port members  |  - Eg... for(members(['LUMSTRUU Index']))
Entire mortgages universe  |  - Eg... for(mortgagesuniv('all'))
get()  |  get(trade_data(source=TRACE))
for()  |  for('FN MA4732 Mtge')
with()  |  with(dates=range(-3m,0d))

## Trades & Spreads Syntax
What's New?
The Trade and Spreads dataset within the CPR<GO> application on the Bloomberg Professional allows you to analyze TRACE reported trades and calculated analytical results for various Fixed Income securitized Product sectors such as Asset Backed and Credit Risk Transfer securities.
Bloomberg Terminal functions (TDH<GO>,CPR<GO>, MM<GO>) combine TRACE-disseminated trade prices, with the Bloomberg cashflow engine and appropriate cashflow assumptions to solve for yields/spreads/discounts margins based on actual trades.
These spreads/discount margins are displayed as indivudal trade results but can also be aggregated into cohorts to track current and historical spread levels for various sectors.
Access to this dataset is now available via BQL (Bloomberg Query Language) using the trade_data field.
Using this dataset via BQL, like you would in TDH<GO>, MM<GO> and CPR<GO> you can:
• View individual securities TRACE based Trade disseminated information such as Trade Date, Price, Trade Size and Bloomberg calculated spread levels based upon multiple industry standard trading scenarios
• View individual spread levels based upon custom security lists based upon broad characteristics such as issuer/Tickers, WAL's, Trade Size, Ratings and Bloomberg Asset Class sector based classification system (SPECS)
• Calculate Aggregated spread levels based upon custom securities lists that are important to you
• View Trade data based upon your portfolio or inventory lists already saved via the Bloomberg Professional Terminal
• View Trade analytics results based upon scenarios and workout assumptions (worst, call, maturity) that are important to you
• This trade based spread analytical results gives you the information that is critical so that you can easily obtain the latest spread levels and trends that are most important to you and your investments. Thus, helping you maximize your return potential
• Access industry standard TRACE trades and additional relevant data leveraging the three pre-canned views (offering increasing levels of granularity) or create your custom view directly using BQL
Learn more about CPR<GO> here
Learn more about MM<GO> here
Learn more about TDH<GO> here
BQL Syntax for TRACE Trades & Spreads
• The trade_data field returns trades info and calculated yields and spreads for Agency CMOs, RMBS, ABS, and CRT securities based on TRACE-reported trade data, so you can get a better picture of a bond or cohorts reported trade history
• Specify the security for which you want to analyze trade info, yields and spreads based on TRACE-reported trades prices. Select a from industry standard robust prepayment scenarios and the assocaited  yield/spread analytics, and a date range for the trade data
• You can filter the dataset for the chosen universe by date, time, volumes, prices or any derived yields and spreads to focus on specific trades like you can do in TDH<GO> and CPR<GO> in the Bloomberg Terminal
Field
Field  |  Definition  |  Description
trade_data  |  TRACE Trades and Spreads  |  Returns trade records, yields and spreads based on TRACE-reported trades for your universe of choice
Parameters
Parameter  |  SOURCE  |  DATES  |  SCENARIO  |  WORKOUT  |  VIEW
Parameter Type  |  Mandatory  |  Optional  |  Optional  |  Optional  |  Optional
Definition  |  Data Source  |  Trade Date  |  Cashflow Scenario  |  Workout  |  View
Description  |  Source of the data  |  Allows to specify a single date or a range of dates for the analysis  |  Credit scenarios  |  Sets the calculation method - Analytics for each TRACE-reported trade are calculated to worst, call, and maturity.  |  Standard (Default)  - Returns a minimum set of trade data points:
ID, PRICE, DATE, TIME, VOLUME, SETTLE_DATE, CURRENCY, CONDITION CODE
Mtge_Analytics - Enriched set of data points which combines the data points available in the standard with with additional analytics:
ID, PRICE, DATE, TIME, VOLUME, SETTLE_DATE, CURRENCY, CONDITION CODE, ADJUSTED_VOLUME, YIELD, I_SPREAD,
DISCOUNT_MARGIN, WAL, WORKOUT, SCENARIO, PREPAY_SPEED, PREPAY_TYPE
Mtge_Extended - Returns a more extensive set of data points:
ID, PRICE, DATE, TIME, VOLUME, SETTLE_DATE, CURRENCY, CONDITION CODE, ADJUSTED_VOLUME, YIELD, I_SPREAD, DISCOUNT_MARGIN, WAL, WORKOUT, SCENARIO, PREPAY_SPEED, PREPAY_TYPE, Z_SPREAD, E_SPREAD, N_SPREAD, P_SPREAD, R_SPREAD, J_SPREAD, FACTOR, IS_CONTRIBUTED_CASH_FLOW, RTG_FITCH_AT_TRADE_DATE, RTG_SP_AT_TRADE_DATE, RTG_MOODY_AT_TRADE_DATE, RTG_KBRA_AT_TRADE_DATE
Accepted Values  |  TRACE  |  • Single Date
Absolute - dates=YYYY-MM-DD
Relative - dates=-1m
• Range
dates=range(YYYY-MM-DD,YYYY-MM-DD)
Note - Alternatively, if you want to use DD/MM/YYYY or MM/DD/YYYY formats to represent the date, use the BQL.Date() function to convert the date to YYYY-MM-DD  |  • MED
• H1M
• H3M
• H6M
• BAM
• BTM
• PX
• CF
• CONTRIBUTED  |  • TO_WORST
• TO_CALL
• TO_MATURITY  |  • STANDARD
• MTGE_ANALYTICS
• MTGE_EXTENDED
Default Value  |  Not Applicable  |  -1d  |  PX  |  TO_WORST  |  STANDARD
Examples  |  =BQL("AMCAR 2024-1 A3 Mtge","trade_data(source=TRACE)","showallcols=t")  |  =BQL("AMCAR 2024-1 A3 Mtge","trade_data(source=TRACE, dates=range(-3m,0d))","showallcols=t")  |  =BQL("AMCAR 2024-1 A3 Mtge",
"trade_data(source=TRACE, scenario=PX)","showallcols=t")  |  =BQL("AMCAR 2024-1 A3 Mtge","trade_data(source=TRACE, scenario=PX, workout=TO_WORST)","showallcols=t")  |  =BQL("AMCAR 2024-1 A3 Mtge","trade_data(source=TRACE, dates=range(-6m,0d), scenario=PX, workout=TO_WORST, view=MTGE_ANALYTICS)","showallcols=t")
Associated Columns (Metadata)
• trade_data returns the price of the trade as default but using "showallcols=t" as you execute your bql query gives you access to several derived analytics and data points
• As default, the pre-canned standard view, returns a set of columns showing key details for the trades over the specified time range
• Additional data (derived analytics) is accessible with the mtge_analytics and mtge_extended views, which contain several data points available to you for your relative value analysis
Views
Associated Cols  |  Description  |  Standard  |  Mtge_Analytics  |  Mtge_Extended
ID  |  Security Identifier  |  included  |  included  |  included
PRICE  |  Trade price  |  included  |  included  |  included
DATE  |  Trade date  |  included  |  included  |  included
TIME  |  Trade time  |  included  |  included  |  included
VOLUME  |  Original Face Volume (Reported Volume)  |  included  |  included  |  included
SETTLE_DATE  |  Settle date  |  included  |  included  |  included
CURRENCY  |  Currency of the trade  |  included  |  included  |  included
CONDITION CODE  |  Condition code for the trade  |  included  |  included  |  included
ADJUSTED_VOLUME  |  Current Face Volume (Reported volume adjusted by the factor at trade date)  |  optional  |  included  |  included
YIELD  |  Yield  |  optional  |  included  |  included
I_SPREAD  |  I Spread  |  optional  |  included  |  included
DISCOUNT_MARGIN  |  Discount margin  |  optional  |  included  |  included
WAL  |  Weighted average Life  |  optional  |  included  |  included
WORKOUT  |  Workout to worst/call/maturity  |  optional  |  included  |  included
SCENARIO  |  Scenario  |  optional  |  included  |  included
PREPAY_SPEED  |  Prepay speed  |  optional  |  included  |  included
PREPAY_TYPE  |  Prepay type  |  optional  |  included  |  included
Z_SPREAD  |  Z Spread  |  optional  |  optional  |  included
E_SPREAD  |  E Spread  |  optional  |  optional  |  included
N_SPREAD  |  N Spread  |  optional  |  optional  |  included
P_SPREAD  |  P Spread  |  optional  |  optional  |  included
R_SPREAD  |  R Spread  |  optional  |  optional  |  included
J_SPREAD  |  J Spread  |  optional  |  optional  |  included
FACTOR  |  Current face of the traded security at the trade date  |  optional  |  optional  |  included
IS_CONTRIBUTED_CASH_FLOW  |  Contributed cashflow flag  |  optional  |  optional  |  included
RTG_FITCH_AT_TRADE_DATE  |  Fitch rating as of trade date  |  optional  |  optional  |  optional
RTG_SP_AT_TRADE_DATE  |  S&P rating as of trade date  |  optional  |  optional  |  optional
RTG_MOODY_AT_TRADE_DATE  |  Moody rating as of trade date  |  optional  |  optional  |  optional
RTG_KBRA_AT_TRADE_DATE  |  KBRA rating as of trade date  |  optional  |  optional  |  optional
• You can access the additional data (metadata) for the different views using "showallcols=t" when you execute your bql query
Enter Security  |  AMCAR 2024-1 A3 Mtge
Select View  |  Mtge_Extended
ID  |  AMCAR 2024-1 A3 Mtge
DATES  |  45573
TIME  |  09:43
SETTLE_DATE  |  45574
VOLUME  |  340
ADJUSTED_VOLUME  |  340
PREPAY_SPEED  |  1.5
PREPAY_TYPE  |  ABS
YIELD  |  4.68747124636
I_SPREAD  |  62.98829360579
DISCOUNT_MARGIN
WAL  |  1900-01-01 15:41:49.982000
WORKOUT  |  Worst
SCENARIO  |  PX
CURRENCY  |  USD
CONDITION_CODE
Z_SPREAD  |  64.55866478728
E_SPREAD  |  79.64911344848
N_SPREAD  |  52.77373502338
P_SPREAD  |  81.4673732581
R_SPREAD  |  79.09651593631
J_SPREAD  |  62.47671854277
FACTOR  |  1
IS_CONTRIBUTED_CASH_FLOW  |  N
#trades  |  101.25
• Download all the available data points for the different pre-canned views using preferences(addcols=[ALL]) when you execute your bql query
ID  |  AMCAR 2024-1 A3 Mtge
DATES  |  45573
TIME  |  09:43
SETTLE_DATE  |  45574
VOLUME  |  340
ADJUSTED_VOLUME  |  340
PREPAY_SPEED  |  1.5
PREPAY_TYPE  |  ABS
YIELD  |  4.68747124636
I_SPREAD  |  62.98829360579
DISCOUNT_MARGIN
WAL  |  1.65405071371
WORKOUT  |  Worst
SCENARIO  |  PX
CURRENCY  |  USD
CONDITION_CODE
Z_SPREAD  |  1900-03-04 13:24:28.638000
E_SPREAD  |  79.64911344848
N_SPREAD  |  52.77373502338
P_SPREAD  |  81.4673732581
R_SPREAD  |  79.09651593631
J_SPREAD  |  62.47671854277
FACTOR  |  1
IS_CONTRIBUTED_CASH_FLOW  |  N
RTG_FITCH_AT_TRADE_DATE  |  N.A.
RTG_SP_AT_TRADE_DATE  |  AAA
RTG_MOODY_AT_TRADE_DATE  |  Aaa
RTG_KBRA_AT_TRADE_DATE  |  N.A.
#trades  |  101.25
• Append selected data points to the output of different views using preferences(addcols=['Column Header1','Column Header2']) when you execute your bql query
For example, use preferences(addcols=['I_SPREAD','WAL']) when you execute your bql query to retrieve I-Spread and WAL alongside the trade details returned in the standard view
ID  |  AMCAR 2024-1 A3 Mtge
DATES  |  45573
TIME  |  09:43
SETTLE_DATE  |  2024-10-09 00:00:00
VOLUME  |  1900-12-05 00:00:00
CURRENCY  |  USD
CONDITION_CODE
I_SPREAD  |  62.98829360579
WAL  |  1.65405071371
#trades  |  101.25

## Examples - Basic
TRACE Trades & Spreads
• The Trades & Spreads dataset allows you to analyze TRACE trade data for securitized securities, such as asset-backed (ABS) and credit risk transfer (CRT) deals.
• Evaluate yields, spreads, discount margins, and weighted average life (WAL) for individual or aggregated trades to determine appropriate valuations for a given security or sector.
Note:
• As default the BQL query returns the traded price, more derived data is accessible using "showallcols=t"
• When a custom date/date range is not specified, trades for the previous day are returned (current day trades are not available)
• Prepayment speed scenario defaults to pricing speed (speed at which deal was brought to market at)
• Workout for yield and spread calculations defaults to worst
Trade Data - Pre-canned and custom views
Security
Bond  |  AMCAR 2024-1 a3 Mtge
Name  |  AMCAR 2024-1 A3
Security Type  |  ABS
Inputs
Range - Start Date  |  2024-09-01 00:00:00
Range - End Date  |  2024-09-30 00:00:00
Scenario  |  PX
Workout  |  TO_WORST
View: STANDARD
View  |  STANDARD
View/Get()  |  dropna(TRADE_DATA(SOURCE=TRACE, SCENARIO=PX , WORKOUT=TO_WORST,
VIEW=STANDARD, dates=range(2024-09-01, 2024-09-30))) as #trades
Universe/For()  |  AMCAR 2024-1 a3 Mtge
BQL Query  |  get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=STANDARD,dates=range(2024-09-01,2024-09-30))) as #trades) for(['AMCAR 2024-1 a3 Mtge'])
Default response
AMCAR 2024-1 A3 Mtge
DATES  |  #trades
2024-09-13 00:00:00  |  101.6875
2024-09-13 00:00:00  |  101.718811
2024-09-24 00:00:00  |  101.625
2024-09-30 00:00:00  |  101.796906
Alternatively, COPY the query below and paste in a new cell/sheet:
=BQL.QUERY("get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=STANDARD,dates=range(2024-09-01,2024-09-30))) as #trades) for(['AMCAR 2024-1 a3 Mtge'])")
Use "showallcols=t" as you execute your query in Excel to retrieve an enriched response with the default set of associated columns (metadata)
#N/A Requesting Data...
Alternatively, COPY the query below and paste in a new cell/sheet:
=BQL.QUERY("get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=STANDARD,dates=range(2024-09-01,2024-09-30))) as #trades) for(['AMCAR 2024-1 a3 Mtge'])","showallcols=t")
View: ANALYTICS
View  |  MTGE_ANALYTICS
View/Get()  |  dropna(TRADE_DATA(SOURCE=TRACE, SCENARIO=PX , WORKOUT=TO_WORST,
VIEW=MTGE_ANALYTICS, dates=range(2024-09-01, 2024-09-30))) as #trades
Universe/For()  |  AMCAR 2024-1 a3 Mtge
BQL Query  |  get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=MTGE_ANALYTICS,dates=range(2024-09-01,2024-09-30))) as #trades) for(['AMCAR 2024-1 a3 Mtge'])
Use "showallcols=t" as you execute your query in Excel to retrieve the default set of associated columns
ID  |  DATES  |  TIME  |  SETTLE_DATE  |  VOLUME  |  ADJUSTED_VOLUME  |  PREPAY_SPEED  |  PREPAY_TYPE  |  YIELD  |  I_SPREAD  |  DISCOUNT_MARGIN  |  WAL  |  WORKOUT  |  SCENARIO  |  CURRENCY  |  CONDITION_CODE  |  #trades
AMCAR 2024-1 A3 Mtge  |  45548  |  12:40  |  45551  |  45  |  45  |  1900-01-01 12:00:00  |  ABS  |  4.44673462506  |  76.70676941133  |  1.71622276721  |  Worst  |  PX  |  USD  |  101.6875
AMCAR 2024-1 A3 Mtge  |  45548  |  13:12  |  45551  |  45  |  45  |  1900-01-01 12:00:00  |  ABS  |  4.42756846107  |  74.53948775668  |  1.71622276721  |  Worst  |  PX  |  USD  |  101.718811
AMCAR 2024-1 A3 Mtge  |  45559  |  15:50  |  45560  |  70  |  70  |  1900-01-01 12:00:00  |  ABS  |  4.4717619126  |  85.14086661165  |  1.6929396026  |  Worst  |  PX  |  USD  |  101.625
AMCAR 2024-1 A3 Mtge  |  45565  |  14:58  |  45566  |  70  |  70  |  1900-01-01 12:00:00  |  ABS  |  4.35445916691  |  59.88734068357  |  1.67627293593  |  Worst  |  PX  |  USD  |  101.796906
Alternatively, COPY the query below and paste in a new cell/sheet:
=BQL.QUERY("get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=MTGE_ANALYTICS,dates=range(2024-09-01,2024-09-30))) as #trades) for(['AMCAR 2024-1 a3 Mtge'])","showallcols=t")
View: EXTENDED
View  |  MTGE_EXTENDED
View/Get()  |  dropna(TRADE_DATA(SOURCE=TRACE, SCENARIO=PX , WORKOUT=TO_WORST,
VIEW=MTGE_EXTENDED, dates=range(2024-09-01, 2024-09-30))) as #trades
Universe/For()  |  AMCAR 2024-1 a3 Mtge
BQL Query  |  get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=MTGE_EXTENDED,dates=range(2024-09-01,2024-09-30))) as #trades) for(['AMCAR 2024-1 a3 Mtge'])
Use "showallcols=t" as you execute your query in Excel to retrieve the default set of associated columns
ID  |  AMCAR 2024-1 A3 Mtge  |  AMCAR 2024-1 A3 Mtge  |  AMCAR 2024-1 A3 Mtge  |  AMCAR 2024-1 A3 Mtge
DATES  |  45548  |  45548  |  45559  |  45565
TIME  |  12:40  |  13:12  |  15:50  |  14:58
SETTLE_DATE  |  45551  |  45551  |  45560  |  45566
VOLUME  |  45  |  45  |  70  |  70
ADJUSTED_VOLUME  |  45  |  45  |  70  |  70
PREPAY_SPEED  |  1.5  |  1.5  |  1.5  |  1.5
PREPAY_TYPE  |  ABS  |  ABS  |  ABS  |  ABS
YIELD  |  4.44673462506  |  4.42756846107  |  4.4717619126  |  4.35445916691
I_SPREAD  |  76.70676941133  |  74.53948775668  |  85.14086661165  |  59.88734068357
DISCOUNT_MARGIN
WAL  |  1900-01-01 17:11:21.647000  |  1900-01-01 17:11:21.647000  |  1900-01-01 16:37:49.982000  |  1900-01-01 16:13:49.982000
WORKOUT  |  Worst  |  Worst  |  Worst  |  Worst
SCENARIO  |  PX  |  PX  |  PX  |  PX
CURRENCY  |  USD  |  USD  |  USD  |  USD
CONDITION_CODE
Z_SPREAD  |  80.67257964215  |  78.5208010583  |  88.66025042786  |  63.5159493777
E_SPREAD  |  95.68149527395  |  93.97022389359  |  104.65844467111  |  79.82254476054
N_SPREAD  |  67.99493000753  |  65.87497664174  |  77.83024787934  |  53.57204988359
P_SPREAD  |  97.98786744571  |  95.85847271974  |  107.01130317016  |  81.90095538745
R_SPREAD  |  95.67069926615  |  93.54630251072  |  104.44404645699  |  79.38867468682
J_SPREAD  |  74.90958375193  |  72.77105061759  |  82.74028328231  |  59.00831297876
FACTOR  |  1  |  1  |  1  |  1
IS_CONTRIBUTED_CASH_FLOW  |  N  |  N  |  N  |  N
#trades  |  101.6875  |  101.718811  |  101.625  |  101.796906
View: CUSTOM
Use field().column name annotation (TRADE_DATA().I_SPREAD) to select the data points you are interested in and create your custom view
Bond  |  AMCAR 2024-1 a3 Mtge
Name  |  AMCAR 2024-1 A3
Security Type  |  ABS
Dates  |  2024-09-30 00:00:00
Use "showallcols=t" as you execute your query in Excel to retrieve the default set of associated columns
TRADE_DATA(SOURCE=TRACE, dates=2024-09-30).DATE as #dates  |  DATES  |  2024-09-30 00:00:00
TRADE_DATA(SOURCE=TRACE, dates=2024-09-30).VALUE as #price  |  #N/A Requesting Data...
TRADE_DATA(SOURCE=TRACE, dates=2024-09-30).VOLUME as #size  |  VOLUME  |  70
TRADE_DATA(SOURCE=TRACE, dates=2024-09-30).I_SPREAD as #I_spread  |  I_SPREAD  |  59.88734068357
CRNCY as #currency  |  #currency  |  USD
CPN as #coupon  |  #coupon  |  5.43
RTG_SP as #rating  |  #rating  |  AAA
MTG_BAL as #collateral_balance  |  #collateral_balance  |  848924
POOL_CPR_1_MONTH as #pool_CPR_1_month  |  #pool_CPR_1_month  |  21.07
Trade Data - Custom List
Universe
Security 1  |  FORDO 2022-A A3 Mtge
Security 2  |  GMCAR 2021-2 A4 Mtge
Inputs
Range - Start Date  |  2024-10-01 00:00:00
Range - End Date  |  2024-10-31 00:00:00
Scenario  |  PX
Workout  |  TO_WORST
View  |  MTGE_ANALYTICS
View/Get()  |  dropna(TRADE_DATA(SOURCE=TRACE, SCENARIO=PX , WORKOUT=TO_WORST, VIEW=MTGE_ANALYTICS, dates=range(2024-10-01, 2024-10-31))) as #trades
Universe/For()  |  ['FORDO 2022-A A3 Mtge','GMCAR 2021-2 A4 Mtge']
BQL Query  |  get(dropna(TRADE_DATA(SOURCE=TRACE,SCENARIO=PX,WORKOUT=TO_WORST,VIEW=MTGE_ANALYTICS,dates=range(2024-10-01,2024-10-31))) as #trades) for(['FORDO 2022-A A3 Mtge','GMCAR 2021-2 A4 Mtge'])
#N/A Requesting Data...

## Examples - Aggregations
TRACE Trades & Spreads - Aggregations
• Analyze current and historical aggregated metrics (e.g. I-Spread) for mortgage sectors based on TRACE-reported trade data
• Perform relative value analysis on custom baskets of bonds to determine trends and spot investment opportunities
• The examples below aim to show how you can define the universe that you want to analyze using BQL and aggregate in seconds trade info and derived analytics
Note:
• As default the BQL query returns the traded price, more derived data is accessible using "showallcols=t"
• When a custom date/date range is not specified, trades for the previous day are returned (current day trades are not available)
• Prepayment speed scenario defaults to pricing speed (speed at which deal was brought to market at)
• Workout for yield and spread calculations defaults to worst
Aggregations
Auto ABS - Weighted Average I Spread Over Time
Universe
Sector  |  AUTO
Rating  |  AAA
Class  |  A3
Credit Quality  |  'Prime','Super Prime'
WAL  |  0.25
Trades Data Inputs
Range - Start Date  |  2024-01-01 00:00:00
Range - End Date  |  2024-06-30 00:00:00
Trade Size  |  1000
Spread  |  300
Scenario  |  PX
Workout  |  TO_WORST
Spread Type  |  I_SPREAD
Variables/Let()  |  let(
#dates= dates=range(2024-01-01, 2024-06-30);
#volume_filter=TRADE_DATA(#dates).volume>=1000;
)
View/Get()  |  get(wavg(group(matches(TRADE_DATA(#dates), TRADE_DATA(#dates).I_SPREAD <= 300 and TRADE_DATA(#dates).volume>= 1000).I_SPREAD,
by=matches(TRADE_DATA(#dates), TRADE_DATA(#dates).I_SPREAD <=  300  and TRADE_DATA(#dates).volume>= 1000).date),
group(matches(TRADE_DATA(#dates), TRADE_DATA(#dates).I_SPREAD <=  300  and TRADE_DATA(#dates).volume>= 1000).adjusted_volume,
by=matches(TRADE_DATA(#dates), TRADE_DATA(#dates).I_SPREAD <=  300  and TRADE_DATA(#dates).volume>= 1000).date)) as #wAvg_Spread)
Universe/For()  |  for(filter(mortgagesuniv(all), STRUCTURED_PROD_ASSET_CLASS==AUTO AND (RTG_SP==AAA OR RTG_MOODY==AAA OR KBRA_RATING==AAA)
AND MTG_WAL>=0.25 AND STRUCTURED_PROD_CLASS_CRED_QUAL IN['Prime','Super Prime'] AND MTG_CMO_CLASS==A3))
Global Params/With()  |  with(source=TRACE, scenario=PX , workout=TO_WORST)
date  |  #N/A Requesting Data...
