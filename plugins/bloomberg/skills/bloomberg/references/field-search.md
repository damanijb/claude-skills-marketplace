# BQL Field Search -- Finding Data Item Mnemonics

When you don't know the exact BQL field name, use these approaches (in priority order):

## 1. Bloomberg MCP Tool (Live Search)

The `bloomberg_field_search` MCP tool searches Bloomberg's field database in real time:

```
bloomberg_field_search(query="yield to maturity", max_results=20)
```

Returns: field ID, mnemonic, and description for each match.

**Good search queries:**
- By concept: `"yield"`, `"spread"`, `"duration"`, `"market cap"`
- By asset class: `"equity"`, `"bond"`, `"fund"`, `"mortgage"`
- By specific metric: `"earnings per share"`, `"return on equity"`, `"ev to ebitda"`

## 2. Parquet Lookup (Offline, Top 2,500 Items)

The `data/bql_data_items.parquet` file contains the 2,500 most commonly used BQL data items,
ranked by usage frequency. Search it with Polars:

```python
import polars as pl

df = pl.read_parquet("data/bql_data_items.parquet")

# Search by keyword in description
results = df.filter(pl.col("description").str.contains("(?i)yield"))
print(results.sort("weight", descending=True).head(20))

# Search by code prefix
results = df.filter(pl.col("code").str.starts_with("CUR_"))
print(results)
```

Columns: `code` (str), `description` (str), `weight` (int -- higher = more commonly used)

## 3. Deep Link to Bloomberg Documentation

For any discovered field code, get full documentation at:

```
https://help.bquant.blpprofessional.com/bql/data-items/{CODE}
```

Where `{CODE}` is the field mnemonic without parentheses.
Example: `https://help.bquant.blpprofessional.com/bql/data-items/PX_LAST`

## Common Field Quick Reference

### Equity
| Field | Description |
|-------|-------------|
| `PX_LAST` | Last trade price |
| `PX_VOLUME` | Daily volume |
| `CUR_MKT_CAP` | Market capitalization |
| `PE_RATIO` | Price/Earnings ratio |
| `EV_TO_EBITDA` | Enterprise value to EBITDA |
| `IS_EPS` | Earnings per share (use fpt=A/Q/LTM) |
| `SALES_REV_TURN` | Revenue |
| `EBITDA` | EBITDA |
| `GROSS_MARGIN` | Gross margin % |
| `RETURN_COM_EQY` | Return on equity |

### Fixed Income
| Field | Description |
|-------|-------------|
| `YIELD` | Bond yield (use type=YTW/YTM/YTC) |
| `SPREAD` | Bond spread (use type=OAS/Z/ASW) |
| `DURATION` | Bond duration (use type=MODIFIED/MACAULAY/EFFECTIVE) |
| `CONVEXITY` | Bond convexity |
| `DV01` | Dollar value of 01 |
| `CPN` | Coupon rate |
| `MATURITY` | Maturity date |
| `AMT_OUTSTANDING` | Amount outstanding |
| `PAYMENT_RANK` | Seniority ranking |

### CDS
| Field | Description |
|-------|-------------|
| `CDS_SPREAD` | CDS spread (use pricing source) |
| `RSK_BB_IMPLIED_CDS_SPREAD` | Bloomberg implied CDS spread |

### Funds
| Field | Description |
|-------|-------------|
| `FUND_NET_ASSET_VAL` | NAV |
| `FUND_TOTAL_ASSETS` | Total AUM |
| `FUND_BENCHMARK` | Benchmark index |
