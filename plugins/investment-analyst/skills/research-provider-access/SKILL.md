---
name: research-provider-access
description: This skill should be used when the user asks to "access JPM Research", "pull from CapitalIQ", "get Fitch rating", "download CreditSights report", "Morgan Stanley research", "pull research from providers", "scrape research platform", "get credit research", "login to research portal", or needs to extract financial data, credit ratings, or research reports from gated research platforms using Chrome browser automation.
version: 0.1.0
---

# Research Provider Access

Automate Chrome-based access to 5 gated financial research platforms: JPM Research, CapitalIQ, FitchRatings, CreditSights, and Morgan Stanley Research.

## Prerequisites

1. Resolve credentials using the `credential-manager` skill first
2. Ensure Chrome MCP (`Claude in Chrome`) is connected — call `tabs_context_mcp` to verify
3. Create a new tab for each provider session: `tabs_create_mcp`

## General Workflow (All Providers)

```
1. Resolve credentials → credential-manager skill
2. Create Chrome tab → tabs_create_mcp
3. Navigate to login URL → navigate tool
4. Fill login form → find + form_input tools
5. Handle SSO/MFA → screenshot + ask user if manual intervention needed
6. Navigate to search → navigate or find tool
7. Search for issuer → form_input + computer (click)
8. Extract data → get_page_text / javascript_tool / computer (screenshot)
9. Save extracted data to workspace → write to {workspace}/data/provider-extracts/
```

## Provider-Specific Flows

### JPM Research (jpmm.com)

**Login:**
1. `navigate` to `https://www.jpmm.com/research`
2. `find` the username field (query: "email input" or "username input")
3. `form_input` username, then `find` and `form_input` password
4. `find` and click the login/submit button
5. `computer` (screenshot) to verify login success — check for research dashboard
6. If redirected to SSO, screenshot and ask user to complete manually

**Search & Extract:**
1. `find` the search bar (query: "search input" or "search bar")
2. `form_input` the issuer name (e.g., "BNP Paribas credit")
3. Click search or press Enter via `computer` (key action)
4. Wait 2-3 seconds for results: `computer` (wait)
5. `find` links matching "Credit Research" or "Fixed Income" filter
6. Click the most recent relevant report
7. `get_page_text` to extract the full report text
8. For embedded charts: `computer` (screenshot) to capture visuals
9. Save text to `{workspace}/data/provider-extracts/jpm-research.md`

### CapitalIQ (S&P Global)

**Login:**
1. `navigate` to `https://www.capitaliq.spglobal.com`
2. Handle SAML redirect — may land on S&P Global identity page
3. `find` username/email field, `form_input` credentials
4. `find` password field, `form_input` password
5. Click sign-in button
6. `computer` (screenshot) to verify — look for CapitalIQ dashboard

**Search & Extract:**
1. `find` the main search bar (typically top of page)
2. `form_input` the issuer name
3. Click on the company from autocomplete results
4. Navigate to key sections using `find`:
   - "Financial Summary" tab → `javascript_tool` to scrape summary table
   - "Credit Ratings" tab → `javascript_tool` to scrape ratings table
   - "Key Statistics" → `javascript_tool` to scrape stats
   - "Income Statement" → `javascript_tool` to extract quarterly financials
   - "Balance Sheet" → `javascript_tool` to extract assets/liabilities
5. For each table, use `javascript_tool` with DOM scraping:
   ```javascript
   // Example: extract table data as JSON
   const rows = document.querySelectorAll('table.financial-data tr');
   const data = Array.from(rows).map(row =>
     Array.from(row.cells).map(cell => cell.textContent.trim())
   );
   JSON.stringify(data);
   ```
6. Save structured JSON to `{workspace}/data/provider-extracts/capitaliq-financials.json`

### FitchRatings

**Login:**
1. `navigate` to `https://www.fitchratings.com`
2. `find` the login/sign-in link, click it
3. `find` email field, `form_input` email
4. `find` password field, `form_input` password
5. Click sign-in button
6. `computer` (screenshot) to verify login

**Search & Extract:**
1. `find` the search bar
2. `form_input` issuer name
3. Search and find the entity page
4. Extract from entity page:
   - Current rating and outlook via `get_page_text`
   - Rating history table via `javascript_tool`
   - Recent rating action commentary via `get_page_text`
5. If PDF research reports are available:
   - `find` download links for PDFs
   - Note the URLs for the `document-collector` skill to process via PageIndex
6. Save to `{workspace}/data/provider-extracts/fitch-ratings.json` with structure:
   ```json
   {
     "issuer": "...",
     "longTermRating": "...",
     "shortTermRating": "...",
     "outlook": "...",
     "ratingHistory": [...],
     "latestAction": "...",
     "actionDate": "...",
     "reportUrls": [...]
   }
   ```

### CreditSights

**Login:**
1. `navigate` to `https://www.creditsights.com`
2. `find` login link, click it
3. `find` email field, `form_input` credentials
4. `find` password field, `form_input` password
5. Click sign-in
6. `computer` (screenshot) to verify

**Search & Extract:**
1. `find` the search functionality
2. `form_input` issuer name
3. Filter results to show latest credit opinions
4. Click the most recent report
5. `get_page_text` to extract the full credit opinion text
6. Look for spread data sections — extract via `javascript_tool` if tabular
7. Look for peer comparison sections — extract those specifically
8. Save to `{workspace}/data/provider-extracts/creditsights-opinion.md`

### Morgan Stanley Research

**Login:**
1. `navigate` to `https://www.morganstanley.com/ideas` or research portal
2. `find` login/sign-in link
3. Handle institutional SSO if detected (screenshot + ask user)
4. `find` and `form_input` credentials on the login form
5. Click sign-in
6. `computer` (screenshot) to verify

**Search & Extract:**
1. `find` the search bar on the research portal
2. `form_input` issuer or sector name
3. Filter for "Credit Research" or "Fixed Income" if available
4. Click the most recent relevant note
5. `get_page_text` for text content
6. `computer` (screenshot) for any embedded charts or tables
7. Save to `{workspace}/data/provider-extracts/ms-research.md`

## Error Handling

- **Login failure**: Screenshot the page, show to user, ask for manual intervention
- **CAPTCHA detected**: Screenshot and ask user to solve manually, then resume
- **MFA prompt**: Screenshot and ask user to complete, then resume
- **Session expired mid-extraction**: Re-run login flow automatically once, then ask user
- **Content not found**: Log which provider/search returned no results, continue with other providers
- **Rate limiting**: Wait 30 seconds and retry once, then move to next provider

## Output Format

Each provider's extracted data is saved to `{workspace}/data/provider-extracts/` as either:
- `.md` files for text content (reports, opinions, commentary)
- `.json` files for structured data (financials, ratings, statistics)

For detailed provider login selectors and URL patterns, load `references/provider-login-flows.md`.
For search query optimization tips, load `references/search-strategies.md`.
