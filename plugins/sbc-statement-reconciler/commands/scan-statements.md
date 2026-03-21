---
description: Scan network share for bank statement folders and report status
allowed-tools: Read, Bash, Glob, Grep
argument-hint: [month]
---

Scan the bank statements network share and report which departments are ready for processing, already reconciled, or missing files.

## Arguments

- `$1` — Optional month filter (e.g., "January 2026"). If omitted, lists all available months.

The base path is auto-detected by OS:
- **macOS**: `/Volumes/Shared/Banking/Bank Statements/`
- **Windows**: `T:/Data/Shared/Banking/Bank Statements/`

Override with `--path` if needed.

## File Access: Auto-Copy from Network Drives

The script knows where the files live. If running inside Cowork where the network path isn't directly mounted:

1. Use bash to test if the default network path is accessible: `ls "/Volumes/Shared/Banking/Bank Statements/" 2>/dev/null`
2. If accessible, **automatically copy** the target month folder into the Cowork workspace:
   ```bash
   cp -r "/Volumes/Shared/Banking/Bank Statements/2026/January 2026" /path/to/cowork/workspace/
   ```
3. Run the scanner on the local copy.
4. If NOT accessible, inform the user the network drive isn't mounted and ask them to verify.

Do NOT ask the user to copy files manually. Just do it.

## Workflow

1. Run the directory scanner (no path argument needed — it auto-detects):
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/scan_directories.js "$1"
   ```
   Or if running on a local copy in the workspace:
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/scan_directories.js --path "<local-copy-path>" "$1"
   ```

2. Parse the JSON output. Each department entry contains:
   - `department`: Department name (e.g., "ACR", "TAX", "REC")
   - `bank`: Bank type ("wells-fargo" or "bofa")
   - `statementPdf`: Path to statement PDF (null if missing)
   - `httpDocument`: Path to HTTP reconciliation document (null if missing)
   - `existingReports`: Array of existing reconciliation report paths
   - `status`: "ready" | "missing-files" | "already-reconciled"

3. Present results as a formatted table:

   | Department | Bank | Status | Details |
   |-----------|------|--------|---------|
   | ACR | Wells Fargo | Ready | Statement + HTTP found |
   | TAX | BofA | Missing Files | No HTTP document |
   | REC | Wells Fargo | Already Reconciled | Report from 2026-02-06 |

4. Summarize: X departments ready, Y already reconciled, Z missing files.

5. If departments are ready, offer next steps:
   - "Run /reconcile for a single department"
   - "Run /bulk-reconcile to process all ready departments"
