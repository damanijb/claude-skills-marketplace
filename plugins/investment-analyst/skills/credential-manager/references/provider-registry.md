# Provider Registry

## JPM Research (J.P. Morgan Markets)

- **Platform URL**: https://www.jpmm.com/research
- **Login URL**: https://www.jpmm.com/research/login
- **Auth Type**: Form login (username/password), may redirect to corporate SSO
- **Env Vars**: `JPM_RESEARCH_USER`, `JPM_RESEARCH_PASS`
- **1Password Path**: `op://Investment Research/JPM Research/`
- **Fields**: username, password
- **Session Behavior**: Session cookies persist ~8 hours, may require re-auth for sensitive sections
- **MFA**: May require if SSO is configured — handle manually if triggered
- **Notes**: Enterprise clients often use SSO redirect. If login form redirects to an SSO page, pause and ask the user to complete SSO manually, then resume after redirect back to jpmm.com.

## CapitalIQ (S&P Global Market Intelligence)

- **Platform URL**: https://www.capitaliq.spglobal.com
- **Login URL**: https://www.capitaliq.spglobal.com/web/client
- **Auth Type**: Multi-step SAML SSO via S&P Global identity provider
- **Env Vars**: `CAPITALIQ_USER`, `CAPITALIQ_PASS`
- **1Password Path**: `op://Investment Research/CapitalIQ/`
- **Fields**: username, password
- **Session Behavior**: Long-lived session (~12 hours), cookies required
- **MFA**: May trigger Duo or similar — handle manually if detected
- **Notes**: After login, the platform loads a single-page app. Use `javascript_tool` to extract data from the DOM rather than `get_page_text` for financial tables. Company search is at the top search bar.

## FitchRatings

- **Platform URL**: https://www.fitchratings.com
- **Login URL**: https://www.fitchratings.com/login
- **Auth Type**: Standard form login (email/password)
- **Env Vars**: `FITCH_USER`, `FITCH_PASS`
- **1Password Path**: `op://Investment Research/Fitch Ratings/`
- **Fields**: username (email), password
- **Session Behavior**: Session cookies persist ~4 hours
- **MFA**: Rare for standard accounts
- **Notes**: Free tier shows limited content. Institutional subscription required for full research reports and rating action commentaries. PDFs available for download — process through PageIndex MCP.

## CreditSights

- **Platform URL**: https://www.creditsights.com
- **Login URL**: https://www.creditsights.com/login
- **Auth Type**: Standard form login (email/password)
- **Env Vars**: `CREDITSIGHTS_USER`, `CREDITSIGHTS_PASS`
- **1Password Path**: `op://Investment Research/CreditSights/`
- **Fields**: username (email), password
- **Session Behavior**: Session cookies persist ~6 hours
- **MFA**: None typically
- **Notes**: Search by issuer name to find latest credit opinions, spread analysis, and peer comparisons. Reports are HTML-based — `get_page_text` works well. Also provides downloadable Excel data for spreads.

## Morgan Stanley Research

- **Platform URL**: https://www.morganstanley.com/ideas
- **Login URL**: https://www.morganstanley.com/auth/login
- **Auth Type**: Institutional SSO or form login depending on account type
- **Env Vars**: `MS_RESEARCH_USER`, `MS_RESEARCH_PASS`
- **1Password Path**: `op://Investment Research/Morgan Stanley/`
- **Fields**: username, password
- **Session Behavior**: Session cookies persist ~8 hours
- **MFA**: Common for institutional clients — may require manual intervention
- **Notes**: Research portal may redirect to institutional login. If SSO is detected, pause and ask user to complete authentication manually. Search by company or sector to find equity and credit research notes. Charts are image-based — use `computer` (screenshot) to capture.
