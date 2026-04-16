---
name: tearsheet
description: >
  Automate quarterly issuer tearsheet updates for SBC Treasury credit analysis.
  Use this skill whenever the user invokes /tearsheet, says "update the tearsheet",
  "run the tearsheet for [issuer]", "process the [issuer] tearsheet", "update [issuer]
  analysis", or asks to update/archive a quarterly credit tearsheet for any covered
  issuer. Orchestrates the full pipeline: pull earnings writeup from Outlook →
  inject narrative into Excel template via COM (Bloomberg formulas refresh automatically) →
  export PDF to quarterly archive folder → update Obsidian vault.
version: 1.0.0
---

# Tearsheet Update Skill

End-to-end automation for quarterly issuer tearsheet updates at SBC Treasury.

## Invocation

```
/tearsheet [issuer] [quarter]
```

**Examples:**
- `/tearsheet Citibank 1Q26`
- `/tearsheet "JP Morgan" 1Q26`
- `/tearsheet "Bank of America" 1Q26`
- `/tearsheet "BNP Paribas" 1Q26`

If the user provides the earnings writeup directly (as a `.docx` upload or pasted
text), skip Step 1 and use what's provided.

---

## Key Paths

| Resource | Path |
|---|---|
| Templates | `T:\Data\Shared\Credit analysis\Quarterly Tearsheets\Tearsheet Templates\{Issuer}.xlsx` |
| Archive | `T:\Data\Shared\Credit analysis\Quarterly Tearsheets\{YEAR}\{QQ}{YY}\{Issuer} {QQ}{YY}.pdf` |
| Vault | See `references/issuer-config.md` for per-issuer vault paths |

For **fiscal calendar issuers** (Canadian banks, Toyota, Visa, John Deere, P&G),
use dual-label PDF naming: `{Issuer} {FiscalQQ}{YY} (Calendar {CalQQ}{YY}).pdf`
See `references/issuer-config.md` for fiscal offset details.

---

## Step 1 — Pull Earnings Writeup from Outlook

Search Sent Items first (Damani sends the writeup out after completing it), then
Inbox if not found. The writeup may be in the email body or a `.docx` attachment.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/outlook-email/scripts/fetch_emails.py" \
  --folder "Sent Items" \
  --subject "{issuer_keyword}" \
  --since "{current_year}-01-01" \
  --limit 5 \
  --output-format json
```

Replace `{issuer_keyword}` with a short form of the issuer name (e.g., "Citi", "JPMorgan",
"BofA", "BNP"). If a `.docx` attachment is found, save it to `/tmp/` and extract
the text via python-docx:

```bash
python3 -c "
from docx import Document
doc = Document('/tmp/writeup.docx')
text = '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
print(text)
"
```

**If no email found:** Ask the user to provide the writeup text or upload the docx.

---

## Step 2 — Inject into Excel + Export PDF

With the issuer's Excel template **open in Excel with Bloomberg running**, call the
injection script. This attaches to the live workbook via Windows COM, injects the
narrative and economic context, triggers a Bloomberg refresh, exports the PDF, and
saves the template.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/tearsheet/scripts/inject_and_export.py" \
  --workbook "{Issuer}.xlsx" \
  --narrative "{full_narrative_text}" \
  --economic-context "{formatted_economic_context_block}" \
  --issuer "{Issuer}" \
  --quarter "{QQ}{YY}" \
  --year "{YYYY}"
```

**Fiscal offset issuers:** Pass `--fiscal-label "{FiscalQQ}{YY}"` and
`--calendar-label "{CalQQ}{YY}"` to generate the dual-label PDF filename.

**Expected output:**
```
==================================================
SBC Tearsheet Update: Citibank 1Q26
==================================================
✓ Connected to workbook: Citibank.xlsx
✓ Narrative injected into Analysis sheet (4821 chars)
✓ Economic context updated on Front Page
✓ Bloomberg refresh triggered
✓ PDF exported: T:\...\1Q26\Citibank 1Q26.pdf
✓ Workbook saved: Citibank.xlsx
==================================================
✓ COMPLETE
==================================================
```

**If Excel is not open:** Instruct the user to open the template in Excel with
Bloomberg running, then re-run. Do not attempt to open Excel programmatically.

**If `win32com` is missing:** Install with `pip install pywin32 --break-system-packages`

---

## Step 3 — Update Obsidian Vault

After the PDF is filed, update the issuer's vault note and coverage grid.

**Vault note path:** `{VAULT}/08 - Tearsheets/{Sector}/{Issuer}.md`
(see `references/issuer-config.md` for exact paths)

Append a new dated section using the `desktop-commander:write_file` (append mode):

```markdown
## {QQ}{YY} Earnings — [Report Date]
[Confirmed {YYYY-MM-DD}] #tearsheet #confirmed #earnings/{ISSUER_TAG}

**Key Metrics:**
- Revenue: $X.XB ([+/-]X% YoY)
- NII: $X.XB | NIM: X.XX%
- CET1: X.X% ([+/-]Xbps QoQ)
- RoTCE: X.X%
- NCO Rate: Xbps | NPL Ratio: X.X%
- Net Income: $X.XB ([+/-]X% YoY)

**Key Takeaways:**
[2-3 bullet points on the most notable developments — credit quality, capital,
strategic, guidance]

**Watch Items:**
[1-2 items flagged for next quarter monitoring]

[[{Issuer} Tearsheet]] | [[TEARSHEET-COVERAGE-GRID]]
```

**Coverage grid:** Edit `{VAULT}/08 - Tearsheets/TEARSHEET-COVERAGE-GRID.md` to
mark this quarter complete for the issuer using `desktop-commander:edit_block`.

---

## Completion Summary

After all steps, display in chat:

```
✅ Tearsheet Complete: {Issuer} {QQ}{YY}

  PDF archived:  T:\...\{QQ}{YY}\{Issuer} {QQ}{YY}.pdf
  Template:      T:\...\Tearsheet Templates\{Issuer}.xlsx  (saved)
  Vault updated: 08 - Tearsheets\{Sector}\{Issuer}.md
  Coverage grid: marked complete

  Key metrics captured:
    Revenue:  $X.XB (+X% YoY)
    CET1:     X.X%
    RoTCE:    X.X%
    NCOs:     $X.XB
```

---

## Reference Files

- `references/issuer-config.md` — Issuer → template filename, CDS ticker, sector,
  vault path, and fiscal offset details for all 44 covered issuers.
