---
name: chart-generator
description: This skill should be used when the user asks to "create chart", "D3 chart", "generate visualization", "interactive chart", "financial chart", "chart for report", "bar chart for CET1", "ROE trend chart", "peer comparison chart", "waterfall chart", "credit scorecard radar", or needs to generate D3.js charts for embedding in financial reports.
version: 1.0.0
---

# Chart Generator

Generate D3.js interactive charts as standalone HTML files, serve them via a local dev server, and screenshot them as PNGs for embedding in DOCX reports.

## Prerequisites

- Financial model data from `{workspace}/model/{issuer}-model.xlsx`
- Or raw data from `{workspace}/data/` directory
- Claude Preview MCP for serving and screenshotting

## Chart Types Available

| Chart Type | Use Case | Example |
|------------|----------|---------|
| Grouped Bar | CET1 ratios across quarters, peer comparison | CET1 by bank, 5Q |
| Line + Events | EUR/USD with annotations, stock price | Time series with markers |
| Horizontal Bar | NPL ratios ranked, cost of risk | Sorted metric comparison |
| Stacked Bar | Revenue composition, funding mix | Component breakdown |
| Radar/Spider | Credit scorecard dimensions | Multi-metric profile |
| Heatmap | Peer comparison matrix | Color-coded metric grid |
| Waterfall | ROE decomposition, P&L bridge | Component contribution |
| Bubble | Risk vs. return positioning | 3-variable scatter |

## Workflow

### Step 1: Prepare Chart Data
Extract data from the financial model or research synthesis and format as JavaScript objects:

```javascript
const chartData = {
  title: "CET1 Ratios — 5Q Trend + 2Q Estimate",
  subtitle: "Capital adequacy comparison across EU G-SIBs",
  data: [
    { bank: "BNP Paribas", quarters: [13.2, 13.5, 13.7, 13.8, 14.0, 14.2, 14.3] },
    // ...
  ],
  labels: ["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25E", "Q3-25E"]
};
```

### Step 2: Generate HTML File
Use the chart template at `${CLAUDE_PLUGIN_ROOT}/skills/chart-generator/assets/chart-template.html` as the base. For each chart:

1. Copy the template HTML structure
2. Replace the placeholder data with actual chart data
3. Select the appropriate D3 chart rendering code from `references/chart-library.md`
4. Embed the data and rendering code in a `<script>` block
5. Write the complete HTML to `{workspace}/charts/{chart-name}.html`

Or create a single multi-chart HTML file: `{workspace}/charts/charts.html` with all charts and a sticky navigation.

### Step 3: Serve Locally
Update `.claude/launch.json` to include the chart server:
```json
{
  "name": "{issuer}-charts",
  "runtimeExecutable": "python3",
  "runtimeArgs": ["-m", "http.server", "8766", "--directory", "{workspace}/charts"],
  "port": 8766
}
```

Start the server: `preview_start(name="{issuer}-charts")`

### Step 4: Screenshot Each Chart
For each chart on the page:
1. Navigate to the specific chart anchor on the page
2. Use `preview_click` to scroll the chart into view if needed
3. Use `preview_screenshot` to capture the current view
4. Save the PNG to `{workspace}/charts/screenshots/{chart-name}.png`

### Step 5: Clean Up
After all screenshots are captured:
- `preview_stop(serverId="{id}")` to stop the server
- The PNGs in `{workspace}/charts/screenshots/` are ready for the report-writer skill

## SBC Treasury Color Palette

Use these colors consistently across all charts:

```javascript
const colors = {
  // Primary
  navy: '#1f4296',
  navyHover: '#1a3a85',
  navyDark: '#112357',

  // Semantic
  positive: '#27ae60',
  negative: '#e74c3c',
  warning: '#f39c12',
  neutral: '#3498db',

  // Grays
  text: '#1a1a2e',
  muted: '#6b7280',
  border: '#e5e7eb',
  background: '#fafafa',
  card: '#ffffff',

  // Bank-specific (for multi-bank charts)
  bankPalette: ['#1f4296', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#3498db', '#1abc9c', '#e67e22']
};
```

## Chart Sizing for Report

- Single column chart: width 700px, height 400px
- Wide chart (full page): width 1000px, height 450px
- Radar chart: width 500px, height 500px
- Small inline chart: width 400px, height 300px

Use SVG `viewBox` for responsive sizing in HTML, but set fixed dimensions for screenshot consistency.

For D3 code patterns and examples, load `references/chart-library.md`.
