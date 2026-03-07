# SBC Treasury Style Guide

## Brand Colors

| Role | Hex | Usage |
|------|-----|-------|
| Primary Navy | `#1f4296` | Headings, chart accents, table headers |
| Navy Hover | `#1a3a85` | Interactive hover states |
| Navy Dark | `#112357` | Cover/header gradients |
| Positive | `#27ae60` | Favorable metrics, upward trends |
| Negative | `#e74c3c` | Adverse metrics, downward trends |
| Warning | `#f39c12` | Caution, watch items, amber scores |
| Neutral Blue | `#3498db` | Informational, supplementary data |
| Text | `#1a1a2e` | Body text |
| Muted | `#6b7280` | Subtitles, captions, axis labels |
| Border | `#e5e7eb` | Table borders, dividers |
| Background | `#fafafa` | Page background (charts only) |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Heading 1 | Inter | 18pt | Bold (700) | Navy `#1f4296` |
| Heading 2 | Inter | 14pt | Bold (700) | Navy `#1f4296` |
| Heading 3 | Inter | 12pt | Bold (700) | Dark Gray `#374151` |
| Body | Inter | 11pt | Regular (400) | Text `#1a1a2e` |
| Table Header | Inter | 10pt | Bold (700) | White on Navy |
| Table Body | Inter | 10pt | Regular (400) | Text `#1a1a2e` |
| Caption | Inter | 9pt | Regular (400) | Muted `#6b7280` |
| Footer | Inter | 8pt | Regular (400) | Muted `#6b7280` |

Fallback font stack: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

## Page Layout

- **Page size**: US Letter (8.5" × 11")
- **Margins**: 1" all sides
- **Line spacing**: 1.15 for body text, 1.0 for tables
- **Paragraph spacing**: 6pt after paragraphs, 12pt before headings
- **Column layout**: Single column for narrative; two-column for side-by-side metrics

## Table Styling

- Header row: Navy background `#1f4296`, white text, bold
- Alternating rows: White `#ffffff` / Light gray `#f9fafb`
- Border: 0.5pt solid `#e5e7eb`
- Cell padding: 4pt vertical, 6pt horizontal
- Numbers: Right-aligned
- Text: Left-aligned
- Header text: Center-aligned

## Chart Embedding

- Charts embedded as PNG images at 2x resolution for print clarity
- Maximum width: 6.5" (fills page between margins)
- Half-width charts: 3.1" (for two-column layout)
- Caption below each chart in 9pt muted text
- 12pt spacing before and after chart images

## Cover Page

```
[Navy gradient header block — full width]

# {Issuer} — Credit Analysis

## {Date}

### Prepared by San Bernardino County Treasury — Investment Division

[Horizontal rule]

[Executive summary infographic image]
```

## Footer

Every page after the cover includes:
- Left: "San Bernardino County Treasury — Investment Division"
- Center: Page number
- Right: "Confidential"
- Font: 8pt Inter, Muted color

## Color Usage Guidelines

- Use Navy for all primary visual elements (headings, chart highlights, table headers)
- Use semantic colors ONLY for their intended meaning (green=positive, red=negative, amber=caution)
- Never use more than 3 accent colors on a single chart
- Gray palette (`#94a3b8`, `#6b7280`, `#4b5563`) for secondary/peer data points
- The target issuer is ALWAYS navy; peers are always gray tones
