---
name: d3-viz
description: Creating interactive data visualisations using d3.js. This skill should be used when creating custom charts, graphs, network diagrams, geographic visualisations, or any complex SVG-based data visualisation that requires fine-grained control over visual elements, transitions, or interactions. Use this for bespoke visualisations beyond standard charting libraries, whether in React, Vue, Svelte, vanilla JavaScript, or any other environment.
---

# D3.js Visualisation

## Overview

This skill provides guidance for creating sophisticated, interactive data visualisations using d3.js. D3.js (Data-Driven Documents) excels at binding data to DOM elements and applying data-driven transformations to create custom, publication-quality visualisations with precise control over every visual element. The techniques work across any JavaScript environment, including vanilla JavaScript, React, Vue, Svelte, and other frameworks.

## When to use d3.js

**Use d3.js for:**
- Custom visualisations requiring unique visual encodings or layouts
- Interactive explorations with complex pan, zoom, or brush behaviours
- Network/graph visualisations (force-directed layouts, tree diagrams, hierarchies, chord diagrams)
- Geographic visualisations with custom projections
- Visualisations requiring smooth, choreographed transitions
- Publication-quality graphics with fine-grained styling control
- Novel chart types not available in standard libraries

**Consider alternatives for:**
- 3D visualisations - use Three.js instead

## Core workflow

### 1. Set up d3.js

Import d3 at the top of your script:

```javascript
import * as d3 from 'd3';
```

Or use the CDN version (7.x):

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

All modules (scales, axes, shapes, transitions, etc.) are accessible through the `d3` namespace.

### 2. Choose the integration pattern

**Pattern A: Direct DOM manipulation (recommended for most cases)**
Use d3 to select DOM elements and manipulate them imperatively. This works in any JavaScript environment:

```javascript
function drawChart(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Select by ID, class, or DOM element

  // Clear previous content
  svg.selectAll("*").remove();

  // Set up dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };

  // Create scales, axes, and draw visualisation
  // ... d3 code here ...
}

// Call when data changes
drawChart(myData);
```

**Pattern B: Declarative rendering (for frameworks with templating)**
Use d3 for data calculations (scales, layouts) but render elements via your framework:

```javascript
function getChartElements(data) {
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([0, 400]);

  return data.map((d, i) => ({
    x: 50,
    y: i * 30,
    width: xScale(d.value),
    height: 25
  }));
}

// In React: {getChartElements(data).map((d, i) => <rect key={i} {...d} fill="#E69F00" />)}
// In Vue: v-for directive over the returned array
// In vanilla JS: Create elements manually from the returned data
```

Use Pattern A for complex visualisations with transitions, interactions, or when leveraging d3's full capabilities. Use Pattern B for simpler visualisations or when your framework prefers declarative rendering.

### 3. Structure the visualisation code

Follow this standard structure in your drawing function:

```javascript
function drawVisualization(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Or pass a selector/element
  svg.selectAll("*").remove(); // Clear previous render

  // 1. Define dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. Create main group with margins
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. Create scales
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]); // Note: inverted for SVG coordinates

  // 4. Create and append axes (Tufte style: remove top/right spines)
  const xAxis = d3.axisBottom(xScale);
  const yAxis = d3.axisLeft(yScale);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(xAxis)
    .call(g => g.select(".domain").remove());  // Remove bottom spine

  g.append("g")
    .call(yAxis)
    .call(g => g.select(".domain").remove());  // Remove left spine

  // 4b. Add horizontal gridlines (behind data, subtle)
  g.insert("g", ":first-child")  // insert before data elements
    .attr("class", "grid")
    .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(""))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line")
      .attr("stroke", "#E5E5E5")
      .attr("stroke-width", 0.8)
      .attr("opacity", 0.7));

  // 5. Bind data and create visual elements
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "#E69F00");  // Okabe-Ito amber
}

// Call when data changes
drawVisualization(myData);
```

### 4. Implement responsive sizing

Make visualisations responsive to container size:

```javascript
function setupResponsiveChart(containerId, data) {
  const container = document.getElementById(containerId);
  const svg = d3.select(`#${containerId}`).append('svg');

  function updateChart() {
    const { width, height } = container.getBoundingClientRect();
    svg.attr('width', width).attr('height', height);

    // Redraw visualisation with new dimensions
    drawChart(data, svg, width, height);
  }

  // Update on initial load
  updateChart();

  // Update on window resize
  window.addEventListener('resize', updateChart);

  // Return cleanup function
  return () => window.removeEventListener('resize', updateChart);
}

// Usage:
// const cleanup = setupResponsiveChart('chart-container', myData);
// cleanup(); // Call when component unmounts or element removed
```

Or use ResizeObserver for more direct container monitoring:

```javascript
function setupResponsiveChartWithObserver(svgElement, data) {
  const observer = new ResizeObserver(() => {
    const { width, height } = svgElement.getBoundingClientRect();
    d3.select(svgElement)
      .attr('width', width)
      .attr('height', height);

    // Redraw visualisation
    drawChart(data, d3.select(svgElement), width, height);
  });

  observer.observe(svgElement.parentElement);
  return () => observer.disconnect();
}
```

## Common visualisation patterns

### Bar chart

```javascript
function drawBarChart(data, svgElement) {
  if (!data || data.length === 0) return;

  const svg = d3.select(svgElement);
  svg.selectAll("*").remove();

  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .call(d3.axisLeft(yScale));

  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.category))
    .attr("y", d => yScale(d.value))
    .attr("width", xScale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", "#56B4E9");  // Okabe-Ito sky blue
}

// Usage:
// drawBarChart(myData, document.getElementById('chart'));
```

### Line chart

```javascript
// Default: curveLinear — faithfully connects data points without interpolation.
// Use this for financial data, actual observations, or any measured values.
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value));

// Only use smooth curves when explicitly interpolating or fitting:
//   .curve(d3.curveMonotoneX)  — smooth interpolation (use ONLY for fitted/modeled data)
//   .curve(d3.curveBasis)      — B-spline smoothing
//   .curve(d3.curveStep)       — step function (good for discrete/categorical time data)

g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "#E69F00")  // Okabe-Ito amber
  .attr("stroke-width", 2)
  .attr("d", line);
```

### Scatter plot

```javascript
g.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", d => sizeScale(d.size)) // Optional: size encoding
  .attr("fill", d => colourScale(d.category)) // Optional: colour encoding
  .attr("opacity", 0.7);
```

### Chord diagram

A chord diagram shows relationships between entities in a circular layout, with ribbons representing flows between them:

```javascript
function drawChordDiagram(data) {
  // data format: array of objects with source, target, and value
  // Example: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // Create matrix from data
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // Create chord layout
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"];
  const colourScale = d3.scaleOrdinal()
    .domain(nodes)
    .range(OKABE_ITO);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // Draw ribbons
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Draw groups (arcs)
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Add labels
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}
```

### Heatmap

A heatmap uses colour to encode values in a two-dimensional grid, useful for showing patterns across categories:

```javascript
function drawHeatmap(data) {
  // data format: array of objects with row, column, and value
  // Example: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Get unique rows and columns
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Create scales
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // Colour scale for values
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // Draw rectangles
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Add x-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // Add y-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // Add colour legend
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale)
    .ticks(5);

  // Draw colour gradient in legend
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}
```

### Pie chart

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(Math.min(width, height) / 2 - 20);

const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"];
const colourScale = d3.scaleOrdinal().range(OKABE_ITO);

const g = svg.append("g")
  .attr("transform", `translate(${width / 2},${height / 2})`);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colourScale(i))
  .attr("stroke", "white")
  .attr("stroke-width", 2);
```

### Force-directed network

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = g.selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke", "#999")
  .attr("stroke-width", 1);

const node = g.selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", 8)
  .attr("fill", "#009E73")  // Okabe-Ito teal
  .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended));

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
  
  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
});

function dragstarted(event) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  event.subject.fx = event.subject.x;
  event.subject.fy = event.subject.y;
}

function dragged(event) {
  event.subject.fx = event.x;
  event.subject.fy = event.y;
}

function dragended(event) {
  if (!event.active) simulation.alphaTarget(0);
  event.subject.fx = null;
  event.subject.fy = null;
}
```

## Adding interactivity

### Tooltips

```javascript
// Create tooltip div (outside SVG)
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background-color", "white")
  .style("border", "1px solid #ddd")
  .style("padding", "10px")
  .style("border-radius", "4px")
  .style("pointer-events", "none");

// Add to elements
circles
  .on("mouseover", function(event, d) {
    d3.select(this).attr("opacity", 1);
    tooltip
      .style("visibility", "visible")
      .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
  })
  .on("mousemove", function(event) {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", function() {
    d3.select(this).attr("opacity", 0.7);
    tooltip.style("visibility", "hidden");
  });
```

### Zoom and pan

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom);
```

### Click interactions

```javascript
circles
  .on("click", function(event, d) {
    // Handle click (dispatch event, update app state, etc.)
    console.log("Clicked:", d);

    // Visual feedback
    d3.selectAll("circle").attr("fill", "#009E73");
    d3.select(this).attr("fill", "#E69F00");

    // Optional: dispatch custom event for your framework/app to listen to
    // window.dispatchEvent(new CustomEvent('chartClick', { detail: d }));
  });
```

## Transitions and animations

Add smooth transitions to visual changes:

```javascript
// Basic transition
circles
  .transition()
  .duration(750)
  .attr("r", 10);

// Chained transitions
circles
  .transition()
  .duration(500)
  .attr("fill", "orange")
  .transition()
  .duration(500)
  .attr("r", 15);

// Staggered transitions
circles
  .transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("cy", d => yScale(d.value));

// Custom easing
circles
  .transition()
  .duration(1000)
  .ease(d3.easeBounceOut)
  .attr("r", 10);
```

## Scales reference

### Quantitative scales

```javascript
// Linear scale
const xScale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

// Log scale (for exponential data)
const logScale = d3.scaleLog()
  .domain([1, 1000])
  .range([0, 500]);

// Power scale
const powScale = d3.scalePow()
  .exponent(2)
  .domain([0, 100])
  .range([0, 500]);

// Time scale
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 500]);
```

### Ordinal scales

```javascript
// Band scale (for bar charts)
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

// Point scale (for line/scatter categories)
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400]);

// Ordinal scale (for colours — use Okabe-Ito palette)
const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"];
const colourScale = d3.scaleOrdinal().range(OKABE_ITO);
```

### Sequential scales

```javascript
// Sequential colour scale
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

// Diverging colour scale
const divScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);
```

## Best practices

### Data preparation

Always validate and prepare data before visualisation:

```javascript
// Filter invalid values
const cleanData = data.filter(d => d.value != null && !isNaN(d.value));

// Sort data if order matters
const sortedData = [...data].sort((a, b) => b.value - a.value);

// Parse dates
const parsedData = data.map(d => ({
  ...d,
  date: d3.timeParse("%Y-%m-%d")(d.date)
}));
```

### Performance optimisation

For large datasets (>1000 elements):

```javascript
// Use canvas instead of SVG for many elements
// Use quadtree for collision detection
// Simplify paths with d3.line().curve(d3.curveStep)
// Implement virtual scrolling for large lists
// Use requestAnimationFrame for custom animations
```

### Accessibility

Make visualisations accessible:

```javascript
// Add ARIA labels
svg.attr("role", "img")
   .attr("aria-label", "Bar chart showing quarterly revenue");

// Add title and description
svg.append("title").text("Quarterly Revenue 2024");
svg.append("desc").text("Bar chart showing revenue growth across four quarters");

// Ensure sufficient colour contrast
// Provide keyboard navigation for interactive elements
// Include data table alternative
```

### Styling

Use the Okabe-Ito colorblind-safe palette and Tufte-inspired styling:

```javascript
// Okabe-Ito colorblind-safe palette (use for ALL categorical series)
const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"];

// For ≤4 series, use direct labels instead of a legend
const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(OKABE_ITO);

// Financial gain/loss colours
const GAIN = "#2E7D32";   // Green for positive
const LOSS = "#C62828";   // Red for negative

// Design system tokens
const DESIGN = {
  text: '#1A1A1A',
  textSecondary: '#767676',
  gridLines: '#E5E5E5',
  background: '#FFFFFF',
  fontStack: "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
};

// Apply consistent typography
svg.selectAll("text")
  .style("font-family", DESIGN.fontStack)
  .style("font-size", "12px")
  .style("fill", DESIGN.text);

// Title: left-aligned, 16px, semibold
svg.append("text")
  .attr("x", margin.left)
  .attr("y", 20)
  .style("font-size", "16px")
  .style("font-weight", "600")
  .style("font-family", DESIGN.fontStack)
  .text("Chart Title");

// Source citation: right-aligned, 9px, secondary text
svg.append("text")
  .attr("x", width - margin.right)
  .attr("y", height - 5)
  .attr("text-anchor", "end")
  .style("font-size", "9px")
  .style("fill", DESIGN.textSecondary)
  .text("Source: Dataset Name");

// Horizontal gridlines only (Tufte data-ink ratio)
g.insert("g", ":first-child")
  .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(""))
  .call(g => g.select(".domain").remove())
  .call(g => g.selectAll(".tick line")
    .attr("stroke", DESIGN.gridLines)
    .attr("stroke-width", 0.8)
    .attr("opacity", 0.7));

// Remove axis spines (Tufte style — ALWAYS do this)
g.selectAll(".domain").remove();
```

## Financial chart patterns

### Time series with multiple indices (total return, price history)

For financial time series, ALWAYS use `curveLinear` — never smooth actual market data.

```javascript
function drawFinancialTimeSeries(seriesData, container) {
  // seriesData: [{ name: "S&P 500", values: [{ date: Date, value: number }] }, ...]
  const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"];
  const DESIGN = {
    text: '#1A1A1A', textSecondary: '#767676', gridLines: '#E5E5E5',
    fontStack: "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
  };

  const width = 960, height = 576;
  const margin = { top: 40, right: 120, bottom: 50, left: 65 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const svg = d3.select(container).append("svg")
    .attr("width", width).attr("height", height)
    .style("font-family", DESIGN.fontStack);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Scales
  const allDates = seriesData.flatMap(s => s.values.map(v => v.date));
  const allValues = seriesData.flatMap(s => s.values.map(v => v.value));

  const xScale = d3.scaleTime()
    .domain(d3.extent(allDates))
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([d3.min(allValues) * 0.95, d3.max(allValues) * 1.05])
    .range([innerHeight, 0]);

  const colourScale = d3.scaleOrdinal().domain(seriesData.map(s => s.name)).range(OKABE_ITO);

  // Axes — Tufte style (no spines)
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale).ticks(d3.timeYear.every(1)))
    .call(g => g.select(".domain").remove());

  g.append("g")
    .call(d3.axisLeft(yScale).tickFormat(d3.format("$,.0f")))
    .call(g => g.select(".domain").remove());

  // Horizontal gridlines (behind data)
  g.insert("g", ":first-child")
    .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(""))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line")
      .attr("stroke", DESIGN.gridLines).attr("stroke-width", 0.8).attr("opacity", 0.7));

  // Line generator — curveLinear for actual data (NO smoothing)
  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value));

  // Draw lines
  seriesData.forEach(series => {
    g.append("path")
      .datum(series.values)
      .attr("fill", "none")
      .attr("stroke", colourScale(series.name))
      .attr("stroke-width", 2)
      .attr("d", line);

    // End-of-line direct labels (for ≤4 series, use labels instead of legend)
    const lastPoint = series.values[series.values.length - 1];
    g.append("text")
      .attr("x", xScale(lastPoint.date) + 8)
      .attr("y", yScale(lastPoint.value))
      .attr("dy", "0.35em")
      .style("font-size", "11px")
      .style("font-weight", "600")
      .style("fill", colourScale(series.name))
      .text(series.name);
  });

  // Title — left-aligned, 16px, semibold
  svg.append("text")
    .attr("x", margin.left).attr("y", 24)
    .style("font-size", "16px").style("font-weight", "600")
    .style("fill", DESIGN.text)
    .text("Total Return: Major US Indexes");

  // Source — right-aligned, 9px
  svg.append("text")
    .attr("x", width - margin.right).attr("y", height - 8)
    .attr("text-anchor", "end")
    .style("font-size", "9px").style("fill", DESIGN.textSecondary)
    .text("Source: Yahoo Finance");
}
```

### Crosshair tooltip for time series

```javascript
// Add after drawing lines — creates vertical crosshair + value readout on hover
function addCrosshairTooltip(g, seriesData, xScale, yScale, colourScale, innerWidth, innerHeight) {
  const bisect = d3.bisector(d => d.date).left;

  const crosshair = g.append("line")
    .attr("class", "crosshair")
    .attr("y1", 0).attr("y2", innerHeight)
    .attr("stroke", "#999").attr("stroke-width", 0.5)
    .attr("stroke-dasharray", "4,4")
    .style("opacity", 0);

  const tooltip = g.append("g").style("opacity", 0);

  // Overlay for mouse events
  g.append("rect")
    .attr("width", innerWidth).attr("height", innerHeight)
    .attr("fill", "none").attr("pointer-events", "all")
    .on("mousemove", function(event) {
      const [mx] = d3.pointer(event);
      const date = xScale.invert(mx);

      crosshair.attr("x1", mx).attr("x2", mx).style("opacity", 1);
      tooltip.style("opacity", 1).selectAll("*").remove();

      seriesData.forEach((series, i) => {
        const idx = bisect(series.values, date, 1);
        const d = series.values[idx] || series.values[idx - 1];
        if (d) {
          tooltip.append("text")
            .attr("x", mx + 10).attr("y", 15 + i * 16)
            .style("font-size", "11px")
            .style("fill", colourScale(series.name))
            .text(`${series.name}: ${d3.format("$,.2f")(d.value)}`);
        }
      });
    })
    .on("mouseleave", () => {
      crosshair.style("opacity", 0);
      tooltip.style("opacity", 0);
    });
}
```

### Gain/loss coloring for returns

```javascript
// Color bars/values based on positive (gain) vs negative (loss)
const GAIN = "#2E7D32";  // Green
const LOSS = "#C62828";  // Red

// For bar charts with positive/negative values
bars.attr("fill", d => d.value >= 0 ? GAIN : LOSS);

// For axis labels showing +/- percentages
yAxis.tickFormat(d => (d >= 0 ? "+" : "") + d3.format(".1%")(d));

// Zero reference line
g.append("line")
  .attr("x1", 0).attr("x2", innerWidth)
  .attr("y1", yScale(0)).attr("y2", yScale(0))
  .attr("stroke", "#1A1A1A")
  .attr("stroke-width", 1);
```

## Economic & statistical chart patterns

### Horizontal bar chart (for country/category comparisons)

```javascript
function drawHorizontalBars(data, container) {
  // data: [{ label: "Country", value: number }, ...]
  const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"];
  const GAIN = "#2E7D32", LOSS = "#C62828";
  const DESIGN = {
    text: '#1A1A1A', textSecondary: '#767676', gridLines: '#E5E5E5',
    fontStack: "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
  };

  const width = 960, height = Math.max(400, data.length * 35 + 100);
  const margin = { top: 40, right: 80, bottom: 40, left: 140 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const svg = d3.select(container).append("svg")
    .attr("width", width).attr("height", height)
    .style("font-family", DESIGN.fontStack);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const sorted = [...data].sort((a, b) => b.value - a.value);

  const xScale = d3.scaleLinear()
    .domain([Math.min(0, d3.min(sorted, d => d.value)), d3.max(sorted, d => d.value)])
    .range([0, innerWidth])
    .nice();

  const yScale = d3.scaleBand()
    .domain(sorted.map(d => d.label))
    .range([0, innerHeight])
    .padding(0.2);

  // Axes — Tufte style
  g.append("g")
    .call(d3.axisBottom(xScale).tickFormat(d3.format("+.1%")))
    .attr("transform", `translate(0,${innerHeight})`)
    .call(g => g.select(".domain").remove());

  g.append("g")
    .call(d3.axisLeft(yScale))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line").remove());

  // Vertical gridlines
  g.insert("g", ":first-child")
    .call(d3.axisBottom(xScale).tickSize(innerHeight).tickFormat(""))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line")
      .attr("stroke", DESIGN.gridLines).attr("stroke-width", 0.8).attr("opacity", 0.7));

  // Bars with gain/loss coloring
  g.selectAll("rect")
    .data(sorted)
    .join("rect")
    .attr("x", d => d.value >= 0 ? xScale(0) : xScale(d.value))
    .attr("y", d => yScale(d.label))
    .attr("width", d => Math.abs(xScale(d.value) - xScale(0)))
    .attr("height", yScale.bandwidth())
    .attr("fill", d => d.value >= 0 ? GAIN : LOSS)
    .attr("rx", 2);

  // Value labels at end of bars
  g.selectAll(".value-label")
    .data(sorted)
    .join("text")
    .attr("x", d => xScale(d.value) + (d.value >= 0 ? 6 : -6))
    .attr("y", d => yScale(d.label) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", d => d.value >= 0 ? "start" : "end")
    .style("font-size", "11px").style("fill", DESIGN.text)
    .text(d => d3.format("+.1%")(d.value));

  // Zero line
  if (d3.min(sorted, d => d.value) < 0) {
    g.append("line")
      .attr("x1", xScale(0)).attr("x2", xScale(0))
      .attr("y1", 0).attr("y2", innerHeight)
      .attr("stroke", DESIGN.text).attr("stroke-width", 1);
  }
}
```

### Distribution / histogram

```javascript
function drawDistribution(values, container, { title, xLabel, bins = 40 } = {}) {
  const DESIGN = {
    text: '#1A1A1A', textSecondary: '#767676', gridLines: '#E5E5E5',
    fontStack: "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
  };

  const width = 960, height = 576;
  const margin = { top: 40, right: 30, bottom: 50, left: 60 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const svg = d3.select(container).append("svg")
    .attr("width", width).attr("height", height)
    .style("font-family", DESIGN.fontStack);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleLinear()
    .domain(d3.extent(values)).nice()
    .range([0, innerWidth]);

  const histogram = d3.bin()
    .domain(xScale.domain())
    .thresholds(xScale.ticks(bins));

  const binData = histogram(values);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(binData, d => d.length)])
    .range([innerHeight, 0])
    .nice();

  // Axes
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale))
    .call(g => g.select(".domain").remove());

  g.append("g")
    .call(d3.axisLeft(yScale))
    .call(g => g.select(".domain").remove());

  // Gridlines
  g.insert("g", ":first-child")
    .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(""))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line")
      .attr("stroke", DESIGN.gridLines).attr("stroke-width", 0.8).attr("opacity", 0.7));

  // Bars
  g.selectAll("rect")
    .data(binData)
    .join("rect")
    .attr("x", d => xScale(d.x0) + 1)
    .attr("y", d => yScale(d.length))
    .attr("width", d => Math.max(0, xScale(d.x1) - xScale(d.x0) - 2))
    .attr("height", d => innerHeight - yScale(d.length))
    .attr("fill", "#56B4E9")
    .attr("opacity", 0.85);

  // Mean line
  const mean = d3.mean(values);
  g.append("line")
    .attr("x1", xScale(mean)).attr("x2", xScale(mean))
    .attr("y1", 0).attr("y2", innerHeight)
    .attr("stroke", "#D55E00").attr("stroke-width", 2)
    .attr("stroke-dasharray", "6,3");

  g.append("text")
    .attr("x", xScale(mean) + 6).attr("y", 12)
    .style("font-size", "11px").style("fill", "#D55E00")
    .text(`μ = ${d3.format(".2f")(mean)}`);
}
```

## Self-contained HTML template

When creating standalone visualizations (not embedded in a framework), use this template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chart Title</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
      background: #FFFFFF;
      display: flex;
      justify-content: center;
      padding: 32px;
    }
    #chart { background: #FFFFFF; }
    .tooltip {
      position: absolute;
      background: white;
      border: 1px solid #E5E5E5;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 12px;
      pointer-events: none;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      opacity: 0;
      transition: opacity 150ms;
    }
  </style>
</head>
<body>
  <div id="chart"></div>
  <div class="tooltip" id="tooltip"></div>
  <script>
    // === DESIGN SYSTEM TOKENS ===
    const OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"];
    const GAIN = "#2E7D32", LOSS = "#C62828";
    const DESIGN = {
      text: '#1A1A1A',
      textSecondary: '#767676',
      gridLines: '#E5E5E5',
      fontStack: "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
    };

    // === DIMENSIONS (10:6 aspect ratio) ===
    const width = 960, height = 576;
    const margin = { top: 40, right: 120, bottom: 50, left: 65 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // === DATA ===
    // Replace with your data loading or inline data
    const data = [];

    // === DRAW ===
    const svg = d3.select("#chart").append("svg")
      .attr("width", width).attr("height", height)
      .style("font-family", DESIGN.fontStack);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Scales
    // const xScale = d3.scaleTime().domain(...).range([0, innerWidth]);
    // const yScale = d3.scaleLinear().domain(...).range([innerHeight, 0]);

    // Axes — Tufte style (ALWAYS remove spines)
    // g.append("g")
    //   .attr("transform", `translate(0,${innerHeight})`)
    //   .call(d3.axisBottom(xScale))
    //   .call(g => g.select(".domain").remove());
    //
    // g.append("g")
    //   .call(d3.axisLeft(yScale))
    //   .call(g => g.select(".domain").remove());

    // Horizontal gridlines (behind data)
    // g.insert("g", ":first-child")
    //   .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(""))
    //   .call(g => g.select(".domain").remove())
    //   .call(g => g.selectAll(".tick line")
    //     .attr("stroke", DESIGN.gridLines).attr("stroke-width", 0.8).attr("opacity", 0.7));

    // Title — left-aligned, 16px, semibold
    svg.append("text")
      .attr("x", margin.left).attr("y", 24)
      .style("font-size", "16px").style("font-weight", "600")
      .style("fill", DESIGN.text)
      .text("Chart Title");

    // Source — right-aligned, 9px
    svg.append("text")
      .attr("x", width - margin.right).attr("y", height - 8)
      .attr("text-anchor", "end")
      .style("font-size", "9px").style("fill", DESIGN.textSecondary)
      .text("Source: Dataset Name");
  </script>
</body>
</html>
```

## Design system integration

This skill follows the Universal Design System. Key rules:

1. **Palette**: Okabe-Ito colorblind-safe: `#E69F00`, `#56B4E9`, `#009E73`, `#F0E442`, `#0072B2`, `#D55E00`, `#CC79A7`
2. **Gain/Loss**: Green `#2E7D32` for positive, Red `#C62828` for negative
3. **Typography**: Inter → Helvetica Neue → Helvetica → Arial → sans-serif
4. **Axis spines**: ALWAYS remove with `.call(g => g.select(".domain").remove())`
5. **Gridlines**: Horizontal only, `#E5E5E5`, 0.8px, 0.7 opacity, inserted behind data
6. **Title**: Left-aligned, 16px, semibold, `#1A1A1A`
7. **Source citation**: Right-aligned, 9px, `#767676`
8. **Figure size**: 960×576px (10:6 ratio) for standalone charts
9. **Labels**: For ≤4 series, use end-of-line direct labels instead of a legend
10. **Line interpolation**: ALWAYS use `curveLinear` for actual/observed data. Only use smooth curves (`curveMonotoneX`, `curveBasis`) when explicitly fitting or interpolating modeled data.
11. **Tooltips**: 150ms transition, subtle shadow `0 2px 8px rgba(0,0,0,0.08)`, 6px border-radius
12. **Dot opacity**: 0.75 with white stroke for scatter plots (overlap visibility)

## Common issues and solutions

**Issue**: Axes not appearing
- Ensure scales have valid domains (check for NaN values)
- Verify axis is appended to correct group
- Check transform translations are correct

**Issue**: Transitions not working
- Call `.transition()` before attribute changes
- Ensure elements have unique keys for proper data binding
- Check that useEffect dependencies include all changing data

**Issue**: Responsive sizing not working
- Use ResizeObserver or window resize listener
- Update dimensions in state to trigger re-render
- Ensure SVG has width/height attributes or viewBox

**Issue**: Performance problems
- Limit number of DOM elements (consider canvas for >1000 items)
- Debounce resize handlers
- Use `.join()` instead of separate enter/update/exit selections
- Avoid unnecessary re-renders by checking dependencies

## Resources

### references/
Contains detailed reference materials:
- `d3-patterns.md` - Comprehensive collection of visualisation patterns and code examples
- `scale-reference.md` - Complete guide to d3 scales with examples
- `colour-schemes.md` - D3 colour schemes and palette recommendations

### assets/

Contains boilerplate templates:

- `chart-template.js` - Starter template for basic chart
- `interactive-template.js` - Template with tooltips, zoom, and interactions
- `sample-data.json` - Example datasets for testing

These templates work with vanilla JavaScript, React, Vue, Svelte, or any other JavaScript environment. Adapt them as needed for your specific framework.

To use these resources, read the relevant files when detailed guidance is needed for specific visualisation types or patterns.
