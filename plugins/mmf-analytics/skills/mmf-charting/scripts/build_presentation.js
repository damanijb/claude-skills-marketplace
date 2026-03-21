#!/usr/bin/env node
/**
 * build_presentation.js — Build MMF monthly meeting presentation using pptxgenjs.
 *
 * Usage:
 *   node build_presentation.js --charts-dir /tmp/mmf_charts --metrics /tmp/mmf_charts/metrics.json --out /path/to/output.pptx
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ── CLI Args ─────────────────────────────────────────────────────────────────

const args = {};
process.argv.slice(2).forEach((a, i, arr) => {
  if (a.startsWith("--")) args[a.slice(2)] = arr[i + 1];
});

const CHARTS_DIR   = args["charts-dir"] || "/tmp/mmf_charts";
const METRICS_FILE = args["metrics"]    || path.join(CHARTS_DIR, "metrics.json");
const OUT_FILE     = args["out"]        || path.join(CHARTS_DIR, "MMF_Investment_Review.pptx");

// ── Colors & Fonts ───────────────────────────────────────────────────────────

const C = {
  navy:     "1E2761",
  iceBlue:  "CADCFC",
  white:    "FFFFFF",
  lightBg:  "F8FAFC",
  darkText: "1E293B",
  muted:    "64748B",
  green:    "16A34A",
  red:      "DC2626",
  amber:    "D97706",
  // Fund colors (no #)
  FRGXX:    "1f77b4",
  GOFXX:    "ff7f0e",
  MVRXX:    "2ca02c",
  BGSXX:    "d62728",
};

const FUND_LABELS = {
  FRGXX: "Fidelity Gov Portfolio",
  GOFXX: "Goldman Sachs Gov Obligations",
  MVRXX: "Morgan Stanley Gov Portfolio",
  BGSXX: "Northern Institutional US Gov Select",
};

const TICKERS = ["FRGXX", "GOFXX", "MVRXX", "BGSXX"];
const FONT_TITLE = "Calibri";
const FONT_BODY  = "Calibri";

// ── Helpers ───────────────────────────────────────────────────────────────────

function imgPath(filename) {
  return path.join(CHARTS_DIR, filename);
}

function hasImg(filename) {
  return fs.existsSync(imgPath(filename));
}

// Add a chart image to a slide with graceful fallback
function addChartImg(slide, filename, x, y, w, h, label) {
  const fp = imgPath(filename);
  if (fs.existsSync(fp)) {
    slide.addImage({ path: fp, x, y, w, h, sizing: { type: "contain", w, h } });
  } else {
    // Placeholder box
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h,
      fill: { color: "E2E8F0" },
      line: { color: "CBD5E1", width: 1 }
    });
    slide.addText(label || filename, {
      x, y, w, h,
      align: "center", valign: "middle",
      fontSize: 10, color: C.muted, fontFace: FONT_BODY
    });
  }
}

// Dark section-break slide
function addSectionSlide(pres, title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: C.navy };

  // Decorative accent bar on left
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.22, h: 7.5,
    fill: { color: C.iceBlue }
  });

  slide.addText(title, {
    x: 0.55, y: 2.8, w: 12, h: 1.2,
    fontFace: FONT_TITLE, fontSize: 42, bold: true,
    color: C.white, valign: "middle"
  });

  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.55, y: 4.0, w: 10, h: 0.7,
      fontFace: FONT_BODY, fontSize: 18,
      color: C.iceBlue, valign: "top"
    });
  }
  return slide;
}

// Stat callout box (for per-fund slides)
function addStatBox(slide, x, y, w, h, label, value, color) {
  const makeShadow = () => ({
    type: "outer", blur: 5, offset: 2, angle: 135,
    color: "000000", opacity: 0.10
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.white },
    line: { color: "E2E8F0", width: 1 },
    shadow: makeShadow()
  });

  // Colored top accent
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h: 0.055,
    fill: { color: color || C.navy }
  });

  slide.addText(value, {
    x, y: y + 0.12, w, h: h * 0.55,
    fontFace: FONT_TITLE, fontSize: 20, bold: true,
    color: C.darkText, align: "center", valign: "middle", margin: 0
  });
  slide.addText(label, {
    x, y: y + h * 0.6, w, h: h * 0.35,
    fontFace: FONT_BODY, fontSize: 9,
    color: C.muted, align: "center", valign: "top", margin: 0
  });
}

// ── Load Metrics ─────────────────────────────────────────────────────────────

let metrics = {};
try {
  metrics = JSON.parse(fs.readFileSync(METRICS_FILE, "utf8"));
  console.log(`Loaded metrics for ${Object.keys(metrics.funds || {}).length} funds`);
} catch (e) {
  console.warn(`Warning: Could not load metrics from ${METRICS_FILE}: ${e.message}`);
  metrics = {
    report_date: "Latest Month", report_month: "", report_year: "",
    funds: {}, cross_fund: { total_aum_B: 0 }
  };
}

const REPORT_DATE    = metrics.report_date    || "Latest Month";
const TOTAL_AUM      = metrics.cross_fund?.total_aum_B || 0;
const FUNDS_METRICS  = metrics.funds || {};

// ── Build Presentation ────────────────────────────────────────────────────────

const pres = new pptxgen();
pres.layout  = "LAYOUT_WIDE";   // 13.3" × 7.5"
pres.author  = "SBC Treasury Analytics";
pres.title   = `MMF Investment Review — ${REPORT_DATE}`;
pres.subject = "Money Market Fund Monthly Review";

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 1 — Title
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.navy };

  // Left accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.3, h: 7.5,
    fill: { color: C.iceBlue }
  });

  // Org / dept header
  slide.addText("SAN BERNARDINO COUNTY TREASURY", {
    x: 0.55, y: 1.2, w: 12, h: 0.5,
    fontFace: FONT_BODY, fontSize: 13, bold: false,
    color: C.iceBlue, charSpacing: 4
  });

  // Main title
  slide.addText("Money Market Fund\nInvestment Review", {
    x: 0.55, y: 1.85, w: 11, h: 2.3,
    fontFace: FONT_TITLE, fontSize: 48, bold: true,
    color: C.white
  });

  // Reporting period
  slide.addText(REPORT_DATE, {
    x: 0.55, y: 4.25, w: 9, h: 0.8,
    fontFace: FONT_BODY, fontSize: 24, bold: false,
    color: C.iceBlue
  });

  // Fund tickers strip
  const tickerY = 5.6;
  TICKERS.forEach((t, i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.55 + i * 3.0, y: tickerY, w: 2.7, h: 0.6,
      fill: { color: C[t] || C.navy },
      line: { color: "FFFFFF", width: 0 }
    });
    slide.addText(`${t}\n${FUND_LABELS[t] || ""}`, {
      x: 0.55 + i * 3.0, y: tickerY, w: 2.7, h: 0.6,
      fontFace: FONT_BODY, fontSize: 8, bold: true,
      color: C.white, align: "center", valign: "middle"
    });
  });

  // Combined AUM callout
  if (TOTAL_AUM > 0) {
    slide.addText(`Combined AUM: $${TOTAL_AUM.toFixed(1)}B`, {
      x: 0.55, y: 6.5, w: 7, h: 0.5,
      fontFace: FONT_BODY, fontSize: 14, bold: false,
      color: "A0AEC0"
    });
  }

  // Source
  slide.addText("Source: SEC EDGAR N-MFP2 Filings", {
    x: 0.55, y: 7.1, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 9, italic: true,
    color: "5A6A8A"
  });
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 2 — Agenda
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 1.1,
    fill: { color: C.navy }
  });
  slide.addText("Meeting Agenda", {
    x: 0.5, y: 0, w: 12, h: 1.1,
    fontFace: FONT_TITLE, fontSize: 30, bold: true,
    color: C.white, valign: "middle"
  });

  const items = [
    ["01", "Executive Summary",    "Cross-fund heatmap — AUM, liquidity, risk at a glance"],
    ["02", "Cross-Fund Trends",    "AUM flows, WAM/WAL evolution, cash positioning"],
    ["03", "Fund Deep Dives",      "Composition & maturity profile for each fund"],
    ["04", "Issuer Concentration", "Top issuers by % of NAV, HHI concentration"],
  ];

  items.forEach(([num, title, desc], i) => {
    const itemX = 0.5;
    const itemY = 1.5 + i * 1.35;

    // Number circle
    slide.addShape(pres.shapes.OVAL, {
      x: itemX, y: itemY + 0.05, w: 0.7, h: 0.7,
      fill: { color: C.navy }
    });
    slide.addText(num, {
      x: itemX, y: itemY + 0.05, w: 0.7, h: 0.7,
      fontFace: FONT_TITLE, fontSize: 18, bold: true,
      color: C.white, align: "center", valign: "middle"
    });

    // Title
    slide.addText(title, {
      x: itemX + 0.9, y: itemY, w: 11, h: 0.45,
      fontFace: FONT_TITLE, fontSize: 18, bold: true,
      color: C.darkText, valign: "bottom"
    });
    // Description
    slide.addText(desc, {
      x: itemX + 0.9, y: itemY + 0.45, w: 11, h: 0.45,
      fontFace: FONT_BODY, fontSize: 13,
      color: C.muted, valign: "top"
    });
    // Separator line (except last)
    if (i < items.length - 1) {
      slide.addShape(pres.shapes.LINE, {
        x: itemX + 0.9, y: itemY + 1.2, w: 11.4, h: 0,
        line: { color: "E2E8F0", width: 0.75 }
      });
    }
  });
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 3 — Section Break: Executive Summary
// ════════════════════════════════════════════════════════════════════════════
addSectionSlide(pres, "Executive Summary", `${REPORT_DATE} — Fund Snapshot`);

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 4 — Heatmap
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 0.85,
    fill: { color: C.navy }
  });
  slide.addText("Fund Comparison Heatmap", {
    x: 0.4, y: 0, w: 11, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 24, bold: true,
    color: C.white, valign: "middle"
  });
  slide.addText(REPORT_DATE, {
    x: 10, y: 0, w: 3, h: 0.85,
    fontFace: FONT_BODY, fontSize: 14,
    color: C.iceBlue, align: "right", valign: "middle"
  });

  addChartImg(slide, "heatmap_comparison.png", 0.5, 1.0, 12.3, 6.1, "Heatmap Comparison");
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 5 — Section Break: Cross-Fund Overview
// ════════════════════════════════════════════════════════════════════════════
addSectionSlide(pres, "Cross-Fund Overview", "12-Month Trend Analysis");

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 6 — AUM & Cash Trends
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 0.85,
    fill: { color: C.navy }
  });
  slide.addText("AUM & Cash Positioning", {
    x: 0.4, y: 0, w: 12, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 24, bold: true,
    color: C.white, valign: "middle"
  });

  // Two charts side by side
  addChartImg(slide, "cross_fund_aum_B.png",    0.2, 1.0, 6.3, 5.6, "AUM Over Time");
  addChartImg(slide, "cross_fund_cash_pct.png", 6.8, 1.0, 6.3, 5.6, "Cash % of NAV");
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 7 — WAM & WAL Risk Metrics
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 0.85,
    fill: { color: C.navy }
  });
  slide.addText("Weighted Average Maturity & Life", {
    x: 0.4, y: 0, w: 12, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 24, bold: true,
    color: C.white, valign: "middle"
  });

  addChartImg(slide, "cross_fund_avg_portfolio_maturity.png", 0.2, 1.0, 6.3, 5.6, "WAM Over Time");
  addChartImg(slide, "cross_fund_avg_life_maturity.png",      6.8, 1.0, 6.3, 5.6, "WAL Over Time");
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 8 — Prior vs Current Month Summary
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 0.85,
    fill: { color: C.navy }
  });
  slide.addText("Month-over-Month Snapshot", {
    x: 0.4, y: 0, w: 12, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 24, bold: true,
    color: C.white, valign: "middle"
  });

  addChartImg(slide, "summary_all_metrics.png", 0.3, 1.0, 12.7, 6.1, "Summary — All Metrics");
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 9 — Section Break: Fund Deep Dives
// ════════════════════════════════════════════════════════════════════════════
addSectionSlide(pres, "Fund Deep Dives", "Portfolio Composition & Maturity by Fund");

// ════════════════════════════════════════════════════════════════════════════
// SLIDES 10–13 — Per Fund (one slide each)
// ════════════════════════════════════════════════════════════════════════════
TICKERS.forEach((ticker) => {
  const fm      = FUNDS_METRICS[ticker] || {};
  const label   = FUND_LABELS[ticker]   || ticker;
  const color   = C[ticker]             || C.navy;

  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  // ── Header bar ────────────────────────────────────────────────────────────
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 1.0,
    fill: { color: color }
  });
  slide.addText(ticker, {
    x: 0.35, y: 0, w: 2.5, h: 1.0,
    fontFace: FONT_TITLE, fontSize: 32, bold: true,
    color: C.white, valign: "middle"
  });
  slide.addText(label, {
    x: 2.9, y: 0, w: 9, h: 1.0,
    fontFace: FONT_BODY, fontSize: 16, bold: false,
    color: C.white, valign: "middle"
  });
  if (fm.report_date) {
    slide.addText(fm.report_date, {
      x: 10, y: 0, w: 3, h: 1.0,
      fontFace: FONT_BODY, fontSize: 12,
      color: "8899BB", align: "right", valign: "middle"
    });
  }

  // ── Stat callouts (row of 5) ──────────────────────────────────────────────
  const stats = [
    ["AUM",       fm.aum_B       != null ? `$${fm.aum_B.toFixed(1)}B`   : "—"],
    ["WAM",       fm.wam         != null ? `${fm.wam.toFixed(0)}d`       : "—"],
    ["WAL",       fm.wal         != null ? `${fm.wal.toFixed(0)}d`       : "—"],
    ["7-Day Yield",fm.yield_7d_pct!= null ? `${fm.yield_7d_pct.toFixed(2)}%` : "—"],
    ["Daily Liq", fm.daily_liq   != null ? `${fm.daily_liq.toFixed(1)}%` : "—"],
  ];

  const boxW = 2.35, boxH = 1.05, boxY = 1.12, gap = 0.15;
  stats.forEach(([lbl, val], i) => {
    addStatBox(slide, 0.25 + i * (boxW + gap), boxY, boxW, boxH, lbl, val, color);
  });

  // ── Charts (side by side) ─────────────────────────────────────────────────
  addChartImg(slide, `${ticker}_composition.png`,
    0.25, 2.32, 6.1, 4.85, `${ticker} Composition`);
  addChartImg(slide, `${ticker}_maturity_buckets.png`,
    6.6,  2.32, 6.4, 4.85, `${ticker} Maturity Buckets`);
});

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 14 — Section Break: Issuer Concentration
// ════════════════════════════════════════════════════════════════════════════
addSectionSlide(pres, "Issuer Concentration", "Top Issuers by % of NAV Across All Funds");

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 15 — Top Issuers (2×2 grid, one per fund)
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.lightBg };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 0.85,
    fill: { color: C.navy }
  });
  slide.addText("Top 10 Issuers by % of NAV", {
    x: 0.4, y: 0, w: 11, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 24, bold: true,
    color: C.white, valign: "middle"
  });

  // 2×2 grid
  const positions = [
    [0.15, 1.0], [6.7, 1.0],
    [0.15, 4.2], [6.7, 4.2],
  ];
  TICKERS.forEach((ticker, i) => {
    const [gx, gy] = positions[i];
    const icolor   = C[ticker] || C.navy;

    // Mini label
    slide.addShape(pres.shapes.RECTANGLE, {
      x: gx, y: gy, w: 6.3, h: 0.28,
      fill: { color: icolor }
    });
    slide.addText(ticker, {
      x: gx, y: gy, w: 6.3, h: 0.28,
      fontFace: FONT_BODY, fontSize: 9, bold: true,
      color: C.white, align: "center", valign: "middle"
    });
    addChartImg(slide, `${ticker}_top_issuers.png`,
      gx, gy + 0.28, 6.3, 2.9, `${ticker} Top Issuers`);
  });
}

// ════════════════════════════════════════════════════════════════════════════
// SLIDE 16 — Data Note / Footer
// ════════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: C.navy };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.22, h: 7.5,
    fill: { color: C.iceBlue }
  });

  slide.addText("Data & Methodology Notes", {
    x: 0.55, y: 1.2, w: 12, h: 0.7,
    fontFace: FONT_TITLE, fontSize: 28, bold: true,
    color: C.white
  });

  const noteItems = [
    ["Data Source",   "SEC EDGAR N-MFP2 / N-MFP3 monthly filings. Filed within 5 business days of month-end."],
    ["Funds Covered", "FRGXX (Fidelity), GOFXX (Goldman Sachs), MVRXX (Morgan Stanley), BGSXX (Northern Institutional)."],
    ["Liquidity",     "Daily liquid ≥ 10% of NAV required; weekly liquid ≥ 30% required under SEC Rule 2a-7."],
    ["HHI",           "Herfindahl-Hirschman Index: Σ(issuer % NAV)². < 1,500 = competitive; > 2,500 = concentrated."],
    ["WAM / WAL",     "Weighted Average Maturity (reset features) and Weighted Average Life (final maturity) in days."],
  ];

  noteItems.forEach(([label, text], i) => {
    slide.addText(label + ":", {
      x: 0.55, y: 2.15 + i * 0.88, w: 2.6, h: 0.4,
      fontFace: FONT_BODY, fontSize: 12, bold: true,
      color: C.iceBlue, valign: "top"
    });
    slide.addText(text, {
      x: 3.2, y: 2.15 + i * 0.88, w: 9.8, h: 0.55,
      fontFace: FONT_BODY, fontSize: 11, bold: false,
      color: C.white, valign: "top"
    });
    if (i < noteItems.length - 1) {
      slide.addShape(pres.shapes.LINE, {
        x: 0.55, y: 2.88 + i * 0.88, w: 12.3, h: 0,
        line: { color: "3A4B80", width: 0.5 }
      });
    }
  });

  // Footer
  slide.addText(`Generated by SBC Treasury Analytics  ·  ${REPORT_DATE}  ·  Powered by SEC EDGAR data`, {
    x: 0.55, y: 7.0, w: 12.3, h: 0.35,
    fontFace: FONT_BODY, fontSize: 9, italic: true,
    color: "5A6A8A", align: "center"
  });
}

// ════════════════════════════════════════════════════════════════════════════
// Write output
// ════════════════════════════════════════════════════════════════════════════
pres.writeFile({ fileName: OUT_FILE })
  .then(() => {
    console.log(`\n✓ Presentation written to: ${OUT_FILE}`);
    console.log(`  Slides: 16`);
  })
  .catch((err) => {
    console.error("Error writing PPTX:", err);
    process.exit(1);
  });
