# Infographic Prompt Templates

## Template 1: Executive Summary Dashboard

```
Clean, professional financial infographic on white background. Executive summary dashboard for {ISSUER} credit analysis dated {DATE}.

Layout: Centered header "{ISSUER}" in dark navy (#1f4296) with subtitle "Credit Analysis Summary". Below, a 2x3 grid of metric cards with thin borders:

Row 1:
- Card 1: "CET1 Ratio" in small gray text, "{CET1_VALUE}%" as large bold number, {CET1_STATUS} dot (green=#27ae60 if strong, amber=#f39c12 if adequate, red=#e74c3c if weak)
- Card 2: "ROE" in small gray text, "{ROE_VALUE}%" as large bold number, {ROE_STATUS} dot
- Card 3: "NPL Ratio" in small gray text, "{NPL_VALUE}%" as large bold number, {NPL_STATUS} dot

Row 2:
- Card 4: "Cost/Income" in small gray text, "{CI_VALUE}%" as large bold number, {CI_STATUS} dot
- Card 5: "LCR" in small gray text, "{LCR_VALUE}%" as large bold number, {LCR_STATUS} dot
- Card 6: "Credit Score" in small gray text, "{SCORE}/10" as large bold number, {SCORE_STATUS} dot

Bottom bar: Three rating badges in a row:
- "Moody's: {MOODYS}" in a navy pill badge
- "S&P: {SP}" in a navy pill badge
- "Fitch: {FITCH}" in a navy pill badge

Assessment line: "{ASSESSMENT_TEXT}"

Style: Minimal corporate design. White background. No gradients, no shadows, no decorative elements. Sans-serif font (like Inter or Helvetica). Maximum 3 accent colors.
```

**Nano-banana flags**: `-s 2K -a 16:9`

---

## Template 2: Risk Assessment & Rating Outlook

```
Clean, professional financial infographic on white background. Credit risk assessment for {ISSUER} dated {DATE}.

Top section: Header "{ISSUER} — Risk Assessment" in dark navy (#1f4296).

Left half: Vertical credit score gauge/thermometer showing scale 0-10. Scale has three color zones: red (0-4), amber (4-7), green (7-10). A marker or arrow points to score {SCORE}. Label: "Composite Credit Score: {SCORE}/10"

Right half: Two stacked boxes:
- Top box: Green border, "Upgrade Probability" label, "{UPGRADE_PCT}%" in large green text, small upward arrow
- Bottom box: Red border, "Downgrade Probability" label, "{DOWNGRADE_PCT}%" in large red text, small downward arrow

Bottom section: Three risk factor cards in a horizontal row:
- Card 1: "{RISK_FACTOR_1}" with {STATUS_1} circle indicator (green=#27ae60 for resolved, amber=#f39c12 for monitoring, red=#e74c3c for elevated)
- Card 2: "{RISK_FACTOR_2}" with {STATUS_2} circle indicator
- Card 3: "{RISK_FACTOR_3}" with {STATUS_3} circle indicator

Style: Same as executive summary. Clean, corporate, white background. No decorative elements.
```

**Nano-banana flags**: `-s 2K -a 16:9`

---

## Template 3: Peer Positioning (Optional)

```
Clean, professional financial infographic on white background. Peer comparison positioning for {ISSUER} among {PEER_GROUP} banks.

Layout: A 2D scatter plot style visualization:
- X-axis label: "ROE (%)" ranging from {ROE_MIN} to {ROE_MAX}
- Y-axis label: "CET1 Ratio (%)" ranging from {CET1_MIN} to {CET1_MAX}

Quadrant lines: Dashed gray lines at median ROE and median CET1 creating 4 quadrants:
- Top-right: "Strong Capital + Earnings" (green tinted)
- Top-left: "Strong Capital, Weak Earnings" (amber tinted)
- Bottom-right: "Weak Capital, Strong Earnings" (amber tinted)
- Bottom-left: "Weak on Both" (red tinted)

Bubbles: Each bank as a circle positioned by ROE (x) and CET1 (y). Size proportional to total assets:
{BANK_POSITIONS}

The target issuer bubble is highlighted in navy (#1f4296) and larger. Other banks in gray (#94a3b8).

Style: Clean, minimal, corporate. White background.
```

**Nano-banana flags**: `-s 2K -a 16:9`

---

## Usage Notes

1. Replace all `{PLACEHOLDER}` values with actual data before generating
2. Status colors: Green = metric scores 8-10, Amber = 5-7, Red = 0-4
3. Use reference images with `-r` flag for style consistency:
   ```
   nano-banana "{prompt}" -s 2K -a 16:9 -r /path/to/reference.png -o output-name -d output-dir
   ```
4. Quality check: Read the generated PNG to verify text is legible and data is correct
5. If text rendering is poor, simplify the prompt (fewer numbers, shorter labels)
6. Maximum 3 generation attempts per infographic before using the last result
