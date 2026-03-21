---
description: Query past reconciliation results from Azure SQL
allowed-tools: Read, Grep, Glob
argument-hint: [department] [period] [status]
---

Query historical reconciliation results from the Azure SQL database. View past status, find unresolved discrepancies, and track processing completeness.

## Arguments

- `$1` — Optional department name filter (e.g., "ACR")
- `$2` — Optional period filter (e.g., "January 2026")
- `$3` — Optional status filter: "balanced", "needs-review", or "all"

## Workflow

### Step 1: Build Query

Construct a SQL query against the reconciliation history tables using the `azure-sql-treasurer` skill (already available in the environment).

Base query targets:
- `banking.statement_reconciliation_history` — Summary records
- `banking.statement_reconciliation_details` — Per-date detail records

Apply filters based on provided arguments:
- Department name (exact or LIKE match)
- Period (month/year match)
- Status (BALANCED or NEEDS_REVIEW)

### Step 2: Execute Query

Use the `azure-sql-treasurer` MCP tools to run the query:
- `mcp__plugin_data_sbcounty__sql_execute_query` for SELECT queries

Example query:
```sql
SELECT
  h.department_name,
  h.bank_type,
  h.period_start,
  h.period_end,
  h.status,
  h.total_discrepancies,
  h.reconciled_date,
  h.report_path
FROM banking.statement_reconciliation_history h
WHERE 1=1
  -- Apply filters as needed
ORDER BY h.reconciled_date DESC
```

### Step 3: Present Results

Format as a readable table:

| Department | Bank | Period | Status | Discrepancies | Reconciled On |
|-----------|------|--------|--------|---------------|---------------|
| ACR | WF | Jan 2026 | BALANCED | 0 | 2026-02-06 |
| TAX | BofA | Jan 2026 | NEEDS_REVIEW | 2 | 2026-02-06 |

### Step 4: Drill-Down Options

If the user asks about a specific reconciliation, query the details table:
```sql
SELECT
  d.comparison_date,
  d.statement_value,
  d.http_value,
  d.difference,
  d.classification
FROM banking.statement_reconciliation_details d
WHERE d.history_id = @historyId
ORDER BY d.comparison_date
```

### Step 5: Highlight Issues

Flag any departments with unresolved NEEDS_REVIEW status. Offer:
- "Run /review-reconciliation to have Claude analyze the discrepancies"
- "Run /reconcile to re-process with updated documents"

### Step 6: Completeness Check

If a period is specified, show a completeness summary:
- Total departments expected
- Departments reconciled
- Departments pending
- Departments with issues
