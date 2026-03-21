#!/bin/bash
set -euo pipefail

# ============================================================
# PII Scrubber — UserPromptSubmit Hook (v2: redact-cli powered)
#
# Intercepts user prompts BEFORE Claude sees them.
# Uses redact-cli (Rust/ONNX BERT) for ML-powered PII detection.
# Falls back to regex if redact-cli unavailable.
# ============================================================

input=$(cat)
user_prompt=$(echo "$input" | jq -r '.user_prompt // empty')

if [ -z "$user_prompt" ]; then
  exit 0
fi

# -----------------------------------------------------------
# STRATEGY: Try redact-cli first, fall back to regex
# -----------------------------------------------------------

REDACT_CLI="${REDACT_CLI_PATH:-$(command -v redact-cli 2>/dev/null || echo "")}"

if [ -n "$REDACT_CLI" ] && [ -x "$REDACT_CLI" ]; then
  # =============================================
  # TIER 1: redact-cli (Rust + ONNX BERT NER)
  # =============================================

  scrubbed=$(echo "$user_prompt" | "$REDACT_CLI" anonymize \
    --strategy replace \
    --replacement "[REDACTED]" 2>/dev/null) || scrubbed=""

  if [ -n "$scrubbed" ] && [ "$scrubbed" != "$user_prompt" ]; then
    context_msg="⚠️ PII DETECTED AND SCRUBBED via redact-cli (ML+patterns). The user's original prompt contained sensitive data that has been replaced with [REDACTED]. IMPORTANT: Do NOT ask the user to re-share redacted information. Do NOT attempt to guess or reconstruct redacted values. Treat all [REDACTED] tokens as permanent redactions. Scrubbed prompt: ${scrubbed}"

    jq -n --arg ctx "$context_msg" '{
      "hookSpecificOutput": {
        "additionalContext": $ctx
      }
    }'
    exit 0
  fi
fi

# =============================================
# TIER 2: Regex fallback (bash-native)
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
if echo "$scrubbed" | grep -qE '[0-9]{3} [0-9]{2} [0-9]{4}'; then
  scrubbed=$(echo "$scrubbed" | sed -E 's/[0-9]{3} [0-9]{2} [0-9]{4}/[REDACTED-SSN]/g')
  if [[ ! " ${found_types[*]} " =~ " SSN " ]]; then
    found_types+=("SSN")
  fi
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

context_msg="⚠️ PII DETECTED AND SCRUBBED via regex fallback. The user's original prompt contained: ${types_list}. All PII replaced with [REDACTED-*]. IMPORTANT: Do NOT ask the user to re-share redacted information. Install redact-cli for ML-powered detection (names, addresses, orgs). Scrubbed prompt: ${scrubbed}"

jq -n --arg ctx "$context_msg" '{
  "hookSpecificOutput": {
    "additionalContext": $ctx
  }
}'

exit 0
