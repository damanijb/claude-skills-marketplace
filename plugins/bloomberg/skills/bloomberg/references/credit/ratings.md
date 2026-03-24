# BQL Credit Ratings Reference

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

## rating() - New Data Model
What's New?
• Issuer Level Bloomberg Composite
Bloomberg's issuer-level composite, now available in BQL (2007 - present) can be used to screen and analyze securities on the Corp, Govt, and Equity yellow keys.
The issuer composite and associated effective date is available for more than 4,500 unique issuers and 140,000 active Corp and Govt bonds.
History dating back to 2007 is also available for historical trend analysis.
How do I see it?
To access Bloomberg's issuer-level composite data via BQL you can use in your formula either BB_COMPOSITE_ISSUER or RATING(SOURCE=BBG). If you want to retrieve/analyze additional metrics alongside the rating value you can also view rating attributes like effective dates, numerical scales, etc. Please note both fields take the dates parameter for historical analysis (single date and range).
How is this helping you?
Unlock composite ratings at the issuer-level for sovereign debt securities. Many sovereign bonds use unsolicited ratings, which are not not included in generating bond level composites.
Bloomberg's new issuer-composite fills the gap to provide ratings on a consistent scale for debt issuers.
• Historical Outlooks
BQL allows you to analyze trends on forward-looking credit quality opinions over time (10 yrs) on countries, issuers, and fixed income instruments across 7 CRAs.
How do I see it?
To access historical outlooks, you can use in your formula the RATING_OUTLOOK field on fixed income securities, issuers or countries. Use the source parameter to specify the preferred CRA and the dates parameter for historical analysis (single date and range).
=BQL("['EI240093 Corp','IBM US Equity','1310Z AR Equity']", "rating_outlook(source=SP,dates=range(-5y,0d, frq=m))")
How is this helping you?
Now that an expanded outlooks offering is available in BQL, learn how analyze historical outlooks, trends, identify outlook changes, and create custom dashboards in Microsoft® Excel and BQuant.
Overview
Now you can enrich your credit rating analysis using the new rating() data item in the Bloomberg Query Language (BQL) in Microsoft® Excel and BQuant.
Rating() allows you to access current and historical security or entity level credit ratings and rating attributes contributed from multiple credit rating agencies.
You can use the rating() data item in BQL to:
• Retrieve current and historical security or entity ratings (back to 2007) across 19 providers.
• Chart credit ratings over time.
• Calculate the weighted average rating for your universe of choice.
• Perform aggregations and pivot data by base credit rating.
• Screen fixed income securities based on ratings that match your investment strategy.
• Identify trends of credit ratings agencies upgrading or downgrading borrowers, so you can analyze performance and the length of historical ratings change cycles
Learn more about credit ratings in RATD<GO> here
rating() - New ratings data model
rating() - BQL Request
Field  |  rating
The rating() field now supports a number of optional parameters:
Description  |  Accepted Values  |  Notes
Parameter 1  |  dates  |  lets you define the date
(single or range)  |  dates=2023-11-28
dates=range(2022-11-28,2023-11-28)
dates=-1d
dates=range(-1y,0d)  |  • Dates=0d is default when dates is not specified
• Historical depth:
  - Using Corps/Govies/Pfds/Loans to query historical ratings(issue/issuer) data is available back to 2007
  - Using Equities to query historical ratings (issuer) data is available back to 2015
Parameter 2  |  type
(alias: rating_type)  |  lets you select the rating type (issue level or issuer level ratings)  |  issue
issuer  |  • Using type=issuer you can get issuer level ratings from a bond
• Default rating type depends on the yellow key of the instrument
• Equities default to issuer level ratings
• Corps/Govies/Pfds/Loans default to issue level ratings
Parameter 3  |  source
(alias: rating_source)  |  lets you pick the credit
rating provider to use for the analysis  |  SP  (Standard & Poors)
MOODY (Moody's)
FITCH (Fitch)
AMBEST (A.M. Best)
BBG (Bloomberg Composite)
CHENGXIN (China Chengxin)
CHINA_LOCAL (China Local)
DBRS (DBRS Morningstar)
FELLER (Feller)
FIX_SCR (Fix Scr)
ICRA (ICRA)
JCR (Japan Credit Rating)
KIS (Korea Investors Service)
KOREA (Korea)
LIANHE (Lianhe)
NICE (Nice)
PEFINDO (Pefindo)
RI (Rating & Investment Information)
SBCR (SBCR)  |  • SP is the default source for isssue/issuer level ratings
• Only the following sources are supported for issuer level ratings:
 A.M. BEST, LIANHE, NICE, KIS, SBCR, RI, DBRS, JCR, FITCH, MOODY, SP, BBG
Parameter 4  |  horizon
(alias: rating_horizon)  |  allows you to choose the
credit rating horizon  |  Waterfall (Long term, else short term)
ST (Short term)
LT (Long term)  |  • Only applicable to issuer level ratings
• Smart defaults are is place per rating provider (documented below)
Parameter 5  |  currency
(alias: rating_currency)  |  lets you choose local or foreign currency rating  |  FC (Foreign currency)
LC (Local currency)
ALL (All currencies)  |  • Only applicable to issuer level ratings
• Smart defaults are is place per rating provider (documented below)
Parameter 6  |  debt_category
(alias: issuer_debt_category)  |  Allows you to retrieve the rating assigned  to the selected debt category  |  SENIOR_UNSECURED
SUBORDINATED
FINANCIAL_STRENGTH
PREFERRED
BANK_DEPOSITS
CORPORATE_FAMILY
SENIOR_SECURED
ALL  |  • Only applicable to issuer level ratings
• Smart defaults are is place per rating provider (documented below)
rating() - BQL Response
Alongside the contributed rating value, the BQL response returned by the rating() data item provides a set of associated columns of rating attributes (metadata):
=BQL("DD103619 Corp","RATING","Showallcols=t")
Column  |  Description
Dates  |  Date of the BQL request
Source Scale  |  Numerical scale provider and field specific
Base Rating  |  Clean rating value (no indicators)
Effective Date  |  Date when the rating became effective
Rating Source  |  Rating provider
Watch  |  Credit watch information
Normalized Scale  |  Normalized numerical scale across 7 providers:
S&P,  R&I, Moodys, Fitch, JCR, DBRS, Bloomberg
Only populated for issue level ratings
Rating  |  Rating string as contributed by the provider
Corps, Govts, Loans, Pfds - Security Level Ratings
The table below illustrates how to query security level ratings from a list of fixed income instruments.
CalcRT ID  |  CalcRT Mnemonic  |  BQL Field  |  BQL  Mandatory Parameters  |  BQL Optional Parameters  |  Notes
RA007  |  BB_COMPOSITE  |  rating  |  source=BBG  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA008  |  RTG_AMBEST  |  rating  |  source=AMBEST  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RG928  |  RTG_CHENGXIN  |  rating  |  source=CHENGXIN  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RN747  |  CHINA_LOCAL_CREDIT_RATING  |  rating  |  source=CHINA_LOCAL  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RB303  |  FELLER_RTG  |  rating  |  source=FELLER  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RB030  |  RTG_FIX_SCR  |  rating  |  source=FIX_SCR  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA327  |  RTG_ICRA  |  rating  |  source=ICRA  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA291  |  RTG_ICRA_LONG_TERM  |  rating  |  source=ICRA
horizon=LT  |  dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA070  |  RTG_KOREA  |  rating  |  source=KOREA  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RG956  |  RTG_LIANHE  |  rating  |  source=LIANHE  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA085  |  RTG_NICE  |  rating  |  source=NICE  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA325  |  RTG_PEF  |  rating  |  source=PEFINDO  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA785  |  RTG_KIS  |  rating  |  source=KIS  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RN301  |  RTG_SBCR  |  rating  |  source=SBCR  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA039  |  RTG_RI  |  rating  |  source=RI  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RA006  |  RTG_DBRS  |  rating  |  source=DBRS  |  horizon=waterfall
dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD
RB378  |  RTG_DBRS_LT_ISSUE_WITH_WATCH  |  rating  |  source=DBRS
horizon=LT  |  dates=0d
type=issue  |  dates parameter accepts:
• single date: dates=2023-11-17, dates=-10d
• range: dates=range(2022-01-01,2023-01-01), dates=range(-1y,0d)
• absolute date format should be YYYY-MM-DD

## rating() - Basic Examples
The following examples in Excel show how you can leverage rating() and this expanded data model to better assess the creditworthiness of a debt issuer or specific fixed income security.
Retrieve Bloomberg composite issuer level rating for a selected bond
Enter Bond  |  EI240093 Corp
Name  |  ARGENT 2.26 12/31/38
View/Get()  |  RATING(SOURCE=BBG, type=ISSUER) as #BBG_Issuer
Universe/For()  |  EI240093 Corp
BQL Query  |  get(RATING(SOURCE=BBG,type=ISSUER) as #BBG_Issuer) for(['EI240093 Corp'])
#N/A Requesting Data...
#N/A Requesting Data...
Retrieve S&P rating for a selected bond
Enter Bond  |  US25468PBW59 Corp
Name  |  DIS 7 03/01/32
View/Get()  |  RATING()
Universe/For()  |  US25468PBW59 Corp
BQL Query  |  get(RATING()) for(['US25468PBW59 Corp'])
#N/A Requesting Data...
#N/A Requesting Data...
Retrieve all rating metadata from custom credit agency at chosen date
Enter Bond  |  US25468PBW59 Corp
Name  |  DIS 7 03/01/32
Select Source  |  MOODY
Select Rating Type  |  ISSUE
Enter Date  |  2020-04-19 00:00:00
View/Get()  |  RATING(SOURCE=MOODY, TYPE='ISSUE', DATES=2020-04-19) as #rating
Universe/For()  |  US25468PBW59 Corp
BQL Query  |  get(RATING(SOURCE=MOODY,TYPE='ISSUE',DATES=2020-04-19) as #rating) for(['US25468PBW59 Corp'])
#N/A Requesting Data...
Compare security and entity level ratings across agencies
Enter Bond  |  GB00BMBL1D50 Corp
Name  |  UKT 0 ½ 10/22/61
Security Level Rating  |  Source1  |  Source2  |  Source3  |  Entity Level Rating  |  Source1  |  Source2  |  Source3
Select Source(s)  |  SP  |  MOODY  |  FITCH  |  Select Source(s)  |  SP  |  MOODY  |  FITCH
Select Rating Type  |  ISSUE  |  Select Rating Type  |  ISSUER
Enter Date  |  2026-03-12 00:00:00  |  Enter Date  |  2026-03-12 00:00:00
View/Get()  |  RATING(SOURCE='SP',TYPE='ISSUE', DATES=2026-03-12) as #SP_ISSUE,
RATING(SOURCE='MOODY',TYPE='ISSUE', DATES=2026-03-12) as #MOODY_ISSUE,
RATING(SOURCE='FITCH',TYPE='ISSUE', DATES=2026-03-12) as #FITCH_ISSUE,
RATING(SOURCE=SP,TYPE='ISSUER', DATES=2026-03-12) as #SP_ISSUER,
RATING(SOURCE=MOODY,TYPE='ISSUER', DATES=2026-03-12)  as #MOODY_ISSUER,
RATING(SOURCE=FITCH,TYPE='ISSUER', DATES=2026-03-12)  as #FITCH_ISSUER
Universe/For()  |  GB00BMBL1D50 Corp
BQL Query  |  get(RATING(SOURCE='SP',TYPE='ISSUE',DATES=2026-03-12) as #SP_ISSUE,RATING(SOURCE='MOODY',TYPE='ISSUE',DATES=2026-03-12) as #MOODY_ISSUE,RATING(SOURCE='FITCH',TYPE='ISSUE',DATES=2026-03-12) as #FITCH_ISSUE,RATING(SOURCE=SP,TYPE='ISSUER',DATES=2026-03-12) as #SP_ISSUER,RATING(SOURCE=MOODY,TYPE='ISSUER',DATES=2026-03-12)  as #MOODY_ISSUER,RATING(SOURCE=FITCH,TYPE='ISSUER',DATES=2026-03-12)  as #FITCH_ISSUER) for(['GB00BMBL1D50 Corp'])
#N/A Requesting Data...
Retrieve the base rating, watch and effective date columns only
Enter Bond  |  US25468PBW59 Corp  |  CRPR <GO>
Name  |  DIS 7 03/01/32
Select Source(s)  |  SP
Select Rating Type  |  ISSUE
Enter Date  |  2020-04-19 00:00:00
Variables/Let()  |  #rating=RATING(SOURCE=SP, TYPE='ISSUE', DATES=2020-04-19)

## rating() - Advanced Examples
The below examples in Excel show how you can leverage rating() and this expanded data model for more advanced analysis to better assess credit quality.
Calculate weighted average spreads or yields (weighted by amount outstanding), by credit rating cohorts using the base rating and the contributed rating for Sr Unsecured GBP Financials bonds, then and compare the results
Enter Starting Universe  |  bondsuniv(Active)
Filter  |  BICS_LEVEL_1_SECTOR_NAME=='Financials' and crncy=='GBP'  and payment_rank=='Sr Unsecured'
Field  |  Spread Z
Field BQL Syntax  |  spread(spread_type=Z)
Grouping
Choose Source  |  SP
Enter Type  |  ISSUE
Variables/Let()  |  #rat=RATING(SOURCE=SP, TYPE='ISSUE')
View/Get() 1  |  wavg(GROUP(spread(spread_type=Z),#rat().base_rating),group(amt_outstanding(currency=GBP),#rat().base_rating)) as #WAVG
count(GROUP(spread(spread_type=Z),#rat().base_rating)) as #COUNT
View/Get() 2  |  wavg(GROUP(spread(spread_type=Z),#rat),group(amt_outstanding(currency=GBP),#rat)) as #WAVG
count(GROUP(spread(spread_type=Z),#rat)) as #COUNT
Universe/For()  |  filter(bondsuniv(Active),BICS_LEVEL_1_SECTOR_NAME=='Financials' and crncy=='GBP'  and payment_rank=='Sr Unsecured')
BQL Query 1  |  let(#rat=RATING(SOURCE=SP,TYPE='ISSUE');) get(wavg(GROUP(spread(spread_type=Z),#rat().base_rating),group(amt_outstanding(currency=GBP),#rat().base_rating)) as #WAVG,count(GROUP(spread(spread_type=Z),#rat().base_rating)) as #COUNT) for(filter(bondsuniv(Active),BICS_LEVEL_1_SECTOR_NAME=='Financials' and crncy=='GBP'  and payment_rank=='Sr Unsecured'))
BQL Query 2  |  let(#rat=RATING(SOURCE=SP,TYPE='ISSUE');) get(wavg(GROUP(spread(spread_type=Z),#rat),group(amt_outstanding(currency=GBP),#rat)) as #WAVG,count(GROUP(spread(spread_type=Z),#rat)) as #COUNT) for(filter(bondsuniv(Active),BICS_LEVEL_1_SECTOR_NAME=='Financials' and crncy=='GBP'  and payment_rank=='Sr Unsecured'))
Aggregation by Base Rating  |  Aggregation by Contributed Rating
#N/A Requesting Data...  |  #N/A Requesting Data...
Analyze the S&P credit watch information distribution for names included in the Bloomberg Global High Yield Index
Enter Index  |  LG30TRUU Index
Name  |  Bloomberg Global High Yield Total Return Index Value Unhedge
Choose Source  |  SP
Enter Type  |  ISSUE
Variables/Let()  |  #RTG_WATCH=RATING(SOURCE=SP, TYPE='ISSUE').WATCH
View/Get()  |  count(group(id,#RTG_WATCH)) as #WATCH
Universe/For()  |  members('LG30TRUU Index')
#N/A Requesting Data...
Get the number of upgrades and downgrades every month for the members of an Index as of end Date
Enter Index  |  LUACTRUU Index
Name  |  Bloomberg US Corporate Total R
Choose Source  |  SP
Enter Type  |  ISSUE
Start Date  |  2025-03-01 00:00:00
End Date  |  2026-03-01 00:00:00
Variables/Let()  |  #rat  |  rating(source=SP,type=ISSUE,dates=range(2025-03-01,2026-03-01,frq=cm))
#upgrades  |  dropna(matches(dropna(#rat()),diff(dropna(#rat()).source_scale)<0),true)
#downgrades  |  dropna(matches(dropna(#rat()),diff(dropna(#rat()).source_scale)>0),true)
#upgrades_count  |  count(group(#upgrades().value,#upgrades().DATE+''))
#downgrades_count  |  count(group(#downgrades().value,#downgrades().DATE+''))
View/Get()  |  #upgrades_count,#downgrades_count
Universe/For()  |  members('LUACTRUU Index',dates=2026-03-01)
#N/A Requesting Data...
