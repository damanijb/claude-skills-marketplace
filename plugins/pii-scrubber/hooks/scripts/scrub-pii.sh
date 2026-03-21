#!/bin/bash
set -euo pipefail

# ============================================================
# PII Scrubber — UserPromptSubmit Hook
# Intercepts user prompts BEFORE Claude sees them.
# Replaces sensitive patterns with [REDACTED-*] tokens.
#
# Treasury-enhanced: includes bank accounts, routing numbers,
# CUSIPs, and SWIFT codes for government finance workflows.
# ============================================================

# Read hook input from stdin
input=$(cat)
user_prompt=$(echo "$input" | jq -r '.user_prompt // empty')

if [ -z "$user_prompt" ]; then
  exit 0
fi

# Track what was found
found_types=()
scrubbed="$user_prompt"

# -----------------------------------------------------------
# FINANCIAL / TREASURY PATTERNS
# -----------------------------------------------------------

# --- ABA Routing Numbers: 9 digits starting with 01-32 (Fed districts) ---
# Match when preceded by whitespace/start and followed by whitespace/end (macOS sed has no \b)
if echo "$scrubbed" | grep -qE '(^|[^0-9])(0[1-9]|[12][0-9]|3[0-2])[0-9]{7}([^0-9]|$)'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(^|[^0-9])(0[1-9]|[12][0-9]|3[0-2])[0-9]{7}([^0-9]|$)/\1[REDACTED-ROUTING]\3/g')
  found_types+=("ABA routing number")
fi

# --- Bank Account Numbers: labeled patterns ---
# Matches "account" or "acct" followed by separators and 6-17 digit numbers
if echo "$scrubbed" | grep -qiE '(account|acct)[# :.-]*[0-9]{6,17}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(account|acct|Account|Acct|ACCOUNT|ACCT)[# :.-]*[0-9]{6,17}/\1 [REDACTED-ACCT]/gI')
  found_types+=("bank account number")
fi

# --- CUSIP: 9-char alphanumeric security identifier ---
# Match near the word "cusip" (within ~50 chars) or standalone 6-alpha + 2-alphanum + 1-check pattern
# Common in portfolio data: "CUSIP 912828YK0" or "CUSIP for the note is 912828YK0"
if echo "$scrubbed" | grep -qiE 'cusip'; then
  # Replace 9-char alphanum tokens that appear after "cusip" context (allowing words between)
  scrubbed=$(echo "$scrubbed" | sed -E 's/(^|[^A-Za-z0-9])([0-9]{3}[A-Za-z0-9]{6})([^A-Za-z0-9]|$)/\1[REDACTED-CUSIP]\3/g')
  found_types+=("CUSIP identifier")
fi

# --- SWIFT/BIC Code: 8 or 11 uppercase alpha chars ---
if echo "$scrubbed" | grep -qiE '(swift|bic|SWIFT|BIC)[: ]*[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(swift|bic|SWIFT|BIC)[: ]*[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?/\1 [REDACTED-SWIFT]/gI')
  found_types+=("SWIFT/BIC code")
fi

# --- Wire Transfer Reference Numbers ---
if echo "$scrubbed" | grep -qiE '(wire|transfer|ref)[# :.-]*[A-Z0-9]{10,20}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(wire|transfer|ref|Wire|Transfer|Ref)[# :.-]*[A-Z0-9]{10,20}/\1 [REDACTED-WIRE-REF]/gI')
  found_types+=("wire transfer reference")
fi

# -----------------------------------------------------------
# STANDARD PII PATTERNS
# -----------------------------------------------------------

# --- SSN: 123-45-6789 or 123 45 6789 ---
if echo "$scrubbed" | grep -qE '[0-9]{3}-[0-9]{2}-[0-9]{4}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[0-9]{3}-[0-9]{2}-[0-9]{4}/[REDACTED-SSN]/g')
  found_types+=("SSN")
fi
if echo "$scrubbed" | grep -qE '[0-9]{3} [0-9]{2} [0-9]{4}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[0-9]{3} [0-9]{2} [0-9]{4}/[REDACTED-SSN]/g')
  if [[ ! " ${found_types[*]} " =~ " SSN " ]]; then
    found_types+=("SSN")
  fi
fi

# --- Credit Card: Visa, MC, Amex, Discover with separators ---
if echo "$scrubbed" | grep -qE '(4[0-9]{3}|5[1-5][0-9]{2}|3[47][0-9]{2}|6011)[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{1,7}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(4[0-9]{3}|5[1-5][0-9]{2}|3[47][0-9]{2}|6011)[- ][0-9]{4}[- ][0-9]{4}[- ][0-9]{1,7}/[REDACTED-CC]/g')
  found_types+=("credit card number")
fi

# --- Email addresses ---
if echo "$scrubbed" | grep -qiE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[REDACTED-EMAIL]/g')
  found_types+=("email address")
fi

# --- US Phone numbers ---
if echo "$scrubbed" | grep -qE '(\+?1[- ]?)?\(?[0-9]{3}\)?[- .][0-9]{3}[- .][0-9]{4}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(\+?1[- ]?)?\(?[0-9]{3}\)?[- .][0-9]{3}[- .][0-9]{4}/[REDACTED-PHONE]/g')
  found_types+=("phone number")
fi

# --- IP Addresses (IPv4) ---
if echo "$scrubbed" | grep -qE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[REDACTED-IP]/g')
  found_types+=("IP address")
fi

# --- Date of Birth patterns: MM/DD/YYYY, MM-DD-YYYY ---
if echo "$scrubbed" | grep -qE '(0[1-9]|1[0-2])[/-](0[1-9]|[12][0-9]|3[01])[/-](19|20)[0-9]{2}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/(0[1-9]|1[0-2])[/-](0[1-9]|[12][0-9]|3[01])[/-](19|20)[0-9]{2}/[REDACTED-DOB]/g')
  found_types+=("date of birth")
fi

# -----------------------------------------------------------
# OUTPUT
# -----------------------------------------------------------

# If no PII found, exit cleanly
if [ ${#found_types[@]} -eq 0 ]; then
  exit 0
fi

# Build the list of found types
types_list=$(printf '%s, ' "${found_types[@]}" | sed 's/, $//')

# Build the additional context message
context_msg="⚠️ PII DETECTED AND SCRUBBED. The user's original prompt contained: ${types_list}. All PII has been replaced with [REDACTED-*] placeholders. IMPORTANT: Do NOT ask the user to re-share the redacted information. Do NOT attempt to guess or reconstruct redacted values. Treat all [REDACTED-*] tokens as permanent redactions. If the user's request cannot be fulfilled without the redacted data, explain what type of information was redacted and why, and suggest they handle it directly. Scrubbed prompt: ${scrubbed}"

# Output proper JSON using jq for safe escaping
jq -n --arg ctx "$context_msg" '{
  "hookSpecificOutput": {
    "additionalContext": $ctx
  }
}'

exit 0
