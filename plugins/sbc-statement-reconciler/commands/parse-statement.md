---
description: Parse a bank statement PDF and extract transactions
allowed-tools: Read, Bash, Write
argument-hint: <pdf-path> [bank-type]
---

Parse a single bank statement PDF and extract all transactions, daily totals, and summary information without performing reconciliation.

## Arguments

- `$1` — Path to the bank statement PDF file
- `$2` — Optional bank type: "wells-fargo" or "bofa". Auto-detected from filename if not provided.

## File Access: Auto-Copy from Network Drives

If the PDF path is outside the Cowork workspace (e.g., a network drive path):

1. Test if the file is accessible by running `ls` on it via bash.
2. If accessible, **automatically copy** the file into the workspace:
   ```bash
   cp "$NETWORK_PATH" /path/to/cowork/workspace/
   ```
3. Then operate on the local copy.
4. Also check `/mnt/uploads/` for files the user may have uploaded directly.
5. If the file is NOT accessible, inform the user and ask them to verify the path or upload the file.

Do NOT ask the user to copy files manually. Just do it.

## Workflow

1. Locate the PDF: check provided path, auto-copy if needed, or search the workspace for matching PDFs.

2. Detect bank type:
   - If `$2` is provided, use it directly
   - If filename contains "WF" or "Wells" → wells-fargo
   - If filename contains "BofA" or "50090" → bofa
   - Otherwise, ask the user

3. Run the appropriate parser:
   ```bash
   # Wells Fargo
   node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_wf_statement.js "$1"

   # Bank of America
   node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_bofa_statement.js "$1"
   ```

4. Parse the JSON output and present a summary:
   - Account number, period dates
   - Opening and closing balances
   - Total debits and credits
   - Transaction count

5. Show a daily totals table:

   | Date | Debits | Credits | Ending Balance |
   |------|--------|---------|----------------|
   | 01/02 | $50,000.00 | $12,000.00 | $1,234,567.89 |

6. Offer next steps:
   - "Export to Excel with /reconcile"
   - "View full transaction list"
   - "Proceed to reconciliation"
