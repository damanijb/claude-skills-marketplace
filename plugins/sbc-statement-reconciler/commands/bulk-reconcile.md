---
description: Reconcile multiple departments sequentially
allowed-tools: Read, Write, Bash, Glob, Grep
argument-hint: <root-path> [month] [--departments dept1,dept2,...]
---

Process multiple departments through the full reconciliation pipeline sequentially. Wraps the /reconcile workflow for batch operations.

## Arguments

- `$1` — Root path to the bank statements directory
- `$2` — Optional month filter (e.g., "January 2026")
- `--departments` — Optional comma-separated list of specific departments to process

## Important Constraint

The OCR webhook cannot handle parallel requests. Process departments **one at a time**, reporting progress after each completion.

## File Access: Auto-Copy from Network Drives

If the root path is outside the Cowork workspace (e.g., a network share):

1. Test if the path is accessible by running `ls` on it via bash.
2. If accessible, **automatically copy** the entire month folder (with all department subfolders) into the workspace:
   ```bash
   cp -r "$NETWORK_PATH" /path/to/cowork/workspace/
   ```
3. Process all departments from the local copy.
4. After ALL departments are processed, **copy all generated reports back** to the original network location in one batch:
   ```bash
   # For each processed department:
   cp /path/to/local/dept/*.txt "$NETWORK_PATH/dept/"
   cp /path/to/local/dept/*.xlsx "$NETWORK_PATH/dept/"
   ```
5. If the path is NOT accessible, inform the user and ask them to verify the network drive is mounted.

Do NOT ask the user to copy files manually. Handle the full round-trip automatically.

## Workflow

### Step 1: Scan for Ready Departments

Auto-copy files if needed (see above), then run the directory scanner:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/scan_directories.js "<local-path>" "$2"
```

Filter results:
- If `--departments` was specified, only include those departments
- Otherwise, include all departments with status "ready"
- Exclude departments already reconciled (unless user explicitly requests re-processing)

### Step 2: Confirm Processing Plan

Present the list of departments to be processed:

| # | Department | Bank | Files Found |
|---|-----------|------|-------------|
| 1 | ACR | Wells Fargo | Statement + HTTP |
| 2 | TAX | BofA | Statement + HTTP |
| 3 | PW | Wells Fargo | Statement + HTTP |

Ask for confirmation before proceeding: "Process these X departments? This may take several minutes due to OCR processing."

### Step 3: Process Each Department

For each department, execute the /reconcile workflow:

1. Parse the statement PDF
2. OCR the HTTP document (sequential — wait for completion)
3. Parse the HTTP content
4. Run reconciliation
5. Generate reports

After each department completes, update progress using the TodoWrite tool:
- Mark completed departments as done
- Show current status (BALANCED / NEEDS_REVIEW)
- Report any errors encountered

If a department fails (OCR timeout, parse error, missing data):
- Log the error
- Continue to the next department
- Include failed departments in the final summary

### Step 4: Copy Results Back to Network Drive

If files were copied from a network drive, batch-copy all generated reports back:
```bash
for dept in ACR TAX PW; do
  cp /path/to/local/$dept/*.txt "$NETWORK_PATH/$dept/"
  cp /path/to/local/$dept/*.xlsx "$NETWORK_PATH/$dept/"
done
```

### Step 5: Final Summary

Present a summary table of all results:

| Department | Bank | Status | Report Path |
|-----------|------|--------|-------------|
| ACR | Wells Fargo | BALANCED | /network/path/ACR/report.xlsx |
| TAX | BofA | NEEDS_REVIEW | /network/path/TAX/report.xlsx |
| PW | Wells Fargo | ERROR | OCR webhook timeout |

Summary statistics:
- X departments processed successfully
- Y balanced, Z need review
- Any failures with error details
- Reports copied back to network share (if applicable)

Offer next steps:
- "Run /review-reconciliation on NEEDS_REVIEW departments"
- "Run /statement-history to see updated history"
