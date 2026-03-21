# Database Schema

## Connection

- **Server**: treasurer.database.windows.net
- **Database**: Configured via `azure-sql-treasurer` skill
- **Schema**: `banking`

## Tables

### banking.statement_reconciliation_history

Stores one row per reconciliation run.

| Column | Type | Description |
|--------|------|-------------|
| id | INT IDENTITY | Primary key |
| department_name | NVARCHAR(100) | Department code (e.g., "ACR", "TAX") |
| bank_type | NVARCHAR(20) | "wells-fargo" or "bofa" |
| account_number | NVARCHAR(20) | Bank account number |
| period_start | DATE | Statement period start date |
| period_end | DATE | Statement period end date |
| status | NVARCHAR(20) | "BALANCED" or "NEEDS_REVIEW" |
| total_discrepancies | INT | Number of dates with unexplained differences |
| total_discrepancy_amount | DECIMAL(18,2) | Sum of absolute discrepancy amounts |
| opening_balance | DECIMAL(18,2) | Statement opening balance |
| closing_balance | DECIMAL(18,2) | Statement closing balance |
| total_debits | DECIMAL(18,2) | Sum of all debits |
| total_credits | DECIMAL(18,2) | Sum of all credits |
| report_path | NVARCHAR(500) | Path to the generated report files |
| reconciled_date | DATETIME2 | When the reconciliation was performed |
| reconciled_by | NVARCHAR(100) | User or system that ran the reconciliation |
| notes | NVARCHAR(MAX) | Optional notes or AI review comments |
| created_at | DATETIME2 | Row creation timestamp |

### banking.statement_reconciliation_details

Stores one row per date comparison within a reconciliation.

| Column | Type | Description |
|--------|------|-------------|
| id | INT IDENTITY | Primary key |
| history_id | INT | FK to statement_reconciliation_history.id |
| comparison_date | DATE | The business date being compared |
| statement_value | DECIMAL(18,2) | Value from bank statement (debit total or balance) |
| http_value | DECIMAL(18,2) | Value from HTTP document |
| difference | DECIMAL(18,2) | statement_value - http_value |
| classification | NVARCHAR(50) | "matched", "explained", "unexplained" |
| explanation | NVARCHAR(500) | Explanation if classified as "explained" |
| statement_debit_count | INT | Number of debit transactions on this date (statement) |
| statement_credit_count | INT | Number of credit transactions on this date (statement) |
| http_debit_count | INT | Number of debit transactions on this date (HTTP) |
| http_credit_count | INT | Number of credit transactions on this date (HTTP) |

## Common Queries

### Recent reconciliations for a department
```sql
SELECT * FROM banking.statement_reconciliation_history
WHERE department_name = 'ACR'
ORDER BY reconciled_date DESC
```

### Unresolved discrepancies for a period
```sql
SELECT h.department_name, h.bank_type, d.comparison_date,
       d.statement_value, d.http_value, d.difference
FROM banking.statement_reconciliation_history h
JOIN banking.statement_reconciliation_details d ON h.id = d.history_id
WHERE h.period_start >= '2026-01-01'
  AND d.classification = 'unexplained'
ORDER BY h.department_name, d.comparison_date
```

### Processing completeness for a month
```sql
SELECT
  department_name,
  status,
  reconciled_date
FROM banking.statement_reconciliation_history
WHERE period_start = '2026-01-01'
ORDER BY department_name
```
