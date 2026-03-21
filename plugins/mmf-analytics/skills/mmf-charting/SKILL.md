---
name: mmf-charting
description: >
  This skill should be used when the user asks to "chart MMF holdings",
  "analyze money market funds", "show MMF analytics", "plot fund data",
  "cross-fund comparison", "deep dive on FRGXX/GOFXX/MVRXX/BGSXX",
  "top issuers", "liquidity ratios", "maturity buckets", "HHI concentration",
  or any request to visualize or analyze Government Money Market Fund data
  from the mmf_holdings.db database.
version: 0.1.0
---

# MMF Charting Skill

Produce clean, professional Datawrapper charts for the four Government Money Market Funds:
**FRGXX**, **GOFXX**, **MVRXX**, **BGSXX**. Charts display inline in chat as PNG images.
If Datawrapper fails, fall back to clean matplotlib (no background, no gridlines).

## Database

Default path: `/sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db`
Override via `--db <path>` or the `MMF_DB_PATH` environment variable.

### Tables

**`series_info`** — one row per (ticker, report_date)
- `ticker` TEXT — fund symbol
- `report_date` TEXT — ISO date (YYYY-MM-DD)
- `net_asset_of_series` REAL — NAV in dollars
- `total_value_portfolio_securities` REAL
- `cash` REAL
- `seven_day_gross_yield` REAL (often NULL)
- `avg_portfolio_maturity` REAL — WAM in days
- `avg_life_maturity` REAL — WAL in days
- `number_of_shares_outstanding` REAL
- `stable_price_per_share` REAL

**`holdings`** — one row per holding per (ticker, report_date)
- `ticker`, `report_date` — FK to series_info
- `name_of_issuer` TEXT
- `title_of_issuer` TEXT
- `investment_category` TEXT — see category map below
- `maturity_date_wam` TEXT, `maturity_date_wal` TEXT, `final_maturity_date` TEXT
- `yield` REAL
- `value_excl_sponsor` REAL — primary value field to use
- `pct_net_assets` REAL
- `daily_liquid` TEXT ('Y'/'N'), `weekly_liquid` TEXT ('Y'/'N')
- `illiquid` TEXT, `level3` TEXT

## Key Derived Fields

```python
aum_B = net_asset_of_series / 1e9
cash_pct = cash / net_asset_of_series * 100
daily_liq_pct = sum(value_excl_sponsor where daily_liquid='Y') / net_asset_of_series * 100
weekly_liq_pct = sum(value_excl_sponsor where weekly_liquid='Y') / net_asset_of_series * 100
wal_days = (maturity_date_wal - report_date).days
HHI = sum((issuer_value / nav * 100) ** 2)
```

## Category Mapping

```python
CAT_MAP = {
    'U.S. Government Agency Debt': 'Agency Debt',
    'U.S. Treasury Debt': 'Treasury Debt',
    'U.S. Government Agency Repurchase Agreement': 'Agency Repo',
    'U.S. Treasury Repurchase Agreement': 'Treasury Repo',
    'Other Repurchase Agreement': 'Other Repo',
    'Other Instrument': 'Other',
    'Variable Rate Demand Note': 'VRDN',
}
```
Apply with: `holdings['simple_cat'] = holdings['investment_category'].map(CAT_MAP).fillna(holdings['investment_category'])`

## Maturity Buckets (WAL-based)

```python
BUCKET_ORDER = ['<=1d', '2-7d', '8-30d', '31-90d', '91-180d', '180+d']
def assign_bucket(days):
    if pd.isna(days): return '180+d'
    if days <= 1: return '<=1d'
    if days <= 7: return '2-7d'
    if days <= 30: return '8-30d'
    if days <= 90: return '31-90d'
    if days <= 180: return '91-180d'
    return '180+d'
```

## Color Palettes

```python
FUND_COLORS = {'FRGXX':'#1f77b4','GOFXX':'#ff7f0e','MVRXX':'#2ca02c','BGSXX':'#d62728'}
BUCKET_COLORS = {'<=1d':'#1a9850','2-7d':'#66bd63','8-30d':'#fee08b',
                 '31-90d':'#fdae61','91-180d':'#f46d43','180+d':'#d73027'}
```

## Regulatory Minimums (draw reference lines)

- Daily liquid: **10%** of NAV minimum
- Weekly liquid: **30%** of NAV minimum
- HHI thresholds: **1500** (moderate), **2500** (high concentration)

## Chart Scripts

All scripts live at `${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/`. Run with:
```bash
python3 <script> [--db <path>] [--ticker <TICKER>] [--out <dir>]
```

| Script | Purpose | Output |
|--------|---------|--------|
| `cross_fund_charts.py` | 4 line charts: AUM, Cash%, WAM, WAL across all funds | 4 PNGs |
| `summary_charts.py` | 6 bar charts: latest-month metrics for all 4 funds | 6 PNGs |
| `fund_deep_dive.py` | Full per-fund analysis (composition, maturity, flow, liquidity, HHI) | 5 PNGs |
| `top_issuers.py` | Top-10 issuer horizontal bar chart for one fund | 1 PNG |
| `all_analytics.py` | Runs all of the above | All PNGs |

## Output Convention

Scripts save PNGs to `--out` dir (default `/tmp/mmf_charts/`).
Each script prints the saved PNG path(s) to stdout, one per line, prefixed with `PNG:`.
Claude reads these lines, then uses the Read tool to display each image inline.

## Datawrapper Configuration

```python
DW_API_TOKEN = "EIZmveiKHi0Yv5me8ZVzUeEqAeEmrO7h38MV6ApweA6N0JoXfws7vGkxmGFZhSrO"
DW_SOURCE = "SEC EDGAR N-MFP2 Filings"
DW_BYLINE = "SBC Treasury Analytics"
```

## Fallback: Clean Matplotlib

When Datawrapper is unavailable, use matplotlib with these settings:
```python
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.grid(False)
for spine in ax.spines.values():
    spine.set_edgecolor('#dddddd')
# No fill between, no background, transparent-friendly
plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
```

## Workflow

1. Parse CLI args (`--db`, `--ticker`, `--out`)
2. Connect to SQLite DB
3. Load and process data (apply CAT_MAP, assign buckets, compute derived fields)
4. Try Datawrapper first; on any exception, fall back to matplotlib
5. Save PNG to `--out` directory
6. Print `PNG:<filepath>` for each saved chart
7. Claude captures these paths and uses Read tool to display inline
