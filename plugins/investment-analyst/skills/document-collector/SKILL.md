---
name: document-collector
description: This skill should be used when the user asks to "collect documents", "gather filings", "get earnings call", "download annual report", "get SEC filing", "collect investor relations documents", "get 10-K", "get 20-F", "get Pillar 3 disclosure", "gather news articles", or needs to download and process financial documents from public sources including investor relations pages, SEC EDGAR, European regulators, earnings call transcripts, and financial news.
version: 1.0.0
---

# Document Collector

Collect financial documents from public sources using Chrome browser automation, then process them through PageIndex MCP for structured analysis and perfect recall.

## Prerequisites

1. Chrome MCP (`Claude in Chrome`) connected — verify with `tabs_context_mcp`
2. PageIndex MCP available for document processing
3. Workspace directory created: `{workspace}/data/documents/`

## Source Categories & Workflows

### 1. Investor Relations (IR) Pages

**Goal**: Download annual reports, quarterly supplements, presentations, and press releases.

**Workflow:**
1. Search for the company's IR page:
   - `navigate` to `https://www.google.com/search?q={issuer}+investor+relations`
   - Or try common patterns: `{company-domain}.com/investor-relations`, `/investors`, `/ir`
2. Once on the IR page:
   - `find` links for "Annual Report", "Quarterly Report", "Presentations", "Press Releases"
   - Identify the most recent annual report and last 2 quarterly reports
3. For each PDF document:
   - Note the download URL
   - Download using Chrome (click the link) with user confirmation
   - Process through PageIndex: `process_document(url="{pdf_url}")`
   - Wait for processing: `get_document(doc_name="{filename}", wait_for_completion=true)`
   - Extract structure: `get_document_structure(doc_name="{filename}")`
   - Extract key sections: `get_page_content(doc_name="{filename}", pages="{relevant_pages}")`
4. Save extracted text to `{workspace}/data/documents/{filename}.md`

### 2. SEC EDGAR Filings (US Issuers)

**Goal**: Download 10-K, 10-Q filings and extract financial data, risk factors, and MD&A.

**Workflow:**
1. `navigate` to EDGAR full-text search:
   ```
   https://efts.sec.gov/LATEST/search-index?q={issuer}&dateRange=custom&startdt=2024-01-01&forms=10-K,10-Q,20-F
   ```
   Or use the company search:
   ```
   https://www.sec.gov/cgi-bin/browse-edgar?company={issuer}&CIK=&type=10-K&dateb=&owner=include&count=10&search_text=&action=getcompany
   ```
2. `find` the filing links in search results
3. Click through to the filing detail page
4. `find` the primary document link (the 10-K/10-Q itself, not exhibits)
5. Process the filing through PageIndex MCP
6. Extract key sections using `get_document_structure` to identify:
   - **MD&A** (Management Discussion & Analysis)
   - **Financial Statements** (income statement, balance sheet, cash flow)
   - **Risk Factors**
   - **Notes to Financial Statements** (especially loan quality, capital ratios)

### 3. European Regulatory Filings (EU Issuers)

**Goal**: Pillar 3 disclosures, EBA stress test results, ECB supervisory data.

**Workflow:**
1. **Pillar 3 Disclosures**: Usually on the bank's IR page under "Regulatory Disclosures"
   - `navigate` to `{bank-ir-page}` and `find` "Pillar 3" or "Regulatory" section
   - Download the PDF and process through PageIndex
2. **EBA Stress Tests** (if recent):
   - `navigate` to `https://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing`
   - Search for the issuer in results
3. **ECB Supervisory Statistics**:
   - `navigate` to `https://www.bankingsupervision.europa.eu/banking/statistics/`
   - Extract aggregate data for peer comparison context

### 4. Earnings Call Transcripts

**Goal**: Extract management commentary from the most recent earnings call.

**Workflow:**
1. **SeekingAlpha** (primary source):
   - `navigate` to `https://seekingalpha.com/symbol/{ticker}/earnings/transcripts`
   - May require login — check if content is gated
   - If accessible: `get_page_text` to extract transcript
   - If gated: try alternative sources
2. **Company IR Page** (alternative):
   - Check if the company hosts webcasts/transcripts directly
   - `find` "Earnings" or "Webcasts" section
3. **Extract key sections**:
   - CEO/CFO prepared remarks (revenue drivers, expense commentary, outlook)
   - Q&A session (analyst questions reveal concerns)
   - Forward guidance (quantitative targets)
4. Save to `{workspace}/data/documents/earnings-{quarter}-{year}.md`

### 5. Financial News

**Goal**: Gather recent news articles about the issuer for context.

**Workflow:**
1. `navigate` to Google News: `https://news.google.com/search?q={issuer}+bank`
2. Or Reuters: `https://www.reuters.com/search/news?query={issuer}`
3. `find` the 5-10 most recent relevant articles
4. For each article:
   - Click to open
   - `get_page_text` to extract article content
   - Note: Respect copyright — extract facts and data points only, not full article text
5. Summarize key themes and save to `{workspace}/data/documents/news-summary.md`

## PageIndex Integration

After downloading any PDF document:

```
1. process_document(url="{public_url}")           # Submit for processing
2. get_document(doc_name="{name}", wait=true)      # Wait for completion
3. get_document_structure(doc_name="{name}")        # Get table of contents
4. get_page_content(doc_name="{name}", pages="1-5") # Extract specific pages
```

**For large documents (>20 pages)**: Always use `get_document_structure` first to identify relevant sections, then extract targeted page ranges.

## Output Organization

```
{workspace}/data/documents/
├── annual-report-{year}.md          # IR annual report extracts
├── quarterly-report-Q{n}-{year}.md  # Quarterly report extracts
├── 10-K-{year}.md                   # SEC 10-K extracts (US)
├── 20-F-{year}.md                   # SEC 20-F extracts (EU in US)
├── pillar3-{year}.md                # Pillar 3 disclosure extracts
├── earnings-Q{n}-{year}.md          # Earnings call transcript
├── news-summary.md                  # Summarized recent news
└── document-index.json              # Catalog of all collected documents
```

The `document-index.json` tracks:
```json
{
  "documents": [
    {
      "name": "annual-report-2025",
      "source": "investor-relations",
      "url": "...",
      "date": "2025-03-15",
      "pageindexName": "...",
      "keyFindings": ["..."]
    }
  ]
}
```

For detailed source URL patterns, load `references/source-registry.md`.
For filing-type-specific extraction guidance, load `references/filing-patterns.md`.
