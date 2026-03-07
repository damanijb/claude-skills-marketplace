# Provider Login Flows — Detailed Selectors & Navigation

> **Important**: Financial platform UIs change frequently. If selectors below fail, use `find` with semantic queries (e.g., "email input", "password field", "sign in button") as a resilient fallback. Always take a screenshot after login attempts to verify state.

## JPM Research (jpmm.com)

### Login Flow
```
URL: https://www.jpmm.com/research
Step 1: Navigate to URL
Step 2: find("sign in" or "log in" link) → click
Step 3: find("email" or "username" input) → form_input(username)
Step 4: find("password" input) → form_input(password)
Step 5: find("sign in" or "submit" button) → click
Step 6: screenshot → verify dashboard loaded
```

### SSO Detection
- If URL redirects to a domain NOT matching `jpmm.com` (e.g., `login.jpmorgan.com`, `adfs.*`), SSO is active
- Screenshot the SSO page, inform user: "JPM Research is using SSO. Please complete authentication in the browser, then tell me when you're back on the research portal."
- After user confirms, verify by checking URL contains `jpmm.com/research`

### Navigation After Login
```
Search: find("search" input at top of page) → form_input("{issuer} credit research")
Filters: find("Credit" or "Fixed Income" filter links) → click to narrow
Results: find("research report" links) → click most recent
Content: get_page_text() for report body
Charts: computer(screenshot) for any embedded visuals
```

### Key URLs
- Research home: `https://www.jpmm.com/research`
- Credit research: `https://www.jpmm.com/research/credit`
- Search: `https://www.jpmm.com/research/search?q={query}`

---

## CapitalIQ (S&P Global Market Intelligence)

### Login Flow
```
URL: https://www.capitaliq.spglobal.com
Step 1: Navigate to URL → may auto-redirect to login
Step 2: find("email" or "user ID" input) → form_input(username)
Step 3: find("next" or "continue" button) → click (multi-step login)
Step 4: find("password" input) → form_input(password)
Step 5: find("sign in" button) → click
Step 6: screenshot → verify CapitalIQ dashboard
```

### Multi-Step SSO Handling
- S&P Global uses a multi-page SAML flow
- Page 1: Enter email → click "Next"
- Page 2: Enter password → click "Sign In"
- If Duo MFA appears: screenshot, ask user to approve on their phone
- Wait up to 30 seconds after MFA prompt before checking again

### Navigation After Login
```
Company Search: find("search" input, typically top-right) → form_input("{issuer}")
Autocomplete: computer(wait, 2s) → find("{issuer}" in dropdown) → click
```

### Data Extraction Pages
Each tab on the company page contains structured data:

**Financial Summary Tab:**
```javascript
// Scrape the summary table
const table = document.querySelector('[data-testid="financial-summary"]') ||
              document.querySelector('.financial-summary-table') ||
              document.querySelector('table');
if (table) {
  const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
  const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr =>
    Array.from(tr.cells).map(td => td.textContent.trim())
  );
  JSON.stringify({ headers, rows });
}
```

**Credit Ratings Tab:**
```javascript
// Scrape ratings information
const ratingElements = document.querySelectorAll('.credit-rating, [data-testid*="rating"]');
const ratings = Array.from(ratingElements).map(el => ({
  agency: el.querySelector('.agency')?.textContent?.trim(),
  rating: el.querySelector('.rating-value')?.textContent?.trim(),
  outlook: el.querySelector('.outlook')?.textContent?.trim()
}));
JSON.stringify(ratings);
```

**Quarterly Financials:**
- Navigate: find("Financials" tab) → click
- Select: find("Quarterly" toggle) → click
- Wait: computer(wait, 3s) for data to load
- Extract: javascript_tool with table scraping as above

---

## FitchRatings

### Login Flow
```
URL: https://www.fitchratings.com
Step 1: Navigate to URL
Step 2: find("sign in" or "log in" link, usually top-right) → click
Step 3: find("email" input) → form_input(email)
Step 4: find("password" input) → form_input(password)
Step 5: find("sign in" or "log in" button) → click
Step 6: screenshot → verify logged-in state (user icon visible)
```

### Cookie/Consent Handling
- Fitch often shows a cookie consent banner
- find("reject all" or "decline" button) → click (privacy-preserving default)
- If no reject option: find("accept necessary" or "essential only") → click

### Navigation After Login
```
Entity Search: find("search" input) → form_input("{issuer}")
Results: computer(wait, 2s) → find("{issuer}" entity link) → click
Entity Page: Contains rating, outlook, history, and research links
```

### Data Extraction
```
Rating: find("long-term rating" or "IDR" element) → read_page for value
Outlook: find("outlook" element) → read_page for value
History: find("rating history" section) → javascript_tool to scrape table
Reports: find("research" or "reports" section) → collect PDF URLs
```

---

## CreditSights

### Login Flow
```
URL: https://www.creditsights.com
Step 1: Navigate to URL
Step 2: find("log in" or "sign in" link) → click
Step 3: find("email" input) → form_input(email)
Step 4: find("password" input) → form_input(password)
Step 5: find("log in" button) → click
Step 6: screenshot → verify dashboard
```

### Navigation After Login
```
Search: find("search" input) → form_input("{issuer}")
Filter: find("credit opinion" or "research type" filter) → select
Results: click most recent report
```

### Data Extraction
```
Report Text: get_page_text() → full credit opinion
Spread Data: find("spread" or "OAS" table) → javascript_tool to scrape
Peer Comparison: find("peer" or "comparable" section) → get_page_text()
Recommendation: find("recommendation" or "view" element) → read_page
```

---

## Morgan Stanley Research

### Login Flow
```
URL: https://www.morganstanley.com/ideas
Step 1: Navigate to URL
Step 2: find("sign in" or "log in" link) → click
Step 3: Detect if institutional SSO (URL redirect away from morganstanley.com)
  → If SSO: screenshot, ask user to complete manually
  → If standard: find("email/username" input) → form_input
Step 4: find("password" input) → form_input(password)
Step 5: find("sign in" button) → click
Step 6: screenshot → verify research portal access
```

### Navigation After Login
```
Search: find("search" input) → form_input("{issuer}")
Filter: find("Fixed Income" or "Credit" category) → click
Results: click most recent report matching issuer
```

### Data Extraction
```
Report Text: get_page_text() → research note content
Charts: computer(screenshot) → capture all embedded charts
Key Metrics: find("key metrics" or "summary" section) → get_page_text()
```

---

## Universal Fallback Strategy

If specific selectors fail for any provider:

1. **Take a screenshot** to see current page state
2. **Use `read_page`** with `filter: "interactive"` to list all interactive elements
3. **Use `find`** with semantic queries that describe the element's purpose
4. **Try `javascript_tool`** to query the DOM directly:
   ```javascript
   document.querySelector('input[type="email"], input[type="text"], input[name*="user"], input[name*="email"]')?.id
   ```
5. If all automated approaches fail, **screenshot and ask the user** to guide you to the right element
