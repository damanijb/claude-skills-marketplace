---
name: financial-model
description: This skill should be used when the user asks to "build financial model", "create Excel workbook", "credit scoring model", "pro forma estimates", "financial spreadsheet", "liquidity analysis", "ROE decomposition", "peer comparison spreadsheet", "WACC calculation", "credit rating scorecard", "build a bank model", or needs to create a structured Excel workbook with historical financial data, forward estimates, credit scoring, and peer benchmarking.
version: 0.1.0
---

# Financial Model Builder

Build a comprehensive Excel workbook for bank credit analysis with 7 sheets: Summary Dashboard, Income Statement, Balance Sheet, Credit Scoring Model, Liquidity & Funding, ROE Decomposition, and Peer Comparison.

## Prerequisites

- Research synthesis data from `fundamental-research` skill at `{workspace}/data/research-synthesis.json`
- Provider extract data from `{workspace}/data/provider-extracts/`
- Collected document data from `{workspace}/data/documents/`

## Workbook Structure

Create the workbook using the `xlsx` skill or Desktop Commander Excel tools. The workbook path: `{workspace}/model/{issuer}-model.xlsx`

### Sheet 1: Summary Dashboard

**Layout:**
| Row | Content |
|-----|---------|
| 1 | **Issuer Name** (large, bold) |
| 2 | Ticker, Sector, Country, Analysis Date |
| 3 | Blank separator |
| 4 | **Credit Ratings** header |
| 5 | Moody's: [rating] / [outlook] |
| 6 | S&P: [rating] / [outlook] |
| 7 | Fitch: [rating] / [outlook] |
| 8 | Blank separator |
| 9 | **Key Metrics Snapshot** header |
| 10-20 | Metric, Current Value, Prior Quarter, YoY Change, Peer Median |

**Key metrics to include:**
- CET1 Ratio, Leverage Ratio
- ROE, ROA
- NIM, Cost/Income Ratio
- NPL Ratio, NPL Coverage
- LCR, Loan/Deposit Ratio
- Total Assets, Market Cap

**Conditional formatting data:**
- Column F: "Green" / "Amber" / "Red" indicator based on scoring bands
- Use these thresholds from the Credit Scoring Model sheet

### Sheet 2: Income Statement (5Q + 2Q Pro Forma)

**Column layout:**
| Col | Content |
|-----|---------|
| A | Line Item |
| B | Q1-{Y-1} (Actual) |
| C | Q2-{Y-1} (Actual) |
| D | Q3-{Y-1} (Actual) |
| E | Q4-{Y-1} (Actual) |
| F | Q1-{Y} (Actual) |
| G | Q2-{Y}E (Estimate) |
| H | Q3-{Y}E (Estimate) |
| I | QoQ Change |
| J | YoY Change |

**Row items:**
```
Net Interest Income
  Interest Income
  Interest Expense
Non-Interest Income
  Fee & Commission Income
  Trading Revenue
  Other Operating Income
Total Revenue
Provision for Credit Losses
Operating Expenses
  Compensation & Benefits
  Non-Compensation Expenses
Pre-Tax Income
Income Tax
Net Income
EPS (Diluted)

--- Derived Metrics ---
NIM (%)
Cost/Income Ratio (%)
Cost of Risk (bps)
Revenue Growth (YoY %)
Jaws Ratio (pp)
Effective Tax Rate (%)
```

**Pro forma estimation methodology:**
- NII: Apply management guidance growth rate, or extrapolate from rate sensitivity + rate forecast
- Fee income: Apply trailing 4Q average growth rate
- Trading: Use trailing 4Q average (high volatility item)
- Provisions: Apply management guidance cost of risk, or trending estimate
- Opex: Apply management cost/income target, or trailing growth rate
- Tax: Apply trailing effective tax rate

### Sheet 3: Balance Sheet (5Q + 2Q Pro Forma)

**Row items:**
```
ASSETS
Cash & Central Bank Deposits
Financial Assets at Fair Value
Securities (AFS + HTM)
Loans and Advances (Gross)
  Less: Allowance for Credit Losses
Loans and Advances (Net)
Other Assets
Total Assets

LIABILITIES
Customer Deposits
  Retail Deposits
  Corporate Deposits
Wholesale Funding
  Senior Unsecured Bonds
  Covered Bonds
  Subordinated Debt
Central Bank Borrowings
Other Liabilities
Total Liabilities

EQUITY
CET1 Capital
AT1 Capital
Tier 2 Capital
Total Regulatory Capital
Total Equity (Book Value)
Tangible Book Value

RISK-WEIGHTED ASSETS
Credit Risk RWA
Market Risk RWA
Operational Risk RWA
Total RWA

--- Derived Metrics ---
CET1 Ratio (%)
Tier 1 Ratio (%)
Total Capital Ratio (%)
Leverage Ratio (%)
RWA Density (RWA/TA %)
Loan/Deposit Ratio (%)
Tangible Book Value per Share
```

### Sheet 4: Credit Scoring Model

**Scoring framework — 6 dimensions, weighted composite:**

Build this as a calculation sheet with:
- Column A: Dimension
- Column B: Sub-Metric
- Column C: Weight (within dimension)
- Column D: Current Value
- Column E: Score (0-10, calculated from scoring bands)
- Column F: Weighted Score
- Column G: Peer Median
- Column H: Peer Rank
- Column I: Trend (3Q direction: Up/Flat/Down)

**Scoring bands** (load from `references/credit-scoring-methodology.md`):

| Dimension (Weight) | Sub-Metric | 8-10 (Strong) | 5-7 (Adequate) | 0-4 (Weak) |
|---------------------|-----------|----------------|-----------------|-------------|
| **Capital (20%)** | CET1 Ratio | >14% | 11-14% | <11% |
| | CET1 Buffer over SREP | >400bp | 200-400bp | <200bp |
| | Leverage Ratio | >5% | 3.5-5% | <3.5% |
| **Profitability (20%)** | ROE | >12% | 8-12% | <8% |
| | Cost/Income | <50% | 50-65% | >65% |
| | NIM | >1.5% | 1.0-1.5% | <1.0% |
| **Asset Quality (20%)** | NPL Ratio | <1% | 1-3% | >3% |
| | NPL Coverage | >100% | 60-100% | <60% |
| | Cost of Risk (bps) | <20 | 20-50 | >50 |
| **Efficiency (15%)** | Cost/Income | <48% | 48-60% | >60% |
| | Revenue/Employee ($K) | >400 | 250-400 | <250 |
| **Liquidity (15%)** | LCR | >150% | 120-150% | <120% |
| | NSFR | >110% | 100-110% | <100% |
| | Loan/Deposit Ratio | <90% | 90-110% | >110% |
| **Ratings (10%)** | Moody's LT | Aa3+ | A1-Baa1 | Baa2- |
| | Outlook | Positive | Stable | Negative |

**Composite score calculation:**
```
Dimension Score = Σ(sub-metric score × sub-metric weight within dimension)
Composite Score = Σ(Dimension Score × dimension weight)
```

**Upgrade/Downgrade Probability Section:**

| Factor | Value | Weight | Contribution |
|--------|-------|--------|-------------|
| Composite Score Level | [0-10] | 30% | [calc] |
| 3Q Composite Trend | [+/flat/-] | 25% | [calc] |
| Peer Relative Position | [above/at/below median] | 20% | [calc] |
| Rating Agency Outlook | [pos/stable/neg] | 15% | [calc] |
| Macro Stress Sensitivity | [low/med/high] | 10% | [calc] |
| **Upgrade Probability** | | | **[X]%** |
| **Downgrade Probability** | | | **[Y]%** |

### Sheet 5: Liquidity & Funding

**LCR Calculation:**
```
High-Quality Liquid Assets (HQLA)
  Level 1: Cash + Central Bank Reserves + Sovereign Bonds
  Level 2A: Covered Bonds, Corporate Bonds (AA-)
  Level 2B: Lower-rated corporates, RMBS
Total HQLA

Net Cash Outflows (30-day stressed)
  Retail Deposit Outflows
  Wholesale Funding Outflows
  Derivative Outflows
  Committed Facility Drawdowns
  Less: Inflows (capped at 75% of outflows)
Total Net Cash Outflows

LCR = Total HQLA / Total Net Cash Outflows
```

**NSFR Calculation:**
```
Available Stable Funding (ASF)
  Regulatory Capital
  Stable Retail Deposits (>1Y or insured)
  Less Stable Retail Deposits
  Wholesale Funding (>1Y maturity)
Total ASF

Required Stable Funding (RSF)
  Cash: 0%
  Sovereign Securities: 5%
  Corporate Loans (<1Y): 50%
  Mortgages: 65%
  Other Loans: 85%
  Other Assets: 100%
Total RSF

NSFR = Total ASF / Total RSF
```

**Funding Mix Table:**
| Source | Amount | % of Total | Cost |
|--------|--------|-----------|------|
| Retail Deposits | | | |
| Corporate Deposits | | | |
| Senior Unsecured | | | |
| Covered Bonds | | | |
| Subordinated Debt | | | |
| Central Bank | | | |

**Maturity Profile:**
| Bucket | <1M | 1-3M | 3-6M | 6-12M | 1-2Y | 2-5Y | >5Y |
|--------|-----|------|------|-------|------|------|-----|
| Assets Maturing | | | | | | | |
| Liabilities Maturing | | | | | | | |
| Net Gap | | | | | | | |
| Cumulative Gap | | | | | | | |

### Sheet 6: ROE Decomposition (DuPont)

**Framework:**
```
ROE = Profit Margin × Asset Turnover × Equity Multiplier
    = (Net Income / Revenue) × (Revenue / Assets) × (Assets / Equity)
```

**Extended bank-specific decomposition:**
```
ROE = NII Contribution + Fee Contribution - Cost Drag - Provision Drag - Tax Drag

Where:
NII Contribution = NII / Average Equity
Fee Contribution = Non-Interest Income / Average Equity
Cost Drag = -Operating Expenses / Average Equity
Provision Drag = -Provisions / Average Equity
Tax Drag = -Tax / Average Equity
```

**5-Quarter trend table:**
| Component | Q1 | Q2 | Q3 | Q4 | Q5 | Direction |
|-----------|----|----|----|----|----|----|
| ROE | | | | | | |
| Profit Margin | | | | | | |
| Asset Turnover | | | | | | |
| Equity Multiplier | | | | | | |
| NII Contribution | | | | | | |
| Fee Contribution | | | | | | |
| Cost Drag | | | | | | |
| Provision Drag | | | | | | |

### Sheet 7: Peer Comparison

**Structure:**
- Row 1: Headers
- Rows 2-N: Each peer as a row
- Highlighted row for the target issuer
- Last rows: Peer Median, Peer Mean, Target Rank, Target Percentile

**Columns:**
| Metric | Target | Peer 1 | Peer 2 | ... | Median | Rank |
|--------|--------|--------|--------|-----|--------|------|
| Total Assets | | | | | | |
| ROE | | | | | | |
| ROA | | | | | | |
| NIM | | | | | | |
| Cost/Income | | | | | | |
| CET1 Ratio | | | | | | |
| NPL Ratio | | | | | | |
| NPL Coverage | | | | | | |
| Cost of Risk | | | | | | |
| LCR | | | | | | |
| Loan/Deposit | | | | | | |
| Leverage Ratio | | | | | | |
| P/TBV | | | | | | |
| Dividend Yield | | | | | | |

## Number Formatting Rules

Apply consistently across all sheets:
- Billions: Format as `$X.XXB` (e.g., `$1.30B`)
- Millions: Format as `$XXXMM` (e.g., `$809MM`, no decimal if `.00`)
- Percentages: `XX.X%` (one decimal)
- Basis points: `XX bps`
- Ratios: Two decimals (e.g., `1.23x`)
- No brackets for negatives — use minus sign

For the complete formula library, load `references/formula-library.md`.
For detailed credit scoring methodology, load `references/credit-scoring-methodology.md`.
