# Bank Statement PDF Formats

## Wells Fargo Statement Format

### Filename Patterns
- `WF {Month} {Year} {Account} Pt {N}.pdf` (multi-part)
- `WF {Month} {Year} {Account}.pdf` (single part)
- Example: `WF  Jul 25 3163 Pt 1.pdf`

### PDF Structure

**Page Header:**
- Bank name: "WELLS FARGO BANK"
- Account number
- Statement period dates

**Transaction Section:**
Transactions are listed chronologically, grouped by date:

```
DATE        DESCRIPTION                          AMOUNT
01/02       ACH CREDIT - PAYROLL DEPT ABC       50,000.00
01/02       WIRE TRANSFER OUT                   -25,000.00
            Daily Balance: $1,234,567.89
```

**Key Parsing Patterns:**
- Date format: MM/DD
- Amounts: Comma-separated with 2 decimal places
- Debits may show negative sign or be in a separate column
- Daily balance line follows each date group
- Continuation lines (no date) belong to previous transaction

**Summary Section:**
- Opening/closing balances
- Total debits and credits
- Number of transactions

### Multi-Part Statement Handling
- Part numbers appear in filename (Pt 1, Pt 2)
- Each part covers a portion of the month
- Combine all parts before reconciliation
- Ensure no date overlap between parts

## Bank of America Statement Format

### Filename Patterns
- `BofA {Account} {Month} {Year}.pdf`
- `{Account} {Month} {Year}.pdf` (account number like 50090)
- Example: `BofA 50090 Jan 25.pdf`

### PDF Structure

**Page Header:**
- "Bank of America" or "BofA" identifier
- Account number
- Statement period

**Transaction Section:**
Transactions listed with ending balance:

```
Date    Description              Debits      Credits     Balance
01/02   INCOMING WIRE           -           50,000.00   1,284,567.89
01/02   CHECK #1234             5,000.00    -           1,279,567.89
```

**Key Parsing Patterns:**
- Date format: MM/DD
- Separate debit and credit columns
- Running balance in rightmost column
- Pending transactions marked with "PENDING" flag

**Summary Section:**
- Beginning and ending balances
- Total deposits and withdrawals

## HTTP Reconciliation Document Format

### Overview
HTTP documents are scanned PDFs from the county's internal banking system. They require OCR processing before parsing.

### Wells Fargo HTTP Format
After OCR, the document contains:
- Daily transaction summaries
- Debit and credit totals per day
- Account identification information
- Dates align directly with statement dates

### Bank of America HTTP Format
After OCR, the document contains:
- Daily ending balances
- Transaction descriptions
- **Dates are shifted forward 1 day** relative to statement (HTTP Jan 3 = Statement Jan 2)
- May contain additional columns not present in statement

### OCR Quality Considerations
- Scanned documents may have OCR artifacts
- Amount parsing must handle common OCR errors:
  - `l` misread as `1`
  - `O` misread as `0`
  - Comma/period confusion
  - Merged or split columns
- Always cross-validate OCR totals against sub-amounts
