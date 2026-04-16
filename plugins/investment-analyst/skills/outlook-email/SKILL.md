---
name: outlook-email
description: "Pull emails from local Microsoft Outlook via Windows COM automation. Use this skill when the user asks to read emails, check Outlook, get messages from a folder, search mail, find emails from a sender, pull recent correspondence, check sent items, or any task involving retrieving email content from their local Outlook client. Also trigger when the user references Outlook folders like Inbox, Sent Items, or custom subfolder names (e.g., 'Earnings Analysis', 'Credit Research') in the context of retrieving information. This skill returns raw plain-text email content for Claude to work with."
version: 1.0.0
---

# Outlook Email Retrieval

Connect to the user's local Microsoft Outlook installation via Windows COM (`win32com.client`) and retrieve emails as plain text for analysis, data extraction, or context gathering.

## Prerequisites

- Microsoft Outlook must be installed and running (or at least configured) on the local Windows machine
- Python `pywin32` package must be available (`pip install pywin32`)

If `pywin32` is not installed, install it before running the script:
```bash
pip install pywin32
```

## How It Works

Use the bundled script at `${CLAUDE_PLUGIN_ROOT}/skills/outlook-email/scripts/fetch_emails.py` to pull emails. The script connects to Outlook's MAPI namespace, navigates to the requested folder, applies filters, and returns structured plain-text output.

## Usage

Run the script via Python with the appropriate arguments:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/outlook-email/scripts/fetch_emails.py" [OPTIONS]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--folder` | Folder path (e.g., `Inbox`, `Sent Items`, `Inbox/Earnings Analysis`) | `Inbox` |
| `--limit` | Maximum number of emails to return | `10` |
| `--from-address` | Filter by sender email or display name (partial match) | — |
| `--subject` | Filter by subject line (partial match) | — |
| `--since` | Only emails after this date (`YYYY-MM-DD`) | — |
| `--before` | Only emails before this date (`YYYY-MM-DD`) | — |
| `--has-attachments` | Only emails with attachments | `false` |
| `--save-attachments` | Save attachments to this directory | — |
| `--output-format` | `text` (default) or `json` | `text` |
| `--list-folders` | List all available folders and exit | — |

### Folder Navigation

- **Top-level folders**: `Inbox`, `Sent Items`, `Drafts`, `Deleted Items`
- **Subfolders**: Use `/` separator — e.g., `Inbox/Earnings Analysis`, `Inbox/Credit Research/Q1 2026`
- The script automatically resolves the default mailbox. If the user has multiple accounts configured, it uses the default delivery account.

### Examples

```bash
# Last 10 inbox emails
python fetch_emails.py

# Emails from a specific subfolder
python fetch_emails.py --folder "Inbox/Earnings Analysis" --limit 20

# Search by sender
python fetch_emails.py --from-address "john.smith" --since 2026-01-01

# Sent items from last quarter with attachments
python fetch_emails.py --folder "Sent Items" --since 2026-01-01 --before 2026-03-31 --has-attachments

# Save attachments to a local directory
python fetch_emails.py --folder "Inbox/Reports" --has-attachments --save-attachments ./attachments

# JSON output for structured processing
python fetch_emails.py --subject "quarterly" --output-format json
```

## Output Format

### Plain Text (default)

Each email is separated by a clear delimiter for readability:

```
========== EMAIL 1 of 5 ==========
From:    John Smith <john.smith@example.com>
To:      Jane Doe <jane.doe@example.com>
CC:      Team <team@example.com>
Date:    2026-03-15 09:30:00
Subject: Q1 Earnings Preview - Regional Banks

[Body]
Plain text content of the email...

[Attachments]
- Q1_Preview.xlsx (245 KB)
- Sector_Notes.pdf (1.2 MB)
=======================================
```

### JSON

Returns a JSON array of email objects with fields: `from`, `to`, `cc`, `date`, `subject`, `body`, `attachments`, `conversation_id`.

## Workflow Integration

This skill is a **data gathering step**. After retrieving emails, Claude can:

- Extract specific data points (dates, figures, names) from the email bodies
- Summarize correspondence threads
- Use email content as context for analysis tasks
- Cross-reference email content with other data sources

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `pywintypes.com_error` | Make sure Outlook is running or has been opened at least once |
| Folder not found | Check exact folder name in Outlook — names are case-sensitive |
| No emails returned | Broaden your date range or check filters |
| Permission dialog | Outlook may prompt to allow programmatic access — click "Allow" |
