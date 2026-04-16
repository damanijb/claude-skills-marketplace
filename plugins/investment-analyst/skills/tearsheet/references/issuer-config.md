# Issuer Configuration Reference

All 44 covered issuers — template filenames, Bloomberg CDS tickers, sector
assignments, vault paths, and fiscal calendar offset details.

---

## US Banks

| Issuer | Template File | CDS Ticker (5Y Sr) | Vault Path |
|---|---|---|---|
| Citibank | `Citibank.xlsx` | `CITI 5Y USD SR CDS` | `08 - Tearsheets/US Banks/Citibank.md` |
| JP Morgan | `JP Morgan.xlsx` | `JPM 5Y USD SR CDS` | `08 - Tearsheets/US Banks/JP Morgan.md` |
| Bank of America | `Bank of America.xlsx` | `BAC 5Y USD SR CDS` | `08 - Tearsheets/US Banks/Bank of America.md` |
| Wells Fargo | `Wells Fargo.xlsx` | `WFC 5Y USD SR CDS` | `08 - Tearsheets/US Banks/Wells Fargo.md` |
| US Bancorp | `US Bancorp.xlsx` | `USB 5Y USD SR CDS` | `08 - Tearsheets/US Banks/US Bancorp.md` |
| Bank of New York | `Bank of New York.xlsx` | `BK 5Y USD SR CDS` | `08 - Tearsheets/US Banks/Bank of New York.md` |
| Metlife | `Metlife.xlsx` | `MET 5Y USD SR CDS` | `08 - Tearsheets/US Banks/Metlife.md` |

**Earnings search keywords (Outlook):** "Citi", "JPMorgan", "JP Morgan", "BofA",
"Bank of America", "Wells Fargo", "US Bancorp", "BNY", "Mellon", "MetLife"

---

## Canadian Banks

All five Canadian banks have a **fiscal year ending October 31**.
Calendar Q1 (Jan–Mar) = Fiscal Q2. Use dual-label PDF naming for all Canadian banks.

| Issuer | Template File | CDS Ticker (5Y Sr) | Vault Path | FY End |
|---|---|---|---|---|
| Royal Bank of Canada | `Royal Bank of Canada.xlsx` | `RY 5Y USD SR CDS` | `08 - Tearsheets/Canadian Banks/Royal Bank of Canada.md` | Oct |
| Toronto Dominion | `Toronto Dominion.xlsx` | `TD 5Y USD SR CDS` | `08 - Tearsheets/Canadian Banks/Toronto Dominion.md` | Oct |
| Bank of Montreal | `Bank of Montreal.xlsx` | `BMO 5Y USD SR CDS` | `08 - Tearsheets/Canadian Banks/Bank of Montreal.md` | Oct |
| Bank of Nova Scotia | `Bank of Nova Scotia.xlsx` | `BNS 5Y USD SR CDS` | `08 - Tearsheets/Canadian Banks/Bank of Nova Scotia.md` | Oct |
| CIBC | `CIBC.xlsx` | `CM 5Y USD SR CDS` | `08 - Tearsheets/Canadian Banks/CIBC.md` | Oct |

### Canadian Bank Quarter Mapping

| Calendar Quarter | Fiscal Quarter (Canadian Banks) |
|---|---|
| Q1 (Jan–Mar) | Fiscal Q2 |
| Q2 (Apr–Jun) | Fiscal Q3 |
| Q3 (Jul–Sep) | Fiscal Q4 |
| Q4 (Oct–Dec) | Fiscal Q1 (of next fiscal year) |

**PDF naming examples:**
- `Royal Bank of Canada 2Q26 (Calendar 1Q26).pdf`
- `Toronto Dominion 3Q26 (Calendar 2Q26).pdf`

**Reporting windows:** Canadian banks report in late May–June (Q2 fiscal / calendar Q1)
and late November–December (Q4 fiscal / calendar Q3). All five report within ~1 week of
each other.

---

## European Banks

| Issuer | Template File | CDS Ticker (5Y Sr) | Vault Path |
|---|---|---|---|
| BNP Paribas | `BNP Paribas.xlsx` | `BNP 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/BNP Paribas.md` |
| Credit Agricole | `Credit Agricole.xlsx` | `ACAFP 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/Credit Agricole.md` |
| Groupe BPCE (Natixis) | `Groupe BPCE (Natixis).xlsx` | `BPCE 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/Groupe BPCE (Natixis).md` |
| ING | `ING.xlsx` | `INTNED 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/ING.md` |
| Nordea | `Nordea.xlsx` | `NDAFH 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/Nordea.md` |
| RaboBank | `RaboBank.xlsx` | `RABOBK 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/RaboBank.md` |
| Svenska Handelsbanken | `Svenska Handelsbanken.xlsx` | `SHBASS 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/Svenska Handelsbanken.md` |
| Swedbank | `Swedbank.xlsx` | `SWEDA 5Y EUR SR CDS` | `08 - Tearsheets/European Banks/Swedbank.md` |

**Note:** BNP Paribas, Credit Agricole, and ING typically report on the same date —
batch those three tearsheet updates together.

**Rabobank:** Semi-annual reporting only (next scheduled: February 10, 2027).
Cooperative entity — no equity ticker. Focus on CET1, LCR, NSFR, and funding metrics.

**EU economic context BQL:** Use EUR swap rates instead of UST for EU bank front pages:
- EUR 2Y swap: `EUSA2 Curncy`
- EUR 10Y swap: `EUSA10 Curncy`
- EUR CDS index: `ITRXEBE Index` (iTraxx Europe Senior Financials)

---

## Corporates

| Issuer | Template File | CDS Ticker (5Y Sr) | Vault Path | FY End | Offset Notes |
|---|---|---|---|---|---|
| Exxon Mobil | `Exxon.xlsx` | `XOM 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Exxon.md` | Dec | None |
| Berkshire Hathaway | `Berkshire Hathaway.xlsx` | `BRK 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Berkshire Hathaway.md` | Dec | None |
| Toyota Motor | `Toyota.xlsx` | `TOYOTA 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Toyota.md` | **Mar** | Cal Q1 = Fiscal Q4 |
| Amazon | `Amazon.xlsx` | `AMZN 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Amazon.md` | Dec | None |
| Apple | `Apple.xlsx` | `AAPL 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Apple.md` | **Sep** | Cal Q1 = Fiscal Q2 |
| Microsoft | `Microsoft.xlsx` | `MSFT 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Microsoft.md` | **Jun** | Cal Q1 = Fiscal Q3 |
| Cisco | `Cisco.xlsx` | `CSCO 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Cisco.md` | **Jul** | Cal Q1 = Fiscal Q3 |
| Visa | `Visa.xlsx` | `V 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Visa.md` | **Sep** | Cal Q1 = Fiscal Q2 |
| Walmart | `Walmart.xlsx` | `WMT 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Walmart.md` | **Jan** | Cal Q1 = Fiscal Q4 |
| Procter & Gamble | `Proctor and Gamble.xlsx` | `PG 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Procter and Gamble.md` | **Jun** | Cal Q1 = Fiscal Q3 |
| Johnson & Johnson | `Johnson and Johnson.xlsx` | `JNJ 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Johnson and Johnson.md` | Dec | None |
| Colgate | `Colgate.xlsx` | `CL 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Colgate.md` | Dec | None |
| Chevron | `Chevron.xlsx` | `CVX 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Chevron.md` | Dec | None |
| John Deere | `John Deere.xlsx` | `DE 5Y USD SR CDS` | `08 - Tearsheets/Corporates/John Deere.md` | **Oct** | Cal Q1 = Fiscal Q2 |
| Nestle | `Nestle.xlsx` | `NESTLE 5Y USD SR CDS` | `08 - Tearsheets/Corporates/Nestle.md` | Dec | None |
| 3M | `3M.xlsx` | `MMM 5Y USD SR CDS` | `08 - Tearsheets/Corporates/3M.md` | Dec | None |

### Corporate Fiscal Offset Quick Reference

| Issuer | Fiscal Year End | Cal Q1 = Fiscal | Dual Label? |
|---|---|---|---|
| Toyota | March | Q4 | Yes: `Toyota 4Q26 (Calendar 1Q26).pdf` |
| Visa | September | Q2 | Yes: `Visa 2Q26 (Calendar 1Q26).pdf` |
| John Deere | October | Q2 | Yes: `John Deere 2Q26 (Calendar 1Q26).pdf` |
| Procter & Gamble | June | Q3 | Yes: `Procter and Gamble 3Q26 (Calendar 1Q26).pdf` |
| Apple | September | Q2 | Yes: `Apple 2Q26 (Calendar 1Q26).pdf` |
| Microsoft | June | Q3 | Yes: `Microsoft 3Q26 (Calendar 1Q26).pdf` |
| Cisco | July | Q3 | Yes: `Cisco 3Q26 (Calendar 1Q26).pdf` |
| Walmart | January | Q4 | Yes: `Walmart 4Q26 (Calendar 1Q26).pdf` |

---

## Vault Root

```
C:/Users/f8631/OneDrive - San Bernardino County Auditor-Controller Treasurer Tax Collector/Obsidian/SBC/
```

Vault tearsheets index: `08 - Tearsheets/TEARSHEETS-INDEX.md`
Coverage grid: `08 - Tearsheets/TEARSHEET-COVERAGE-GRID.md`

---

## #earnings Tag Reference

| Issuer | Tag |
|---|---|
| Citibank | `#earnings/C` |
| JP Morgan | `#earnings/JPM` |
| Bank of America | `#earnings/BAC` |
| Wells Fargo | `#earnings/WFC` |
| US Bancorp | `#earnings/USB` |
| Bank of New York | `#earnings/BK` |
| Metlife | `#earnings/MET` |
| Royal Bank of Canada | `#earnings/RY` |
| Toronto Dominion | `#earnings/TD` |
| Bank of Montreal | `#earnings/BMO` |
| Bank of Nova Scotia | `#earnings/BNS` |
| CIBC | `#earnings/CM` |
| BNP Paribas | `#earnings/BNP` |
| Credit Agricole | `#earnings/ACA` |
| Groupe BPCE | `#earnings/BPCE` |
| ING | `#earnings/ING` |
| Nordea | `#earnings/NDA` |
| RaboBank | `#earnings/RABO` |
| Svenska Handelsbanken | `#earnings/SHB` |
| Swedbank | `#earnings/SWED` |
| Exxon | `#earnings/XOM` |
| Berkshire Hathaway | `#earnings/BRK` |
| Toyota | `#earnings/TM` |
| Amazon | `#earnings/AMZN` |
| Apple | `#earnings/AAPL` |
| Microsoft | `#earnings/MSFT` |
| Cisco | `#earnings/CSCO` |
| Visa | `#earnings/V` |
| Walmart | `#earnings/WMT` |
| Procter & Gamble | `#earnings/PG` |
| Johnson & Johnson | `#earnings/JNJ` |
| Colgate | `#earnings/CL` |
| Chevron | `#earnings/CVX` |
| John Deere | `#earnings/DE` |
| Nestle | `#earnings/NESN` |
| 3M | `#earnings/MMM` |
