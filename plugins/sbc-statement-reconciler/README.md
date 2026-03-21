# SBC Statement Reconciler

Automate bank statement reconciliation for San Bernardino County Treasury. This plugin converts the Statement App Electron desktop application into a conversational Cowork plugin with slash commands.

## Overview

The plugin processes Wells Fargo and Bank of America PDF statements, performs OCR on HTTP reconciliation documents, compares transaction data, generates Excel and text reports, and uses Claude's native AI capabilities for validation — all through conversational commands.

## Commands

| Command | Description |
|---------|-------------|
| `/scan-statements` | Scan a directory for bank statement folders and report processing status |
| `/parse-statement` | Parse a single bank statement PDF and extract transactions |
| `/reconcile` | Full reconciliation pipeline for one department |
| `/bulk-reconcile` | Process multiple departments sequentially |
| `/statement-history` | Query past reconciliation results from Azure SQL |
| `/review-reconciliation` | AI-powered review and validation of a completed reconciliation |

## Skills

| Skill | Purpose |
|-------|---------|
| `statement-processor` | Bank statement PDF parsing knowledge and pipeline guidance |
| `reconciliation-engine` | Business rules for comparing statement vs HTTP data |

## Setup

### 1. Install Node.js Dependencies

Run the setup script to install required packages:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh
```

Required packages: `pdf-parse`, `exceljs`, `mssql`

### 2. Network Access

| Service | URL | Required For |
|---------|-----|-------------|
| OCR Webhook | `samaritan.tail8478e1.ts.net` | `/reconcile` (HTTP document parsing) |
| Azure SQL | `treasurer.database.windows.net` | `/statement-history`, database saves |

The OCR webhook requires Tailscale VPN connectivity.

### 3. File Access

Select the bank statements directory via the Cowork folder picker. The expected directory structure is documented in `references/directory-structure.md`.

### 4. Database

Database connectivity is handled through the `azure-sql-treasurer` skill already configured in your environment. No additional database setup is needed.

## Usage

### Quick Start

1. Select your bank statements folder in Cowork
2. Run `/scan-statements` to see which departments are ready
3. Run `/reconcile <department-folder>` to process a department
4. Run `/review-reconciliation <report>` for AI validation

### Batch Processing

```
/bulk-reconcile "/path/to/January 2026"
```

### Historical Queries

```
/statement-history ACR "January 2026"
/statement-history --status needs-review
```

## Architecture

Scripts in the `scripts/` directory are compiled from the original Electron app's TypeScript parsers. They run as standalone Node.js processes, accepting file paths as arguments and outputting JSON to stdout.

The `references/` directory contains business rules, bank format documentation, database schemas, and configuration templates that Claude uses for context during reconciliation.

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OCR_WEBHOOK_URL` | Override OCR webhook endpoint | Tailscale marker-pdf URL |

## Integration with Existing Skills

This plugin works alongside:
- **azure-sql-treasurer** — Database queries for history and saves
- **sbc-data-scientist** — PDF extraction and data cleaning
- **portfolio-risk-compliance** — Cross-reference with portfolio positions
