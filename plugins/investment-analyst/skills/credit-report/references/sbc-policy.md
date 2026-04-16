# SBC Treasury Investment Policy — Tenor & Concentration Limits

Reference for the SBC Portfolio section of the credit report.
Load this file when populating the SBC Exposure panel or checking policy compliance.

---

## SBC Investment Policy Statement — Tenor Limits by Security Type

The following maximum maturities apply to the **SBC Operating Pool** under the current
Investment Policy Statement. Limits are stated as final maturity from settlement date.

| Security Type | SBC Max Maturity | Min Rating (S&P / Fitch) | Notes |
|---|---|---|---|
| U.S. Treasuries | 5 years | N/A | No credit limit |
| U.S. Agency Debentures | 5 years | Implicit AAA | FHLB, FNMA, FHLMC, FFCB |
| Agency CMO / MBS | 5 years (WAL) | AAA | WAL ≤ 5 years at purchase |
| Asset-Backed Securities | 5 years (WAL) | AAA (all agencies) | WAL ≤ 5 years at purchase |
| Commercial Paper | 270 days | A-1 / F1 | Or equivalent S&P/Fitch |
| Certificates of Deposit | 5 years | A / A (LT); A-1 / F1 (ST) | Domestic + foreign banks |
| Bank Notes / Corporate Notes | 5 years | A- / A- | Approved Issuer List only |
| Banker's Acceptances | 180 days | A-1 / F1 | |
| Repurchase Agreements | 30 days | — | Governed by PSA/ISMA |
| Money Market Funds | Overnight / 60-day WAM | AAAm | SEC 2a-7 compliant |
| Negotiable CDs | 5 years | A / A | |
| Medium-Term Notes | 5 years | A- / A- | Approved Issuer List only |

---

## PFM Managed Pool — Tenor Limits

PFM Asset Management manages a separate investment pool for SBC Treasury under an
Investment Management Agreement (IMA). The PFM pool is typically more conservatively
positioned with shorter maximum tenors:

| Security Type | PFM Max Maturity | Min Rating | Notes |
|---|---|---|---|
| U.S. Treasuries | 3 years | N/A | |
| U.S. Agency Debentures | 3 years | Implicit AAA | |
| Agency CMO / MBS | 3 years (WAL) | AAA | |
| Asset-Backed Securities | 2 years (WAL) | AAA | |
| Commercial Paper | 270 days | A-1+ / F1+ | Higher bar than SBC pool |
| Certificates of Deposit | 1 year | A-1 / F1 | Short-term ratings only |
| Bank Notes / Corporate Notes | 2 years | A / A | |
| Money Market Funds | Overnight / 60-day WAM | AAAm | |

> **Note:** PFM limits reflect the IMA's more liquidity-focused mandate.
> Confirm with the most recent IMA amendment if a specific trade falls near a boundary.

---

## Approved Issuer List — Bank Sector

Covered US bank issuers currently on the Approved Issuer List (AIL):

| Issuer | AIL Name / Bucket | Approved Instruments | Max Exposure (% of Portfolio) |
|---|---|---|---|
| JPMorgan Chase | JPM / JPMORGAN | CP, CD, BN, Corp Notes | Per AIL concentration limit |
| Bank of America | BAC / BOFA | CP, CD, BN, Corp Notes | Per AIL concentration limit |
| Citigroup / Citibank | CITI / CITIGRP | CP, CD, BN, Corp Notes | Per AIL concentration limit |
| Wells Fargo | WFC / WFARGO | CP, CD, BN, Corp Notes | Per AIL concentration limit |
| BNP Paribas | BNPP / BNPPNY | CP, CD (NY Branch) | Per AIL concentration limit |
| Svenska Handelsbanken | SHB | CP, CD | Per AIL concentration limit |

> Full concentration limits and per-issuer position caps are in:
> `T:\Data\Shared\Credit analysis\Approved list\Approved Issuer List.xlsm`

---

## SQL Query — Current SBC Holdings for Issuer

To pull current portfolio exposure for a given issuer bucket, query `portfolio.latest_pfm`:

```sql
SELECT
    issuer,
    security_type,
    sector,
    description,
    maturity_date,
    duration,
    par_value,
    yield,
    fitch_rating,
    sp_rating
FROM portfolio.latest_pfm
WHERE issuer IN ('{ISSUER_BUCKET_1}', '{ISSUER_BUCKET_2}')
ORDER BY maturity_date
```

**Common issuer bucket codes for banks:**

| Issuer | Bucket Codes to Query |
|---|---|
| JPMorgan | 'JPM', 'JPMORGAN', 'JPMORG' |
| Bank of America | 'BAC', 'BOFA', 'BOFASEC' |
| Citigroup | 'CITI', 'CITIGRP', 'CITIBANK' |
| Wells Fargo | 'WFC', 'WFARGO', 'WFBK' |
| BNP Paribas | 'BNPP', 'BNPPNY', 'BNP' |
| Svenska Handelsbanken | 'SHB', 'SHBA' |

---

## Bloomberg BQL — Current Ratings

Preferred BQL pattern for pulling all three agency ratings:

```
-- S&P and Fitch via equity ticker (most reliable)
get(rating(source=SP).value, rating(source=FITCH).value)
for(['JPM US Equity'])

-- Moody's via Corp bond ticker (equity ticker returns N.A.)
get(rating(source=MOODY).value)
for(['JPM 4 3/4 01/10/2028 Corp'])
```

**Known Moody's Corp ticker examples:**

| Issuer | Example Corp Ticker |
|---|---|
| JPMorgan Chase | JPM 4 3/4 01/10/2028 Corp |
| Bank of America | BAC 3 1/2 04/19/2026 Corp |
| Citigroup | C 4.45 09/29/2027 Corp |
| Wells Fargo | WFC 3.0 04/22/2026 Corp |
| BNP Paribas | BNP 3 1/2 03/01/2028 Corp |

> **Note:** Moody's equity-level ratings require the `RTG_MOODY_LONG_TERM` field via BDP,
> not BQL's `rating(source=MOODY)`. BQL ratings pull bond-level Moody's ratings.
> If the specific bond is matured/unavailable, search for an active benchmark bond
> using Bloomberg ticker format: `[TICKER] [COUPON] [MATURITY] Corp`

---

## FRED Series — Sector Economic Indicators

Pull these via `mcp__sbcounty-treasurer__fred_get_series` for the economics section:

**Banking Sector:**

| Indicator | FRED Series ID | Unit |
|---|---|---|
| SOFR (Overnight) | SOFR | % |
| Fed Funds Rate | FEDFUNDS | % |
| 2Y Treasury | DGS2 | % |
| 5Y Treasury | DGS5 | % |
| 10Y Treasury | DGS10 | % |
| 2s10s Spread | — | Calculate: DGS10 − DGS2 |
| Prime Rate | DPRIME | % |
| Bank Prime Loan Rate | MPRIME | % |
| Unemployment Rate | UNRATE | % |
| CPI All Items | CPIAUCSL | Index |
| PCE Price Index | PCEPI | Index |
| Real GDP Growth | A191RL1Q225SBEA | % QoQ annualized |
| Commercial Bank Credit | TOTCI | $B |
| C&I Loans | BUSLOANS | $B |
| Consumer Credit Outstanding | TOTALSL | $B |
| 30-Day AA CP Rate (nonfinancial) | DCPN30 | % |
| 30-Day AA CP Rate (financial) | DCPF30 | % |

**Corporate Sector:**

| Indicator | FRED Series ID | Unit |
|---|---|---|
| IG Corporate OAS | BAMLC0A0CM | bps |
| HY Corporate OAS | BAMLH0A0HYM2 | bps |
| Investment Grade Spread | BAMLC0A0CMEY | % |
| WTI Oil Price | DCOILWTICO | $/bbl |
| Industrial Production | INDPRO | Index |

---

## Tenor Compliance Check Logic

When populating the SBC Exposure section of the credit report, flag any position where:

```
maturity_date > TODAY + SBC_MAX_TENOR_DAYS
```

Where SBC_MAX_TENOR_DAYS = 1825 (5 years) for Bank Notes / Corporate Notes.

For PFM positions, flag when:
```
maturity_date > TODAY + PFM_MAX_TENOR_DAYS
```
Where PFM_MAX_TENOR_DAYS = 730 (2 years) for Bank Notes / Corporate Notes.

Display a ⚠️ flag next to any position exceeding the applicable pool's tenor limit.
