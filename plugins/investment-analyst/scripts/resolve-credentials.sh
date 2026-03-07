#!/usr/bin/env bash
# resolve-credentials.sh — Resolve credentials for a research provider
# Usage: resolve-credentials.sh <provider-key>
# Provider keys: jpm, capitaliq, fitch, creditsights, morganstanley
# Output: USER=<value>\nPASS=<value> or USER=MISSING\nPASS=MISSING

set -euo pipefail

PROVIDER="${1:-}"
if [[ -z "$PROVIDER" ]]; then
  echo "Usage: resolve-credentials.sh <provider-key>" >&2
  echo "Keys: jpm, capitaliq, fitch, creditsights, morganstanley" >&2
  exit 1
fi

# Map provider key to env var prefixes and 1Password item names
case "$PROVIDER" in
  jpm)
    ENV_PREFIX="JPM_RESEARCH"
    OP_ITEM="JPM Research"
    ;;
  capitaliq)
    ENV_PREFIX="CAPITALIQ"
    OP_ITEM="CapitalIQ"
    ;;
  fitch)
    ENV_PREFIX="FITCH"
    OP_ITEM="Fitch Ratings"
    ;;
  creditsights)
    ENV_PREFIX="CREDITSIGHTS"
    OP_ITEM="CreditSights"
    ;;
  morganstanley)
    ENV_PREFIX="MS_RESEARCH"
    OP_ITEM="Morgan Stanley"
    ;;
  *)
    echo "Unknown provider: $PROVIDER" >&2
    exit 1
    ;;
esac

USER_VAR="${ENV_PREFIX}_USER"
PASS_VAR="${ENV_PREFIX}_PASS"

resolve_user=""
resolve_pass=""

# Step 1: Check environment variables
if [[ -n "${!USER_VAR:-}" ]] && [[ -n "${!PASS_VAR:-}" ]]; then
  echo "USER=${!USER_VAR}"
  echo "PASS=${!PASS_VAR}"
  echo "SOURCE=env"
  exit 0
fi

# Step 2: Check project .env (current directory)
if [[ -f ".env" ]]; then
  resolve_user=$(grep "^${USER_VAR}=" .env 2>/dev/null | cut -d'=' -f2- || true)
  resolve_pass=$(grep "^${PASS_VAR}=" .env 2>/dev/null | cut -d'=' -f2- || true)
  if [[ -n "$resolve_user" ]] && [[ -n "$resolve_pass" ]]; then
    echo "USER=$resolve_user"
    echo "PASS=$resolve_pass"
    echo "SOURCE=project-env"
    exit 0
  fi
fi

# Step 3: Check global .env
GLOBAL_ENV="$HOME/.investment-analyst/.env"
if [[ -f "$GLOBAL_ENV" ]]; then
  resolve_user=$(grep "^${USER_VAR}=" "$GLOBAL_ENV" 2>/dev/null | cut -d'=' -f2- || true)
  resolve_pass=$(grep "^${PASS_VAR}=" "$GLOBAL_ENV" 2>/dev/null | cut -d'=' -f2- || true)
  if [[ -n "$resolve_user" ]] && [[ -n "$resolve_pass" ]]; then
    echo "USER=$resolve_user"
    echo "PASS=$resolve_pass"
    echo "SOURCE=global-env"
    exit 0
  fi
fi

# Step 4: Try 1Password CLI
if command -v op &>/dev/null; then
  resolve_user=$(op read "op://Investment Research/${OP_ITEM}/username" 2>/dev/null || true)
  resolve_pass=$(op read "op://Investment Research/${OP_ITEM}/password" 2>/dev/null || true)
  if [[ -n "$resolve_user" ]] && [[ -n "$resolve_pass" ]]; then
    echo "USER=$resolve_user"
    echo "PASS=$resolve_pass"
    echo "SOURCE=1password"
    exit 0
  fi
fi

# Step 5: Not found
echo "USER=MISSING"
echo "PASS=MISSING"
echo "SOURCE=none"
exit 0
