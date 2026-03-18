# BQL Universe Functions — Complete Reference

## Equity & General

| Function | Params | Example |
|----------|--------|---------|
| `members('INDEX')` | `dates=` for historical membership | `members('SPX Index')` |
| `members('ID', type=PORT)` | `type=PORT` for portfolios | `members('U17911388-100', type=PORT)` |
| `equitiesUniv(['active','primary'])` | status flags | Use `with(mode=cached)` for large screens |
| `fundsUniv(['Primary','Active'])` | status flags | |
| `countries(['g8'])` | country group | `for(countries(['g8'])) get(cpi)` |
| `filter(univ, predicate)` | any condition | `filter(members('SPX Index'), pe_ratio<20)` |
| `top(univ, n, field)` | sort desc, take n | `top(members('INDU Index'), 10, CUR_MKT_CAP)` |
| `bottom(univ, n, field)` | sort asc, take n | `bottom(members('INDU Index'), 5, PE_RATIO)` |
| `peers('TICK', type=BLOOMBERG_BEST_FIT)` | peer type | `peers('TSLA US Equity', type=BLOOMBERG_BEST_FIT)` |
| `list(['A','B'])` | ad hoc | `list(['IBM US Equity', 'AAPL US Equity'])` |

## Fixed Income Universes

| Function | Description | Key Params |
|----------|-------------|------------|
| `bondsUniv('Active')` | Active bonds (SRCH equivalent) | `ConsolidateDuplicates`, `IncludePrivateSecurities` |
| `debtUniv('ACTIVE')` | All bonds + loans + munis + preferreds | |
| `loansUniv('active')` | Active loans (LSRC equivalent) | |
| `mortgagesUniv(ACTIVE)` | Active MBS | |
| `municipalsUniv(ACTIVE)` | Active municipal bonds | |
| `preferredsUniv(ACTIVE)` | Active preferred securities | |
| `axedUniv(ASK)` | Dealer-axed securities | `ASK` or `BID` |
| `screenresults(SRCH, '@NAME')` | Saved SRCH/LSRC screen | `type=SRCH` or `LSRC` |

## Issuer Chains

| Function | Description | Note |
|----------|-------------|------|
| `bonds('AAPL US Equity')` | All bonds of issuer | `ISSUEDBY=CREDIT_FAMILY` for broader group |
| `loans('MSFT US Equity')` | All loans of issuer | |
| `debt(['GE US Equity'])` | All debt of issuer | bonds + loans + munis + preferreds |
| `municipals(['ISSUER'])` | All munis of issuer | |
| `preferreds(['GE US Equity'])` | All preferreds of issuer | |
| `mortgages(['MS US Equity'])` | All MBS of issuer | |
| `holdings('HYG US Equity')` | Fund holdings | `dates=-1y` for historical |
| `cds('JPM US Equity', tenor=5Y)` | CDS for issuer | tenors: 1Y 2Y 3Y 5Y(default) 7Y 10Y |
| `options('AAPL US Equity')` | Options chain | |
| `futures(['CLA Comdty'])` | Futures chain | |
| `curveMembers('YCGT0025 Index')` | Yield curve members | |
| `segments(['AAPL US Equity'])` | Business segments | |

## Set Operations

```
union(members('INDU Index'), ['PEP US Equity', 'T US Equity'])
intersect(members('SX5E Index'), members('CAC Index'))
setDiff(members('LEGATRUU Index'), members('LEGASTAT Index'))
```

## Entity Translation

```
fundamentalTicker(members('SHSZ300 index'))       # nearest financial reporting entity
translateSymbols(members('PORT'), targetidtype='fundamentalticker')
translateSymbols(members('PORT'), instrumentidtype=Corp)  # FI → equity
relativeIndex(['AAPL US Equity'])                 # benchmark index
issuerOf(['AZ791428 Corp'])                       # issuer from bond
parent(['FIAT GR Equity'])                        # parent company
equityPricingTicker(['FIAT GR Equity'])           # nearest listed company
esgTicker(['FIAT GR Equity'])                     # nearest ESG-reporting entity
```

## CDS-Specific

```
# CDS index membership
for(members(['ITRXEXE Curncy']))   # ITRX EUR Crossover
for(members(['IBOXUMAE Index']))   # CDX.NA.IG
for(members(['IBOXHYAE Index']))   # CDX.NA.HY

# CDS for all INDU members at 5Y tenor
for(cds(members(['INDU Index']), tenor=5Y))
```

## Portfolio-Specific

```
# Equity portfolio
for(filter(members('U17911388-100', type=PORT), SECURITY_TYP=='Common Stock'))

# FI portfolio
for(members('U17911388-181', type=PORT))

# Drifting weight portfolio (use positions not weights)
get(id().positions) for(members('PORT_ID', type=PORT))
```
