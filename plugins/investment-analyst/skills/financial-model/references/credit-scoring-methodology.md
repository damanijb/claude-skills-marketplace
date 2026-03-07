# Credit Scoring Methodology

## Overview

The custom credit scoring model evaluates bank creditworthiness across 6 dimensions, each scored 0-10 based on quantitative metrics. The weighted composite score drives upgrade/downgrade probability estimates.

## Dimension Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Capital Adequacy | 20% | First loss absorption capacity — most critical for credit |
| Profitability | 20% | Earnings power to absorb losses and generate capital |
| Asset Quality | 20% | Current and forward-looking credit risk in the loan book |
| Efficiency | 15% | Cost management and operating leverage |
| Liquidity | 15% | Ability to meet short-term obligations under stress |
| External Ratings | 10% | Market consensus and additional information |

## Detailed Scoring Bands

### Capital Adequacy (20%)

| Sub-Metric | Weight | Score 10 | Score 8 | Score 6 | Score 4 | Score 2 | Score 0 |
|-----------|--------|----------|---------|---------|---------|---------|---------|
| CET1 Ratio | 40% | >16% | 14-16% | 12-14% | 10-12% | 8-10% | <8% |
| CET1 Buffer over SREP | 35% | >500bp | 400-500bp | 300-400bp | 200-300bp | 100-200bp | <100bp |
| Leverage Ratio | 25% | >6% | 5-6% | 4-5% | 3.5-4% | 3-3.5% | <3% |

**Interpolation**: For values between thresholds, linearly interpolate the score. Example: CET1 of 15% = Score 9 (midpoint between 14% at 8 and 16% at 10).

### Profitability (20%)

| Sub-Metric | Weight | Score 10 | Score 8 | Score 6 | Score 4 | Score 2 | Score 0 |
|-----------|--------|----------|---------|---------|---------|---------|---------|
| ROE | 40% | >15% | 12-15% | 9-12% | 6-9% | 3-6% | <3% |
| Cost/Income | 35% | <45% | 45-50% | 50-55% | 55-65% | 65-75% | >75% |
| NIM | 25% | >2.0% | 1.5-2.0% | 1.2-1.5% | 0.9-1.2% | 0.6-0.9% | <0.6% |

**Note on Cost/Income**: Lower is better — scoring is inverted.

### Asset Quality (20%)

| Sub-Metric | Weight | Score 10 | Score 8 | Score 6 | Score 4 | Score 2 | Score 0 |
|-----------|--------|----------|---------|---------|---------|---------|---------|
| NPL Ratio | 40% | <0.5% | 0.5-1% | 1-2% | 2-3% | 3-5% | >5% |
| NPL Coverage | 35% | >120% | 100-120% | 80-100% | 60-80% | 40-60% | <40% |
| Cost of Risk (bps) | 25% | <10 | 10-20 | 20-35 | 35-50 | 50-80 | >80 |

**Note on NPL Ratio and Cost of Risk**: Lower is better — scoring is inverted.

### Efficiency (15%)

| Sub-Metric | Weight | Score 10 | Score 8 | Score 6 | Score 4 | Score 2 | Score 0 |
|-----------|--------|----------|---------|---------|---------|---------|---------|
| Cost/Income | 50% | <45% | 45-50% | 50-55% | 55-65% | 65-75% | >75% |
| Revenue/Employee ($K) | 50% | >500 | 400-500 | 300-400 | 200-300 | 100-200 | <100 |

### Liquidity (15%)

| Sub-Metric | Weight | Score 10 | Score 8 | Score 6 | Score 4 | Score 2 | Score 0 |
|-----------|--------|----------|---------|---------|---------|---------|---------|
| LCR | 40% | >180% | 150-180% | 130-150% | 110-130% | 100-110% | <100% |
| NSFR | 30% | >120% | 110-120% | 105-110% | 100-105% | 95-100% | <95% |
| Loan/Deposit | 30% | <80% | 80-90% | 90-100% | 100-110% | 110-130% | >130% |

**Note on Loan/Deposit**: Lower is better (more deposit-funded).

### External Ratings (10%)

| Sub-Metric | Weight | Score 10 | Score 8 | Score 6 | Score 4 | Score 2 | Score 0 |
|-----------|--------|----------|---------|---------|---------|---------|---------|
| Moody's LT | 60% | Aaa-Aa2 | Aa3-A1 | A2-A3 | Baa1-Baa2 | Baa3-Ba1 | Ba2 or below |
| Outlook | 40% | Positive (all) | Mixed positive | Stable (all) | Mixed negative | Negative (all) | Under review neg |

**Rating mapping (Moody's numeric scale):**
```
Aaa=10, Aa1=9.5, Aa2=9, Aa3=8.5, A1=8, A2=7.5, A3=7
Baa1=6.5, Baa2=6, Baa3=5.5, Ba1=5, Ba2=4.5, Ba3=4
B1=3, B2=2.5, B3=2, Caa1=1.5, Caa2=1, Caa3=0.5, Ca/C=0
```

---

## Composite Score Calculation

```
For each dimension:
  Dimension Score = Σ(sub-metric i score × sub-metric i weight)

Composite Score = Σ(Dimension j Score × Dimension j weight)
```

### Composite Score Interpretation

| Composite Score | Credit Assessment | Equivalent Rating Range |
|----------------|-------------------|------------------------|
| 8.5 - 10.0 | Very Strong | Aa range |
| 7.0 - 8.4 | Strong | A range |
| 5.5 - 6.9 | Adequate | Baa range |
| 4.0 - 5.4 | Marginal | Ba range |
| 2.5 - 3.9 | Weak | B range |
| 0.0 - 2.4 | Very Weak | Caa range and below |

---

## Upgrade/Downgrade Probability Model

### Factor Weights

| Factor | Weight | Description |
|--------|--------|-------------|
| Composite Score Level | 30% | Current absolute score position |
| 3-Quarter Trend | 25% | Direction and magnitude of score change |
| Peer Relative Position | 20% | Score vs. peer median and distribution |
| Agency Outlook | 15% | Rating agency forward guidance |
| Macro Sensitivity | 10% | Vulnerability to macro stress scenarios |

### Scoring Each Factor

**Composite Score Level (30%):**
- Score ≥ 8: Upgrade contribution = +15%, Downgrade contribution = +0%
- Score 6-8: Upgrade = +5%, Downgrade = +2%
- Score 4-6: Upgrade = +2%, Downgrade = +5%
- Score < 4: Upgrade = +0%, Downgrade = +15%

**3-Quarter Trend (25%):**
- Improving >0.5 points: Upgrade = +12%, Downgrade = +0%
- Improving 0.1-0.5: Upgrade = +6%, Downgrade = +1%
- Stable ±0.1: Upgrade = +2%, Downgrade = +2%
- Deteriorating 0.1-0.5: Upgrade = +1%, Downgrade = +6%
- Deteriorating >0.5: Upgrade = +0%, Downgrade = +12%

**Peer Relative Position (20%):**
- Top quartile: Upgrade = +8%, Downgrade = +0%
- 2nd quartile: Upgrade = +4%, Downgrade = +1%
- 3rd quartile: Upgrade = +1%, Downgrade = +4%
- Bottom quartile: Upgrade = +0%, Downgrade = +8%

**Agency Outlook (15%):**
- All positive: Upgrade = +10%, Downgrade = +0%
- Mixed/stable: Upgrade = +2%, Downgrade = +2%
- All negative: Upgrade = +0%, Downgrade = +10%

**Macro Sensitivity (10%):**
- Low sensitivity to stress: Upgrade = +3%, Downgrade = +1%
- Medium: Upgrade = +1%, Downgrade = +3%
- High: Upgrade = +0%, Downgrade = +5%

### Final Probability Calculation

```
Upgrade Probability = Σ(factor upgrade contribution)
Downgrade Probability = Σ(factor downgrade contribution)

Cap both at 50% maximum.
Round to nearest 5%.
```

### Example Calculation

| Factor | Upgrade Contribution | Downgrade Contribution |
|--------|---------------------|----------------------|
| Score Level: 7.2 (Strong) | +5% | +2% |
| Trend: +0.3 (Improving) | +6% | +1% |
| Peer: 2nd quartile | +4% | +1% |
| Outlook: Stable | +2% | +2% |
| Macro: Low sensitivity | +3% | +1% |
| **Total** | **20%** | **7%** |

Result: 20% upgrade probability, 7% downgrade probability → net positive bias.
