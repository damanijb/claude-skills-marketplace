# Search Strategies for Research Providers

## General Principles

1. **Be specific**: Use the full legal entity name + "credit" or "fixed income" qualifier
2. **Avoid abbreviations first**: Search "BNP Paribas" not "BNPP" — use ticker as fallback
3. **Add recency signals**: Append "2025" or "2026" if searching for recent research
4. **Use issuer + topic**: "Deutsche Bank NPL" is better than just "Deutsche Bank"

## Provider-Specific Search Patterns

### JPM Research
- **Primary**: `{full issuer name} credit` (e.g., "BNP Paribas credit")
- **Sector**: `{sector} credit outlook` (e.g., "European banks credit outlook")
- **Topic**: `{issuer} {topic}` (e.g., "Société Générale capital adequacy")
- **Filters**: After search, apply "Credit Research" or "Fixed Income" filter
- **Sort**: Most recent first (default)

### CapitalIQ
- **Company Search**: Use exact legal name in the main search bar
- **Autocomplete**: Wait for dropdown, select the correct entity (watch for parent vs. subsidiary)
- **For financials**: Navigate to "Financials" tab after reaching company page
- **For ratings**: Navigate to "Credit Ratings" tab
- **Quarterly vs Annual**: Toggle on the financials page — default to quarterly for 5Q analysis

### FitchRatings
- **Entity Search**: `{issuer name}` — Fitch auto-matches to rated entities
- **Disambiguation**: If multiple entities (e.g., parent holding co vs. operating subsidiary), select the one with the long-term IDR
- **Research**: After reaching entity page, look for "Research" or "Reports" section
- **Rating Actions**: Check "Rating Action Commentary" for latest changes

### CreditSights
- **Search**: `{issuer name}` — results show latest publications
- **Report Types**: Prioritize "Quick Take" for recent events, "Full Report" for deep analysis
- **Spread Analysis**: Look for OAS/ASW spread data in dedicated sections
- **Peer Group**: CreditSights often includes peer comparisons in reports

### Morgan Stanley
- **Search**: `{issuer name}` or `{sector}` in the research portal search
- **Category Filter**: "Fixed Income" or "Credit" to exclude equity research
- **Analyst Filter**: If you know the covering analyst, filter by name
- **Note Types**: "Blue Paper" = deep dive, "Note" = regular update, "Quick Comment" = event-driven

## Handling No Results

1. Try the ticker symbol instead of full name
2. Try the parent company name
3. Try a broader sector search
4. Check if the issuer is covered by that provider (not all providers cover all issuers)
5. If still no results, log which provider returned nothing and move on

## Data Quality Checks

After extracting data from any provider:
- Verify the issuer name matches what you searched for
- Check that financial data periods are recent (within last 2 quarters)
- Cross-reference ratings across providers for consistency
- Flag any significant discrepancies between sources
