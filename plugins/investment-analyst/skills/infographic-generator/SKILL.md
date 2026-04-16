---
name: infographic-generator
description: This skill should be used when the user asks to "create infographic", "generate infographic", "visual summary", "nano-banana infographic", "executive summary visual", "risk dashboard image", "create visual for report", or needs to generate AI-powered infographic images for embedding in financial reports using nano-banana.
version: 1.0.0
---

# Infographic Generator

Generate nano-banana infographic images for visual summaries in financial reports. Produces 2 infographics per analysis: an Executive Summary dashboard and a Risk/Rating visual.

## Prerequisites

- `nano-banana` CLI must be installed. Install via: `pip install nano-banana --break-system-packages`
- Research synthesis data from `{workspace}/data/research-synthesis.json`
- Financial model data from `{workspace}/model/`
- Reference images from prior reports (optional, for style consistency)

## Standard Infographics for Each Analysis

### 1. Executive Summary Dashboard

**Purpose**: Single-image overview of key metrics, ratings, and assessment.

**Prompt template** (customize with issuer data):
```
Clean, professional financial infographic on white background. Executive summary dashboard for {issuer} credit analysis.

Layout: Centered header with company name "{issuer}" in dark navy (#1f4296). Below, a 2×3 grid of metric cards:
- Card 1: "CET1 Ratio" large number "{CET1}%" with green/amber/red status dot
- Card 2: "ROE" large number "{ROE}%" with status dot
- Card 3: "NPL Ratio" large number "{NPL}%" with status dot
- Card 4: "Cost/Income" large number "{CI}%" with status dot
- Card 5: "LCR" large number "{LCR}%" with status dot
- Card 6: "Credit Score" large number "{score}/10" with status dot

Bottom section: Credit ratings row showing Moody's: {moody}, S&P: {sp}, Fitch: {fitch}
Below: Assessment text: "{assessment}"

Style: Minimal, clean, corporate. No decorative gradients. Maximum 3 accent colors (navy, green, red). White background. Sans-serif font.
```

**Nano-banana command:**
```bash
nano-banana "{prompt}" -s 2K -a 16:9 -o executive-summary -d {workspace}/infographics
```

### 2. Risk/Rating Visual

**Purpose**: Visualize upgrade/downgrade probability, risk factors, and rating trajectory.

**Prompt template:**
```
Clean, professional financial infographic on white background. Risk assessment and rating outlook for {issuer}.

Layout:
- Top: Company name in dark navy. Subtitle: "Credit Risk Assessment — {date}"
- Left panel: Vertical gauge showing composite credit score of {score}/10 with color gradient (red at bottom, amber middle, green top). Needle pointing to {score}.
- Right panel: Two probability boxes:
  - "Upgrade Probability: {upgrade_pct}%" with upward green arrow
  - "Downgrade Probability: {downgrade_pct}%" with downward red arrow

Bottom section: 3 risk factor cards in a row:
- "{risk1}" with {status1} status (green circle = resolved, amber = monitoring, red = elevated)
- "{risk2}" with {status2} status
- "{risk3}" with {status3} status

Style: Clean corporate design. Navy (#1f4296) headers. Status colors: green (#27ae60), amber (#f39c12), red (#e74c3c). White background. No decorative elements.
```

**Nano-banana command:**
```bash
nano-banana "{prompt}" -s 2K -a 16:9 -o risk-assessment -d {workspace}/infographics
```

## Workflow

1. **Extract data** from research synthesis and financial model
2. **Compose prompt** by filling in the template with actual values
3. **Generate image**: Run nano-banana CLI command
4. **Validate**: Read the generated PNG to check quality
5. **Iterate if needed**: Refine prompt and regenerate (up to 3 attempts)
6. **Optional**: Use a reference image from previous reports for style consistency:
   ```bash
   nano-banana "{prompt}" -s 2K -a 16:9 -r {reference_image} -o {name} -d {workspace}/infographics
   ```

## Quality Checks

After generation, verify:
- [ ] White/light background (no dark mode)
- [ ] Company name is correctly spelled
- [ ] Numbers are legible and correctly placed
- [ ] Color coding matches status (green = good, red = bad)
- [ ] No decorative gradients or shadows
- [ ] Professional corporate appearance

## Reference Images

If prior infographics exist for style consistency, pass one using the `-r` flag:
```bash
nano-banana "{prompt}" -s 2K -a 16:9 -r "{path/to/prior-infographic.png}" -o {name} -d {workspace}/infographics
```

Look for prior infographics in `T:/Data/Shared/Credit analysis/Quarterly Tearsheets/{YEAR}/{QQ}{YY}/`
or the issuer's most recent quarterly archive folder.

For detailed prompt templates for additional infographic types, load `references/infographic-prompts.md`.
