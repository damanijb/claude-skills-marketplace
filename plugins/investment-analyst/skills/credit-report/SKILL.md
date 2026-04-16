---
name: credit-report
description: >
  Generate a CreditSights-style quarterly credit analysis report for any SBC Treasury covered
  issuer. This skill should be used when the user invokes /credit-report, says "generate a
  credit report", "write a credit analysis for [issuer]", "make a CreditSights-style report",
  "produce a bond credit report", or "run the credit report for [issuer] [quarter]". Produces
  a self-contained HTML report with recommendation badge, earnings snapshot table, capital
  waterfall, segment charts, sector economics panel, SBC/PFM portfolio exposure with tenor
  compliance, and current Bloomberg ratings. A companion DOCX is also saved to the workspace.
version: 1.0.0
---

# Credit Report Skill

Automates CreditSights-style quarterly credit analysis for SBC Treasury covered issuers.
Output is a standalone HTML report with embedded Chart.js charts, live Bloomberg ratings,
FRED macro indicators, SBC portfolio exposure, and SBC/PFM tenor limit compliance checks.

## Invocation

```
/credit-report [issuer] [quarter]
```

**Examples:**
- `/credit-report JPM 1Q26`
- `/credit-report Citigroup 1Q26`
- `/credit-report "Bank of America" 1Q26`
- `/credit-report "BNP Paribas" 1Q26`

If no arguments are provided, use AskUserQuestion to ask which issuer and quarter.

---

## Key Output Paths

| Deliverable | Path |
|---|---|
| HTML report | `{workspace}/Credit Analysis/{Issuer} {Quarter} Credit Report.html` |
| DOCX companion | `{workspace}/Credit Analysis/{Issuer} {Quarter}.docx` |

---

## Step 1 — Load Source Data

Check for available earnings data in priority order:

1. **Press release PDF** — scan `T:\Data\Shared\Credit analysis\Quarterly Tearsheets\{YEAR}\{QQ}{YY}\` and the session workspace `US Banks/` folder
2. **Earnings DOCX write-up** — check for `{Issuer} {QQ}{YY}.docx` in the Credit Analysis workspace
3. **Outlook email** — use the outlook-email skill to pull from Sent Items or Inbox
4. **Obsidian vault** — use the obsidian-memory skill for the issuer's tearsheet note

Extract text via pypdf (PDF) or python-docx (DOCX).

---

## Step 2 — Pull Bloomberg Ratings (Live)

Pull current agency ratings via BQL. Run both queries:

```
-- S&P and Fitch via equity ticker
get(rating(source=SP).value, rating(source=FITCH).value)
for(['{TICKER} US Equity'])

-- Moody's via a Corp bond ticker (equity ticker returns N.A. for Moody's)
get(rating(source=MOODY).value)
for(['{ISSUER_CORP_BOND_TICKER}'])
```

See `references/sbc-policy.md` for the canonical Corp bond tickers by issuer.
If a specific bond has matured, search Bloomberg for an active benchmark bond: `[TICKER] [COUPON] [MATURITY] Corp`.

Store: S&P rating, Moody's rating, Fitch rating, and any outlook/watch flags.

---

## Step 3 — Pull Sector Economics (FRED)

Pull the following FRED series via `mcp__sbcounty-treasurer__fred_get_series`.
Use `observation_start` = 3 months ago, or last available observation for each:

**Banking sector core macro (always pull for bank issuers):**
- `SOFR` — Secured Overnight Financing Rate
- `DGS2` — 2-Year Treasury Yield
- `DGS10` — 10-Year Treasury Yield
- `FEDFUNDS` — Effective Federal Funds Rate
- `UNRATE` — Unemployment Rate
- `CPIAUCSL` — CPI (calculate YoY % change from 12 months prior)

**Additional for corporate sector issuers:**
- `BAMLC0A0CM` — IG Corporate OAS (bps)
- `BAMLH0A0HYM2` — HY Corporate OAS (bps)
- `DCOILWTICO` — WTI Oil Price (for energy issuers)

See `references/sbc-policy.md` for the full FRED series reference table by sector.

Calculate derived indicators:
- **2s10s spread** = DGS10 − DGS2 (key for bank NIM outlook)
- **CPI YoY** = (latest CPIAUCSL / CPIAUCSL 12 months prior − 1) × 100
- **Real rate** = DGS2 − CPI YoY (or DGS10 − CPI YoY for 10Y real rate)

---

## Step 4 — Pull SBC Portfolio Exposure

Query the live portfolio database for current SBC holdings in this issuer:

```sql
SELECT
    issuer, security_type, sector, description,
    maturity_date, duration, par_value, yield,
    fitch_rating, sp_rating
FROM portfolio.latest_pfm
WHERE issuer IN ('{BUCKET_1}', '{BUCKET_2}')
ORDER BY maturity_date
```

See `references/sbc-policy.md` for the issuer bucket code mapping (e.g., BAC → 'BAC', 'BOFA', 'BOFASEC').

After pulling, apply tenor compliance check:
- **SBC Pool**: flag positions where `maturity_date > TODAY + 1825 days` (5Y limit for Corp Notes/BN)
- **PFM Pool**: flag positions where `maturity_date > TODAY + 730 days` (2Y limit for Corp Notes/BN)
- Adjust the limit by security type (CP = 270 days, CD = 1825 days, etc.)

See `references/sbc-policy.md` for the full tenor limits table by security type and pool.

---

## Step 5 — Extract Key Financial Data Points

Extract from the earnings source loaded in Step 1. Missing figures = "N/A" — never fabricate.

**Overall:** Managed revenue, NII, NIR, Expenses (overhead ratio), NCOs, provision,
reserve build/release, Net income, EPS, ROTCE, ROE

**Capital:** CET1 (std + advanced), SLR, LCR, RWA, TBVPS, capital returned, payout ratio,
QoQ CET1 change drivers (earnings, dividends, buybacks, RWA, AOCI)

**Per segment:** Revenue (QoQ + YoY), NI, overhead ratio, key drivers, ROE/ROTCE where disclosed

**Asset quality:** Non-accruals ($B, QoQ %), NCO rate (bps), NPL ratio, reserve/loan ratio

---

## Step 6 — Apply Recommendation Logic

| Signal | Outperform | Underperform |
|--------|-----------|--------------|
| CET1 buffer vs. regulatory minimum | > 300 bps | < 150 bps |
| ROTCE trajectory (last 3Q trend) | Rising, ≥ peer median | Declining, < peer median |
| Non-accrual trend | Stable or declining | Rising > 20% YoY, no sector attribution |
| Payout ratio tension | < 100%, stable CET1 | > 120%, compressing CET1 |
| Operating leverage | Revenue growth ≥ expense growth | Expense growth > revenue growth |

Default to **Market Perform** unless 3+ signals are clearly directional.
Full recommendation language templates are in `references/report-format.md`.

---

## Step 7 — Generate HTML Report

Build via Python Bash script using the section structure below. Use Chart.js 4.4.1 CDN.
**Always write HTML using `cat > 'filepath' << 'HTMLEOF' ... HTMLEOF`** to avoid security hook blocks.

Key rules:
- All charts must use actual extracted data, never placeholders
- Positive color: `#2a7d6b` | Negative: `#c43030` | Neutral: `#888`
- Recommendation badge: Outperform = `#2a7d6b`, Market Perform = `#f0a500`, Underperform = `#c43030`

---

## Report Structure (Full Sections)

```
1.  Header band (navy, issuer, quarter, recommendation badge, ratings row)
2.  Executive summary (4–6 bullets | relative value box)
3.  KPI strip (6 metrics)
4.  Earnings snapshot table (5-quarter trend)
5.  Charts row 1: Operating leverage bars + CET1 trend line
6.  Capital position narrative + CET1 waterfall table
7.  Segment charts: Revenue 1Q vs. PY + Segment NI with ROE labels
8.  Segment narrative cards (2×2 grid)
9.  ── NEW: Bloomberg Ratings Panel ──────────────────────
10. ── NEW: Sector Economics Panel (FRED data) ────────────
11. ── NEW: SBC Portfolio Exposure + Tenor Compliance ──────
12. Key Monitoring Flags table
13. Peer comparison table
```

See `references/report-format.md` for full section specs, chart configs, and CSS.

---

## Step 8 — Generate DOCX Companion

python-docx with Calibri font, navy headings (`#1F3864`), horizontal rule dividers.
Follow the `report-writer` skill standards. Include all narrative sections; omit charts.

---

## Completion Output

After generating, display:

```
✅ Credit Report Complete: {Issuer} {Quarter}

  Recommendation:  [Outperform / Market Perform / Underperform]
  Ratings:         S&P [X] | Moody's [X] | Fitch [X]
  SBC Exposure:    $[X]M across [N] positions (max maturity: [date])
  SOFR:            [X]% | 2Y: [X]% | 10Y: [X]% | 2s10s: [±X]bps

  HTML report:     [link]
  DOCX companion:  [link]

  Key monitoring flags:
    1. [Flag] — [one-line summary]
    2. [Flag] — [one-line summary]
    3. [Flag] — [one-line summary]
```

---

## Reference Files

- `references/report-format.md` — Full CreditSights format spec, chart configs, section CSS,
  monitoring flag taxonomy, peer comparison table columns, recommendation language templates
- `references/sbc-policy.md` — SBC/PFM tenor limits by security type, AIL approved instruments,
  SQL query patterns for portfolio exposure, Bloomberg BQL rating patterns, FRED series IDs
