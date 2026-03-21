---
name: reconciliation-engine
description: >
  This skill should be used when the user asks to "reconcile a statement",
  "compare statement to HTTP", "check for discrepancies", "generate a
  reconciliation report", "run reconciliation", or needs guidance on
  the business rules for matching bank statement data against HTTP
  reconciliation documents for San Bernardino County Treasury.
version: 0.1.0
---

# Reconciliation Engine

Compare bank statement transaction data against HTTP reconciliation document data, identify discrepancies, and generate Excel and text reports.

## Reconciliation Logic by Bank

### Wells Fargo Reconciliation
- **Compare**: Daily debit totals from statement vs HTTP document
- **Why debits only**: Credits differ due to ZBA (Zero Balance Account) transfers that appear on the statement but not in the HTTP document
- **Debit exceptions**: ACH Returns, Reversals, and Deletes appear as credits on the statement but explain differences in debit totals. When a debit discrepancy is found, check for offsetting credit entries with these descriptions.
- **Match criteria**: Daily debit totals must match within $0.01 tolerance
- **Status**: BALANCED if all dates match, NEEDS_REVIEW if any date has unexplained variance

### Bank of America Reconciliation
- **Compare**: Ending daily balances from statement vs HTTP document
- **Date alignment**: HTTP document dates are shifted back 1 business day. The HTTP entry for "January 3" corresponds to the statement entry for "January 2" (the prior business day).
- **Timing differences**: Pending transactions and sweep transfers cause legitimate timing differences that should be noted but don't necessarily indicate errors.
- **Match criteria**: Ending balances must match after date alignment
- **Status**: BALANCED if all dates match, NEEDS_REVIEW if any date has unexplained variance

## Reconciliation Workflow

1. **Parse both documents** — Statement PDF and HTTP document (post-OCR)
2. **Align dates** — Map statement dates to HTTP dates (direct for WF, shifted for BofA)
3. **Compare values** — Apply bank-specific comparison logic
4. **Identify discrepancies** — Flag dates where values don't match
5. **Classify discrepancies** — Known exceptions (ZBA, ACH Returns) vs unknown
6. **Generate reports** — Excel workbook and text summary

## Report Generation

### Excel Report
Generated using ExcelJS with these worksheets:
- **Summary** — Overall status, period, account info, totals
- **Daily Comparison** — Side-by-side statement vs HTTP by date
- **Discrepancies** — Only dates with differences, with classification
- **Statement Transactions** — Full transaction listing from statement
- **HTTP Transactions** — Full transaction listing from HTTP document

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/export_excel.js --input reconciliation.json --output "/path/to/report.xlsx"
```

### Text Report
Human-readable summary saved alongside the Excel report:
- Header with department, period, bank, account number
- Status line: BALANCED or NEEDS_REVIEW
- Summary totals
- List of discrepancies with amounts and possible explanations

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/reconcile.js --statement statement.json --http http.json --output "/path/to/report"
```

## Database Integration

Reconciliation results can be saved to Azure SQL for historical tracking:
- Table: `banking.statement_reconciliation_history` — One row per reconciliation run
- Table: `banking.statement_reconciliation_details` — One row per date comparison
- Use the `azure-sql-treasurer` skill for database operations

## Additional Resources

- **`references/reconciliation-logic.md`** — Detailed business rules and edge cases
- **`references/database-schema.md`** — Azure SQL table schemas for reconciliation data
