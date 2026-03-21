# Reconciliation Business Rules

## Overview

Bank statement reconciliation compares data from two sources:
1. **Bank Statement PDF** — The official monthly statement from the bank
2. **HTTP Reconciliation Document** — A scanned document from the county's internal banking system (requires OCR)

The goal is to verify that all transactions recorded internally match the bank's records.

## Wells Fargo Reconciliation Rules

### Comparison Method: Daily Debit Totals

Compare **debit totals only** for each business day. Credits are excluded from comparison because:
- ZBA (Zero Balance Account) transfers appear on the bank statement as credits
- ZBA transfers do NOT appear in the HTTP reconciliation document
- This creates a known, expected credit difference that is not a discrepancy

### Debit Exception Handling

When a debit discrepancy is found for a given date, check for these credit-side entries that explain debit differences:

| Entry Type | Description Pattern | How It Affects Debits |
|-----------|-------------------|---------------------|
| ACH Return | "ACH RETURN" or "RETURN ITEM" | Reverses a prior debit — appears as credit but offsets debit total |
| Reversal | "REVERSAL" or "REV" | Corrects a prior debit — credit that explains debit shortfall |
| Delete | "DELETE" or "DEL" | Removes a prior debit — credit that explains debit shortfall |

**Resolution**: If the debit discrepancy amount matches the sum of these credit-side exceptions for the same date, the discrepancy is **explained** and the date is considered balanced.

### Tolerance

- Daily debit totals must match within **$0.01** (penny rounding)
- Amounts beyond this tolerance require investigation

### Multi-Part Statements

Wells Fargo statements may be split across multiple PDFs (Part 1, Part 2, etc.) when the department has high transaction volume. All parts must be parsed and combined before reconciliation.

## Bank of America Reconciliation Rules

### Comparison Method: Ending Daily Balances

Compare **ending balances** for each business day rather than transaction totals.

### Date Alignment (Critical)

HTTP document dates are **shifted back 1 business day** relative to statement dates:
- HTTP entry dated "January 3" corresponds to statement entry for "January 2"
- This shift accounts for the bank's processing cutoff time
- Weekend and holiday handling: Skip non-business days when computing the shift

**Example:**
| HTTP Date | Statement Date | Balance |
|-----------|---------------|---------|
| Mon Jan 6 | Fri Jan 3 | $1,234,567.89 |
| Tue Jan 7 | Mon Jan 6 | $1,245,678.90 |

### Timing Differences

These cause legitimate balance differences that should be noted but are not errors:

| Type | Description | Impact |
|------|-------------|--------|
| Pending Transactions | Authorized but not yet posted | Temporary balance difference |
| Sweep Transfers | Automated end-of-day transfers | Balance differs until sweep posts |
| Wire Transfers in Transit | Sent but not yet received | Multi-day settlement lag |

### Weekend/Holiday Dates

- Skip weekends (Saturday, Sunday) when aligning dates
- Skip federal banking holidays
- Statement may show Friday's closing balance for the weekend period

## Status Classification

### BALANCED
- All dates in the comparison match within tolerance
- Any initial discrepancies have been explained by known exceptions
- Calculation cross-checks pass

### NEEDS_REVIEW
- One or more dates have unexplained discrepancies
- The reconciliation requires human investigation
- Report should list each discrepancy with:
  - Date
  - Statement value
  - HTTP value
  - Difference amount
  - Any partial explanations found

## Cross-Check Validations

Regardless of bank type, verify:

1. **Opening balance continuity**: Prior month's closing balance = current month's opening balance
2. **Balance equation**: Opening + credits - debits = closing (within $0.01)
3. **Date completeness**: Every business day in the period has an entry
4. **No duplicates**: No transaction appears twice in the parsed data
5. **Period boundaries**: First and last dates match the statement period

## Report File Naming Convention

```
{Department} {Account} {Month} {Year} Reconciliation {STATUS} {Date}.{ext}
```

Examples:
- `ACR 3163 Jan 26 Reconciliation BALANCED 2026-02-06.txt`
- `TAX 50090 Jan 26 Reconciliation NEEDS_REVIEW 2026-02-06.xlsx`
