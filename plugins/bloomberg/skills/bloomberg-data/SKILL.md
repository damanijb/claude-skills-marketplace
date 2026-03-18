---
name: bloomberg-data
description: Retrieve Bloomberg financial data using polars-bloomberg (BQuery), PyBQL (bql.Service), or bqapi. Use this skill for BQL queries, time series pulls, reference data, screening universes, and market data subscriptions. Covers bdp/bdh/bql patterns, PyBQL object-based queries, and bqapi async sessions.
---

# Bloomberg Data Retrieval

## Execution Environments

| Library | Best For | Environment |
|---------|----------|-------------|
| `polars-bloomberg` (BQuery) | BQL + bdp/bdh, returns Polars DataFrames, no BQuant subscription needed | `sbc` conda env |
| `bql` (PyBQL) | Object-based BQL query construction, BQuant notebooks, returns pandas DataFrames | `bqnt-3` conda env |
| `bqapi` | Async Bloomberg API — market data, subscriptions, reference data | `bqnt-3` conda env |

**Run scripts via PowerShell** (avoids cp1252 Unicode issues in bash):
```
powershell.exe -NonInteractive -Command "conda run -n sbc python script.py"
```

---

## polars-bloomberg (BQuery) — Preferred

```python
from polars_bloomberg import BQuery
from datetime import date

with BQuery() as bq:
    # Snapshot: multiple securities x multiple fields
    df = bq.bdp(["AAPL US Equity", "MSFT US Equity"], ["PX_LAST", "PE_RATIO", "CUR_MKT_CAP"])

    # Time series: long format (security, date, field)
    df = bq.bdh(["AAPL US Equity"], ["PX_LAST", "PX_VOLUME"],
                date(2024, 1, 1), date.today())

    # Pivot for charting
    df_wide = df.pivot(on="security", index="date", values="PX_LAST").sort("date")

    # BQL query -> BqlResult
    result = bq.bql("get(px_last, pe_ratio, cur_mkt_cap/1B) for(members('SPX Index'))")
    df = result.combine()        # joined Polars DataFrame
    df = result[0]               # first item only
    names = result.names         # ['px_last', 'pe_ratio', 'cur_mkt_cap/1B']
```

---

## PyBQL (bql.Service) — BQuant / bqnt-3 env

```python
import bql

bq = bql.Service()

# String query
request = bql.Request("get(px_last, pe_ratio) for(members('SPX Index'))")
response = bq.execute(request)
df = bql.combined_df(response)   # pandas DataFrame

# Object-based query construction
universe = bq.univ.members('SPX Index')
px = bq.data.px_last()
pe = bq.data.pe_ratio()
request = bql.Request(universe, [px, pe])
response = bq.execute(request)

# Access individual item responses
px_response = response[bq.data.px_last()]   # bql.SingleItemResponse
px_df = px_response.df()                     # pandas DataFrame
df_all = bql.combined_df(response)           # merged pandas DataFrame

# Object-based filtering
sector = bq.data.gics_sector_name()
pe = bq.data.pe_ratio()
mktcap = bq.data.cur_mkt_cap(currency='USD')
universe = bq.univ.filter(
    bq.univ.members('SPX Index'),
    (sector == 'Technology') & (pe < 30) & (mktcap > 10e9)
)

# let() for reusable variables
r = bq.func.range(start='-2Y', end='0D', frq='M')
R = bql.let(name='R', expression=bq.data.return_series(calc_interval=r, per='M'))
Cum = bql.let(name='Cum', expression=bq.func.cumprod(bq.func.dropna(R) + 1) - 1)
```

---

## BQL Query Structure

```
[let(#var = expr;)]   <- optional: reusable variables
get(DataItem(params)) <- what to retrieve
for(universe)         <- which securities
[with(global_params)] <- optional: dates, frq, fill, currency
```

### Quick Patterns
```
# Snapshot
get(px_last, pe_ratio, cur_mkt_cap/1B) for('AAPL US Equity')

# Index screen with filter
get(name, px_last, pe_ratio, cur_mkt_cap/1B)
for(filter(members('SPX Index'), pe_ratio<20 and cur_mkt_cap>10B))

# Top N by field
for(top(members('INDU Index'), 10, CUR_MKT_CAP)) get(name, cur_mkt_cap/1B, pe_ratio)

# Historical time series (daily, forward-fill)
get(px_last(dates=range(-1Y,0D))) for('AAPL US Equity') with(frq=d, fill=prev)

# Sector aggregation
get(groupAvg(pe_ratio, gics_sector_name)) for(members('SPX Index'))

# Fixed income analytics
get(yield(yield_type=YTW), spread(spread_type='OAS'), duration(duration_type=MODIFIED))
for(filter(bondsUniv('Active'), rating(source=SP) in ['A+','A','A-']))

# CDS term structure via let()
let(#3Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=3Y), mapby=lineage).value;
    #5Y = value(cds_spread(Pricing_source='CBIN',fill=prev).value, cds(tenor=5Y), mapby=lineage).value;)
get(name, #3Y, #5Y) for(members('INDU Index'))
```

### Global Parameters (with())
```
with(dates=range(-1Y,0D), frq=M, fill=prev, currency=USD, mode=cached, side=MID)
```
- **frq**: `D` `W` `M` `Q` `Y` `SA`
- **fill**: `prev` `none`
- **Date shortcuts**: `0d` `-1d` `-1m` `ytd` `mtd` `qtd` `wtd`

---

## Searching BQL Data Items

19,715 total BQL data items; the top 2,500 by usage are in `data/bql_data_items.parquet`:

```python
import polars as pl

df = pl.read_parquet(
    r"C:\Users\f8631\Documents\claude-skills-marketplace\plugins\bloomberg"
    r"\skills\bloomberg-data\data\bql_data_items.parquet"
)

# Search by keyword in description
results = df.filter(pl.col("description").str.contains("(?i)credit rating"))

# Get top 50 most-used items
print(df.head(50))

# Search by code prefix
print(df.filter(pl.col("code").str.starts_with("spread")))
```

Schema: `code` (str), `description` (str), `weight` (int, higher = more used).
Deep-link: `https://help.bquant.blpprofessional.com/bql/data-items/{code_without_parens}?view=desktop`

---

## Universe Functions

| Function | Description |
|----------|-------------|
| `members('SPX Index')` | Index constituents |
| `members('PORT_ID', type=PORT)` | Portfolio holdings |
| `filter(univ, condition)` | Subset by predicate |
| `top(univ, n, field)` / `bottom(...)` | Top/bottom N |
| `equitiesUniv(['active','primary'])` | All active equities (use `mode=cached`) |
| `fundsUniv(['Primary','Active'])` | All active funds |
| `bondsUniv('Active')` | Active bonds (SRCH) |
| `debtUniv('ACTIVE')` | Bonds + loans + munis + preferreds |
| `loansUniv('active')` | Active loans (LSRC) |
| `mortgagesUniv(ACTIVE)` | Active MBS |
| `peers('AAPL US Equity', type=BLOOMBERG_BEST_FIT)` | Peer group |
| `bonds('AAPL US Equity')` | All bonds of issuer |
| `holdings('HYG US Equity')` | Fund holdings |
| `cds('JPM US Equity', tenor=5Y)` | CDS for issuer |
| `union()` / `intersect()` / `setDiff()` | Set operations |
| `countries(['g8'])` | Country group |

---

## Key Data Items Quick Reference

### Equity
```
PX_LAST, PX_BID, PX_ASK, PX_VOLUME, CUR_MKT_CAP(currency=USD)
DAY_TO_DAY_TOTAL_RETURN, EQY_SH_OUT
IS_EPS(fpt,fpo,fpr,ae), PE_RATIO, SALES_REV_TURN, EBITDA, NET_INCOME, EV_TO_EBITDA
GROSS_MARGIN, OPER_MARGIN, RETURN_COM_EQY, TOT_DEBT_TO_EBITDA, NET_DEBT_TO_EBITDA
GICS_SECTOR_NAME, BICS_LEVEL_1_SECTOR_NAME, CNTRY_OF_RISK, SECURITY_TYP
```

### Fundamental Period Params
| Param | Values |
|-------|--------|
| `fpt` | `A` Annual · `Q` Quarterly · `LTM` · `BA` Calendarized · `BT` NTM |
| `fpo` | `0` latest · `-1` prior · `range(-4,0)` · `range(-5,2)` (hist+fcast) |
| `fpr` | `range(2010,2018)` · `range(2017Q1,2018Q4)` · `2017-09-30` |
| `ae`  | `A` actual · `E` estimate · (omit for both) |

### Fixed Income
```
YIELD(YIELD_TYPE=YTW)          # YTW YTM YTC YTP CON CUR
SPREAD(SPREAD_TYPE='OAS')      # Z I OAS N E J A P R BMK ASW G
DURATION(DURATION_TYPE=MODIFIED)  # SPREAD MODIFIED MACAULAY EFFECTIVE
CONVEXITY, RISK, DV01, KRD(TENOR=5Y), S_KRD(TENOR=5Y)
TOTAL_RETURN(CALC_INTERVAL=Range(-3M,0D), DISPLAY_RETURNS='Percent')
RETURN_SERIES(CALC_INTERVAL=range(-1Y,0D), PER=M)
CPN, MATURITY, AMT_OUTSTANDING(currency=USD), PAYMENT_RANK, ID_ISIN, CRNCY
rating(source=SP)  # SP MOODY FITCH AMBEST BBG DBRS
#rating().BASE_RATING, #rating().WATCH, #rating().EFFECTIVE_DATE
```

---

## bqapi — Async Bloomberg API

```python
import bqapi
from bqapi.requests import refdata, mktdata

# Reference data (BDP-style)
with bqapi.Session() as session:
    req = refdata.ReferenceDataRequest(
        securities=["AAPL US Equity", "MSFT US Equity"],
        fields=["PX_LAST", "PE_RATIO"]
    )
    response = session.send_and_receive(req)

# Historical data (BDH-style)
with bqapi.Session() as session:
    req = refdata.HistoricalDataRequest(
        securities=["AAPL US Equity"],
        fields=["PX_LAST"],
        start_date="20240101",
        end_date="20241231"
    )
    response = session.send_and_receive(req)

# Async EventLoop for subscriptions
event_loop = bqapi.EventLoop()

@event_loop.run
async def subscribe_live():
    async with bqapi.Session(event_loop) as session:
        sub = bqapi.Subscription(["AAPL US Equity"], ["PX_LAST", "PX_BID", "PX_ASK"])
        async for tick in session.subscribe(sub):
            print(tick)
```

---

## Anti-Patterns

| Wrong | Correct | Why |
|-------|---------|-----|
| `result.combined_df()` | `result.combine()` | polars-bloomberg API method name |
| `per=M` in BQL string | `frq=M` in `with()` | `per=` only for `RETURN_SERIES` |
| `conda run` in bash | Use PowerShell | cp1252 encoding error on Unicode output |
| `bondsUniv` large screen | Add `with(mode=cached)` | timeout on large universes |
| `BB_COMPOSITE=='BBB'` | `rating(source=BBG)=='BBB'` | legacy field maps to new rating model |
| `bql.Response[0]` | `bql.combined_df(response)` | PyBQL response access pattern |

---

## References
- `references/data-items-guide.md` — full data item catalog by asset class
- `references/bql-language.md` — complete BQL function reference
- `references/example-queries.md` — ready-to-run queries by asset class
- `references/bqapi-reference.md` — bqapi async API reference
- `data/bql_data_items.parquet` — top-2,500 BQL data items (searchable)
