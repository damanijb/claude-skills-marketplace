---
description: Reconcile a department's bank statement against HTTP document
allowed-tools: Read, Write, Bash, Glob, Grep
argument-hint: <department-folder> [--save-to-db]
---

Run the full reconciliation pipeline for a single department: parse the statement PDF, OCR and parse the HTTP document, compare transactions, and generate reports.

## Arguments

- `$1` — Path to the department folder containing statement PDF and HTTP document
- `--save-to-db` — Optional flag to save results to Azure SQL database

## File Access: Auto-Copy from Network Drives

If the department folder path is outside the Cowork workspace (e.g., network drive):

1. Test if the path is accessible by running `ls` on it via bash.
2. If accessible, **automatically copy** the entire department folder into the workspace:
   ```bash
   cp -r "$NETWORK_PATH" /path/to/cowork/workspace/
   ```
3. Operate on the local copy for all processing steps.
4. After generating reports, **automatically copy results back** to the original network location:
   ```bash
   cp /path/to/cowork/workspace/department/*.txt "$NETWORK_PATH/"
   cp /path/to/cowork/workspace/department/*.xlsx "$NETWORK_PATH/"
   ```
5. If the path is NOT accessible, inform the user and ask them to verify the network drive is mounted.

Do NOT ask the user to copy files manually. Handle the round-trip automatically: copy in, process, copy results back.

## Workflow

### Step 1: Validate Folder Structure

Examine the department folder to locate required files:
- **Statement PDF**: File matching `*.pdf` excluding files containing "http" (case-insensitive)
- **HTTP Document**: File matching `*http*.pdf` or `*HTTP*.pdf`

If files are ambiguous, list what was found and ask the user to confirm which is which.

Detect bank type from filenames:
- "WF" or "Wells" → Wells Fargo
- "BofA" or "50090" → Bank of America

### Step 2: Parse Statement PDF

Run the appropriate statement parser:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_wf_statement.js "/path/to/statement.pdf"
# or
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_bofa_statement.js "/path/to/statement.pdf"
```

Save the JSON output for reconciliation.

### Step 3: OCR the HTTP Document

Send the HTTP document PDF to the OCR webhook for text extraction:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/ocr_webhook.js "/path/to/http-document.pdf"
```

If the OCR webhook is unavailable (network error, timeout), inform the user and suggest:
- Pre-processing the HTTP document outside Cowork
- Providing already-parsed HTML/markdown content
- Using an alternative OCR method

### Step 4: Parse HTTP Content

Run the appropriate HTTP parser on the OCR output:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_wf_http.js "/path/to/ocr-output.md"
# or
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_bofa_http.js "/path/to/ocr-output.md"
```

### Step 5: Reconcile

Run the reconciliation engine comparing statement data vs HTTP data:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/reconcile.js \
  --statement statement-data.json \
  --http http-data.json \
  --bank "wells-fargo" \
  --output "/path/to/department-folder/"
```

This produces:
- A text report (`.txt`) with reconciliation summary
- A JSON file with structured reconciliation data

### Step 6: Generate Excel Report

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/export_excel.js \
  --input reconciliation-data.json \
  --output "/path/to/department-folder/Reconciliation Report.xlsx"
```

### Step 7: Copy Results Back to Network Drive

If the original path was on a network drive, copy the generated reports back:
```bash
cp /path/to/local/department/*.txt "$ORIGINAL_NETWORK_PATH/"
cp /path/to/local/department/*.xlsx "$ORIGINAL_NETWORK_PATH/"
```

Confirm to the user: "Reports generated and copied back to the network share."

### Step 8: Present Results

Display the reconciliation summary:
- **Status**: BALANCED or NEEDS_REVIEW
- **Department**: Name extracted from folder
- **Period**: Statement date range
- **Bank**: Wells Fargo or Bank of America
- **Account**: Account number

If NEEDS_REVIEW, show the discrepancy table:

| Date | Statement | HTTP | Difference | Possible Cause |
|------|-----------|------|------------|----------------|
| 01/15 | $45,000 | $43,500 | $1,500 | ACH Return? |

List files created with their locations (both local workspace and network share if applicable).

### Step 9: Optional Database Save

If `--save-to-db` was specified, use the `azure-sql-treasurer` skill to insert results into:
- `banking.statement_reconciliation_history` — Summary row
- `banking.statement_reconciliation_details` — Per-date detail rows

### Step 10: Offer Next Steps

- "Run /review-reconciliation to have Claude AI validate the results"
- "Run /statement-history to see past reconciliations for this department"
- "Run /bulk-reconcile to process additional departments"
