# Model Structure — Workbook Layout Guide

## Sheet Organization

| Sheet # | Name | Purpose | Data Flow |
|---------|------|---------|-----------|
| 1 | Summary Dashboard | At-a-glance overview | Pulls from all other sheets |
| 2 | Income Statement | P&L history + estimates | Source: provider extracts, filings |
| 3 | Balance Sheet | Asset/liability structure | Source: provider extracts, filings |
| 4 | Credit Scoring | Custom rating model | Calculated from Sheets 2, 3, 5, 7 |
| 5 | Liquidity & Funding | LCR, NSFR, funding mix | Source: filings, regulatory disclosures |
| 6 | ROE Decomposition | DuPont analysis | Calculated from Sheets 2, 3 |
| 7 | Peer Comparison | Relative benchmarking | Source: provider extracts for peers |

## Data Input Process

### Step 1: Populate Income Statement (Sheet 2)
- Source: CapitalIQ financials, 10-K/10-Q extracts, earnings transcripts
- Enter 5 quarters of historical data
- Calculate derived metrics (NIM, cost/income, etc.)
- Estimate 2 forward quarters using pro forma methodology

### Step 2: Populate Balance Sheet (Sheet 3)
- Source: CapitalIQ, regulatory filings, Pillar 3
- Enter 5 quarters of historical data
- Calculate capital ratios, RWA density, L/D ratio
- Estimate 2 forward quarters

### Step 3: Populate Liquidity (Sheet 5)
- Source: Pillar 3 disclosure, annual report liquidity section
- Enter LCR components, NSFR components
- Enter funding mix breakdown
- Enter maturity profile

### Step 4: Populate Peer Data (Sheet 7)
- Source: CapitalIQ for peers, research provider comparisons
- Enter same metrics for 4-8 peers
- Calculate medians, ranks, percentiles

### Step 5: Calculate Scoring Model (Sheet 4)
- Inputs automatically from Sheets 2, 3, 5
- Apply scoring bands from credit-scoring-methodology.md
- Calculate composite score and upgrade/downgrade probability

### Step 6: Calculate ROE Decomposition (Sheet 6)
- Inputs from Sheets 2, 3
- Apply DuPont formula decomposition
- Show 5-quarter trend with waterfall bridge

### Step 7: Populate Summary Dashboard (Sheet 1)
- Pull key metrics from all other sheets
- Apply traffic light indicators from scoring model
- Display ratings and key snapshot data

## Excel-Specific Implementation Notes

When creating the workbook using the `xlsx` skill:

1. **Sheet creation**: Create each sheet as a 2D JSON array
2. **Headers**: First row of each sheet is the header row
3. **Number formatting**: Format numbers in the data itself (e.g., "$1.30B" as text in summary, raw numbers in calculation sheets)
4. **Conditional formatting indicators**: Add a column with "Green"/"Amber"/"Red" text based on scoring thresholds
5. **Cross-sheet references**: Since xlsx skill writes data directly, calculate all derived values before writing

## Workbook Naming Convention

```
{workspace}/model/{issuer}-model-{YYYY-MM-DD}.xlsx
```

Example: `workspaces/bnp-paribas-2026-03-07/model/bnp-paribas-model-2026-03-07.xlsx`
