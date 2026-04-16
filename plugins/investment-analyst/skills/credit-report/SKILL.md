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
version: 1.1.0
---

# Credit Report Skill

Automates CreditSights-style quarterly credit analysis for SBC Treasury covered issuers.
Output is a standalone HTML report with embedded Chart.js charts, live Bloomberg ratings,
FRED macro indicators, SBC portfolio exposure, and SBC/PFM tenor limit compliance checks,
plus a companion narrative DOCX writeup.

## Canonical Format Anchors

Both deliverables have a **canonical template** — always match these exactly:

| Deliverable | Canonical template file |
|---|---|
| HTML | `{workspace}/Credit Analysis/JP Morgan 1Q26 Credit Report.html` |
| DOCX | `{workspace}/Credit Analysis/Citigroup 1Q26.docx` |

If a prior-quarter writeup for the target issuer exists (Outlook email, docx), use it for tone
and narrative structure only. Financial numbers must come from the quarter's source PDFs — never
copy figures from a reference doc. See `references/report-format.md` for the full format specs.

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

1. **Press release + Supplement PDFs** — scan the session workspace `US Banks/` folder first
   for `{YYYYMMDD}_{Issuer}_*_Press_Release_*.pdf` and `*_Supplement_*.pdf` dated in the target
   quarter. This is the authoritative source for financial figures.
2. **Quarterly Tearsheets** — `T:\Data\Shared\Credit analysis\Quarterly Tearsheets\{YEAR}\{QQ}{YY}\`
3. **Earnings DOCX write-up** — check for `{Issuer} {QQ}{YY}.docx` in the Credit Analysis workspace
   (treat as tone/structure reference, NOT source of numbers)
4. **Outlook email** — use the outlook-email skill to pull from Sent Items or Inbox
5. **Obsidian vault** — use the obsidian-memory skill for the issuer's tearsheet note

Extract text via pypdf (PDF) or python-docx (DOCX).

> **Critical:** If the user provides a prior-quarter writeup, treat it as a TEMPLATE for voice
> and section order only. Never port its numbers into the current-quarter output. Pull real
> figures from the quarter's press release / supplement PDFs.

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

## Step 7 — Generate HTML Report (Canonical JPM Template)

Build via Python or heredoc Bash script. Chart.js 4.4.1 via CDN.
**Always write HTML using `cat > 'filepath' << 'HTMLEOF' ... HTMLEOF`** to avoid security hook blocks.

**Canonical HTML = the JP Morgan 1Q26 Credit Report template.** Do not invent structure — mirror
its DOM, class names, and chart configs exactly. If in doubt, open `JP Morgan 1Q26 Credit Report.html`
in the Credit Analysis workspace and match it section-for-section.

Structural requirements (see `references/report-format.md` for full CSS tokens):

- **Layout:** 1000px `.page` container on a `#f5f6f8` body with subtle box-shadow
- **Header band:** `.header-band` navy `#1F3864`; `.issuer` 22px/700; `.sub`; `.rec-badge` with
  semi-transparent white background `rgba(255,255,255,.18)` + 1px white border (NOT a solid
  colored pill); ticker + date on the right
- **Section titles:** `.section-title` = 13px uppercase navy with 2px navy `border-bottom` and
  .5px letter-spacing. Do NOT use generic `<h2>`.
- **Executive Summary:** 2-col `.exec-grid`. Left = `.exec-bullets` (list-style:none, ▸ chevron
  pseudo-element, 6 bullets, border-bottom between rows). Right = `.rv-box` (#f0f4fb bg, 3px
  `#2a5da8` left border, "Relative Value" uppercase title in blue, single paragraph explaining
  the call)
- **KPI strip:** `.kpi-strip` flex row of 6 `.kpi` cells with separator borders. `.kpi-val`
  17px/600 navy, `.kpi-chg` uses `.pos` (green `#1a6e3a`) or `.neg` (red `#c43030`)
- **5-Quarter Snapshot Table:** columns = Metric | 1Q[Y-1] | 2Q[Y-1] | 3Q[Y-1] | 4Q[Y-1] | current
  quarter (with `.hi` class on header+cells, #e8f0fb bg) | YoY Δ. Required rows: Managed Revenue,
  NII, NIR, Expenses, Provision, NCOs, Reserve Build, Net Income, EPS, ROTCE, Overhead Ratio,
  CET1, plus segment-specific rows as appropriate
- **Charts row 1 — `.chart-grid` (2-col):**
    - `opLevChart` — grouped bars: Managed Revenue (solid blue) + Noninterest Expense (light red
      fill), with custom afterDraw plugin labeling the gap ($X.XB) above each quarter
    - `cet1Chart` — line chart with area fill, custom afterDraw plugin drawing a dashed "watch
      level" line and labeling each point with the CET1 %
- **Capital Position:** 3 narrative paragraphs (12.5px, line-height 1.7) + a max-480px CET1 QoQ
  waterfall mini-table (QoQ drivers + `<tfoot>` ending CET1)
- **Charts row 2 — Segment charts:** `segRevChart` (grouped bars: prior-year grey + current-year
  colored, YoY % labels above each current-year bar) + `segNIChart` (single bars colored by
  segment, dual labels: $X.XB NI + "ROE XX%")
- **Segment narratives:** 2x2 `.segment-grid` of `.seg-card`. Each card = `.seg-name` + 3
  `.seg-stat` tiles (Revenue / Net Income / ROE with QoQ+YoY chg) + `.seg-body` paragraph
- **Key Monitoring Flags:** `.flag-table` with 4 columns (Flag, Status, Detail, Trigger). Status
  uses `.flag-badge` with `.flag-monitor` (yellow #fff8e1/#8a6d00), `.flag-concern` (red
  #fce8e6/#c43030), `.flag-ok` (green #e6f4ea/#1a6e3a). Minimum 5 flag rows.
- **Peer Comparison:** 4-bank peer table (issuer-specific peer set per `references/sbc-policy.md`).
  Subject column highlighted with `.hi`. 9 rows of comparable metrics.
- **Footer:** slim `.footer` bar with issuer + date on one side, "For internal use only" on the
  other

Optional panels (Bloomberg Ratings, Sector Economics, SBC Portfolio Exposure) may be inserted
between Capital Position and Monitoring Flags when Bloomberg/FRED/SQL data is loaded. They must
use the `.section-title` rhythm and not disrupt the 2-col page layout.

**Palette:**
- Navy `#1F3864` | Blue `#2a5da8` | Green `#1a6e3a` | Red `#c43030` | Neutral `#888`
- Chart canvas height: 190px (main chart-cards) or 100px (segment inline)
- The `.rec-badge` background is always `rgba(255,255,255,.18)` — the text value communicates
  the call; do NOT change the badge background color

---

## Step 8 — Generate DOCX Companion (Canonical Citi Template)

The DOCX is a **plain narrative writeup** — not a report with tables and charts. Match the
`Citigroup 1Q26.docx` template exactly.

**Canonical format:**
- Calibri, 12pt, black text throughout
- Every paragraph uses Word's `Normal` style (do NOT use Heading 1 / Heading 2 — just bold the
  section label paragraphs)
- Margins: Cm(2.16) top/bottom, Cm(2.54) left/right
- Zero tables, zero charts, zero images, zero colored headings, zero horizontal rules
- Section headings = a plain paragraph with the run in **bold** (e.g., "Consumer Banking", "Global
  Markets", "Asset Quality, Capital and Liquidity", "2026 Guidance")
- Body paragraphs are dense prose — no bullets, no numbered lists

**Required structure (in order):**
1. Empty leading paragraph
2. Opening firmwide paragraph — revenues, NII, NIR, provisions, expenses, NI/EPS, ROA/ROE/ROTCE
3. Capital return / CET1 context paragraph — dividends, buybacks, payout, CET1, SLR, liquidity
4. Four segment sections (bold heading + body each):
    - Consumer Banking / Consumer & Community Banking
    - Wealth Management / GWIM / Asset & Wealth Management
    - Corporate & Investment Bank / Global Banking / Banking / Services
    - Markets / Global Markets
   (Adjust labels per issuer's reported segments — match the press release naming exactly)
5. Blank spacer paragraph
6. Asset Quality, Capital and Liquidity — one bold heading + 2 body paragraphs (credit quality,
   then capital/liquidity)
7. Forward Guidance section (bold heading + body) with the current-year outlook as stated by
   management

**Python-docx recipe:**
```python
from docx import Document
from docx.shared import Pt, Cm
doc = Document()
for section in doc.sections:
    section.top_margin = Cm(2.16); section.bottom_margin = Cm(2.16)
    section.left_margin = Cm(2.54); section.right_margin = Cm(2.54)
def para(text, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text); r.font.name = 'Calibri'; r.font.size = Pt(12); r.bold = bold
    return p
# leading blank, firmwide, capital, segments, spacer, asset quality, guidance
```

The DOCX should read as a drop-in replacement for the email-distributed earnings writeup — no
report chrome.

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

- `references/report-format.md` — Full CreditSights format spec, JPM HTML canonical layout,
  Citi DOCX canonical layout, chart configs, section CSS, monitoring flag taxonomy, peer
  comparison table columns, recommendation language templates
- `references/sbc-policy.md` — SBC/PFM tenor limits by security type, AIL approved instruments,
  SQL query patterns for portfolio exposure, Bloomberg BQL rating patterns, FRED series IDs
