# SBC Pool Report Plugin

Generate publication-quality monthly Investment Pool Reports for the San Bernardino County Treasurer's portfolio.

## What It Does

This plugin enables any team member to generate the monthly board presentation from a single command. Claude handles everything: pulling live data from the database and FRED, generating charts, writing institutional market commentary, and assembling a branded PowerPoint deck.

## Components

| Type | Name | Purpose |
|------|------|---------|
| Command | `/pool-report` | Generate a report on demand — type `/pool-report latest` or `/pool-report 20260130` |
| Skill | pool-report-generator | Auto-triggers when you mention "pool report", "monthly report", "board presentation", etc. |

## How to Use

### Option 1: Slash Command
```
/pool-report latest
/pool-report 20260130
```

### Option 2: Natural Language
Just ask Claude:
- "Generate the pool report for January"
- "Create the monthly board presentation"
- "Run the investment pool report"

Claude will ask for any missing parameters and walk through the full workflow.

## What Gets Generated

A 34-slide PowerPoint presentation with:
- **Cover & Executive Summary** — key metrics at a glance
- **Economic Environment** (10 slides) — rates, yield curve, market themes with AI commentary
- **Portfolio Analysis** (5 slides) — summary, characteristics, income, concentration, maturity
- **Credit Quality** (2 slides) — S&P and Moody's distributions
- **Compliance** (3 slides) — Investment Policy limits with headroom analysis
- **Return Analysis** (3 slides) — 12-month total return, monthly detail, attribution
- **Cash Flow** (3 slides) — 12-month projections with methodology
- **Horizon Analysis** (3 slides) — ±100 bps scenario analysis
- **Risk & Disclosures** (2 slides)

## Requirements

These MCP connections must be active:
- **Azure SQL** — connection to `treasurer.database.windows.net / ATC_TREASURER`
- **FRED** — Federal Reserve Economic Data API access

The environment needs Node.js (with pptxgenjs) and Python 3 (with matplotlib, numpy).

## Design Standards

The report follows San Bernardino County branding with navy (#003366) headers, gold (#C8910A) accents, and a clear typography hierarchy. All market commentary uses an institutional stewardship voice aligned with the County's Investment Policy and California Government Code §53600-53686.
