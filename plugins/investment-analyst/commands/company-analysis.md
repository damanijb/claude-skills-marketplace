---
description: Produce a quarterly earnings writeup for a covered issuer by collecting source documents from investor relations, SEC EDGAR, and earnings transcripts in parallel, then writing a docx that matches the prior quarter's structure with every number cited to a source. Runs before /tearsheet when the writeup email doesn't exist yet.
allowed-tools: Bash, Read, Write, Edit, Agent, TodoWrite, AskUserQuestion, mcp__desktop-commander__read_file, mcp__desktop-commander__write_file, mcp__desktop-commander__list_directory
argument-hint: "[issuer] [quarter] — e.g., Citi 1Q26 | JP Morgan 1Q26 | BNP Paribas 1Q26"
---

<!--
Produces the earnings writeup that feeds /tearsheet. Flow:
  1. Resolve issuer config and prior quarter
  2. Pull prior-quarter writeup from Outlook Sent Items (reference structure)
  3. Dispatch 4 source-collector agents in parallel (press release, supplement, filing, transcript)
  4. Dispatch 1 analysis-writer agent with all sources + prior writeup
  5. Save docx to workspace folder, summarize, point user at /tearsheet
-->

**Arguments provided:** $ARGUMENTS

Parse `$ARGUMENTS` to extract:
- **issuer** — covered issuer short name (e.g., "Citi", "JPM", "BNP")
- **quarter** — calendar quarter label (e.g., "1Q26", "2Q26")

If either argument is missing, use `AskUserQuestion` to get them. Do NOT
proceed with partial arguments.

---

## Step 1 — Resolve Issuer and Prior Quarter

Load the issuer config reference to get the full issuer name, ticker, sector,
template filename, vault path, and any fiscal-offset details:

@${CLAUDE_PLUGIN_ROOT}/skills/tearsheet/references/issuer-config.md

Resolve the short name in `$ARGUMENTS` to the canonical issuer record. If no
match, stop and list the covered issuers.

Compute the **prior calendar quarter** from `quarter`:
- 1Q26 → 4Q25
- 2Q26 → 1Q26
- 3Q26 → 2Q26
- 4Q26 → 3Q26

For **fiscal-offset issuers** (Canadian banks, Toyota, Visa, John Deere,
Procter & Gamble — see issuer-config.md), also compute the issuer's fiscal
quarter label for the current calendar quarter. Both labels will be passed to
the writer so it can dual-label the docx output.

Determine the **sector** from the issuer config (`us_banks`, `eu_banks`,
`canadian_banks`, `corporates`, `insurance`).

---

## Step 2 — Pull Prior Quarter Writeup from Outlook

The prior quarter's writeup is the **structural and voice reference**, not
the content source. Pull it from Sent Items:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/outlook-email/scripts/fetch_emails.py" \
  --folder "Sent Items" \
  --subject "{issuer_keyword} {prior_quarter}" \
  --since "{prior_quarter_year}-01-01" \
  --limit 5 \
  --output-format json
```

Use a short issuer keyword that matches your typical subject line convention
(e.g., "Citi", "JPMorgan", "BofA", "BNP", "Toyota").

**Resolution rules:**
- If exactly one email matches: use it. If it has a `.docx` attachment,
  save to `/tmp/prior-writeup.docx` and prefer the attachment over the body.
- If multiple match: prefer the one with a `.docx` attachment; otherwise,
  show the subjects and dates to the user and ask which to use.
- If none match: ask the user whether to (a) proceed without a prior
  writeup (the writer will use a default sector template) or (b) abort so
  they can provide one manually.

---

## Step 3 — Prepare Workspace

Create the per-run workspace inside the Credit Analysis folder:

```
T:/Data/Shared/Credit analysis/Earnings Emails/{Issuer} {Quarter}/
├── sources/
│   └── raw/             <-- PDFs land here
├── prior-writeup.{docx|md}
└── {Issuer} {Quarter} Earnings Writeup.docx  <-- final output
```

Create the directory structure with `mkdir -p`. If the folder already
exists and contains a prior run's `Earnings Writeup.docx`, ask before
overwriting.

---

## Step 4 — Dispatch Source Collection Agents (PARALLEL)

Dispatch **four `source-collector` agents in a single message**, one per
source type. Each agent gets the same issuer/quarter/ticker/output_dir and
a distinct `source_type`.

Agent prompt template (fill in per-source):

```
Collect the {source_type} document for the following quarterly earnings run.

issuer: {full_issuer_name}
ticker: {bloomberg_ticker}
quarter: {calendar_quarter}  (e.g., 1Q26)
fiscal_quarter: {fiscal_quarter_if_offset, else same as calendar}
source_type: {press_release | supplement | filing | transcript}
output_dir: T:/Data/Shared/Credit analysis/Earnings Emails/{Issuer} {Quarter}/sources
plugin_root: ${CLAUDE_PLUGIN_ROOT}

Follow your full workflow (navigate → download → extract → write). Return
the single-line status result. Do not analyze or summarize.
```

Launch all four in one `Agent` tool call block. Wait for all to complete
before proceeding.

---

## Step 5 — Aggregate Collection Results

After agents return, read the `sources_dir`:
- For each `{source_type}.md` present: note size, log as available
- For each `{source_type}-unavailable.txt` present: read the reason, log

If **fewer than 2 sources** returned available, stop and report: the
writeup would be too thin. Ask the user whether to proceed anyway, provide
documents manually, or abort.

If **press release is unavailable**, this is unusual — the press release is
the easiest source to obtain. Ask the user whether this is expected (e.g.,
issuer has not yet reported) or whether to retry.

---

## Step 6 — Dispatch Analysis-Writer Agent

Single `analysis-writer` agent invocation with all inputs:

```
Produce the {Issuer} {Quarter} earnings writeup docx.

issuer: {full_issuer_name}
quarter: {calendar_quarter}
prior_quarter: {prior_calendar_quarter}
sector: {us_banks | eu_banks | canadian_banks | corporates | insurance}
fiscal_label: {fiscal_quarter_or_null}
prior_writeup_path: T:/Data/Shared/Credit analysis/Earnings Emails/{Issuer} {Quarter}/prior-writeup.docx
sources_dir: T:/Data/Shared/Credit analysis/Earnings Emails/{Issuer} {Quarter}/sources
output_path: T:/Data/Shared/Credit analysis/Earnings Emails/{Issuer} {Quarter}/{Issuer} {Quarter} Earnings Writeup.docx
plugin_root: ${CLAUDE_PLUGIN_ROOT}

Follow your full process (structural prior → metric table → section drafts →
new-section inserts → data gaps footer → docx). Return your structured
summary.
```

---

## Step 7 — Present Results to User

Display a concise summary:

```
✅ Earnings Writeup Complete: {Issuer} {Quarter}

  File:              [View the writeup](computer://T:/Data/Shared/Credit analysis/Earnings Emails/{Issuer} {Quarter}/{Issuer} {Quarter} Earnings Writeup.docx)
  Word count:        {N}
  Sources used:      {list}
  Sources missing:   {list with reasons, or "none"}
  New sections:      {count} {list titles if any}
  Not-found metrics: {count} {list if any}

  Next step:
    1. Review and edit the docx
    2. Send the email to your Sent Items as usual
    3. Run: /tearsheet {issuer} {quarter}
```

If the writer returned `INSUFFICIENT SOURCES`, display that instead and do
not claim completion.

---

## Failure Modes

- **Chrome MCP not connected:** All four source agents will return
  UNAVAILABLE. Writer will produce INSUFFICIENT SOURCES. Tell user to
  connect Chrome MCP and retry.
- **pymupdf4llm not installed:** Source agents will return UNAVAILABLE with
  extractor-error reason. Tell user: `pip install pymupdf4llm --break-system-packages`
- **Outlook COM unavailable:** Prior writeup fetch fails. Fall back to
  asking user for a manual path, or proceed with default sector template.
- **Issuer not in covered universe:** Stop with clear message, show the
  covered list, suggest `/credit-report` for one-off analysis of
  non-covered issuers.
