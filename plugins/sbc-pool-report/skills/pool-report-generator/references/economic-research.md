# Economic Research & Commentary Guide

## Purpose

This reference guides the **Economic Research agent** (Phase 1C) and the
**Economic Commentary agent** (Phase 2B) in producing plain-English economic
content for the Board of Supervisors.

The economic section of the Pool Report should tell a **story** — not just
present numbers. Board members are intelligent professionals but most are NOT
finance specialists. Every slide should answer: "What is happening, why does
it matter, and what does it mean for our county's money?"

---

## Research Methodology (Phase 1C)

### WebSearch Queries

Run these searches to gather current information. Replace `{month}` and `{year}`
with the report's current month and year.

**Federal Reserve & Rates:**
- `"Federal Reserve FOMC decision {month} {year}"`
- `"Fed interest rate outlook {year}"`
- `"FOMC dot plot projections {year}"`

**Inflation:**
- `"CPI inflation report {month} {year}"`
- `"inflation outlook United States {year}"`
- `"PCE price index latest {year}"`

**Employment:**
- `"jobs report unemployment {month} {year}"`
- `"labor market conditions United States {year}"`

**Credit Markets:**
- `"investment grade credit spreads {year}"`
- `"corporate bond market outlook {year}"`
- `"high yield default rate {year}"`

**Fixed-Income Themes:**
- `"treasury market outlook {month} {year}"`
- `"municipal bond market {year}"`
- `"government bond investors {year}"`

### Research Output Schema

Save to `/tmp/sbc_economic_research.json`:

```json
{
  "research_date": "February 12, 2026",
  "fed_policy": {
    "headline": "Fed holds rates at 4.25-4.50% range",
    "detail": "The FOMC voted to maintain the current rate...",
    "forward_guidance": "Dot plot suggests 2 more cuts in 2026...",
    "data_points": {"current_rate": 4.33, "last_change": "December 2025", "direction": "holding"}
  },
  "inflation": {
    "headline": "CPI inflation at 2.8%, trending toward Fed's 2% target",
    "detail": "...",
    "data_points": {"cpi_yoy": 2.8, "pce_yoy": 2.5, "core_cpi": 3.1}
  },
  "employment": {
    "headline": "Unemployment steady at 4.3%, labor market cooling gradually",
    "detail": "...",
    "data_points": {"unemployment": 4.3, "nonfarm_payrolls": 150000}
  },
  "credit_markets": {
    "headline": "Investment-grade spreads tight at 98 bps",
    "detail": "...",
    "data_points": {"ig_spread": 0.98, "hy_spread": 3.2}
  },
  "market_themes": [
    {
      "title": "Fed Rate Cut Expectations Shifting",
      "narrative": "Markets now expect...",
      "chart_suggestion": "FEDFUNDS history",
      "relevance": "HIGH"
    },
    {
      "title": "Treasury Supply Dynamics",
      "narrative": "The U.S. Treasury's borrowing needs...",
      "chart_suggestion": "DGS10 history",
      "relevance": "MODERATE"
    }
  ]
}
```

### Theme Selection Criteria

Pick the top 2-3 themes based on:
1. **Relevance** — Does it directly affect a $16B government fixed-income pool?
2. **Recency** — Is it a current talking point (last 30 days)?
3. **Materiality** — Could it move the portfolio's value, income, or risk profile?

**Good themes:** Fed policy changes, yield curve shifts, credit spread moves, Treasury issuance, inflation surprises, employment shocks, banking sector conditions.

**Bad themes (skip):** Equity market moves, crypto, individual stock performance, trade wars (unless directly affecting Treasury demand), gold prices.

---

## Writing Guidelines (Phase 2B)

### Target Audience: "Average Joe" Board Member

Imagine you're explaining the economy to a successful business owner who reads
the Wall Street Journal occasionally but doesn't manage bond portfolios. They're
smart, but they don't know what "OAS" or "duration" means without explanation.

### The 5 Rules

1. **Lead with the headline.** Start every section with what happened.
   - BAD: "The Federal Open Market Committee convened on January 29th..."
   - GOOD: "The Fed held interest rates steady at 3.64% this month."

2. **Explain why it matters.** Connect the fact to the county's money.
   - BAD: "The unemployment rate was 4.3%."
   - GOOD: "Unemployment held at 4.3%, suggesting the economy is still growing but cooling — which supports the Fed's gradual rate-cutting path."

3. **Use analogies.** Make abstract concepts concrete.
   - "Think of the yield curve like a price list for lending money — normally you charge more for longer loans. When the curve flattens, it means investors aren't demanding much extra for tying up money longer."
   - "Credit spreads are like a risk premium — the extra interest companies pay above Treasuries. When spreads are tight (low), it means investors feel confident about corporate health."

4. **Numbers in context.** Always compare to something.
   - BAD: "CPI is 2.8%"
   - GOOD: "Inflation has dropped to 2.8% from its 2022 peak of 9.1%, and is approaching the Fed's 2% target."

5. **End with "So What?"** Every slide gets a Portfolio Impact callout.
   - "PORTFOLIO IMPACT: The current rate environment allows the pool to reinvest maturing securities at competitive yields, supporting continued income generation consistent with Investment Policy objectives."

### Tone Rules (from tone-guide.md)

- **Fiduciary stewardship** — we manage the public's money prudently
- **Never say**: "positioned to benefit", "opportunistically", "outperforms"
- **Always say**: "consistent with Investment Policy objectives", "within policy parameters"
- **Qualified language**: "may", "projected", "illustrative", "is expected to"
- **No exclamation marks**, no first person (except disclosures), no prediction language

### Content Length Per Slide

Each economic slide has two columns:
- **Left column (4.25" wide)**: Chart image or KPI cards
- **Right column (4.5" wide)**: Commentary text

At 10.5pt font, the right column fits approximately:
- Headline: 1 line (bold)
- Body narrative: 4-6 sentences (about 60-80 words)
- Sub-section (if any): 2-3 sentences
- Portfolio Impact callout: 1-2 sentences at bottom of slide

**Total words per slide: 80-120 words** (excluding the callout)

---

## Slide-by-Slide Commentary Templates

### Slide 3: Economic Overview
```
HEADLINE: [One sentence state of the economy]

NARRATIVE: The U.S. economy [is growing/slowing/stable] as measured by
[GDP/employment/inflation metrics]. The Federal Reserve [action] interest
rates [to/at X%], reflecting [confidence in/concern about] [economic factor].
Key indicators suggest [direction of travel].

For the county's Investment Pool, these conditions mean [impact on
yields/income/risk].

PORTFOLIO IMPACT: [How current conditions affect the pool's returns, risk, or strategy]
```

### Slide 4: The Fed & Interest Rates
```
HEADLINE: The Fed [held rates steady at / cut rates to / raised rates to] X%.

WHAT THIS MEANS: When the Fed [raises/lowers/holds] rates, it directly affects
the interest the county earns on short-term investments like money market funds
and commercial paper, which make up [X%] of the pool. [Higher/Lower/Stable]
rates mean [more/less/steady] income from these holdings.

The Fed's forward guidance suggests [X more cuts/holds/hikes] through [year],
which would [support/challenge] the pool's current yield of [X%].

PORTFOLIO IMPACT: [Specific link to pool's short-term holdings yield]
```

### Slide 5: Inflation Update
```
HEADLINE: Inflation [fell to / rose to / held at] X%, [approaching / still above] the Fed's 2% target.

WHY IT MATTERS: Inflation determines the "real" return on investments — if the
pool earns 3.6% but inflation is 2.8%, the real return is only 0.8%. The good news
is inflation has [declined significantly / remained stable] from [historical comparison],
meaning the pool's returns are [providing positive real income / being eroded by rising prices].

PORTFOLIO IMPACT: [Real return calculation and what it means]
```

### Slide 6: Labor Market
```
HEADLINE: Unemployment [held steady at / rose to / fell to] X%.

NARRATIVE: The labor market [remains resilient / is showing signs of cooling / continues to tighten].
[Context about jobs created, sectors, wage growth]. A [strong/softening] job market
[supports/pressures] the Fed's ability to [continue cutting / hold / raise] rates,
which in turn affects the yields available for the county's investments.

PORTFOLIO IMPACT: [Link between employment and rates/investment opportunities]
```

### Slide 7: Yield Curve Analysis
```
HEADLINE: The yield curve is [positively sloped / flat / inverted], with 10-year Treasuries
yielding X% versus 2-year at Y% (a spread of Z%).

ANALOGY: Think of the yield curve as a price list for lending money to the government.
Normally, you charge more for longer loans because there's more uncertainty. Right now,
the curve is [steep/flat/inverted], which historically signals [expectations of growth / uncertainty / recession risk].

WHAT SHAPE MEANS: For the county, a [steep] curve means [we earn meaningfully more by extending
maturity / short-term and long-term rates offer similar returns]. The pool's weighted average
duration of [X years] positions it [well / conservatively] relative to the current curve shape.

PORTFOLIO IMPACT: [How curve shape affects reinvestment and duration decisions]
```

### Slide 8: Credit Market Conditions
```
HEADLINE: Investment-grade credit spreads are [tight / wide / moderate] at X basis points.

NARRATIVE: Credit spreads measure the extra interest companies pay above government bonds.
At [X bps], spreads are [near historical lows / wider than average / in line with norms],
indicating that investors are [confident / cautious / neutral] about corporate health.
The county holds [X%] of its portfolio in corporate-linked securities (corporate notes,
commercial paper, and ABS).

PORTFOLIO IMPACT: [How spread levels affect the pool's credit holdings]
```

---

## KPI Card Content for Economic Overview (Slide 3)

Present 6 economic indicators as KPI cards (3×2 grid):

| Card | Value Source | Label |
|------|------------|-------|
| Fed Funds Rate | FEDFUNDS latest | "Fed Funds Rate" |
| Unemployment | UNRATE latest | "Unemployment" |
| CPI Inflation | Calculated YoY | "Inflation (CPI YoY)" |
| 10-Year Treasury | DGS10 latest | "10-Year Treasury" |
| BBB Spread | BAMLC0A4CBBB latest | "IG Credit Spread" |
| Yield Curve Slope | T10Y2Y latest | "10Y-2Y Spread" |

Each card shows the value prominently (28pt) with the label below (10pt).

---

## Market Theme Slide Template

Each market theme slide follows the same two-column layout:

**Left column:** A relevant chart image (from FRED history data) or a set of
KPI cards illustrating the theme.

**Right column:**
```
SECTION LABEL: "MARKET THEME"

TITLE: [Bold headline, 14pt]

NARRATIVE: [4-5 sentences explaining the theme in plain English.
What happened, why, and where things are heading. Include specific
numbers from FRED data or web research.]

SIGNIFICANCE: [HIGH / MODERATE / LOW]

PORTFOLIO IMPACT: [2 sentences on specific implications for the
county's investment pool.]
```

---

## Economic Summary Slide (Slide 11)

Two-column layout:

**Left: Key Takeaways**
4-5 bullet points summarizing the most important economic observations:
- "The Fed [action] rates, signaling [direction]"
- "Inflation at X% is [approaching/above/below] the 2% target"
- "Labor market [strong/cooling], supporting [current/changed] Fed policy"
- "Credit conditions [favorable/tightening], with spreads at [X bps]"
- "Yield curve [shape] suggests [market expectation]"

**Right: Portfolio Implications**
3-4 sentences connecting economic conditions to portfolio positioning:
"Given these economic conditions, the county's Investment Pool is [well-positioned /
conservatively structured / appropriately balanced]. The portfolio's [X%] weighted
average yield [exceeds/meets] the current inflation rate of [Y%], providing positive
real returns. The moderate duration of [Z years] provides [flexibility/stability]
as the Federal Reserve [continues its rate path]. All positions remain within
Investment Policy limits."
