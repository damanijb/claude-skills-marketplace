# Source Registry — URL Patterns by Source Type

## Investor Relations Page Patterns

Most companies follow one of these URL patterns:
```
{domain}/investor-relations
{domain}/investors
{domain}/ir
{domain}/en/investor-relations
{domain}/about/investor-relations
```

### Major EU Banks — Direct IR Links
| Bank | IR URL |
|------|--------|
| BNP Paribas | https://invest.bnpparibas/en/ |
| Société Générale | https://investors.societegenerale.com/en |
| Deutsche Bank | https://investor-relations.db.com/ |
| Barclays | https://home.barclays/investor-relations/ |
| HSBC | https://www.hsbc.com/investors |
| UBS | https://www.ubs.com/global/en/investor-relations.html |
| Credit Agricole | https://www.credit-agricole.com/en/finance/finance/financial-information |
| Santander | https://www.santander.com/en/shareholders-and-investors |
| ING | https://www.ing.com/Investor-relations.htm |
| UniCredit | https://www.unicreditgroup.eu/en/investors.html |
| Intesa Sanpaolo | https://group.intesasanpaolo.com/en/investor-relations |
| Nordea | https://www.nordea.com/en/investor-relations |
| BBVA | https://shareholdersandinvestors.bbva.com/financials/ |

### Major US Banks — Direct IR Links
| Bank | IR URL |
|------|--------|
| JPMorgan Chase | https://www.jpmorganchase.com/ir |
| Bank of America | https://investor.bankofamerica.com/ |
| Citigroup | https://www.citigroup.com/global/news/investor-relations |
| Wells Fargo | https://www.wellsfargo.com/about/investor-relations/ |
| Goldman Sachs | https://www.goldmansachs.com/investor-relations/ |
| Morgan Stanley | https://www.morganstanley.com/about-us-ir |

## SEC EDGAR URLs

### Company Search
```
https://www.sec.gov/cgi-bin/browse-edgar?company={name}&CIK=&type={form_type}&dateb=&owner=include&count=10&search_text=&action=getcompany
```

### Full-Text Search (EFTS)
```
https://efts.sec.gov/LATEST/search-index?q={query}&dateRange=custom&startdt={YYYY-MM-DD}&forms={form_types}
```

### Common Form Types
| Form | Description | Use Case |
|------|-------------|----------|
| 10-K | Annual report | Comprehensive financial analysis |
| 10-Q | Quarterly report | Recent quarter data |
| 20-F | Annual report (foreign) | EU banks listed in US |
| 8-K | Current report | Material events, earnings |
| DEF 14A | Proxy statement | Management compensation |
| 6-K | Foreign private issuer | Interim reports |

## European Regulatory Sources

### ECB Banking Supervision
- Supervisory statistics: `https://www.bankingsupervision.europa.eu/banking/statistics/`
- SREP results (if public): Usually in bank's own IR disclosures
- Supervisory priorities: `https://www.bankingsupervision.europa.eu/banking/priorities/`

### EBA (European Banking Authority)
- Risk dashboard: `https://www.eba.europa.eu/risk-analysis-and-data/risk-dashboard`
- Stress test results: `https://www.eba.europa.eu/risk-analysis-and-data/eu-wide-stress-testing`
- Transparency exercise: `https://www.eba.europa.eu/risk-analysis-and-data/eu-wide-transparency-exercise`

### National Regulators
| Country | Regulator | URL |
|---------|-----------|-----|
| France | ACPR | https://acpr.banque-france.fr/ |
| Germany | BaFin | https://www.bafin.de/EN/ |
| UK | PRA | https://www.bankofengland.co.uk/prudential-regulation |
| Spain | BdE | https://www.bde.es/bde/en/ |
| Italy | BoI | https://www.bancaditalia.it/compiti/vigilanza/ |
| Netherlands | DNB | https://www.dnb.nl/en/supervision/ |

## News Sources

### Financial News
```
Google News: https://news.google.com/search?q={issuer}
Reuters: https://www.reuters.com/search/news?query={issuer}
Bloomberg: https://www.bloomberg.com/search?query={issuer}
Financial Times: https://www.ft.com/search?q={issuer}
```

### Earnings Calendar
```
Nasdaq: https://www.nasdaq.com/market-activity/earnings?date={YYYY-MM-DD}
Investing.com: https://www.investing.com/earnings-calendar/
```
