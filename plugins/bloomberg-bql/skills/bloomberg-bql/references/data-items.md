# BQL Data Items — Complete Reference by Asset Class

## Equity — Price & Market
```
PX_LAST                              last price
PX_BID / PX_ASK                      bid / ask
PX_VOLUME                            daily volume
CUR_MKT_CAP(currency=USD)            market cap
DAY_TO_DAY_TOTAL_RETURN              daily total return
EQY_SH_OUT                           shares outstanding
OPEN_INT                             open interest (options)
```

## Equity — Fundamentals
```
IS_EPS(fpt, fpo, fpr, ae)            EPS (see period params)
PE_RATIO                             P/E (LTM default)
SALES_REV_TURN                       revenue
GROSS_PROFIT / GROSS_MARGIN
EBIT / EBITDA / NET_INCOME
OPER_MARGIN / PROF_MARGIN / EBITDA_TO_REVENUE / FREE_CASH_FLOW_MARGIN
CF_CASH_FROM_OPER / CF_FREE_CASH_FLOW / CAPITAL_EXPEND
ENTERPRISE_VALUE
EV_TO_EBITDA / EV_TO_SALES / EV_TO_EBIT
RETURN_COM_EQY / RETURN_ON_ASSET / ASSET_TURNOVER
CUR_RATIO / CASH_RATIO / ALTMAN_Z_SCORE
TOT_DEBT_TO_EBITDA / NET_DEBT_TO_EBITDA / TOT_DEBT_TO_TOT_CAP / EBITDA_TO_TOT_INT_EXP
LT_DEBT_TO_TOT_ASSET / FCF_TO_TOTAL_DEBT
BS_CASH_NEAR_CASH_ITEM / CASH_AND_ST_INVESTMENTS / SHORT_AND_LONG_TERM_DEBT
SALES_5YR_AVG_GR / EPS_GROWTH
NUM_OF_EMPLOYEES
```

## Equity — Classification
```
NAME / LONG_COMP_NAME
GICS_SECTOR_NAME / GICS_INDUSTRY_NAME / GICS_SUB_INDUSTRY_NAME
BICS_LEVEL_1_SECTOR_NAME
CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BICS, classification_level=2)
CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS, classification_level=3)  # FI
CNTRY_OF_RISK / COUNTRY_FULL_NAME
SECURITY_TYP                        "Common Stock", etc.
PRIMARY_EXCHANGE_NAME
INDUSTRY_SECTOR
```

## Fixed Income — Analytics
```
YIELD(YIELD_TYPE=YTW)
  # Types: YTW YTM YTC YTP CON CUR AVL SAVL TAX_EQUIVALENT
  # Params: SIDE PRICING_SOURCE DATES PRICE

SPREAD(SPREAD_TYPE='OAS')
  # Types: Z I OAS N E J A P R ZV_OAS BMK ASW G
  # Params: SIDE PRICING_SOURCE DATES CURRENCY (XCCY) CURVE_ID FORWARD_CURVE_ID DISCOUNT_CURVE_ID YIELD PRICE WORKOUT

DURATION(DURATION_TYPE=MODIFIED)
  # Types: SPREAD MODIFIED MACAULAY EFFECTIVE
  # Params: SIDE PRICING_SOURCE DATES PRICE YIELD YIELD_TYPE

CONVEXITY(SIDE=MID)             # Params: SIDE PRICING_SOURCE DATES PRICE YIELD
RISK                            # DV01 × 100
DV01                            # dollar value of a basis point
KRD(TENOR=5Y)                   # key rate duration (Treasury): 6M 1Y 2Y 3Y 5Y 7Y 10Y 20Y 30Y
S_KRD(TENOR=5Y)                 # key rate duration (swap curve)
KEY_RATE_DUR_6MO / _1YR / _2YR / _5YR / _10YR / _30YR   # securitized

TOTAL_RETURN(CALC_INTERVAL=Range(-3M,0D), DISPLAY_RETURNS='Percent')
  # RETURN_TYPE: TOTAL PRICE CPN PAYDOWN
  # REINVESTMENT_TYPE: None Fixed Mmkt
  # CALC_INTERVAL shortcuts: 1D MTD QTD YTD

RETURN_SERIES(CALC_INTERVAL=range(-1Y,0D), PER=M)   # period-over-period returns

CASHFLOWS                       # projected cashflow schedule
  # Params: settle_dt workout_date yield_flag trade_date workout_price face_amount

PRICE                           # clean price (or custom analytics price)
```

## Fixed Income — YAS Custom Analytics
```
PRICE(YIELD=5, DATES=2023-09-01)
PRICE(SPREAD=250, SPREAD_TYPE='OAS', DATES=2023-09-01)
PRICE(SPREAD=150, SPREAD_TYPE='I', CURVE_ID='S42', DATES=2023-09-01)
YIELD(PRICE=115)
YIELD(WORKOUT_PRICE=100, WORKOUT_DATE=2025-10-25, DATES=2023-09-01)
SPREAD(SPREAD_TYPE='OAS', PRICE=103, DATES=2023-09-01)
SPREAD(CURRENCY=EUR)                # cross-currency Z-spread
SPREAD(CURRENCY=CAD, SPREAD_TYPE='BMK')
DURATION(DURATION_TYPE=MODIFIED, PRICE=110, DATES=2023-09-01)
DURATION(DURATION_TYPE=MACAULAY, YIELD=4, DATES=2023-09-01)
DV01(PRICE=90, DATES=2023-09-01)
RISK(YIELD=5, YIELD_TYPE=YTM, DATES=2023-09-01)
CONVEXITY(PRICE=90, DATES=2023-09-01)
# YAS spread types: Z BMK OAS G I ASW
# CURVE_ID format: 'S42' (from CRVF<GO>)
```

## Fixed Income — Reference Data
```
CPN / CPN_TYP
MATURITY / MATURITY_YEARS / ISSUE_DT
AMT_OUTSTANDING(currency=USD) / AMT_ISSUED(currency=USD)
CRNCY
PAYMENT_RANK                    Sr Unsecured, Subordinated, etc.
ID_ISIN / TICKER
CALLABLE
SENIORITY / MARKET_CLASSIFICATION
CREDIT_RATING / CREDIT_RATING_GRADE_INDICATOR
BB_COMPOSITE  → use rating(source=BBG)
RTG_SP        → use rating(source=SP)
RTG_SP_INITIAL / RTG_MDY_INITIAL / RTG_FITCH_INITIAL  # at issuance
CLASSIFICATION_NAME(CLASSIFICATION_SCHEME=BCLASS, classification_level=3)
SPREAD_TYPE / SECURITY_PRICING_DATE
```

## Credit Ratings (rating() data model)
```
rating()                                     # default: LT then ST waterfall
rating(source=SP)                            # S&P
rating(source=MOODY)                         # Moody's
rating(source=FITCH)                         # Fitch
rating(source=BBG)                           # Bloomberg composite
rating(source=SP, type=ISSUE, dates=range(-1y,0d))   # historical

# Sources: SP MOODY FITCH AMBEST BBG CHENGXIN CHINA_LOCAL FELLER FIX_SCR ICRA KOREA LIANHE NICE PEFINDO KIS SBCR RI DBRS JCR
# horizon: Waterfall(default) ST LT
# currency: FC LC ALL
# debt_category: SENIOR_UNSECURED SUBORDINATED FINANCIAL_STRENGTH PREFERRED BANK_DEPOSITS CORPORATE_FAMILY SENIOR_SECURED
# type: issue(default for Corps/Govts) issuer

# Metadata access
#rating().BASE_RATING      # rating string without watch indicator
#rating().WATCH            # CreditWatch/Outlook status
#rating().EFFECTIVE_DATE   # when rating was assigned
```

## CDS
```
CDS_SPREAD(side=mid, pricing_source=CBIN)    # mid/bid/ask
RSK_BB_IMPLIED_CDS_SPREAD(dates=-1d, fill=prev)
CDS_TENOR / CDS_RED_PAIR_ID

# Pricing sources: CBBT CBIL CBIN CBIT CBGL CBGN CBGT PRXY BEST DRSK
# CDS indices: ITRXEXE IBOXUMAE IBOXHYAE ITRXESE
# term structure via let() + value() + mapby=lineage — see example-queries.md
```

## Funds
```
FUND_NET_ASSET_VAL              NAV
FUND_TOTAL_ASSETS               AUM
FUND_MANAGEMENT_CO
FUND_BENCHMARK_PRIM
FUND_OBJECTIVE_LONG
FUND_TYP                        ETF, Open-End Fund, UCIT
FUND_MGMT_STYLE                 Active, Passive
FUND_GEO_FOCUS / FUND_ASSET_CLASS_FOCUS / FUND_INDUSTRY_FOCUS
FUND_RTG_CLASS_FOCUS            High Yield, Investment Grade
FUND_MKT_CAP_FOCUS              Large-cap, Mid-cap, Small-cap
FUND_STRATEGY
FUND_DOMICILE_TYP / FUND_LEVERAGE_TYPE / FUND_MATURITY_BAND_FOCUS
MGR_COUNTRY_NAME
ACTIVELY_MANAGED / INDEX_WEIGHTING_METHODOLOGY / REPLICATION_STRATEGY
```

## Portfolio
```
id().weights     # security weights (Fixed Weight or Shares/Par portfolios)
id().positions   # security positions (Drifting Weight portfolios)
```

## Mortgage / Securitized
```
MTG_WAL / MTG_FACTOR / MTG_ORIG_AMT
MTG_LTV_WAVG / MTG_DSCR_WAVG / MTG_WHLN_WALA
MTG_DEAL_TYP / MTG_TYP / MTG_WAC
MTG_STATIC_MOD_DUR / MTG_PREPAY_SPEED / MTG_PREPAY_TYP
MTG_DELINQUENCIES_PCT / MTG_CASH_FLOW / HIST_CASH_FLOW / EXTENDED_CASH_FLOW
MTG_HIST_FACT / MTG_HIST_CPN / HISTORICAL_CREDIT_SUPPORT
STRUCTURED_PROD_ASSET_CLASS      AUTO, etc.
STRUCTURED_PROD_CLASS_AST_SUBCL  CREDIT_RISK_TRANSFER, etc.
FIRST_LOSS_DATE / MTG_PRINC_WIN

# Key rate durations for securitized
KEY_RATE_DUR_6MO / KEY_RATE_DUR_1YR / KEY_RATE_DUR_2YR
KEY_RATE_DUR_5YR / KEY_RATE_DUR_10YR / KEY_RATE_DUR_30YR
```

## TRACE Trade Data (Securitized)
```
TRADE_DATA(source=TRACE)
TRADE_DATA(source=TRACE, dates=range(-30d,0d),
           scenario=PX, workout=TO_WORST, view=MTGE_ANALYTICS)

# Scenarios: MED H1M H3M H6M BAM BTM PX(default) CF CONTRIBUTED
# Workout: TO_WORST(default) TO_CALL TO_MATURITY
# Views:
#   STANDARD        → ID PRICE DATE TIME VOLUME SETTLE_DATE CURRENCY CONDITION_CODE
#   MTGE_ANALYTICS  → adds ADJUSTED_VOLUME YIELD I_SPREAD DISCOUNT_MARGIN WAL WORKOUT SCENARIO PREPAY_SPEED PREPAY_TYPE
#   MTGE_EXTENDED   → adds Z_SPREAD E_SPREAD N_SPREAD P_SPREAD R_SPREAD J_SPREAD
```

## New Issuance Analytics
```
ISSUANCE_PRICING(STAGE=IPT)           initial price talk
ACTIVE_BOOKRUNNERS
BOOK_SIZE
COVER_RATIO_FOR_INITIAL_ISSUANCE
NEW_ISSUE_COMPRESSION                 IPT to pricing compression
```

## FI Market / Issuer Financials
```
# Corporate leverage
TOT_DEBT_TO_EBITDA / NET_DEBT_TO_EBITDA / TOT_DEBT_TO_TOT_CAP
EBITDA_TO_TOT_INT_EXP / FREE_CASH_FLOW_MARGIN / ALTMAN_Z_SCORE

# Financial institutions
NET_INT_MARGIN / EFF_RATIO / TOT_LOAN_TO_TOT_DPST / TEXAS_RATIO / NPLS_TO_TOTAL_LOANS

# Numeric shorthand
/1M  → ÷1,000,000    /1B  → ÷1,000,000,000
5Y   → 5 years fwd    -3M → 3 months back    0D → today
```
