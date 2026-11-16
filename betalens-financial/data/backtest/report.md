# BetaLens back-test

4582 company-month observations, 1190 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is about two years, returns exclude dividends, and monthly samples overlap.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 426 | 10.6 | 1.81 | 48.8 | 62.7 |
| BUY | 283 | 7.9 | -0.62 | 42.4 | 54.1 |
| HOLD | 272 | 8.23 | 1.04 | 40.1 | 55.5 |
| SELL | 133 | 5.82 | -2.1 | 34.6 | 48.1 |
| STRONG_SELL | 76 | 9.06 | -1.82 | 35.5 | 56.6 |
| INSUFFICIENT_DATA | 3392 | 10.26 | -1.58 | 36.7 | 61.0 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 268 | 7.89 | -0.6 | 45.9 | 58.2 |
| Q2 | 232 | 11.37 | 3.04 | 47.8 | 63.4 |
| Q3 | 234 | 8.95 | 0.65 | 45.3 | 56.0 |
| Q4 | 232 | 8.0 | -0.5 | 33.6 | 51.7 |
| Q5 | 224 | 7.81 | -0.53 | 41.1 | 55.4 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 133 | 8.48 | -0.2 | 46.6 | 60.9 |
| BUY | 233 | 13.08 | 3.26 | 51.5 | 66.5 |
| HOLD | 468 | 7.2 | -0.71 | 40.8 | 53.6 |
| SELL | 230 | 6.81 | 0.73 | 39.1 | 52.2 |
| STRONG_SELL | 126 | 10.64 | -0.86 | 37.3 | 56.3 |

Overall score rank correlation with later out-performance: 0.138 (positive in 77.1% of 35 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.113 | 10 | 60.0 |
| revenue_growth | 0.075 | 29 | 75.9 |
| valuation | 0.069 | 41 | 80.5 |
| price_trend | 0.008 | 47 | 46.8 |
| earnings_growth | 0.007 | 29 | 44.8 |
| profitability | -0.024 | 41 | 41.5 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 369 | 25.32 | 3.85 | 43.9 | 72.9 |
| BUY | 213 | 22.15 | 0.82 | 36.6 | 70.9 |
| HOLD | 209 | 21.55 | 3.81 | 38.3 | 59.8 |
| SELL | 109 | 10.39 | -9.16 | 33.0 | 54.1 |
| STRONG_SELL | 69 | 18.88 | -4.29 | 44.9 | 59.4 |
| INSUFFICIENT_DATA | 3316 | 24.7 | -2.24 | 35.6 | 70.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 222 | 20.18 | -0.63 | 36.0 | 71.6 |
| Q2 | 188 | 29.1 | 8.54 | 50.5 | 72.9 |
| Q3 | 190 | 20.64 | 0.15 | 37.4 | 67.9 |
| Q4 | 188 | 21.56 | 0.98 | 34.0 | 58.5 |
| Q5 | 181 | 16.98 | -3.21 | 42.5 | 60.8 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 125 | 20.33 | 0.93 | 39.2 | 68.0 |
| BUY | 206 | 30.12 | 5.89 | 46.1 | 78.2 |
| HOLD | 346 | 20.78 | 0.9 | 36.4 | 66.8 |
| SELL | 181 | 15.64 | -0.5 | 39.8 | 54.7 |
| STRONG_SELL | 111 | 20.09 | -4.11 | 40.5 | 62.2 |

Overall score rank correlation with later out-performance: 0.169 (positive in 62.5% of 32 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.097 | 38 | 92.1 |
| revenue_growth | 0.065 | 26 | 65.4 |
| dividend | 0.042 | 7 | 42.9 |
| price_trend | -0.01 | 44 | 47.7 |
| earnings_growth | -0.023 | 26 | 34.6 |
| profitability | -0.031 | 38 | 42.1 |

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 75 | 86 |
| buy | 60 | 78 |
| hold | 40 | 54 |
| sell | 25 | 32 |
