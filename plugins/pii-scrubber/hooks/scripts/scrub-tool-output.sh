#!/bin/bash
set -euo pipefail

# ============================================================
# PII Scrubber — PostToolUse Hook
# Intercepts tool OUTPUT after execution but before Claude
# processes the result. This catches PII from file reads,
# bash output, and other tool results.
#
# Critical for bank statement reconciliation:
# Claude reads a PDF → this hook strips account numbers
# from the output → Claude only sees [REDACTED-ACCT]
# ============================================================

# Read hook input from stdin
input=$(cat)

# Get the tool output content
# PostToolUse receives "tool_response" (object), not "tool_output"
# Convert the response object to string for scanning
tool_output=$(echo "$input" | jq -r '.tool_response // empty | if type == "object" then tostring else . end')
tool_name=$(echo "$input" | jq -r '.tool_name // "unknown"')

if [ -z "$tool_output" ]; then
  exit 0
fi

found_types=()
scrubbed="$tool_output"

# -----------------------------------------------------------
# FINANCIAL / TREASURY PATTERNS (most critical for tool output)
# -----------------------------------------------------------

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
if echo "$scrubbed" | grep -qiE '(cusip|CUSIP)[: ]*[A-Za-z0-9]{9}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/([Cc][Uu][Ss][Ii][Pp])[: ]*[A-Za-z0-9]{9}/\1 [REDACTED-CUSIP]/g')
  found_types+=("CUSIP identifier")
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

# -----------------------------------------------------------
# OUTPUT
# -----------------------------------------------------------

if [ ${#found_types[@]} -eq 0 ]; then
  exit 0
fi

types_list=$(printf '%s, ' "${found_types[@]}" | sed 's/, $//')

# For PostToolUse, we replace the tool output with scrubbed version
# and add context about what was redacted
jq -n \
  --arg scrubbed "$scrubbed" \
  --arg types "$types_list" \
  --arg tool "$tool_name" \
  '{
    "hookSpecificOutput": {
      "additionalContext": ("⚠️ PII SCRUBBED FROM TOOL OUTPUT [" + $tool + "]: Detected " + $types + ". All sensitive values replaced with [REDACTED-*] tokens. The data above has been sanitized. Do NOT attempt to re-read the source to get unscrubbed data.")
    }
  }'

exit 0
