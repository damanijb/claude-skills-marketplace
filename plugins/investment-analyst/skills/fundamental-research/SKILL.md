---
name: fundamental-research
description: This skill should be used when the user asks to "research management", "analyze peers", "assess operating environment", "identify key drivers", "country economic health analysis", "fundamental research", "credit assessment", "macro analysis for banks", "management quality review", "peer comparison research", or needs to synthesize collected data into a structured research narrative covering management, competitive positioning, macro environment, and business drivers.
---

# Fundamental Research

Synthesize data from research providers, collected documents, and economic databases into a structured research narrative. This skill produces the analytical foundation that feeds into the financial model and report writer.

## Research Framework — 5 Pillars

### Pillar 1: Management Assessment

**What to evaluate:**
- Board composition, independence, and tenure
- CEO/CFO track record — strategic decisions over last 3-5 years
- Governance quality — AML/sanctions history, regulatory actions
- Executive compensation alignment with shareholder interests
- Management credibility — have they delivered on prior guidance?

**Data sources:**
- Annual report (governance section) — from `document-collector`
- Proxy statement / remuneration report
- Regulatory actions (ECB, Fed, OCC penalties) — from news and provider research
- Earnings call transcripts — management tone and consistency

**Output format:**
```markdown
## Management Assessment
- **Board**: [composition, independence ratio, recent changes]
- **Leadership**: [CEO/CFO tenure, strategic track record]
- **Governance**: [any flags: regulatory actions, AML issues, litigation]
- **Compensation**: [alignment with ROE/TSR targets]
- **Credibility**: [guidance accuracy over last 4 quarters]
- **Score**: [qualitative: Strong / Adequate / Weak]
```

### Pillar 2: Peer Comparison

**Peer selection criteria:**
- Same geography (e.g., Eurozone G-SIBs for a French bank)
- Similar size (total assets within 0.5x-2x range)
- Similar business mix (universal bank vs. specialist)
- Same regulatory regime (SSM-supervised for EU)

**Metrics to compare (quantitative):**
| Category | Metrics |
|----------|---------|
| Profitability | ROE, ROA, NIM, Cost/Income |
| Capital | CET1 ratio, leverage ratio, SREP buffer |
| Asset Quality | NPL ratio, NPL coverage, cost of risk |
| Liquidity | LCR, NSFR, loan/deposit ratio |
| Valuation | P/TBV, P/E, dividend yield |
| Size | Total assets, market cap, RWA |

**Standard peer groups by region:**
- **EU G-SIBs**: BNP Paribas, Société Générale, Deutsche Bank, Barclays, HSBC, UBS, Santander, ING, UniCredit, Intesa Sanpaolo
- **US Large Banks**: JPMorgan, Bank of America, Citigroup, Wells Fargo, Goldman Sachs, Morgan Stanley
- **Nordic Banks**: Nordea, Danske Bank, SEB, Swedbank, Handelsbanken, DNB

**Output**: Peer comparison table saved to `{workspace}/data/research-synthesis.json` for the financial model to consume.

### Pillar 3: Operating Environment

**Macro factors to assess:**

| Factor | Source | FRED Series ID |
|--------|--------|---------------|
| GDP growth | FRED / Eurostat | `GDP` (US), Chrome for EU |
| Unemployment | FRED | `UNRATE` (US) |
| Interest rates | FRED | `FEDFUNDS`, `DFF` |
| Yield curve | FRED | `T10Y2Y` (10Y-2Y spread) |
| Inflation | FRED | `CPIAUCSL` |
| Housing prices | FRED | `CSUSHPISA` (Case-Shiller) |
| Consumer confidence | FRED | `UMCSENT` |
| Bank lending standards | FRED | `DRTSCILM` (C&I loan tightening) |

**For European issuers, use Chrome to access:**
- ECB key rates: `https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/`
- Eurostat GDP: `https://ec.europa.eu/eurostat/databrowser/view/tec00115/default/table`
- EBA risk dashboard: `https://www.eba.europa.eu/risk-analysis-and-data/risk-dashboard`

**Use FRED MCP tools:**
```
fred_get_latest_value(series_id="GDP")
fred_get_series(series_id="FEDFUNDS", observation_start="2024-01-01")
fred_search_series(search_text="eurozone GDP")
```

**Assessment framework:**
- **Tailwinds**: Higher rates (NII benefit), strong employment (credit quality), loan demand
- **Headwinds**: Yield curve inversion (NIM compression), rising unemployment (provisions), geopolitical risk
- **Regulatory**: Basel III endgame, FRTB, digital euro impact, ESG requirements

### Pillar 4: Key Business Drivers

**Revenue drivers:**
- Net Interest Income (NII): Rate sensitivity, loan/deposit growth, mix shift
- Fee & Commission Income: Wealth management, investment banking, payments
- Trading Revenue: Fixed income, equities, derivatives — volatility dependency
- Other Income: Insurance, asset management, real estate

**Expense drivers:**
- Compensation: Headcount trends, variable comp, restructuring charges
- Technology: Digital transformation spend, cyber security
- Regulatory costs: Compliance, capital requirements, resolution fund contributions
- Restructuring: Branch closures, efficiency programs

**Credit quality drivers:**
- Loan growth by segment (corporate, retail, mortgage)
- Sector concentration risks
- Geographic exposure
- Stage 2 migration trends (early warning)
- Management overlay provisions

### Pillar 5: Country & Sovereign Health

**Key indicators:**
- Sovereign credit rating (Moody's/S&P/Fitch)
- Government debt / GDP ratio
- Current account balance
- Banking system stability (NPL system average, bank profitability)
- Sovereign-bank nexus (domestic sovereign bond holdings)

**Why this matters for bank credit:**
- Sovereign ceiling effects on bank ratings
- Domestic government bond portfolio losses/gains
- Country risk premium in funding costs
- Regulatory and political risk (e.g., windfall profit taxes)

## Synthesis Process

1. **Gather** data from all collected sources:
   - `{workspace}/data/provider-extracts/` (research provider data)
   - `{workspace}/data/documents/` (collected filings and transcripts)
   - FRED MCP queries (macro data)

2. **Analyze** each pillar independently using the frameworks above

3. **Cross-reference** findings across sources:
   - Do provider opinions align with raw financial data?
   - Does management's narrative match quantitative trends?
   - Are peer comparisons consistent across data sources?

4. **Synthesize** into `{workspace}/data/research-synthesis.json`:
   ```json
   {
     "issuer": "BNP Paribas",
     "analysisDate": "2026-03-07",
     "management": { "score": "Strong", "keyFindings": [...] },
     "peers": { "group": [...], "relativePosition": {...} },
     "environment": { "outlook": "Neutral", "tailwinds": [...], "headwinds": [...] },
     "drivers": { "revenue": [...], "expenses": [...], "credit": [...] },
     "country": { "sovereignRating": "Aa2", "outlook": "Stable" },
     "overallAssessment": "..."
   }
   ```

For the detailed bank analysis template, load `references/bank-analysis-template.md`.
For FRED series IDs and ECB data sources, load `references/macro-indicators.md`.
