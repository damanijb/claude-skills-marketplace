# BQL Funds Reference

## Intro to BQL
Why use BQL?
Bloomberg Query Language(BQL) is Bloomberg's new API. It is the latest advance from Bloomberg which allows users to perform custom calculations/analysis in the Bloomberg Cloud. This makes it possible to extract the right information by synthesizing large amounts of data.
BQL is based on normalized, curated, point-in-time data. BQL allows you to define the data + the analytics (for eg., aggregation/ trend/ filtering/ scoring/ ranking / zscore) you need - to get the answer rather than the data.
Resources:
- HELP BQLX<Go>
- Specialised team on Analytics i.e. HELPHELP<GO>
- BQL Builder in Excel (Future)
Example
How do I pull IBM's Last Price in USD using BQL?
=BQL("IBM US Equity","PX_LAST","CURRENCY=USD")  |  247.67999267578125

## Screening
FOR clause in BQL can take 3 inputs,
Single security       - Eg. .. For ('SPY US Equity')
List of securities    - Eg. .. For (['SPY US Equity', 'EUE IM Equity'])
Universe                   - Eg. .. For (FundsUniv(['Primary','Active']) )
Filtered universe  - Eg. .. For (filter( FundsUniv(['Primary','Active']), FUND_TYP=='ETF') )
How is the Universe filtered / screened using BQL?
To screen, you would need a "filter" function to form part of your "for" clause.
With a filter, you can narrow down your target universe before performing further analysis. Using the correct predicates, you can easily create a curated universe for your analysis.
Syntax:  |  for(filter(universe, predicates))
universe  |  The securities to screen, usually an index or a "Universe".
predicates  |  The conditions to be met by the screen. *Note: when filtering where the values involve text, use quotes around the values. Also, "equals" requires two "=" signs. Ie. "=="
Multiple conditions can be added using "AND" and "OR"
Examples of filtering:
for(filter(FundsUniv(['Primary','Active'], FUND_TYP=='ETF')))

## Aggregation
Step -1 : Group
To perform any Arithmetic operation in BQL, you need to first group the data.
GROUP allows you to create different "buckets" within which you can perform operations. For example:
get(count(group(ID, by=FUND_STRATEGY))) for(...)
The above clause groups all the IDs by Fund Strategy for the funds specified within "for", and counts the number of IDs in those groups.
To put this into an example:
What is the number of ETFs by strategy?
get(count(group(ID, FUND_STRATEGY))) for (filter(FundsUniv(['Primary','Active']), FUND_TYP=='ETF'))
#N/A Requesting Data...  |  count(group(ID,FUND_STRATEGY))
Aggregate  |  210
Aggressive Allocation  |  15
Agriculture  |  12
Bank Loans  |  13
Bear Market  |  12
Blend  |  3409
Broad Based  |  41
CTA/Managed Futures  |  5
Conservative Allocation  |  17
Convertible  |  8
Corporate  |  305
Currency  |  43
Currency Focused  |  6
Derivative  |  34
Dynamic Allocation  |  46
Energy  |  44
Enhanced MMKT  |  1
Equity Hedge  |  22
Event Driven  |  4
Fixed Income Directional  |  2
General MMKT  |  22
Global  |  1
Global Allocation  |  14
Government  |  366
Government and Agency  |  1
Growth  |  351
Industrial Metals  |  4
Inflation Protected  |  43
Macro  |  1
Moderate Allocation  |  13
Mortgage Backed  |  8
Multi-Strategy  |  9
Municipal  |  41
NullGroup  |  44
Physical Assets and Securities  |  2
Precious Metals  |  98
Preferred  |  35
Specialty  |  17
Value  |  225

## Risk Return Metrics
Field  |  Field Description  |  Parameters
Return_Series  |  Time series of returns  |  Calc_Interval(range),Per(default 'D'), Currency(default local)
Total_Return  |  Holding Period Return  |  Calc_Interval(Date), Currency(default local)
Ann_Tot_Return  |  Annualized Holding Per Return  |  Calc_Interval(Date), Currency(default local)
Volatility  |  Standard Dev of Returns  |  Calc_Interval(date), Per(default 'D'), Currency(default local), Ann_Factor
Sharpe_Ratio  |  Returns-Riskfree/Std Returns  |  Calc_Interval(range), Per(default 'D'), Currency(default local), Ann_Factor, Risk_Free_Ticker
Sortino_Ratio  |  Returns-Riskfree/DownsideVol  |  Calc_Interval(range), Per(default 'D'), Currency(default local), Ann_Factor, Target_Return
Downside_Volatility  |  Std Returns below Target  |  Calc_Interval(range), Per(default 'D'), Currency(default local), Ann_Factor, Target_Return

## Fund Fields
Field Description  |  Field Definition
FUND_NET_ASSET_VAL  |  Net Asset Value (NAV)  |  Net Asset Value (NAV).  Determined by subtracting the liabilities from the portfolio value of the fund's securities, and dividing that figure by the number of outstanding shares. NAV is a per share value. The NAV is the value at which an investor buys and sells shares of a mutual fund.
Values are reported to Bloomberg by a variety of sources, including but not limited to fund companies, transfer agents, official documents, third parties, and other pricing sources.
The pricing source of a fund is stored in Fund Pricing Source (FD046, FUND_PRICING_SOURCE).
Open-End and Hedge Funds:
Returns the net asset value (NAV). If no NAV is available, the bid is returned. If no bid is available, the ask is returned.
Korean non-ETFs:
NAVs are displayed in thousands.
FUND_TOTAL_ASSETS  |  Fund Total Assets  |  Total amount of money invested in the fund, including cash and securities.
Values are reported to Bloomberg by a variety of sources, including but not limited to fund companies, transfer agents, official documents, third parties, and other pricing sources.
When retrieving historic values, the data will be returned in the currency as noted in Total Assets Currency (FD053, FUND_TOTAL_ASSETS_CRNCY) unless a different currency is specified in the history formula.
Display:
This field is displayed in millions (i.e., $10,000,000 is displayed as 10).
The associated currency of this field is stored in Total Assets Currency (FD053, FUND_TOTAL_ASSETS_CRNCY).
The displayed value is effective as of the date stored in Total Assets Date (FD054, FUND_TOTAL_ASSETS_DT).
Korean Mutual Funds:
Fund Total Assets (FD004, FUND_TOTAL_ASSETS) can be found under 'primary fund'. Korean 'Class funds' only display the Class Assets (FD055, FUND_CLASS_ASSETS).
FUND_MANAGEMENT_CO  |  Management Company  |  Company responsible for the management of the fund. Also referred to as an asset management company or investment company.
FUND_BENCHMARK_PRIM  |  Fund Benchmark Primary  |  Ticker of the fund's primary benchmark, as defined by the fund company or documentation. A fund's primary benchmark will typically represent the broader market of the fund.
For funds which aim to track multiple benchmarks, additional benchmark tickers are stored in Fund Benchmark Secondary (FD049, FUND_BENCHMARK_SECONDARY) and Fund Benchmark Third (FD050, FUND_BENCHMARK_THIRD).
FUND_OBJECTIVE_LONG  |  Fund Objective  |  Objective determined by Bloomberg's classification system. The objective is an aggregated value based off of the combination of Bloomberg Classifications. These classifications are interpreted from the language in the fund's prospectus.
FUND_RTG_CLASS_FOCUS  |  Rating Class Focus  |  States the quality rating of the debt securities the fund will invest in as stated in the prospectus; for funds with an asset classification of debt.
FUND_MKT_CAP_FOCUS  |  Market Cap Focus  |  Market capitalization of equity securities the fund will target for investment as stated in the prospectus.
This field is supported for funds with Asset Class Focus (FD121, FUND_ASSET_CLASS_FOCUS) = Equity
FUND_STRATEGY  |  Strategy  |  Investment strategy the fund focuses on for investment opportunities as stated in the prospectus or offering memorandum.
FUND_MGMT_STYLE  |  Management Style  |  The investment strategy the manager implements for investment decisions as stated in the prospectus.
FUND_TYP  |  Fund Type  |  Description of a product designation provided by the fund company through a regulatory filing or prospectus.
Possible Values:
SICAV (Societe d'Investissement a Capital Variable); Unit Trust; FCP (Fond Commun de Placement); UCIT (Undertakings For Collective Investment In Transferable Securities); Open-End Fund; OEIC (Open-End Investment Company); Open-End Pension; SICAF (Societe d'Investissement a Capital Fixe); Trust Units; Investment Trust; Closed-End Fund; Closed-End Pension; Hedge Fund; Fund of Funds; Fund of Hedge Funds; UIT (Unit Investment Trust); ETF (Exchange Traded Fund); ETC (Exchange Traded Commodity); ETN (Exchange Traded Notes); Variable Annuity; Private Equity Fund; Private Equity Fund of Fund; FIDC (Fundo de Investimento em Direitos Creditorios); Funds of FIDCs.
FUND_DOMICILE_TYP  |  Domicile Type  |  Specifies if the fund is domiciled in an off-shore tax haven, or if it is a domestic fund in a non-tax haven country.
FUND_GEO_FOCUS  |  Geographic Focus  |  Geographic area of focus the fund intends to invest in as stated in the prospectus. The classification selections include region, country and state.
FUND_ASSET_CLASS_FOCUS  |  Asset Class Focus  |  Broad asset class that the fund intends to invest in. An asset class is a grouping of investments that exhibit similar characteristics and are subject to the same laws and regulations. This focus is interpreted from the fund's prospectus.
Possible Values:
Equity; Fixed Income; Mixed Allocation; Money Market; Real Estate; Commodity; Specialty; Private Equity; Alternative.
The field returns the asset class focus as defined by the fund company. Holdings Based Asset Class Focus (FD326, HB_ASSET_CLASS_FOCUS) returns the asset class focus calculated based off of the reported portfolio holdings of the fund.
FUND_MATURITY_BAND_FOCUS  |  Maturity Band Focus  |  This refers to the time range that the principal amount of a debt instrument in a fund becomes due as stated in the prospectus. This is for funds with an asset classification of debt.
FUND_INDUSTRY_FOCUS  |  Fund Industry Focus  |  This is the industry (sector) the fund targets for investment as stated in the prospectus.
FUND_OPEN_INVESTOR_SHR  |  Open-end Investor Share Type  |  This identifies the type of investor that will be allowed to invest in the fund.
FUND_LEVERAGE_TYPE  |  Leverage Type  |  Indicates the type of leverage.
Exchange Traded Products (ETPs):
Leveraged funds are those that seek to achieve a daily return that is a multiple of, or inverse of, the daily return of their associated index. Possible values are Long and Short.
Closed-End Funds (CEFs):
Leverage refers to a process by which fund managers issue senior securities or borrow money to potentially enhance yields and returns to investors. Possible values are Preferred Assets, Short-term debt and Other.
This field is actively maintained and supported for ETPs, globally, as well as U.S. and U.K. CEFs.
MGR_COUNTRY_NAME  |  Manager Location - Country or Territory  |  Specifies the country or territory where the fund manager resides. This is a fund-specific field.
MGR_CITY_NAME  |  Manager Location - City  |  City where fund manager resides. This is a fund-specific field.
ACTIVELY_MANAGED  |  Fund Actively Managed  |  Indicates if the fund employs some form of active management.
Returns 'Yes' if a fund seeks to outperform the benchmark or does not seek to track a benchmark; and 'No' if a fund is attempting to replicate the returns of an index, according to the investment strategies and objectives of the prospectus.
INDEX_WEIGHTING_METHODOLOGY  |  Index Weighting Methodology  |  Funds:
Process the Exchange Traded Fund (ETF) (or other Exchange Traded Product (ETP)) uses to weight the holdings of each security in the underlying portfolio based on predetermined criteria.
Possible selections include:
Dividend - Holdings are weighted based on their dividend yield.
Duration - Holdings are weighted by their duration characteristics.
Equal - Each security in the holdings is given the same weighting in the ETF.
Fundamentals - Holdings are weighted based on one or many fundamental factors. (i.e., Price/Book, Price/Earnings ratios)
Market Cap - Each security in the holdings is weighted according to its market capitalization. For fixed income funds it may also be based on size of debt outstanding.
Multi Factor - Holdings are weighted based on more than one specific characteristic.
Proprietary - Unique methodology used by the fund. May be undisclosed.
Single Asset- For ETFs that hold physical commodities. Also applies to Funds/ETPs that track the performance of a single underlying security, at par, leveraged, or inverse.
Price - Each security in the holdingsmakes up a fraction of the ETF, proportional to its trading price.
Indices:
Methodology for which underlying securities are assigned shares/weights within the index, i.e. price weight, capital weight, etc.
REPLICATION_STRATEGY  |  Replication Strategy  |  Represents whether this is an Exchange Traded Fund (ETF) that tracks its index. Possible values are Full, Optimized, Derivative, Blend.
A 90% threshold based on (Count of ETF Holdings also in the index) / (Count of Index Members) is used to determine whether an ETF maintains a full or optimized replication strategy.
Full: ETF holds 90% or more members of the index.
Optimized: ETF holds a representative sample of the index that with less than 90% of members of the index.
Derivative: returns if the ETF uses swaps or futures to synthetically replicate the index return.
Blend: returns if the ETF uses a combination of derivatives and index members.
Actively Managed: this fund is actively managed. It does not specifically track a single underlying index but may be managed with consideration to one or more reference benchmark indices.
ECONOMIC_ASSOCIATION  |  Economic Association  |  Attributes that are applicable to funds with a prospectus stated investment strategy of emerging markets, emerging markets local currency or developed markets.
