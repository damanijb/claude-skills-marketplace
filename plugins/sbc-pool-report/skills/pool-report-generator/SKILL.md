---
name: pool-report-generator
description: >
  Generate monthly investment pool reports for San Bernardino County's treasury
  portfolio. This skill should be used when the user mentions "pool report",
  "monthly report", "treasury report", "portfolio report", "board presentation",
  "investment report", or wants to generate any portfolio summary, compliance
  check, or performance analysis as a slide deck. Also triggers when asked to
  "create slides about the portfolio", "prepare board materials", or "run the
  report for [month]".
version: 2.0.0
---

# Pool Report Generator v2

Generate publication-quality monthly pool reports for the San Bernardino County
Treasurer's investment portfolio. Output is a branded PowerPoint (.pptx) presentation
ready for the Board of Supervisors and authorized participants.

**Key v2 features:**
- Parallel sub-agent architecture for faster generation
- Rich economic storytelling section (8-9 slides) with trend charts and plain-English narratives
- Web research for current market themes and Fed policy context

## Before Starting

1. Read the PPTX skill for PptxGenJS syntax and best practices.
2. Read ALL reference files in `references/`:
   - `design-system.md` — Colors, fonts, layout geometry
   - `data-dictionary.md` — Database schema, SQL queries, FRED series
   - `policy-limits.md` — IPS Schedule I compliance limits
   - `chart-specs.md` — Chart types, sizes, colors (portfolio + economic)
   - `tone-guide.md` — Institutional voice and language rules
   - `economic-research.md` — Economic research methodology, writing guidelines, slide templates

## Architecture: Parallel Phase Pipeline

This plugin uses the **Task tool** to launch sub-agents that work in parallel,
cutting total generation time significantly.

```
Phase 0: Setup (read refs, determine params)
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
Phase 1A   Phase 1B     Phase 1C
SQL Pull   FRED Pull    Economic Research
(Agent)    (Agent)      (Agent - WebSearch)
    │         │            │
    └────┬────┘            │
         ▼                 ▼
      Phase 2A          Phase 2B
      Transform +       Economic Narrative
      Charts (Agent)    Writing (Agent)
         │                 │
         └────────┬────────┘
                  ▼
            Phase 3: Build PPTX (sequential)
                  ▼
            Phase 4: QA & Deliver (sequential)
```

---

## Phase 0: Setup

**Runs on main Claude (sequential).**

1. Read all reference files listed in "Before Starting" above.
2. Determine report parameters:
   - **Report date**: Use argument if provided (YYYYMMDD), else query DB for latest.
   - **Format**: PPTX (always).
   - If the user says "generate the pool report" without detail, use the latest date and full report.
3. Create a TodoWrite task list to track progress through the phases.

---

## Phase 1: Data Gathering (3 Parallel Agents)

Launch **three Task agents simultaneously** in a single message. Each agent writes
its output to a JSON file that downstream phases will read.

### Phase 1A — SQL Data Pull (general-purpose agent)

**Prompt template:**
```
You are pulling portfolio data from Azure SQL for the SBC Investment Pool Report.
Report date: {report_date_int}

Use the sql_execute_query MCP tool. The connection to treasurer.database.windows.net / ATC_TREASURER is pre-configured.

Run these queries:

1. Holdings extract:
SELECT Cat_Desc, SubCat_Desc, Sec_Cd,
    CAST(Par_Val AS FLOAT) AS Par_Val,
    CAST(Book_Val AS FLOAT) AS Book_Val,
    CAST(Market_Val AS FLOAT) AS Market_Val,
    CAST(Book_Yld AS FLOAT) AS Book_Yld,
    CAST(Dura AS FLOAT) AS Dura,
    CAST(Rate AS FLOAT) AS Rate,
    Mat_dt, SP, Mdy,
    CAST(Accru_Todate AS FLOAT) AS Accru_Todate,
    Cusip, Short_Desc, Long_Desc_1, [Group]
FROM portfolio.fis_gold_extract
WHERE Rpt_Date = {report_date_int}
ORDER BY Market_Val DESC

2. Cash flow data:
SELECT TOP 100 * FROM portfolio.cashflow ORDER BY Date DESC

Write the holdings results as JSON to /tmp/sbc_holdings.json
Write the cashflow results as JSON to /tmp/sbc_cashflow.json
Print "PHASE_1A_COMPLETE" when done.
```

### Phase 1B — FRED Data Pull (general-purpose agent)

**Prompt template:**
```
You are pulling economic data from FRED for the SBC Investment Pool Report.

Use the fred_get_latest_value MCP tool for current readings of each series.
Use the fred_get_series MCP tool with observation_start="2025-02-01" to get
12 months of history for trend charts.

Pull these series (run multiple fred calls in parallel where possible):

RATE INDICATORS: FEDFUNDS, SOFR, DTB3, DTB6, DGS1, DGS2, DGS5, DGS10, DGS30
INFLATION: CPIAUCSL, PCEPI
EMPLOYMENT: UNRATE
GROWTH: A191RL1Q225SBEA
SPREADS: BAMLC0A2CAA, BAMLC0A4CBBB, BAMLH0A0HYM2, T10Y2Y
MORTGAGE: MORTGAGE30US

For each series, save:
- latest: {value, date}
- history: [{date, value}, ...] (12 months)

Write the combined result as JSON to /tmp/sbc_fred_data.json with structure:
{
  "latest": { "FEDFUNDS": {value, date}, ... },
  "history": { "FEDFUNDS": [{date, value}, ...], ... }
}
Print "PHASE_1B_COMPLETE" when done.
```

### Phase 1C — Economic Research (general-purpose agent)

**Prompt template:**
```
You are researching current economic conditions for a county treasury Board presentation.
Read the economic research guide at: {plugin_root}/skills/pool-report-generator/references/economic-research.md

Use WebSearch to research these topics:

1. FEDERAL RESERVE: Latest FOMC decision, rate changes, forward guidance, dot plot expectations
   Search: "Federal Reserve FOMC decision {current_month} {current_year}"
   Search: "Fed interest rate outlook {current_year}"

2. INFLATION: Latest CPI reading, trend direction, Fed's 2% target progress
   Search: "CPI inflation {current_month} {current_year}"
   Search: "inflation outlook United States {current_year}"

3. EMPLOYMENT: Latest jobs report, unemployment rate, labor market health
   Search: "unemployment rate jobs report {current_month} {current_year}"

4. CREDIT MARKETS: Corporate bond spreads, issuance trends, default rates
   Search: "investment grade credit spreads {current_year}"
   Search: "corporate bond market outlook {current_year}"

5. FIXED-INCOME THEMES: Top 2-3 themes affecting government/municipal bond investors
   Search: "treasury market outlook {current_month} {current_year}"
   Search: "municipal bond market {current_year}"

For each topic, write:
- headline: one-sentence summary
- detail: 2-3 sentences of context in PLAIN ENGLISH for non-finance readers
- data_points: key numbers (rates, percentages, changes)
- portfolio_impact: 1-2 sentences on what this means for a $16B county investment pool

Also identify the top 2-3 MARKET THEMES — major stories affecting fixed-income investors.
For each theme:
- title: short headline (e.g., "Fed Signals Rate Cuts Ahead")
- narrative: 3-4 sentences explaining the theme in simple terms
- chart_suggestion: what FRED series would best illustrate this theme
- portfolio_impact: specific implication for the county portfolio

Write everything to /tmp/sbc_economic_research.json
Print "PHASE_1C_COMPLETE" when done.
```

---

## Phase 2: Processing (2 Parallel Agents)

Wait for ALL Phase 1 agents to complete. Then launch **two agents simultaneously**.

### Phase 2A — Data Transformation + Chart Generation (general-purpose agent)

**Prompt template:**
```
You are transforming portfolio data and generating charts for the SBC Pool Report.

INPUT FILES:
- /tmp/sbc_holdings.json (raw holdings from Azure SQL)
- /tmp/sbc_cashflow.json (cash flow data)
- /tmp/sbc_fred_data.json (FRED economic data with latest + 12mo history)

STEP 1: TRANSFORM PORTFOLIO DATA
Read the data_transformer.py script at {plugin_root}/skills/pool-report-generator/scripts/data_transformer.py
Apply all transformations: security type mapping, NAV fix, duration filter, yield conversion, implied ratings.
Calculate all aggregates: sectors, credit quality, maturity distribution, compliance, issuer concentration, monthly income, horizon analysis.
Include the FRED latest values in the output.

Save transformed data to /tmp/sbc_report_data.json

STEP 2: GENERATE PORTFOLIO CHARTS (save all to /tmp/charts/)
Using matplotlib, generate these charts at DPI 200, white background:

1. sector_allocation.png — Doughnut chart (5"×5"), center text "$XXB", labels for slices ≥3%
2. maturity_distribution.png — Bar chart (9"×4"), single color #003366
3. credit_sp.png — Doughnut chart for S&P ratings
4. credit_moodys.png — Doughnut chart for Moody's ratings
5. compliance.png — Horizontal bar chart showing actual vs limit
6. yield_curve.png — Line chart of current treasury yields (6"×3.5")
7. monthly_returns.png — Grouped bar chart
8. horizon_analysis.png — Conditional color bar chart
9. cashflow_projection.png — Stacked bar chart

STEP 3: GENERATE ECONOMIC TREND CHARTS (save to /tmp/charts/)
Using the FRED 12-month history data, generate:

10. fed_funds_history.png — Line chart (4.5"×3.0") Fed Funds rate trend
    - Navy line (#003366), light blue area fill (#E2E8F0)
    - Endpoint annotation with latest value
    - Month abbreviations on x-axis (Mar, Apr, May...)
    - Y-axis: "Rate (%)"

11. cpi_yoy.png — Line chart (4.5"×3.0") CPI year-over-year % change
    - Calculate YoY: (current / 12_months_ago - 1) × 100
    - Orange line (#E97007)
    - Add horizontal dashed line at 2.0% (Fed target)
    - Y-axis: "Year-over-Year Change (%)"

12. unemployment_trend.png — Line chart (4.5"×3.0") Unemployment rate
    - Navy line (#003366)
    - Y-axis: "Rate (%)"

13. credit_spread.png — Line + area chart (4.5"×3.0") AA OAS spread
    - Red line (#C00000), light red area fill
    - Y-axis: "Spread (percentage points)"

14. yield_curve_comparison.png — Dual line chart (4.5"×3.0")
    - Current curve: #003366 (solid, thick)
    - 12-months-ago curve: #FFB703 (dashed)
    - X-axis: tenor labels (3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y)
    - Y-axis: "Yield (%)"
    - Legend: "Current" vs "1 Year Ago"

All economic charts: clean design, despine (remove top/right borders), no gridlines,
endpoint value annotation, DPI 200, white background.

Print "PHASE_2A_COMPLETE" when done.
```

### Phase 2B — Economic Commentary Writing (general-purpose agent)

**Prompt template:**
```
You are writing economic commentary for a county treasury Board presentation.
Target audience: County Board of Supervisors — these are NOT finance professionals.
Write in plain English that any intelligent adult can follow.

READ THESE FILES:
- /tmp/sbc_economic_research.json (web research findings)
- /tmp/sbc_fred_data.json (actual FRED data points)
- {plugin_root}/skills/pool-report-generator/references/tone-guide.md
- {plugin_root}/skills/pool-report-generator/references/economic-research.md

WRITING RULES:
- Lead with a clear headline sentence
- Explain WHY things matter, not just WHAT happened
- Use analogies for complex concepts
- Put numbers in context (compare to history, benchmarks)
- Every slide MUST end with "PORTFOLIO IMPACT: [1-2 sentences]"
- Never say "positioned to benefit" — say "consistent with policy objectives"
- Font will be 10.5-11pt, so keep paragraphs concise (4-6 sentences max)

Write commentary for each of these slides as a JSON file:

{
  "economic_overview": {
    "headline": "one sentence summarizing current economic conditions",
    "narrative": "3-4 sentences of plain-English overview",
    "portfolio_impact": "1-2 sentences"
  },
  "fed_rates": {
    "headline": "what the Fed did/is doing",
    "narrative": "3-4 sentences explaining Fed policy in simple terms",
    "what_this_means": "2-3 sentences on implications for county investments",
    "portfolio_impact": "1-2 sentences"
  },
  "inflation": {
    "headline": "current inflation reading",
    "narrative": "3-4 sentences on inflation trend with historical context",
    "why_it_matters": "2-3 sentences on real returns for the pool",
    "portfolio_impact": "1-2 sentences"
  },
  "labor_market": {
    "headline": "current unemployment/jobs picture",
    "narrative": "3-4 sentences on employment conditions",
    "portfolio_impact": "1-2 sentences"
  },
  "yield_curve": {
    "headline": "describe curve shape (steep/flat/inverted)",
    "narrative": "3-4 sentences with analogy for non-specialists",
    "what_shape_means": "2-3 sentences on investment implications",
    "portfolio_impact": "1-2 sentences"
  },
  "credit_markets": {
    "headline": "spreads tight/wide/stable",
    "narrative": "3-4 sentences on corporate bond conditions",
    "portfolio_impact": "1-2 sentences"
  },
  "market_themes": [
    {
      "title": "theme headline",
      "narrative": "4-5 sentences explaining the theme",
      "portfolio_impact": "1-2 sentences"
    },
    ...
  ],
  "economic_summary": {
    "key_takeaways": ["takeaway 1", "takeaway 2", "takeaway 3", "takeaway 4"],
    "portfolio_implications": "3-4 sentences tying economic conditions to portfolio positioning"
  }
}

Save to /tmp/sbc_economic_commentary.json
Print "PHASE_2B_COMPLETE" when done.
```

---

## Phase 3: Build the PowerPoint

**Runs on main Claude (sequential).** All data is now available:
- `/tmp/sbc_report_data.json` — portfolio data + FRED latest values
- `/tmp/sbc_economic_commentary.json` — all economic narratives
- `/tmp/charts/*.png` — all chart images (portfolio + economic)

### PPTX Generation

Run the V12 generator script at `scripts/generate_pptx.js`:

```bash
node scripts/generate_pptx.js /tmp/sbc_report_data.json /tmp/SBC_Pool_Report.pptx /tmp/charts [logo_path]
```

The script reads all data from the JSON file and generates a 24-slide PPTX.

**CRITICAL FORMATTING RULES (built into the script):**

1. **Content safe zone** — ALL text and charts between y: 0.9" and y: 4.9"
2. **Typography hierarchy** — Arial Black for titles (20pt), Calibri for body (11pt), gold section labels (10pt ALL CAPS)
3. **Footer** — Navy bar at y: 5.08", h: 0.545" with date and page number
4. **Header** — Navy bar at y: 0, h: 0.75" with gold accent line at bottom
5. **Two-column layouts** — Left x: 0.5" w: 4.25", Right x: 5.0" w: 4.5"
6. **Tables** — PptxGenJS native addTable(), navy headers, alternating rows
7. **Credit quality** — Sorted by creditworthiness (AAA first), not by percentage
8. **Issuer concentration** — Aggregated by parent issuer (FHLMC includes REMICs, FRESB, etc.)
9. **Charts** — Embed as PNG with exact aspect ratio matching

### Slide Sequence (24 slides)

| # | Slide | Type | Content |
|---|-------|------|---------|
| 1 | Cover Page | Full-bleed | Title, date, county branding, logo |
| 2 | Table of Contents | Two-col | Four sections: Portfolio, Economic, Risk, Analytics |
| **PORTFOLIO OVERVIEW** | | | |
| 3 | Section Divider | Full-bleed | "Portfolio Overview" |
| 4 | Executive Summary | Two-col | Overview narrative (left) + 6 KPI cards (right) |
| 5 | Sector Allocation | Two-col | Doughnut chart (left) + allocation table (right) |
| 6 | Sector Detail | Full-width | 7-column sector breakdown table |
| **ECONOMIC & MARKET** | | | |
| 7 | Section Divider | Full-bleed | "Economic & Market Commentary" |
| 8 | Economic Snapshot | Two-col | Rates table (left) + yield curve chart (right) |
| 9 | Monetary Policy | Two-col | Fed narrative (left) + rate trajectory table (right) |
| 10 | Growth & Inflation | Two-col | Labor narrative (left) + inflation narrative (right) |
| 11 | Fixed Income | Two-col | Credit/FI markets (left) + portfolio implications (right) |
| **RISK & COMPLIANCE** | | | |
| 12 | Section Divider | Full-bleed | "Risk & Compliance" |
| 13 | Maturity Distribution | Full-width | Stacked bar chart |
| 14 | Credit Quality — S&P | Two-col | Pie chart (left) + sorted ratings table (right) |
| 15 | Credit Quality — Moody's | Two-col | Pie chart (left) + sorted ratings table (right) |
| 16 | Policy Compliance | Two-col | Bar chart (left) + compliance table (right) |
| **PERFORMANCE & ANALYTICS** | | | |
| 17 | Section Divider | Full-bleed | "Performance & Analytics" |
| 18 | Top 10 Issuers | Full-width | Aggregated parent-issuer concentration table |
| 19 | Income Analysis | Full-width | Monthly income by sector + total footer |
| 20 | Securities Cashflow | Full-width | Stacked bar chart (Jan-Dec current year) |
| 21 | Horizon Analysis | Two-col | Bar chart (left) + scenario table + methodology (right) |
| 22 | Duration & Risk | KPI + text | 3 KPI cards + risk narrative |
| 23 | Constraints | Two-col | Regulatory framework (left) + market considerations (right) |
| 24 | Disclosures & Contact | Two-col | Disclaimers (left) + contact info (right) |

### Economic Commentary

The economic slides (8-11) use commentary from the Phase 2B agent stored in `economic_commentary` in the data JSON.
The `generate_pptx.js` script reads this commentary and populates the economic slides dynamically.
If commentary is not available, placeholder text is shown.

---

## Phase 4: QA & Deliver

1. Convert to PDF: `libreoffice --headless --convert-to pdf output.pptx`
2. Extract images: `pdftoppm -jpeg -r 150 output.pdf slides/slide`
3. Visually inspect ALL slides for:
   - Text overflow below y=4.9"
   - Chart stretching or aspect ratio issues
   - Table column truncation
   - Missing "Portfolio Impact" callouts on economic slides
   - Tone compliance (no active management language)
   - Typography hierarchy (headers distinct from body)
4. Fix any issues and re-verify
5. Deliver the final .pptx to the user's workspace folder

---

## Dependencies

- **Node.js** with `pptxgenjs` (check: `node -e "require('pptxgenjs')"`)
- **Python 3** with `matplotlib`, `numpy` (check: `python3 -c "import matplotlib"`)
- **MCP tools**: `sql_execute_query` (Azure SQL), `fred_get_latest_value` / `fred_get_series` (FRED)
- **Task tool** for launching parallel sub-agents
- **WebSearch tool** for economic research (Phase 1C)

## File Structure

```
skills/pool-report-generator/
├── SKILL.md                      ← This file (workflow guide)
├── references/
│   ├── design-system.md          ← Colors, fonts, layout geometry
│   ├── data-dictionary.md        ← Database schema, SQL, FRED series
│   ├── policy-limits.md          ← IPS Schedule I compliance limits
│   ├── chart-specs.md            ← Chart types, sizes, colors
│   ├── tone-guide.md             ← Institutional voice rules
│   └── economic-research.md      ← Economic research methodology + writing guide
├── scripts/
│   ├── data_transformer.py       ← SQL→JSON transformation + economic calcs
│   └── chart_renderer.py         ← Matplotlib chart functions (portfolio + economic)
└── assets/
    └── sbc_logo.txt              ← County logo (base64 data URI)
```
