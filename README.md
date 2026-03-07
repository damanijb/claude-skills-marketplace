# Claude Skills Marketplace

Custom Claude Code skills for finance, data visualization, and AI image generation.

## Skills

### nano-banana `v3.0.0`
AI image generation using Google's Gemini 3.1 Flash model, tuned for **finance and investment research**.

- Enterprise-grade infographics with white backgrounds
- Restrained typography and clean minimalist aesthetics
- Templates for tiered comparisons, status trackers, flow diagrams, executive summaries, and metric tables
- Suitable for research PDFs, board presentations, and printed reports

### d3-viz `v1.0.0`
Interactive data visualizations using **D3.js v7**.

- Comprehensive chart types: bar, line, area, scatter, pie, treemap, network, geographic
- Financial chart patterns: candlestick, yield curves, waterfall, heatmaps
- Built-in interactivity: tooltips, zoom, brush, transitions
- Reference materials for color schemes, scales, and common patterns
- JSX templates for quick starts

### investment-analyst `v0.1.0`
End-to-end **investment credit analysis pipeline** with 8 coordinated skills.

- **Research Provider Access** — Chrome automation for JPM Research, CapitalIQ, FitchRatings, CreditSights, Morgan Stanley with 1Password/env credential resolution
- **Document Collection** — IR pages, SEC EDGAR, ECB/EBA filings, earnings transcripts, news via Chrome + PageIndex MCP
- **Fundamental Research** — 5-pillar framework (management, peers, environment, drivers, country health) with FRED macro data integration
- **Financial Model** — 7-sheet Excel workbook: income statement, balance sheet, credit scoring model (6 dimensions, 0-10 scale), liquidity, ROE decomposition, peer comparison
- **Chart Generator** — 8 D3.js chart types (grouped bar, waterfall, radar, heatmap, etc.) with SBC Treasury color palette
- **Infographic Generator** — nano-banana prompts for executive summary dashboards and risk assessment visuals
- **Report Writer** — DOCX with SBC Treasury branding, formatting rules (banned language, number formatting, neutral tone), and section templates

## Installation

Add this marketplace to Claude Code:

```
/install-plugin https://github.com/damanijb/claude-skills-marketplace
```

## License

MIT
