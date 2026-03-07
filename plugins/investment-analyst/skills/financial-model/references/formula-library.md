# Formula Library — Bank Financial Analysis

## Capital Ratios

```
CET1 Ratio = CET1 Capital / Total RWA
Tier 1 Ratio = (CET1 + AT1 Capital) / Total RWA
Total Capital Ratio = (CET1 + AT1 + Tier 2) / Total RWA
Leverage Ratio = Tier 1 Capital / Total Exposure Measure
RWA Density = Total RWA / Total Assets

CET1 Buffer = CET1 Ratio - SREP Requirement (in bps)
Organic Capital Generation = (Retained Earnings for Quarter / Average RWA) × 4 (annualized, in bps)
```

## Profitability Ratios

```
ROE = Net Income / Average Total Equity (annualized)
ROA = Net Income / Average Total Assets (annualized)
ROTE = Net Income / Average Tangible Equity (annualized)
NIM = (Interest Income - Interest Expense) / Average Earning Assets (annualized)
Cost/Income = Operating Expenses / Total Operating Income
Jaws = Revenue Growth Rate - Expense Growth Rate (in percentage points)
Pre-Provision Operating Profit (PPOP) = Total Revenue - Operating Expenses
PPOP/Average Assets = PPOP / Average Total Assets (annualized)
Effective Tax Rate = Income Tax / Pre-Tax Income
```

## Asset Quality Ratios

```
NPL Ratio = Non-Performing Loans / Gross Loans
NPL Coverage = Allowance for Credit Losses / Non-Performing Loans
Cost of Risk = Provision for Credit Losses / Average Gross Loans (annualized, in bps)
  bps conversion: (Provision / Average Loans) × 10,000

Stage 2 Ratio = Stage 2 Loans / Total Loans (IFRS 9)
Texas Ratio = (NPLs + OREO) / (Tangible Equity + Loan Loss Reserves)
Net Charge-Off Rate = (Gross Charge-Offs - Recoveries) / Average Loans (annualized)
Reserve Ratio = Allowance / Total Loans
```

## Liquidity Ratios

```
LCR = High-Quality Liquid Assets / Total Net Cash Outflows (30-day)
NSFR = Available Stable Funding / Required Stable Funding
Loan/Deposit Ratio = Net Loans / Total Customer Deposits
Cash Ratio = Cash & Central Bank / Total Assets
Liquid Asset Ratio = (Cash + Securities) / Total Assets
```

## DuPont Decomposition

### Classic 3-Factor
```
ROE = Profit Margin × Asset Turnover × Equity Multiplier
    = (Net Income / Revenue) × (Revenue / Total Assets) × (Total Assets / Equity)
```

### Bank-Specific Extended DuPont
```
ROE = NII Yield × Asset Utilization + Fee Yield - Cost Efficiency - Provision Impact - Tax Impact

Where:
NII Yield = NII / Average Equity
Fee Yield = Non-Interest Income / Average Equity
Cost Efficiency = Operating Expenses / Average Equity
Provision Impact = Provisions / Average Equity
Tax Impact = Taxes / Average Equity

Validation: NII Yield + Fee Yield - Cost Efficiency - Provision Impact - Tax Impact ≈ ROE
```

### Waterfall Bridge (Quarter-over-Quarter)
```
ROE Change = ΔNII Contribution + ΔFee Contribution + ΔCost Impact + ΔProvision Impact + ΔTax Impact

Where each Δ = (Component / Avg Equity)_current - (Component / Avg Equity)_prior
```

## Funding & Debt Metrics

```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tc))
  Where: E = Market Cap, D = Total Debt, V = E + D
  Re = Cost of Equity (CAPM: Rf + β × ERP)
  Rd = Cost of Debt (weighted average coupon / yield)
  Tc = Corporate Tax Rate

Weighted Average Cost of Funding = Σ(Funding Source Amount × Cost) / Total Funding
Deposit Beta = Change in Deposit Rate / Change in Policy Rate (over same period)
```

## Per Share Metrics

```
EPS (Diluted) = Net Income / Weighted Average Diluted Shares
TBVPS = (Total Equity - Goodwill - Intangibles) / Shares Outstanding
DPS = Total Dividends Paid / Shares Outstanding
Payout Ratio = DPS / EPS (or Total Dividends / Net Income)
P/E = Share Price / EPS
P/TBV = Share Price / TBVPS
Dividend Yield = DPS / Share Price
```

## Pro Forma Estimation Formulas

### NII Projection
```
NII_est = NII_current × (1 + NII_growth_rate)
NII_growth_rate = f(rate sensitivity, loan growth, deposit repricing)

Simple approach:
NII_est = (Avg Earning Assets × Projected NIM)
Avg Earning Assets_est = Current × (1 + loan_growth_rate)
Projected NIM = Current NIM + (ΔRate × NII_sensitivity / NII_current)
```

### Provision Projection
```
PCL_est = Average Gross Loans_est × (Cost of Risk Target / 10,000)
Cost of Risk Target = Management guidance OR trailing 4Q average (if stable)
```

### Opex Projection
```
Opex_est = Revenue_est × Cost/Income Target
OR
Opex_est = Opex_current × (1 + opex_growth_rate)
opex_growth_rate = management guidance rate OR trailing 4Q CAGR
```

### Capital Projection
```
CET1_est = CET1_current + Net Income_est - Dividends_est - AT1 Coupons - RWA Growth Impact
CET1 Ratio_est = CET1_est / RWA_est
RWA_est = RWA_current × (1 + RWA_growth_rate)
```

## Number Formatting Reference

| Value Range | Format | Example |
|------------|--------|---------|
| ≥ $1 billion | $X.XXB | $1.30B |
| $1-999 million | $XXXMM | $809MM |
| < $1 million | $X.XK or $X,XXX | $45.2K |
| Percentage | X.X% | 14.2% |
| Basis points | XX bps | 35 bps |
| Ratio | X.XXx | 1.23x |
| Negative | -$XMM (no brackets) | -$23MM |
| Ending in .00 | Drop decimal | $809MM not $809.00MM |
