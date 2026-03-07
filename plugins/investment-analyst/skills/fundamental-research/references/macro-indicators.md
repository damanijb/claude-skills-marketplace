# Macro Indicators — FRED Series IDs & European Data Sources

## US Economic Indicators (FRED MCP)

### GDP & Growth
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Real GDP | `GDPC1` | Quarterly | Billions (2017$) |
| Real GDP Growth (annualized) | `A191RL1Q225SBEA` | Quarterly | % |
| Nominal GDP | `GDP` | Quarterly | Billions |
| Industrial Production | `INDPRO` | Monthly | Index |
| ISM Manufacturing PMI | `MANEMP` | Monthly | Index (>50 = expansion) |

### Labor Market
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Unemployment Rate | `UNRATE` | Monthly | % |
| Nonfarm Payrolls | `PAYEMS` | Monthly | Thousands |
| Initial Jobless Claims | `ICSA` | Weekly | Persons |
| Labor Force Participation | `CIVPART` | Monthly | % |
| Average Hourly Earnings | `CES0500000003` | Monthly | $/hour |

### Inflation
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| CPI (All Items) | `CPIAUCSL` | Monthly | Index |
| CPI YoY Change | `CPIAUCNS` | Monthly | % |
| Core CPI (ex food/energy) | `CPILFESL` | Monthly | Index |
| PCE Price Index | `PCEPI` | Monthly | Index |
| Core PCE | `PCEPILFE` | Monthly | Index |
| 5Y Breakeven Inflation | `T5YIE` | Daily | % |

### Interest Rates & Yield Curve
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Fed Funds Rate | `FEDFUNDS` | Monthly | % |
| Fed Funds Effective | `DFF` | Daily | % |
| 2Y Treasury Yield | `DGS2` | Daily | % |
| 5Y Treasury Yield | `DGS5` | Daily | % |
| 10Y Treasury Yield | `DGS10` | Daily | % |
| 30Y Treasury Yield | `DGS30` | Daily | % |
| 10Y-2Y Spread | `T10Y2Y` | Daily | % |
| 10Y-3M Spread | `T10Y3M` | Daily | % |
| 3M T-Bill | `DTB3` | Daily | % |

### Banking & Credit Conditions
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Bank Lending Standards (C&I) | `DRTSCILM` | Quarterly | Net % tightening |
| C&I Loans Outstanding | `BUSLOANS` | Weekly | Billions |
| Consumer Loans | `CONSUMER` | Monthly | Billions |
| Delinquency Rate (C&I) | `DRBLACBS` | Quarterly | % |
| Delinquency Rate (Mortgage) | `DRSFRMACBS` | Quarterly | % |
| Delinquency Rate (Credit Card) | `DRCCLACBS` | Quarterly | % |
| Charge-Off Rate (All Loans) | `CORBLACBS` | Quarterly | % |
| Total Bank Credit | `TOTBKCR` | Weekly | Billions |

### Housing
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Case-Shiller Home Price | `CSUSHPISA` | Monthly | Index |
| Existing Home Sales | `EXHOSLUSM495S` | Monthly | Millions |
| Housing Starts | `HOUST` | Monthly | Thousands |
| 30Y Mortgage Rate | `MORTGAGE30US` | Weekly | % |

### Financial Conditions
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Chicago Fed FCI | `NFCI` | Weekly | Index (0 = avg conditions) |
| VIX (Volatility) | `VIXCLS` | Daily | Index |
| BBB Corporate Spread | `BAMLC0A4CBBB` | Daily | % |
| High Yield Spread | `BAMLH0A0HYM2` | Daily | % |
| IG Corporate Spread | `BAMLC0A0CM` | Daily | % |
| TED Spread (risk premium) | `TEDRATE` | Daily | % |

### Consumer
| Indicator | FRED Series ID | Frequency | Unit |
|-----------|---------------|-----------|------|
| Consumer Confidence | `UMCSENT` | Monthly | Index |
| Retail Sales | `RSAFS` | Monthly | Millions |
| Personal Savings Rate | `PSAVERT` | Monthly | % |
| Household Debt Service Ratio | `TDSP` | Quarterly | % |

---

## European Economic Indicators (Chrome Access)

### ECB Data

**Key Interest Rates:**
- URL: `https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/`
- Main refinancing rate, deposit facility rate, marginal lending rate

**Bank Lending Survey:**
- URL: `https://www.ecb.europa.eu/stats/ecb_surveys/bank_lending_survey/`
- Credit standards, loan demand, terms and conditions

**Monetary Statistics:**
- URL: `https://www.ecb.europa.eu/stats/money_credit_banking/`
- M3 growth, bank lending to euro area

### Eurostat Data

**GDP:**
- URL: `https://ec.europa.eu/eurostat/databrowser/view/tec00115/default/table`
- Quarterly GDP growth by country

**Unemployment:**
- URL: `https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table`
- Monthly unemployment by country

**Inflation (HICP):**
- URL: `https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_manr/default/table`
- Monthly HICP by country

**Government Finance:**
- URL: `https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table`
- Government debt and deficit by country

### Country-Specific Indicators

| Country | Key GDP Source | Key Banking Source |
|---------|---------------|-------------------|
| France | INSEE | ACPR banking statistics |
| Germany | Destatis | Bundesbank banking statistics |
| UK | ONS | Bank of England financial stability |
| Spain | INE | Banco de España banking statistics |
| Italy | ISTAT | Banca d'Italia banking statistics |
| Netherlands | CBS | DNB banking statistics |

---

## Example FRED Queries

### Quick Macro Snapshot
```
fred_get_latest_value("GDPC1")      # Latest GDP
fred_get_latest_value("UNRATE")     # Unemployment
fred_get_latest_value("CPIAUCSL")   # CPI
fred_get_latest_value("DFF")        # Fed Funds
fred_get_latest_value("T10Y2Y")     # Yield curve slope
fred_get_latest_value("BAMLH0A0HYM2")  # HY spread
```

### Historical Series (5 quarters)
```
fred_get_series("GDPC1", observation_start="2024-10-01")
fred_get_series("FEDFUNDS", observation_start="2024-10-01")
fred_get_series("DRSFRMACBS", observation_start="2024-01-01")  # Quarterly delinquencies
```

### Banking Sector Health
```
fred_get_latest_value("DRTSCILM")   # Lending standards
fred_get_latest_value("DRBLACBS")   # C&I delinquencies
fred_get_latest_value("CORBLACBS")  # Charge-off rate
fred_get_latest_value("BUSLOANS")   # C&I loan volume
```
