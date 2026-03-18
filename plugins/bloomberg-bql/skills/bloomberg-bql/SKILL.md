---
name: bloomberg-bql
description: Build and execute Bloomberg Query Language (BQL) queries in Python using polars-bloomberg (BQuery). Use this skill when constructing BQL queries for equities, fixed income, portfolios, funds, CDS, or MBS — or when using BQL functions for screening, time series, grouping, or custom analytics.
---

# Bloomberg BQL Skill

## Execution Environment

**Preferred:** `polars-bloomberg` (`BQuery`) in the `sbc` conda environment.
- Works over standard BLPAPI session (port 8194) — no BQuant subscription needed
- Returns Polars DataFrames
- Run scripts via PowerShell: `conda run -n sbc python script.py`

**Alternative:** `cli-anything-wintrv bql run "..."` — requires BQuant subscription.

---

## polars-bloomberg Pattern

```python
from polars_bloomberg import BQuery

with BQuery() as bq:
    # Single snapshot
    df = bq.bdp(["AAPL US Equity", "MSFT US Equity"], ["PX_LAST", "PE_RATIO"])

    # Historical time series (long format: security, date, field)
    df = bq.bdh(["AAPL US Equity"], ["PX_LAST"],
                date(2024, 1, 1), date.today())

    # BQL query → BqlResult
    result = bq.bql("get(px_last, pe_ratio) for(members('SPX Index'))")
    df = result.combine()        # joined DataFrame
    df = result[0]               # first item only
    names = result.names         # ['px_last', 'pe_ratio']
```

**bdh output** → wide pivot for charting:
```python
df_wide = df.pivot(on="security", index="date", values="PX_LAST").sort("date")
```

---

## BQL Query Structure

```
[let(#var = expr;)]   ← optional: reusable variables
get(DataItem(params)) ← what to retrieve
for(universe)         ← which securities
[with(global_params)] ← optional: dates, frq, fill, currency
```

### Quick examples
```
# Snapshot
get(px_last, pe_ratio, cur_mkt_cap/1B) for('AAPL US Equity')

# Index screen
get(name, px_last) for(filter(members('SPX Index'), pe_ratio<20 and cur_mkt_cap>10B))

# Historical (daily, forward-fill)
get(px_last(dates=range(-1Y,0D))) for('AAPL US Equity') with(frq=d, fill=prev)

# Sector aggregation
get(groupAvg(pe_ratio, gics_sector_name)) for(members('SPX Index'))

# Fixed income yield
get(yield(yield_type=YTW), spread(spread_type='OAS'), duration(duration_type=MODIFIED))
for(filter(bondsUniv('Active'), rating(source=SP) in ['A+','A','A-']))

# Portfolio weighted avg
get(groupWAvg(pe_ratio, id.weights))
for(filter(members('PORT_ID', type=PORT), SECURITY_TYP=='Common Stock'))
```

---

## Core Universe Functions

| Function | Description |
|----------|-------------|
| `members('SPX Index')` | Index constituents |
| `members('PORT_ID', type=PORT)` | Portfolio holdings |
| `filter(univ, condition)` | Subset by predicate |
| `top(univ, n, field)` / `bottom(...)` | Top/bottom N |
| `equitiesUniv(['active','primary'])` | All active equities (use `mode=cached`) |
| `fundsUniv(['Primary','Active'])` | All active funds |
| `bondsUniv('Active')` | Active bonds |
| `peers('AAPL US Equity', type=BLOOMBERG_BEST_FIT)` | Peer group |
| `bonds('AAPL US Equity')` | All bonds of issuer |
| `holdings('HYG US Equity')` | Fund holdings |
| `cds('JPM US Equity', tenor=5Y)` | CDS for issuer |
| `union()` / `intersect()` / `setDiff()` | Set operations |

For the full universe function reference, see `references/universe-functions.md`.

---

## Key Global Parameters

```
with(
  dates=range(-1Y,0D),  frq=M,       fill=prev,
  currency=USD,          mode=cached,  side=MID
)
```

**Date shortcuts:** `0d`, `-1d`, `-1m`, `ytd`, `mtd`, `qtd`, `wtd`
**frq values:** `D` `W` `M` `Q` `Y` `SA`

---

## Fundamental Period Parameters

Use with `IS_EPS`, `SALES_REV_TURN`, and other fundamental items.

| Param | Values |
|-------|--------|
| `fpt` | `A` Annual · `Q` Quarterly · `LTM` · `BA` Calendarized Annual · `BT` NTM |
| `fpo` | `0` latest · `-1` prior · `range(-4,0)` · `range(-5,2)` (hist+fcast) |
| `fpr` | `range(2010,2018)` · `range(2017Q1,2018Q4)` · `2017-09-30` |
| `ae`  | `A` actual · `E` estimate · (omit for both) |

```
get(is_eps(fpt=BA, fpo=range(-2,2), ae=A)) for('AAPL US Equity')
```

---

## Common Data Items

### Equity
```
PX_LAST, PX_BID, PX_ASK, PX_VOLUME, CUR_MKT_CAP(currency=USD)
DAY_TO_DAY_TOTAL_RETURN, EQY_SH_OUT
IS_EPS, PE_RATIO, SALES_REV_TURN, EBITDA, NET_INCOME, EV_TO_EBITDA
GROSS_MARGIN, OPER_MARGIN, RETURN_COM_EQY, TOT_DEBT_TO_EBITDA
GICS_SECTOR_NAME, BICS_LEVEL_1_SECTOR_NAME, CNTRY_OF_RISK
```

### Fixed Income
```
YIELD(YIELD_TYPE=YTW)                         # YTW YTM YTC YTP CON CUR
SPREAD(SPREAD_TYPE='OAS')                     # Z I OAS N E J A P R BMK ASW G
DURATION(DURATION_TYPE=MODIFIED)              # SPREAD MODIFIED MACAULAY EFFECTIVE
CONVEXITY, RISK, DV01
KRD(TENOR=5Y), S_KRD(TENOR=5Y)               # key rate durations
TOTAL_RETURN(CALC_INTERVAL=Range(-3M,0D), DISPLAY_RETURNS='Percent')
RETURN_SERIES(CALC_INTERVAL=range(-1Y,0D), PER=M)
CPN, MATURITY, AMT_OUTSTANDING(currency=USD), PAYMENT_RANK, ID_ISIN
rating(source=SP)                             # SP MOODY FITCH AMBEST BBG DBRS
#rating().BASE_RATING, #rating().WATCH, #rating().EFFECTIVE_DATE
```

For the full data item catalog, see `references/data-items.md`.

---

## BQL Functions Quick Reference

### Cross-security grouping
```
groupAvg(pe_ratio, gics_sector_name)     # sector averages
groupWAvg(pe_ratio, id.weights)          # portfolio weighted avg
groupZscore(day_to_day_total_return)     # z-score vs peers
groupSum(eqy_sh_out)                     # total across universe
SUM(GROUP(amt_outstanding(currency=USD)/1B))
```

### Time series
```
cumProd(1+dropNA(day_to_day_total_return(dates=range(-3M,0d))))-1  # cumulative return
pct_chg(cur_mkt_cap), diff(eqy_sh_out)
rolling(avg(px_last(-1m,0d)), iterationdates=range(-1y,0d))
```

### Data handling
```
dropNA(expr)                # remove NaN rows
dropNA(expr, remove_id=true)# also drop the security
avail(expr1, expr2)         # first non-null
matches(series, condition)  # filter parallel series
value(expr, universe)       # evaluate in private universe, project to global
```

For the complete function catalog, see `references/function-reference.md`.

---

## let() Clause

```
let(#var = expression;) get(#var) for(universe)

# Example: cumulative returns
let(#R = return_series(calc_interval=range(-2Y,0d), per=M);
    #Cum = cumProd(dropna(#R)+1)-1;)
get(#Cum) for('BACR0 Index')

# Example: CDS term structure
let(#5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=5Y), mapby=lineage).value;)
get(name, #5Y) for(members('INDU Index'))
```

---

## YAS Custom Analytics

```
get(PRICE(YIELD=5, DATES=2023-09-11)) for(['US25468PBW59'])
get(YIELD(PRICE=115) as #yield) for(['US25468PBW59'])
get(SPREAD(SPREAD_TYPE='OAS', PRICE=103) as #spread) for(['US25468PBW59'])
get(DURATION(DURATION_TYPE=MODIFIED, PRICE=110) as #dur) for(['US25468PBW59'])
get(SPREAD(CURRENCY=EUR) as #xccy) for(['US25468PBW59'])   # cross-currency
```

---

## Anti-Patterns

| Wrong | Correct | Why |
|-------|---------|-----|
| `per=M` in BQL string | `frq=M` | `per=` is only for `RETURN_SERIES` |
| `result.combined_df()` | `result.combine()` | polars-bloomberg API |
| `conda run` printing to bash | Use PowerShell | cp1252 encoding error on Unicode |
| `bondsUniv` for huge screens | Add `with(mode=cached)` | timeout on large universes |
| `BB_COMPOSITE=='BBB'` | `rating(source=BBG)=='BBB'` | legacy field maps to new model |

---

## References

- `references/universe-functions.md` — complete universe function catalog
- `references/data-items.md` — full data item reference by asset class
- `references/function-reference.md` — all BQL functions (arithmetic, statistical, grouping, time series, date, string, filtering, data handling)
- `references/example-queries.md` — ready-to-run queries by asset class
