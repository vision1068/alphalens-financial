# BetaLens back-test

4581 company-month observations, 1153 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 105 | 12.92 | 5.01 | 51.4 | 61.9 |
| BUY | 232 | 13.27 | 2.87 | 53.9 | 69.8 |
| HOLD | 461 | 6.7 | -0.63 | 39.0 | 52.5 |
| SELL | 239 | 7.26 | -0.37 | 39.3 | 54.0 |
| STRONG_SELL | 116 | 8.72 | -1.98 | 35.3 | 53.4 |
| INSUFFICIENT_DATA | 3428 | 10.27 | -1.54 | 36.6 | 60.9 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 249 | 11.24 | 2.88 | 49.0 | 60.6 |
| Q2 | 230 | 10.11 | 1.61 | 48.7 | 65.7 |
| Q3 | 225 | 8.6 | 0.48 | 44.9 | 55.1 |
| Q4 | 230 | 7.81 | -0.79 | 33.0 | 51.3 |
| Q5 | 219 | 6.46 | -1.97 | 37.9 | 53.0 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 123 | 13.64 | 5.12 | 52.0 | 65.0 |
| BUY | 231 | 12.03 | 1.99 | 51.5 | 67.5 |
| HOLD | 453 | 6.75 | -0.42 | 40.0 | 52.5 |
| SELL | 230 | 7.58 | -0.37 | 38.7 | 53.9 |
| STRONG_SELL | 116 | 8.72 | -1.98 | 35.3 | 53.4 |

Overall score rank correlation with later out-performance: 0.201 (positive in 85.7% of 35 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.118 | 10 | 60.0 |
| revenue_growth | 0.075 | 29 | 79.3 |
| valuation | 0.07 | 41 | 78.0 |
| price_trend | 0.01 | 47 | 48.9 |
| earnings_growth | 0.006 | 29 | 44.8 |
| profitability | -0.024 | 41 | 43.9 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 97 | 33.26 | 14.54 | 48.5 | 67.0 |
| BUY | 200 | 28.37 | 4.18 | 47.5 | 80.5 |
| HOLD | 342 | 20.06 | 0.87 | 36.5 | 65.2 |
| SELL | 197 | 15.59 | -3.05 | 37.1 | 57.9 |
| STRONG_SELL | 102 | 17.53 | -5.61 | 41.2 | 58.8 |
| INSUFFICIENT_DATA | 3346 | 24.77 | -2.14 | 35.4 | 70.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 205 | 30.41 | 9.73 | 46.3 | 73.7 |
| Q2 | 187 | 22.63 | 1.9 | 45.5 | 72.7 |
| Q3 | 181 | 17.51 | -2.55 | 33.7 | 65.7 |
| Q4 | 187 | 24.05 | 3.36 | 38.5 | 61.0 |
| Q5 | 178 | 13.99 | -6.45 | 38.8 | 57.9 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 114 | 34.32 | 14.98 | 50.0 | 70.2 |
| BUY | 195 | 26.05 | 2.01 | 44.6 | 80.0 |
| HOLD | 336 | 20.24 | 1.28 | 37.5 | 64.6 |
| SELL | 191 | 15.92 | -3.08 | 36.6 | 57.6 |
| STRONG_SELL | 102 | 17.53 | -5.61 | 41.2 | 58.8 |

Overall score rank correlation with later out-performance: 0.221 (positive in 71.9% of 32 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.098 | 38 | 92.1 |
| revenue_growth | 0.065 | 26 | 65.4 |
| dividend | 0.045 | 7 | 42.9 |
| price_trend | -0.009 | 44 | 50.0 |
| earnings_growth | -0.023 | 26 | 34.6 |
| profitability | -0.031 | 38 | 44.7 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 3.07 | -2.66 | 5.73 | 48.9 | 0.201 |
| current | 6m | 10.54 | -7.75 | 18.29 | 45.8 | 0.221 |
| original | 3m | -0.06 | -1.33 | 1.27 | 46.8 | 0.147 |
| original | 6m | 1.18 | -4.74 | 5.92 | 40.5 | 0.18 |
| equal | 3m | 1.51 | -1.18 | 2.69 | 45.9 | 0.136 |
| equal | 6m | 4.84 | -4.4 | 9.24 | 40.5 | 0.17 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 86 |
| buy | 76 | 75 |
| hold | 49 | 48 |
| sell | 24 | 24 |
