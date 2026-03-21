# Chart Type Reference

## Datawrapper Types Used in This Plugin

| Chart | DW Type | Description |
|-------|---------|-------------|
| Line (multi-series) | `d3-lines` | AUM trends, liquidity ratios, HHI over time |
| Column chart | `column-chart` | Latest-month per-fund bar charts |
| Stacked bar | `d3-bars-stacked` | Portfolio composition, maturity buckets |
| Horizontal bar | `d3-bars` | Top 10 issuers (sorted ascending → longest bar at top) |

## Data Shape for Each DW Chart Type

### `d3-lines` (line chart)
Rows = dates, columns = series names. First column must be `Date` (YYYY-MM-DD string).
```
Date,FRGXX,GOFXX,MVRXX,BGSXX
2025-02-28,8.1,12.3,5.6,9.2
2025-03-31,8.3,12.1,5.8,9.4
```

### `column-chart` (grouped column)
Column = category, rows = each bar.
```
Fund,AUM ($B)
FRGXX,8.3
GOFXX,12.1
MVRXX,5.8
BGSXX,9.4
```

### `d3-bars-stacked` (stacked bar)
Rows = months/categories (stacked axis), columns = stack segments.
```
Date,Agency Debt,Treasury Debt,Agency Repo,Treasury Repo
2025-02-28,25.3,18.1,42.5,14.1
2025-03-31,24.1,19.3,43.2,13.4
```

### `d3-bars` (horizontal bar)
Two columns: label and value.
```
Issuer,% of NAV
Federal Home Loan Bank,8.4
US Treasury,7.2
...
```

## Matplotlib Fallback Style Rules

Always apply these settings for the fallback path:
```python
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.grid(False)
for spine in ax.spines.values():
    spine.set_edgecolor('#dddddd')
fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
```

## Color Palette

```python
# Fund colors (consistent across all charts)
FUND_COLORS = {
    'FRGXX': '#1f77b4',  # Blue
    'GOFXX': '#ff7f0e',  # Orange
    'MVRXX': '#2ca02c',  # Green
    'BGSXX': '#d62728',  # Red
}

# Maturity bucket colors (green=short → red=long)
BUCKET_COLORS = {
    '<=1d':    '#1a9850',
    '2-7d':    '#66bd63',
    '8-30d':   '#fee08b',
    '31-90d':  '#fdae61',
    '91-180d': '#f46d43',
    '180+d':   '#d73027',
}

# Investment category colors
CAT_COLORS = {
    'Agency Debt':   '#1f77b4',
    'Treasury Debt': '#aec7e8',
    'Agency Repo':   '#ff7f0e',
    'Treasury Repo': '#ffbb78',
    'Other Repo':    '#2ca02c',
    'VRDN':          '#98df8a',
    'Other':         '#d62728',
}
```
