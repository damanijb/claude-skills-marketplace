# D3 Chart Library — Code Patterns

## Common Setup (used by all charts)

```javascript
// Standard margins and dimensions
const margin = { top: 40, right: 30, bottom: 50, left: 60 };
const width = 700 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// Create SVG
const svg = d3.select('#chartN')
  .append('svg')
  .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);
```

## 1. Grouped Bar Chart (CET1, ROE comparison)

```javascript
function groupedBar(container, data, labels, title) {
  const svg = createSvg(container, 700, 400);
  const g = svg.append('g').attr('transform', `translate(60,40)`);
  const w = 580, h = 300;

  const x0 = d3.scaleBand().domain(labels).range([0, w]).padding(0.2);
  const x1 = d3.scaleBand().domain(data.map(d => d.name)).range([0, x0.bandwidth()]).padding(0.05);
  const y = d3.scaleLinear().domain([0, d3.max(data, d => d3.max(d.values))]).nice().range([h, 0]);

  // Axes
  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${h})`).call(d3.axisBottom(x0));
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(6).tickFormat(d => d + '%'));

  // Bars
  const groups = g.selectAll('.group').data(data).join('g')
    .attr('fill', (d, i) => COLORS.bankPalette[i]);

  groups.selectAll('rect').data(d => labels.map((l, i) => ({ label: l, value: d.values[i] })))
    .join('rect')
    .attr('x', d => x0(d.label) + x1(groups.datum().name))
    .attr('y', d => y(d.value))
    .attr('width', x1.bandwidth())
    .attr('height', d => h - y(d.value))
    .attr('rx', 2)
    .on('mouseover', (e, d) => showTooltip(e, `${d.label}: ${d.value.toFixed(1)}%`))
    .on('mouseout', hideTooltip);
}
```

## 2. Line Chart with Event Annotations

```javascript
function lineWithEvents(container, series, events) {
  const svg = createSvg(container, 700, 400);
  const g = svg.append('g').attr('transform', 'translate(60,40)');
  const w = 600, h = 300;

  const x = d3.scaleTime().domain(d3.extent(series, d => d.date)).range([0, w]);
  const y = d3.scaleLinear().domain(d3.extent(series, d => d.value)).nice().range([h, 0]);

  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${h})`).call(d3.axisBottom(x).ticks(6));
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y));

  // Line
  const line = d3.line().x(d => x(d.date)).y(d => y(d.value)).curve(d3.curveMonotoneX);
  g.append('path').datum(series).attr('d', line)
    .attr('fill', 'none').attr('stroke', COLORS.navy).attr('stroke-width', 2.5);

  // Event markers
  events.forEach(evt => {
    const cx = x(evt.date), cy = y(evt.value);
    g.append('circle').attr('cx', cx).attr('cy', cy).attr('r', 5)
      .attr('fill', evt.color || COLORS.warning).attr('stroke', 'white').attr('stroke-width', 2);
    g.append('text').attr('x', cx).attr('y', cy - 12).attr('text-anchor', 'middle')
      .attr('font-size', '10px').attr('fill', COLORS.muted).text(evt.label);
  });
}
```

## 3. Horizontal Bar Chart (NPL, Cost of Risk ranking)

```javascript
function horizontalBar(container, data) {
  // data: [{ name: "Bank", value: 1.5 }, ...] sorted
  const svg = createSvg(container, 700, 400);
  const g = svg.append('g').attr('transform', 'translate(150,20)');
  const w = 500, h = 360;

  const sorted = data.sort((a, b) => a.value - b.value);
  const y = d3.scaleBand().domain(sorted.map(d => d.name)).range([0, h]).padding(0.3);
  const x = d3.scaleLinear().domain([0, d3.max(sorted, d => d.value) * 1.1]).range([0, w]);

  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).tickSize(0));
  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${h})`).call(d3.axisBottom(x).ticks(5));

  g.selectAll('rect').data(sorted).join('rect')
    .attr('y', d => y(d.name)).attr('height', y.bandwidth())
    .attr('x', 0).attr('width', d => x(d.value))
    .attr('fill', (d, i) => d.highlight ? COLORS.navy : '#94a3b8').attr('rx', 3);

  g.selectAll('.val-label').data(sorted).join('text')
    .attr('x', d => x(d.value) + 6).attr('y', d => y(d.name) + y.bandwidth() / 2 + 4)
    .attr('font-size', '11px').attr('fill', COLORS.text).text(d => d.value.toFixed(1) + '%');
}
```

## 4. Radar/Spider Chart (Credit Scorecard)

```javascript
function radarChart(container, dimensions, scores) {
  // dimensions: ["Capital", "Profitability", "Asset Quality", "Efficiency", "Liquidity", "Ratings"]
  // scores: [8.5, 7.2, 6.8, 7.5, 8.0, 7.0] (0-10 scale)
  const svg = createSvg(container, 500, 500);
  const g = svg.append('g').attr('transform', 'translate(250,260)');
  const r = 180;
  const levels = 5;
  const n = dimensions.length;
  const angle = (2 * Math.PI) / n;

  // Grid lines
  for (let lvl = 1; lvl <= levels; lvl++) {
    const radius = (r * lvl) / levels;
    const points = dimensions.map((_, i) => {
      const a = angle * i - Math.PI / 2;
      return [radius * Math.cos(a), radius * Math.sin(a)];
    });
    g.append('polygon')
      .attr('points', points.map(p => p.join(',')).join(' '))
      .attr('fill', 'none').attr('stroke', '#e5e7eb').attr('stroke-width', 1);
  }

  // Axis lines
  dimensions.forEach((_, i) => {
    const a = angle * i - Math.PI / 2;
    g.append('line').attr('x1', 0).attr('y1', 0)
      .attr('x2', r * Math.cos(a)).attr('y2', r * Math.sin(a))
      .attr('stroke', '#d1d5db').attr('stroke-width', 1);
  });

  // Data polygon
  const dataPoints = scores.map((s, i) => {
    const a = angle * i - Math.PI / 2;
    const radius = (r * s) / 10;
    return [radius * Math.cos(a), radius * Math.sin(a)];
  });
  g.append('polygon')
    .attr('points', dataPoints.map(p => p.join(',')).join(' '))
    .attr('fill', COLORS.navy).attr('fill-opacity', 0.2)
    .attr('stroke', COLORS.navy).attr('stroke-width', 2.5);

  // Data dots
  dataPoints.forEach((p, i) => {
    g.append('circle').attr('cx', p[0]).attr('cy', p[1]).attr('r', 5)
      .attr('fill', COLORS.navy).attr('stroke', 'white').attr('stroke-width', 2);
  });

  // Labels
  dimensions.forEach((dim, i) => {
    const a = angle * i - Math.PI / 2;
    const lx = (r + 24) * Math.cos(a);
    const ly = (r + 24) * Math.sin(a);
    g.append('text').attr('x', lx).attr('y', ly)
      .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle')
      .attr('font-size', '12px').attr('font-weight', '600').attr('fill', COLORS.text)
      .text(`${dim} (${scores[i].toFixed(1)})`);
  });
}
```

## 5. Waterfall Chart (ROE Decomposition)

```javascript
function waterfall(container, components) {
  // components: [{ name: "NII", value: 8.5 }, { name: "Fees", value: 3.2 }, { name: "Costs", value: -6.1 }, ...]
  const svg = createSvg(container, 700, 400);
  const g = svg.append('g').attr('transform', 'translate(60,40)');
  const w = 600, h = 300;

  let cumulative = 0;
  const processed = components.map(d => {
    const start = cumulative;
    cumulative += d.value;
    return { ...d, start, end: cumulative };
  });
  // Add total bar
  processed.push({ name: 'ROE', value: cumulative, start: 0, end: cumulative, isTotal: true });

  const x = d3.scaleBand().domain(processed.map(d => d.name)).range([0, w]).padding(0.3);
  const yMax = d3.max(processed, d => Math.max(d.start, d.end)) * 1.2;
  const yMin = d3.min(processed, d => Math.min(d.start, d.end, 0)) * 1.2;
  const y = d3.scaleLinear().domain([yMin, yMax]).nice().range([h, 0]);

  g.append('g').attr('class', 'axis').attr('transform', `translate(0,${h})`).call(d3.axisBottom(x));
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(6).tickFormat(d => d + '%'));

  // Zero line
  g.append('line').attr('x1', 0).attr('x2', w).attr('y1', y(0)).attr('y2', y(0))
    .attr('stroke', '#9ca3af').attr('stroke-width', 1);

  // Bars
  g.selectAll('rect').data(processed).join('rect')
    .attr('x', d => x(d.name))
    .attr('y', d => d.isTotal ? y(Math.max(0, d.end)) : y(Math.max(d.start, d.end)))
    .attr('width', x.bandwidth())
    .attr('height', d => d.isTotal ? Math.abs(y(0) - y(d.end)) : Math.abs(y(d.start) - y(d.end)))
    .attr('fill', d => d.isTotal ? COLORS.navy : d.value >= 0 ? COLORS.positive : COLORS.negative)
    .attr('rx', 3);

  // Value labels
  g.selectAll('.val').data(processed).join('text')
    .attr('x', d => x(d.name) + x.bandwidth() / 2)
    .attr('y', d => y(d.end) - 6)
    .attr('text-anchor', 'middle').attr('font-size', '11px').attr('font-weight', '600')
    .attr('fill', COLORS.text)
    .text(d => (d.value >= 0 ? '+' : '') + d.value.toFixed(1) + '%');
}
```

## 6. Heatmap (Peer Comparison Matrix)

```javascript
function heatmap(container, metrics, banks, values) {
  // metrics: ["ROE", "CET1", "NPL", ...]
  // banks: ["BNP", "SocGen", "DB", ...]
  // values: 2D array [bank][metric] with normalized 0-1 scores
  const svg = createSvg(container, 800, 400);
  const g = svg.append('g').attr('transform', 'translate(120,40)');
  const cellW = 65, cellH = 35;

  const colorScale = d3.scaleSequential(d3.interpolateRdYlGn).domain([0, 1]);

  // Cells
  banks.forEach((bank, bi) => {
    metrics.forEach((metric, mi) => {
      const val = values[bi][mi];
      g.append('rect')
        .attr('x', mi * cellW).attr('y', bi * cellH)
        .attr('width', cellW - 2).attr('height', cellH - 2)
        .attr('fill', colorScale(val)).attr('rx', 4);
      g.append('text')
        .attr('x', mi * cellW + cellW / 2).attr('y', bi * cellH + cellH / 2 + 4)
        .attr('text-anchor', 'middle').attr('font-size', '11px')
        .attr('fill', val > 0.5 ? '#1a1a2e' : 'white')
        .text(values[bi][mi].toFixed(1));
    });
  });

  // Labels
  banks.forEach((bank, i) => {
    g.append('text').attr('x', -8).attr('y', i * cellH + cellH / 2 + 4)
      .attr('text-anchor', 'end').attr('font-size', '12px').attr('fill', COLORS.text).text(bank);
  });
  metrics.forEach((metric, i) => {
    g.append('text').attr('x', i * cellW + cellW / 2).attr('y', -8)
      .attr('text-anchor', 'middle').attr('font-size', '11px').attr('fill', COLORS.muted).text(metric);
  });
}
```

## Helper: Create SVG

```javascript
function createSvg(container, width, height) {
  return d3.select(container)
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('width', width)
    .attr('height', height);
}
```
