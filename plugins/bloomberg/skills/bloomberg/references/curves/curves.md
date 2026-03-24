# BQL Curves Reference (Sovereign, Custom, BVAL, HSA, Issuer)

## Curves Syntax
Curves Universe Function - curveMembers()
curveMembers() returns the list of bonds associated with an on-the-run curve, or list of tenor series for a constant-maturity curve
curveMembers(symbols={curve ticker}, curve_type=FI, tenors={tenors}, dates={date})
Parameters:  |  Columns:
symbols  |  Curve ticker, or a list of curve tickers  |  ID  |  Bond or Tenor index ticker associated with the tenor point
curve type  |  Optional, defaulting to FI  |  ID().ID_dates  |  Date for which membership is requested
tenors  |  Optional, defaulting to the entire term structure  |  ID().tenor  |  String representation of the tenor point associated with the bond
dates  |  A single date, defaulting to today  |  ID().orig_ids  |  The curve ID originally requested
ID().year_fraction  |  A number indicating the number of years equivalent to the tenor
Syntax Examples:
get(id) for(curveMembers(['YCGT0025 Index'], dates=2022-01-17))  |  Retrieve the entire term structure (all tenors) for the selected curve
get(id) for(curveMembers(['YCGT0025 Index'], tenors='1Y', dates=2022-01-17))  |  Retrieve a single tenor/point for the selected curve
get(id) for(curveMembers(['YCGT0025 Index'], tenors=(['1Y','5Y']), dates=2022-01-17))  |  Retrieve a list of tenors for the selected curve
get(id) for(curveMembers(['YCGT0025 Index'], tenors=range('1Y','10Y'), dates=2022-01-17))  |  Retrieve a part of the selected curve (range of tenors)
Example - Retrieve the list of bonds associated with the US Treasury Active Curve (I25) as of end of June 2023
Get()  |  get(ID)
For()  |  for(curveMembers(['YCGT0025 Index'], dates=2023-06-30))
ID  |  ID.ID_DATES  |  ID.TENOR  |  ID.ORIG_IDS  |  ID.YEAR_FRACTION  |  ID
912797GA Govt  |  2023-06-30 00:00:00  |  1M  |  YCGT0025 Index  |  0.0821917808219178  |  912797GA Govt
912797GJ Govt  |  2023-06-30 00:00:00  |  2M  |  YCGT0025 Index  |  0.1643835616438356  |  912797GJ Govt
912796CS Govt  |  2023-06-30 00:00:00  |  3M  |  YCGT0025 Index  |  0.2465753424657534  |  912796CS Govt
912797HD Govt  |  2023-06-30 00:00:00  |  4M  |  YCGT0025 Index  |  0.3287671232876712  |  912797HD Govt
912796ZN Govt  |  2023-06-30 00:00:00  |  6M  |  YCGT0025 Index  |  0.4931506849315068  |  912796ZN Govt
912797FS Govt  |  2023-06-30 00:00:00  |  1Y  |  YCGT0025 Index  |  1  |  912797FS Govt
91282CHL Govt  |  2023-06-30 00:00:00  |  2Y  |  YCGT0025 Index  |  2  |  91282CHL Govt
91282CHH Govt  |  2023-06-30 00:00:00  |  3Y  |  YCGT0025 Index  |  3  |  91282CHH Govt
91282CHK Govt  |  2023-06-30 00:00:00  |  5Y  |  YCGT0025 Index  |  5  |  91282CHK Govt
91282CHJ Govt  |  2023-06-30 00:00:00  |  7Y  |  YCGT0025 Index  |  7  |  91282CHJ Govt
91282CHC Govt  |  2023-06-30 00:00:00  |  10Y  |  YCGT0025 Index  |  10  |  91282CHC Govt
912810TS Govt  |  2023-06-30 00:00:00  |  20Y  |  YCGT0025 Index  |  20  |  912810TS Govt
912810TR Govt  |  2023-06-30 00:00:00  |  30Y  |  YCGT0025 Index  |  30  |  912810TR Govt
Curve Rates - Rate()
Rate() returns the rate associated with the curve at each requested tenor point. Note that depending on the curve this may be a yield, spread, zero rate or other measure.
rate(side={BID|MID|ASK}, type={PAR|ZERO}, dates={date})
Parameters:  |  Columns:
side  |  Specifies the market side.  |  ID  |  Bond or Tenor index ticker associated with the tenor point
dates  |  A single date, defaulting to today  |  Dates  |  Date for corresponding rate
type  |  Specifies the rate type returned, par (default) or zero.  |  Value  |  Rate applicable or this curve, tenor point and date
Note: Zero rates are only available for sovereign curves.
Example - Retrieve the rate for the 3Y tenor on the US Treasury Active Curve (I25) as of end of June 2023
Get()  |  get(ID().tenor, rate(side=Mid).value as #mid_rate)
For()  |  for(CurveMembers(['YCGT0025 Index'], tenors='3Y'))
With()  |  with(dates=2022-01-17)
ID  |  ID().tenor  |  #mid_rate
91282CDS Govt  |  3Y  |  1.262
Curve Interpolation - Interpolation()
Given a series of (x,y) pairs, interpolation returns the value of y that corresponds to a paricular x value
Interpolation(Interpol_by={item x}, interpol_value={item y}, interpol_points={x point to interpolate at}, interpolation_type=PIECEWISE_LINEAR)
Parameters:  |  Columns:
interpol_by  |  The 'x' value series to compare the point to  |  ID  |  Ticker
interpol_value  |  The 'y' value series to interpolate and return  |  Value  |  interpolated value
interpol_points  |  The 'x' value to lookup in the interpol_by series
interpolation_type  |  Currently only PIECEWISE_LINEAR is supported. This is the default.
Example - Get the interpolated point of an I curve (I25) to a specific number of years (duration based, 4.5)
Get()  |  get(interpolation(value(duration,curveMembers(curve_type=FI), mapby=lineage), value(yield,curveMembers(curve_type=FI), mapby=lineage), 4.5) as #Interopolated_point)
For()  |  for(['YCGT0025 Index'])
ID  |  #Interopolated_point
YCGT0025 Index  |  4.240523627479343
Curve Regression - Regression()
Given a series of (x,y) pairs, regression() fits a regression curve to the data and returns the value of y that corresponds to a paricular x value
Regression(reg_by={item x}, reg_value={item y}, regression_points={x point to interpolate at}, regression_type={REGRESSION_METHOD})
Parameters:  |  Columns:
reg_by  |  The 'x' value series to compare the point to  |  ID  |  Ticker
reg_value  |  The 'y' value series to regress and return  |  Value  |  regressed value
regression_points  |  The 'x' value to lookup in the reg_by series
regression_type  |  LINEAR, LINEAR_LOG, LOG_LOG,
NELSON_SIEGEL, NELSON_SIEGEL_SVENSON
Example - Fit a NSS curve to a set of benchmark bonds and interpolate the curve at the 6yr point
Get()  |  get(regression(value(duration,curvemembers(curve_type=FI), mapby=lineage), value(yield,curvemembers(curve_type=FI), mapby=lineage), 6, NELSON_SIEGEL_SVENSON) as #regressed_point)
For()  |  for(['YCGT0025 Index'])
ID  |  #regressed_point
YCGT0025 Index  |  4.34043286360305

## Sovereign Curves
Sovereign Curves
BQL allows you to monitor changing rate conditions for all sovereign curves and gain insight into how the curve term structure has evolved over time by providing current and historical snapshots.
Sovereign curve tickers can be found in SECF<GO> (Security Finder) in the Bloomberg Terminal in the Curves tab.
1. Retrieve the term structure of the US Treasury Actives Curve (I25) bond curve
Curve Ticker  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
Side  |  Mid
get(ID().tenor as #tenor, id().year_fraction as #year_fraction, rate(side=Mid).value as #rate) for(curveMembers(['YCGT0025 Index'])) with(dates=2023-06-30)
ID  |  #tenor  |  #year_fraction  |  #rate
912797GA Govt  |  1M  |  0.0821917808219178  |  5.142
912797GJ Govt  |  2M  |  0.1643835616438356  |  5.28
912796CS Govt  |  3M  |  0.2465753424657534  |  5.298
912797HD Govt  |  4M  |  0.3287671232876712  |  5.411
912796ZN Govt  |  6M  |  0.4931506849315068  |  5.433
912797FS Govt  |  1Y  |  1  |  5.416
91282CHL Govt  |  2Y  |  2  |  4.866
91282CHH Govt  |  3Y  |  3  |  4.496
91282CHK Govt  |  5Y  |  5  |  4.121
91282CHJ Govt  |  7Y  |  7  |  3.968
91282CHC Govt  |  10Y  |  10  |  3.808
912810TS Govt  |  20Y  |  20  |  4.051
912810TR Govt  |  30Y  |  30  |  3.841
2a. Retrieve a specific tenor point on the selected curve (I25)
Curve Ticker  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
Side  |  Mid
Tenor  |  3Y
get(ID().tenor as #tenor, rate(side=Mid).value as #rate) for(curveMembers(['YCGT0025 Index'], tenors=3Y)) with(dates=2023-06-30)
ID  |  #tenor  |  #rate
91282CHH Govt  |  3Y  |  4.496
2b. Retrieve a specified range of tenor points on the selected curve (I25)
Curve Ticker  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
Side  |  Mid
Tenor Range  |  2Y  |  5Y
get(ID().tenor, rate(side=Mid).value as #rate) for(curveMembers(['YCGT0025 Index'], tenors=range(2Y,5Y))) with(dates=2023-06-30)
ID  |  ID().tenor  |  #rate
91282CHL Govt  |  2Y  |  4.866
91282CHH Govt  |  3Y  |  4.496
91282CHK Govt  |  5Y  |  4.121
3. Plot a bond curve with specified duration/maturity and yield field
Curve Ticker  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
get(duration().value, yield().value) for(curveMembers(['YCGT0025 Index'])) with(dates=2023-06-30)
ID  |  duration().value  |  yield().value
912797GA Govt  |  0.07738854  |  5.14705124
912797GJ Govt  |  0.15201743  |  5.27820846
912796CS Govt  |  0.23201127  |  5.30302781
912797HD Govt  |  0.31454045  |  5.4065956
912796ZN Govt  |  0.47440705  |  5.44558729
912797FS Govt  |  0.92238093  |  5.40584035
91282CHL Govt  |  1.87500457  |  4.86883356
91282CHH Govt  |  2.72497544  |  4.49800516
91282CHK Govt  |  4.43664601  |  4.12302518
91282CHJ Govt  |  6.01606356  |  3.97064136
91282CHC Govt  |  8.14748108  |  3.8096491
912810TS Govt  |  13.46406127  |  4.0516411
912810TR Govt  |  17.41785359  |  3.84195794
4a. Plot multiple curves (I16 and I40)
Curve Ticker 1  |  YCGT0016 Index
Curve Ticker 2  |  YCGT0040 Index
Date  |  2023-06-30 00:00:00
Tenors  |  1Y  |  30Y
get(CNTRY_OF_RISK as #country, id().year_fraction as #year_fraction, rate().value as #rate) for(curveMembers(['YCGT0016 Index','YCGT0040 Index'])) with(tenors=range(1Y,30Y), dates=2023-06-30)
ID  |  #country  |  #year_fraction  |  #rate
ZK941271 Corp  |  DE  |  1  |  3.589
ZK225394 Corp  |  DE  |  2  |  3.196
BQ312492 Corp  |  DE  |  3  |  2.817
BX303989 Corp  |  DE  |  4  |  2.637
ZK885444 Corp  |  DE  |  5  |  2.55
BP153186 Corp  |  DE  |  6  |  2.488
BZ636318 Corp  |  DE  |  7  |  2.469
BN261261 Corp  |  DE  |  8  |  2.376
BT245031 Corp  |  DE  |  9  |  2.352
ZM198538 Corp  |  DE  |  10  |  2.392
BV982438 Corp  |  DE  |  15  |  2.494
EI322934 Corp  |  DE  |  20  |  2.487
AP115404 Corp  |  DE  |  25  |  2.34
BY899086 Corp  |  DE  |  30  |  2.389
ZK912175 Corp  |  IT  |  1  |  3.864
ZL162943 Corp  |  IT  |  2  |  3.9
ZL520919 Corp  |  IT  |  3  |  3.818
BU719159 Corp  |  IT  |  4  |  3.741
ZN621438 Corp  |  IT  |  5  |  3.753
BW443138 Corp  |  IT  |  6  |  3.813
ZK116654 Corp  |  IT  |  7  |  3.881
BP968841 Corp  |  IT  |  8  |  3.895
BW152567 Corp  |  IT  |  9  |  3.957
ZK356093 Corp  |  IT  |  10  |  4.072
BW763624 Corp  |  IT  |  15  |  4.259
ZM337817 Corp  |  IT  |  20  |  4.379
AN868354 Corp  |  IT  |  25  |  4.295
ZL106368 Corp  |  IT  |  30  |  4.443
4b. Plot multiple curves (I16 and I40)  - value() version

## Zero Sovereign
Sovereign Curves - Zero Rates
The rate() field in BQL accepts a type parameter which allows you to retrieve and analyse current/historical zero rates for sovereign curves.
Bloomberg transforms coupon bearing instruments to non-coupon (zero) bearing instruments by using a bootstrapping methodology to mathematically solve for the implied spot rates from the curve.
Zero sovereign rates are visible also in GC<GO> in the Bloomberg Terminal, setting the Y-Axis dropdown to Bid/Mid/Ask Zero Coupon.
1. Plot the mid par rate and the mid zero rate for the US Treasury Actives Curve (I25)
Curve Ticker  |  YCGT0025 Index
Date  |  2022-01-20 00:00:00
Rate Type 1  |  Par
Rate Type 2  |  Zero
Side  |  Mid
get(ID().tenor as #tenor,ID().year_fraction as #year_fraction, rate(type=Par,side=Mid).value as #par_rate,rate(type=Zero,side=Mid).value as #zero_rate) for(curveMembers(['YCGT0025 Index'])) with(dates=2022-01-20)
ID  |  #tenor  |  #year_fraction  |  #par_rate  |  #zero_rate
912796R8 Govt  |  1M  |  0.0821917808219178  |  0.038
912796S8 Govt  |  2M  |  0.1643835616438356  |  0.046
912796G4 Govt  |  3M  |  0.2465753424657534  |  0.171  |  0.168
912796S4 Govt  |  6M  |  0.4931506849315068  |  0.352  |  0.349
912796R2 Govt  |  1Y  |  1  |  0.547  |  0.601
91282CDR Govt  |  2Y  |  2  |  1.027  |  1.047
91282CDS Govt  |  3Y  |  3  |  1.335  |  1.313
91282CDQ Govt  |  5Y  |  5  |  1.609  |  1.594
91282CDP Govt  |  7Y  |  7  |  1.768  |  1.756
91282CDJ Govt  |  10Y  |  10  |  1.819  |  1.822
912810TC Govt  |  20Y  |  20  |  2.188  |  2.216
912810TB Govt  |  30Y  |  30  |  2.124  |  2.122
2. Retrieve the zero rate for a specific point/tenor on the curve
Curve Ticker  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
Side  |  Mid
Type  |  Zero
Tenor  |  3Y
get(ID().tenor, rate(type=Zero,side=Mid).value as #zero_mid) for(curveMembers(['YCGT0025 Index'],tenors=3Y)) with(dates=2023-06-30)
ID  |  ID().tenor  |  #zero_mid
91282CHH Govt  |  3Y  |  4.409
3. Get the GBP United Kingdom Sovereign bid zero curve (I22)
Curve Ticker  |  YCGT0022 Index
Date  |  2023-06-30 00:00:00
Side  |  Bid
Type  |  Zero
get(ID().tenor, rate(type=Zero,side=Bid).value as #zero_mid) for(curveMembers(['YCGT0022 Index'])) with(dates=2023-06-30)
ID  |  ID().tenor  |  #zero_mid
ZM451807 Corp  |  1M
ZL675763 Corp  |  3M  |  5.251
ZJ020708 Corp  |  6M  |  5.595
AT647761 Corp  |  1Y  |  5.238
AZ278084 Corp  |  2Y  |  5.162
JK030916 Corp  |  3Y  |  4.978
AM781675 Corp  |  4Y  |  4.799
AR641250 Corp  |  5Y  |  4.626
BR181418 Corp  |  6Y  |  4.559
BH295614 Corp  |  7Y  |  4.394
BM310773 Corp  |  8Y  |  4.314
EC256595 Corp  |  9Y  |  4.206
ZN905632 Corp  |  10Y  |  4.307
ZO277567 Corp  |  12Y
BZ691391 Corp  |  15Y  |  4.47
EG506481 Corp  |  20Y  |  4.44
AU379648 Corp  |  25Y
ZM382322 Corp  |  30Y  |  4.317
BJ457937 Corp  |  40Y
BU075688 Corp  |  50Y

## Custom Curves
Custom Curves
In addition to retrieving sovereign curves (I-curves), you can also analyze custom sovereign/credit curves using BQL created using Custom Curve Builder CRV<GO> in the Bloomberg Terminal.
To use your custom curves in BQL, please ensure you selected 'Tickerised Tenors' in CRV<GO>.
How to create a custom curve?
Run CRV<GO> in the Bloomberg Terminal. The home screen allows you to begin the curve creation process by selecting the type of curve you want to create e.g. Fitted Curve.
Then, move to the 'Choose Securities' page, which allows you to define the list of securities that you want to constitute the custom curve, so you can create a curve to suit your analysis.
Moving then to the 'Construct Curve' page, this step allows you to analyze and adjust the tenors/points that are included in the custom curve, so you can remove any outliers or smooth out the curve. Note: 'Tickerize Tenors' must be select for your custom curve to be accessible in BQL.
The 'My Curves' tab in CRV<GO> displays all of the curves you have created on CRV, so you can easily locate and edit a curve.
1. Retrieve a custom bond curve with tickerized tenors (Created in CRV<GO>)
Curve Ticker  |  YCFC3YSS Index  |  < Replace with the idenifier for one of your custom curves (with tickerized tenors)
Date  |  2023-09-18 00:00:00
Side  |  Bid
get(ID().tenor, rate(side=Mid).value as #rate) for(curveMembers(['YCFC3YSS Index'])) with(dates=2023-09-18)
#N/A Invalid Security: Unable to evaluate universe. Either the identifier is invalid or you do not have access to the data. Check inputs and try again.
2. Retrieve a selected point on the custom bond curve
Curve Ticker  |  YCFC3YSS Index
Date  |  2023-09-18 00:00:00
Side  |  Mid
Tenor  |  3Y
get(ID().tenor as #tenor, rate(side=Mid).value as #rate) for(curveMembers(['YCFC3YSS Index'], tenors=3Y)) with(dates=2023-09-18)
#N/A Invalid Security: Unable to evaluate universe. Either the identifier is invalid or you do not have access to the data. Check inputs and try again.
3. Retrieve a specified range of tenor points
Curve Ticker  |  YCFC3YSS Index
Date  |  2023-09-09 00:00:00
Side  |  Mid
Tenor Range  |  2Y  |  5Y
get(ID().tenor, rate(side=Mid).value) for(curveMembers(['YCFC3YSS Index'], tenors=range(2Y,5Y))) with(dates=2023-09-09)
#N/A Invalid Security: Unable to evaluate universe. Either the identifier is invalid or you do not have access to the data. Check inputs and try again.
4. Plot multiple curves (Tickerized Bloomberg Curves and Custom Curves)
Curve Ticker 1  |  YCFC3YSS Index
Curve Ticker 2  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
get(id().orig_id, id().year_fraction, rate().value) for(curveMembers(['YCFC3YSS Index','YCGT0025 Index'])) with(dates=2023-06-30)
#N/A Invalid Security: Unable to evaluate universe. Either the identifier is invalid or you do not have access to the data. Check inputs and try again.
5. Compare steepness between two tenor points of different curves
Curve Ticker 1  |  YCFC3YSS Index
Curve Ticker 2  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
Tenor a  |  2Y
Tenor b  |  10Y
let(#a= value(rate, curveMembers(tenors=2Y), mapby=lineage);   #b= value(rate, curveMembers(tenors=10Y), mapby=lineage);)    get(100*(#b - #a)) for(['YCFC3YSS Index','YCGT0025 Index']) with(dates=2023-06-30)
#N/A

## BVAL Curves
BVAL Curves across Government, Agency, Investment-Grade Corporate and U.S. Municipal bond asset classes
You can now use the Bloomberg Query Language (BQL) in Microsoft Excel® and BQuant to analyze current and historical BVAL curves.
Bloomberg's evaluated pricing service, BVAL, offers a deep library of approximately 1,000 Issuer Curves across the Government, Agency, Investment-Grade Corporate and U.S. Municipal bond asset classes.
In addition, BVAL offers a comprehensive library of more than 700 Corporate and U.S. Municipal sector curves. Curves are published once daily based on the regional close for the respective currency.
1. Retrieve the term structure for the USD US Corporate BBB+, BBB, BBB- BVAL Yield Curve
Curve Ticker  |  BVSC0075 Index  |  USD US Corporate BBB+, BBB, BBB- BVAL Yield Curve
get(name, ID().year_fraction as #tenor, rate().value as #rate) for(curveMembers(['BVSC0075 Index']))
ID  |  name  |  #tenor
IGUUBC3M BVLI Index  |  BVAL BBB Curve 3 Mo  |  0.2465753424657534
IGUUBC6M BVLI Index  |  BVAL BBB Curve 6 Mo  |  0.4931506849315068
IGUUBC01 BVLI Index  |  BVAL BBB Curve 1 Yr  |  1
IGUUBC02 BVLI Index  |  BVAL BBB Curve 2 Yr  |  2
IGUUBC03 BVLI Index  |  BVAL BBB Curve 3 Yr  |  3
IGUUBC04 BVLI Index  |  BVAL BBB Curve 4 Yr  |  4
IGUUBC05 BVLI Index  |  BVAL BBB Curve 5 Yr  |  5
IGUUBC06 BVLI Index  |  BVAL BBB Curve 6 Yr  |  6
IGUUBC07 BVLI Index  |  BVAL BBB Curve 7 Yr  |  7
IGUUBC08 BVLI Index  |  BVAL BBB Curve 8 Yr  |  8
IGUUBC09 BVLI Index  |  BVAL BBB Curve 9 Yr  |  9
IGUUBC10 BVLI Index  |  BVAL BBB Curve 10 Yr  |  10
IGUUBC15 BVLI Index  |  BVAL BBB Curve 15 Yr  |  15
IGUUBC20 BVLI Index  |  BVAL BBB Curve 20 Yr  |  20
IGUUBC25 BVLI Index  |  BVAL BBB Curve 25 Yr  |  25
IGUUBC30 BVLI Index  |  BVAL BBB Curve 30 Yr  |  30
2. Retrieve data on a specific tenor point for the selected BVAL Curve
Curve Ticker  |  BVSC0075 Index  |  USD US Corporate BBB+, BBB, BBB- BVAL Yield Curve
Date  |  today
Tenor  |  3Y
get(name, ID().tenor as #tenor, rate().value as #rate) for(curveMembers(['BVSC0075 Index'], tenors=3Y)) with(dates=2024-09-15)
ID  |  name  |  #tenor
IGUUBC03 BVLI Index  |  BVAL BBB Curve 3 Yr  |  3Y
3. Retrieve a specified range of tenor points for the selected BVAL Curve
Curve Ticker  |  BVSC0075 Index  |  USD US Corporate BBB+, BBB, BBB- BVAL Yield Curve
Date  |  today
Tenor Range  |  1Y  |  10Y
get(name, ID().tenor, rate().value as #rate) for(curveMembers(['BVSC0075 Index'], tenors=range(1Y,10Y))) with(dates=2024-09-15)
ID  |  name  |  ID().tenor
IGUUBC01 BVLI Index  |  BVAL BBB Curve 1 Yr  |  1Y
IGUUBC02 BVLI Index  |  BVAL BBB Curve 2 Yr  |  2Y
IGUUBC03 BVLI Index  |  BVAL BBB Curve 3 Yr  |  3Y
IGUUBC04 BVLI Index  |  BVAL BBB Curve 4 Yr  |  4Y
IGUUBC05 BVLI Index  |  BVAL BBB Curve 5 Yr  |  5Y
IGUUBC06 BVLI Index  |  BVAL BBB Curve 6 Yr  |  6Y
IGUUBC07 BVLI Index  |  BVAL BBB Curve 7 Yr  |  7Y
IGUUBC08 BVLI Index  |  BVAL BBB Curve 8 Yr  |  8Y
IGUUBC09 BVLI Index  |  BVAL BBB Curve 9 Yr  |  9Y
IGUUBC10 BVLI Index  |  BVAL BBB Curve 10 Yr  |  10Y
4. Plot a bond curve with specified maturity and yield as of a past date
Curve Ticker  |  BVSC0075 Index  |  USD US Corporate BBB+, BBB, BBB- BVAL Yield Curve
Date  |  2024-07-30 00:00:00
get(name, id().year_fraction as #tenor, rate().value as #yield) for(curveMembers(['BVSC0075 Index'])) with(dates=2024-07-30)
ID  |  name  |  #tenor
IGUUBC3M BVLI Index  |  BVAL BBB Curve 3 Mo  |  0.2465753424657534
IGUUBC6M BVLI Index  |  BVAL BBB Curve 6 Mo  |  0.4931506849315068
IGUUBC01 BVLI Index  |  BVAL BBB Curve 1 Yr  |  1
IGUUBC02 BVLI Index  |  BVAL BBB Curve 2 Yr  |  2
IGUUBC03 BVLI Index  |  BVAL BBB Curve 3 Yr  |  3
IGUUBC04 BVLI Index  |  BVAL BBB Curve 4 Yr  |  4
IGUUBC05 BVLI Index  |  BVAL BBB Curve 5 Yr  |  5
IGUUBC06 BVLI Index  |  BVAL BBB Curve 6 Yr  |  6
IGUUBC07 BVLI Index  |  BVAL BBB Curve 7 Yr  |  7
IGUUBC08 BVLI Index  |  BVAL BBB Curve 8 Yr  |  8
IGUUBC09 BVLI Index  |  BVAL BBB Curve 9 Yr  |  9
IGUUBC10 BVLI Index  |  BVAL BBB Curve 10 Yr  |  10
IGUUBC15 BVLI Index  |  BVAL BBB Curve 15 Yr  |  15
IGUUBC20 BVLI Index  |  BVAL BBB Curve 20 Yr  |  20
IGUUBC25 BVLI Index  |  BVAL BBB Curve 25 Yr  |  25
IGUUBC30 BVLI Index  |  BVAL BBB Curve 30 Yr  |  30
5. Analyze how the term structure changes over time for the chosen BVAL Curve
Curve Ticker  |  BVSC0484 Index  |  USD US Treasury Bills & Bonds BVAL Yield Curve
Date 1  |  2023-08-21 00:00:00
Date 2  |  2024-02-21 00:00:00
Date 3  |  2024-08-21 00:00:00
get(id().year_fraction as #tenor, rate().value) for(curveMembers('BVSC0484 Index')) with(dates=2023-08-21)
get(rate().value) for(curveMembers('BVSC0484 Index')) with(dates=2024-02-21)
get(rate().value) for(curveMembers('BVSC0484 Index')) with(dates=2024-08-21)
2023-08-21 00:00:00  |  2024-02-21 00:00:00  |  2024-08-21 00:00:00
ID  |  #tenor  |  #N/A  |  #N/A
BVCVXH1M BVLI Index  |  0.0821917808219178
BVCVXH3M BVLI Index  |  0.2465753424657534
BVCVXH6M BVLI Index  |  0.4931506849315068
BVCVXH01 BVLI Index  |  1
BVCVXH02 BVLI Index  |  2
BVCVXH03 BVLI Index  |  3
BVCVXH04 BVLI Index  |  4
BVCVXH05 BVLI Index  |  5
BVCVXH07 BVLI Index  |  7

## HSA Curve Strategies
What's New?
Now you can incorporate custom spread analysis for multiple curve strategies using the Bloomberg Query Language (BQL) in Microsoft Excel® and BQuant so you can determine the relative value of current strategies and generate trade ideas (similar to the type of analysis you can do in HSA<GO> in the Bloomberg Terminal). Choose whether you want to create a curve, butterfly, or box strategy using a swap, government, credit or custom curve. You can search for curves available in the Bloomberg database that are relevant to your fixed income market analysis using CRVF<GO> in the Bloomberg Terminal.
Creating Curve Strategies
The new curve_strategy field allows you to create your desired curve strategy.
The strategy_type parameter lets you define the type of strategy to create (spread, butterfly, box).
Add tenor spreads to analyze current and historical data for your custom strategy.
Curve_Strategy
Define your custom curve strategy. Choose whether you want to create a curve, butterfly, or box strategy using a swap, government, credit or custom curve.
curve_strategy(strategy_type=spread, tenor_1={tenor 1}, tenor_2={tenor 2})
curve_strategy(strategy_type=butterfly, tenor_1={tenor 1}, tenor_2={tenor 2}, tenor_3={tenor 3})
curve_strategy(strategy_type=box, tenor_1={tenor 1}, tenor_2={tenor 2}, tenor_3={tenor 3}, tenor_4={tenor 4})
Parameters  |  Values  |  Parameter Type
curve_strategy  |  spread / butterfly / box  |  Mandatory
tenor_1  |  any supported tenor for the chosen curve e.g. 2Y  |  Mandatory for all strategy types
tenor_2  |  any supported tenor for the chosen curve e.g. 5Y  |  Mandatory for all strategy types
tenor_3  |  any supported tenor for the chosen curve e.g. 7Y  |  Mandatory for butterfly strategy
tenor_4  |  any supported tenor for the chosen curve e.g. 10Y  |  Mandatory for box strategy
Examples
Curve Spread Strategy
Curve  |  YCGT0025 Index  |  US Treasury Actives Curve
Strategy  |  curve_strategy(spread, 2y, 10y)
Spread  |  11.000000000000032
Curve Butterfly Strategy
Curve  |  YCSW0490 Index  |  USD SOFR (vs. FIXED RATE)
Strategy  |  curve_strategy(butterfly, 2y, 5y, 10y)
Spread  |  -15.59999999999997
Curve Box Strategy
Curve  |  YCSW0490 Index  |  USD SOFR (vs. FIXED RATE)
Strategy  |  curve_strategy(box, 5y, 10y, 12y, 15y)
Spread  |  -2.020000000000002
Historical Sovereign Spread Analysis
Analyze historical spreads for your strategy for the selected date range to see if they are widening or tightening over time.
Example 1 - Analyze how the 2y-10y US Government curve spread evolved over the last six months (March to September 2024).
Curve  |  YCGT0025 Index  |  US Treasury Actives Curve
Strategy  |  curve_strategy(spread, 2y, 10y)
Date  |  Spread
2024-03-01 00:00:00  |  -35.099999999999994
2024-03-02 00:00:00  |  -35.099999999999994
2024-03-03 00:00:00  |  -35.099999999999994
2024-03-04 00:00:00  |  -38.39999999999995
2024-03-05 00:00:00  |  -41.09999999999996
2024-03-06 00:00:00  |  -45.39999999999998
2024-03-07 00:00:00  |  -41.99999999999999
2024-03-08 00:00:00  |  -39.800000000000054
2024-03-09 00:00:00  |  -39.800000000000054
2024-03-10 00:00:00  |  -39.800000000000054
2024-03-11 00:00:00  |  -43.599999999999994
2024-03-12 00:00:00  |  -44.00000000000004
2024-03-13 00:00:00  |  -43.599999999999994
2024-03-14 00:00:00  |  -39.79999999999997
2024-03-15 00:00:00  |  -41.99999999999999
2024-03-16 00:00:00  |  -41.99999999999999
2024-03-17 00:00:00  |  -41.99999999999999
2024-03-18 00:00:00  |  -40.20000000000002
2024-03-19 00:00:00  |  -39.39999999999992
2024-03-20 00:00:00  |  -33.70000000000006
2024-03-21 00:00:00  |  -36.7
2024-03-22 00:00:00  |  -38.60000000000001
2024-03-23 00:00:00  |  -38.60000000000001
2024-03-24 00:00:00  |  -38.60000000000001
2024-03-25 00:00:00  |  -38.19999999999997
2024-03-26 00:00:00  |  -35.20000000000003
2024-03-27 00:00:00  |  -38.09999999999994
2024-03-28 00:00:00  |  -42.10000000000002
2024-03-29 00:00:00  |  -42.10000000000002
2024-03-30 00:00:00  |  -42.10000000000002
2024-03-31 00:00:00  |  -42.10000000000002
2024-04-01 00:00:00  |  -39.20000000000003
2024-04-02 00:00:00  |  -34.19999999999996
2024-04-03 00:00:00  |  -32.89999999999998
2024-04-04 00:00:00  |  -33.60000000000003
2024-04-05 00:00:00  |  -35.00000000000006
2024-04-06 00:00:00  |  -35.00000000000006
2024-04-07 00:00:00  |  -35.00000000000006
2024-04-08 00:00:00  |  -37.29999999999993
2024-04-09 00:00:00  |  -37.999999999999986
2024-04-10 00:00:00  |  -41.700000000000074
2024-04-11 00:00:00  |  -37.100000000000044
2024-04-12 00:00:00  |  -37.39999999999996
2024-04-13 00:00:00  |  -37.39999999999996
2024-04-14 00:00:00  |  -37.39999999999996
2024-04-15 00:00:00  |  -31.099999999999994
2024-04-16 00:00:00  |  -30.70000000000004
2024-04-17 00:00:00  |  -34.500000000000064
2024-04-18 00:00:00  |  -35.400000000000006
2024-04-19 00:00:00  |  -36.20000000000001
2024-04-20 00:00:00  |  -36.20000000000001
2024-04-21 00:00:00  |  -36.20000000000001
2024-04-22 00:00:00  |  -35.50000000000004
2024-04-23 00:00:00  |  -32.599999999999966
2024-04-24 00:00:00  |  -28.800000000000026
2024-04-25 00:00:00  |  -29.300000000000015
2024-04-26 00:00:00  |  -33.09999999999995
2024-04-27 00:00:00  |  -33.09999999999995
2024-04-28 00:00:00  |  -33.09999999999995
2024-04-29 00:00:00  |  -36.00000000000003
2024-04-30 00:00:00  |  -35.299999999999976
2024-05-01 00:00:00  |  -32.70000000000009
2024-05-02 00:00:00  |  -30.400000000000027
2024-05-03 00:00:00  |  -30.799999999999983
2024-05-04 00:00:00  |  -30.799999999999983
2024-05-05 00:00:00  |  -30.799999999999983
2024-05-06 00:00:00  |  -34.59999999999992
2024-05-07 00:00:00  |  -37.09999999999995
2024-05-08 00:00:00  |  -34.3
2024-05-09 00:00:00  |  -35.9
2024-05-10 00:00:00  |  -36.7
2024-05-11 00:00:00  |  -36.7
2024-05-12 00:00:00  |  -36.7
2024-05-13 00:00:00  |  -37.80000000000001
2024-05-14 00:00:00  |  -37.19999999999999
2024-05-15 00:00:00  |  -38.3
2024-05-16 00:00:00  |  -41.69999999999998
2024-05-17 00:00:00  |  -40.79999999999995
2024-05-18 00:00:00  |  -40.79999999999995
2024-05-19 00:00:00  |  -40.79999999999995
2024-05-20 00:00:00  |  -40.39999999999999

## Curve Fitting and Interpolation
Regressions and Interpolations
Regression()
Given a series of (x,y) pairs, regression() fits a regression curve to the data and returns the value of y that corresponds to a paricular x value
Regression(reg_by={item x}, reg_value={item y}, regression_points={x point to interpolate at}, regression_type={REGRESSION_METHOD})
Parameters:  |  Columns:
reg_by  |  The 'x' value series to compare the point to  |  ID  |  Ticker
reg_value  |  The 'y' value series to regress and return  |  Value  |  regressed value
regression_points  |  The 'x' value to lookup in the reg_by series
regression_type  |  LINEAR, LINEAR_LOG, LOG_LOG,
NELSON_SIEGEL, NELSON_SIEGEL_SVENSON
Interpolation()
Given a series of (x,y) pairs, interpolation returns the value of y that corresponds to a paricular x value
Interpolation(Interpol_by={item x}, interpol_value={item y}, interpol_points={x point to interpolate at}, interpolation_type=PIECEWISE_LINEAR)
Parameters:  |  Columns:
interpol_by  |  The 'x' value series to compare the point to  |  ID  |  Ticker
interpol_value  |  The 'y' value series to interpolate and return  |  Value  |  interpolated value
interpol_points  |  The 'x' value to lookup in the interpol_by series
interpolation_type  |  Currently only PIECEWISE_LINEAR is supported (default)
1. Piecewise-linear Interpolation of an I curve to a specific number of years (duration based):
Curve Ticker  |  YCGT0025 Index
Interpol Point  |  2023-06-30 00:00:00
get(interpolation(INTERPOL_BY=group(duration), INTERPOL_VALUE=group(yield),  INTERPOL_POINTS=4.5, INTERPOLATION_TYPE=PIECEWISE_LINEAR)) for(curveMembers(['YCGT0025 Index']))
4.240523627479343
2. Piecewise-linear Interpolation of an I curve to a specific number of years (duration based) - value() version:
Curve Ticker  |  YCGT0025 Index
Interpol Point  |  4
get(interpolation(INTERPOL_BY=value(duration,curveMembers(curve_type=FI), mapby=lineage), INTERPOL_VALUE=value(yield,curveMembers(curve_type=FI), mapby=lineage),  INTERPOL_POINTS=4, INTERPOLATION_TYPE=PIECEWISE_LINEAR)) for(['YCGT0025 Index'])
4.2323183374346804
3. Piecewise-linear Interpolation of an I curve to a specific number of years (tenor based, matching CG) value() version:
Curve Ticker  |  YCGT0025 Index
Date  |  2023-06-30 00:00:00
Interpol Point  |  4.5
let(#d=2023-06-30;  #c=curveMembers();  #x=value(ID().year_fraction, #c, mapby=lineage); #y=value(rate, #c, mapby=lineage);) get(interpolation(#x,#y,  4.5, PIECEWISE_LINEAR)) for(['YCGT0025 Index']) with(dates=#d)
4.21625
4. Piecewise-linear Interpolation of multiple I or custom curves to a specific date (tenor based, custom field):
Curve Ticker 1  |  YCGT0025 Index
Curve Ticker 2  |  YCGT0214 Index
Date  |  2022-01-12 00:00:00
Interpol Point  |  5
let(#d=2022-01-12;) get(interpolation(INTERPOL_BY=value(duration, members(type=curve_tenors), mapby=lineage), INTERPOL_VALUE=value(yield, members(type=curve_tenors), mapby=lineage),  INTERPOL_POINTS=5, INTERPOLATION_TYPE=PIECEWISE_LINEAR) as #Interpol_Point) for(['YCGT0025 Index','YCGT0214 Index']) with(dates=#d)
ID  |  #Interpol_Point
YCGT0025 Index  |  1.5164305906851006  |  ID  |  value(duration().value,members(type=curve_tenors),mapby=lineage).SOURCE_ID  |  value(duration().value,members(type=curve_tenors),mapby=lineage)  |  value(yield().value,members(type=curve_tenors),mapby=lineage).SOURCE_ID  |  value(yield().value,members(type=curve_tenors),mapby=lineage)
YCGT0214 Index  |  2.950311211268635  |  YCGT0025 Index  |  912796R7 Govt  |  0.07117074  |  912796R7 Govt  |  0.03757937
YCGT0025 Index  |  912796S7 Govt  |  0.1478108  |  912796S7 Govt  |  0.04478235
YCGT0025 Index  |  912796P2 Govt  |  0.2489975  |  912796P2 Govt  |  0.1179456
YCGT0025 Index  |  912796K5 Govt  |  0.4975947  |  912796K5 Govt  |  0.2788034
YCGT0025 Index  |  912796R2 Govt  |  0.9566058  |  912796R2 Govt  |  0.452199
YCGT0025 Index  |  91282CDR Govt  |  1.947719  |  91282CDR Govt  |  0.9086003
YCGT0025 Index  |  91282CDS Govt  |  2.944933  |  91282CDS Govt  |  1.215276
YCGT0025 Index  |  91282CDQ Govt  |  4.815389  |  91282CDQ Govt  |  1.498663
YCGT0025 Index  |  91282CDP Govt  |  6.646434  |  91282CDP Govt  |  1.674889
YCGT0025 Index  |  91282CDJ Govt  |  9.190969  |  91282CDJ Govt  |  1.73728
YCGT0025 Index  |  912810TC Govt  |  16.34991  |  912810TC Govt  |  2.14253
YCGT0025 Index  |  912810TB Govt  |  22.53473  |  912810TB Govt  |  2.088047
YCGT0214 Index  |  EJ112948 Corp  |  0.2169195  |  EJ112948 Corp  |  1.910979
YCGT0214 Index  |  EJ827000 Corp  |  1.589519  |  EJ827000 Corp  |  1.895399
YCGT0214 Index  |  LW192995 Corp  |  3.950893  |  LW192995 Corp  |  2.765805
YCGT0214 Index  |  AO061913 Corp  |  4.873655  |  AO061913 Corp  |  2.93604
YCGT0214 Index  |  AR790243 Corp  |  6.146267  |  AR790243 Corp  |  3.079787
YCGT0214 Index  |  AX800911 Corp  |  9.783198  |  AX800911 Corp  |  3.674073
YCGT0214 Index  |  EJ827012 Corp  |  13.32175  |  EJ827012 Corp  |  3.799456
YCGT0214 Index  |  AO061706 Corp  |  15.06238  |  AO061706 Corp  |  3.943004
5. Fit a NSS curve to a set of benchmark bonds and interpolate the curve at the 5yr point
Ticker  |  IBM US Equity
Filters  |  AMT_OUTSTANDING > 1B AND CPN_TYP==FIXED AND CRNCY==USD
Method  |  NELSON_SIEGEL_SVENSON
Point (years)  |  5
let(#criteria=AMT_OUTSTANDING > 1B AND CPN_TYP==FIXED AND CRNCY==USD; #x=value(duration, filter(bonds(),#criteria));   #y=value(yield, filter(bonds(),#criteria));)   get(Regression(#x, #y, 5, NELSON_SIEGEL_SVENSON)) for (['IBM US Equity'])
4.945072036046904
get(groupsort(duration().value) as #duration,yield().value as #yield) for(filter(bonds(['IBM US Equity']),AMT_OUTSTANDING > 1B AND CPN_TYP==FIXED AND CRNCY==USD))
ID  |  #duration  |  #yield  |  Regressed point
ZF667904 Corp  |  13.99142388  |  5.66064072  |  5.60753930642852
ZS542668 Corp  |  13.94683276  |  5.58255186  |  5.578886167149541
EJ222340 Corp  |  11.66663411  |  5.53010596  |  5.478096423744224
ZS542666 Corp  |  10.43983778  |  5.45950744  |  5.409148757306598
BJ226366 Corp  |  5.04929315  |  4.87108131  |  4.950393077869847
ZS542665 Corp  |  4.07172698  |  4.76568767  |  4.843339439502869
BJ226365 Corp  |  2.37400897  |  4.60058132  |  4.667090134223971
ZS542664 Corp  |  1.42498673  |  4.63399031  |  4.60669658386259
JK138051 Corp  |  1.19706939  |  4.63938225  |  4.608510186655698
#N/A Unclassified: Unable to parse request at '(Regression(#x,#y,,'.

## Issuer Curve
*This template visualizes credit curves for certain issuer at different dates. Bonds screening criteria and curve regression metrics can both be customised.
Issuer ID ( Equity / FI )  |  VOD LN EQUITY  |  X  |  Maturity_Years
Issued By  |  CREDIT_FAMILY  |  Y  |  Zspread
Method  |  NELSON_SIEGEL_SVENSON
let(#today=2024-11-19+0d;)  |  let(#today=2023-01-01+0d;)  |  let(#today=2024-11-19+0d;
#univ=filter(bonds(issuedby=CREDIT_FAMILY),  (crncy==USD  ) and (payment_rank=='Sr Unsecured'  ) and duration!=na);
#x=value((maturity-#today)/365.25, #univ);
#y=value(Spread(spread_type=z).value, #univ);)  |  let(#today=2023-01-01+0d;
#univ=filter(bonds(issuedby=CREDIT_FAMILY),  (crncy==USD  ) and (payment_rank=='Sr Unsecured'  ) and duration!=na);
#x=value((maturity-#today)/365.25, #univ);
#y=value(Spread(spread_type=z).value, #univ);)
get(groupsort(security_des,order=asc,sortby=(maturity-#today)/365.25) as#Name,(maturity-#today)/365.25 as#Maturity_Years,Spread(spread_type=z).value as#Zspread)  |  get(regression(#x,#y,3,NELSON_SIEGEL_SVENSON))
for(filter(BONDS('VOD LN EQUITY',issuedby=CREDIT_FAMILY), (crncy==USD  ) and (payment_rank=='Sr Unsecured'  ) and duration!=na))  |  for('VOD LN EQUITY')
with(dates=2024-11-19,fill=prev)  |  with(dates=2023-01-01,fill=prev)
Individual Bonds (2024-11-19)  |  Individual Bonds (2023-01-01)  |  3 Year Tenor History
Date 1  |  2024-11-19 00:00:00  |  Date 2  |  2023-01-01 00:00:00  |  Tenor  |  3
ID  |  #Name  |  #Maturity_Years  |  #Zspread  |  Regressed Point  |  ID  |  #Name  |  #Maturity_Years  |  #Zspread  |  Regressed Point  |  Historical Data for Certain Tenor
AS779472 Corp  |  VOD 4 ⅛ 05/30/25  |  0.5256673511293635  |  32.40478755  |  29.83572544537746  |  AS779472 Corp  |  VOD 4 ⅛ 05/30/25  |  2.409308692676249  |  54.09333292  |  54.72126424045361  |  2024-05-19 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
AS779498 Corp  |  VOD 4 ⅜ 05/30/28  |  3.5263518138261465  |  50.20544617  |  59.4118312567868  |  AS779498 Corp  |  VOD 4 ⅜ 05/30/28  |  5.409993155373032  |  106.07788262  |  122.01219252219937  |  2024-05-20 00:00:00  |  57.26201612278044
EC326613 Corp  |  VOD 7 ⅞ 02/15/30  |  5.240246406570842  |  88.94117148  |  82.45431242191117  |  EC765722 Corp  |  VOD 6 ¼ 11/30/32  |  9.91375770020534  |  204.97386921  |  186.70163528873246  |  2024-05-21 00:00:00  |  55.48895243260296
EC225480 Corp  |  VOD 7 ⅞ 02/15/30  |  5.240246406570842  |  88.94117148  |  82.45431242191117  |  AS779549 Corp  |  VOD 5 05/30/38  |  15.408624229979466  |  224.64573837  |  231.0418681308836  |  2024-05-22 00:00:00  |  57.22134213176474
EC765722 Corp  |  VOD 6 ¼ 11/30/32  |  8.030116358658454  |  109.39927116  |  115.93692724155709  |  AS779551 Corp  |  VOD 5 ¼ 05/30/48  |  25.409993155373034  |  273.03438271  |  265.91101768552585  |  2024-05-23 00:00:00  |  57.64339215731712
EG212194 Corp  |  VOD 6.15 02/27/37  |  12.27378507871321  |  152.08331483  |  152.89782714916447  |  2024-05-24 00:00:00  |  58.70593891111025
AS779549 Corp  |  VOD 5 05/30/38  |  13.52498288843258  |  153.24154234  |  161.1016441020236  |  2024-05-25 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
EJ552321 Corp  |  VOD 4 ⅜ 02/19/43  |  18.250513347022586  |  156.57402245  |  184.60315254099336  |  2024-05-26 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
QJ878733 Corp  |  VOD 5.35 12/03/45  |  21.037645448323065  |  234.56956569  |  194.55177167895567  |  2024-05-27 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
QZ019348 Corp  |  VOD 4.6 08/09/46  |  21.71937029431896  |  231.22988957  |  196.66733507159898  |  2024-05-28 00:00:00  |  57.31062911751218
AM418639 Corp  |  VOD 5.35 03/09/47  |  22.299794661190965  |  210.24253985  |  198.38366793813623  |  2024-05-29 00:00:00  |  61.804745335077385
AS779551 Corp  |  VOD 5 ¼ 05/30/48  |  23.526351813826146  |  183.27680206  |  201.77472324976867  |  2024-05-30 00:00:00  |  61.845227021122184
AZ135175 Corp  |  VOD 4 ⅞ 06/19/49  |  24.580424366872005  |  194.81483898  |  204.45602333770424  |  2024-05-31 00:00:00  |  62.39451844712927
ZR549306 Corp  |  VOD 4 ¼ 09/17/50  |  25.82614647501711  |  199.98644201  |  207.37666242391836  |  2024-06-01 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
ZM925878 Corp  |  VOD 5 ⅝ 02/10/53  |  28.227241615331966  |  205.49176357  |  212.34626307392554  |  2024-06-02 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
YX980079 Corp  |  VOD 5 ¾ 06/28/54  |  29.60438056125941  |  205.68194375  |  214.85626786323806  |  2024-06-03 00:00:00  |  62.51232721270344
AZ135179 Corp  |  VOD 5 ⅛ 06/19/59  |  34.57905544147844  |  217.75759846  |  222.2690270725642  |  2024-06-04 00:00:00  |  63.16042519873544
ZM925883 Corp  |  VOD 5 ¾ 02/10/63  |  38.2258726899384  |  235.08155159  |  226.39626738218772  |  2024-06-05 00:00:00  |  63.74058656004409
YX980080 Corp  |  VOD 5 ⅞ 06/28/64  |  39.605749486652975  |  234.02894471  |  227.72651531359494  |  2024-06-06 00:00:00  |  63.42754694992365
2024-06-07 00:00:00  |  63.231776357480584
2024-06-08 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
2024-06-09 00:00:00  |  #N/A Invalid Parameter: Function REGRESSION_IMPL called with empty input.
2024-06-10 00:00:00  |  58.7177648998059
2024-06-11 00:00:00  |  62.55035701972903
2024-06-12 00:00:00  |  58.746624421525524
2024-06-13 00:00:00
2024-06-14 00:00:00
2024-06-15 00:00:00
2024-06-16 00:00:00
2024-06-17 00:00:00
2024-06-18 00:00:00
2024-06-19 00:00:00
2024-06-20 00:00:00
2024-06-21 00:00:00
2024-06-22 00:00:00
2024-06-23 00:00:00
2024-06-24 00:00:00
2024-06-25 00:00:00
2024-06-26 00:00:00
2024-06-27 00:00:00
2024-06-28 00:00:00
2024-06-29 00:00:00
2024-06-30 00:00:00
2024-07-01 00:00:00
2024-07-02 00:00:00
2024-07-03 00:00:00
2024-07-04 00:00:00
2024-07-05 00:00:00
2024-07-06 00:00:00
2024-07-07 00:00:00
2024-07-08 00:00:00
2024-07-09 00:00:00
2024-07-10 00:00:00
2024-07-11 00:00:00
2024-07-12 00:00:00
2024-07-13 00:00:00
2024-07-14 00:00:00
2024-07-15 00:00:00
2024-07-16 00:00:00
2024-07-17 00:00:00
2024-07-18 00:00:00
2024-07-19 00:00:00
2024-07-20 00:00:00
2024-07-21 00:00:00
2024-07-22 00:00:00
2024-07-23 00:00:00
2024-07-24 00:00:00
2024-07-25 00:00:00
2024-07-26 00:00:00
2024-07-27 00:00:00
2024-07-28 00:00:00
2024-07-29 00:00:00
2024-07-30 00:00:00
2024-07-31 00:00:00
2024-08-01 00:00:00
2024-08-02 00:00:00
2024-08-03 00:00:00
2024-08-04 00:00:00
2024-08-05 00:00:00
2024-08-06 00:00:00
2024-08-07 00:00:00
2024-08-08 00:00:00
2024-08-09 00:00:00
2024-08-10 00:00:00
2024-08-11 00:00:00
2024-08-12 00:00:00
2024-08-13 00:00:00
2024-08-14 00:00:00
2024-08-15 00:00:00
2024-08-16 00:00:00
2024-08-17 00:00:00
2024-08-18 00:00:00
2024-08-19 00:00:00
2024-08-20 00:00:00
2024-08-21 00:00:00
2024-08-22 00:00:00
2024-08-23 00:00:00
2024-08-24 00:00:00
2024-08-25 00:00:00
2024-08-26 00:00:00
2024-08-27 00:00:00
2024-08-28 00:00:00
2024-08-29 00:00:00
2024-08-30 00:00:00
2024-08-31 00:00:00
2024-09-01 00:00:00
