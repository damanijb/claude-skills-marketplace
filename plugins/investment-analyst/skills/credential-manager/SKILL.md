---
name: credential-manager
description: This skill should be used when the user asks to "set up credentials", "configure API keys", "authenticate research providers", "credential setup", "configure 1Password for research", "set up .env for research providers", or needs to resolve login credentials for JPM Research, CapitalIQ, FitchRatings, CreditSights, or Morgan Stanley Research platforms.
version: 0.1.0
---

# Credential Manager

Resolve authentication credentials for gated financial research platforms. Supports a 4-step resolution chain with secure fallbacks.

## Resolution Chain (in priority order)

For each provider, attempt credential resolution in this order:

1. **Environment variables** — Check for `{PROVIDER}_USER` and `{PROVIDER}_PASS` in the current shell environment
2. **Project `.env`** — Check for a `.env` file in the current workspace root
3. **Global `.env`** — Check `~/.investment-analyst/.env`
4. **1Password CLI** — If `op` is available, run `op read "op://Investment Research/{Provider}/{field}"`
5. **Interactive prompt** — If all above fail, ask the user to provide credentials

## Provider Environment Variable Map

| Provider | Username Var | Password Var | 1Password Item |
|----------|-------------|-------------|----------------|
| JPM Research | `JPM_RESEARCH_USER` | `JPM_RESEARCH_PASS` | `JPM Research` |
| CapitalIQ | `CAPITALIQ_USER` | `CAPITALIQ_PASS` | `CapitalIQ` |
| FitchRatings | `FITCH_USER` | `FITCH_PASS` | `Fitch Ratings` |
| CreditSights | `CREDITSIGHTS_USER` | `CREDITSIGHTS_PASS` | `CreditSights` |
| Morgan Stanley | `MS_RESEARCH_USER` | `MS_RESEARCH_PASS` | `Morgan Stanley` |

## Workflow

1. Determine which providers the user needs credentials for
2. Run `${CLAUDE_PLUGIN_ROOT}/scripts/resolve-credentials.sh {provider}` for each
3. Parse the output — format is `USER=value` and `PASS=value` on separate lines
4. If a provider returns `MISSING`, ask the user interactively
5. Never write credentials to any file other than `.env` — and only when the user explicitly asks to persist them

## Security Rules

- NEVER log, echo, or write credentials to workspace files, git-tracked files, or reports
- NEVER include credentials in tool call outputs visible to other skills
- Credentials are ephemeral — resolved per session, not cached
- The `.env` file should be in `.gitignore` and never committed
- If the user asks to "save credentials", write ONLY to `~/.investment-analyst/.env` with restrictive permissions (chmod 600)

## Setting Up Credentials

When a user asks to configure credentials for the first time:

1. Create `~/.investment-analyst/.env` if it doesn't exist
2. For each provider, ask for username and password
3. Write to the `.env` file in the format:
   ```
   JPM_RESEARCH_USER=user@company.com
   JPM_RESEARCH_PASS=secretvalue
   ```
4. Set file permissions: `chmod 600 ~/.investment-analyst/.env`
5. Confirm setup is complete

## 1Password Setup (Optional)

If the user prefers 1Password:

1. Verify `op` CLI is installed: `which op`
2. Verify authentication: `op whoami`
3. Guide the user to create a vault named "Investment Research" with items for each provider
4. Each item should have `username` and `password` fields
5. Test with: `op read "op://Investment Research/JPM Research/username"`

For detailed provider-specific configuration, load `references/provider-registry.md`.
