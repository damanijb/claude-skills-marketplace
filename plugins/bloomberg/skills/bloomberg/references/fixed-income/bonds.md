# BQL Fixed Income Bond Analytics & YAS

## BQL Syntax
False
bbg://screens/LPHP CURR:0:1 591037  |  Help!A1
Required Parameters  |  Description  |  let()  |  (Optional) lab expressions for later reuse in your query
Universe  |  The security universe including ticker(s), isin(s), cusip(s) or larger universes such CDS of equity or fixed income index members.
get()  |  DataItem(Parameters) to be retrieved
Data Item(s)  |  The data fields such as SPREAD. You can find a current list of available fields via the BQL Builder on the Bloomberg Ribbon in Excel.
for()  |  Security, wrapped in single quotes '
with()  |  (Optional) global parameters that are applied to all applicable data items.
The FOR clause in BQL() can take several inputs, e.g.
Single security  |  - Eg... for(['IBM US Equity'])
List of securities  |  - Eg... for(['VOD LN Equity','IBM US Equity'])
Debt Chains  |  - Eg… for(bonds(['CBA AU Equity']))
Index/Port members:  |  - Eg... for(members(['LEGATRUU Index']))
let()  |  let(#Spread_Chg =pct_chg(spread(pricing_source=BGN, dates=range(-1m,0d)));)
showquery: displays the full BQL Query
get()  |  Get(#Spread_Chg)
BQL()  |  #N/A  |  showquery=F
BQL()  |  get(PX_LAST) for(['IBM 7 10/30/25 Corp'])  |  showquery=T  |  for()  |  for(bonds('TSLA US Equity'))
BQL.Query()  |  get(PX_LAST)for('IBM 7 10/30/25 Corp')  |  with()  |  with(fill=prev)
showids: displays your Ticker ID
BQL()  |  IBM 7 10/30/25 Corp  |  #N/A  |  showids=T
#N/A  |  showids=F
BQL.Query()  |  IBM 7 10/30/25 Corp  |  #N/A  |  showids=T
#N/A Requesting Data...  |  showids=F
showheaders: displays headers of Data Items
BQL()  |  #N/A Requesting Data...  |  showheaders=T
BQL.Query()  |  2018-06-11 00:00:00  |  3.7479  |  showheaders=F
2018-06-12 00:00:00  |  3.754109
showdates : Hide / Show Dates
BQL()  |  2018-06-11 00:00:00  |  3.7479  |  showdates=T
2018-06-12 00:00:00  |  3.754109
BQL.Query()  |  3.7479  |  showdates=F
3.754109
Transpose: changes layout between horizontal and vertical alignment
BQL()  |  2018-06-11 00:00:00  |  2018-06-12 00:00:00  |  Transpose=T
3.7479  |  3.754109
BQL.Query()  |  2018-06-11 00:00:00  |  3.7479  |  Transpose=F
2018-06-12 00:00:00  |  3.754109

## Basic Examples
BQL allows you to use multiple fields in single formula to make the data retrival more convenient. You can easily create a table with the descriptive fields of your choice with single BQL formula.
BQL standardises the many fields within Bloomberg API to make it easier to retrieve pricing and analytics data. For example, instead of YAS_ASW_SPREAD and BLP_Z_SPRD, we can use "SPREAD" with parameters to specify the type of spread.
Furthermore, you can use any pricing source available to you on your ALLQ<GO> page on the Terminal.
Requesting Descriptive Data on a Bond
How do I get the ticker of EH469710 Corp, issue date, ISIN, issue currency, coupon, and payment rank?  |  #N/A Requesting Data...
=BQL("EH469710 Corp","NAME, ISSUE_DT, ID_ISIN, CRNCY, CPN, PAYMENY_RANK","transpose=true")
Requesting Point-In-Time Credit Ratings
How do I pull a DIS 7 03/01/32 Corp's Bloomberg Composite Rating as of 2021-06-24?
=BQL("25468PBW5 Corp","BB_COMPOSITE","DATES=2021-06-24")  |  A-
Requesting time series of prices using a selected source  |  Enter your own Source and Side ↓
Source  |  CBBT
How do I pull DBR 4 3/4 07/04/40 Corp's bid price from a specific source e.g. CBBT over the last 7 days?  |  Side  |  Bid
=BQL("EH469710 Corp","PRICE","pricing_source='CBBT', side='Bid', dates=range(-7d,0d)")  |  #N/A Requesting Data...
Requesting volume data from a selected source on a specific date
How do I pull IBM 7 Corp's volume from a specific source on a particular date?  |  Enter your own Source and Date ↓
Source  |  TRAC
=BQL("DD103619 Corp","PX_VOLUME","pricing_source='TRAC', dates=2021-11-29")  |  Date  |  2021-11-29
#N/A Requesting Data...
Requesting Different Types of Spread
How do I retrieve the latest ask side ASW spread of the DBR 4 3/4 07/04/40 Corp using BGN as source?  |  Enter your own Spread Type, Source and Side↓
Spread Type  |  ASW
=BQL("EH469710 Corp","SPREAD", "spread_type='ASW', pricing_source=BGN, side='Ask'")  |  Source  |  BVAL
Side  |  Bid
12.87643841
Available Parameters: Spread_Type =  'I', 'Z', 'ASW', 'OAS', 'BMK', 'G'
Requesting Different Types of Yield
How do I pull DBR 4 3/4 07/04/40 Corp's latest ask Yield To Maturity using BGN as source?  |  Enter your own Yield Type, Source and Side↓
Yield Type  |  YTM
=BQL("EH469710 Corp","YIELD", "yield_type='YTM', pricing_source=BGN, side='Ask'")  |  Source  |  BGN
Side  |  Ask
3.218528170735746
Available Parameters: Yield_Type = 'YTM', 'YTW', Side='Bid','Ask','Mid'
Bid-offer Spread Evolution Over Time
How do I calculate bid-ask spread evolution over the last 30 days for a given bond?

## Analytics
What's New?
Expanded Fixed Income Analytics Offering Now Available in BQL.
You can now access additional fixed income analytics directly in the Bloomberg Query Language (BQL) in Microsoft® Excel and BQuant.
Perform more detailed yield analysis with additional yield types now avaialble in BQL i.e. YTM, convention, current.
Additional risk measures and cross currency spreads are now available so you can better assess the risk and relative value of fixed income securities.
Now you can perform more detailed yield analysis, the yield_type parameter associated with the yield() data item now supports additional values, so you can retrieve and analyze yield to convention, current yield, and yield to maturity for a bond or list of bonds.
The duration() data item now supports a duration type parameter that lets you select different duration measures (Spread, Modified, Macaulay, Effective).
Two new data items, risk() and dv01(), have been introduced to help you analyse the sensitivity of a change in interest rates.
The spread() data item now supports a currency parameter which lets you select a foreign currency for the cross currency spread calculation for different spread types (Z, ASW, G, Benchmark).
Using optional parameters in your query you can also specify the desired market side and pricing source.
Several other analytics like SPREAD(), etc. are already available in BQL and you can explore applicable parameters and defaults using FLDS<GO> or BQL Builder.
What's New?  |  Data Items  |  Parameters  |  Parameter Type  |  Values  |  Details  |  Examples
Additional
Yield
Measures  |  Yield  |  Yield_type  |  Optional  |  YTW
YTM
YTC
YTP
CON
CUR
AVL
SAVL
TAX_EQUIVALENT  |  Optional yield_type parameter can be used to specify the yield type in the query.
YTW (yield to worst) is the default yield type.
The list of supported enumerations for the yield_type parameter now includes:
YTW: Yield To Worst (Default)
YTM: Yield to Maturity
YTC: Yield to Call
YTP: Yield to Put
CONVENTION: Yield to Convention
CURRENT: Current Yield
AVL: Yield to Average Life
SAVL: Yield to Shortest Average Life
TAX_EQUIVALENT: Tax Equivalent Yield (Muni bonds only)  |  =BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTW)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTM)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=CONVENTION)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=CURRENT)")
=BQL("ZG524583 Corp","YIELD(YIELD_TYPE=YTC)")
Side  |  Optional  |  Bid
Mid
Ask  |  Optional side parameter to specify the market side in the query. Bid is default.  |  =BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTW, SIDE=MID)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTM, SIDE=BID)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=CONVENTION, SIDE=ASK)")
Pricing_Source  |  Optional  |  BVAL
BGN
...
Any other PCS  |  BVAL is the default pricing source, a different pricing source can be specified using the chosen PCS code.  |  =BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTW, PRICING_SOURCE=BVAL)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTM, PRICING_SOURCE=TRAC)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTM, PRICING_SOURCE=CBBT)")
Dates  |  Optional  |  0d
Single date
Range  |  Optional dates parameter to retrieve current and historical yields. 0d is default.  |  =BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTW, DATES=2024-02-29)")
=BQL("DD103619 Corp","YIELD(YIELD_TYPE=YTW, DATES=-1M)")
Additional
Duration Measures  |  Duration  |  Duration_type  |  Optional  |  Spread
Modified
Macaulay
Effective  |  Optional duration type parameter that can be used to specify the duration type in the query. Spread duration is the default type but modified, macaulay and effective and also available.  |  =BQL("DD103619 Corp","DURATION(DURATION_TYPE=SPREAD)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MODIFIED)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MACAULAY)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=EFFECTIVE)")
Side  |  Optional  |  Bid
Mid
Ask  |  Optional side parameter that can be used to specify the market side in the query. Bid is default.  |  =BQL("DD103619 Corp","DURATION(DURATION_TYPE=MODIFIED, SIDE=ASK)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MACAULAY, SIDE=MID)")
Pricing_Source  |  Optional  |  BVAL
BGN
...
Any other PCS  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query.  |  =BQL("DD103619 Corp","DURATION(DURATION_TYPE=SPREAD","PRICING_SOURCE=BVAL)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MODIFIED","PRICING_SOURCE=BGN)")
Dates  |  Optional  |  0d
Single date
Range  |  =BQL("DD103619 Corp","DURATION(DATES=RANGE(-1M,0D))")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=SPREAD, SIDE=BID, DATES=RANGE(-10D,0D))")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=EFFECTIVE, SIDE=BID, DATES=RANGE(-30D,0D))")
Cross Currency Spreads  |  Spread  |  Currency  |  Mandatory  |  USD
EUR
..
Any other currency code  |  To access cross currency spreads using BQL, specify the currency parameter in the SPREAD data item.  |  =BQL("DD103619 Corp","SPREAD(CURRENCY=EUR)")
=BQL("DD103619 Corp","SPREAD(CURRENCY=GBP)")
Spread_type  |  Optional  |  Z
ASW
BMK
G  |  Z Spread is the default spread type, different spread types can be specified using the spread_type parameter in the query.  |  =BQL("DD103619 Corp","SPREAD(SPREAD_TYPE=ASW, CURRENCY=EUR)")
=BQL("DD103619 Corp","SPREAD(SPREAD_TYPE=Z, CURRENCY=GBP)")
Pricing_Source  |  Optional  |  BVAL
BGN
...
Any other PCS  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query.  |  =BQL("DD103619 Corp","SPREAD(SPREAD_TYPE=ASW, CURRENCY=EUR, PRICING_SOURCE=BVAL)")
=BQL("DD103619 Corp","SPREAD(SPREAD_TYPE=Z, CURRENCY=GBP, PRICING_SOURCE=BGN)")
Yield  |  Optional  |  Custom yield value  |  Specify a custom yield value to calculate the chosen cross currency spread using the 'Yield' parameter.  |  =BQL("DD103619 Corp","SPREAD(CURRENCY=EUR, YIELD=5)")
=BQL("DD103619 Corp","SPREAD(SPREAD_TYPE=ASW, YIELD=6)")
Yield_Type  |  Optional  |  YTW
YTM
YTP
YTC  |  When a custom Yield value is specified in the query, the yield type can also be customised using the 'Yield_Type' parameter.  |  =BQL("DD103619 Corp","SPREAD(CURRENCY=EUR, YIELD=5, YIELD_TYPE=YTM)")
=BQL("AL580550 Corp","SPREAD(SPREAD_TYPE=ASW, YIELD=6, YIELD_TYPE=YTC)")
Price  |  Optional  |  Custom price value  |  Specify a custom price value to calculate the chosen cross currency spread using the 'Price' parameter.  |  =BQL("DD103619 Corp","SPREAD(CURRENCY=EUR, PRICE=90)")
=BQL("AL580550 Corp","SPREAD(CURRENCY=GBP, SPREAD_TYPE=ASW, PRICE=95)")
Risk  |  Risk  |  Side  |  Optional  |  Bid
Mid
Ask  |  Optional side parameter that can be used to specify the market side in the query. Bid is default.  |  =BQL("DD103619 Corp","RISK(SIDE=MID)")
=BQL("DD103619 Corp","RISK(SIDE=BID)")
Pricing_Source  |  Optional  |  BVAL
BGN
...
Any other PCS  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query.  |  =BQL("DD103619 Corp","RISK(SIDE=MID,PRICING_SOURCE=BGN)")
=BQL("DD103619 Corp","RISK(SIDE=BID,PRICING_SOURCE=BVAL)")
DV01  |  DV01  |  Side  |  Optional  |  Bid
Mid
Ask  |  Optional side parameter that can be used to specify the market side in the query. Bid is default.  |  =BQL("DD103619 Corp","DV01(SIDE=MID)")
=BQL("DD103619 Corp","DV01(SIDE=BID)")

## Risk Measures
What's New?
Expanded Set of Risk Measures Now Available in BQL
• The latest enhancement to Bloomberg Query Language (BQL) in Microsoft Excel and BQuant includes historical risk measures back to 2018, so that you can perform in-depth risk and relative value analysis on bonds.
• You can now analyze historical Modified and Macaulay durations, Risk metrics (DV01*100), Convexity and Key Rate Durations on individual bonds and portfolios.
• Access historical option-adjusted risk measures to the sovereign curve (2018) to better analyze risk of selected fixed income securities.
How Do I See It?
• The duration() data item now supports a dates parameter that lets you specify a single date or a range. It can be used in combination with the duration_type parameter. Set the duration_type parameter to Modified or Macaulay to access historical Modified and Macaulay durations.
• The risk() and convexity() data items now support a dates parameter that lets you specify a single date or a range to retrieve historical data.
• Two new fields, krd() and s_krd(), have been introduced to help you analyze key rate durations and quickly identify which tenors contribute the most interest rate risk.
- Use the krd() field and the tenor parameter to access the partial option-adjusted duration that shows the price sensitivity to an up move of the chosen tenor on the par treasury curve.
- Similarly use the s_krd() field and the tenor parameter to access the partial option-adjusted duration that shows the price sensitivity to an up move of the chosen tenor on the par swap curve.
- Available tenors are 6M, 2Y, 5Y, 10Y, 20Y, 30Y. The krd() field supports the dates parameter so that you can access historical sovereign key rate durations.
Please note that historical risk measures are only available for the GSAC (Government, Supranational, Agency, and Corporate Bonds) universe using BVAL pricing source and the bid market side back to 2018.
• A new set of option-adjusted sovereign risk measures is now available in BQL  (Option-adjusted spread, option-adjusted duration, otion-adjusted spread duration, option-adjusted convexity) with daily time series going back to 2018.
How Do I Access It?
What's New?  |  Data Items  |  Parameters  |  Parameter Type  |  Values  |  Details  |  Examples
Historical
Modified & Macaulay
Durations  |  Duration  |  Duration_type  |  Mandatory  |  Modified
Macaulay  |  Duration_type parameter that can be used to specify the duration type in the query.
Spread is the default duration type so you can use the duration_type parameter to obtain modified and macaulay durations.
History is now available for all duration types.  |  =BQL("DD103619 Corp","DURATION(DURATION_TYPE=MODIFIED, DATES=2020-08-16)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MODIFIED, DATES=RANGE(-10D,0D))")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MACAULAY, DATES=-1W)")
=BQL("DD103619 Corp","DURATION(DURATION_TYPE=MACAULAY, DATES=RANGE(-5Y,0D))")
Side  |  Optional  |  Bid  |  Optional side parameter that can be used to specify the market side in the query. Bid is default. Please leverage bid side for historical analysis.
Pricing_Source  |  Optional  |  BVAL  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query. Please leverage BVAL for historical analysis.
Dates  |  Optional  |  0d
Single date
Range  |  Historical Macaulay and Modified Durations for GSAC are available for:
• BVAL
• Bid Side
• Back to 2018
Fill  |  Optional  |  NA
Prev
Next  |  Fill NA values with the previous or next available value. Fill is not applied as default.
Historical
Risk  |  Risk  |  Side  |  Optional  |  Bid  |  Optional side parameter that can be used to specify the market side in the query. Bid is default. Please leverage bid side for historical analysis.  |  =BQL("DD103619 Corp","RISK(DATES=2020-08-16)")
=BQL("DD103619 Corp","RISK(DATES=RANGE(-10D,0D))")
=BQL("DD103619 Corp","RISK(DATES=-1W)")
=BQL("DD103619 Corp","RISK(DATES=RANGE(-5Y,0D))")
Pricing_Source  |  Optional  |  BVAL  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query. Please leverage BVAL for historical analysis.
Dates  |  Optional  |  0d
Single date
Range  |  Historical Risk for GSAC is available for:
• BVAL
• Bid Side
• Back to 2018
Fill  |  Optional  |  NA
Prev
Next  |  Fill NA values with the previous or next available value. Fill is not applied as default.
Historical
Convexity  |  Convexity  |  Side  |  Optional  |  Bid
Mid
Ask  |  Optional side parameter that can be used to specify the market side in the query. Bid is default. Please leverage bid side for historical analysis.  |  =BQL("DD103619 Corp","CONVEXITY(DATES=2020-08-16)")
=BQL("DD103619 Corp","CONVEXITY(DATES=RANGE(-10D,0D))")
=BQL("DD103619 Corp","CONVEXITY(DATES=-1W)")
=BQL("DD103619 Corp","CONVEXITY(DATES=RANGE(-5Y,0D))")
Pricing_Source  |  Optional  |  BVAL  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query. Please leverage BVAL for historical analysis.
Dates  |  Optional  |  0d
Single date
Range  |  Historical Convexity for GSAC is available for:
• BVAL
• Bid Side
• Back to 2018
Fill  |  Optional  |  NA
Prev
Next  |  Fill NA values with the previous or next available value. Fill is not applied as default.
Treasury KRDs
&
Swap KRDs  |  KRD  |  Tenor  |  Mandatory  |  6M
1Y
2Y
3Y
5Y
7Y
10Y
20Y
30Y  |  Available tenors for KRDs (to Treasury) - Note that tenor is a mandatory parameter.  |  =BQL("DD103619 Corp","KRD(DATES=2020-08-16)")
=BQL("DD103619 Corp","KRD(DATES=RANGE(-10D,0D))")
=BQL("DD103619 Corp","KRD(DATES=-1W)")
=BQL("DD103619 Corp","KRD(DATES=RANGE(-5Y,0D))")
Pricing_Source  |  Optional  |  BVAL  |  BVAL is the default pricing source, different pricing sources can be specified using the pricing source parameter in the query. Please leverage BVAL for historical analysis.
Dates  |  Optional  |  0d
Single date
Range  |  Historical KRDs to treasury are available for:
• BVAL
• Bid Side
• Limited history
• GSAC
Fill  |  Optional  |  NA
Prev
Next  |  Fill NA values with the previous or next available value. Fill is not applied as default.
S_KRD  |  Tenor  |  Mandatory  |  6M
1Y
2Y
3Y
5Y
7Y
10Y
20Y
30Y  |  Available tenors for KRDs - Note that tenor is a mandatory parameter.  |  =BQL("DD103619 Corp","S_KRD(DATES=2020-08-16)")
=BQL("DD103619 Corp","S_KRD(DATES=RANGE(-10D,0D))")
=BQL("DD103619 Corp","S_KRD(DATES=-1W)")
=BQL("DD103619 Corp","S_KRD(DATES=RANGE(-5Y,0D))")

## Screening
Retrieving a Query on the Bonds/Loans Universe
Bond/Loan Universes:
Universe  |  Behaviour  |  Parameters  |  Example
Bondsuniv()  |  Queries the Bloomberg bonds universe as found on SRCH <GO>  |  Type, ConsolidateDuplicates, IncludePreliminarySecurities, IncludePrivateSecurities, IncludeNonBloombergVerifiedBonds  |  Bondsuniv('Active')
Loansuniv()  |  Queries the Bloomberg bonds universe as found on LSRC <GO>  |  Type, IncludePreliminarySecurities, IncludePrivateSecurities, IncludeNonBloombergVerifiedBonds, IncludeStrips  |  Loansuniv('Matured',IncludeStrips=True)
Debtuniv()  |  Queries the Bloomberg bonds and loans universe  |  Type, ConsolidateDuplicates, IncludePreliminarySecurities, IncludePrivateSecurities, IncludeNonBloombergVerifiedBonds  |  Debtuniv('All')
Members()  |  Queries the constituents of an index.  |  Dates  |  Click here for a full tutorial on FI Indices  |  Members('BACR0 Index')
Holdings()  |  Queries the constituents of a fund. Click here for a full funds tutorial.  |  Dates  |  Click here for a full tutorial on Fund Holdings  |  Holdings('HYG US Equity',dates=-1y)
Screenresults()  |  Queries the results of a saved fixed income search on SRCH <GO>  |  Screen_Name  |  screenresults(type=srch, screen_name='@KUNGFUBOND')
Possible Types are Active, Matured or All
All other parameters are True/False (eg: IncludePrivateSecurities=False)
For more fixed income universes in BQL, visit BQLX <GO>
The following examples use Filter() to use BQL to screen our results
More on Filter() can be found here
How many investment grade Sr Non Preferred or Sr Preferred bonds are currently outstanding?
get()  |  get(count(group(ID)))  |  #N/A Requesting Data...
for()  |  for(filter(bondsuniv(Active), RTG_SP>'BBB-' AND IN(PAYMENT_RANK,['Sr Preferred','Sr Non Preferred'])))
How many outstanding bonds with contry of risk equal to Spain, Germany, France?
get()  |  get(count(Group(id)))  |  #N/A Requesting Data...
for()  |  for(filter(bondsuniv(active),IN(cntry_of_risk,['ES','DE','FR'])))
Calculate the total amount outstanding for EUR bonds with a Bloomberg Composite between AAA and A- in USD Millions
get()  |  get(sum(Group(amt_outstanding(currency=USD)))/1M)  |  #N/A Requesting Data...
for()  |  for(filter(bondsuniv(active),in(BB_composite,['AAA','AA+','AA','AA-','A+','A','A-'])))
Identify Apple bonds with maturity between 5 and 10 years
get()  |  get(ID)  |  #N/A Requesting Data...
for()  |  for(filter(bonds('AAPL US Equity'),BETWEEN(MATURITY,5Y,10Y)))
Analyse the total amount issued YTD (in EUR) for EUR and GBP denominated bonds by Payment Rank and Currency
get()  |  get(sum(Group(amt_issued(currency=EUR)/1M,[CRNCY,PAYMENT_RANK])) as #amt_out)  |  #N/A Requesting Data...
for()  |  for(filter(bondsuniv(active),in(CRNCY,['EUR','GBP']) AND ISSUE_DT>2023-01-01))
Identify outstanding USD bonds in the Health Care or Utilities sector

## YAS Custom Analytics Syntax
What's New?
Now you can perform additional custom bond calculations using the Bloomberg Query Language (BQL) in BQL <GO>, Microsoft® Excel and BQuant.
This allows you to better evaluate floating rate instruments and securities with optionality features, as you would in YAS <GO> on the Bloomberg Terminal®.
The YAS<GO> Calculator via BQL offers enhanced functionality for fixed income analysis.
In addition to standard valuation and risk tools, you can calculate discount margins based on custom inputs and perform a wide range of bond analytics, such as by calculating price, yield, and spreads across different workout scenarios.
This supports interactive and assumption-driven analysis of individual securities or portfolios, providing deeper insight into valuation, relative value, and scenario-based performance.
Using the YAS<GO> Calculator via BQL, you can now:
• Calculate discount margin for a security using custom inputs.
• Customize price, yield and spread calculations by selecting the preferred workout option (Worst, Maturity, Next Call/Put, Custom) alongside other custom inputs. Workout defines the redemption date for the security given the selected inputs and redemption schedule.
YAS<GO> Custom Analytics in BQL
You can now perform custom bond calculations using BQL formulas within Microsoft Excel, so you can analyze one or more securities at once in a spreadsheet as you would on YAS<GO> in the Bloomberg Terminal.
Access the Price / Yield / Spread / Risk calculator (YAS) using BQL to perform custom analytics calculations and to assess if a security meets your investment criteria.
Price a bond or recalculate the various yields, spreads and risk measures based on custom inputs (price, yield, or spread value).
Learn more about YAS<GO> here
It is now possible to compute:
• Price Given Yield
The price of a bond, based on a custom yield (e.g. 5), yield type (e.g. YTM) and a trade date (e.g. October 10th, 2023)
• Yield Given Price
The yield (e.g. YTW) of a bond, based on custom price (e.g. 102) and a trade date (e.g. October 10th, 2023)
• Risk Measures Given Price or Yield
The desired risk measure of a bond (Modified Duration, Macaulay Duration, Risk, DV01) based on custom yield and yield type (e.g. 5, YTW) or price (e.g. 101) and a trade date (e.g. October 10th, 2023) to help you analyse interest rate sensitivity
• Custom Spreads
The Spread (BMK, G, I, OAS, Z, ASW) of a bond based on custom yield and yield type (e.g. 5, YTW) or custom price (e.g. 101), trade date (e.g. October 10th, 2023) and customize the curves used in the calculation
Additionally, calculate custom cross currency spreads defining the foreign currency for the cross currency spread calculation, the spread type (Z, ASW, G, Benchmark) based on custom yield or price values
BQL Syntax for Custom Analytics
In the Bloomberg Terminal, YAS<GO> would allow you to use the Price / Yield / Spread / Risk calculator to evaluate fixed income securities.
YAS<GO> - Price/Yields/Spreads/Risk Measures  |  YAS XCCY<GO> - Cross Currency Spreads
Field  |  Calculation  |  Parameters  |  Accepted Values  |  Example BQL Queries  |  Notes
PRICE  |  Price Given Yield  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(PRICE(YIELD=5,DATES=2023-09-01)) for('DD103619 Corp')
get(PRICE(YIELD=5,DATES=-5d)) for('DD103619 Corp')  |  • Dates corresponds to the trade date (default is 0d)
YIELD  |  Number  |  get(PRICE(YIELD=5)) for('DD103619 Corp')  |  • Default yield type is YTW
YIELD_TYPE  |  YTW, YTM, YTC, YTP  |  get(PRICE(YIELD=7, YIELD_TYPE=YTW)) for('AL580550 Corp')
WORKOUT_PRICE  |  Number  |  get(PRICE(WORKOUT_PRICE=103, WORKOUT_DATE=2024-01-01, YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Use the workout_date and workout_price parameters to calculate yield to custom
WORKOUT_DATE  |  Single Date (YYYY-MM-DD)
WORKOUT  |  TO_WORST, TO_MATURITY, TO_NEXT_CALL, TO_NEXT_PUT, TO_CUSTOM  |  get(PRICE(WORKOUT=TO_CUSTOM, WORKOUT_PRICE=103, WORKOUT_DATE=2024-01-01, YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Set the optional workout parameter to TO_CUSTOM and calculate yield to custom
Price Given Spread  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(PRICE(SPREAD=250, DATES=2023-09-20)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
SPREAD  |  Number  |  get(PRICE(SPREAD=200)) for('DD103619 Corp')  |  • Default spread type is Z
WORKOUT  |  TO_WORST, TO_MATURITY, TO_NEXT_CALL, TO_NEXT_PUT, TO_CUSTOM  |  get(PRICE(SPREAD=200, WORKOUT=TO_MATURITY)) for('DD103619 Corp')  |  • WORKOUT can be used to set the calculation workout scenario
SPREAD_TYPE  |  Z, BMK, OAS, G, I, ASW  |  get(PRICE(SPREAD=60,SPREAD_TYPE='OAS', DATES=2023-09-01)) for('DD103619 Corp')
get(PRICE(SPREAD=70,SPREAD_TYPE='Z')) for('DD103619 Corp')
get(PRICE(SPREAD=50,SPREAD_TYPE='I')) for('DD103619 Corp')
get(PRICE(SPREAD=55,SPREAD_TYPE='G')) for('DD103619 Corp')
get(PRICE(SPREAD=65,SPREAD_TYPE='ASW')) for('DD103619 Corp')
get(PRICE(SPREAD=50,SPREAD_TYPE='BMK')) for('DD103619 Corp')  |  • Default spread type is Z
• Spread to benchmark does not yet support the dates parameter
CURVE_ID  |  Curve Number - See CRVF<GO> (S490, I25)  |  get(PRICE(SPREAD=250,SPREAD_TYPE='I',DATES=2023-09-01,CURVE_ID='S42')) for('DD103619 Corp')  |  •  The curve ID for the swap or sovereign curve can be found in CRVF<GO>
•  The expected format is usually a letter followed by the curve number e.g. S45 or I25
FORWARD_CURVE_ID  |  Curve Number - See CRVF<GO> (S490)  |  get(PRICE(SPREAD=250,SPREAD_TYPE=ASW, FORWARD_CURVE_ID='S42', DISCOUNT_CURVE_ID='S42', dates=2023-09-20)) for('DD103619 Corp')  |  •  The curve ID for the swap or sovereign curve can be found in CRVF<GO>
•  The expected format is usually a letter followed by the curve number e.g. S45 or I25
•  Forward and discount curve overrides are only applicable to ASW
DISCOUNT_CURVE_ID
YIELD  |  Yield Given Price  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(YIELD(PRICE=90, dates=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date (default is 0d)
PRICE  |  Number  |  get(YIELD(PRICE=95)) for('DD103619 Corp')  |  • Default yield type is YTW
WORKOUT  |  TO_WORST, TO_MATURITY, TO_NEXT_CALL, TO_NEXT_PUT, TO_CUSTOM  |  get(YIELD(PRICE=95, WORKOUT=TO_MATURITY)) for('DD103619 Corp')  |  • WORKOUT can be used to set the calculation workout scenario
Yield Given Spread  |  DATES  |  Single Date (YYYY-MM-DD)  |  get(YIELD(SPREAD=60, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
SPREAD  |  Number  |  get(YIELD(SPREAD=60)) for('DD103619 Corp')  |  • Default spread type is Z
SPREAD_TYPE  |  Z, BMK, OAS, G, I, ASW  |  get(YIELD(SPREAD=60,SPREAD_TYPE='OAS', DATES=2023-09-01)) for('DD103619 Corp')
get(YIELD(SPREAD=70,SPREAD_TYPE='Z', DATES=2023-09-01)) for('DD103619 Corp')
get(YIELD(SPREAD=50,SPREAD_TYPE='I', DATES=2023-09-01)) for('DD103619 Corp')
get(YIELD(SPREAD=55,SPREAD_TYPE='G', DATES=2023-09-01)) for('DD103619 Corp')
get(YIELD(SPREAD=65,SPREAD_TYPE='ASW', DATES=2023-09-01)) for('DD103619 Corp')
get(YIELD(SPREAD=50,SPREAD_TYPE='BMK')) for('DD103619 Corp')  |  • Default spread type is Z
• Spread to benchmark does not yet support the dates parameter
WORKOUT  |  TO_WORST, TO_MATURITY, TO_NEXT_CALL, TO_NEXT_PUT, TO_CUSTOM  |  get(YIELD(SPREAD=200,  WORKOUT=TO_MATURITY)) for('DD103619 Corp')  |  • WORKOUT can be used to set the calculation workout scenario
CURVE_ID  |  Curve Number - See CRVF<GO> (S490, I25)  |  get(YIELD(SPREAD=250,SPREAD_TYPE='I',DATES=2023-09-01,CURVE_ID='S490')) for('DD103619 Corp')  |  •  The curve ID for the swap or sovereign curve can be found in CRVF<GO>
•  The expected format is usually a letter followed by the curve number e.g. S45 or I25
FORWARD_CURVE_ID  |  Curve Number - See CRVF<GO> (S490)  |  get(YIELD(SPREAD=250,SPREAD_TYPE=ASW, FORWARD_CURVE_ID='S42', DISCOUNT_CURVE_ID='S42', dates=2023-09-20)) for('DD103619 Corp')  |  •  The curve ID for the swap or sovereign curve can be found in CRVF<GO>
•  The expected format is usually a letter followed by the curve number e.g. S45 or I25
•  Forward and discount curve overrides are only applicable to ASW
DISCOUNT_CURVE_ID
DURATION  |  Duration Given Price  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(DURATION(DURATION_TYPE=MODIFIED,PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
DURATION_TYPE  |  MODIFIED, MACAULAY  |  get(DURATION(DURATION_TYPE=MODIFIED,PRICE=90)) for('DD103619 Corp')  |  • Duration types available are modified and macaulay duration
PRICE  |  Number  |  get(DURATION(DURATION_TYPE=MACAULAY,PRICE=90)) for('DD103619 Corp')  |  • Duration type must be specified and set to either modified or macaulay
Duration Given Yield  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(DURATION(DURATION_TYPE=MODIFIED,YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
YIELD  |  Number  |  get(DURATION(DURATION_TYPE=MACAULAY,YIELD=6)) for('DD103619 Corp')  |  • Default yield type is YTW
DURATION_TYPE  |  MODIFIED, MACAULAY  |  get(DURATION(DURATION_TYPE=MODIFIED,YIELD=6)) for('DD103619 Corp')
YIELD_TYPE  |  YTW, YTM, YTC, YTP  |  get(DURATION(DURATION_TYPE=MACAULAY,YIELD=6, YIELD_TYPE=YTM)) for('DD103619 Corp')
RISK  |  Risk Given Price  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(RISK(PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
PRICE  |  Number  |  get(RISK(PRICE=90)) for('DD103619 Corp')
Risk Given Yield  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(RISK(YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
YIELD  |  Number  |  get(RISK(YIELD=5)) for('DD103619 Corp')  |  • Default yield type is YTW
YIELD_TYPE  |  YTW, YTM, YTC, YTP  |  get(RISK(YIELD=5,YIELD_TYPE=YTW, DATES=2023-09-01)) for('DD103619 Corp')
DV01  |  DV01 Given Price  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(DV01(PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
PRICE  |  Number  |  get(DV01(PRICE=90)) for('DD103619 Corp')
DV01 Given Yield  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(DV01(YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
YIELD  |  Number  |  get(DV01(YIELD=5)) for('DD103619 Corp')  |  • Default yield type is YTW
YIELD_TYPE  |  YTW, YTM, YTC, YTP  |  get(DV01(YIELD=5,YIELD_TYPE=YTW, DATES=2023-09-01)) for('DD103619 Corp')
CONVEXITY  |  Convexity Given Price  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(CONVEXITY(PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
PRICE  |  Number  |  get(CONVEXITY(PRICE=90)) for('DD103619 Corp')
Convexity Given Yield  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(DV01(YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
YIELD  |  Number  |  get(DV01(YIELD=5)) for('DD103619 Corp')  |  • Default yield type is YTW
YIELD_TYPE  |  YTW, YTM, YTC, YTP  |  get(DV01(YIELD=5,YIELD_TYPE=YTW, DATES=2023-09-01)) for('DD103619 Corp')
SPREAD  |  Spread Given Price  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(SPREAD(PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')  |  • Dates corresponds to the trade date and curve date (default is 0d)
• Default spread type is Z
PRICE  |  Number  |  get(SPREAD(SPREAD_TYPE=OAS,PRICE=90)) for('DD103619 Corp')
WORKOUT  |  TO_WORST, TO_MATURITY, TO_NEXT_CALL, TO_NEXT_PUT, TO_CUSTOM  |  get(SPREAD(SPREAD_TYPE=OAS,PRICE=90,WORKOUT=TO_MATURITY)) for('DD103619 Corp')  |  • WORKOUT can be used to set the calculation workout scenario
SPREAD  |  Z, BMK, OAS, G, I, ASW  |  get(SPREAD(SPREAD_TYPE=OAS,PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')
get(SPREAD(SPREAD_TYPE=Z, PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')
get(SPREAD(SPREAD_TYPE=I, PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')
get(SPREAD(SPREAD_TYPE=G, PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')
get(SPREAD(SPREAD_TYPE=ASW, PRICE=90, DATES=2023-09-01)) for('DD103619 Corp')
get(SPREAD(SPREAD_TYPE=BMK, PRICE=90)) for('DD103619 Corp')  |  • Default spread type is Z
• Spread to benchmark does not yet support the dates parameter
CURVE_ID  |  Curve Number - See CRVF<GO> (S490, I25)  |  get(SPREAD(PRICE=90, SPREAD_TYPE='I',DATES=2023-09-01,CURVE_ID='S490')) for('DD103619 Corp')  |  •  The curve ID for the swap or sovereign curve can be found in CRVF<GO>
•  The expected format is usually a letter followed by the curve number e.g. S45 or I25
FORWARD_CURVE_ID  |  Curve Number - See CRVF<GO> (S490)  |  get(SPREAD(PRICE=90,SPREAD_TYPE=ASW, FORWARD_CURVE_ID='S42', DISCOUNT_CURVE_ID='S42', dates=2023-09-20)) for('DD103619 Corp')  |  •  The curve ID for the swap or sovereign curve can be found in CRVF<GO>
•  The expected format is usually a letter followed by the curve number e.g. S45 or I25
•  Forward and discount curve overrides are only applicable to ASW
DISCOUNT_CURVE_ID
Spread Given Yield  |  DATES  |  Single Date (YYYY-MM-DD), 0d  |  get(SPREAD(SPREAD_TYPE='OAS',YIELD=5, DATES=2023-09-01)) for('DD103619 Corp')  |  • Default yield type is YTW
• Dates corresponds to the trade date and curve date (default is 0d)
• Default spread type is Z
YIELD  |  Number  |  get(SPREAD(SPREAD_TYPE='OAS',YIELD=6)) for('DD103619 Corp')

## Examples - Price Yield
YAS Custom Analytics in BQL - Price and Yield Analytics
BQL now allows you to compute custom analytics on-the-fly based on user defined inputs:
• The PRICE() data item now supports new parameters that allow you to compute price given the specified yield value and type. Additionally, it is possible to calculate price given a custom spread value and type.
• The YIELD() data item now supports new parameters that allow you to compute yield given the specified price. Additionally, it is possible to calculate yield given a custom spread value and type.
1. Price Given Yield
How to match the YAS<GO> screen to calculate price for given yield and date
Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Yield  |  5
Date  |  2023-09-11 00:00:00
View/Get()  |  PRICE(YIELD=5,DATES=2023-09-11)
Universe/For()  |  US25468PBW59
BQL Query  |  get(PRICE(YIELD=5,DATES=2023-09-11)) for([US25468PBW59])
Derived Price  |  #N/A
Retrieve Price with custom Z/I/G/OAS/ASW/BMK Spread and date
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose Spread Type  |  OAS  |  
Enter Spread  |  250
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  PRICE(SPREAD=250, SPREAD_TYPE='OAS', DATES=2023-09-01) as #price
Universe/For()  |  US25468PBW59
BQL Query  |  get(PRICE(SPREAD=250,SPREAD_TYPE='OAS',DATES=2023-09-01) as #price) for([US25468PBW59])
#N/A Requesting Data...
Retrieve price with custom I/G Spread with selected curve and date
Enter Bond  |  US25468PBW59  |  CRVF <GO>  |  ICVS <GO>
Name  |  DIS 7 03/01/32
Choose Spread Type  |  I  |  
Enter Spread  |  150
Enter Swap Curve ID  |  S42
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  PRICE(SPREAD=150, SPREAD_TYPE='I', CURVE_ID=S42, DATES=2023-09-01) as #price
Universe/For()  |  US25468PBW59
BQL Query  |  get(PRICE(SPREAD=150,SPREAD_TYPE='I',CURVE_ID=S42,DATES=2023-09-01) as #price) for([US25468PBW59])
ID  |  #price
US25468PBW59  |  #N/A
Retrieve price with custom ASW Spread with selected forward, discount curve and date
Enter Bond  |  US25468PBW59  |  ICVS <GO>
Name  |  DIS 7 03/01/32
Choose Spread Type  |  ASW
Enter Spread  |  120
Enter Forward Curve  |  S42
Enter Discount Curve  |  S42
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  PRICE(SPREAD=120, SPREAD_TYPE='ASW', FORWARD_CURVE_ID=S42, DISCOUNT_CURVE_ID=S42, DATES=2023-09-01) as #price
Universe/For()  |  US25468PBW59
BQL Query  |  get(PRICE(SPREAD=120,SPREAD_TYPE='ASW',FORWARD_CURVE_ID=S42,DISCOUNT_CURVE_ID=S42,DATES=2023-09-01) as #price) for([US25468PBW59])
#N/A Requesting Data...
2. Yield Given Price

## Examples - Spread
YAS Custom Analytics in BQL - Spread Analytics
BQL now allows you to compute custom analytics on-the-fly based on user defined inputs:
• SPREAD() now supports new parameters that allow you to compute current and historical spread given a specified price or yield value and yield type
• SPREAD() also supports a CURVE_ID to customize the curve used in the I or G Spread calculation
• SPREAD() also supports new optional parameters FORWARD_CURVE_ID and DISOUNT_CURVE_ID to choose the curves used to calculate the ASW spreads
1. Spread Given Price
Retrieve Z/I/G/OAS/ASW/BMK Spreads with custom price and date as seen on YAS <GO> screen
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose Spread Type  |  OAS  |  
Enter Price  |  103
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  SPREAD(SPREAD_TYPE='OAS', PRICE=103, DATES=2023-09-01) as #spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(SPREAD_TYPE='OAS',PRICE=103,DATES=2023-09-01) as #spread) for([US25468PBW59])
#N/A Requesting Data...
Retrieve I/G Spread with selected curve, custom price and date
Enter Bond  |  US25468PBW59  |  CRVF <GO>  |  ICVS <GO>
Name  |  DIS 7 03/01/32
Choose Spread Type  |  I  |  
Enter Swap Curve ID  |  S42
Enter Price  |  103
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  SPREAD(SPREAD_TYPE='I', CURVE_ID=S42, PRICE=103, DATES=2023-09-01) as #spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(SPREAD_TYPE='I',CURVE_ID=S42,PRICE=103,DATES=2023-09-01) as #spread) for([US25468PBW59])
ID  |  #spread
US25468PBW59  |  267.6937944109925
Retrieve ASW Spread with selected forward, discount curve, custom price and date
Enter Bond  |  US25468PBW59  |  ICVS <GO>
Name  |  DIS 7 03/01/32
Choose Spread Type  |  ASW
Enter Forward Curve  |  S42
Enter Discount Curve  |  S42
Enter Price  |  103
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  SPREAD(SPREAD_TYPE='ASW', FORWARD_CURVE_ID=S42, DISCOUNT_CURVE_ID=S42, PRICE=103, DATES=2023-09-01) as #spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(SPREAD_TYPE='ASW',FORWARD_CURVE_ID=S42,DISCOUNT_CURVE_ID=S42,PRICE=103,DATES=2023-09-01) as #spread) for([US25468PBW59])
ID  |  #spread
US25468PBW59  |  266.22262358458505
2. Spread Given Yield
Retrieve Z/I/G/OAS/ASW/BMK Spread with custom yield to maturity / worst / call / put and date
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose Spread Type  |  OAS  |  
Enter Yield  |  6
Choose Yield Type  |  YTM  |  
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  SPREAD(SPREAD_TYPE='OAS', YIELD=6, YIELD_TYPE=YTM, DATES=2023-09-01) as #spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(SPREAD_TYPE='OAS',YIELD=6,YIELD_TYPE=YTM,DATES=2023-09-01) as #spread) for([US25468PBW59])

## Examples - XCCY Spread
YAS Custom Analytics in BQL - Cross Currency Spreads: Z, ASW, Government, Benchmark
BQL now allows you to compute custom analytics on-the-fly based on user defined inputs:
• The SPREAD() data item now supports a currency parameter which lets you select a foreign currency for the cross currency spread calculation for different spread types (Z, ASW, G, Benchmark)
• Historical cross currency spread calculations are not yet supported
• Curve overrides for cross currency spread calculations is not yet supported
1. Cross Currency Spreads
Retrieve the current EUR Cross Currency Z Spread
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Bond Currency  |  USD
Enter XCCY Currency  |  EUR
**The screenshot was taken for demonstration purposes only
View/Get()  |  SPREAD(CURRENCY=EUR) as #XCCY_spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(CURRENCY=EUR) as #XCCY_spread) for([US25468PBW59])
ID  |  #XCCY_spread
US25468PBW59  |  77.33941449432868
Retrieve the CAD Cross Currency Spread to Benchmark
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Bond Currency  |  USD
Enter XCCY Currency  |  CAD
**The screenshot was taken for demonstration purposes only
View/Get()  |  SPREAD(CURRENCY=CAD, SPREAD_TYPE='BMK') as #XCCY_BMK_spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(CURRENCY=CAD,SPREAD_TYPE='BMK') as #XCCY_BMK_spread) for([US25468PBW59])
#N/A Requesting Data...
Retrieve the current CAD Cross Currency Spread to Government
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Bond Currency  |  USD
Enter XCCY Currency  |  CAD
View/Get()  |  SPREAD(CURRENCY=CAD, SPREAD_TYPE='G') as #XCCY_G_spread
Universe/For()  |  US25468PBW59
BQL Query  |  get(SPREAD(CURRENCY=CAD,SPREAD_TYPE='G') as #XCCY_G_spread) for([US25468PBW59])
#N/A Requesting Data...
2. Cross Currency Spreads Given Price
Calculate the EUR Cross Currency Asset Swap Spread for IBM 4 06/20/42 given a price of 105
Enter Bond  |  US459200HF10
Name  |  IBM 4 06/20/42
Bond Currency  |  USD
Enter Price  |  105
Enter XCCY Currency  |  EUR
View/Get()  |  SPREAD(CURRENCY=EUR, SPREAD_TYPE='ASW', PRICE=105) as #XCCY_ASW_spread
Universe/For()  |  US459200HF10
BQL Query  |  get(SPREAD(CURRENCY=EUR,SPREAD_TYPE='ASW',PRICE=105) as #XCCY_ASW_spread) for([US459200HF10])
#N/A Requesting Data...
3. Cross Currency Spreads Given Yield
Calculate the GBP Cross Currency Z Spread for IBM 4 06/20/42 given a yield to worst

## Examples - Risk Measures
YAS Custom Analytics in BQL - Risk Measure Analytics
BQL now allows you to compute custom analytics on-the-fly based on user defined inputs:
• DURATION() now supports new parameters that allow you to compute current and historical duration given a specified price or yield value and yield type
• RISK() now supports new parameters that allow you to compute current and historical risk calculations given a specified price or yield value and yield type
• DV01() now supports new parameters that allow you to compute current and historical risk calculations given a specified price or yield value and yield type
• CONVEXITY() now supports new parameters that allow you to compute current and historical convexity given a specified price or yield value and yield type
1. Duration Given Price or Yield
Retrieve Modified / Macaulay's Duration with custom price and date
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose Duration Type  |  MODIFIED  |  
Enter Price  |  110
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  DURATION(DURATION_TYPE=MODIFIED, PRICE=110, DATES=2023-09-01) as #duration
Universe/For()  |  US25468PBW59
BQL Query  |  get(DURATION(DURATION_TYPE=MODIFIED,PRICE=110,DATES=2023-09-01) as #duration) for([US25468PBW59])
ID  |  #duration
US25468PBW59  |  6.460256701474758
Retrieve Modified / Macaulay's Duration with custom yield to maturity (YTM) and date
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose Duration Type  |  MACAULAY  |  
Enter Yield  |  4
Enter Yield Type  |  YTM
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  DURATION(DURATION_TYPE=MACAULAY, YIELD=4, DATES=2023-09-01) as #duration
Universe/For()  |  US25468PBW59
BQL Query  |  get(DURATION(DURATION_TYPE=MACAULAY,YIELD=4,DATES=2023-09-01) as #duration) for([US25468PBW59])
ID  |  #duration
US25468PBW59  |  6.740770507394431
2. DV01 / Risk Given Yield or Price
Retrieve DV01 / RISK with custom price and date
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose FIELD  |  DV01  |  
Enter Price  |  110
Enter Date  |  2023-09-06 00:00:00
View/Get()  |  DV01(PRICE=110, DATES=2023-09-06) as #dv01
Universe/For()  |  US25468PBW59
BQL Query  |  get(DV01(PRICE=110,DATES=2023-09-06) as #dv01) for([US25468PBW59])
ID  |  #dv01
US25468PBW59  |  710.9207233917658
Retrieve DV01 / RISK with custom yield and date
Enter Bond  |  US25468PBW59
Name  |  DIS 7 03/01/32
Choose FIELD  |  RISK  |  
Enter Yield  |  4
Enter Yield Type  |  YTM  |  
Enter Date  |  2023-09-01 00:00:00
View/Get()  |  RISK(YIELD=4, YIELD_TYPE=YTM, DATES=2023-09-01) as #risk
Universe/For()  |  US25468PBW59
BQL Query  |  get(RISK(YIELD=4,YIELD_TYPE=YTM,DATES=2023-09-01) as #risk) for([US25468PBW59])
ID  |  #risk

## Use Cases
How does the Price change, if the Yield to Worst increases by 50 bps?
Bond  |  US459200AN17  |  < Enter Bond
Name  |  IBM 7 10/30/45
Latest Yield  |  6.29265109
Shift YTW by (bps):  |  50  |  < Enter Yield shift in bps
Derived Yield  |  6.79265109
Derived Price  |  102.21866547353883
View/Get()  |  PRICE(YIELD=6.79265109, YIELD_TYPE='YTW')
Universe/For()  |  US459200AN17
BQL Query  |  get(PRICE(YIELD=6.79265109,YIELD_TYPE='YTW')) for([US459200AN17])
How does the Yield to Worst and Yield to Call change, if the Price increases by 10%?
Bond  |  US345370CS72  |  < Enter Bond
Name  |  F 5.291 12/08/46
Latest Price  |  79.98304
Shift Price by (%)  |  10  |  < Enter Price Shift in %
Derived Price  |  89.98304
Derived Yield  |  #YTW  |  #YTC
6.151581  |  6.163054
View/Get()  |  YIELD(PRICE=89.98304, YIELD_TYPE='YTW') as #YTW,
YIELD(PRICE=89.98304, YIELD_TYPE='YTC') as #YTC
Universe/For()  |  US345370CS72
BQL Query  |  get(YIELD(PRICE=89.98304,YIELD_TYPE='YTW') as #YTW,YIELD(PRICE=89.98304,YIELD_TYPE='YTC') as #YTC) for([US345370CS72])
Calculate Yield and Benchmark Spread based on Custom Price
Bond  |  US25468PBW59  |  < Enter Bond  |  Benchmark  |  #N/A  |  #N/A  |  < Benchmark Bond with closest Tenor from the curve will be selected
Currency  |  USD  |  Benchmark Yield  |  #N/A
Tenor  |  5.968514715947981  |  Benchmark Tenor  |  #N/A
#N/A Requesting Data...  |  #Abs Dist to Bond
Custom Price  |  101  |  < Enter Custom Price
Derived Yield  |  6.792611
BMK Spread (bps)  |  #N/A
View/Get()  |  YIELD(PRICE=101)
Universe/For()  |  US25468PBW59
BQL Query  |  get(YIELD(PRICE=101)) for([US25468PBW59])
Benchmark Curve vs Derived Yield and BMK Spread
#N/A
#N/A
How does the G Spread change, customising the curve used for the calculation?
Bond  |  FR001400IVT8  |  < Enter Bond
Name  |  CADES 3 11/25/31
Last Price  |  99.26399993896484
Curve ID 1  |  I13  |  Euro Benchmarks Curve
G Spread Curve 1  |  #N/A Requesting Data...
Curve ID 2  |  I14  |  EUR France Sovereign Curve
G Spread Curve 2  |  #N/A Requesting Data...
BQL Query  |  get(SPREAD(SPREAD_TYPE=G,CURVE_ID=I13,PRICE=99.2639999389648),SPREAD(SPREAD_TYPE=G,CURVE_ID=I14,PRICE=99.2639999389648)) for([FR001400IVT8])
Weighted average Cross Currency Asset Swap Spread for BBB- rated Energy bonds with less than 30 years to maturity
Custom Filters
BCLASS 3 Sector  |  Energy
BB Composite  |  BBB-
XCCY Currency  |  USD  |  < Customize Fields
Min Tenor  |  0Y
Max Tenor  |  30Y
View/Get()  |  WAVG(GROUP(SPREAD(SPREAD_TYPE=ASW, CURRENCY=USD),bins(maturity_years,[3,5,10,20],['a. 0-3','b. 03-05','c. 05-10','d. 10-20','e. 20+'])),
GROUP(AMT_OUTSTANDING(CURRENCY=USD),bins(maturity_years,[3,5,10,20],['a. 0-3','b. 03-05','c. 05-10','d. 10-20','e. 20+']))) as #WAVG_XCCY_ASW  |  #N/A Requesting Data...
