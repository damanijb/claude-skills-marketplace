---
name: statement-processor
description: >
  This skill should be used when the user asks to "parse a bank statement",
  "extract transactions from a PDF", "read a Wells Fargo statement",
  "read a BofA statement", "process a statement PDF", or needs guidance
  on how bank statement PDFs are structured and parsed for San Bernardino
  County Treasury reconciliation.
version: 0.1.0
---

# Statement Processor

Parse Wells Fargo and Bank of America bank statement PDFs into structured transaction data for reconciliation.

## Supported Banks

### Wells Fargo
- Statement PDFs contain daily transaction listings with debits and credits
- Transactions are grouped by date with daily subtotals
- Key fields: date, description, amount, running balance
- ACH Returns, Reversals, and Deletes appear as credits but explain debit-side differences
- ZBA (Zero Balance Account) transfers create credit entries not present in HTTP documents

### Bank of America
- Statement PDFs list transactions with ending daily balances
- Transactions include pending items and sweep transfers
- Key fields: date, description, amount, ending balance
- HTTP document dates are shifted back 1 business day relative to statement dates

## Processing Pipeline

1. **PDF Text Extraction** — Use `pdf-parse` to extract raw text from the statement PDF
2. **Bank Detection** — Identify bank type from header text or filename patterns
3. **Transaction Parsing** — Apply bank-specific regex patterns to extract transaction rows
4. **Date Normalization** — Parse dates into ISO format, handle month boundaries
5. **Amount Parsing** — Convert formatted amounts ($1,234.56) to numeric values
6. **Daily Aggregation** — Group transactions by date and compute daily totals
7. **Validation** — Cross-check extracted totals against statement summary section

## Script Usage

### Wells Fargo Statement
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_wf_statement.js "/path/to/statement.pdf"
```

### Bank of America Statement
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_bofa_statement.js "/path/to/statement.pdf"
```

### Wells Fargo HTTP Document (post-OCR)
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_wf_http.js "/path/to/http-content.md"
```

### Bank of America HTTP Document (post-OCR)
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/parse_bofa_http.js "/path/to/http-content.md"
```

All scripts output JSON to stdout with this structure:
```json
{
  "bank": "wells-fargo | bofa",
  "accountNumber": "XXXX1234",
  "periodStart": "2026-01-01",
  "periodEnd": "2026-01-31",
  "openingBalance": 1234567.89,
  "closingBalance": 1234567.89,
  "transactions": [
    {
      "date": "2026-01-02",
      "description": "ACH CREDIT DEPOSIT",
      "amount": 50000.00,
      "type": "credit",
      "balance": 1284567.89
    }
  ],
  "dailyTotals": {
    "2026-01-02": { "debits": 0, "credits": 50000.00, "balance": 1284567.89 }
  }
}
```

## OCR Pipeline

HTTP reconciliation documents are scanned PDFs requiring OCR before parsing.

1. Send the HTTP PDF to the marker-pdf webhook for OCR processing
2. Receive markdown/HTML output with extracted text and tables
3. Parse the OCR output using the appropriate HTTP parser script

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/ocr_webhook.js "/path/to/http-document.pdf"
```

The OCR webhook returns markdown content that is then piped to the HTTP parser.

## Additional Resources

- **`references/bank-formats.md`** — Detailed PDF format documentation per bank
- **`references/ocr-pipeline.md`** — OCR webhook configuration and fallback options
