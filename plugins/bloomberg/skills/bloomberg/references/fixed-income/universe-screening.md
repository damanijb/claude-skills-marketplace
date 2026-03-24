# BQL Fixed Income Universe & Screening Reference

> **VERIFIED**: All examples below use parameter names confirmed against live Bloomberg BQL.
> Key corrections from prior version:
> - `bondsuniv(Active)` NOT `bondsUniv(COUNTRY='US', SECURITY_TYP='Corp')` — named params error
> - `yield(yield_type=YTW)` NOT `yield(type=ytw)` — `type` is not a valid parameter
> - `duration(duration_type=modified)` NOT `duration(type=modified)`
> - `spread(spread_type=OAS)` NOT `spread(type=oas)`
> - Rating filter uses `.source_scale` numeric comparison, NOT string comparison like `>= 'BBB-'`

## Universe Functions

### Equity Universes
```
members('SPX Index')              # Index members
equitiesUniv(COUNTRY='US')        # All US equities
peers('AAPL US Equity')           # GICS peers
```

### Fixed Income Universes

**IMPORTANT**: `bondsuniv` must be lowercase and takes a single positional argument.
Named parameters like `COUNTRY='US'` cause validation errors.
Filter by currency/type in the `filter()` clause instead.

```
bondsuniv(Active)                    # All active bonds (no quotes around Active)
bondsuniv('USD')                     # USD bonds (use filter for more specificity)
debtUniv(ISSUER='AAPL')             # All AAPL debt
loansUniv(COUNTRY='US')             # US leveraged loans
mortgagesUniv(MTG_DEAL_TYP='Agency CMO')  # Agency CMO
municipalsUniv(STATE='CA')          # California munis
preferredsUniv(COUNTRY='US')        # US preferreds
```

### Issuer Chain Functions
```
bonds('AAPL US Equity')           # All bonds from AAPL's issuer
loans('AAPL US Equity')           # All loans
debt('AAPL US Equity')            # All debt instruments
cds('AAPL US Equity')             # CDS contracts
```

### Fund Universes
```
fundsUniv(FUND_TYP='Open-End Fund', FUND_GEO_FOCUS='United States')
```

### Set Operations
```
union(members('SPX Index'), members('INDU Index'))       # Combine
intersect(members('SPX Index'), members('NDX Index'))    # Overlap
setDiff(members('SPX Index'), members('NDX Index'))      # Difference
```

### Entity Translation
```
fundamentalTicker('AAPL US Equity')        # Fundamental entity
issuerOf('AAPL US Equity')                 # Parent issuer
relativeIndex('AAPL US Equity')            # Related index
```

### Screen Results
```
screenresults('MY_SAVED_SCREEN')           # Results from saved SRCH<GO> screen
```

## Field Parameter Reference (VERIFIED)

These are the correct parameter names. Using shorthand like `type=` will error.

| Data Item | Parameter | Values | Default |
|-----------|-----------|--------|---------|
| `yield()` | `yield_type` | YTW, YTM, YTC, YTP, CON, CUR, AVL, SAVL, TAX_EQUIVALENT | YTW |
| `duration()` | `duration_type` | Spread, Modified, Macaulay, Effective | Spread |
| `spread()` | `spread_type` | I, Z, ASW, OAS, BMK, G | OAS |
| All analytics | `side` | Bid, Mid, Ask | Bid |
| All analytics | `pricing_source` | BVAL, BGN, TRAC, CBBT, etc. | BVAL |
| All analytics | `dates` | 0d, -1M, range(-1Y,0D) | 0d |

## Rating Filters (VERIFIED)

**String comparison (`>= 'BBB-'`) does NOT work in BQL filter().**
Use the numeric `source_scale` attribute instead.

### S&P Source Scale (lower = better)
| Scale | Rating |
|-------|--------|
| 1 | AAA |
| 2 | AA+ |
| 3 | AA |
| 4 | AA- |
| 5 | A+ |
| 6 | A |
| 7 | A- |
| 8 | BBB+ |
| 9 | BBB |
| 10 | BBB- |
| 11 | BB+ |
| 12 | BB |
| 13 | BB- |
| 14+ | B+ and below |
| 23 | NR |

### Filter pattern
```
# AA- or better (source_scale 1-4)
rating(source=SP).source_scale <= 4

# Investment grade (source_scale 1-10, i.e. BBB- or better)
rating(source=SP).source_scale <= 10

# High yield only (source_scale 11+, excluding NR)
rating(source=SP).source_scale >= 11 and rating(source=SP).source_scale < 23
```

### Get rating in output
```
# In get() clause — returns the rating string + metadata columns
get(rating(source=SP))
get(rating(source=MOODY))
get(rating(source=BBG))        # Bloomberg composite
```

## Screening Patterns (VERIFIED)

### Filter by Multiple Criteria
```
# Investment grade USD corporate bonds, >$500M outstanding
get(name, cpn, maturity,
    yield(yield_type=YTW),
    spread(spread_type=OAS),
    duration(duration_type=modified))
for(filter(bondsuniv(Active),
    crncy == 'USD' and
    rating(source=SP).source_scale <= 10 and
    amt_outstanding > 500000000))
```

### Top/Bottom N
```
# Top 20 highest yielding IG bonds
get(name, yield(yield_type=YTW), spread(spread_type=OAS))
for(top(filter(bondsuniv(Active),
    crncy == 'USD' and rating(source=SP).source_scale <= 10),
    20, yield(yield_type=YTW)))
```

### Maturity Band Screening
```
# Bonds maturing in 5-10 years
get(name, maturity, yield(yield_type=YTW), spread(spread_type=OAS))
for(filter(bondsuniv(Active),
    crncy == 'USD' and
    maturity >= '2031-01-01' and maturity <= '2036-01-01'))
```

### Sector/Rating Aggregation
```
# Average OAS by rating bucket using base_rating metadata
let(#rat=rating(source=SP);)
get(groupavg(spread(spread_type=OAS), #rat().base_rating))
for(filter(bondsuniv(Active), crncy == 'USD'))
```

### New Issuance Screen
```
# Bonds issued in the past year
get(name, cpn, maturity, issue_dt, amt_outstanding,
    yield(yield_type=YTW),
    duration(duration_type=modified),
    rating(source=SP))
for(filter(bondsuniv(Active),
    crncy == 'USD' and
    issue_dt >= '2025-03-23'))
```

### Short Duration + High Quality Screen
```
# AA- or better, duration <2, yield >4%, issued past year
get(name, cpn, maturity, issue_dt, amt_outstanding,
    yield(yield_type=YTW),
    duration(duration_type=modified),
    spread(spread_type=OAS),
    rating(source=SP))
for(filter(bondsuniv(Active),
    crncy == 'USD' and
    issue_dt >= '2025-03-23' and
    duration(duration_type=modified) < 2 and
    yield(yield_type=YTW) > 4 and
    rating(source=SP).source_scale <= 4))
```

## Common with() Parameters for FI Queries
```
with(mode=cached)          # Use cached data for large universes (faster, but may be stale)
with(currency='USD')       # Convert to USD
with(dates=range(-1Y,0D))  # Historical date range
with(frq=M)                # Monthly frequency
```

## Performance Notes

- `bondsuniv(Active)` is a HUGE universe. Without tight filters, queries will timeout (default 32s).
- Use `--timeout 120000` on the bql.py runner for large universe screens.
- Adding `with(mode=cached)` can help but may return stale data.
- Filter on `crncy`, `issue_dt`, and analytics fields to narrow the universe quickly.
- Requesting `rating(source=SP)` and `rating(source=MOODY)` in the same `get()` causes
  `result.combine()` to create duplicate rows. Query one rating source at a time, or use
  `--separate` flag to inspect individual result DataFrames.
