# Investment Policy Statement — Schedule I Limits

San Bernardino County Investment Policy per California Government Code.

## Sector Limits

| Security Type | Max % Portfolio | Max Issuer % | Max Maturity | Min Rating | CA Gov Code |
|---------------|----------------|-------------|-------------|------------|-------------|
| U.S. Treasuries | 100% | None | 5 years | N/A | §53601(b) |
| Federal Agencies | 100% | 40% | 5 years | N/A | §53601(f) |
| Agency Mortgage-Backed | 100% | 5% | 5 years | AA- | §53601(o) |
| Asset-Backed Securities | 20% | 5% | 5 years | AA- | §53601(o) |
| Commercial Paper | 25% | 5% | 270 days | A-1 | §53601(h) |
| Corporate Notes | 30% | 5% | 5 years | A | §53601(k) |
| Joint Powers Authority | 100% | None | N/A | N/A | §53601 |
| Money Market Funds | 20% | 5% | N/A | AAAm | §53601(l) |
| Repurchase Agreements | 100% | None | 1 year | N/A | §53601(j) |
| Supranationals | 30% | 10% | 5 years | AA | §53601(q) |
| Negotiable CDs | 30% | 5% | 5 years | A-1 | §53601(i) |
| Bankers Acceptances | 40% | 5% | 180 days | N/A | §53601(g) |
| LAIF | N/A | $75M max | N/A | N/A | §16429.1 |
| Municipal Bonds | 30% | 5% | 5 years | A | §53601(e) |
| Certificates of Deposit | 30% | 5% | 5 years | N/A | §53601.8 |
| Medium-Term Notes | 30% | 5% | 5 years | A | §53601(k) |

## Global Constraints

| Constraint | Limit |
|-----------|-------|
| Maximum portfolio duration | 3.0 years |
| Corporate issuer concentration | 5% per issuer |
| LAIF maximum deposit | $75,000,000 |
| Maximum single maturity | 5 years (most types) |

## Compliance Check Logic

For each security type in the portfolio:

```python
actual_pct = sector_market_value / total_market_value * 100

if actual_pct > max_pct:
    status = "EXCEEDS"       # Red — violation
elif actual_pct > max_pct * 0.9:
    status = "Near Limit"    # Yellow — warning
else:
    status = "Compliant"     # Green — OK
```

## Status Indicators

| Status | Color | Condition |
|--------|-------|-----------|
| Compliant (✓) | #70AD47 (green) | Below 90% of limit |
| Near Limit | #FFC000 (amber) | 90%–100% of limit |
| EXCEEDS (⚠) | #C00000 (red) | Over limit |

## Security Types with Issuer Limits
These types have 5% per-issuer concentration limits:
- Agency Mortgage-Backed
- Asset-Backed Securities
- Commercial Paper
- Corporate Notes
- Money Market Funds
- Supranationals (10%)
- Negotiable CDs
- Municipal Bonds

## Security Types without Issuer Limits
- U.S. Treasuries
- Federal Agencies (but has 40% per-agency limit)
- Joint Powers Authority
- Repurchase Agreements
