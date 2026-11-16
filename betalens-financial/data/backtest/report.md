# BetaLens back-test

4628 company-month observations, 1182 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 114 | 12.44 | 4.6 | 51.8 | 60.5 |
| BUY | 242 | 12.98 | 2.29 | 51.2 | 69.0 |
| HOLD | 471 | 6.69 | -0.61 | 39.9 | 52.9 |
| SELL | 239 | 7.26 | -0.37 | 39.3 | 54.0 |
| STRONG_SELL | 116 | 8.72 | -1.98 | 35.3 | 53.4 |
| INSUFFICIENT_DATA | 3446 | 10.27 | -1.53 | 36.7 | 60.9 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 264 | 10.73 | 2.1 | 47.3 | 59.8 |
| Q2 | 232 | 10.04 | 1.67 | 49.6 | 64.7 |
| Q3 | 231 | 8.93 | 0.48 | 45.0 | 57.1 |
| Q4 | 232 | 7.7 | -0.8 | 32.8 | 50.4 |
| Q5 | 223 | 6.48 | -1.78 | 38.6 | 53.4 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 114 | 12.44 | 4.6 | 51.8 | 60.5 |
| BUY | 244 | 12.94 | 2.25 | 51.2 | 69.3 |
| HOLD | 469 | 6.68 | -0.6 | 39.9 | 52.7 |
| SELL | 239 | 7.26 | -0.37 | 39.3 | 54.0 |
| STRONG_SELL | 116 | 8.72 | -1.98 | 35.3 | 53.4 |

Overall score rank correlation with later out-performance: 0.194 (positive in 82.9% of 35 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.113 | 10 | 60.0 |
| revenue_growth | 0.074 | 29 | 75.9 |
| valuation | 0.069 | 41 | 80.5 |
| price_trend | 0.008 | 47 | 48.9 |
| earnings_growth | 0.007 | 29 | 44.8 |
| profitability | -0.024 | 41 | 39.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 106 | 31.67 | 12.69 | 46.2 | 67.0 |
| BUY | 209 | 27.63 | 3.09 | 45.0 | 80.4 |
| HOLD | 350 | 20.05 | 0.89 | 36.6 | 65.7 |
| SELL | 197 | 15.59 | -3.05 | 37.1 | 57.9 |
| STRONG_SELL | 102 | 17.53 | -5.61 | 41.2 | 58.8 |
| INSUFFICIENT_DATA | 3364 | 24.79 | -2.11 | 35.4 | 70.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 220 | 29.1 | 8.14 | 42.3 | 73.2 |
| Q2 | 188 | 22.83 | 2.2 | 46.3 | 73.4 |
| Q3 | 188 | 17.23 | -3.37 | 33.5 | 66.5 |
| Q4 | 188 | 24.44 | 3.85 | 39.4 | 61.7 |
| Q5 | 180 | 13.77 | -6.47 | 38.3 | 57.2 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 106 | 31.67 | 12.69 | 46.2 | 67.0 |
| BUY | 211 | 27.5 | 2.96 | 44.5 | 80.6 |
| HOLD | 348 | 20.09 | 0.96 | 36.8 | 65.5 |
| SELL | 197 | 15.59 | -3.05 | 37.1 | 57.9 |
| STRONG_SELL | 102 | 17.53 | -5.61 | 41.2 | 58.8 |

Overall score rank correlation with later out-performance: 0.213 (positive in 68.8% of 32 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.097 | 38 | 92.1 |
| revenue_growth | 0.065 | 26 | 65.4 |
| dividend | 0.042 | 7 | 42.9 |
| price_trend | -0.01 | 44 | 50.0 |
| earnings_growth | -0.023 | 26 | 34.6 |
| profitability | -0.03 | 38 | 44.7 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 2.5 | -2.46 | 4.96 | 48.9 | 0.194 |
| current | 6m | 9.29 | -7.76 | 17.05 | 43.2 | 0.213 |
| original | 3m | -0.45 | -1.2 | 0.75 | 47.2 | 0.139 |
| original | 6m | -0.9 | -4.57 | 3.67 | 37.5 | 0.17 |
| equal | 3m | 1.3 | -1.22 | 2.52 | 45.5 | 0.13 |
| equal | 6m | 3.96 | -4.53 | 8.49 | 38.5 | 0.161 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 87 |
| buy | 76 | 76 |
| hold | 49 | 49 |
| sell | 24 | 24 |
