---
name: bloomberg
description: >
  Query Bloomberg market data using BQL (Bloomberg Query Language).
  Use this skill whenever the user wants to pull prices, fundamentals,
  time series, reference data, or run BQL queries against Bloomberg — whether they say
  "get me AAPL data", "pull the last year of prices for...", "fetch Bloomberg fundamentals",
  "run a BQL query", "get historical prices from Bloomberg", "screen the S&P 500",
  or anything involving live or historical Bloomberg data. Also trigger when the user
  asks to chart, analyze, or process data that would come from Bloomberg.
---

# Bloomberg BQL

Query Bloomberg market data via the `bql_query` MCP tool. The Bloomberg terminal
must be running and logged in.

## Workflow

1. **Check examples first** — call `bql_examples` with the relevant domain to see verified syntax
2. **Read the reference file** — for complex queries, read the appropriate reference doc (see Quick Dispatch below)
3. **Run the query** — call `bql_query` with your BQL string
4. **Iterate if needed** — if a query errors, read the error + hints, fix, and retry

## IMPORTANT: Read Reference Files Before Writing BQL

The `references/` directory contains verified BQL syntax for every domain.
**Always read the relevant reference file before writing a query.**
Do not guess at field names or parameter names — the BQL API is strict and
will reject queries with wrong parameter names silently or with cryptic errors.

### Quick Dispatch

| Query About | Read This Reference |
|-------------|-------------------|
| Stock prices, volumes, market data, equity screens | `references/equity/market.md` |
| EPS, PE, margins, ratios, peer analysis | `references/equity/fundamental.md` |
| Bond yield, spread, duration, DV01, YAS analytics | `references/fixed-income/bonds.md` |
| Portfolio (PORT) BQL queries, holdings, weights | `references/fixed-income/portfolio.md` |
| bondsuniv, debtUniv, loansUniv, FI screening | `references/fixed-income/universe-screening.md` |
| Structured products, FISP, relative value | `references/fixed-income/structured.md` |
| Credit ratings, rating() data model | `references/credit/ratings.md` |
| CDS spreads, CDS indices, credit default swaps | `references/credit/cds.md` |
| Market sizing, issuance trends, issuer financials | `references/credit/issuance.md` |
| Total return, cross-asset returns | `references/returns/returns.md` |
| Sovereign curves, BVAL, HSA, issuer curves | `references/curves/curves.md` |
| Fund screening, NAV, risk/return metrics | `references/funds/funds.md` |
| Agency CMBS price/yield/spread/DM analytics | `references/securitized/cmbs-analytics.md` |
| TRACE trades, spreads, aggregations | `references/securitized/trades-spreads.md` |
| BQL functions (groupAvg, cumProd, rolling, etc.) | `references/functions/functions.md` |

---

## BQL Quick Patterns (VERIFIED)

### Equity
```
get(px_last, pe_ratio, cur_mkt_cap) for('AAPL US Equity')

get(name, px_last, pe_ratio, cur_mkt_cap/1B)
for(filter(members('SPX Index'), pe_ratio<20 and cur_mkt_cap>10B))

get(px_last(dates=range(-1Y,0D))) for('AAPL US Equity') with(frq=d, fill=prev)

for(top(members('INDU Index'), 10, CUR_MKT_CAP)) get(name, cur_mkt_cap/1B, pe_ratio)

get(is_eps(fa_period_type=A, fa_period_offset=range(-4,2))) for('AAPL US Equity')

get(groupavg(pe_ratio, gics_sector_name)) for(members('SPX Index'))
```

### Fixed Income (VERIFIED — correct parameter names)
```
# Single bond analytics — use yield_type, duration_type, spread_type (NOT just 'type')
get(name, cpn, maturity, yield(yield_type=YTW), duration(duration_type=modified), spread(spread_type=OAS))
for('EH469710 Corp')

# Bond universe screen — bondsuniv must be lowercase, no named params
get(name, cpn, maturity, yield(yield_type=YTW), duration(duration_type=modified), rating(source=SP))
for(filter(bondsuniv(Active),
    crncy == 'USD' and
    duration(duration_type=modified) < 5 and
    rating(source=SP).source_scale <= 10))

# CRITICAL: bondsuniv(Active) — lowercase, positional arg only
# CRITICAL: yield_type=YTW, duration_type=modified, spread_type=OAS — full param names
# CRITICAL: Rating filter uses .source_scale numeric, NOT string >= 'BBB-'
#   Scale: 1=AAA, 2=AA+, 3=AA, 4=AA-, 5=A+, 6=A, 7=A-, 8=BBB+, 9=BBB, 10=BBB-

# Issuer debt chain
get(name, cpn, maturity, amt_outstanding) for(bonds('AAPL US Equity'))
```

### CDS
```
get(cds_spread) for(cds('JPM US Equity', tenor=5Y))
get(cds_spread(dates=range(-30D,0D))) for(cds('JPM US Equity', tenor=5Y))
```

### Returns
```
get(total_return(calc_interval=range(-1M,0D))) for('AAPL US Equity')
get(return_series(calc_interval=range(-1M,0D), per=W)) for('AAPL US Equity')
```

### Curves
```
get(id) for(curveMembers(['YCGT0025 Index']))
get(id().tenor, rate(side=Mid).value) for(curveMembers(['YCGT0025 Index'], tenors='5Y'))
```

### Funds
```
get(count(group(id, fund_typ))) for(fundsUniv(['Primary','Active']))
```

---

## Security Identifier Formats

```
AAPL US Equity     # Equity — ticker + exchange code + asset class
SPX Index          # Index
CL1 Comdty         # WTI front-month futures
EURUSD Curncy      # FX rate
US912810 Govt      # US Treasury
EH469710 Corp      # Corporate bond
```

Asset class suffix is required: `Equity`, `Index`, `Comdty`, `Curncy`, `Corp`, `Govt`, `Mtge`.

---

## Common Bloomberg Fields

### Equity
```
PX_LAST, PX_BID, PX_ASK, PX_VOLUME
CUR_MKT_CAP, PE_RATIO, EV_TO_EBITDA
SALES_REV_TURN, EBITDA, NET_INCOME, IS_EPS
GROSS_MARGIN, OPER_MARGIN, RETURN_COM_EQY
GICS_SECTOR_NAME, NAME, CRNCY, ID_ISIN
```

---

## Anti-Patterns to Avoid

| Wrong | Correct | Why |
|-------|---------|-----|
| `yield(type=ytw)` | `yield(yield_type=YTW)` | `type` is not a valid parameter |
| `duration(type=modified)` | `duration(duration_type=modified)` | Full param name required |
| `spread(type=oas)` | `spread(spread_type=OAS)` | Full param name required |
| `bondsUniv(COUNTRY='US')` | `bondsuniv(Active)` + filter | Named params error; use filter() |
| `rating(source=SP) >= 'AA-'` | `rating(source=SP).source_scale <= 4` | String comparison doesn't work |
| Guessing at BQL syntax | Read reference files first | References are verified against live Bloomberg |
