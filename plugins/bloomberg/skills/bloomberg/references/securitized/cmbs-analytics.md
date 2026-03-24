# BQL Agency CMBS Analytics

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
Single security  |  - Eg... for(['FN MA4732 Mtge'])
List of securities  |  - Eg... for(['FN MA4732 Mtge', 'BMARK 2024-V5 A3 Mtge', 'TAOT 2024-A A3 Mtge'])
Debt Chains  |  - Eg… for(mortgages(['FN MA4732 Mtge']))
Index/Port members  |  - Eg... for(members(['LUMSTRUU Index']))
Entire mortgages universe  |  - Eg... for(mortgagesuniv('all'))
let()  |  let(
#CF_assumptions="136 PSA";
#spread=125;
#I=I;
)
get()  |  get(price(assumptions=#CF_assumptions, spread=#spread, spread_type=#I))
for()  |  for('FN MA4732 Mtge')
with()  |  with(applyusersettings=Y, market_date=REALTIME)

## YT<GO> Custom Analytics Syntax
What's New?
You can now perform custom bond calculations for Fixed Income Securitized Products using the Bloomberg Query Language (BQL) in Microsoft® Excel and BQuant. This allows you to evaluate one or more securities at once as you would in the Yield Table, YT<GO> on the Bloomberg Terminal.
The Yield Table (YT) calculator via BQL provides essential tools to price, evaluate and determine risk analysis on all Fixed Income Securitized Products.
Learn more about YT<GO> here
Using the YT<GO> calculator via BQL you can:
• Solve for Price, Yield or Spreads based upon customize Prepayment Assumptions
• View a variety of key measurements to determine a securities risk profile such as Weighted Average Life (WAL), Durations and Convexities
• Run the BAM (Bloomberg Agency Model) Prepayment Model or custom curves
• Quickly run bid lists with multiple bond line items
• Perform single security multiple scenario cash flow analysis
• Perform all functionality that is available on YT via Bloomberg's Query Language (BQL)
BQL Syntax for Custom Analytics
• In the Bloomberg Terminal, YT<GO> would allow you to use the Price / Yield / Spread / Duration calculator to evaluate fixed income securities
• YT<GO> - Price/Yields/Spreads/Risk Measures given custom inputs
• The table below shows, for each field, applicable parameters, defaults, accepted values
Fields
Field  |  Definition  |  Description  |  Input/Output
Settle_date  |  Settle date  |  The date on which payment is due to settle a trade. The date on which the analytics will be calculated. Default will be standard market settle.  |  In/Out
Market_date  |  Market date  |  The date on which the market environment for analytics will be determined. A date or the following values "CLOSE", "REALTIME".  |  In/Out
Price  |  Price  |  The price for the bond.  |  In/Out
Yield  |  Yield  |  The yield of the bond.  |  In/Out
Spread  |  Spread  |  The spread for the bond. The type of spread depends on the selected spread_type. Supported spread types are I, N, Z, J, E, A, R, P.  |  In/Out
Discount_Margin  |  Discount Margin  |  The discount margin of the bond. Applies to floaters. The discount margin, which is the margin relative to the base index rate, such that the present value of cash flow equals the price plus accrued interest.  |  In/Out
WAL  |  WAL  |  The bond's weighted average life, given the corresponding prepay and other assumptions. The weighted average number of years until the receipt of remaining principal payments.  |  Out
Principal_Window  |  Principal Window  |  The month and year of the first and last principal payments.  |  Out
Duration  |  Modified Duration  |  Percentage price change given 100 bs point shift in yields. Assuming static prepayment assumptions.  |  Out
Workout  |  Workout  |  Parameter to return analytics based on either the scenario run to maturity/call/worst.  |  In/Out
Rate_type  |  Rate type  |  Index rate projection type.  |  In/Out
Rate_shift  |  Rate shift  |  Index Rate Scenario.  |  In/Out
Cashflow_Assumptions  |  Cashflow Assumptions  |  Allows you to specify the preferred prepayment rate and type.  |  In/Out
Parameters
Parameter  |  ApplyUserSettings  |  Price  |  Yield  |  Spread  |  Spread_type  |  Discount_Margin  |  Duration_type  |  Cashflow_Assumptions  |  Rate_type  |  Rate_shifts  |  Dates  |  Market_date  |  Settle_date  |  Workout
Parameter Type  |  Mandatory  |  Mandatory  |  Mandatory  |  Mandatory  |  Mandatory  |  Mandatory  |  Mandatory  |  Optional  |  Optional  |  Optional  |  Optional  |  Optional  |  Optional  |  Optional
Definition  |  Apply User Settings Flag  |  Price  |  Yield  |  Spread  |  Spread Type  |  Discount Margin  |  Duration Type  |  Cashflow Assumptions - Prepayment speed and type  |  Forward index rate projection type  |  Index Rate Scenario.
Forward index rate shifts or custom overrides.  |  Trade Date  |  Market Date  |  Settle Date  |  Workout
Description  |  Apply user settings flag must be set to Y in order to run custom analytics.  |  The price for the bond.  |  The bond's yield.  |  The bond's spread. The type of spread that appears depends on the selected spread_type.  |  The type of spread depends on the selected spread_type.
Conventional Yield Spreads
• I: Yield spread to a linearly interpolated point on the sovereign yield curve using actual maturities.
• J: Yield spread to a linearly interpolated point on the sovereign yield curve using nominal maturities.
• A: Yield spread to a benchmark security from the sovereign yield curve that has the closest nominal maturity to the weighted average life of the mortgage bond.
• N: Yield spread to a linearly interpolated point on the swap curve, using nominal maturities.
• P: Yield spread to a linearly interpolated point on the risk-free rate-based swap curve, using actual maturities. This spread is only defined for certain currencies.
Cash Flow Spreads
• Z: The cash flow spread to the spot curve implied by the sovereign curve.
• R: Cash flow spread to the spot curve implied by the risk-free curve (e.g., SOFR, TONAR, SONIA, SARON).
• E: For market dates on or after April 15, 2023, the cash flow spread to the SOFR Futures curve (CME). For market dates before April 15, 2023, the cash flow spread to the USD Eurodollar spot curve.  |  Applies to floaters. The discount margin, which is the margin relative to the base index rate, such that the present value of cash flow equals the price plus accrued interest.  |  Duration_type is a mandatory parameter when the duration() field is used.
Modified Duration - Uses static prepayment when shifting interest rates to calculate the percentage price change.  |  Allows you to specify the preferred prepayment speed and type. If you are not overriding assumptions in the query, default assumptions (MDF<GO>) will be applied.
• Prepayment speed: Single constant rate (ie., 3 = 3 CPR), comma separated list of rates (ie., 3,4,5 ..), Bloomberg vector syntax (ie., "O 2 12R 10" or "A 5/1/2022 2 12R 10") (case insensitive). Optionally, this may be followed by a prepayment type (case insensitive), ie., "10 PSA" or "2 6R 5 SMM", with a space separating the prepayment rate and type.
• Prepay type: Any of "BAM", "BTM", "BTMC", "BCM", "CPR", "VPR", "PSA", "SMM", "CPY", "CPP", "CPJ", "CPB", "ABS" or "PPS" as applicable to the security.
Historical speed prepay types available are "H1M", "H3M", "H6M", "H1Y", "HLF".  |  Allows you to specify the forward index rate projection type.
Accepted values are "static","forward","constant" or "custom". If rate type is "custom", any index rates not provided will use Bloomberg static rates. If omitted: will use "forward".
"constant": Grab the latest value (or as-of some NY 4PM SNST) of the required index rate. Assume all future values of that rate are the same as the value we retrieved.
"static": Compute a forward rate from a spot curve for the market date, as if we were computing forward rates normally. Assume all futures values of that rate are the same as the singular forward rate we computed for the market date.
"forward": Forward index rate projection type.
"custom": Replace index with a comma separated list of numbers (ie., 3.0 for 3%) or Bloomberg vector syntax (2 12R 10). Separate multiple indices with a semicolon. Special index name "all" will shift all index rates. If rate type is custom, any index rate not replaced will use Bloomberg static rates.  |  If rate type is "static" or "forward", shift a single value for each index (ie., 100 bps). Examples when rate_type is static or forward: "all:100" (shift all rates +100 bps), "100" (shift all rates +100 bps), "MTGEFNCL:100;MTGEFNCI:100" (shift both MTGEFNCL and MTGEFNCI +100bps).
If rate type is "custom", will replace index with a comma separated list of numbers (ie., 3.0 for 3%) or Bloomberg vector syntax (2 12R 10) (case insensitive). Separate multiple indices with a semicolon. Either a special index name "all" (case insensitive) (ie., "all:100 " or a single number (ie., 100) will shift all index rates.
If rate type is custom, any index rate not replaced will use Bloomberg static rates. Example when rate_type is custom:
"TSFR3M:2,2.1,2.2,3,3.5,3.75;SOFR30A:3 36R 5" (replace 3M SOFR with 2% for the first 3 months, then 3% for the remaining periods. And replace SOFR 30A with 3% ramping to 5% over 3 years and 5% for the remaining periods. All other rates will use Bloomberg static rates).  |  The date on which the market environment for analytics will be determined.
The dates parameter represents the trade date and it uses the associated rate environment. When the trade date is set to be a past date, the settle date and market date (rate environment) are adjusted by default based on the chosen trade date.  |  The date on which the market environment for analytics will be determined.
Accepted values are:
• Close: previous day's closing market
• Realtime: latest available intraday market
• Single date: If a specific date is provided, that date will be specified. When the date is set to today's date, will use the latest available closing market.
• If omitted, close will be used as default.  |  The date on which payment is due to settle a trade, in MM/DD/YY format. The date on which the analytics will be calculated.
When settle date (settle_dt) is backdated, no adjustments are made to the trade date (and market date) so it is necessary to also backdate the trade date using the dates parameter.  |  Parameter to return analytics based on either the scenario run to maturity/call/worst
Accepted Values  |  • Y
• N  |  • I
• N
• Z
• J
• E
• A
• R
• P  |  • MODIFIED  |  Prepay assumptions: Expected format is prepayment speed followed by prepayment type.
• Single Prepay Assumption: "10 CPR", "135 PSA"
• Vector Prepay Assumption e.g. Run cash flows at 50% BAM for 12 months with a ramp up to 150% BAM for the remaining months "50 12R 150 BAM"  |  • STATIC
• FORWARD
• CONSTANT
• CUSTOM  |  Rate shifts:
• all 10: rate_shifts="all:10"
• all 10 to a single index: rate_shifts="TSFR1M:10"
• all 10 to multiple indices: rate_shifts="RFUCCT1M:10;RFUCCT1Y:10"
• custom 10 12S 7 24S 5 12S 3 to a single index: rate_shifts="RFUCCT1M:10 12S 7 24S 5 12S 3"
• custom 10 12S 7 to multiple index: rate_shifts="RFUCCT1M:10 12S 7;RFUCCT1Y:10 12S 7"  |  Single date
• Absolute (YYYY-MM-DD)
• Relative -1y, etc.  |  • REALTIME
• CLOSE
• Single date  |  Single date
• Absolute (YYYY-MM-DD)
• Relative -1y, etc.  |  • TO_WORST
• TO_MATURITY
• TO_CALL
Default Value  |  FORWARD  |  CLOSE  |  Standard settle based upon market date  |  TO_WORST
Value Type  |  Boolean  |  Number  |  Number  |  Number  |  Enum  |  Number  |  Enum  |  String  |  Enum  |  String  |  Date  |  Date  |  Date  |  Enum
Resources  |  Learn more  |  Learn more
Field  |  Description
Settle_date  |  Settle Date  |  X  |  X  |  X  |  X
Market_date  |  Market Date  |  X  |  X  |  X  |  X
Price  |  Price given Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Price  |  Price given DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Price  |  Price given Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Price  |  Price given Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Yield  |  Yield given Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Yield  |  Yield given DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Yield  |  Yield given Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Yield  |  Yield given Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Discount_Margin  |  DM given Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Discount_Margin  |  DM given Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Discount_Margin  |  DM given Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Discount_Margin  |  DM given DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Spread  |  Spread given Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Spread  |  Spread given Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Spread  |  Spread given DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Spread  |  Spread given Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
WAL  |  Weighted Average Life given Assumptions and Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
WAL  |  Weighted Average Life given Assumptions and Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
WAL  |  Weighted Average Life given Assumptions and DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
WAL  |  Weighted Average Life given Assumptions and Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Principal_Window  |  Pricipal Window given Assumptions and Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Principal_Window  |  Pricipal Window Life given Assumptions and Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Principal_Window  |  Pricipal Window Life given Assumptions and DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Principal_Window  |  Pricipal Window Life given Assumptions and Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Duration  |  Modified Duration given Assumptions and Price  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Duration  |  Modified Duration given Assumptions and Yield  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Duration  |  Modified Duration given Assumptions and DM  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Duration  |  Modified Duration given Assumptions and Spread  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X
Workout  |  Workout/Calculation to  |  X
Rate_type  |  Rate given Type  |  X
Rate_shift  |  Rate given Shift  |  X
Cashflow_Assumptions  |  Cashflow Assumptions  |  X

## Examples - PRICE
YT<GO> Custom Analytics in BQL - PRICE
BQL now allows you to calulate prices (solve for prices) on-the-fly based on user defined inputs for securitized products.
• The price() data item now supports new parameters so you can compute price given custom inputs
• You can now input one of the following valuation measures: price, yield, discount margin (only applies to floaters) as well as workout, custom prepayment assumptions, rate type and shifts to calculate custom analytics given the specified assumptions
• The dates parameter allows you to specify a single (absolute or relative) date to perform historical/'as-of' custom analysis
• Output prices and sensitivity measures (weighted average life, modified duration, principal window) given custom inputs side-by-side in one single query
• Gain transparency retrieving default inputs and additional analytics included in the bql response (metadata)
Note:
• MDF <GO> defaults are applied whenever cashflow assumptions are not specified
• Market_date default is close which is the prior rate business day rate environment whenever the dates parameter is not overridden. When market_date is set to realtime, it uses the current/live rate environment
• Rate_type when not specified defaults to forwards
• Custom analytics are calculated to worst unless a different workout is specified
• The dates parameter represents the trade date and it uses the associated rate environment. When the trade date is set to be a past date, the settle date and market date (rate environment) will be adjusted by default based on chosen trade date.
However, when settle date (settle_dt) is backdated, no adjustments are made to the trade date (and market date) so it is necessary to also backdate the trade date using the dates parameter.
Price Given Custom Spread And Spread Type
Bond  |  FN MA4732 Mtge
Name  |  FN MA4732
Security Type  |  Pool
Inputs
Spread  |  125
Spread type  |  I
View/Get()  |  PRICE(SPREAD=125,SPREAD_TYPE=I) as #PRICE
Universe/For()  |  FN MA4732 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(PRICE(SPREAD=125,SPREAD_TYPE=I) as #PRICE) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Price  |  92.29818861053
Note: BQL query is running live (real-time or prior close rate environment) and will not match the screen image above.
Price Given Custom Spread And Spread Type - Retrieve Available Metadata (Associated Columns)
Bond  |  FN MA4732 Mtge
Name  |  FN MA4732
Security Type  |  Pool
Inputs
Spread  |  125
Spread type  |  I
View/Get()  |  PRICE(SPREAD=125,SPREAD_TYPE=I) as #PRICE
Universe/For()  |  FN MA4732 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(PRICE(SPREAD=125,SPREAD_TYPE=I) as #PRICE) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Use "showallcols=t" as you execute your query in Excel to retrieve the default set of associated columns
Derived Price & Default Associated Columns  |  ID  |  #PRICE.SETTLE_DATE  |  DATES  |  #PRICE.MARKET_DATE  |  #PRICE
FN MA4732 Mtge  |  2026-04-13 00:00:00  |  2026-03-13 00:00:00  |  2026-03-12 00:00:00  |  92.29818861053
In addition to "showallcols=t", use "addcols=all" in the preferences clause as you execute your query in Excel to retrieve all available metadata/associated columns
BQL Query  |  get(PRICE(SPREAD=125,SPREAD_TYPE=I) as #PRICE) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME) preferences(addcols=all)
Derived Price & All Associated Columns  |  ID  |  FN MA4732 Mtge
#PRICE.I_SPREAD  |  125
#PRICE.SETTLE_DATE  |  2026-04-13 00:00:00
DATES  |  2026-03-13 00:00:00
#PRICE.A_SPREAD  |  131.05428611108
#PRICE.R_SPREAD  |  151.93773993816
#PRICE.J_SPREAD  |  125.32484027295
#PRICE.ASSUMPTIONS  |  142.0 PSA
#PRICE.DISCOUNT_MARGIN
#PRICE.YIELD  |  5.35113286111
#PRICE.RATE_SHIFTS
#PRICE.Z_SPREAD  |  100.75779998782
#PRICE.WORKOUT  |  TO_WORST
#PRICE.RATE_TYPE  |  FORWARD
#PRICE.N_SPREAD  |  138.82396448447
#PRICE.E_SPREAD  |  154.66472419025
#PRICE.WAL  |  7.80886294185
#PRICE.MARKET_DATE  |  2026-03-12 00:00:00
#PRICE.P_SPREAD  |  167.57193830313
#PRICE.DURATION  |  5.6824407393
#PRICE.PRINCIPAL_WINDOW  |  05/26-12/51
#PRICE  |  92.29818861053
Use "addcols=['Column header 1', 'Column Header 2'])" in the preferences clause in Excel in the BQL query to retrieve selected associated columns/metadata
BQL Query  |  get(PRICE(SPREAD=125,SPREAD_TYPE=I) as #PRICE) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME) preferences(addcols=['YIELD','DURATION','WAL'])
Derived Price & Selected Columns  |  ID  |  FN MA4732 Mtge
#PRICE.SETTLE_DATE  |  2026-04-13 00:00:00
DATES  |  2026-03-13 00:00:00
#PRICE.YIELD  |  5.35113286111
#PRICE.WAL  |  7.80886294185
#PRICE.MARKET_DATE  |  2026-03-12 00:00:00
#PRICE.DURATION  |  5.6824407393
#PRICE  |  92.29818861053

## Examples - YIELD
YT<GO> Custom Analytics in BQL - YIELD
BQL now allows you to calulate yields (solve for yields) on-the-fly based on user defined inputs for securitized products.
• The yield() data item now supports new parameters so you can compute yield given custom inputs
• You can now input one of the following valuation measures: price, yield, discount margin (only applies to floaters) as well as workout, custom prepayment assumptions, rate type and shifts to calculate custom analytics given the specified assumptions
• The dates parameter allows you to specify a single (absolute or relative) date to perform historical/'as-of' custom analysis
• Output yields and sensitivity measures (weighted average life, modified duration, principal window) given custom inputs side-by-side in one single query
• Gain transparency retrieving default inputs and additional analytics included in the bql response (metadata)
Note:
• MDF <GO> defaults are applied whenever cashflow assumptions are not specified
• Market_date default is close which is the prior rate business day rate environment whenever the dates parameter is not overridden. When market_date is set to realtime, it uses the current/live rate environment
• Rate_type when not specified defaults to forwards
• Custom analytics are calculated to worst unless a different workout is specified
• The dates parameter represents the trade date and it uses the associated rate environment. When the trade date is set to be a past date, the settle date and market date (rate environment) will be adjusted by default based on chosen trade date.
However, when settle date (settle_dt) is backdated, no adjustments are made to the trade date (and market date) so it is necessary to also backdate the trade date using the dates parameter.
Custom Yield Calcs
Yield Given Custom Price And Single Prepay Assumption
Bond  |  FN MA4732 Mtge
Name  |  FN MA4732
Security Type  |  Pool
Inputs
Price  |  95.5
Cashflow Assumptions  |  136 PSA
View/Get()  |  YIELD(PRICE=95.5, ASSUMPTIONS='136 PSA')
Universe/For()  |  FN MA4732 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(YIELD(PRICE=95.5,ASSUMPTIONS='136 PSA')) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Yield  |  4.74514744277
Note: BQL query is running live (real-time or prior close rate environment) and will not match the screen image above.
Yield Given Custom Price & Single Prepay Assumption
Bond  |  BMARK 2024-V5 A3 Mtge
Name  |  BMARK 2024-V5 A3
Security Type  |  CMBS
Inputs
Price  |  105
Cashflow Assumptions  |  0 CPY
View/Get()  |  YIELD, WAL, DURATION(DURATION_TYPE=MODIFIED) as #MOD_DUR, PRINCIPAL_WINDOW
Universe/For()  |  BMARK 2024-V5 A3 Mtge
Global Params/With()  |  PRICE=105, ASSUMPTIONS='0 CPY', applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(YIELD,WAL,DURATION(DURATION_TYPE=MODIFIED) as #MOD_DUR,PRINCIPAL_WINDOW) for(['BMARK 2024-V5 A3 Mtge']) with(PRICE=105,ASSUMPTIONS='0 CPY',applyusersettings=Y,market_date=REALTIME)
Derived Yield, Mod Dur, WAL, Principal Window  |  YIELD  |  WAL  |  #MOD_DUR  |  PRINCIPAL_WINDOW
3.87229060037  |  2.76581597834  |  2.51718206795  |  11/28-01/29
Note: BQL query is running live (real-time or prior close rate environment) and will not match the screen image above.
Yield Given Custom Price And Vector Prepay Assumptions
Bond  |  TAOT 2024-A A3 Mtge
Name  |  TAOT 2024-A A3
Security Type  |  ABS
Inputs
Spread  |  62
Spread type  |  I
Cashflow Assumptions  |  0.6, 8.1, 1.5, 1.4, 1.6, 1.8, 2.2, 2.1, 1.9, 1.7, 1.5 ABS
View/Get()  |  YIELD(SPREAD=62, SPREAD_TYPE=I, ASSUMPTIONS='0.6, 8.1, 1.5, 1.4, 1.6, 1.8, 2.2, 2.1, 1.9, 1.7, 1.5 ABS')
Universe/For()  |  TAOT 2024-A A3 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(YIELD(SPREAD=62,SPREAD_TYPE=I,ASSUMPTIONS='0.6,8.1,1.5,1.4,1.6,1.8,2.2,2.1,1.9,1.7,1.5 ABS')) for(['TAOT 2024-A A3 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Yield  |  4.24640759737
Yield Given Custom Price And Vector Prepay Assumptions
Bond  |  FN AN2017 Mtge
Name  |  FN AN2017
Security Type  |  Pool
Inputs
Price  |  95
Cashflow Assumptions  |  10 12S 7 24S 5 12S 3
View/Get()  |  YIELD(PRICE=95, ASSUMPTIONS='10 12S 7 24S 5 12S 3')
Universe/For()  |  FN AN2017 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(YIELD(PRICE=95,ASSUMPTIONS='10 12S 7 24S 5 12S 3')) for(['FN AN2017 Mtge']) with(applyusersettings=Y,market_date=REALTIME)

## Examples - SPREAD
YT<GO> Custom Analytics in BQL - SPREAD
BQL now allows you to calulate spreads on-the-fly based on user defined inputs for securitized products.
• The spread() data item now supports new parameters so you can compute the selected spread given custom inputs
• You can now input one of the following valuation measures: price, yield, discount margin (only applies to floaters) as well as workout, custom prepayment assumptions, rate type and shifts to calculate custom analytics given the specified assumptions
• The dates parameter allows you to specify a single (absolute or relative) date to perform historical/'as-of' custom analysis
• Output spreads and sensitivity measures (weighted average life, modified duration, principal window) given custom inputs side-by-side in one single query
• Gain transparency retrieving default inputs and additional analytics included in the bql response (metadata)
Note:
• MDF <GO> defaults are applied whenever cashflow assumptions are not specified
• Market_date default is close which is the prior rate business day rate environment whenever the dates parameter is not overridden. When market_date is set to realtime, it uses the current/live rate environment
• Rate_type when not specified defaults to forwards
• Custom analytics are calculated to worst unless a different workout is specified
• The dates parameter represents the trade date and it uses the associated rate environment. When the trade date is set to be a past date, the settle date and market date (rate environment) will be adjusted by default based on chosen trade date.
However, when settle date (settle_dt) is backdated, no adjustments are made to the trade date (and market date) so it is necessary to also backdate the trade date using the dates parameter.
Spread Given Custom Price & Cashflow Assumptions
Bond  |  FN MA4732 Mtge
Name  |  FN MA4732
Security Type  |  Pool
Inputs
Output Spread Type  |  I
Price  |  95.5
View/Get()  |  SPREAD(PRICE=95.5, SPREAD_TYPE='I')
Universe/For()  |  FN MA4732 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(SPREAD(PRICE=95.5,SPREAD_TYPE='I')) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Spread  |  65.93987525797
Spread Given Custom Price & Vector Prepay Assumptions
Bond  |  FN MA4732 Mtge
Name  |  FN MA4732
Security Type  |  Pool
Inputs
Output Spread Type  |  I
Price  |  95.5
Cashflow Assumptions  |  3.4 4.6 5.7 6.3 6.7 6.9 7.3 7.5 7.7 7.9 8.2 7.7 7.3 6.5 6 CPR
View/Get()  |  SPREAD(PRICE=95.5, SPREAD_TYPE='I', ASSUMPTIONS='3.4 4.6 5.7 6.3 6.7 6.9 7.3 7.5 7.7 7.9 8.2 7.7 7.3 6.5 6 CPR')
Universe/For()  |  FN MA4732 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(SPREAD(PRICE=95.5,SPREAD_TYPE='I',ASSUMPTIONS='3.4 4.6 5.7 6.3 6.7 6.9 7.3 7.5 7.7 7.9 8.2 7.7 7.3 6.5 6 CPR')) for(['FN MA4732 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Spread  |  45.55412434634
Spread Given Custom Price And Cashflow Assumptions
Bond  |  BMARK 2024-V5 A3 Mtge
Name  |  BMARK 2024-V5 A3
Security Type  |  CMBS
Inputs
Output Spread Type  |  J
Price  |  95.5
Cashflow Assumptions  |  10 CPY
View/Get()  |  SPREAD(PRICE=95.5, SPREAD_TYPE='J', ASSUMPTIONS='10 CPY')
Universe/For()  |  BMARK 2024-V5 A3 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(SPREAD(PRICE=95.5,SPREAD_TYPE='J',ASSUMPTIONS='10 CPY')) for(['BMARK 2024-V5 A3 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Spread  |  394.47398782507
Spread Given Custom Price, Cashflow Assumptions, Workout
Bond  |  TAOT 2024-A A3 Mtge
Name  |  TAOT 2024-A A3
Security Type  |  ABS
Inputs
Output Spread Type  |  I
Price  |  100.5
Cashflow Assumptions  |  1.36 ABS
Workout  |  TO_MATURITY
View/Get()  |  SPREAD(PRICE=100.5, SPREAD_TYPE='I', ASSUMPTIONS='1.36 ABS', WORKOUT=TO_MATURITY)
Universe/For()  |  TAOT 2024-A A3 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(SPREAD(PRICE=100.5,SPREAD_TYPE='I',ASSUMPTIONS='1.36 ABS',WORKOUT=TO_MATURITY)) for(['TAOT 2024-A A3 Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived Spread  |  45.05301518562

## Examples - DM
YT<GO> Custom Analytics in BQL - DISCOUNT_MARGIN
BQL now allows you to calulate discount margin on-the-fly based on user defined inputs for securitized products.
• The discount_margin() data item now supports new parameters so you can compute price given custom inputs
• You can now input one of the following valuation measures: price, yield, discount margin (only applies to floaters) as well as workout, custom prepayment assumptions, rate type and shifts to calculate custom analytics given the specified assumptions
• The dates parameter allows you to specify a single (absolute or relative) date to perform historical/'as-of' custom analysis
• Output discount margin and sensitivity measures (weighted average life, modified duration, principal window) given custom inputs side-by-side in one single query
• Gain transparency retrieving default inputs and additional analytics included in the bql response (metadata)
Note:
• MDF <GO> defaults are applied whenever cashflow assumptions are not specified
• Market_date default is close which is the prior rate business day rate environment whenever the dates parameter is not overridden. When market_date is set to realtime, it uses the current/live rate environment
• Rate_type when not specified defaults to forwards
• Custom analytics are calculated to worst unless a different workout is specified
• The dates parameter represents the trade date and it uses the associated rate environment. When the trade date is set to be a past date, the settle date and market date (rate environment) will be adjusted by default based on chosen trade date.
However, when settle date (settle_dt) is backdated, no adjustments are made to the trade date (and market date) so it is necessary to also backdate the trade date using the dates parameter.
DM Given Price And Cashflow Assumptions And Rate Type
Bond  |  FHR 5410 DF Mtge
Name  |  FHR 5410 DF
Security Type  |  CMO
Inputs
Price  |  100.25
Cashflow Assumptions  |  250 PSA
Rate Type  |  CONSTANT
View/Get()  |  DISCOUNT_MARGIN(PRICE=100.25, ASSUMPTIONS='250 PSA', RATE_TYPE=CONSTANT)
Universe/For()  |  FHR 5410 DF Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(DISCOUNT_MARGIN(PRICE=100.25,ASSUMPTIONS='250 PSA',RATE_TYPE=CONSTANT)) for(['FHR 5410 DF Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived DM  |  139.04711381323
DM Given Price, Cashflow Assumptions And Rate Type
Bond  |  FHR 5410 DF Mtge
Name  |  FHR 5410 DF
Security Type  |  CMO
Inputs
Price  |  100.25
Cashflow Assumptions  |  BAM
Rate Type  |  FORWARD
View/Get()  |  DISCOUNT_MARGIN(PRICE=100.25, ASSUMPTIONS='BAM', RATE_TYPE=FORWARD)
Universe/For()  |  FHR 5410 DF Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(DISCOUNT_MARGIN(PRICE=100.25,ASSUMPTIONS='BAM',RATE_TYPE=FORWARD)) for(['FHR 5410 DF Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived DM  |  134.94214666529
DM Given Custom Price, Single Prepay Assumptions, Rate Type and Rate Shift
Bond  |  FNR 2024-70 FA Mtge
Name  |  FNR 2024-70 FA
Security Type  |  CMO
Inputs
Price  |  98.375
Cashflow Assumptions  |  BAM
Rate Type  |  FORWARD
Rate Shifts  |  -100
View/Get()  |  DISCOUNT_MARGIN(PRICE=98.375, ASSUMPTIONS='BAM' ,RATE_TYPE='FORWARD', RATE_SHIFTS='-100')
Universe/For()  |  FNR 2024-70 FA Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME
BQL Query  |  get(DISCOUNT_MARGIN(PRICE=98.375,ASSUMPTIONS='BAM',RATE_TYPE='FORWARD',RATE_SHIFTS='-100')) for(['FNR 2024-70 FA Mtge']) with(applyusersettings=Y,market_date=REALTIME)
Derived DM  |  227.76843687303
Discount Margin Given Price And Single Prepay Assumptions
Bond  |  ARES 2024-74a A1 Mtge
Name  |  ARES 2024-74A A1
Security Type  |  LL
Inputs
Price  |  99
Cashflow Assumptions  |  20 CPR
View/Get()  |  DISCOUNT_MARGIN, DURATION(DURATION_TYPE=MODIFIED) as #MOD_DUR,WAL,PRINCIPAL_WINDOW
Universe/For()  |  ARES 2024-74a A1 Mtge
Global Params/With()  |  applyusersettings=Y, market_date=REALTIME, PRICE=99, ASSUMPTIONS='20 CPR'
BQL Query  |  get(DISCOUNT_MARGIN,DURATION(DURATION_TYPE=MODIFIED) as #MOD_DUR,WAL,PRINCIPAL_WINDOW) for(['ARES 2024-74a A1 Mtge']) with(applyusersettings=Y,market_date=REALTIME,PRICE=99,ASSUMPTIONS='20 CPR')
Derived Price, MDur, WAL, Princ Wind  |  DISCOUNT_MARGIN  |  #MOD_DUR  |  WAL  |  PRINCIPAL_WINDOW
158.2473588148  |  4.21598912069  |  4.80163457487  |  01/30-01/32
