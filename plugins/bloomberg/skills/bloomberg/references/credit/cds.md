# BQL CDS (Credit Default Swaps) Reference

## BQL Intro
False
bbg://screens/LPHP CURR:0:1 591037  |  Help!A1
Required Parameters  |  Description  |  let()  |  (Optional) lab expressions for later reuse in your query
Universe  |  The security universe including ticker(s), isin(s), cusip(s) or larger universes such CDS of equity or fixed income index members.
get()  |  DataItem(Parameters) to be retrieved
Data Item(s)  |  The data fields such as CDS_SPREAD. You can find a current list of available fields via the BQL Builder on the Bloomberg Ribbon in Excel.
for()  |  Security, wrapped in single quotes '
with()  |  (Optional) global parameters that are applied to all applicable data items.
The FOR clause in BQL() can take several inputs, e.g.
Single security  |  - Eg... for(['IBM US Equity'])
List of securities  |  - Eg... for(['VOD LN Equity','IBM US Equity'])
Debt Chains  |  - Eg… for(bonds(['CBA AU Equity']))
Index/Port members:  |  - Eg... for(members(['LEGATRUU Index']))
let()  |  let(#Spread_Chg =pct_chg(cds_spread(pricing_source=CBIL,dates=range(-1m,0d)));)
get()  |  Get(#Spread_Chg)
for()  |  for(CDS('TSLA US Equity'))
with()  |  with(fill=prev)

## CDS Single Names
CDS Single Names in BQL
What's a CDS (Credit Default Swap)?
CDS are a type of derivative, which is a contract whose value is derived from price movements of an underlying financial asset, index or instrument. In this case, the value is tied to the risk that a company or country will default on its debt. A buyer of a credit default swap receives a payout from the seller if a borrower fails to make good on its obligations.
How do CDS (Credit Default Swap) work?
Purchasers of a credit derivative, usually debt investors, make payments to a seller, who provides a payout if a borrower fails to make good on its obligations.
If the borrower skips an interest payment or otherwise fails to pay debt, the International Swaps and Derivatives Association, a trade group, determines if the swap pays out.
Analyze CDS single names using BQL
You can return credit default swap (CDS) tickers and analyze current and historical spreads from your preferred pricing source directly in the Bloomberg Query Language (BQL) in Microsoft® Excel and BQuant.
The cds() universe function helps you return the CDS ticker associated with a security, and the function's tenor parameter lets you pick the term remaining on the contract.
You can also combine cds() with the pricing_source parameter in the px_last() or cds_spread() data items to retrieve pricing info from any source available to you in ALLQ <GO>.
Note: Premium pricing sources such as CMA are available in Excel to clients with additional data subscriptions. Contact your account manager to enable premium pricing sources.
Universe  |  Description  |  Parameter  |  Example
cds()  |  cds() lets you return data about a single-name credit default swap (CDS) by specifying one of the company's debt or equity securities. By default, cds() retrieves the five-year CDS, but you can choose a different tenor.  |  tenor
- Description: Specifies the length of the CDS at the contract's inception.
- Default: 5Y
- Other Values: 1Y, 2Y, 10Y, 4Y, 7Y, 3Y, 6M  |  get(id()) for(cds('JPM US Equity', tenor=2Y))
get(id())for(cds('JPM US Equity', tenor=5Y))
get(id())for(cds('GM US Equity', tenor=3Y))
Data Item  |  Description  |  Parameter  |  Example
cds_spread()  |  cds_spread() returns data for the chosen cds name(s) and the specified pricing source and date(s). Please note that cds_spread will only return data for cds quoted in spread. Alternatively, please use px_last with the preferred pricing source to retrieve prices for cds.  |  side
- Description: quote side
- Default: mid
- Other Values: bid, ask
pricing_source
- Description: pricing source for the cds spread quotes
- Default: Default pricing source is based on CDSD<GO> > 83<GO>
- Other Values: any PCS code
spread_type
- Description: spread type
- Default: Default pricing source is based on CDSD<GO> > 83<GO>
- Other values: flat
dates
- Description: dates used for the cds spread analysis
- Default: 0d
- Other values: single date (absolute, relative), range
fill
- Description: Indicates what value to return when data is missing
- Default: NA
- Other values: prev, next
frq (per)
- Description: Used with dates. Specifies the sampling frequency for values in a historical time series.
- Default: D
- Other Values: Q, S, M, Y, W  |  get(cds_spread) for(cds('JPM US Equity', tenor=2Y))
get(cds_spread) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread) for(cds('GM US Equity', tenor=3Y))
get(cds_spread(pricing_source=CBBT)) for(cds('JPM US Equity', tenor=2Y))
get(cds_spread(pricing_source=CBIN)) for(cds('JPM US Equity', tenor=10Y))
get(cds_spread(dates=-1m)) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread(dates=range(-1m,0d))) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread(dates=range(2021-01-01,2024-01-01))) for(cds('JPM US Equity'))
get(cds_spread(fill=prev, dates=range(2021-01-01,2024-01-01))) for(cds('JPM US Equity'))
Bloomberg Pricing Sources for CDS Analysis
PCS Code  |  Source Description
Bloomberg
CDS Sources  |  CBBT  |  Composite Bloomberg Bond Trader
CBIL  |  BBG CDS Intra LN
CBIN  |  BBG CDS Intra NY
CBIT  |  BBG CDS Intra TK
CBGL  |  BBG CDS 5:15PM LN
CBGN  |  BBG CDS 5:15PM NY
CBGT  |  BBG CDS 5:15PM TK
PRXY  |  CDS Sector Curve
BEST  |  Bloomberg's Expanded Source of Ticks
DRSK  |  Bloomberg Models CDS
Note: Additional subscription might be required to retrieve CDS spreads from third parties.
For example: CMA (eg CMAN, CMAL, CMAT, CMAI) in excel.
Getting Started - Basic Examples
Retrieve the 5y CDS spread for a given issuer
Security  |  JPM US Equity
Name  |  JPMorgan Chase & Co  |  46.76121520996094
Field  |  cds_spread
Pricing Source  |  CBIN
get()  |  cds_spread(pricing_source=CBIN)
for()  |  cds('JPM US Equity')
Retrieve the spread for a given cds single name
Security  |  CJPM1U5 Curncy
Name  |  JPMCC CDS USD SR 5Y D14  |  46.76121520996094
Field  |  cds_spread
Pricing Source  |  CBIN
get()  |  cds_spread(pricing_source=CBIN)
for()  |  CJPM1U5 Curncy
Retrieve the 10y CDS spread for a given issuer
Security  |  JPM US Equity
Name  |  JPMorgan Chase & Co  |  72.49540710449219
Tenor  |  10Y
Field  |  cds_spread
Pricing Source  |  CBIN
get()  |  cds_spread(pricing_source=CBIN)
for()  |  cds('JPM US Equity', tenor=10Y)
Retrieve the 2y CDS spread for a given issuer as of one month ago
Security  |  JPM US Equity
Name  |  JPMorgan Chase & Co  |  24.21801
Tenor  |  2Y
Field  |  cds_spread
Pricing Source  |  CBIN
Date  |  -1m
get()  |  cds_spread(pricing_source=CBIN, dates=-1m, fill=prev)
for()  |  cds('JPM US Equity', tenor=2Y)
Retrieve the spread for a given 10y CDS name over the last week
Security  |  CVOD1E10 Curncy  |  dates  |  spread
Name  |  VODFON CDS EUR SR 10Y D14  |  #N/A Requesting Data...
Tenor  |  10Y
Field  |  cds_spread
Pricing Source  |  CBIN
Date  |  range(-1w,0d)

## CDS Single Names - Use Cases
Retrieve the 5y CDS given a custom list of bonds and stocks
custom list  |  #N/A Requesting Data...
Field  |  name, px_last(pricing_source=CBIN).value as #spread  |  ibm us equity
Pricing source  |  CBIN  |  vod ln equity
Date  |  today  |  EI798988 Corp
ZB310991 Corp
BJ457937 Corp
get()  |  name, px_last(pricing_source=CBIN).value as #spread  |  ZF145541 Corp
for()  |  CDS(['ibm us equity','vod ln equity','EI798988 Corp','ZB310991 Corp','BJ457937 Corp','ZF145541 Corp'])
with()  |  dates=2024-10-16
Retrieve the term structure for the CDS curve given an issuer ticker
Issuer  |  VOD LN Equity
Name  |  Vodafone Group PLC
Field  |  px_last(pricing_source=CBIN).value
Pricing source  |  CBIN
Date  |  today
ID  |  Issuer CDS Curve  |  Spread
3Y  |  cds('VOD LN Equity', tenor=3Y)  |  28.76709747314453
5Y  |  cds('VOD LN Equity', tenor=5Y)  |  51
7Y  |  cds('VOD LN Equity', tenor=7Y)  |  69.85026550292969
10Y  |  cds('VOD LN Equity', tenor=10Y)  |  94.50994110107422
Retrieve the term structure for selected CDS sovereign curves
Pricing source  |  CBIN
let()  |  #3Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=3Y),mapby=lineage).value;
#5Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=5Y),mapby=lineage).value;
#7Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=7Y),mapby=lineage).value;
#10Y=value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=10Y),mapby=lineage).value
get()  |  name,#3Y,#7Y,#5Y,#10Y
for()  |  (['6152Z LN Equity','1426Z MM Equity','50184Z SJ Equity','1153Z CB Equity','1131Z PE Equity','1323Z BZ Equity','223727Z FP Equity','3413Z GR Equity','1266Z ID Equity','45793Z CI Equity','3344634Z PP Equity'])
Countries  |  Name  |  3Y  |  5Y  |  7Y  |  10Y
6152Z LN Equity  |  #N/A Requesting Data...
1426Z MM Equity
50184Z SJ Equity
1153Z CB Equity
1131Z PE Equity
1323Z BZ Equity
223727Z FP Equity
3413Z GR Equity
1266Z ID Equity
45793Z CI Equity
3344634Z PP Equity
Note: for country ticker, please refer to CSDR<GO>
Calculate the spread between Bloomberg default risk model (DRSK) versus 5y CDS for names included in a given equity index
Index  |  SPX Index
Index Name  |  S&P 500 INDEX  |  Name  |  Implied CDS  |  CDS (5Y)  |  Spread
Sector  |  Banking  |  #N/A Requesting Data...
Pricing source  |  CBIN
let()  |  #Implied_CDS = RSK_BB_IMPLIED_CDS_SPREAD(dates=-1d,fill=prev).value;
#5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, CDS(tenor=5Y),mapby=lineage);
#Spread = #Implied_CDS-#5Y;)
get()  |  name, #Implied_CDS, #5Y, #Spread
for()  |  filter(members(['SPX Index']),Classification_Name(BICS,3)=='Banking' and #Implied_CDS*#5Y!=na)
Note: for DRSK spread details, please refer to DRSK <GO>
Identify single names CDS for issuers in the selected index
Index  |  Indu Index
Index Name  |  Dow Jones Industrial Average  |  #N/A Requesting Data...
Tenor  |  5Y
Pricing Source  |  CBGN
let()  |  #spread=cds_spread(pricing_source='CBGN').value;
get()  |  long_comp_name as #name, #spread
for()  |  CDS(members(['Indu Index']), tenor=5Y)
Note: to retrieve CDS on portfolio holdings, please change the members() query using your own portfolio ID as shown below
members('U17911388-100',type=PORT)

## CDS Indices - Membership
What's New?
Using BQL, it is now possible to access current and historical members for credit default swap (CDS) indices similar to the data available using MEMC <GO>  in the Bloomberg Terminal.
 How is this helping you?
 • Access current and historical members for one or several CDS indices
 • Further analyze index's constituents filtering and sorting the data based on custom condition(s) so that you can make comparisons that are important to you
   For example, CDS index members within a specific industry sector or only display members for a given index with a spread equal to or greater than X basis points
 • Pull key descriptive and pricing information for names included in one or a list of CDS indices. Then easily compare some of this information to the information for a specific index member to determine relative value.
 • Enrich your index analysis joining membership for CDS indices with other data datasets available for CDS single names.
 How can you see this?
 • members() decomposes an ID representing a CDS index into the IDs of its constituents so you can access membership data
   =BQL("members('ITRXEXE Curncy')","id")
 • the dates parameter used with the members() universe function lets you access historical constituents (as-of a past date). Both absolute (YYYY-MM-DD) and relative dates are supported.
   =BQL("members('ITRXEXE Curncy', dates=-6m)","id")  | =BQL("members('ITRXEXE Curncy', dates=2024-07-10)","id")
 The examples below aim to showcase how you can analyse membership for CDS Indices.
Retrieve reference data for the CDS contract and count number of CDS names included in the selected CDS Index using different tickers
Generic CDS Index Ticker  |  Specific CDS Index Series  |  Specific CDS Index Series and Version
Index  |  ITRXEXE Curncy  |  Index  |  ITRX XOVER CDSI S41 5Y Corp  |  Index  |  ITRX XOVER CDSI S4 V2 5Y Corp
Name  |  MARKIT ITRX EUR XOVER 12/30  |  Name  |  MARKIT ITRX EUR XOVER 06/29*  |  Name  |  MARKIT ITRX EUR XOVER 12/10
Currency  |  EUR  |  Currency  |  EUR  |  Currency  |  EUR
Recovery Rate  |  0.4  |  Recovery Rate  |  0.4  |  Recovery Rate  |  0.4
Tenor  |  5  |  Tenor  |  5  |  Tenor  |  5
Coupon (bps)  |  500  |  Coupon (bps)  |  500  |  Coupon (bps)  |  295
Coupon Freq  |  Q  |  Coupon Freq  |  Q  |  Coupon Freq  |  Q
Day Count  |  ACT/360  |  Day Count  |  ACT/360  |  Day Count  |  ACT/360
Maturity  |  2030-12-20 00:00:00  |  Maturity  |  2029-06-20 00:00:00  |  Maturity  |  2010-12-20 00:00:00
ISDA Definitions Year  |  2014  |  ISDA Definitions Year  |  2014  |  ISDA Definitions Year  |  2014
Field  |  count(group(id) as #count)  |  Field  |  count(group(id) as #count)  |  Field  |  count(group(id) as #count)
get()  |  count(group(id) as #count)  |  get()  |  count(group(id) as #count)  |  get()  |  count(group(id) as #count)
for()  |  members(['ITRXEXE Curncy'])  |  for()  |  members(['ITRX XOVER CDSI S41 5Y Corp'])  |  for()  |  members(['ITRX XOVER CDSI S4 V2 5Y Corp'])
Count  |  #N/A Requesting Data...  |  Count  |  #N/A Requesting Data...  |  Count  |  40
Retrieve current membership for the selected CDS Index
Index  |  ITRXEXE Curncy
Name  |  MARKIT ITRX EUR XOVER 12/30
Field  |  id
get()  |  id
for()  |  members(['ITRXEXE Curncy'])
#N/A Requesting Data...

## CDS Indices - Use Cases
What's New?
Using BQL, it is now possible to access index level data, members for credit default swap (CDS) indices in addition to data on CDS single names similar to analysis supported in CDIA<GO>, WCDS<GO>, CRDV<GO> in the Bloomberg Terminal.
How is this helping you?
• Calculate intrinsic values (bps), performance, and basis for CDS indices, so you can perform index roll and historical charting analyses for the indices you select
• Create custom market surveillance monitors that provide transparency into the credit default swap (CDS) market, so you can easily identify trends and anomalies, and assess how they may impact investment and risk strategies
• Track current and historical performance of names included in CDS indices
• Analyze the relative richness/cheapness of an issuer's bonds versus the issuer's credit default swap curve, so you can determine the most advantageous means of gaining credit exposure to the issuer
The examples below aim to showcase how you can leverage index level data and membership for CDS Indices and join this data with data available for CDS single names/bonds.
Retrieve membership, reference and market data for names in the selected CDS Index
Index  |  ITRXESE Curncy
Name  |  MARKIT ITRX EUR SNR FIN 12/30
Fields  |  name, crncy, seniority, cds_tenor, credit_rating_grade_indicator as #rating,
classification_name as #sector, cds_red_pair_code as #red_code, px_last().value as #spread, probability_of_default_cds().value as #1y_def_prob
get()  |  name, crncy, seniority, cds_tenor, credit_rating_grade_indicator as #rating,
classification_name as #sector, cds_red_pair_code as #red_code, px_last().value as #spread, probability_of_default_cds().value as #1y_def_prob
for()  |  members(['ITRXESE Curncy'])
#N/A Requesting Data...
Retrieve membership, reference and market data for names in the selected CDS Index matching specific condition(s) e.g. CDS Single names in the ITRX XOVER Index in the Energy sector
Index  |  ITRXEXE Curncy
Name  |  MARKIT ITRX EUR XOVER 12/30
Fields  |  name, crncy, seniority, cds_tenor, credit_rating_grade_indicator as #rating,
classification_name as #sector, px_last().value as #spread
Filter membership by
Sector  |  Energy
get()  |  name, crncy, seniority, cds_tenor, credit_rating_grade_indicator as #rating,
classification_name as #sector, px_last().value as #spread
for()  |  filter(members(['ITRXEXE Curncy']), classification_name==Energy)
#N/A Requesting Data...
Compare constituents for different CDS indices to identify constituents that are not shared by Index 1 and Index 2
Index 1  |  CDX IG CDSI S43 5Y Corp  |  Index 1 Name  |  MARKIT CDX.NA.IG.43 12/29
Index 2  |  CDX IG CDSI S42 5Y Corp  |  Index 2 Name  |  MARKIT CDX.NA.IG.42 06/29
Fields  |  long_comp_name as #name
get()  |  long_comp_name as #name
for()  |  setdiff(members('CDX IG CDSI S43 5Y Corp'),members('CDX IG CDSI S42 5Y Corp'))
setdiff(members('CDX IG CDSI S42 5Y Corp'),members('CDX IG CDSI S43 5Y Corp'))
Identify securities unique to each CDS index
CDX IG CDSI S43 5Y Corp  |  CDX IG CDSI S42 5Y Corp
#N/A Requesting Data...  |  #N/A Requesting Data...
Custom CDS Index Monitor - Create custom monitors for tradeable credit default swap (CDS) indices for so you can evaluate a diversified global portfolio of credit risk
Pricing source  |  CBIN
Range  |  -6m
Markit Indices - EMEA  |  Historical Data - Spread
Index ticker  |  Index name  |  spread  |  high  |  average  |  low  |  % chg
ITRXEBE Curncy  |  #N/A Requesting Data...  |  62.78630065917969  |  62.78630065917969  |  53.580343312277  |  #N/A Requesting Data...  |  23.338715176819857
ITRXEXE Curncy  |  #N/A Requesting Data...  |  296.948486328125  |  296.948486328125  |  256.8192219395916  |  240.2581  |  17.93404330881243
ITRXESE Curncy  |  MARKIT ITRX EUR SNR FIN 12/30  |  67.03242492675781  |  67.03242492675781  |  56.99360791280911  |  52.72076  |  24.25220584962933
ITRXEUE Curncy  |  MARKIT ITRX EUR SUB FIN 12/30  |  113.349853515625  |  113.349853515625  |  97.11241947650095  |  89.25703  |  23.919614183271378
Charting historical spreads for selected CDS Indices
Index 1  |  ITRXEBE Curncy  |  Index 1 Name  |  #N/A Requesting Data...
