---
name: report-writer
description: This skill should be used when the user asks to "write report", "generate DOCX", "credit report", "investment memo", "format report", "SBC Treasury style report", "write up analysis", "generate credit write-up", "create investment document", "compile analysis into report", or needs to assemble a formatted DOCX document from financial analysis data with SBC Treasury branding, charts, and infographics.
version: 1.0.0
---

# Report Writer

Generate a comprehensive DOCX credit analysis report following San Bernardino County Treasury formatting standards. Assembles narrative, embedded charts, infographics, and data tables into a branded document.

## Prerequisites

- Research synthesis from `{workspace}/data/research-synthesis.json`
- Financial model from `{workspace}/model/{issuer}-model.xlsx`
- Chart screenshots from `{workspace}/charts/screenshots/`
- Infographic images from `{workspace}/infographics/`

## Document Setup

**Output path**: `{workspace}/output/{issuer}-credit-report-{YYYY-MM-DD}.docx`

Use the `docx` skill or Desktop Commander `write_file` with `.docx` extension. The document is written in markdown which gets converted to styled DOCX paragraphs:
- `#` = Heading 1 (18pt, Bold, Navy)
- `##` = Heading 2 (14pt, Bold, Navy)
- `###` = Heading 3 (12pt, Bold, Dark Gray)
- Body text = 11pt, Regular
- Tables = Markdown table syntax

## CRITICAL FORMATTING RULES

### Banned Language
- NEVER use "record" as an adjective (e.g., "record growth", "record profits")
  - Replace with: "continued growth", "strong growth", "highest since [year]", "strongest in [period]"
- NEVER use "a record" as a noun
  - Remove entirely or rephrase
- Avoid superlatives: "unprecedented", "remarkable", "exceptional", "outstanding"
  - Replace with factual descriptors: "significant", "notable", "above-trend"

### Number Formatting
| Value | Format | Example |
|-------|--------|---------|
| Billions | $X.XXB | $1.30B |
| Millions (no .00) | $XXXMM | $809MM |
| Millions (with decimals) | $XXX.XXMM | $809.14MM |
| Thousands | $X.XK | $45.2K |
| Percentages | X.X% or X% | 14.2%, 3% |
| Basis points | XX bps | 35 bps |
| Negative values | -$XMM | -$23MM (NEVER brackets) |

### Number-in-Context Rules
- WRONG: `Revenue was $800MM(+3.00%)`
- RIGHT: `Revenue rose 3% YoY to $800MM driven by [reasons]`
- WRONG: `NII of $1,304 million`
- RIGHT: `NII of $1.30B`
- Always describe the change before the number, followed by the driver

### Tone Rules
- Neutral, factual, and comprehensive throughout
- No promotional language, no advocacy
- Let the data tell the story — state facts, then provide context
- Use "rose", "declined", "expanded", "compressed" — not "soared", "plummeted", "surged"
- Attribute claims: "Management stated..." not "The bank achieved..."
- Balance positive and negative factors — do not cherry-pick

### Narrative Flow
Every section follows top-line to bottom-line:
Revenue → Revenue Drivers → Expenses → Expense Drivers → Provisions → Net Income

## Report Sections

### Cover / Header
```
# {Issuer} — Credit Analysis
## {Analysis Date}
### Prepared by San Bernardino County Treasury — Investment Division
```

### Section 1: Company Summary

**Structure (2-3 pages):**

```markdown
# Company Summary

## Revenue Performance
[Total revenue figure and YoY change. Then stated drivers from earnings call/annual report.]

[Quantitative research on what really drove revenue — decompose NII vs fees vs trading.
Compare to peer revenue growth. Note if stated drivers match quantitative evidence.]

## Operating Expenses
[Total opex and cost/income ratio. Stated efficiency drivers.]

[Quantitative analysis against peers — is the cost/income ratio justified?
Forensic comparison: revenue/employee vs peers, cost trends vs stated programs.]

## Credit Quality & Provisions
[Provision charge and cost of risk. NPL ratio trend.]

[Context: credit cycle position, sector-specific risks, coverage adequacy vs peers.]

## Net Income & Returns
[Net income, EPS, ROE. YoY comparison.]

[DuPont decomposition: what drove ROE changes? Sustainable vs one-time factors.]

## Ratings & Strategic Overview
[Current agency ratings with any recent actions.]

[M&A activity, strategic initiatives, digital transformation progress.]

[Business model assessment using quantitative research.]
```

**Writing approach**: Start with the headline number, give context immediately, then go deeper with quantitative analysis. Each sub-section should be 2-4 paragraphs.

### Section 2: Segment Performance

**Structure (1-2 pages):**

For each major business segment:
```markdown
## {Segment Name}

Revenue of $X.XB, representing XX% of group total, [rose/declined] X% YoY. [Key drivers.]

[Segment-specific metrics: ROE, cost/income, RWA consumption.]

[Strategic assessment: growth/mature/wind-down? Capital allocation changes?]
```

Include a segment comparison table:
```markdown
| Segment | Revenue | % of Total | YoY Change | Cost/Income | ROE |
|---------|---------|-----------|------------|-------------|-----|
```

### Section 3: Balance Sheet, Capital, Liquidity, Risks

**Structure (2-3 pages):**

```markdown
# Balance Sheet & Risk Profile

## Capital Adequacy
[CET1 ratio, buffer over SREP, leverage ratio. Organic capital generation.]

[Capital trajectory: distributions vs retention. Peer comparison.]

## Asset Quality
[NPL ratio, coverage, cost of risk trends over 5 quarters.]

[Stage 2 migration, sector concentrations, geographic risks.]

## Liquidity & Funding
[LCR, NSFR, loan/deposit ratio.]

[Funding mix, deposit stability, wholesale maturity profile.]

## Key Risks
[Top 3-5 risks with assessment: credit, market, operational, regulatory, strategic.]
```

### Embedded Content Placement

Charts and infographics should be embedded at natural narrative points:

- **Executive Summary infographic**: After the cover, before Section 1
- **CET1 comparison chart**: In Capital Adequacy section
- **ROE trend/waterfall chart**: In Net Income & Returns section
- **NPL/cost of risk chart**: In Asset Quality section
- **Credit scorecard radar**: In the Credit Rating section
- **Peer comparison heatmap**: In a dedicated Peer Comparison section or appendix
- **Risk assessment infographic**: After Key Risks section

### Tables

Use markdown table syntax. Tables in the report should follow:
- Header row in navy with white text (handled by DOCX styling)
- Alternating row colors (white / light gray)
- Right-align numbers, left-align text
- Use the standard number formatting rules

Example:
```markdown
| Metric | Q4-24 | Q1-25 | QoQ Change | Peer Median |
|--------|------:|------:|-----------:|------------:|
| CET1 Ratio | 13.8% | 14.0% | +20 bps | 13.5% |
| ROE | 11.2% | 11.5% | +30 bps | 10.8% |
```

## Document Layout Options

The report can mix single-column and two-column sections:
- **Single column**: Narrative text, full-width charts, tables
- **Two column**: Side-by-side metrics, small charts next to commentary

For two-column layout, describe the intended layout in markdown and note it for manual adjustment in Word if needed.

## Quality Checklist

Before finalizing the report, verify:
- [ ] No use of "record" as adjective or noun
- [ ] All numbers formatted correctly ($XB, $XMMM, no brackets)
- [ ] No promotional or enthusiastic language
- [ ] Narrative flows top-line to bottom-line in each section
- [ ] Changes described before numbers (e.g., "rose 3% to $800MM")
- [ ] All charts and infographics properly referenced
- [ ] Peer comparisons included for key metrics
- [ ] Credit scoring model results discussed
- [ ] Upgrade/downgrade probability stated
- [ ] Risks section is balanced (not only positive or negative)

For the complete style guide, load `references/style-guide.md`.
For detailed formatting rules, load `references/formatting-rules.md`.
For section-by-section templates, load `references/section-templates.md`.
