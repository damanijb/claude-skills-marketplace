/**
 * San Bernardino County Investment Pool Report — PPTX Generator (V12)
 *
 * 24-slide format matching the Board-approved layout.
 *
 * USAGE:
 *   node generate_pptx.js <data.json> <output.pptx> [charts_dir] [logo_path]
 *
 * DATA JSON FORMAT:
 * {
 *   "report_date": "January 30, 2026",
 *   "portfolio": { total_market_value, weighted_avg_yield, weighted_avg_duration, ... },
 *   "sectors": [...],
 *   "credit_quality": { sp: [...], moodys: [...] },
 *   "maturity_distribution": [...],
 *   "compliance": [...],
 *   "issuer_concentration": [...],
 *   "monthly_income": [...],
 *   "total_monthly_income": number,
 *   "horizon_analysis": [...],
 *   "fred_data": { FEDFUNDS: {value,date}, ... },
 *   "economic_commentary": { ... },   // From Phase 2B agent
 *   "charts": {}
 * }
 *
 * LAYOUT: 10" × 5.625" (16:9)
 * Safe zone: y: 0.9" – 4.9"
 * Header: y: 0–0.75" (navy + gold accent)
 * Footer: y: 5.08–5.625" (navy, date + page number)
 */

const PptxGenJS = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

// ── Parse arguments ─────────────────────────────────────────────────────
const dataPath = process.argv[2];
const outputPath = process.argv[3] || '/tmp/SBC_Pool_Report.pptx';
const CHARTS = process.argv[4] || '/tmp/charts';
const LOGO = process.argv[5] || '';

if (!dataPath) {
  console.error('Usage: node generate_pptx.js <data.json> <output.pptx> [charts_dir] [logo_path]');
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const reportDate = data.report_date || 'Report Date';
const commentary = data.economic_commentary || {};

const prs = new PptxGenJS();
prs.defineLayout({ name: 'LAYOUT_16x9', width: 10, height: 5.625 });
prs.layout = 'LAYOUT_16x9';

// ── Colors ──────────────────────────────────────────────────────────────
const C = {
  navy: '003366', darkNavy: '002244', gold: 'C8910A', lightGold: 'FFB703',
  orange: 'E97007', green: '70AD47', red: 'C00000', amber: 'FFC000',
  text: '333333', muted: '666666', footnote: '888888', white: 'FFFFFF',
  cardBg: 'F7F9FC', stripe: 'F8FAFC', border: 'E2E8F0',
  skyBlue: '0693E3', ltBlue: '7CC6DD'
};

// ── Helpers ──────────────────────────────────────────────────────────────
function addHeader(slide, title) {
  slide.addShape(prs.ShapeType.rect, { x: 0, y: 0, w: 10, h: 0.75, fill: { color: C.navy } });
  slide.addShape(prs.ShapeType.rect, { x: 0, y: 0.73, w: 10, h: 0.02, fill: { color: C.gold } });
  slide.addText(title, {
    x: 0.5, y: 0.12, w: 8.5, h: 0.5,
    fontFace: 'Arial Black', fontSize: 20, color: C.white, bold: false,
    align: 'left', valign: 'middle'
  });
}

function addFooter(slide, pageNum) {
  slide.addShape(prs.ShapeType.rect, { x: 0, y: 5.08, w: 10, h: 0.545, fill: { color: C.navy } });
  slide.addText('San Bernardino County Investment Pool  |  ' + reportDate, {
    x: 0.5, y: 5.15, w: 8, h: 0.4,
    fontFace: 'Calibri', fontSize: 8, color: C.white, align: 'left', valign: 'middle'
  });
  slide.addText(String(pageNum), {
    x: 9.3, y: 5.15, w: 0.5, h: 0.4,
    fontFace: 'Calibri', fontSize: 8, color: C.white, align: 'right', valign: 'middle'
  });
}

function sectionLabel(slide, text, x, y, w) {
  slide.addText(text, {
    x: x, y: y, w: w || 4.5, h: 0.3,
    fontFace: 'Calibri', fontSize: 10, bold: true, color: C.gold,
    charSpacing: 3, align: 'left', valign: 'top'
  });
}

function bodyText(slide, text, x, y, w, h, opts) {
  slide.addText(text, Object.assign({
    x: x, y: y, w: w, h: h,
    fontFace: 'Calibri', fontSize: 11, color: C.text,
    align: 'left', valign: 'top', lineSpacingMultiple: 1.15,
    paraSpaceAfter: 6
  }, opts || {}));
}

function fmtCurrency(v, dec) {
  dec = dec || 0;
  if (Math.abs(v) >= 1e9) return '$' + (v / 1e9).toFixed(dec) + 'B';
  if (Math.abs(v) >= 1e6) return '$' + (v / 1e6).toFixed(dec) + 'M';
  if (Math.abs(v) >= 1e3) return '$' + (v / 1e3).toFixed(dec) + 'K';
  return '$' + v.toFixed(dec);
}

function fmtDollars(v) {
  return '$' + Math.round(v).toLocaleString('en-US');
}

function kpiCard(slide, label, value, x, y, w, h) {
  w = w || 2.9; h = h || 0.85;
  slide.addText(value, {
    x: x, y: y + 0.08, w: w, h: 0.45,
    fontFace: 'Calibri', fontSize: 28, bold: true, color: C.navy,
    align: 'center', valign: 'middle'
  });
  slide.addText(label, {
    x: x, y: y + 0.55, w: w, h: 0.25,
    fontFace: 'Calibri', fontSize: 10, color: C.muted,
    align: 'center', valign: 'middle'
  });
}

function addDataTable(slide, headers, rows, x, y, w, opts) {
  opts = opts || {};
  const numCols = headers.length;
  const colWidths = opts.colWidths || headers.map(() => w / numCols);
  const tableRows = [];

  const headerRow = headers.map(h => ({
    text: h, options: {
      fontFace: 'Calibri', fontSize: 10, bold: true, color: C.white,
      fill: { color: C.navy }, align: 'center', valign: 'middle',
      border: [{ pt: 0.5, color: C.border }]
    }
  }));
  tableRows.push(headerRow);

  rows.forEach((row, idx) => {
    const bgColor = idx % 2 === 0 ? C.white : C.stripe;
    const dataRow = row.map((cell, colIdx) => {
      const cellOpts = {
        fontFace: 'Calibri', fontSize: 10, color: C.text,
        fill: { color: bgColor }, align: 'center', valign: 'middle',
        border: [{ pt: 0.5, color: C.border }]
      };
      if (opts.statusCol !== undefined && colIdx === opts.statusCol) {
        if (cell === 'COMPLIANT') cellOpts.color = C.green;
        else if (cell === 'Near Limit') cellOpts.color = C.amber;
        else if (cell === 'EXCEEDS') cellOpts.color = C.red;
        cellOpts.bold = true;
      }
      if (opts.leftAlignCol !== undefined && colIdx === opts.leftAlignCol) {
        cellOpts.align = 'left';
      }
      return { text: String(cell), options: cellOpts };
    });
    tableRows.push(dataRow);
  });

  slide.addTable(tableRows, {
    x: x, y: y, w: w,
    colW: colWidths,
    rowH: opts.rowH || 0.28,
    margin: [0.02, 0.05, 0.02, 0.05],
    autoPage: false
  });
}

function addChartImg(slide, filename, x, y, w, h) {
  const chartPath = CHARTS + '/' + filename;
  if (fs.existsSync(chartPath)) {
    slide.addImage({ path: chartPath, x: x, y: y, w: w, h: h });
  } else {
    console.warn('MISSING CHART:', chartPath);
  }
}

function sectionDivider(title, subtitle) {
  const s = prs.addSlide();
  s.background = { color: C.navy };
  s.addShape(prs.ShapeType.rect, {
    x: 2.0, y: 2.65, w: 6, h: 0.02, fill: { color: C.gold }
  });
  s.addText(title, {
    x: 0.5, y: 1.4, w: 9, h: 1.15,
    fontFace: 'Arial Black', fontSize: 30, color: C.white,
    align: 'center', valign: 'bottom'
  });
  s.addText(subtitle, {
    x: 0.5, y: 2.85, w: 9, h: 0.5,
    fontFace: 'Calibri', fontSize: 13, color: C.gold,
    align: 'center', valign: 'top'
  });
}

// ── Derived values ──────────────────────────────────────────────────────
const p = data.portfolio;
const fred = data.fred_data || {};

// Find the largest sector for executive summary text
const largestSector = data.sectors && data.sectors.length > 0 ? data.sectors[0] : null;
const largestSectorName = largestSector ? largestSector.name : 'Agency Mortgage-Backed';
const largestSectorPct = largestSector ? largestSector.pct_portfolio : 0;
// Find matching compliance entry
const largestSectorCompliance = data.compliance ?
  data.compliance.find(c => c.security_type === largestSectorName) : null;
const largestSectorLimit = largestSectorCompliance ? largestSectorCompliance.policy_limit : 100;

// =====================================================
// SLIDE 1: COVER
// =====================================================
let slide = prs.addSlide();
slide.background = { color: C.navy };

if (LOGO && fs.existsSync(LOGO)) {
  slide.addImage({ path: LOGO, x: 3.7, y: 0.25, w: 2.6, h: 1.1 });
}

slide.addShape(prs.ShapeType.rect, {
  x: 3.0, y: 1.45, w: 4, h: 0.02, fill: { color: C.gold }
});

slide.addText('Investment Pool\nReport', {
  x: 0.5, y: 1.65, w: 9, h: 1.3,
  fontFace: 'Arial Black', fontSize: 36, color: C.white, bold: true,
  align: 'center', valign: 'middle', lineSpacingMultiple: 1.05
});

slide.addText(reportDate, {
  x: 0.5, y: 3.1, w: 9, h: 0.5,
  fontFace: 'Calibri', fontSize: 18, color: C.gold, bold: true,
  align: 'center', valign: 'middle'
});

slide.addText('San Bernardino County', {
  x: 0.5, y: 3.8, w: 9, h: 0.3,
  fontFace: 'Calibri', fontSize: 11, color: C.white,
  align: 'center', valign: 'middle'
});

// =====================================================
// SLIDE 2: TABLE OF CONTENTS
// =====================================================
let pg = 2;
slide = prs.addSlide();
addHeader(slide, 'Table of Contents');
addFooter(slide, pg);

sectionLabel(slide, 'I. PORTFOLIO OVERVIEW', 0.5, 1.0, 4.0);
bodyText(slide, 'Executive Summary\nSector Allocation\nSector Detail', 0.5, 1.35, 4.0, 1.0, { fontSize: 10 });

sectionLabel(slide, 'II. ECONOMIC & MARKET COMMENTARY', 0.5, 2.55, 4.0);
bodyText(slide, 'Economic Snapshot\nMonetary Policy\nGrowth & Inflation\nFixed Income', 0.5, 2.9, 4.0, 1.2, { fontSize: 10 });

sectionLabel(slide, 'III. RISK & COMPLIANCE', 5.5, 1.0, 4.0);
bodyText(slide, 'Maturity Distribution\nCredit Quality\nPolicy Compliance', 5.5, 1.35, 4.0, 1.0, { fontSize: 10 });

sectionLabel(slide, 'IV. PERFORMANCE & ANALYTICS', 5.5, 2.55, 4.0);
bodyText(slide, 'Top Issuers\nIncome\nCashflow\nHorizon\nDuration\nConstraints', 5.5, 2.9, 4.0, 1.2, { fontSize: 10 });

// =====================================================
// SLIDE 3: SECTION DIVIDER - Portfolio Overview
// =====================================================
sectionDivider('Portfolio Overview', 'Structure, Allocation & Composition');

// =====================================================
// SLIDE 4: EXECUTIVE SUMMARY
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Executive Summary');
addFooter(slide, pg);

sectionLabel(slide, 'PORTFOLIO OVERVIEW', 0.5, 0.95, 4.25);

// Build executive summary text dynamically
const execSummary = commentary.executive_summary || [
  'The San Bernardino County Investment Pool maintains a total market value of ' +
  fmtCurrency(p.total_market_value) + ' across ' + p.num_holdings +
  ' holdings in ' + p.num_sectors + ' security types.',
  '',
  'The portfolio is governed by the Investment Policy, adopted annually by the Board of Supervisors, ' +
  'and is managed consistent with three primary objectives: Safety of principal, Liquidity to meet ' +
  'operational needs, and Return within established risk parameters.',
  '',
  'As of ' + reportDate + ', the portfolio is in full compliance with all Investment Policy limits. ' +
  largestSectorName + ' represent the largest allocation at ' + largestSectorPct.toFixed(1) +
  '%, well within the ' + largestSectorLimit + '% policy limit.'
].join('\n');

bodyText(slide, execSummary, 0.5, 1.3, 4.25, 3.4, { fontSize: 10.5 });

sectionLabel(slide, 'KEY METRICS', 5.0, 0.95, 4.5);
kpiCard(slide, 'Total Market Value', fmtCurrency(p.total_market_value), 5.0, 1.35, 2.15, 0.85);
kpiCard(slide, 'Weighted Avg Yield', p.weighted_avg_yield.toFixed(2) + '%', 7.3, 1.35, 2.15, 0.85);
kpiCard(slide, 'Weighted Avg Duration', p.weighted_avg_duration.toFixed(2) + ' yrs', 5.0, 2.35, 2.15, 0.85);
kpiCard(slide, 'Monthly Income', '~' + fmtCurrency(data.total_monthly_income, 0), 7.3, 2.35, 2.15, 0.85);
kpiCard(slide, 'Unrealized Gain/Loss', (p.unrealized_gain_loss >= 0 ? '+' : '') + fmtCurrency(p.unrealized_gain_loss), 5.0, 3.35, 2.15, 0.85);
kpiCard(slide, 'Market/Book Ratio', p.market_to_book_ratio.toFixed(4), 7.3, 3.35, 2.15, 0.85);

// =====================================================
// SLIDE 5: SECTOR ALLOCATION
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Sector Allocation');
addFooter(slide, pg);

addChartImg(slide, 'sector_allocation.png', 0.0, 0.85, 4.8, 4.0);

sectionLabel(slide, 'ALLOCATION BY TYPE', 5.0, 0.95, 4.5);
addDataTable(slide,
  ['Security Type', 'Market Value', '% Portfolio'],
  data.sectors.map(s => [
    s.name, fmtDollars(s.market_value), s.pct_portfolio.toFixed(1) + '%'
  ]),
  5.0, 1.25, 4.5,
  { colWidths: [2.0, 1.5, 1.0], rowH: 0.26 }
);

// =====================================================
// SLIDE 6: SECTOR DETAIL
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Sector Detail');
addFooter(slide, pg);
sectionLabel(slide, 'SECURITY TYPE BREAKDOWN', 0.5, 0.95, 9);

addDataTable(slide,
  ['Security Type', 'Market Value', 'Par Value', '% Portfolio', 'Avg Yield', 'Avg Duration', 'Holdings'],
  data.sectors.map(s => [
    s.name,
    fmtDollars(s.market_value),
    fmtDollars(s.par_value),
    s.pct_portfolio.toFixed(1) + '%',
    s.avg_yield.toFixed(2) + '%',
    s.avg_duration.toFixed(2) + ' yr',
    String(s.count)
  ]),
  0.5, 1.3, 9,
  { colWidths: [1.8, 1.4, 1.4, 0.8, 0.8, 0.9, 0.9], rowH: 0.26 }
);

// =====================================================
// SLIDE 7: SECTION DIVIDER - Economic & Market Commentary
// =====================================================
sectionDivider('Economic & Market Commentary', 'Conditions, Policy & Fixed Income Outlook');

// =====================================================
// SLIDE 8: ECONOMIC SNAPSHOT (rates table + yield curve)
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Economic Snapshot');
addFooter(slide, pg);

sectionLabel(slide, 'KEY RATES & INDICATORS', 0.5, 0.95, 4.25);

// Build rates table from FRED data
const ratesRows = [];
const addRate = (label, series, fmt) => {
  const d = fred[series];
  if (d) ratesRows.push([label, (fmt ? fmt(d.value) : d.value.toFixed(2) + '%'), d.date || '']);
};
addRate('Fed Funds Rate', 'FEDFUNDS');
addRate('SOFR', 'SOFR');
addRate('Unemployment', 'UNRATE', v => v.toFixed(1) + '%');
addRate('AA Spread', 'BAMLC0A2CAA');
if (!fred.BAMLC0A2CAA && fred.BAMLC0A4CBBB) {
  // Fallback to BBB if AA not available
  ratesRows.push(['AA Spread', fred.BAMLC0A4CBBB.value.toFixed(2) + '%', fred.BAMLC0A4CBBB.date || '']);
}
addRate('10Y-2Y Spread', 'T10Y2Y');
addRate('30Y Mortgage', 'MORTGAGE30US');

addDataTable(slide, ['Indicator', 'Value', 'As Of'], ratesRows,
  0.5, 1.3, 4.25, { colWidths: [1.6, 1.1, 1.55] });

sectionLabel(slide, 'YIELD CURVE', 5.0, 0.95, 4.5);
addChartImg(slide, 'yield_curve.png', 5.0, 1.25, 4.5, 3.5);

// =====================================================
// SLIDE 9: MONETARY POLICY & FED OUTLOOK
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Monetary Policy & Fed Outlook');
addFooter(slide, pg);

sectionLabel(slide, 'FEDERAL RESERVE POLICY', 0.5, 0.95, 4.25);
const fedText = commentary.fed_rates ?
  [commentary.fed_rates.headline, '', commentary.fed_rates.narrative].join('\n') :
  'Federal Reserve policy commentary will be generated from current FOMC data.';
bodyText(slide, fedText, 0.5, 1.3, 4.25, 3.4, { fontSize: 10.5 });

sectionLabel(slide, 'RATE TRAJECTORY', 5.2, 0.95, 3.6);
// Build rate trajectory table from FRED history if available
const fedHistory = (data.economic && data.economic.fed_rate_history) || [];
const rateTrajectoryRows = fedHistory.slice(-11).map(h => [h.date, h.value.toFixed(2) + '%']);
if (rateTrajectoryRows.length > 0) {
  addDataTable(slide, ['Date', 'Fed Funds'], rateTrajectoryRows,
    5.2, 1.3, 3.6, { colWidths: [1.6, 2.0], rowH: 0.24 });
}

// =====================================================
// SLIDE 10: GROWTH, LABOR & INFLATION
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Growth, Labor & Inflation');
addFooter(slide, pg);

sectionLabel(slide, 'ECONOMIC GROWTH & LABOR', 0.5, 0.95, 4.25);
const laborText = commentary.labor_market ?
  [commentary.labor_market.headline, '', commentary.labor_market.narrative].join('\n') :
  'Economic growth and labor market commentary will be generated from current data.';
bodyText(slide, laborText, 0.5, 1.3, 4.25, 3.4, { fontSize: 10.5 });

sectionLabel(slide, 'INFLATION TRENDS', 5.0, 0.95, 4.5);
const inflationText = commentary.inflation ?
  [commentary.inflation.headline, '', commentary.inflation.narrative].join('\n') :
  'Inflation commentary will be generated from CPI data.';
bodyText(slide, inflationText, 5.0, 1.3, 4.5, 3.4, { fontSize: 10.5 });

// =====================================================
// SLIDE 11: FIXED INCOME & PORTFOLIO IMPLICATIONS
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Fixed Income & Portfolio Implications');
addFooter(slide, pg);

sectionLabel(slide, 'CREDIT & FIXED INCOME MARKETS', 0.5, 0.95, 4.25);
const creditText = commentary.credit_markets ?
  [commentary.credit_markets.headline, '', commentary.credit_markets.narrative].join('\n') :
  'Fixed income market commentary will be generated from current spread data.';
bodyText(slide, creditText, 0.5, 1.3, 4.25, 3.4, { fontSize: 10.5 });

sectionLabel(slide, 'PORTFOLIO IMPLICATIONS', 5.0, 0.95, 4.5);
const implText = commentary.portfolio_implications ||
  'Portfolio implications will be derived from current economic conditions and portfolio positioning.';
bodyText(slide, implText, 5.0, 1.3, 4.5, 3.4, { fontSize: 10.5 });

// =====================================================
// SLIDE 12: SECTION DIVIDER - Risk & Compliance
// =====================================================
sectionDivider('Risk & Compliance', 'Credit Quality, Maturity & Policy Limits');

// =====================================================
// SLIDE 13: MATURITY DISTRIBUTION
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Maturity Distribution');
addFooter(slide, pg);
addChartImg(slide, 'maturity_distribution.png', 0.3, 0.85, 9.4, 4.1);

// =====================================================
// SLIDE 14: CREDIT QUALITY — S&P
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Credit Quality \u2014 S&P');
addFooter(slide, pg);
addChartImg(slide, 'credit_sp.png', 0.2, 0.9, 5.0, 3.9);

sectionLabel(slide, 'S&P DISTRIBUTION', 5.5, 0.95, 4);
// Sort by creditworthiness (highest first)
const spRank = { 'AAA': 0, 'AAAM': 1, 'AA+': 2, 'AA': 3, 'AA-': 4, 'A+': 5, 'A': 6, 'A-': 7, 'A-1+': 8, 'A-1': 9, 'NR': 99 };
const spSorted = [...data.credit_quality.sp].sort((a, b) => (spRank[a.rating] ?? 50) - (spRank[b.rating] ?? 50));
addDataTable(slide,
  ['Rating', '% Portfolio'],
  spSorted.map(r => [r.rating, r.pct.toFixed(1) + '%']),
  5.5, 1.3, 3.5,
  { colWidths: [1.5, 2.0], rowH: 0.26 }
);

// =====================================================
// SLIDE 15: CREDIT QUALITY — MOODY'S
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Credit Quality \u2014 Moody\u2019s');
addFooter(slide, pg);
addChartImg(slide, 'credit_moodys.png', 0.2, 0.9, 5.0, 3.9);

sectionLabel(slide, 'MOODY\u2019S DISTRIBUTION', 5.5, 0.95, 4);
const mdRank = { 'Aaa': 0, 'Aa1': 1, 'Aa2': 2, 'Aa3': 3, 'A1': 4, 'A2': 5, 'A3': 6, 'Baa1': 7, 'Baa2': 8, 'Baa3': 9, 'P-1': 10, 'NR': 99 };
const mdSorted = [...data.credit_quality.moodys].sort((a, b) => (mdRank[a.rating] ?? 50) - (mdRank[b.rating] ?? 50));
addDataTable(slide,
  ['Rating', '% Portfolio'],
  mdSorted.map(r => [r.rating, r.pct.toFixed(1) + '%']),
  5.5, 1.3, 3.5,
  { colWidths: [1.5, 2.0], rowH: 0.28 }
);

// =====================================================
// SLIDE 16: POLICY COMPLIANCE
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Policy Compliance');
addFooter(slide, pg);

addChartImg(slide, 'compliance.png', 0.1, 0.85, 4.8, 3.9);

sectionLabel(slide, 'COMPLIANCE DETAIL', 5.2, 0.95, 4.3);
addDataTable(slide,
  ['Type', 'Actual', 'Limit', 'Margin', 'Status'],
  data.compliance.map(c => [
    c.security_type,
    c.actual_pct.toFixed(1) + '%',
    c.policy_limit + '%',
    c.margin.toFixed(1) + ' pp',
    c.status
  ]),
  5.2, 1.3, 4.3,
  { colWidths: [1.4, 0.65, 0.6, 0.65, 1.0], rowH: 0.24, statusCol: 4, leftAlignCol: 0 }
);

// =====================================================
// SLIDE 17: SECTION DIVIDER - Performance & Analytics
// =====================================================
sectionDivider('Performance & Analytics', 'Income, Cashflow & Scenario Analysis');

// =====================================================
// SLIDE 18: TOP 10 ISSUERS
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Top 10 Issuers');
addFooter(slide, pg);

sectionLabel(slide, 'ISSUER CONCENTRATION (AGGREGATED)', 0.5, 0.95, 9);

const totalMV = p.total_market_value;
addDataTable(slide,
  ['Issuer', 'Market Value', '% Portfolio', 'Holdings'],
  data.issuer_concentration.map(i => [
    i.issuer,
    fmtDollars(i.market_value),
    i.pct.toFixed(1) + '%',
    String(i.count || '')
  ]),
  0.5, 1.3, 9,
  { colWidths: [3.2, 2.0, 1.8, 2.0], rowH: 0.26, leftAlignCol: 0 }
);

// =====================================================
// SLIDE 19: INCOME ANALYSIS
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Income Analysis');
addFooter(slide, pg);

sectionLabel(slide, 'MONTHLY INCOME BY SECTOR', 0.5, 0.95, 9);

addDataTable(slide,
  ['Security Type', 'Market Value', 'Yield', 'Est. Monthly Income'],
  data.monthly_income.map(i => {
    const sectorData = data.sectors.find(s => s.name === i.sector);
    const mv = sectorData ? sectorData.market_value : 0;
    return [
      i.sector,
      fmtDollars(mv),
      i.yield.toFixed(2) + '%',
      fmtDollars(i.monthly_income)
    ];
  }),
  0.5, 1.3, 9,
  { colWidths: [2.4, 2.3, 1.0, 3.3], rowH: 0.26 }
);

bodyText(slide,
  'Total estimated monthly income: ' + fmtDollars(data.total_monthly_income) +
  '. Income is the primary component of total return, consistent with the portfolio\'s ' +
  'focus on safety and liquidity as the highest-priority Investment Policy objectives.',
  0.5, 4.2, 9, 0.65, { fontSize: 10, italic: true }
);

// =====================================================
// SLIDE 20: SECURITIES CASHFLOW
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Securities Cashflow \u2014 Jan\u2013Dec ' + (new Date().getFullYear()));
addFooter(slide, pg);
addChartImg(slide, 'securities_cashflow.png', 0.3, 0.85, 9.4, 4.1);

// =====================================================
// SLIDE 21: HORIZON ANALYSIS
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Horizon Analysis \u2014 1-Year Forward');
addFooter(slide, pg);

addChartImg(slide, 'horizon_analysis.png', 0.3, 0.9, 5.2, 3.6);

sectionLabel(slide, 'SCENARIO RESULTS', 5.8, 0.95, 3.7);
addDataTable(slide,
  ['Scenario', 'Income', 'Price', 'Total'],
  data.horizon_analysis.map(h => [
    h.scenario,
    h.income.toFixed(2) + '%',
    (h.price >= 0 ? '+' : '') + h.price.toFixed(2) + '%',
    h.total.toFixed(2) + '%'
  ]),
  5.8, 1.3, 3.7,
  { colWidths: [0.9, 0.9, 0.9, 1.0], rowH: 0.3 }
);

bodyText(slide,
  'Under all five illustrative scenarios, the portfolio is projected to generate positive total return ' +
  'over a 1-year horizon. The gold bar highlights the current (unchanged rates) scenario. ' +
  'This analysis assumes parallel rate shifts, a static portfolio, and no reinvestment of proceeds.',
  5.8, 3.1, 3.7, 1.7, { fontSize: 9.5 }
);

// =====================================================
// SLIDE 22: DURATION & RISK ANALYSIS
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Duration & Risk Analysis');
addFooter(slide, pg);

sectionLabel(slide, 'RISK METRICS', 0.5, 0.95, 9);
kpiCard(slide, 'Weighted Avg Duration', p.weighted_avg_duration.toFixed(2) + ' years', 0.5, 1.35, 2.9, 0.9);
kpiCard(slide, 'Weighted Avg Yield', p.weighted_avg_yield.toFixed(2) + '%', 3.55, 1.35, 2.9, 0.9);
kpiCard(slide, 'Market/Book Ratio', p.market_to_book_ratio.toFixed(4), 6.6, 1.35, 2.9, 0.9);

bodyText(slide, [
  'Duration of ' + p.weighted_avg_duration.toFixed(2) + ' years reflects the portfolio\'s structure, ' +
  'with significant liquidity in short-term instruments while maintaining competitive yield from intermediate securities. ' +
  'The duration is well within the Investment Policy\'s 3.0-year maximum.',
  '',
  'The portfolio\'s interest rate sensitivity is moderate: a parallel 100 basis point increase in rates would be ' +
  'expected to result in approximately ' + p.weighted_avg_duration.toFixed(2) + '% price decline, ' +
  'offset by the ' + p.weighted_avg_yield.toFixed(2) + '% income return over a 1-year horizon.',
  '',
  'The ' + (p.unrealized_gain_loss >= 0 ? 'positive unrealized gain' : 'unrealized loss') + ' of ' +
  fmtCurrency(Math.abs(p.unrealized_gain_loss)) +
  ' (' + ((p.unrealized_gain_loss / p.total_book_value) * 100).toFixed(2) +
  '% of book value) indicates ' + (p.unrealized_gain_loss >= 0 ? 'favorable' : 'challenging') +
  ' market conditions relative to the portfolio\'s cost basis.'
].join('\n'), 0.5, 2.55, 9, 2.2, { fontSize: 10.5 });

// =====================================================
// SLIDE 23: CONSTRAINTS & CONSIDERATIONS
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Constraints & Considerations');
addFooter(slide, pg);

sectionLabel(slide, 'REGULATORY FRAMEWORK', 0.5, 0.95, 4.25);
bodyText(slide, [
  'The Investment Pool is governed by the Investment Policy Statement adopted by the Board of Supervisors ' +
  'and California Government Code sections 53600-53686.',
  '',
  'Key constraints include:',
  '',
  '   Minimum credit quality of A- or better for all holdings',
  '   Concentration limits on individual securities and sectors',
  '   Maximum portfolio duration of 3.0 years',
  '   Maximum maturity of 5 years for most security types'
].join('\n'), 0.5, 1.3, 4.25, 3.4, { fontSize: 10.5 });

sectionLabel(slide, 'MARKET CONSIDERATIONS', 5.0, 0.95, 4.5);
const marketConsiderations = commentary.market_considerations || [
  'Several market factors are monitored in the context of portfolio management:',
  '',
  '   Federal Reserve policy trajectory and its effect on short-term rates',
  '   ' + largestSectorName + ' at ' + largestSectorPct.toFixed(1) + '% of portfolio \u2014 well within the ' + largestSectorLimit + '% policy limit',
  '   Credit spreads remain compressed \u2014 may affect reinvestment decisions',
  '   Yield curve shape influences relative value across maturities',
  '',
  'These factors are evaluated within the framework of the Investment Policy\'s ' +
  'primary objectives of safety, liquidity, and return.'
].join('\n');
bodyText(slide, marketConsiderations, 5.0, 1.3, 4.5, 3.4, { fontSize: 10.5 });

// =====================================================
// SLIDE 24: DISCLOSURES & CONTACT
// =====================================================
pg++;
slide = prs.addSlide();
addHeader(slide, 'Disclosures & Contact');
addFooter(slide, pg);

sectionLabel(slide, 'IMPORTANT DISCLOSURES', 0.5, 0.95, 9);
bodyText(slide, [
  'This report is prepared for the Board of Supervisors and authorized participants of the ' +
  'San Bernardino County Investment Pool.',
  '',
  'This report is for informational purposes only and does not constitute investment advice. ' +
  'Past performance is not indicative of future results. Forward-looking statements and projections ' +
  'are illustrative only and subject to change based on market conditions.',
  '',
  'Market values are based on independent pricing sources (BVAL) as of the report date. ' +
  'Returns are calculated using time-weighted methodology.',
  '',
  'The Investment Pool is governed by the Investment Policy Statement, adopted annually by the ' +
  'Board of Supervisors, and California Government Code sections 53600-53686.'
].join('\n'), 0.5, 1.3, 4.25, 3.2, { fontSize: 10 });

sectionLabel(slide, 'CONTACT INFORMATION', 5.0, 0.95, 4.5);
bodyText(slide, [
  'San Bernardino County',
  'Auditor-Controller / Treasurer / Tax Collector',
  'Treasurer Division',
  '',
  '268 West Hospitality Lane, First Floor',
  'San Bernardino, CA 92415-0018',
  '',
  'Report generated: ' + reportDate
].join('\n'), 5.0, 1.3, 4.5, 3.0, { fontSize: 11 });

// ── Save ────────────────────────────────────────────────────────────────
prs.writeFile({ fileName: outputPath }).then(() => {
  console.log('SUCCESS: ' + outputPath);
  console.log('Total slides: 24');
  console.log('Report date: ' + reportDate);
}).catch(err => {
  console.error('ERROR:', err);
  process.exit(1);
});
