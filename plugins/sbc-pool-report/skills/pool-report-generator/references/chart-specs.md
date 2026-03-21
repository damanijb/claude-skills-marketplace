# Chart Specifications

## Brand Color Palette

### Primary Colors
```python
BRAND_COLORS = {
    'primary': '#003366',       # SB County ATC navy blue
    'secondary': '#002244',     # Dark navy (gradients)
    'accent': '#7CC6DD',        # Light cyan (highlights)
    'accent_light': '#A8DBE8',  # Lighter cyan variant
    'gold': '#FFB703',          # Gold (accents, hover)
    'orange': '#E97007',        # Orange (charts)
    'green': '#70AD47',         # Green (positive indicators)
    'gray': '#A5A5A5',          # Neutral gray
    'text': '#2D3748',          # Body text
    'light_bg': '#F7F9FC',      # Card background
    'table_stripe': '#F8FAFC',  # Alternating rows
}
```

### Chart Sequence (12 colors)
```python
CHART_COLORS = [
    '#003366', '#E97007', '#FFB703', '#70AD47',
    '#7CC6DD', '#A5A5A5', '#002244', '#A8DBE8',
    '#F4B183', '#FFD966', '#A9D18E', '#D6DCE4',
]
```

### Doughnut Colors (high contrast)
```python
DOUGHNUT_COLORS = [
    '#003366', '#0693E3', '#7CC6DD', '#FFB703',
    '#E97007', '#00D084', '#9B51E0', '#C00000',
    '#3b5ea1', '#f59e42', '#2ea87e', '#7c3aed',
]
```

## Chart Types & Specifications

### 1. Sector Allocation — Doughnut Chart
- **Function:** `render_doughnut(labels, values, colors, center_text, figsize)`
- **Size:** 5" × 5"
- **Center text:** Total market value (e.g., "$14.23B")
- **Colors:** DOUGHNUT_COLORS
- **Labels:** Show % for slices ≥ 3%
- **Ring width:** 0.45 (matplotlib wedgeprops)
- **Paired with:** Color-coded table on the right

### 2. Maturity Distribution — Bar Chart
- **Function:** `render_bar_chart(categories, values, y_label, colors, data_label_fmt, figsize)`
- **Size:** 9" × 4"
- **Color:** Single color #003366
- **Data labels:** Dollar amounts (e.g., "$1,234M")
- **Categories:** Top 10 maturity buckets by value
- **Y-axis:** "Market Value ($M)"

### 3. Credit Quality — Doughnut Chart (×2: S&P and Moody's)
- **Same specs as Sector Allocation**
- **One chart per rating agency**
- **Paired with rating summary table**

### 4. Yield Curve — Line Chart
- **Function:** `render_line_chart(series_list, labels, series_names, y_label, colors, point_markers, figsize)`
- **Size:** 6" × 3.5"
- **Series:** Current yields + Prior Year yields
- **Colors:** #003366 (current), #FFB703 (prior)
- **Point markers:** Yes
- **Y-axis label:** "Yield (%)"
- **Labels:** Treasury tenors (1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y)

### 5. Return Comparison — Grouped Bar Chart
- **Function:** `render_grouped_bar(categories, groups, group_labels, colors, y_label)`
- **Size:** 7" × 3.5"
- **Groups:** Portfolio return + Benchmark return
- **Colors:** #003366 (portfolio), #FFB703 (benchmark)
- **Categories:** Monthly periods (Jan '25, Feb '25, etc.)

### 6. Cumulative Returns — Line Chart
- **Same specs as Yield Curve**
- **Series:** Cumulative portfolio + Cumulative benchmark
- **Y-axis:** "Cumulative Return (%)"

### 7. Cash Flow Projections — Stacked Bar Chart
- **Function:** `render_stacked_bar(categories, groups, group_labels, colors, y_label)`
- **Size:** 7" × 3.5"
- **Stacks:** Principal ($M) + Coupon ($M)
- **Colors:** #003366 (principal), #FFB703 (coupon)
- **Categories:** Monthly periods

### 8. Horizon Analysis — Bar Chart (conditional colors)
- **Function:** `render_bar_chart(categories, values, colors, y_label, data_label_fmt)`
- **Size:** 7" × 3.5"
- **Colors:** Conditional — #70AD47 (positive return), #C00000 (negative)
- **Categories:** Scenario names (-25 bps, 0, +25, +50, +100)
- **Data labels:** Return % (e.g., "2.45%")

## Rendering Details

### Font Configuration
```python
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Helvetica Neue', 'Arial'],
    'font.size': 10,
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.5,
    'xtick.color': '#666666',
    'ytick.color': '#666666',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': False,
})
```

### Output Format
- DPI: 150
- Background: White
- No gridlines
- Despine: Remove top and right axis borders
- X-labels: Max 8 visible, never rotated
- All charts render to base64 PNG `<img>` tags for HTML

### For PPTX
Use the `_figure` variants (e.g., `render_bar_chart_figure()`) which return matplotlib Figure objects. Save to PNG buffer, then embed in slides with PptxGenJS via base64.

---

## Economic Trend Charts (NEW in v2)

All economic trend charts share these common specs:
- **Size:** 4.5" × 3.0" (fits in left column of two-column layout)
- **DPI:** 200
- **Background:** White (RGB)
- **Despine:** Remove top and right axis borders
- **Gridlines:** None (clean look)
- **X-axis:** Month abbreviations (Mar, Apr, May...), max 12 labels
- **Endpoint annotation:** Latest value displayed at right end of line
- **Font:** Same as other charts (Segoe UI / Helvetica Neue / Arial)

### 9. Fed Funds Rate History — Line + Area Chart
- **Data source:** FEDFUNDS 12-month history
- **Line color:** #003366 (navy), linewidth 2.5
- **Area fill:** #E2E8F0 (light blue-gray), alpha 0.3
- **Y-axis:** "Rate (%)"
- **Endpoint annotation:** Latest rate with date
- **Notable feature:** If rate changed during period, mark the change point

### 10. CPI Year-over-Year — Line Chart
- **Data source:** CPIAUCSL 12-month history (calculate YoY % change)
- **Calculation:** `yoy_pct = (current_value / value_12_months_ago - 1) * 100`
- **Line color:** #E97007 (orange), linewidth 2.5
- **Reference line:** Horizontal dashed line at 2.0% (Fed target), color #70AD47 (green), label "Fed Target: 2%"
- **Y-axis:** "Year-over-Year Change (%)"

### 11. Unemployment Rate — Line Chart
- **Data source:** UNRATE 12-month history
- **Line color:** #003366 (navy), linewidth 2.5
- **Y-axis:** "Rate (%)"
- **Y-axis range:** Auto with slight padding (don't start at 0 — show granularity)

### 12. BBB Credit Spread — Line + Area Chart
- **Data source:** BAMLC0A4CBBB 12-month history
- **Line color:** #C00000 (red), linewidth 2.5
- **Area fill:** #FADBD8 (light red), alpha 0.3
- **Y-axis:** "Spread (percentage points)"
- **Context annotation:** "Tighter = more confidence" or "Wider = more risk" as subtle footnote

### 13. Yield Curve Comparison — Dual Line Chart
- **Data sources:** Current DGS* values + 12-month-ago DGS* values
- **Current curve:** #003366 (solid, linewidth 2.5, marker 'o')
- **Prior curve:** #FFB703 (dashed, linewidth 1.5, marker 's')
- **X-axis:** Tenor labels: 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y
- **Y-axis:** "Yield (%)"
- **Legend:** "Current (Jan 2026)" vs "1 Year Ago (Jan 2025)"
- **Point markers:** Yes, with value annotations on current curve endpoints

---

## Typography

### Slide Dimensions
- Width: 11 inches
- Height: 8.5 inches (landscape letter)
- Header height: 55px
- Footer height: 40px
- Content padding: 25px 40px

### Font Sizes
| Element | Size |
|---------|------|
| Slide title (h1) | 24px bold |
| Subtitle (h2) | 11px |
| Body text | 11px |
| Table header | 10px uppercase |
| Table body | 11px |
| Table footnote | 9px |
| Summary card value | 28px bold |
| Summary card label | 11px |
| Footer text | 10px |
