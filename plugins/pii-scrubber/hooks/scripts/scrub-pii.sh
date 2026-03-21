#!/bin/bash
set -euo pipefail

# ============================================================
# PII Scrubber — UserPromptSubmit Hook
#
# Two responsibilities:
#   1. Scan the user's typed text for PII
#   2. Detect @-attached files, pre-scan their content,
#      and BLOCK if PII is found (@ bypasses PostToolUse)
#
# If a file attachment has PII, we block (exit 2) with guidance
# to use "Read /path/to/file" instead — that path goes through
# the PostToolUse hook which scrubs the output.
#
# Tier 1: Presidio (spaCy NER + treasury patterns)
# Tier 2: Regex fallback (bash-native)
# ============================================================

input=$(cat)
user_prompt=$(echo "$input" | jq -r '.user_prompt // empty')

if [ -z "$user_prompt" ]; then
  exit 0
fi

PRESIDIO_SCRIPT="${CLAUDE_PLUGIN_ROOT}/hooks/scripts/scrub-presidio.py"

# =============================================================
# STEP 1: Check for file paths in the prompt (@-attached files)
# Claude Code uses @/path/to/file syntax which injects content
# directly — no tool call, no PostToolUse hook. We must catch
# PII here or it reaches the API unredacted.
# =============================================================

scan_file_for_pii() {
  local fpath="$1"
  local file_text=""

  if [ ! -f "$fpath" ]; then
    return 1
  fi

  # Extract text based on file type
  case "$fpath" in
    *.pdf)
      file_text=$(python3 -c "
import sys
text = ''
# Try pymupdf first (fastest)
try:
    import fitz
    doc = fitz.open(sys.argv[1])
    for page in doc:
        t = page.get_text()
        if t.strip():
            text += t
except ImportError:
    pass

# Try pdfplumber
if not text:
    try:
        import pdfplumber
        with pdfplumber.open(sys.argv[1]) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t
    except ImportError:
        pass

# OCR fallback for scanned/image PDFs
if not text:
    try:
        from pdf2image import convert_from_path
        import pytesseract
        images = convert_from_path(sys.argv[1], first_page=1, last_page=3)
        for img in images:
            text += pytesseract.image_to_string(img)
    except ImportError:
        pass

if text:
    print(text)
" "$fpath" 2>/dev/null) || file_text=""
      ;;
    *.csv|*.txt|*.tsv|*.log|*.json|*.xml)
      file_text=$(head -500 "$fpath" 2>/dev/null) || file_text=""
      ;;
    *.xlsx|*.xls)
      file_text=$(python3 -c "
import sys
try:
    import openpyxl
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
    for ws in wb.worksheets:
        for row in ws.iter_rows(max_row=200, values_only=True):
            print(' '.join(str(c) for c in row if c is not None))
except:
    pass
" "$fpath" 2>/dev/null) || file_text=""
      ;;
  esac

  if [ -z "$file_text" ]; then
    return 1
  fi

  # Scan with Presidio first
  if [ -f "$PRESIDIO_SCRIPT" ] && command -v python3 &>/dev/null; then
    result=$(echo "$file_text" | python3 "$PRESIDIO_SCRIPT" 2>/dev/null) || result=""
    if [ -n "$result" ]; then
      types=$(echo "$result" | jq -r '.types | join(", ")' 2>/dev/null)
      if [ -n "$types" ]; then
        echo "$types"
        return 0
      fi
    fi
  fi

  # Regex fallback for file scanning
  local found=false
  if echo "$file_text" | grep -qE '(4[0-9]{3}|5[1-5][0-9]{2}|3[47][0-9]{2}|6011)[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{1,7}'; then
    found=true
  fi
  if echo "$file_text" | grep -qE '[0-9]{3}-[0-9]{2}-[0-9]{4}'; then
    found=true
  fi
  if echo "$file_text" | grep -qiE '(account|acct)[# :.-]*[0-9]{6,17}'; then
    found=true
  fi
  if echo "$file_text" | grep -qE '(^|[^0-9])(0[1-9]|[12][0-9]|3[0-2])[0-9]{7}([^0-9]|$)'; then
    found=true
  fi

  if $found; then
    echo "credit card, SSN, account number, or routing number (regex)"
    return 0
  fi

  return 1
}

# Extract file paths from the prompt
# Handles spaces in filenames by matching from / or ~ to known extensions
# Catches: @/Users/djb/Downloads/September Statement.pdf, ~/docs/file.csv
file_paths=$(echo "$user_prompt" | grep -oE '((/[^@]+|~[^@]+)\.(pdf|csv|xlsx|xls|txt|tsv|doc|docx|json|xml))' 2>/dev/null | head -5) || file_paths=""

if [ -n "$file_paths" ]; then
  while IFS= read -r fpath; do
    # Expand ~ if present
    fpath="${fpath/#\~/$HOME}"

    pii_types=$(scan_file_for_pii "$fpath" 2>/dev/null) || continue

    if [ -n "$pii_types" ]; then
      # BLOCK the submission — PII in attached file
      basename_f=$(basename "$fpath")
      cat >&2 <<EOF
⚠️  PII DETECTED in attached file: ${basename_f}

Detected: ${pii_types}

File attachments (@) bypass the PII scrubber because content is
injected directly into the conversation without a tool call.

Instead, ask Claude to read the file:
  → "Read ${fpath} and tell me about it"

The PostToolUse hook will automatically scrub PII from the
Read tool's output before Claude processes it.
EOF
      exit 2
    fi
  done <<< "$file_paths"
fi

# =============================================================
# STEP 2: Scan the typed text itself for PII
# =============================================================

# Presidio
if [ -f "$PRESIDIO_SCRIPT" ] && command -v python3 &>/dev/null; then
  result=$(echo "$user_prompt" | python3 "$PRESIDIO_SCRIPT" 2>/dev/null) || result=""

  if [ -n "$result" ]; then
    scrubbed=$(echo "$result" | jq -r '.scrubbed' 2>/dev/null)
    types=$(echo "$result" | jq -r '.types | join(", ")' 2>/dev/null)
    context_msg="⚠️ PII DETECTED AND SCRUBBED via Presidio (NER+patterns): ${types}. IMPORTANT: Do NOT ask the user to re-share redacted information. Do NOT attempt to guess or reconstruct redacted values. Treat all redacted tokens as permanent. Scrubbed prompt: ${scrubbed}"
    jq -n --arg ctx "$context_msg" '{"hookSpecificOutput":{"additionalContext":$ctx}}'
    exit 0
  fi
fi

# Regex fallback for typed text
found_types=()
scrubbed="$user_prompt"

# --- ABA Routing Numbers ---
if echo "$scrubbed" | grep -qE '(^|[^0-9])(0[1-9]|[12][0-9]|3[0-2])[0-9]{7}([^0-9]|$)'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(^|[^0-9])(0[1-9]|[12][0-9]|3[0-2])[0-9]{7}([^0-9]|$)/\1[REDACTED-ROUTING]\3/g')
  found_types+=("ABA routing number")
fi

# --- Bank Account Numbers (labeled) ---
if echo "$scrubbed" | grep -qiE '(account|acct)[# :.-]*[0-9]{6,17}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(account|acct|Account|Acct|ACCOUNT|ACCT)[# :.-]*[0-9]{6,17}/\1 [REDACTED-ACCT]/gI')
  found_types+=("bank account number")
fi

# --- CUSIP ---
if echo "$scrubbed" | grep -qiE 'cusip'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(^|[^A-Za-z0-9])([0-9]{3}[A-Za-z0-9]{6})([^A-Za-z0-9]|$)/\1[REDACTED-CUSIP]\3/g')
  found_types+=("CUSIP identifier")
fi

# --- SWIFT/BIC ---
if echo "$scrubbed" | grep -qiE '(swift|bic)[: ]*[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(swift|bic|SWIFT|BIC)[: ]*[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?/\1 [REDACTED-SWIFT]/gI')
  found_types+=("SWIFT/BIC code")
fi

# --- Wire Transfer Reference ---
if echo "$scrubbed" | grep -qiE '(wire|transfer|ref)[# :.-]*[A-Z0-9]{10,20}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(wire|transfer|ref|Wire|Transfer|Ref)[# :.-]*[A-Z0-9]{10,20}/\1 [REDACTED-WIRE-REF]/gI')
  found_types+=("wire transfer reference")
fi

# --- SSN ---
if echo "$scrubbed" | grep -qE '[0-9]{3}-[0-9]{2}-[0-9]{4}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[0-9]{3}-[0-9]{2}-[0-9]{4}/[REDACTED-SSN]/g')
  found_types+=("SSN")
fi

# --- Credit Card ---
if echo "$scrubbed" | grep -qE '(4[0-9]{3}|5[1-5][0-9]{2}|3[47][0-9]{2}|6011)[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{1,7}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(4[0-9]{3}|5[1-5][0-9]{2}|3[47][0-9]{2}|6011)[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{1,7}/[REDACTED-CC]/g')
  found_types+=("credit card number")
fi

# --- Email ---
if echo "$scrubbed" | grep -qiE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[REDACTED-EMAIL]/g')
  found_types+=("email address")
fi

# --- Phone ---
if echo "$scrubbed" | grep -qE '(\+?1[- ]?)?\(?[0-9]{3}\)?[- .][0-9]{3}[- .][0-9]{4}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(\+?1[- ]?)?\(?[0-9]{3}\)?[- .][0-9]{3}[- .][0-9]{4}/[REDACTED-PHONE]/g')
  found_types+=("phone number")
fi

# --- IP Addresses ---
if echo "$scrubbed" | grep -qE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[REDACTED-IP]/g')
  found_types+=("IP address")
fi

# --- Date of Birth ---
if echo "$scrubbed" | grep -qE '(0[1-9]|1[0-2])[/-](0[1-9]|[12][0-9]|3[01])[/-](19|20)[0-9]{2}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(0[1-9]|1[0-2])[/-](0[1-9]|[12][0-9]|3[01])[/-](19|20)[0-9]{2}/[REDACTED-DOB]/g')
  found_types+=("date of birth")
fi

if [ ${#found_types[@]} -eq 0 ]; then
  exit 0
fi

types_list=$(printf '%s, ' "${found_types[@]}" | sed 's/, $//')

context_msg="⚠️ PII DETECTED AND SCRUBBED via regex: ${types_list}. All PII replaced with [REDACTED-*]. IMPORTANT: Do NOT ask the user to re-share redacted information. Scrubbed prompt: ${scrubbed}"

jq -n --arg ctx "$context_msg" '{"hookSpecificOutput":{"additionalContext":$ctx}}'

exit 0
