---
name: charting
description: Create professional data visualizations and charts. Use this skill whenever the user asks to chart, graph, plot, visualize, or diagram any data — including bar charts, line charts, time series, scatter plots, heatmaps, radar charts, dumbbell charts, waterfalls, treemaps, network diagrams, geographic maps, or any other chart type. Also trigger when the user says "recreate this chart", "make this clearer", "redo this visual", uploads chart screenshots for reproduction, or provides tabular data that would benefit from visualization. This skill covers Chart.js, D3.js, raw Canvas, and HTML-based visualizations. Use it for both simple single-chart requests and complex multi-panel dashboards.
---

# Charting Skill

## Overview

A unified charting skill that selects the right rendering approach for each visualization request. The skill routes between three tiers based on chart complexity and type, applies consistent professional styling, and encodes best practices for financial and institutional data visualization.

## Tool Selection — Pick the Right Tier

Before writing any code, classify the request into one of three tiers:

### Tier 1: Chart.js (Default — use for ~70% of charts)

**When to use:** Any chart with standard cartesian or radial axes.

- Bar charts (vertical, horizontal, stacked, grouped)
- Line charts, area charts, time series
- Scatter plots, bubble charts
- Doughnut/pie charts
- Waterfall charts (via stacked bar tricks)
- Combo charts (bar + line overlays)

**Why it wins:** Handles axes, gridlines, tooltips, responsive scaling, and hover interactions out of the box. Custom plugins add annotations, reference lines, and data labels without reinventing the wheel.

**CDN:** `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`

### Tier 2: Raw Canvas / HTML (Use for custom layouts)

**When to use:** The chart has a non-standard layout that would fight Chart.js conventions.

- Dumbbell / lollipop charts
- Heatmap tables with color-coded cells
- Scorecard grids
- Custom gauge or meter visualizations
- Bullet charts
- Marimekko / mosaic charts
- Any layout where positioning elements manually is simpler than configuring a library

**Why it wins:** Full control over positioning. No library overhead. Clean and lightweight.

### Tier 3: D3.js (Reserve for complex/interactive visuals)

**When to use:** The visualization requires element-level DOM control, complex interactions, or unusual geometry.

- Force-directed network graphs (counterparty exposure, org charts)
- Treemaps, sunbursts, circle packing
- Geographic choropleths and custom projections
- Chord diagrams, Sankey flows
- Custom interactive explorations with brush, zoom, pan
- Hierarchical layouts (tree, cluster, radial)
- Novel or bespoke chart types

**CDN:** `https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js`

**Why it wins:** Unmatched control over data binding, transitions, and custom geometry. Necessary when Chart.js can't express the visual structure.

### Decision Flowchart

```
Does the chart have standard axes (x/y, radial)?
├── YES → Does Chart.js support the chart type natively?
│   ├── YES → Tier 1: Chart.js
│   └── NO  → Is the layout essentially a custom arrangement of shapes/text?
│       ├── YES → Tier 2: Raw Canvas/HTML
│       └── NO  → Tier 3: D3.js
└── NO → Does it need force simulation, hierarchy layout, or geo projection?
    ├── YES → Tier 3: D3.js
    └── NO  → Tier 2: Raw Canvas/HTML
```

## Aesthetic Standards

Apply these standards to ALL charts regardless of tier. These reflect institutional reporting quality.

### Color Palette

Primary palette for categorical data (use in order, skip as needed):

| Name    | Hex       | Use case                              |
|---------|-----------|---------------------------------------|
| Teal    | `#1a6e5e` | Primary / positive / Nordic banks     |
| Blue    | `#2a5da8` | Time series lines / neutral emphasis  |
| Purple  | `#6b4c9a` | Secondary category                    |
| Coral   | `#c45a2c` | Tertiary / French banks               |
| Red     | `#c43030` | Negative / downgrade / reference line |
| Green   | `#2a7d6b` | Positive / upgrade / trough marker    |
| Gray    | `#888`    | Neutral / stable / de-emphasized      |

Semantic usage:
- **Reference lines** (ECB avg, thresholds): `#c43030` with dashed stroke `[8, 5]`
- **Peak annotations**: `#c43030`
- **Trough annotations**: `#2a7d6b`
- **Current value dot**: Match line color (e.g., `#2a5da8`)

### Heatmap Color Scale

For scorecards and matrix-style visuals, use a three-stop diverging scale:
- Low (0–3): warm red tint `rgba(198,68,48,0.18)`
- Mid (4–6): amber tint `rgba(240,200,120,0.18)`
- High (7–10): green tint `rgba(40,140,80,0.20)`

Composite summary cells use distinct background fills:
- Strong (≥7.0): `#e6f4ea` text `#1a6e3a`
- Moderate (5.0–6.9): `#fff8e1` text `#8a6d00`
- Weak (<5.0): `#fce8e6` text `#a33030`

### Typography

- Font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Chart title: `20px`, weight `600`, color `#1a1a1a`
- Subtitle: `14px`, color `#666`
- Axis labels: `12px`, color `rgba(0,0,0,0.5)`
- Data labels on bars: `500 12px`, color `rgba(0,0,0,0.7)`
- Annotation labels: `500 12px`
- Metric card values: `24px`, weight `500`
- Metric card labels: `13px`, color `#888`

### Layout

- Background: `#fff` (white, clean — no gray backgrounds on charts)
- Grid lines: `rgba(0,0,0,0.06)` or `rgba(0,0,0,0.08)`, weight `0.5px`
- No border on axes (`border: { display: false }`)
- No Chart.js default legend — always build custom HTML legends
- Bar border radius: `2px` (subtle rounding)
- Padding: generous `top: 30` to avoid clipping data labels

### Annotations Pattern

Reference lines and event markers are a recurring need. Standard approach:

```javascript
// Reference line plugin (e.g., ECB average, threshold)
{
  id: 'refLine',
  afterDraw(chart) {
    const ctx = chart.ctx;
    const yScale = chart.scales.y;
    const xScale = chart.scales.x;
    const yVal = yScale.getPixelForValue(TARGET_VALUE);
    ctx.save();
    ctx.setLineDash([8, 5]);
    ctx.strokeStyle = '#c43030';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(xScale.left, yVal);
    ctx.lineTo(xScale.right, yVal);
    ctx.stroke();
    ctx.restore();
    // Label
    ctx.save();
    ctx.font = '500 12px sans-serif';
    ctx.fillStyle = '#c43030';
    ctx.textAlign = 'left';
    ctx.fillText('Label: ' + TARGET_VALUE, xScale.left, yVal - 6);
    ctx.restore();
  }
}
```

Event annotation (vertical dashed line with label):

```javascript
// Inside afterDraw plugin
events.forEach(e => {
  const pt = meta.data[e.idx];
  ctx.setLineDash([3, 3]);
  ctx.strokeStyle = 'rgba(0,0,0,0.2)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pt.x, yScale.top);
  ctx.lineTo(pt.x, yScale.bottom);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.font = '500 12px sans-serif';
  ctx.fillStyle = 'rgba(0,0,0,0.5)';
  ctx.textAlign = e.side === 'left' ? 'right' : 'left';
  const xOff = e.side === 'left' ? -6 : 6;
  ctx.fillText(e.label, pt.x + xOff, yScale.top + e.yOff);
});
```

Data label plugin (values above/below bars):

```javascript
{
  id: 'barLabels',
  afterDraw(chart) {
    const ctx = chart.ctx;
    const meta = chart.getDatasetMeta(0);
    ctx.save();
    ctx.font = '500 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(0,0,0,0.7)';
    meta.data.forEach((bar, i) => {
      const v = values[i];
      const yPos = v >= 0 ? bar.y - 8 : bar.y + 16;
      ctx.fillText(formatValue(v), bar.x, yPos);
    });
    ctx.restore();
  }
}
```

## Chart.js Configuration Patterns

### Standard vertical bar chart

```javascript
new Chart(canvas, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      data: values,
      backgroundColor: colors,
      borderRadius: 2,
      barPercentage: 0.7,
      categoryPercentage: 0.8
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { top: 30 } },
    plugins: { legend: { display: false }, tooltip: { enabled: true } },
    scales: {
      x: {
        grid: { display: false },
        ticks: {
          color: 'rgba(0,0,0,0.5)', font: { size: 12 },
          maxRotation: 40, minRotation: 40, autoSkip: false
        },
        border: { display: false }
      },
      y: {
        ticks: { color: 'rgba(0,0,0,0.5)', font: { size: 12 } },
        grid: { color: 'rgba(0,0,0,0.08)', lineWidth: 0.5 },
        border: { display: false }
      }
    }
  },
  plugins: [/* custom plugins here */]
});
```

### Horizontal stacked bar chart

```javascript
new Chart(canvas, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [
      { label: 'Segment A', data: segA, backgroundColor: '#2a7d6b', borderRadius: { topLeft: 3, bottomLeft: 3 } },
      { label: 'Segment B', data: segB, backgroundColor: '#c4e0d8', borderRadius: { topRight: 3, bottomRight: 3 } }
    ]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { right: 80 } },
    plugins: { legend: { display: false } },
    scales: {
      x: { stacked: true, /* ... */ },
      y: { stacked: true, grid: { display: false }, /* ... */ }
    }
  }
});
```

### Time series line chart

```javascript
new Chart(canvas, {
  type: 'line',
  data: {
    labels: dateLabels,
    datasets: [{
      data: values,
      borderColor: '#2a5da8',
      backgroundColor: 'rgba(42,93,168,0.06)',
      borderWidth: 1.5,
      pointRadius: 0,
      pointHitRadius: 6,
      fill: true,
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(0,0,0,0.8)',
        displayColors: false,
        callbacks: {
          title: function(items) { /* format date */ },
          label: function(ctx) { return ctx.raw.toFixed(1) + ' bps'; }
        }
      }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: 'rgba(0,0,0,0.5)', font: { size: 12, weight: '500' }, maxRotation: 0 },
        border: { display: false }
      },
      y: {
        ticks: { color: 'rgba(0,0,0,0.4)', font: { size: 11 }, callback: v => v + ' bps' },
        grid: { color: 'rgba(0,0,0,0.06)', lineWidth: 0.5 },
        border: { display: false }
      }
    }
  },
  plugins: [/* annotation plugins */]
});
```

### X-Axis Label Strategy for Large Datasets

When charting >200 data points, avoid assigning a label to every point. Instead, assign labels only at meaningful intervals and use `autoSkip` to keep things clean:

```javascript
// Deduplicated semi-annual labels for multi-year daily data
const labels = [];
let lastKey = '';
parsedDates.forEach(d => {
  const mon = d.getMonth();
  const yr = d.getFullYear();
  const key = yr + '-' + mon;
  if (mon % 6 === 0 && key !== lastKey) {
    labels.push(d.toLocaleString('en-US',{month:'short'}) + ' ' + yr.toString().slice(-2));
    lastKey = key;
  } else {
    labels.push('');
  }
});

// In scales config:
x: {
  ticks: {
    autoSkip: true,
    maxTicksLimit: 14,
    callback: function(val, idx) { return labels[idx] || undefined; }
  }
}
```

**Common pitfall:** Using `autoSkip: false` with 1000+ data points renders a tick for every point, creating a blurry unreadable axis. Always use deduplication + `autoSkip: true` + `maxTicksLimit` for large datasets.

## Tier 2 Patterns — Raw Canvas / HTML

### Dumbbell Chart (e.g., rating migration)

Use raw Canvas 2D when each row is a custom drawn element with dots, lines, arrows, and labels at arbitrary positions. Structure:

1. Set up HiDPI canvas: `canvas.width = W * dpr; canvas.height = H * dpr; ctx.scale(dpr, dpr);`
2. Define a scale function: `function xFor(value) { return leftPad + (valueToNum[value] / maxVal) * chartW; }`
3. Draw gridlines at each scale step
4. For each data row at `y = topPad + rowH * i + rowH / 2`:
   - Draw connecting line between old/new positions
   - Draw arrowhead if directional
   - Draw hollow dot for old value, solid dot for new value
   - Draw labels (bank name left, status right)

### Heatmap / Scorecard Table

Use HTML `<table>` with JS-computed inline `background` and `color` styles per cell. Structure:

1. Define a color function: `function scoreColor(v) { /* returns {bg, text} */ }`
2. Build HTML string row by row
3. Apply sort order (e.g., by composite score descending)
4. Use rank badges: `<span class="rank">1</span>`
5. Composite column separated by a left border

### Metric Summary Cards

For header stats above a chart:

```html
<div class="meta">
  <span>Current: <span class="val">65.2 bps</span></span>
  <span>1Y high: <span class="val" style="color:#c43030;">91.9 bps</span></span>
  <span>1Y low: <span class="val" style="color:#2a7d6b;">50.5 bps</span></span>
</div>
```

### Custom Legends

Always disable Chart.js default legend and build HTML:

```html
<div class="legend">
  <span><span class="swatch" style="background: #2a7d6b;"></span>Stressed CET1</span>
  <span><span class="swatch" style="background: #c4e0d8;"></span>Depletion</span>
</div>
```

## Tier 3 Patterns — D3.js

For detailed D3 patterns, read the reference files:

- `references/d3-patterns.md` — Tree diagrams, treemaps, force-directed graphs, chord diagrams, geographic maps, Sankey flows
- `references/scale-reference.md` — Complete guide to D3 scales (linear, log, band, time, ordinal, sequential, diverging)
- `references/colour-schemes.md` — D3 color scheme recommendations and accessibility guidance

### Key D3 Setup

```javascript
import * as d3 from 'd3';
// or CDN: https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js

// Standard structure
const svg = d3.select('#chart');
svg.selectAll("*").remove();
const width = 800, height = 400;
const margin = { top: 20, right: 30, bottom: 40, left: 50 };
const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
```

### When D3 + Chart.js overlap

Some charts could go either way. Rules of thumb:
- If you need tooltips, responsive resize, and axis management → Chart.js is faster to implement
- If you need custom animations, drag interactions, or non-rectangular layouts → D3
- If you need to render >5000 elements → use D3 with Canvas renderer, not SVG

## Output Format

### Standalone HTML file (default for artifacts)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chart Title</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fff; padding: 2rem; }
  h2 { font-size: 20px; font-weight: 600; margin-bottom: 4px; color: #1a1a1a; }
  p.sub { font-size: 14px; color: #666; margin-bottom: 1.5rem; }
  .chart-wrap { position: relative; width: 100%; max-width: 860px; height: 400px; }
</style>
</head>
<body>
<h2>Chart title — context</h2>
<p class="sub">Key takeaway in one sentence.</p>
<!-- Optional: metric cards, legend -->
<div class="chart-wrap">
  <canvas id="chart"></canvas>
</div>
<script src="CDN_URL"></script>
<script>
// Chart code
</script>
</body>
</html>
```

### Inline Visualizer widget

When rendering in chat (not as an artifact file), use the Visualizer tool. Same aesthetic standards apply — just output the chart content without DOCTYPE/html/body wrappers.

## Checklist Before Shipping

1. **Tier selected?** Chart.js / Canvas / D3 — don't default to D3 for a bar chart
2. **White background?** No gray or colored page backgrounds
3. **Custom legend?** Chart.js default legend disabled, HTML legend built
4. **Data labels?** Values shown on bars/points where meaningful
5. **Axes clean?** No border, subtle gridlines, readable font size
6. **Large dataset x-axis?** Deduplicated labels, autoSkip enabled, maxTicksLimit set
7. **Annotations don't overlap?** Stagger yOff values, check side alignment, add padding
8. **Right padding for edge labels?** Annotations near right edge need extra layout padding
9. **Number formatting?** Negative = `-$5M` not `$-5M`. Round all displayed values.
10. **Responsive?** `maintainAspectRatio: false` + wrapper div with explicit height

## Resources

### references/
- `d3-patterns.md` — D3 visualization patterns (trees, force, chord, geo, Sankey)
- `scale-reference.md` — D3 scales guide
- `colour-schemes.md` — Color scheme recommendations

### assets/
- `chartjs-bar-template.html` — Starter template for Chart.js bar chart with plugins
- `chartjs-timeseries-template.html` — Time series template with annotations
- `canvas-dumbbell-template.html` — Raw Canvas dumbbell chart template
- `html-heatmap-template.html` — HTML heatmap scorecard template
