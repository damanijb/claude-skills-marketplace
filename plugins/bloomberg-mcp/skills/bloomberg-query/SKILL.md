---
name: bloomberg-query
description: Generate and execute Bloomberg queries — BDP, BDH, BDIB, BQL, bond analytics, screening, field search, and charting. Use when the user asks for financial data, market prices, historical data, bond analytics, security screening, or any Bloomberg Terminal data. Triggers on mentions of tickers, securities, BQL, Bloomberg, financial data, market data, yield, spread, duration, or portfolio analytics.
version: 1.0.0
metadata:
  filePattern: "**/bloomberg*/**"
  bashPattern: "bloomberg|blpapi|xbbg|bql"
---

# Bloomberg Query Generation

You have access to 10 Bloomberg MCP tools. This skill teaches you how to use them effectively.

## Available Tools

| Tool | Purpose | Requires Terminal |
|------|---------|-------------------|
| `bloomberg_status` | Check connectivity | Yes |
| `bloomberg_bdp` | Reference/snapshot data (current values) | Yes |
| `bloomberg_bdh` | Historical time series | Yes |
| `bloomberg_bdib` | Intraday bar data (OHLCV) | Yes |
| `bloomberg_bql` | Bloomberg Query Language (most powerful) | Yes |
| `bloomberg_bql_build` | Natural language → BQL template | No |
| `bloomberg_bond_info` | Fixed income analytics | Yes |
| `bloomberg_screen` | Security screening (saved or ad-hoc) | Yes |
| `bloomberg_field_search` | Discover field mnemonics | Yes |
| `bloomberg_chart` | Generate charts from data | No |

## Tool Selection Guide

**"What's the current price of X?"** → `bloomberg_bdp`
**"Show me prices over the last year"** → `bloomberg_bdh`
**"5-minute bars for today"** → `bloomberg_bdib`
**"Screen for bonds where..."** → `bloomberg_bql` or `bloomberg_screen`
**"What fields exist for..."** → `bloomberg_field_search`
**"Bond yield, duration, spread"** → `bloomberg_bond_info`
**"Chart the results"** → `bloomberg_chart` (after fetching data)
**Complex multi-entity queries** → `bloomberg_bql`

## Ticker Format

Bloomberg tickers follow this format: `{IDENTIFIER} {MARKET} {ASSET_CLASS}`

### Common patterns:
- **US Equities**: `AAPL US Equity`, `MSFT US Equity`
- **Indices**: `SPX Index`, `INDU Index`, `NDX Index`
- **US Treasuries**: `T 4.5 05/15/38 Govt`, `CT10 Govt` (generic 10Y)
- **Corporate Bonds**: `AAPL 3.85 08/04/46 Corp`
- **Municipal Bonds**: `CASGEN 5 06/01/48 Muni`
- **ETFs**: `SPY US Equity`, `HYG US Equity`
- **FX**: `EURUSD Curncy`, `USDJPY Curncy`
- **Commodities**: `CL1 Comdty` (WTI front month), `GC1 Comdty` (Gold)
- **By CUSIP**: `/cusip/037833100` (AAPL)
- **By ISIN**: `/isin/US0378331005`

## BDP — Reference Data

For current/snapshot values. Best for: latest price, company info, ratings, static fields.

```
bloomberg_bdp(
  securities=["AAPL US Equity", "MSFT US Equity"],
  fields=["PX_LAST", "SECURITY_NAME", "CUR_MKT_CAP", "PE_RATIO"]
)
```

### Common equity fields:
`PX_LAST`, `PX_OPEN`, `PX_HIGH`, `PX_LOW`, `PX_VOLUME`, `SECURITY_NAME`, `CUR_MKT_CAP`, `PE_RATIO`, `BEST_EPS`, `DVD_YLD_IND`, `RETURN_COM_EQY`, `TOT_DEBT_TO_TOT_EQY`, `GICS_SECTOR_NAME`, `COUNTRY_ISO`

### Common FI fields:
`YLD_YTM_MID`, `OAS_SPREAD_MID`, `Z_SPRD_MID`, `DUR_ADJ_MID`, `CONVEXITY_MID`, `DV01`, `COUPON`, `MATURITY`, `RTG_SP`, `RTG_MOODY`, `RTG_FITCH`, `AMT_OUTSTANDING`, `CRNCY`

### Using overrides:
```
bloomberg_bdp(
  securities=["IBM US Equity"],
  fields=["BEST_EPS"],
  overrides={"BEST_FPERIOD_OVERRIDE": "2025FY"}
)
```

## BDH — Historical Data

For time series. Best for: price history, fundamental trends, total returns.

```
bloomberg_bdh(
  securities=["SPY US Equity"],
  fields=["PX_LAST", "PX_VOLUME"],
  start_date="2024-01-01",
  end_date="2025-01-01",
  periodicity="M"    # D=daily, W=weekly, M=monthly, Q=quarterly, Y=yearly
)
```

### Multi-security comparison:
```
bloomberg_bdh(
  securities=["SPY US Equity", "AGG US Equity", "GLD US Equity"],
  fields=["PX_LAST"],
  start_date="2024-01-01",
  periodicity="W"
)
```

## BDIB — Intraday Bars

For intraday OHLCV. Single security, single day only.

```
bloomberg_bdib(
  security="SPY US Equity",
  date="2026-03-21",
  interval=5,          # minutes per bar
  session="allday"     # or: day, am, pm
)
```

## BQL — Bloomberg Query Language

The most powerful tool. Supports screening, aggregation, time series, cross-entity analytics.

### BQL Syntax Rules (CRITICAL):
1. **Always wrap tickers in brackets**: `for(['AAPL US Equity'])` NOT `for('AAPL US Equity')`
2. **Use == for comparisons**: `crncy=='USD'` NOT `crncy='USD'`
3. **Each let() variable ends with ;**: `let(#x=px_last;) get(#x) for(...)`
4. **Balance all parentheses**
5. **String values use single quotes**: `'USD'`, `'A+'`

### BQL Patterns:

**Single security snapshot:**
```
bloomberg_bql(query="get(px_last, name) for(['AAPL US Equity'])")
```

**Historical time series:**
```
bloomberg_bql(query="get(px_last) for(['SPY US Equity']) with(dates=range(-1Y,0D))")
```

**Index members with data:**
```
bloomberg_bql(query="get(px_last, pe_ratio(), dvd_yld()) for(members(['SPX Index']))")
```

**Bond screening:**
```
bloomberg_bql(query="get(name, yield(), spread(), dur_adj_mid()) for(filter(bondsUniv('active'), crncy=='USD' and rtg_sp() in ['AAA','AA+','AA','AA-','A+','A','A-'] and maturity() > '2030-01-01'))")
```

**Sector aggregation:**
```
bloomberg_bql(query="get(avg(group(pe_ratio(), gics_sector_name()))) for(members(['SPX Index']))")
```

**Fundamentals with period overrides:**
```
bloomberg_bql(query="get(is_eps(fpt=A,fpo=0), sales_rev_turn(fpt=A,fpo=0), ebitda(fpt=A,fpo=0)) for(['AAPL US Equity'])")
```

**Multi-period fundamentals (last 5 years):**
```
bloomberg_bql(query="get(is_eps(fpt=A,fpo=-4), is_eps(fpt=A,fpo=-3), is_eps(fpt=A,fpo=-2), is_eps(fpt=A,fpo=-1), is_eps(fpt=A,fpo=0)) for(['AAPL US Equity'])")
```

**Let() variables for complex queries:**
```
bloomberg_bql(query="let(#ret=return(dates=range(-1Y,0D));#vol=std(#ret)*sqrt(252);) get(#ret,#vol) for(members(['SPX Index']))")
```

### BQL Universe Functions:
- `members(['SPX Index'])` — Index constituents
- `filter(bondsUniv('active'), ...)` — Active bonds with criteria
- `filter(members(['SPX Index']), ...)` — Filtered index members
- `loansUniv('active')` — Active leveraged loans
- `segments('BCLASS3', ['SPX Index'])` — Sector segments

### BQL Date Functions:
- `range(-1Y, 0D)` — Last 1 year to today
- `range(-5Y, 0D)` — Last 5 years
- `range('2020-01-01', '2025-01-01')` — Specific range
- `-1M`, `-1W`, `-1D` — Relative dates

### BQL Aggregate Functions:
- `avg()`, `sum()`, `min()`, `max()`, `median()`, `std()`
- `count()`, `countIf()`
- `group(metric, groupBy)` — Group by category
- `rank()`, `percentile()`

## Bond Info

Shortcut for common fixed income analytics. Returns coupon, maturity, price, yield, risk metrics, and spreads.

```
bloomberg_bond_info(
  securities=["T 4.5 05/15/38 Govt", "AAPL 3.85 08/04/46 Corp"],
  include_risk=true,     # duration, convexity, DV01
  include_spreads=true   # OAS, Z-spread, ASW
)
```

**By CUSIP:**
```
bloomberg_bond_info(securities=["/cusip/912810TD8"])
```

## Screening

**Saved Bloomberg screen (BEQS):**
```
bloomberg_screen(screen_name="MyInvestmentGradeScreen")
```

**Ad-hoc BQL filter:**
```
bloomberg_screen(
  bql_filter="crncy=='USD' and rtg_sp() in ['A+','A','A-'] and maturity()>'2030-01-01'",
  fields=["name", "yield()", "spread()", "dur_adj_mid()"],
  max_results=50
)
```

## Field Search

When you don't know the exact field mnemonic:

```
bloomberg_field_search(query="yield to maturity", max_results=10)
bloomberg_field_search(query="earnings per share")
bloomberg_field_search(query="credit default swap spread")
```

## Charting

After fetching data, generate professional charts:

```
# First fetch data
data = bloomberg_bdh(securities=["SPY US Equity"], fields=["PX_LAST"], start_date="2024-01-01")

# Then chart it
bloomberg_chart(
  chart_type="timeseries",    # timeseries, bar, scatter, heatmap, multipanel, facet
  library="matplotlib",       # matplotlib (PNG) or altair (interactive HTML)
  data_json=data["data"],     # Pass the .data array from any bloomberg result
  title="S&P 500 ETF — 1 Year Performance"
)
```

### Chart types by library:
- **matplotlib**: timeseries, bar, scatter, heatmap, multipanel
- **altair**: timeseries, bar, scatter, facet

## Workflow Patterns

### Equity Research Quick Look
1. `bloomberg_bdp` → current price, P/E, market cap, sector
2. `bloomberg_bdh` → 1Y price history
3. `bloomberg_chart` → timeseries chart
4. `bloomberg_bql` → peer comparison via index members

### Fixed Income Analysis
1. `bloomberg_bond_info` → yield, duration, spreads
2. `bloomberg_screen` → find comparable bonds
3. `bloomberg_bql` → relative value analysis
4. `bloomberg_chart` → spread comparison bar chart

### Portfolio Overview
1. `bloomberg_bdp` → current prices for all holdings
2. `bloomberg_bdh` → historical performance
3. `bloomberg_bql` → sector/rating aggregation
4. `bloomberg_chart` → multipanel performance chart

### Always Check Connectivity First
If any tool returns an error, run `bloomberg_status()` to diagnose. Common issues:
- Terminal not running → start Bloomberg Terminal
- API not connected → restart Terminal, wait for full load
- Missing entitlements → check Bloomberg subscription
