"""
Fetch emails from local Microsoft Outlook via Windows COM automation.
Returns plain-text or JSON output for use by Claude.
"""

import argparse
import json
import os
import sys
from datetime import datetime


def connect_outlook():
    """Connect to Outlook via COM and return the MAPI namespace."""
    try:
        import win32com.client
    except ImportError:
        print("ERROR: pywin32 is not installed. Run: pip install pywin32", file=sys.stderr)
        sys.exit(1)

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        return namespace
    except Exception as e:
        print(f"ERROR: Could not connect to Outlook: {e}", file=sys.stderr)
        print("Make sure Outlook is installed and has been opened at least once.", file=sys.stderr)
        sys.exit(1)


def resolve_folder(namespace, folder_path):
    """
    Navigate to a folder by path string.

    Top-level folders map to Outlook's default folder constants:
        Inbox=6, Sent Items=5, Drafts=16, Deleted Items=3, Outbox=4, Junk=23
    Subfolders are resolved by walking the folder tree with '/'.
    """
    KNOWN_FOLDERS = {
        "inbox": 6,
        "sent items": 5,
        "sent": 5,
        "drafts": 16,
        "deleted items": 3,
        "outbox": 4,
        "junk email": 23,
        "junk": 23,
    }

    parts = [p.strip() for p in folder_path.split("/") if p.strip()]
    if not parts:
        parts = ["Inbox"]

    root_name = parts[0].lower()

    # Try default folder constants first
    if root_name in KNOWN_FOLDERS:
        try:
            folder = namespace.GetDefaultFolder(KNOWN_FOLDERS[root_name])
        except Exception:
            print(f"ERROR: Could not access default folder '{parts[0]}'", file=sys.stderr)
            sys.exit(1)
    else:
        # Try to find it as a subfolder of the default store's root
        try:
            root = namespace.DefaultStore.GetRootFolder()
            folder = root.Folders[parts[0]]
        except Exception:
            print(f"ERROR: Folder '{parts[0]}' not found. Check the exact name in Outlook.", file=sys.stderr)
            sys.exit(1)

    # Navigate into subfolders
    for subfolder_name in parts[1:]:
        try:
            folder = folder.Folders[subfolder_name]
        except Exception:
            print(f"ERROR: Subfolder '{subfolder_name}' not found under '{folder.Name}'.", file=sys.stderr)
            available = [f.Name for f in folder.Folders]
            if available:
                print(f"Available subfolders: {', '.join(available)}", file=sys.stderr)
            sys.exit(1)

    return folder


def format_size(size_bytes):
    """Format byte count to human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def extract_email(item):
    """Extract relevant fields from an Outlook MailItem."""
    try:
        # Get sender info
        sender = ""
        try:
            sender_name = item.SenderName or ""
            sender_email = item.SenderEmailAddress or ""
            if sender_name and sender_email and sender_name != sender_email:
                sender = f"{sender_name} <{sender_email}>"
            else:
                sender = sender_name or sender_email
        except Exception:
            sender = "(unknown sender)"

        # Get recipients
        to_list = ""
        cc_list = ""
        try:
            to_list = item.To or ""
            cc_list = item.CC or ""
        except Exception:
            pass

        # Get date
        date_str = ""
        try:
            received = item.ReceivedTime
            date_str = received.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            try:
                sent = item.SentOn
                date_str = sent.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                date_str = "(unknown date)"

        # Get subject and body
        subject = ""
        body = ""
        try:
            subject = item.Subject or "(no subject)"
        except Exception:
            subject = "(no subject)"

        try:
            body = item.Body or ""
        except Exception:
            body = "(could not read body)"

        # Get attachments
        attachments = []
        try:
            for i in range(1, item.Attachments.Count + 1):
                att = item.Attachments.Item(i)
                attachments.append({
                    "name": att.FileName,
                    "size": att.Size,
                    "size_display": format_size(att.Size),
                })
        except Exception:
            pass

        # Conversation ID for threading
        conversation_id = ""
        try:
            conversation_id = item.ConversationID or ""
        except Exception:
            pass

        return {
            "from": sender,
            "to": to_list,
            "cc": cc_list,
            "date": date_str,
            "subject": subject,
            "body": body.strip(),
            "attachments": attachments,
            "conversation_id": conversation_id,
        }
    except Exception as e:
        return {"error": str(e)}


def matches_filters(email, args):
    """Check if an email matches the user's filter criteria."""
    if args.from_address:
        from_field = email.get("from", "").lower()
        if args.from_address.lower() not in from_field:
            return False

    if args.subject:
        subj = email.get("subject", "").lower()
        if args.subject.lower() not in subj:
            return False

    if args.since or args.before:
        date_str = email.get("date", "")
        if date_str and date_str != "(unknown date)":
            try:
                email_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if args.since:
                    since_date = datetime.strptime(args.since, "%Y-%m-%d")
                    if email_date < since_date:
                        return False
                if args.before:
                    before_date = datetime.strptime(args.before, "%Y-%m-%d")
                    if email_date >= before_date:
                        return False
            except ValueError:
                pass

    if args.has_attachments:
        if not email.get("attachments"):
            return False

    return True


def save_attachments(item, dest_dir):
    """Save attachments from an Outlook MailItem to a directory."""
    os.makedirs(dest_dir, exist_ok=True)
    saved = []
    try:
        for i in range(1, item.Attachments.Count + 1):
            att = item.Attachments.Item(i)
            filepath = os.path.join(dest_dir, att.FileName)
            # Avoid overwriting
            base, ext = os.path.splitext(filepath)
            counter = 1
            while os.path.exists(filepath):
                filepath = f"{base}_{counter}{ext}"
                counter += 1
            att.SaveAsFile(filepath)
            saved.append(filepath)
    except Exception as e:
        print(f"WARNING: Error saving attachment: {e}", file=sys.stderr)
    return saved


def list_folders(namespace, folder=None, indent=0, max_depth=3):
    """Print available Outlook folders as a tree."""
    if folder is None:
        root = namespace.DefaultStore.GetRootFolder()
        print(f"Mailbox: {namespace.DefaultStore.DisplayName}")
        print("-" * 40)
        for f in root.Folders:
            print(f"  {f.Name} ({f.Items.Count} items)")
            if indent < max_depth:
                list_folders(namespace, f, indent + 1, max_depth)
    else:
        try:
            for f in folder.Folders:
                prefix = "    " * (indent + 1)
                print(f"{prefix}{f.Name} ({f.Items.Count} items)")
                if indent < max_depth:
                    list_folders(namespace, f, indent + 1, max_depth)
        except Exception:
            pass


def format_text(emails, total_count):
    """Format emails as readable plain text."""
    lines = []
    for i, email in enumerate(emails, 1):
        lines.append(f"========== EMAIL {i} of {len(emails)} (total matching: {total_count}) ==========")
        lines.append(f"From:    {email['from']}")
        lines.append(f"To:      {email['to']}")
        if email.get("cc"):
            lines.append(f"CC:      {email['cc']}")
        lines.append(f"Date:    {email['date']}")
        lines.append(f"Subject: {email['subject']}")
        lines.append("")
        lines.append("[Body]")
        lines.append(email["body"])

        if email.get("attachments"):
            lines.append("")
            lines.append("[Attachments]")
            for att in email["attachments"]:
                lines.append(f"- {att['name']} ({att['size_display']})")

        lines.append("=" * 55)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch emails from local Outlook")
    parser.add_argument("--folder", default="Inbox", help="Folder path (e.g., Inbox, Sent Items, Inbox/Subfolder)")
    parser.add_argument("--limit", type=int, default=10, help="Max emails to return")
    parser.add_argument("--from-address", help="Filter by sender (partial match)")
    parser.add_argument("--subject", help="Filter by subject (partial match)")
    parser.add_argument("--since", help="Only emails after this date (YYYY-MM-DD)")
    parser.add_argument("--before", help="Only emails before this date (YYYY-MM-DD)")
    parser.add_argument("--has-attachments", action="store_true", help="Only emails with attachments")
    parser.add_argument("--save-attachments", help="Save attachments to this directory")
    parser.add_argument("--output-format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--scan-limit", type=int, default=0, help="Max items to scan (0 = auto, based on limit)")
    parser.add_argument("--list-folders", action="store_true", help="List available folders and exit")
    args = parser.parse_args()

    namespace = connect_outlook()

    if args.list_folders:
        list_folders(namespace)
        return

    folder = resolve_folder(namespace, args.folder)

    # Get items sorted by received date (most recent first)
    items = folder.Items
    items.Sort("[ReceivedTime]", True)

    # Build DASL restriction for server-side filtering (much faster on large folders)
    restrictions = []
    if args.subject:
        safe_subj = args.subject.replace("'", "''")
        restrictions.append(f"@SQL=\"urn:schemas:httpmail:subject\" LIKE '%{safe_subj}%'")
    if args.since:
        restrictions.append(f"@SQL=\"urn:schemas:httpmail:datereceived\" >= '{args.since}'")
    if args.before:
        restrictions.append(f"@SQL=\"urn:schemas:httpmail:datereceived\" < '{args.before}'")
    if args.has_attachments:
        restrictions.append("@SQL=\"urn:schemas:httpmail:hasattachment\" = 1")

    if restrictions:
        try:
            combined = " AND ".join(restrictions)
            items = items.Restrict(combined)
            items.Sort("[ReceivedTime]", True)
        except Exception:
            # Fall back to client-side filtering if DASL fails
            items = folder.Items
            items.Sort("[ReceivedTime]", True)

    # Scan limit: user-specified or auto-calculated
    if args.scan_limit > 0:
        scan_limit = args.scan_limit
    else:
        scan_limit = max(args.limit * 5, 200)

    results = []
    total_matching = 0
    scanned = 0

    for item in items:
        if scanned >= scan_limit:
            break
        scanned += 1

        # Skip non-mail items (meeting requests, etc.)
        try:
            if item.Class != 43:  # 43 = olMail
                continue
        except Exception:
            continue

        email = extract_email(item)
        if "error" in email:
            continue

        if not matches_filters(email, args):
            continue

        total_matching += 1

        if len(results) < args.limit:
            results.append(email)

            # Save attachments if requested
            if args.save_attachments and email.get("attachments"):
                saved = save_attachments(item, args.save_attachments)
                if saved:
                    email["saved_attachment_paths"] = saved

    if not results:
        print(f"No emails found in '{args.folder}' matching your filters.", file=sys.stderr)
        print(f"(Scanned {scanned} items)", file=sys.stderr)
        sys.exit(0)

    if args.output_format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_text(results, total_matching))


if __name__ == "__main__":
    main()
