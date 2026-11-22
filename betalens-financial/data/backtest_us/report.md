# BetaLens back-test

23183 company-month observations, 22870 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 3295 | 3.9 | -0.65 | 44.6 | 56.3 |
| BUY | 5101 | 4.3 | -0.48 | 45.4 | 58.6 |
| HOLD | 7765 | 3.81 | -0.81 | 44.2 | 58.3 |
| SELL | 3620 | 4.32 | -0.41 | 43.8 | 57.8 |
| STRONG_SELL | 3089 | 7.62 | 2.68 | 47.7 | 60.5 |
| INSUFFICIENT_DATA | 313 | 3.76 | -1.06 | 41.9 | 58.8 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 4601 | 4.39 | -0.32 | 45.6 | 57.3 |
| Q2 | 4567 | 3.83 | -0.88 | 44.5 | 58.4 |
| Q3 | 4575 | 3.75 | -0.96 | 44.1 | 58.6 |
| Q4 | 4567 | 4.3 | -0.41 | 44.2 | 58.3 |
| Q5 | 4560 | 6.38 | 1.67 | 46.4 | 58.8 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 2389 | 4.41 | -0.26 | 45.5 | 57.4 |
| BUY | 4581 | 3.9 | -0.69 | 45.1 | 57.2 |
| HOLD | 9204 | 3.93 | -0.76 | 44.3 | 58.5 |
| SELL | 4517 | 4.2 | -0.51 | 43.8 | 57.8 |
| STRONG_SELL | 2179 | 9.19 | 4.12 | 49.1 | 61.5 |

Overall score rank correlation with later out-performance: -0.008 (positive in 53.2% of 47 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| price_to_book | 0.066 | 47 | 57.4 |
| liquidity | 0.051 | 47 | 68.1 |
| price_trend | 0.021 | 47 | 57.4 |
| valuation | 0.011 | 47 | 53.2 |
| revenue_growth | 0.009 | 47 | 55.3 |
| profitability | -0.009 | 47 | 40.4 |
| debt | -0.016 | 47 | 53.2 |
| earnings_growth | -0.024 | 47 | 36.2 |
| cash_flow_quality | -0.03 | 47 | 29.8 |
| dividend | -0.039 | 47 | 40.4 |
| cash_conversion_cycle | -0.044 | 47 | 34.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 3173 | 7.61 | -2.03 | 41.3 | 59.4 |
| BUY | 4785 | 8.63 | -1.16 | 41.5 | 62.5 |
| HOLD | 7172 | 7.68 | -2.21 | 40.2 | 63.1 |
| SELL | 3347 | 8.68 | -1.29 | 39.6 | 60.1 |
| STRONG_SELL | 2908 | 16.99 | 6.82 | 45.7 | 65.4 |
| INSUFFICIENT_DATA | 301 | 7.33 | -2.89 | 42.2 | 61.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 4304 | 8.84 | -1.04 | 42.2 | 60.4 |
| Q2 | 4270 | 7.34 | -2.53 | 39.8 | 62.6 |
| Q3 | 4278 | 7.32 | -2.56 | 40.2 | 63.3 |
| Q4 | 4270 | 8.47 | -1.41 | 40.1 | 61.4 |
| Q5 | 4263 | 14.57 | 4.69 | 44.4 | 63.6 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 2320 | 8.3 | -1.51 | 42.0 | 60.1 |
| BUY | 4319 | 8.19 | -1.31 | 41.2 | 60.6 |
| HOLD | 8503 | 7.79 | -2.17 | 40.4 | 63.5 |
| SELL | 4180 | 8.85 | -1.07 | 40.3 | 60.6 |
| STRONG_SELL | 2063 | 19.95 | 9.61 | 46.6 | 66.5 |

Overall score rank correlation with later out-performance: -0.018 (positive in 43.2% of 44 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| price_to_book | 0.102 | 44 | 54.5 |
| price_trend | 0.077 | 44 | 70.5 |
| liquidity | 0.064 | 44 | 70.5 |
| revenue_growth | 0.022 | 44 | 63.6 |
| valuation | -0.002 | 44 | 40.9 |
| profitability | -0.021 | 44 | 40.9 |
| debt | -0.027 | 44 | 56.8 |
| earnings_growth | -0.047 | 44 | 31.8 |
| cash_flow_quality | -0.05 | 44 | 13.6 |
| cash_conversion_cycle | -0.057 | 44 | 34.1 |
| dividend | -0.058 | 44 | 31.8 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | -0.37 | 1.75 | -2.12 | 45.8 | -0.007 |
| current | 6m | -1.14 | 4.69 | -5.83 | 42.0 | -0.016 |
| original | 3m | -0.77 | 1.85 | -2.62 | 44.4 | -0.013 |
| original | 6m | -1.94 | 4.79 | -6.73 | 41.2 | -0.018 |
| equal | 3m | -0.69 | 1.8 | -2.49 | 44.4 | -0.014 |
| equal | 6m | -1.63 | 4.64 | -6.27 | 41.6 | -0.013 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 74 | 76 |
| buy | 66 | 68 |
| hold | 54 | 54 |
| sell | 44 | 41 |
