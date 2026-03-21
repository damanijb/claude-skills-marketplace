# Directory Structure

## Network Share Layout

Bank statements are stored on a network share with this hierarchy:

```
/Volumes/Shared/Banking/Bank Statements/
└── {Year}/
    └── {Month} {Year}/
        ├── {Department}/
        │   ├── {Statement PDF}
        │   ├── {HTTP Document PDF}
        │   └── {Reconciliation Reports}  (generated)
        ├── {Department}/
        │   └── ...
        └── ...
```

### Example

```
/Volumes/Shared/Banking/Bank Statements/
└── 2026/
    └── January 2026/
        ├── ACR/
        │   ├── WF  Jan 26 3163 Pt 1.pdf
        │   ├── WF  Jan 26 3163 Pt 2.pdf
        │   ├── WF  Jan 26 3163 http.pdf
        │   ├── ACR 3163 Jan 26 Reconciliation BALANCED 2026-02-06.txt
        │   └── ACR 3163 Jan 26 Reconciliation BALANCED 2026-02-06.xlsx
        ├── TAX/
        │   ├── BofA 50090 Jan 26.pdf
        │   ├── 50090 Jan 26 http.pdf
        │   └── ...
        └── PW/
            ├── WF  Jan 26 4521.pdf
            ├── WF  Jan 26 4521 http.pdf
            └── ...
```

## File Identification Rules

### Statement PDFs
- Wells Fargo: Filename contains "WF" and does NOT contain "http"
- Bank of America: Filename contains "BofA" or starts with account number (e.g., "50090")
- May be multi-part: "Pt 1", "Pt 2" in filename

### HTTP Documents
- Filename contains "http" (case-insensitive)
- These are scanned PDFs requiring OCR before parsing
- One HTTP document per department per month

### Generated Reports
- Text reports: `.txt` extension with "Reconciliation" in filename
- Excel reports: `.xlsx` extension with "Reconciliation" in filename
- Include status in filename: "BALANCED" or "NEEDS_REVIEW"
- Include generation date: YYYY-MM-DD format

## Department Codes

Common department abbreviations used as folder names:

| Code | Department |
|------|-----------|
| ACR | Auditor-Controller-Recorder |
| TAX | Tax Collector |
| REC | Recorder |
| PW | Public Works |
| SHERIFF | Sheriff's Department |
| DA | District Attorney |
| PROB | Probation |
| HR | Human Resources |
| ISD | Information Services |

## Cowork Access

In Cowork, the network share must be selected by the user via the directory picker. The selected folder is mounted into the VM at the Cowork workspace path.

If the user selects `/Volumes/Shared/Banking/Bank Statements`, the full hierarchy is accessible. If they select a specific month folder, only that month's departments are available.
