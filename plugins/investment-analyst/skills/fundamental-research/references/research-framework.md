# Research Framework — Detailed Analysis Guide

## Pillar 1: Management Assessment — Deep Dive

### Board Analysis Checklist
- [ ] Total board size (typical: 10-15 for large banks)
- [ ] Independent directors ratio (target: >50%)
- [ ] Average tenure (watch for entrenchment >12 years)
- [ ] Diversity metrics (gender, nationality, expertise)
- [ ] Recent board changes (signal of strategic shifts?)
- [ ] Risk committee chair — background and expertise
- [ ] Audit committee — financial expertise

### CEO/CFO Evaluation
- How long in role? (<2 years = still executing predecessor's strategy)
- Previous roles — internal promotion vs. external hire
- Key strategic decisions:
  - Acquisitions — were they value accretive?
  - Divestitures — strategic focus or distress sale?
  - Capital allocation — buybacks vs. organic growth
  - Technology investments — digital transformation progress
- Crisis management track record (if applicable)

### Governance Red Flags
- AML/BSA violations (severity and remediation)
- Regulatory enforcement actions
- Material litigation
- Whistleblower complaints
- Executive turnover (>2 C-suite departures in 12 months)
- Related-party transactions

### Compensation Analysis
- CEO total comp vs. peer median
- % variable vs. fixed
- Performance metrics tied to comp:
  - ROE target? → Aligns with profitability
  - TSR target? → Aligns with shareholders
  - ESG targets? → Signal of strategic priorities
- Clawback provisions — strength and trigger events
- Insider buying/selling patterns

---

## Pillar 2: Peer Comparison — Methodology

### Step 1: Peer Selection
Select 4-8 peers using these criteria (in priority order):
1. **Same regulatory regime** (SSM for EU, Fed for US)
2. **Similar asset size** (0.5x to 2x target's total assets)
3. **Similar business mix** (universal vs. investment bank vs. retail)
4. **Same geographic exposure** (domestic market overlap)

### Step 2: Data Collection
For each peer, collect the following for the last 5 quarters:

**Income Statement:**
- Total revenue
- Net interest income
- Non-interest income (fees, trading, other)
- Provision for credit losses
- Operating expenses
- Net income

**Balance Sheet:**
- Total assets
- Gross loans
- Total deposits
- Risk-weighted assets
- CET1 capital

**Ratios:**
- ROE, ROA
- NIM
- Cost/income ratio
- NPL ratio, NPL coverage
- CET1 ratio, leverage ratio
- LCR
- Loan/deposit ratio
- Dividend yield, payout ratio

### Step 3: Relative Positioning
For each metric:
1. Rank the issuer among peers (1 = best)
2. Calculate percentile position
3. Calculate distance from peer median (in % or bps)
4. Flag outliers (>1 standard deviation from peer mean)

### Step 4: Trend Comparison
Compare 5-quarter trends:
- Is the issuer improving faster or slower than peers?
- Are trends converging or diverging?
- Identify structural advantages or disadvantages

---

## Pillar 3: Operating Environment — Analysis Framework

### Interest Rate Impact Analysis

**NII Sensitivity (critical for banks):**
- Parallel shift sensitivity: NII impact of +100bp / -100bp rate shock
- Curve shape sensitivity: Steepening vs. flattening impact
- Repricing gap: Asset vs. liability repricing mismatch
- Fixed/floating mix: Proportion of fixed-rate loans vs. floating

**Rate Environment Assessment:**
| Environment | Impact on Banks | NII Effect |
|-------------|----------------|------------|
| Rising rates, steep curve | Positive | Strong NII growth |
| Rising rates, flat curve | Mixed | Modest NII, margin pressure |
| Falling rates, steep curve | Mixed | NII pressure, credit demand up |
| Falling rates, flat curve | Negative | NII compression, credit stress |

### Credit Cycle Assessment

**Leading indicators (monitor via FRED + news):**
- Consumer delinquency rates (`DRSFRMACBS`)
- C&I loan delinquencies
- Credit card delinquencies (`DRCCLACBS`)
- Bankruptcy filings
- Unemployment trends
- PMI/ISM manufacturing and services

**Credit cycle position:**
| Phase | Characteristics | Bank Impact |
|-------|----------------|-------------|
| Expansion | Low defaults, strong loan growth | High earnings, low provisions |
| Peak | Tight lending standards, high leverage | Maximum NII, rising stage 2 |
| Contraction | Rising defaults, falling demand | Provision surge, earnings decline |
| Trough | High NPLs, deleveraging | Maximum provisions, write-offs |
| Recovery | Falling NPLs, provision releases | Earnings recovery, reserve releases |

### Regulatory Environment

**Current key regulatory themes:**
- Basel III endgame / Basel IV implementation
- FRTB (Fundamental Review of the Trading Book)
- Resolution planning (TLAC/MREL requirements)
- Climate risk stress testing
- Digital operational resilience (DORA for EU)
- Anti-money laundering (6AMLD)

---

## Pillar 4: Key Drivers — Quantitative Framework

### Revenue Decomposition

```
Total Revenue = NII + Non-Interest Income

NII = (Earning Assets × NIM)
    = (Loans × Loan Yield - Deposits × Deposit Cost) + Securities Income

Non-Interest Income = Fee Income + Trading Revenue + Other
  Fee Income = Asset Management + Investment Banking + Transaction Banking + Insurance
  Trading Revenue = FICC + Equities + Derivatives
```

### Revenue Driver Analysis

For each component, assess:
1. **Historical growth rate** (5Q CAGR)
2. **Peer-relative growth** (above or below peer median)
3. **Sustainability** (one-time vs. recurring)
4. **Sensitivity** to external factors (rates, markets, volumes)

### Expense Decomposition

```
Operating Expenses = Compensation + Non-Compensation
  Compensation = Salaries + Variable (Bonuses) + Benefits
  Non-Compensation = Technology + Occupancy + Professional Fees + Regulatory + Other
```

### Efficiency Analysis
- Cost/income ratio trend (improving or deteriorating?)
- Jaws ratio = Revenue growth - Expense growth (positive jaws = improving efficiency)
- Cost per employee trend
- Revenue per employee trend
- Branch footprint changes
- Technology investment as % of revenue

---

## Pillar 5: Country Health — Sovereign-Bank Nexus

### Sovereign Rating Impact on Banks

| Sovereign Action | Bank Impact |
|-----------------|-------------|
| Sovereign downgrade | Bank rating ceiling may lower, funding costs rise |
| Sovereign outlook negative | Banks on review, CDS widens |
| Government debt crisis | Domestic bond portfolio losses, deposit flight risk |
| Political instability | Regulatory uncertainty, FX volatility |

### Key Country Metrics

| Metric | Green | Amber | Red |
|--------|-------|-------|-----|
| Debt/GDP | <60% | 60-100% | >100% |
| Budget deficit/GDP | <3% | 3-5% | >5% |
| Current account/GDP | Surplus | Small deficit | Large deficit |
| GDP growth | >2% | 0-2% | <0% |
| Unemployment | <5% | 5-10% | >10% |
| Banking system NPL | <3% | 3-7% | >7% |

### Domestic Sovereign Bond Exposure
- What % of the bank's securities portfolio is domestic sovereign debt?
- Mark-to-market risk under rate scenarios
- Concentration limit vs. regulatory expectation
- Comparison to peer sovereign exposure
