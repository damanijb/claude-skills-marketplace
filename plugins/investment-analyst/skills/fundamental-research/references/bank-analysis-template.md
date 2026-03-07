# Bank Credit Analysis Template

## Structure

This template provides the analytical framework for a bank-specific credit assessment. Follow this structure when synthesizing research from all collected sources.

---

## 1. Franchise Overview

- **Legal entity**: Full legal name, ticker, LEI
- **Domicile**: Country of incorporation, primary regulator
- **Business model**: Universal bank / investment bank / retail / specialty
- **Geographic footprint**: Revenue by region, branch count
- **Market position**: Domestic market share (deposits, loans, mortgages)
- **Systemically important**: G-SIB? D-SIB? SREP bucket?
- **Total assets**: Current and 5Y trend
- **Employee count**: Current and trend
- **Credit ratings**: Moody's / S&P / Fitch — long-term, short-term, outlook

---

## 2. Income Statement Analysis (Top-Line to Bottom-Line)

### Net Interest Income (NII)
- NII amount and YoY/QoQ growth
- Net interest margin (NIM) and trend
- NII as % of total revenue (dependency metric)
- Rate sensitivity: Disclosed +/-100bp impact
- Loan/deposit repricing dynamics
- Deposit beta (% of rate changes passed to depositors)
- Outlook: Management guidance on NII trajectory

### Non-Interest Income
- Fee & commission income (% of revenue, growth)
- Key fee lines: wealth management, investment banking, payments, insurance
- Trading revenue (FICC, equities — volatility sensitivity)
- Other income (one-time items, disposal gains)
- Diversification assessment: How dependent on NII?

### Provision for Credit Losses (PCL)
- Provision amount and cost of risk (bps of average loans)
- Stage 1/2/3 migration trends (IFRS 9) or CECL reserves
- Management overlays (conservatism assessment)
- Sector-specific provisions (CRE, leveraged lending, consumer)
- Coverage ratio trend
- Comparison to peer provisioning

### Operating Expenses
- Total opex and cost/income ratio
- Compensation: Fixed vs. variable, headcount trend
- Non-comp: Technology spend, regulatory costs, restructuring
- Jaws ratio (revenue growth minus cost growth)
- Efficiency programs: Targets, progress, credibility
- Restructuring charges: One-time or recurring?

### Net Income & Returns
- Net income and EPS (diluted)
- ROE and ROA
- DuPont decomposition: margin × turnover × leverage
- Effective tax rate and trend
- Exceptional items (adjust for underlying performance)
- Dividend per share, payout ratio, buyback programs

---

## 3. Balance Sheet & Capital

### Asset Quality
- **Gross NPLs / Total Loans**: Trend over 5Q
- **NPL Coverage Ratio**: Provisions / NPLs
- **Cost of Risk**: PCL / Average Gross Loans (annualized, bps)
- **Stage 2 Loans / Total Loans**: Early warning indicator
- **Loan Book Composition**: Corporate, retail, mortgage, CRE, consumer
- **Sector Concentrations**: Top 5 sector exposures
- **Geographic Concentration**: Top 5 country exposures
- **Forbearance**: Forborne loan stock and trend
- **Write-offs**: Gross write-offs and recovery rates

### Capital Adequacy
- **CET1 Ratio**: Current vs. SREP requirement vs. management target
- **CET1 Buffer**: Distance above SREP requirement (bps)
- **Tier 1 Ratio**: Including AT1 instruments
- **Total Capital Ratio**: Including Tier 2
- **Leverage Ratio**: Tier 1 / Total Exposure (min 3% EU, 4-5% US)
- **RWA Composition**: Credit, market, operational risk breakdown
- **RWA Density**: RWA / Total Assets (lower = more optimized)
- **MREL / TLAC**: Subordinated instruments for resolution
- **Capital Generation**: Organic CET1 generation (bps per quarter)
- **Capital Distribution**: Dividends + buybacks as % of net income

### Liquidity & Funding
- **LCR**: HQLA / Net Cash Outflows 30d (regulatory minimum 100%)
- **NSFR**: Available Stable Funding / Required Stable Funding (min 100%)
- **Loan/Deposit Ratio**: Self-funding assessment
- **Deposit Mix**: Retail vs. corporate vs. wholesale
- **Deposit Stability**: % covered/insured, stickiness assessment
- **Wholesale Funding**: Bonds outstanding, maturity profile
- **Central Bank Funding**: TLTRO / discount window usage (if any)
- **Funding Cost Trend**: Weighted average cost of funding

---

## 4. Segment Analysis

For each business segment, assess:

| Metric | What to Evaluate |
|--------|-----------------|
| Revenue | Size, growth, contribution to group |
| Profitability | Segment ROE, cost/income |
| Asset Quality | Segment-specific NPL rate |
| Capital Allocation | RWA allocation, return on allocated capital |
| Strategy | Growth/mature/wind-down? |

Common segments for universal banks:
- **Retail Banking**: Domestic consumer and SME
- **Corporate & Institutional Banking (CIB)**: Corporate lending, trade finance, FX, rates
- **Investment Banking**: Advisory, capital markets, trading
- **Wealth/Asset Management**: Private banking, fund management
- **Insurance** (if applicable)
- **Other/Corporate Center**: Treasury, legacy portfolios, shared costs

---

## 5. Credit Rating Assessment

### Internal Score Components
Map findings to the credit scoring model dimensions:

1. **Capital**: CET1, leverage, buffer over requirements
2. **Profitability**: ROE, ROA, NIM, cost/income
3. **Asset Quality**: NPL ratio, coverage, cost of risk
4. **Efficiency**: Cost/income, revenue/employee
5. **Liquidity**: LCR, NSFR, loan/deposit ratio
6. **External Ratings**: Agency ratings, outlook, recent actions

### Upgrade/Downgrade Triggers
**Potential upgrade factors:**
- CET1 ratio improvement >100bp with sustainable trend
- ROE consistently above cost of equity for 4+ quarters
- NPL ratio declining toward peer median
- Positive rating agency outlook
- Successful strategic execution (M&A integration, digital transformation)

**Potential downgrade factors:**
- CET1 ratio approaching or breaching SREP requirement
- Sharp NPL increase or provision spike
- Cost overruns on transformation programs
- Negative rating agency actions
- Regulatory sanctions or material litigation
- Sovereign downgrade of home country

### Rating Migration Probability Framework
```
Strong Positive Trend (3Q improving, above peers) → Upgrade probability: 20-30%
Stable with Positive Bias (stable, at/above peers) → Upgrade probability: 5-10%
Stable (no clear trend) → Migration probability: <5% either direction
Stable with Negative Bias (stable, below peers) → Downgrade probability: 5-10%
Negative Trend (3Q deteriorating, below peers) → Downgrade probability: 20-30%
Stress Scenario (capital breach, liquidity event) → Downgrade probability: 50%+
```

---

## 6. Risk Assessment Summary

| Risk Category | Assessment | Trend | Key Factor |
|--------------|------------|-------|------------|
| Credit Risk | Low/Medium/High | Improving/Stable/Deteriorating | [main driver] |
| Market Risk | Low/Medium/High | Improving/Stable/Deteriorating | [main driver] |
| Liquidity Risk | Low/Medium/High | Improving/Stable/Deteriorating | [main driver] |
| Operational Risk | Low/Medium/High | Improving/Stable/Deteriorating | [main driver] |
| Regulatory Risk | Low/Medium/High | Improving/Stable/Deteriorating | [main driver] |
| Strategic Risk | Low/Medium/High | Improving/Stable/Deteriorating | [main driver] |
