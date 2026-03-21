---
description: AI review and validation of a completed reconciliation
allowed-tools: Read, Glob, Grep
argument-hint: <report-path-or-folder>
---

Use Claude's native reasoning to review and validate a completed reconciliation report. Analyze the statement vs HTTP data and either confirm the results or identify corrections needed.

## Arguments

- `$1` — Path to a reconciliation report file (.txt or .xlsx) or the department folder containing reports

## Context

In the original Electron app, this was an external API call to Claude costing tokens and adding latency. In this plugin, Claude IS the host — the analysis happens natively within the conversation at no additional cost.

## Workflow

### Step 1: Load Reconciliation Data

Locate and read the reconciliation artifacts:
- Text report file (`.txt`) — contains the human-readable summary
- JSON data file (if available) — contains structured reconciliation data
- Excel report (`.xlsx`) — contains detailed worksheets

If given a folder path, scan for the most recent reconciliation files.

Read the reconciliation-logic reference for business rules:
```
@${CLAUDE_PLUGIN_ROOT}/references/reconciliation-logic.md
```

### Step 2: Analyze the Reconciliation

Review the data using the bank-specific business rules from the reconciliation-engine skill:

**For Wells Fargo:**
- Verify that only debit totals were compared (not credits, due to ZBA transfers)
- Check if any flagged discrepancies can be explained by ACH Returns, Reversals, or Deletes
- Verify that credit-side entries with these descriptions were checked against debit differences
- Confirm daily debit totals are within $0.01 tolerance

**For Bank of America:**
- Verify the 1-business-day date shift was correctly applied
- Check if timing differences from pending transactions or sweeps explain discrepancies
- Confirm ending balance comparison methodology
- Verify weekend/holiday date handling

### Step 3: Cross-Check Calculations

Independently verify:
- Opening balance + net transactions = closing balance
- Sum of daily totals matches period totals
- Transaction counts are consistent between statement and HTTP
- No duplicate transactions detected
- Date coverage is complete (no gaps in the statement period)

### Step 4: Assess Status

Determine if the reconciliation status is correct:

**Confirm BALANCED** if:
- All daily comparisons match within tolerance
- No unexplained discrepancies remain
- Calculations are internally consistent

**Confirm NEEDS_REVIEW** if:
- Unexplained discrepancies exist
- But also check if any can be reclassified as explained

**Flag ERRORS** if:
- Calculation mistakes found in the original reconciliation
- Wrong comparison methodology applied (e.g., credits compared for WF)
- Date alignment errors
- Missing dates in the comparison

### Step 5: Present Review Findings

Structure the review as:

1. **Overall Assessment**: Confirmed / Corrections Needed / Errors Found
2. **Status Validation**: Is the BALANCED/NEEDS_REVIEW classification correct?
3. **Calculation Verification**: Independent check results
4. **Discrepancy Analysis**: For each discrepancy:
   - Amount and date
   - Likely explanation based on business rules
   - Whether it's a genuine error or expected variance
5. **Recommendations**: Specific actions if corrections are needed

### Step 6: Offer Follow-Up

- "Save this review to the database alongside the reconciliation"
- "Re-run /reconcile with corrections applied"
- "View /statement-history for comparison with prior periods"
