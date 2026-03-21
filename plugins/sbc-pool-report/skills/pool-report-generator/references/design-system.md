# Design System

San Bernardino County Investment Pool Report — visual design tokens and layout geometry.

## Slide Dimensions

- Layout: `LAYOUT_16x9` (10" × 5.625")
- All coordinates in inches

## Layout Geometry

### Header
- Position: x: 0, y: 0, w: 10, h: 0.75
- Fill: #003366 (primary navy)
- Title: white, Arial Black 20pt, x: 0.5, y: 0.15, margin: 0
- Gold accent line: x: 0, y: 0.73, w: 10, h: 0.02, fill: #C8910A
- County logo: top-right corner with dark triangle background

### Footer
- Position: x: 0, y: 5.08, w: 10, h: 0.545
- Fill: #003366
- Page number: right-aligned, white, 8pt, x: 9.3, y: 5.15

### Content Safe Zone
- Top: y = 0.9" (below header + padding)
- Bottom: y = 4.9" (above footer)
- Left: x = 0.5"
- Right: x = 9.5"
- Available height: 4.0"
- Available width: 9.0"

**CRITICAL: No text, chart, or table may extend below y = 4.9" or it will overlap the footer.**

### Two-Column Layout
- Left column: x: 0.5, w: 4.25
- Right column: x: 5.0, w: 4.5
- Gap: 0.25"
- Both columns share the same y-range: 0.9" to 4.9"

### KPI Cards (3-across)
- Card width: (9.0 - 2 * 0.15) / 3 = 2.9"
- Card height: 0.8"
- Card y: 0.95"
- Card 1 x: 0.5, Card 2 x: 3.55, Card 3 x: 6.6
- Fill: #F7F9FC
- Border: thin line #E2E8F0

### KPI Cards (4-across)
- Card width: (9.0 - 3 * 0.15) / 4 = 2.1375"
- Same y-position rules

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Primary Navy | 003366 | Headers, footers, primary backgrounds |
| Dark Navy | 002244 | Gradient overlay on cover |
| Gold | C8910A | Accent lines, section labels |
| Light Gold | FFB703 | Chart accent, hover states |
| Orange | E97007 | Chart data points |
| Green | 70AD47 | Positive indicators, COMPLIANT status |
| Red | C00000 | Negative indicators, EXCEEDS status |
| Amber | FFC000 | Warning, Near Limit status |

### Text Colors
| Element | Hex |
|---------|-----|
| Body text | 333333 |
| Muted text | 666666 |
| Footnotes | 888888 |
| White (on dark bg) | FFFFFF |

### Background Colors
| Element | Hex |
|---------|-----|
| Card background | F7F9FC |
| Table stripe | F8FAFC |
| Table header | 003366 |
| Slide background | FFFFFF |

### Chart Color Sequence (12 colors)
```
003366, E97007, FFB703, 70AD47, 7CC6DD, A5A5A5,
002244, A8DBE8, F4B183, FFD966, A9D18E, D6DCE4
```

### Doughnut Colors (high contrast)
```
003366, 0693E3, 7CC6DD, FFB703, E97007, 00D084,
9B51E0, C00000, 3b5ea1, f59e42, 2ea87e, 7c3aed
```

## Typography

### Font Pairing
- **Headers**: Arial Black (slide titles) — bold, institutional presence
- **Body**: Calibri — clean, readable, universal availability

### Size Hierarchy
| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Slide title | Arial Black | 20pt | Normal | FFFFFF |
| Section label | Calibri | 10pt | Bold | C8910A |
| Section label style | ALL CAPS | — | charSpacing: 3 | — |
| Body text | Calibri | 12pt | Normal | 333333 |
| Body text lineSpacing | — | — | lineSpacingMultiple: 1.15 | — |
| Table header | Calibri | 10pt | Bold | FFFFFF |
| Table body | Calibri | 10pt | Normal | 333333 |
| KPI value | Calibri | 28pt | Bold | 003366 |
| KPI label | Calibri | 10pt | Normal | 666666 |
| Footnote | Calibri | 8pt | Italic | 888888 |
| Page number | Calibri | 8pt | Normal | FFFFFF |

### Text Box Defaults
- `margin: [0.05, 0.1, 0.05, 0.1]` (top, right, bottom, left in inches)
- `valign: "top"` for body text
- `valign: "middle"` for KPI cards and table cells
- `paraSpaceAfter: 6` for body paragraphs (prevents cramping)

## Table Styling

### Standard Data Table
```javascript
// Header row
{ fill: { color: "003366" }, color: "FFFFFF", bold: true, fontSize: 10, fontFace: "Calibri" }

// Body rows (alternating)
{ fill: { color: "FFFFFF" }, color: "333333", fontSize: 10, fontFace: "Calibri" }
{ fill: { color: "F8FAFC" }, color: "333333", fontSize: 10, fontFace: "Calibri" }

// Border
{ pt: 0.5, color: "E2E8F0" }
```

### Compliance Status Colors
| Status | Text Color | Background |
|--------|-----------|------------|
| COMPLIANT / PASS | 70AD47 | — |
| Near Limit | FFC000 | — |
| EXCEEDS | C00000 | — |

## Cover Slide Design

- Full navy background: #003366
- Dark triangle overlay in top-right (using shapes)
- County logo in the triangle
- Department text: "Auditor-Controller / Treasurer / Tax Collector" — white, 12pt
- Sub-department: "Treasurer Division" — white, 10pt
- Title: "Investment Pool Report" — white, bold, 44pt, centered
- Date: formatted as "Month DD, YYYY" — gold (#C8910A), 24pt, centered
