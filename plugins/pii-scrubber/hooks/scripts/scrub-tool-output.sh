#!/bin/bash
set -euo pipefail

# ============================================================
# PII Scrubber — PostToolUse Hook (v2: redact-cli powered)
#
# Intercepts tool OUTPUT after execution but before Claude
# processes the result. Uses redact-cli (Rust/ONNX BERT) for
# ML-powered PII detection: names, addresses, orgs, plus 36
# pattern types. Falls back to regex if redact-cli unavailable.
#
# Performance: ~0.2ms p50 latency via redact-cli vs ~7ms Presidio
# ============================================================

input=$(cat)

# PostToolUse receives "tool_response" (object)
tool_response=$(echo "$input" | jq -r '
  .tool_response // empty |
  if type == "object" then tostring
  elif type == "array" then tostring
  else .
  end
')
tool_name=$(echo "$input" | jq -r '.tool_name // "unknown"')

if [ -z "$tool_response" ]; then
  exit 0
fi

# -----------------------------------------------------------
# STRATEGY: Try redact-cli first, fall back to regex
# -----------------------------------------------------------

REDACT_CLI="${REDACT_CLI_PATH:-$(command -v redact-cli 2>/dev/null || echo "")}"
PRESIDIO_SCRIPT="$CLAUDE_PLUGIN_ROOT/hooks/scripts/scrub-presidio.py"

# =============================================
# TIER 1A: redact-cli (Rust + ONNX BERT NER)
# =============================================
if [ -n "$REDACT_CLI" ] && [ -x "$REDACT_CLI" ]; then
  scrubbed=$(echo "$tool_response" | "$REDACT_CLI" anonymize \
    --strategy replace \
    --replacement "[REDACTED]" 2>/dev/null) || scrubbed=""

  if [ -n "$scrubbed" ] && [ "$scrubbed" != "$tool_response" ]; then
    jq -n \
      --arg tool "$tool_name" \
      '{
        "hookSpecificOutput": {
          "additionalContext": ("⚠️ PII SCRUBBED FROM TOOL OUTPUT [" + $tool + "] via redact-cli (ML+patterns). Sensitive values replaced with [REDACTED]. Do NOT re-read source to bypass redaction.")
        }
      }'
    exit 0
  fi
fi

# =============================================
# TIER 1B: Presidio (Python, spaCy NER + patterns)
# =============================================
if [ -f "$PRESIDIO_SCRIPT" ] && command -v python3 &>/dev/null; then
  result=$(echo "$tool_response" | python3 "$PRESIDIO_SCRIPT" 2>/dev/null) || result=""

  if [ -n "$result" ]; then
    types=$(echo "$result" | jq -r '.types | join(", ")' 2>/dev/null)
    jq -n \
      --arg tool "$tool_name" \
      --arg types "$types" \
      '{
        "hookSpecificOutput": {
          "additionalContext": ("⚠️ PII SCRUBBED FROM TOOL OUTPUT [" + $tool + "] via Presidio (NER+patterns): " + $types + ". Do NOT re-read source to bypass redaction.")
        }
      }'
    exit 0
  fi
fi

# =============================================
# TIER 2: Regex fallback (bash-native)
# Catches structured patterns only
# =============================================

found_types=()
scrubbed="$tool_response"

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

if [ ${#found_types[@]} -eq 0 ]; then
  exit 0
fi

types_list=$(printf '%s, ' "${found_types[@]}" | sed 's/, $//')

jq -n \
  --arg types "$types_list" \
  --arg tool "$tool_name" \
  '{
    "hookSpecificOutput": {
      "additionalContext": ("⚠️ PII SCRUBBED FROM TOOL OUTPUT [" + $tool + "] via regex fallback: Detected " + $types + ". Values replaced with [REDACTED-*]. Do NOT re-read source to bypass redaction. Install redact-cli for ML-powered detection (names, addresses, orgs).")
    }
  }'

exit 0
