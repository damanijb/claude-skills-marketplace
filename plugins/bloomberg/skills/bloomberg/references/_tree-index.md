# BQL Reference Tree -- Navigation Index

Read this file first to find the right reference for your query domain.

## Quick Dispatch

| If you need...                                          | Read this file                              |
|---------------------------------------------------------|---------------------------------------------|
| Stock prices, volumes, market cap, equity screening     | `equity/market.md`                          |
| EPS, PE, margins, ratios, peer group analysis           | `equity/fundamental.md`                     |
| Bond yield, spread, duration, DV01, YAS custom analytics| `fixed-income/bonds.md`                     |
| Portfolio (PORT) BQL queries, holdings, weights         | `fixed-income/portfolio.md`                 |
| bondsUniv, debtUniv, loansUniv, FI screening/SRCH       | `fixed-income/universe-screening.md`        |
| Structured products (FISP), ABS, relative value         | `fixed-income/structured.md`                |
| Credit ratings, rating() data model                     | `credit/ratings.md`                         |
| CDS spreads, CDS indices, credit default swaps          | `credit/cds.md`                             |
| Market sizing, issuance trends, issuer financials       | `credit/issuance.md`                        |
| Total return, cross-asset returns, return series        | `returns/returns.md`                        |
| Sovereign curves, BVAL, HSA, custom, issuer curves      | `curves/curves.md`                          |
| Fund screening, NAV, risk/return metrics                | `funds/funds.md`                            |
| Agency CMBS analytics (price, yield, spread, DM)        | `securitized/cmbs-analytics.md`             |
| TRACE trades, spreads, aggregations                     | `securitized/trades-spreads.md`             |
| BQL functions (groupAvg, cumProd, rolling, filter, etc.)| `functions/functions.md`                    |
| Find a BQL field mnemonic by keyword                    | `field-search.md`                           |

## Domain Tree

```
references/
+-- equity/
|   +-- market.md              Prices, volumes, market cap, shares, basic screening
|   +-- fundamental.md         EPS, PE, margins, ratios, peer analysis, custom ratios
|
+-- fixed-income/
|   +-- bonds.md               Bond analytics + YAS custom price/yield/spread/duration
|   +-- portfolio.md           PORT queries for equity & FI portfolios
|   +-- universe-screening.md  bondsUniv, debtUniv, loansUniv, SRCH filter patterns
|   +-- structured.md          FISP structured products, relative value, ABS
|
+-- credit/
|   +-- ratings.md             rating() data model, basic & advanced examples
|   +-- cds.md                 CDS single names, indices, membership, use cases
|   +-- issuance.md            Market sizing, issuance trends, issuer financials
|
+-- returns/
|   +-- returns.md             Total return, cross-asset, return series analysis
|
+-- curves/
|   +-- curves.md              Sovereign, zero, custom, BVAL, HSA, issuer curves
|
+-- funds/
|   +-- funds.md               Fund screening, aggregation, risk/return metrics
|
+-- securitized/
|   +-- cmbs-analytics.md      Agency CMBS price/yield/spread/DM analytics
|   +-- trades-spreads.md      TRACE trades, spreads, aggregations
|
+-- functions/
|   +-- functions.md           All BQL functions: arithmetic, stats, grouping, time series
|
+-- field-search.md            How to discover BQL data items & field mnemonics
```

## Source Workbooks

| Workbook | Domain | Target Reference |
|----------|--------|-----------------|
| 2089580.xlsx | BQL Functions | functions/functions.md |
| 2085678.xlsx | Equity Quick Start | equity/market.md + equity/fundamental.md |
| 2098844.xlsx | Fixed Income | fixed-income/bonds.md |
| 2139460.xlsx | YAS Custom Analytics | fixed-income/bonds.md (appended) |
| 2096050.xlsx | Returns Analysis | returns/returns.md |
| 2142562.xlsx | Credit Ratings | credit/ratings.md |
| 2088954.xlsx | Funds | funds/funds.md |
| 2090418.xlsx | Portfolio (PORT) | fixed-income/portfolio.md |
| 2097527.xlsx | CDS | credit/cds.md |
| 2098358.xlsx | Curves | curves/curves.md |
| 2098648.xlsx | Structured Products | fixed-income/structured.md |
| 2148204.xlsx | Issuance & Market Sizing | credit/issuance.md |
| 2168185.xlsm | Agency CMBS | securitized/cmbs-analytics.md |
| 2171225.xlsm | TRACE Trades | securitized/trades-spreads.md |
