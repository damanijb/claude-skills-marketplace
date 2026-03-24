# BQL Fixed Income Structured Products (FISP)

## BQL Syntax
False
bbg://screens/LPHP CURR:0:1 591037  |  Help!A1
Required Parameters  |  Description  |  let()  |  (Optional) lab expressions for later reuse in your query
Universe  |  The security universe including ticker(s), isin(s), cusip(s) or larger universes such as index members or the equity universe.
get()  |  DataItem(Parameters) to be retrieved
Data Item(s)  |  The data fields such as TOTAL_RETURN. You can find a current list of available fields via the BQL Builder on the Bloomberg Ribbon in Excel.
for()  |  Security, wrapped in single quotes '
with()  |  (Optional) global parameters that are applied to all applicable data items.
The FOR clause in BQL() can take several inputs, e.g.
Single security  |  - Eg... for(['IBM US Equity'])
List of securities  |  - Eg... for(['VOD LN Equity','IBM US Equity'])
Debt Chains  |  - Eg… for(bonds(['CBA AU Equity']))
Index/Port members:  |  - Eg... for(members(['LEGATRUU Index']))
let()  |  let(#Px_Chg =pct_chg(px_last(dates=range(-3m,0d)));)
get()  |  Get(#Px_Chg)
for()  |  for(peers('NAB AU Equity'))
with()  |  with(fill=prev)

## NEW - Analytics
What's New?
Expanded Analytics Offering Now Available in BQL
You can now access additional historical analytics for securitized products directly in the Bloomberg Query Language (BQL) in BQL<GO>, Microsoft® Excel and BQuant.
An expanded set of current and historical analytics giving you access to yields and risk measures are now available.
Additional risk measures are now available so you can better assess the risk and relative value of those securities.
Using optional parameters in your BQL query, you can also specify the dates (single or range), desired market side, and pricing source for your analysis.
• Now you can perform more detailed spread analysis, the spread_type parameter associated with the spread() data item now supports additional values, so you can retrieve and analyze:
I, Z, OAS, Zero Volatility OAS, N, E, J, A, P, R-Spread for a list of structured products.
• The duration() data item supports a duration_type parameter that lets you select different duration measures (Spread, Modified, Macaulay, Effective).
• Convexity is also available to help you analyse the sensitivity of a change in yield using the convexity() data item.
• Yield is available to help you analyse different yields using the yield() data item and the yield_type parameter that lets you select different yield measures (Convention, Worst, Call, Maturity).
Using optional parameters in your query you can also specify the desired market side and pricing source.
Please note that historical data is only available for BVAL. Historical depth varies depending on the securitized product sector.
Several other fields to analyze securitized products are already available in BQL and you can explore applicable parameters and defaults using FLDS<GO> or BQL Builder.
What's New?
Note: Default behaviours in bold
Field  |  Parameters  |  Definitions  |  Examples
YIELD  |  YIELD_TYPE
• Yield to Convention - YIELD(YIELD_TYPE='CONVENTION')
• Yield to Worst - YIELD(YIELD_TYPE='YTW')
• Yield to Maturity - YIELD(YIELD_TYPE='YTM')
• Yield to Next Call - YIELD(YIELD_TYPE='YTC')
SIDE
• BID - YIELD(SIDE='BID')
• MID - YIELD(SIDE='MID')
• ASK - YIELD(SIDE='ASK')
PRICING_SOURCE
• BVAL -  YIELD(PRICING_SOURCE='BVAL')
• Specify PCS code to use an alternative dealer - YIELD(PRICING_SOURCE='BGN')
DATES
• Single - DATES=YYYY-MM-DD
• Range - DATES=RANGE(Start Date, End Date)
FILL
• NA - Fill with NAs
• Prev - Fill NAs with previous available value
• Next - Fill NAs with next available value  |  get(yield(yield_type='CONVENTION'))for('3137H8QV6')
get(yield(yield_type='YTW'))for('3137H8QV6')
get(yield(yield_type='YTM'))for('3137H8QV6')
get(yield(yield_type='YTC'))for('3137H8QV6')
get(yield(yield_type='EFFECTIVE', side='BID'))for('3137H8QV6')
get(yield(yield_type='EFFECTIVE', side='MID'))for('3137H8QV6')
get(yield(yield_type='EFFECTIVE', side='ASK'))for('3137H8QV6')
get(yield(yield_type='EFFECTIVE', side='BID', PRICING_SOURCE='BVAL'))for('3137H8QV6')
get(yield(yield_type='EFFECTIVE', side='BID', PRICING_SOURCE='BGN'))for('3137H8QV6')
get(yield(yield_type='Z', dates=2024-05-10))for('3137H8QV6')
get(yield(yield_type='I', dates=range(-3m,0d)))for('3137H8QV6')
get(yield(yield_type='I', dates=-1m, fill=prev))for('3137H8QV6')
get(yield(yield_type='I', dates=range(-3m,0d), fill=prev))for('3137H8QV6')
• Convention -  The market convention yield that corresponds to the bid price. Typically, the convention is yield to worst, meaning the lowest yield resulting from all possible redemption scenarios on callable securities or the highest yield resulting from all possible redemption scenarios on puttable securities.
• Worst - The yield of a bond calculated to worst
• Maturity - The yield of a bond calculated to maturity
• Next Call -  The yield of a bond to the next possible call date
SPREAD  |  SPREAD_TYPE
• Z-Spread - SPREAD(SPREAD_TYPE='Z')
• I-Spread - SPREAD(SPREAD_TYPE='I')
• OAS - SPREAD(SPREAD_TYPE='OAS')
• N-Spread - SPREAD(SPREAD_TYPE='N')
• E-Spread - SPREAD(SPREAD_TYPE='E')
• J-Spread - SPREAD(SPREAD_TYPE='J')
• A-Spread - SPREAD(SPREAD_TYPE='A')
• P-Spread - SPREAD(SPREAD_TYPE='P')
• R-Spread - SPREAD(SPREAD_TYPE='R')
• ZV OAS - SPREAD(SPREAD_TYPE='ZV_OAS')
SIDE
• BID - SPREAD(SIDE='BID')
• MID - SPREAD(SIDE='MID')
• ASK - SPREAD(SIDE='ASK')
PRICING_SOURCE
• BVAL -  SPREAD(PRICING_SOURCE='BVAL')
• Specify PCS code for the chosen dealer -  SPREAD(PRICING_SOURCE='BGN')
DATES
• Single - DATES=YYYY-MM-DD
• Range - DATES=RANGE(Start Date, End Date)
FILL
• NA - Fill with NAs
• Prev - Fill NAs with previous available value
• Next - Fill NAs with next available value  |  get(spread(spread_type='Z'))for('3137H8QV6')
get(spread(spread_type='I'))for('3137H8QV6')
get(spread(spread_type='OAS'))for('3137H8QV6')
get(spread(spread_type='N'))for('3137H8QV6')
get(spread(spread_type='E'))for('3137H8QV6')
get(spread(spread_type='J'))for('3137H8QV6')
get(spread(spread_type='A'))for('3137H8QV6')
get(spread(spread_type='P'))for('3137H8QV6')
get(spread(spread_type='R'))for('3137H8QV6')
get(spread(spread_type='ZV_OAS'))for('3137H8QV6')
get(spread(spread_type='I', side='BID'))for('3137H8QV6')
get(spread(spread_type='I', side='MID'))for('3137H8QV6')
get(spread(spread_type='I', side='ASK'))for('3137H8QV6')
get(spread(spread_type='I', side='BID', PRICING_SOURCE='BVAL'))for('3137H8QV6')
get(spread(spread_type='I', side='BID', PRICING_SOURCE='BGN'))for('3137H8QV6')
get(spread(spread_type='Z', dates=2024-05-10))for('3137H8QV6')
get(spread(spread_type='I', dates=range(-3m,0d)))for('3137H8QV6')
get(spread(spread_type='I', dates=-1m, fill=PREV))for('3137H8QV6')
get(spread(spread_type='I', dates=range(-3m,0d), fill=PREV))for('3137H8QV6')
• Z-Spread - Cash flow spread to the spot curve implied by the sovereign curve.
• I-Spread - Conventional yield spread to a linearly interpolated point on the sovereign yield curve.
• OAS - Option adjusted spread. Continuously compounded spread added to the discount curve along each Monte Carlo simulated interest rate path that equates dirty price (price + accrued) and the average present value of cash flows across all paths.
• N-Spread - The conventional yield spread to a linearly interpolated point on the swap curve, using nominal maturities.
• E-Spread - For market dates on or after April 15, 2023, the cash flow spread to the SOFR Futures curve (CME). For market dates before April 15, 2023, the cash flow spread to the USD Eurodollar spot curve.
• J-Spread - Conventional yield spread to a linearly interpolated point on the sovereign yield curve using nominal maturities.
• A-Spread - Conventional yield spread to a benchmark security from the sovereign yield curve that has the closest nominal maturity to the WAL of the mortgage bond.
• P-Spread - Conventional yield spread to a linearly interpolated point on the risk-free rate-based swap curve, using actual maturities.
• R-Spread - Cash flow spread to the spot curve implied by the risk-free rate curve (e.g., SOFR, TONAR, SONIA, SARON).
• Zero Volatility OAS -  Bps the spot curve would have to shift for the present value of the cashflows to equal the security's price, using a 0% volatility assumption.
DURATION  |  DURATION_TYPE
• Spread Duration - DURATION(DURATION_TYPE='SPREAD')
• Effective Duration - DURATION(DURATION_TYPE='EFFECTIVE')
• Modified Duration - DURATION(DURATION_TYPE='MODIFIED')
• Modified Duration - DURATION(DURATION_TYPE='MACAULAY')
SIDE
• BID - DURATION(SIDE='BID')
• MID - DURATION(SIDE='MID')
• ASK - DURATION(SIDE='ASK')
PRICING_SOURCE
• BVAL -  DURATION(PRICING_SOURCE='BVAL')
• Specify PCS code to use an alternative dealer -  DURATION(PRICING_SOURCE='BGN')
DATES
• Single - DATES=YYYY-MM-DD
• Range - DATES=RANGE(Start Date, End Date)
FILL
• NA - Fill with NAs
• Prev - Fill NAs with previous available value
• Next - Fill NAs with next available value  |  get(duration(duration_type='SPREAD'))for('3137H8QV6')
get(duration(duration_type='EFFECTIVE'))for('3137H8QV6')
get(duration(duration_type='MODIFIED'))for('3137H8QV6')
get(duration(duration_type='MACAULAY'))for('3137H8QV6')
get(duration(duration_type='EFFECTIVE', side='BID'))for('3137H8QV6')
get(duration(duration_type='EFFECTIVE', side='MID'))for('3137H8QV6')
get(duration(duration_type='EFFECTIVE', side='ASK'))for('3137H8QV6')
get(duration(duration_type='EFFECTIVE', side='BID', PRICING_SOURCE='BVAL'))for('3137H8QV6')
get(duration(duration_type='EFFECTIVE', side='BID', PRICING_SOURCE='BGN'))for('3137H8QV6')
get(spread(spread_type='Z', dates=2024-05-10))for('3137H8QV6')
get(spread(spread_type='I', dates=range(-3m,0d)))for('3137H8QV6')
get(spread(spread_type='I', dates=-1m, fill=prev))for('3137H8QV6')
get(spread(spread_type='I', dates=range(-3m,0d), fill=prev))for('3137H8QV6')
• Spread -  Measure of price sensitivity calculated by shifting OAS +/- 100 BP and holding the treasury curve constant using the bid/mid/ask price.
• Effective - Measures the security's price/yield sensitivity calculated by shifting the entire yield curve. Based on bid/mid/ask prices.
• Modified - Uses static prepayment when shifting interest to calculate the duration.
• Macaulay - Uses static prepayment when shifting interest to calculate the duration.
CONVEXITY  |  SIDE
• BID -  CONVEXITY(SIDE='BID')
• MID - CONVEXITY(SIDE='MID')
• ASK - CONVEXITY(SIDE='ASK')
PRICING_SOURCE
• BVAL -  CONVEXITY(PRICING_SOURCE='BVAL')
• Specify PCS code to use an alternative dealer -  CONVEXITY(PRICING_SOURCE='BGN')
DATES
• Single - DATES=YYYY-MM-DD
• Range - DATES=RANGE(Start Date, End Date)
FILL
• NA - Fill with NAs
• Prev - Fill NAs with previous available value
• Next - Fill NAs with next available value  |  get(convexity)for('3137H8QV6')
get(convexity(side=BID))for('3137H8QV6')
get(convexity(side=MID))for('3137H8QV6')
get(convexity(side=ASK))for('3137H8QV6')
get(convexity(pricing_source='BVAL'))for('3137H8QV6')
get(convexity(pricing_source='BGN'))for('3137H8QV6')
get(convexity(dates=-3m))for('3137H8QV6')
get(convexity(dates=2024-05-10))for('3137H8QV6')
get(convexity(dates=range(-3m,0d),fill=prev))for('3137H8QV6')
get(convexity(dates=range(2024-04-10,2024-05-10),fill=prev))for('3137H8QV6')
get(convexity(dates=range(2024-04-10,2024-05-10),fill=next))for('3137H8QV6')
• Bid OAS Convexity - Spread Rate of change in OAS duration as the bid yield changes.
• Mid OAS Convexity - Spread Rate of change in OAS duration as the mid yield changes.
• Ask OAS Convexity - Spread Rate of change in OAS duration as the ask yield changes.

## Expanded FISP Offering
What's New?
New fields have been added to BQL in order to significantly expand capabilities to analyze securitized products and enable users to conduct in-depth analysis across the following domains:
- Cash Flow Analysis
- Historical Bond Analysis
- Current/Historical Collateral Analysis
Expanded Offering by Analytical Domain
ID  |  Mnemonic  |  Analytical Domain  |  Description
AN152  |  EXTENDED_CASH_FLOW  |  Cashflow Analysis  |  Extended Cashflows
AN022  |  MTG_CASH_FLOW  |  Cashflow Analysis  |  Projected CashFlows
AN055  |  HIST_CASH_FLOW  |  Cashflow Analysis  |  Historical Cashflows
AN174  |  PROJ_PREPAYMENT_SPEEDS_IN_CPR  |  Cashflow Analysis  |  Projected Prepayment Speeds in CPR
DT131  |  CDR_VECTOR_PROJ_BY_CREDIT_MOD  |  Cashflow Analysis  |  CDR Vector Projected by Credit Model
Example: Retrieve historical cashflows for FHR 5000 DA Mtge. Data returned includes metadata showing the coupon, period number, date, interest, principal paid, and principal balance.
Security  |  FHR 5000 DA Mtge
ID  |  Coupon  |  Period  |  Date  |  Interest  |  Principal Balance  |  Cashflow
FHR 5000 DA Mtge  |  1.25  |  1  |  2025-09-25 00:00:00  |  43144.64  |  40841837.14  |  577013.77
FHR 5000 DA Mtge  |  1.25  |  2  |  2025-08-25 00:00:00  |  43643.74  |  41418850.9  |  479137.3
FHR 5000 DA Mtge  |  1.25  |  3  |  2025-07-25 00:00:00  |  44047.26  |  41897988.2  |  387378.05
FHR 5000 DA Mtge  |  1.25  |  4  |  2025-06-25 00:00:00  |  44821.72  |  42285366.25  |  743485.35
FHR 5000 DA Mtge  |  1.25  |  5  |  2025-05-25 00:00:00  |  45433.38  |  43028851.59  |  587189.25
FHR 5000 DA Mtge  |  1.25  |  6  |  2025-04-25 00:00:00  |  45871.51  |  43616040.85  |  420606.38
FHR 5000 DA Mtge  |  1.25  |  7  |  2025-03-25 00:00:00  |  46247.53  |  44036647.23  |  360979.41
FHR 5000 DA Mtge  |  1.25  |  8  |  2025-02-25 00:00:00  |  46709.12  |  44397626.64  |  443130.58
FHR 5000 DA Mtge  |  1.25  |  9  |  2025-01-25 00:00:00  |  47221.24  |  44840757.22  |  491632.08
FHR 5000 DA Mtge  |  1.25  |  10  |  2024-12-25 00:00:00  |  47672.72  |  45332389.3  |  433423.12
FHR 5000 DA Mtge  |  1.25  |  11  |  2024-11-25 00:00:00  |  48359.35  |  45765812.42  |  659163.94
FHR 5000 DA Mtge  |  1.25  |  12  |  2024-10-25 00:00:00  |  48802.32  |  46424976.36  |  425250.93
FHR 5000 DA Mtge  |  1.25  |  13  |  2024-09-25 00:00:00  |  49274.67  |  46850227.29  |  453454.13
FHR 5000 DA Mtge  |  1.25  |  14  |  2024-08-25 00:00:00  |  49898.72  |  47303681.42  |  599093.78
FHR 5000 DA Mtge  |  1.25  |  15  |  2024-07-25 00:00:00  |  50430.28  |  47902775.2  |  510290.79
FHR 5000 DA Mtge  |  1.25  |  16  |  2024-06-25 00:00:00  |  50964.24  |  48413065.99  |  512604.12
FHR 5000 DA Mtge  |  1.25  |  17  |  2024-05-25 00:00:00  |  51443.44  |  48925670.11  |  460032.42
FHR 5000 DA Mtge  |  1.25  |  18  |  2024-04-25 00:00:00  |  51962.69  |  49385702.53  |  498478.67
FHR 5000 DA Mtge  |  1.25  |  19  |  2024-03-25 00:00:00  |  52643.94  |  49884181.2  |  654004.65
FHR 5000 DA Mtge  |  1.25  |  20  |  2024-02-25 00:00:00  |  53205.38  |  50538185.85  |  538977.91
FHR 5000 DA Mtge  |  1.25  |  21  |  2024-01-25 00:00:00  |  53796.01  |  51077163.76  |  567009.19
FHR 5000 DA Mtge  |  1.25  |  22  |  2023-12-25 00:00:00  |  54257.1  |  51644172.96  |  442645.65
FHR 5000 DA Mtge  |  1.25  |  23  |  2023-11-25 00:00:00  |  54825.01  |  52086818.61  |  545194.5
FHR 5000 DA Mtge  |  1.25  |  24  |  2023-10-25 00:00:00  |  55637.23  |  52632013.11  |  779731.55
FHR 5000 DA Mtge  |  1.25  |  25  |  2023-09-25 00:00:00  |  56175.82  |  53411744.66  |  517045.96
FHR 5000 DA Mtge  |  1.25  |  26  |  2023-08-25 00:00:00  |  56942.66  |  53928790.62  |  736165.75
FHR 5000 DA Mtge  |  1.25  |  27  |  2023-07-25 00:00:00  |  57721.58  |  54664956.37  |  747760.24
FHR 5000 DA Mtge  |  1.25  |  28  |  2023-06-25 00:00:00  |  58647.07  |  55412716.61  |  888468.16
FHR 5000 DA Mtge  |  1.25  |  29  |  2023-05-25 00:00:00  |  59210.66  |  56301184.77  |  541048.78
FHR 5000 DA Mtge  |  1.25  |  30  |  2023-04-25 00:00:00  |  59825.45  |  56842233.56  |  590195.2
FHR 5000 DA Mtge  |  1.25  |  31  |  2023-03-25 00:00:00  |  60534.32  |  57432428.75  |  680518.55
FHR 5000 DA Mtge  |  1.25  |  32  |  2023-02-25 00:00:00  |  61308.44  |  58112947.31  |  743154.44
FHR 5000 DA Mtge  |  1.25  |  33  |  2023-01-25 00:00:00  |  61963.25  |  58856101.75  |  628619.59
FHR 5000 DA Mtge  |  1.25  |  34  |  2022-12-25 00:00:00  |  62752.8  |  59484721.34  |  757962.56
FHR 5000 DA Mtge  |  1.25  |  35  |  2022-11-25 00:00:00  |  63270.07  |  60242683.9  |  496584.68
FHR 5000 DA Mtge  |  1.25  |  36  |  2022-10-25 00:00:00  |  64000.47  |  60739268.58  |  701183.54
FHR 5000 DA Mtge  |  1.25  |  37  |  2022-09-25 00:00:00  |  64887.33  |  61440452.12  |  851386.26
FHR 5000 DA Mtge  |  1.25  |  38  |  2022-08-25 00:00:00  |  65955.42  |  62291838.38  |  1025365.24
FHR 5000 DA Mtge  |  1.25  |  39  |  2022-07-25 00:00:00  |  67115.2  |  63317203.62  |  1113391.16
FHR 5000 DA Mtge  |  1.25  |  40  |  2022-06-25 00:00:00  |  68237.31  |  64430594.79  |  1077223.47
FHR 5000 DA Mtge  |  1.25  |  41  |  2022-05-25 00:00:00  |  69635.04  |  65507818.26  |  1341816.96
FHR 5000 DA Mtge  |  1.25  |  42  |  2022-04-25 00:00:00  |  70611.04  |  66849635.21  |  936963.7
FHR 5000 DA Mtge  |  1.25  |  43  |  2022-03-25 00:00:00  |  71430.94  |  67786598.92  |  787098.84
FHR 5000 DA Mtge  |  1.25  |  44  |  2022-02-25 00:00:00  |  72731.74  |  68573697.76  |  1248775.83
FHR 5000 DA Mtge  |  1.25  |  45  |  2022-01-25 00:00:00  |  74199.43  |  69822473.59  |  1408977.17
FHR 5000 DA Mtge  |  1.25  |  46  |  2021-12-25 00:00:00  |  75723.07  |  71231450.76  |  1462692.61
FHR 5000 DA Mtge  |  1.25  |  47  |  2021-11-25 00:00:00  |  77652.98  |  72694143.37  |  1852719.86
FHR 5000 DA Mtge  |  1.25  |  48  |  2021-10-25 00:00:00  |  79472.29  |  74546863.24  |  1746535.07
FHR 5000 DA Mtge  |  1.25  |  49  |  2021-09-25 00:00:00  |  80844.14  |  76293398.31  |  1316976.45
FHR 5000 DA Mtge  |  1.25  |  50  |  2021-08-25 00:00:00  |  82387.82  |  77610374.75  |  1481935.61
FHR 5000 DA Mtge  |  1.25  |  51  |  2021-07-25 00:00:00  |  83995.6  |  79092310.37  |  1543467.51
FHR 5000 DA Mtge  |  1.25  |  52  |  2021-06-25 00:00:00  |  86181.07  |  80635777.87  |  2098047.5
FHR 5000 DA Mtge  |  1.25  |  53  |  2021-05-25 00:00:00  |  87738.31  |  82733825.38  |  1494949.11
FHR 5000 DA Mtge  |  1.25  |  54  |  2021-04-25 00:00:00  |  89871.62  |  84228774.49  |  2047981.91
FHR 5000 DA Mtge  |  1.25  |  55  |  2021-03-25 00:00:00  |  91181.32  |  86276756.4  |  1257313.7
FHR 5000 DA Mtge  |  1.25  |  56  |  2021-02-25 00:00:00  |  93180.37  |  87534070.1  |  1919084.12
FHR 5000 DA Mtge  |  1.25  |  57  |  2021-01-25 00:00:00  |  94832.35  |  89453154.22  |  1585905.45
FHR 5000 DA Mtge  |  1.25  |  58  |  2020-12-25 00:00:00  |  96490.15  |  91039059.68  |  1591485.08
FHR 5000 DA Mtge  |  1.25  |  59  |  2020-11-25 00:00:00  |  97843.71  |  92630544.75  |  1299420.75
FHR 5000 DA Mtge  |  1.25  |  60  |  2020-10-25 00:00:00  |  99731.55  |  93929965.5  |  1812318.01
FHR 5000 DA Mtge  |  1.25  |  61  |  2020-09-25 00:00:00  |  2178-07-10 14:24:00  |  95742283.51  |  1919088.09
FHR 5000 DA Mtge  |  1.25  |  62  |  2020-08-25 00:00:00  |  2183-05-25 10:04:48  |  97661371.6  |  1708628.4
ID  |  Mnemonic  |  Analytical Domain  |  Description
FP025  |  MTG_HIST_FACT  |  Hist Bond Analysis  |  Mtge Historical Factors
DS647  |  MTG_HIST_CPN  |  Hist Bond Analysis  |  Mtge Historical Coupons
DY127  |  HISTORICAL_CREDIT_SUPPORT  |  Hist Bond Analysis  |  Mtge Historical Credit Support
DY122  |  HIST_PRINCIPAL_DISTRIBUTED  |  Hist Bond Analysis  |  Hist Principal Distributed
DY126  |  HIST_LOSSES  |  Hist Bond Analysis  |  Hist Losses
DY123  |  HIST_INTEREST_DISTRIBUTED  |  Hist Bond Analysis  |  Hist Interest Distributed
DT736  |  HIST_UNSUPPORTED_RISK_SHORTFALL  |  Hist Bond Analysis  |  Historical Unsupported Risk Shortfall
DY124  |  HIST_DEFERRED_INTERST  |  Hist Bond Analysis  |  Hist Deferred Interest

## Relative Value
The examples below aim to showcase how you can perform relative value analysis on securitized products directly in Excel, using BQL.
DO NOTE DELETE
Historical Spread / Duration Analysis  |  0  |  Spread  |  Duration
Security 1  |  3137H8QV6 Mtge  |  1  |  I  |  SPREAD
Security 2  |  01F05WG00 Mtge
Spread / Duration  |  Spread  |  2  |  OAS  |  EFFECTIVE
Spread Type  |  I  |  3  |  Z
Relative Start Period  |  -3M
let()  |  let(#type=I; #start=-3M;)
get()  |  get(Spread(Spread_type=#type, dates=range(#start, 0d), fill=prev))
for()  |  for(['3137H8QV6 Mtge','01F05WG00 Mtge'])
3137H8QV6 Mtge  |  01F05WG00 Mtge
2025-06-19 00:00:00  |  85.34832542234  |  140.3682683016
2025-06-20 00:00:00  |  86.06200320515  |  140.48602349527
2025-06-21 00:00:00  |  86.06200320515  |  140.48602349527
2025-06-22 00:00:00  |  86.06200320515  |  140.48602349527
2025-06-23 00:00:00  |  84.00585553647  |  144.18589708986
2025-06-24 00:00:00  |  83.81921289637  |  147.64075210094
2025-06-25 00:00:00  |  83.29239862186  |  148.29362343277
2025-06-26 00:00:00  |  83.9106400075  |  151.78038675596
2025-06-27 00:00:00  |  85.21312667218  |  147.40476678535
2025-06-28 00:00:00  |  85.21312667218  |  147.40476678535
2025-06-29 00:00:00  |  85.21312667218  |  147.40476678535
2025-06-30 00:00:00  |  84.05081220746  |  151.20785697375
2025-07-01 00:00:00  |  84.6833425711  |  149.76801444604
2025-07-02 00:00:00  |  83.94016484768  |  145.56786446508
2025-07-03 00:00:00  |  83.89773191402  |  141.18274287608
2025-07-04 00:00:00  |  83.89773191402  |  141.18274287608
2025-07-05 00:00:00  |  83.89773191402  |  141.18274287608
2025-07-06 00:00:00  |  83.89773191402  |  141.18274287608
2025-07-07 00:00:00  |  83.8367691986  |  136.9421547397
2025-07-08 00:00:00  |  79.12350250776  |  134.24619451171
2025-07-09 00:00:00  |  81.36745946032  |  140.47141125907
2025-07-10 00:00:00  |  81.34192968912  |  139.7589513011
2025-07-11 00:00:00  |  82.43016559105  |  134.89571880059
2025-07-12 00:00:00  |  82.43016559105  |  134.89571880059
2025-07-13 00:00:00  |  82.43016559105  |  134.89571880059
2025-07-14 00:00:00  |  82.6484755845  |  134.34943563962
2025-07-15 00:00:00  |  84.32395099224  |  130.33630419982
2025-07-16 00:00:00  |  82.97133227186  |  131.91653304582
2025-07-17 00:00:00  |  82.91266843453  |  131.55725882061
2025-07-18 00:00:00  |  83.8763760436  |  134.04543724898
2025-07-19 00:00:00  |  83.8763760436  |  134.04543724898
2025-07-20 00:00:00  |  83.8763760436  |  134.04543724898
2025-07-21 00:00:00  |  83.27015980332  |  138.19043744085
2025-07-22 00:00:00  |  85.39405556569  |  141.50072111752
2025-07-23 00:00:00  |  86.89886421417  |  136.98232226075
2025-07-24 00:00:00  |  87.03239239754  |  135.84320473993
2025-07-25 00:00:00  |  84.79339153338  |  137.72047721517
2025-07-26 00:00:00  |  84.79339153338  |  137.72047721517
2025-07-27 00:00:00  |  84.79339153338  |  137.72047721517
2025-07-28 00:00:00  |  84.47974000498  |  134.98987641688
2025-07-29 00:00:00  |  84.14885175932  |  142.6703438701
2025-07-30 00:00:00  |  83.550699248  |  140.0930581981
2025-07-31 00:00:00  |  84.30922926848  |  140.60778880976
2025-08-01 00:00:00  |  85.3340243604  |  151.95231651054
2025-08-02 00:00:00  |  85.3340243604  |  151.95231651054
2025-08-03 00:00:00  |  85.3340243604  |  151.95231651054
2025-08-04 00:00:00  |  85.06585273866  |  153.64622781932
2025-08-05 00:00:00  |  87.66754615593  |  153.79485496676
2025-08-06 00:00:00  |  87.78083945537  |  150.66868689282
2025-08-07 00:00:00  |  87.08122426676  |  147.70915012704
2025-08-08 00:00:00  |  86.87531396138  |  143.52389294842
2025-08-09 00:00:00  |  86.87531396138  |  143.52389294842
2025-08-10 00:00:00  |  86.87531396138  |  143.52389294842
2025-08-11 00:00:00  |  87.15818983234  |  143.78809640546
2025-08-12 00:00:00  |  86.28699099729  |  143.43650301508
2025-08-13 00:00:00  |  85.89305796019  |  148.61088261721
2025-08-14 00:00:00  |  85.81073186763  |  143.31996498983
2025-08-15 00:00:00  |  85.89069800919  |  140.59403185373
2025-08-16 00:00:00  |  85.89069800919  |  140.59403185373
2025-08-17 00:00:00  |  85.89069800919  |  140.59403185373
2025-08-18 00:00:00  |  84.46077598049  |  139.09531803611
2025-08-19 00:00:00  |  85.15313742968  |  142.77021318064
2025-08-20 00:00:00  |  85.00843753812  |  144.35112542568
2025-08-21 00:00:00  |  84.66185195941  |  140.21656212734
2025-08-22 00:00:00  |  85.15965337531  |  146.0972803201
2025-08-23 00:00:00  |  85.15965337531  |  146.0972803201
2025-08-24 00:00:00  |  85.15965337531  |  146.0972803201
2025-08-25 00:00:00  |  84.67027737036  |  143.29668033429
2025-08-26 00:00:00  |  84.51051057165  |  146.81857131143

## Screening & Aggregations
Identify securitized products that match your search criteria and apply filters and groupings to further analyze the results directly in Excel using BQL.
Univ Function  |  Description  |  Parameters  |  Example
mortgages()  |  Pulls all mortgages of a given issuer  |  Useactiveonly
Consolidateduplicates
Includeprivatesecurities  |  mortgages('MS US Equity',useactiveonly=True)
mortgagesuniv()  |  Pulls all mortgages by status  |  Types (Active, Matured, All)
Consolidateduplicates
Includeprivatesecurities  |  mortgagesuniv('active')
screenresults()  |  Pull an example search or user saved search  |  Screen_Name (Found on SRCH<GO> or MTGS <GO>)  |  screenresults(type=SRCH, screen_name='@MOD')
Count the total number of securities included in the saved SRCH<GO> search US ABS Issuance @IABS
Screen Name  |  @IABS
let()  |  let(#count= count(group(id));)  |  19138
get()  |  get(#count)
for()  |  for(screenresults(SRCH, screen_name='@IABS'))
Average I-spread of US Auto ABS maturing in the next 3 years by S&P Rating
Spread Type  |  I
I
get()  |  get(groupsort(avg(group(spread(spread_type=I), rtg_sp)), order=desc) as #Average_I_Spread)  |  ID  |  #Average_I_Spread  |  Z
N.A.  |  590.5380037397647  |  OAS
for()  |  for(filter(mortgagesuniv(Active), structured_prod_class_ast_subcl=='CARS'
AND maturity <= 3Y AND crncy=='USD'))  |  NR  |  264.19248699437  |  N
BB-  |  230.17094480293  |  E
BB  |  119.390154291295  |  J
BBB  |  111.989705010905  |  A
A+  |  95.916583033824  |  P
BBB+  |  92.1127714672  |  R
A-  |  84.26661702299144
A  |  67.05799708512
AA-  |  65.94335717882
AA+  |  64.8395829198012
AA  |  54.37501390754381
(P)AAA  |  48.42829061761
A-1+  |  29.395831147362635
AAA  |  27.101766850785758
(P)A-1+  |  21.036719396247502
B  |  #N/A
B-  |  #N/A
Top 20 IG US Auto ABS that are maturing in the next 3 years with WAL greater than 0.5 by 1 week I-Spread change
Spread Type  |  I
let()  |  let(#I_spread = spread(spread_type=I, fill=prev).value;
#1W_I_spread_change = net_chg(spread(spread_type=I, dates=range(-1w,0d), fill=prev)).value;
#rank = grouprank(#1W_I_spread_change);
#Name = groupsort(name, sortby=#1W_I_spread_change, order=desc);
#Delinquencies_Pct = mtg_delinquencies_pct;)  |  ID  |  #Name  |  #I_spread  |  #1W_I_spread_change  |  #Delinquencies_Pct
!!036JC7 Mtge  |  FCAT 2022-2 C  |  93.1091752551  |  36.14467651594  |  9.34
!!037GP4 Mtge  |  FCAT 2022-3 C  |  94.05696542399  |  22.897581643539993  |  9
!!03D8TT Mtge  |  HALST 2024-A B  |  67.27593709075  |  13.181681103190009  |  0.12
!!031TL7 Mtge  |  DTAOT 2021-3A E  |  5.61729405689  |  12.60945799368  |  12.25
!!035RFD Mtge  |  CRVNA 2022-P1 C  |  120.68471563584  |  12.237514604830011  |  #N/A
!!036RQX Mtge  |  GCAR 2022-2A D  |  99.70753615591  |  11.754496975100011  |  2.66
get()  |  get(#Name, #I_spread, #1W_I_spread_change, #Delinquencies_Pct)  |  !!032LLP Mtge  |  CRVNA 2021-P3 C  |  112.44066843855  |  11.091212474910009  |  #N/A
!!0314ML Mtge  |  CRVNA 2021-P2 C  |  111.73114669459  |  10.956853733030002  |  #N/A
for()  |  for(filter(filter(mortgagesuniv(Active), structured_prod_class_ast_subcl=='CARS'
AND maturity <= 3Y and rtg_sp>'BB+' AND mtg_wal>=0.5), #rank<=20))  |  !!037V2N Mtge  |  FORDO 2022-C B  |  55.47615080113  |  10.574651665909997  |  #N/A
!!0349DX Mtge  |  CRVNA 2021-P4 C  |  108.31144177128  |  10.564445621559997  |  #N/A
!!036JT3 Mtge  |  CRVNA 2022-P2 C  |  117.10907376114  |  9.83785705919999  |  #N/A
!!03BXHC Mtge  |  WLAKE 2023-3A C  |  103.6817112762  |  9.242791128779999  |  1.75
!!03BPPK Mtge  |  GMCAR 2023-3 A3  |  35.0885151648  |  9.15265369881  |  #N/A
!!03974L Mtge  |  WOSAT 2023-A B  |  53.5986240397  |  8.669974157059997  |  #N/A
!!038Q3T Mtge  |  WLAKE 2023-1A C  |  83.38316569893  |  7.654213433630005  |  1.67
!!03NT8T Mtge  |  GMALT 2025-3 A2B  |  45.01171487046  |  7.1905017647600005  |  #N/A
!!03N9CM Mtge  |  WLAKE 2025-2A A2A  |  38.92452167468  |  6.904412288370004  |  #N/A
!!03NJC9 Mtge  |  HALST 2025-C A2B  |  43.90235451713  |  6.862139062129998  |  0.01
!!03D8TS Mtge  |  HALST 2024-A A4  |  41.56913465048  |  6.816644290399999  |  0.12
!!03CBVX Mtge  |  GMCAR 2023-4 A3  |  29.30759322708  |  6.60752869713  |  #N/A

## Additional Examples
Total Amount Outstanding (Billions) of UK RMBS Deals by Next Call Date
I
get()  |  get(sum(group(amt_outstanding/1B, year(NXT_CALL_DT))) as #Amt_Out_GBP_Blns)  |  ID  |  #Amt_Out_GBP_Blns  |  Z
2025.0  |  9.783716904071364  |  OAS
for()  |  for(filter(mortgagesuniv('active'), MTG_DEAL_TYP=='CMO' and
CRNCY=='GBP' AND NEXT_CALL_DT!=NA))  |  2026.0  |  17.556822117961744  |  N
2027.0  |  15.961323060429999  |  E
2028.0  |  11.211571080590003  |  J
2029.0  |  5.365255952160003  |  A
2030.0  |  2.335753  |  P
2031.0  |  2.1  |  R
2032.0  |  0.09064110213000001
2033.0  |  1
NullGroup  |  10.989217276789997
CLO Issuance in the last 5 years: EUR vs USD
I
get()  |  get(sum(group(MTG_ORIG_AMT,[crncy, year(issue_dt)]))/1B as #Issuance)  |  ID  |  #Issuance  |  Z
2016  |  EUR:2016.0  |  45.10329555105  |  OAS
for()  |  for(filter(mortgagesuniv('all'), MTG_DEAL_TYP=='CLO' AND
ISSUE_DT>=2016-01-01 and IN(CRNCY, ['USD', 'EUR'])))  |  2017  |  EUR:2017.0  |  60.4202424417  |  N
2018  |  EUR:2018.0  |  79.816314667  |  E
2019  |  EUR:2019.0  |  67.22426476540001  |  J
2020  |  EUR:2020.0  |  46.179102298160004  |  A
2021  |  EUR:2021.0  |  125.18056139353  |  P
2022  |  EUR:2022.0  |  66.49509343542  |  R
2023  |  EUR:2023.0  |  66.095392053
2024  |  EUR:2024.0  |  8.537295
2025  |  EUR:2025.0  |  39.304578
2016  |  USD:2016.0  |  121.88292037698
2017  |  USD:2017.0  |  282.9601424717
2018  |  USD:2018.0  |  304.93930121690005
2019  |  USD:2019.0  |  181.39107688882
2020  |  USD:2020.0  |  137.88007266787
2021  |  USD:2021.0  |  489.23362797633007
2022  |  USD:2022.0  |  187.56568258
2023  |  USD:2023.0  |  146.27154373251
2024  |  USD:2024.0  |  62.49271293628
USD:2025.0  |  161.19227385768002
Average basic spread (coupon/quoted margin) since 2017 for the top tranche of EUR CLOs
I
get()  |  get(avg(group(BASIC_SPREAD, year(ISSUE_DT))) as #Avg_Coupon)  |  ID  |  #Avg_Coupon  |  Z
.0  |  2017.0  |  1.1743750000000002  |  OAS
for()  |  for(filter(mortgagesuniv('all'), MTG_DEAL_TYP=='CLO' AND CRNCY=='EUR' AND TRANCHE_NUM==1 and ISSUE_DT>=2017-01-01))  |  .0  |  2018.0  |  0.48026315789473695  |  N
.0  |  2019.0  |  0.46517241379310353  |  E
.0  |  2020.0  |  0.755625  |  J
.0  |  2021.0  |  0.8811320754716979  |  A
.0  |  2022.0  |  1.3699206349206354  |  P
.0  |  2023.0  |  1.6492207792207798  |  R
.0  |  2024.0  |  1.5399999999999998
.0  |  2025.0  |  1.3054901960784315
