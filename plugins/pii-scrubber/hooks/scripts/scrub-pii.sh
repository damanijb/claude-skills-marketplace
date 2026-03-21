#!/bin/bash
set -euo pipefail

# ============================================================
# PII Scrubber — UserPromptSubmit Hook
#
# Intercepts user prompts BEFORE Claude sees them.
# Tier 1: Presidio (Python, spaCy NER + treasury patterns)
# Tier 2: Regex fallback (bash-native, no dependencies)
#
# Dependencies: pip install presidio-analyzer presidio-anonymizer
# ============================================================

input=$(cat)
user_prompt=$(echo "$input" | jq -r '.user_prompt // empty')

if [ -z "$user_prompt" ]; then
  exit 0
fi

PRESIDIO_SCRIPT="$CLAUDE_PLUGIN_ROOT/hooks/scripts/scrub-presidio.py"

# =============================================
# TIER 1: Presidio (spaCy NER + custom patterns)
# Catches: SSN, phone, email, dates, routing,
# CUSIP, SWIFT, wire refs, bank accounts
# =============================================
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

# =============================================
# TIER 2: Regex fallback (no Python required)
# =============================================

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
