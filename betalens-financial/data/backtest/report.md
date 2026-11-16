# BetaLens back-test

4493 company-month observations, 1165 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 114 | 12.44 | 4.6 | 51.8 | 60.5 |
| BUY | 242 | 12.98 | 2.29 | 51.2 | 69.0 |
| HOLD | 468 | 6.93 | -0.53 | 40.2 | 53.6 |
| SELL | 227 | 6.69 | -0.91 | 39.6 | 54.2 |
| STRONG_SELL | 114 | 7.46 | -3.47 | 35.1 | 53.5 |
| INSUFFICIENT_DATA | 3328 | 10.35 | -1.39 | 37.0 | 61.3 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 262 | 10.91 | 2.17 | 47.7 | 60.3 |
| Q2 | 229 | 10.05 | 1.66 | 49.8 | 64.6 |
| Q3 | 227 | 8.76 | 0.2 | 44.1 | 56.8 |
| Q4 | 229 | 7.96 | -0.56 | 33.6 | 51.5 |
| Q5 | 218 | 5.51 | -2.95 | 39.0 | 54.1 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 114 | 12.44 | 4.6 | 51.8 | 60.5 |
| BUY | 244 | 12.94 | 2.25 | 51.2 | 69.3 |
| HOLD | 451 | 7.05 | -0.39 | 40.6 | 53.7 |
| SELL | 242 | 6.48 | -1.14 | 38.8 | 53.7 |
| STRONG_SELL | 114 | 7.46 | -3.47 | 35.1 | 53.5 |

Overall score rank correlation with later out-performance: 0.195 (positive in 82.9% of 35 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.069 | 10 | 60.0 |
| valuation | 0.069 | 41 | 78.0 |
| revenue_growth | 0.065 | 29 | 72.4 |
| price_trend | 0.007 | 47 | 48.9 |
| earnings_growth | 0.006 | 29 | 41.4 |
| profitability | -0.024 | 41 | 39.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 106 | 31.67 | 12.69 | 46.2 | 67.0 |
| BUY | 209 | 27.63 | 3.09 | 45.0 | 80.4 |
| HOLD | 350 | 20.29 | 0.88 | 36.9 | 66.3 |
| SELL | 187 | 15.62 | -3.3 | 37.4 | 58.8 |
| STRONG_SELL | 101 | 16.41 | -6.93 | 40.6 | 58.4 |
| INSUFFICIENT_DATA | 3249 | 24.9 | -1.91 | 35.5 | 70.2 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 218 | 29.37 | 8.25 | 42.2 | 73.4 |
| Q2 | 186 | 23.15 | 2.38 | 47.3 | 74.2 |
| Q3 | 186 | 17.19 | -3.61 | 32.8 | 66.7 |
| Q4 | 186 | 24.46 | 3.72 | 39.2 | 61.8 |
| Q5 | 177 | 13.31 | -7.23 | 39.0 | 58.2 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 106 | 31.67 | 12.69 | 46.2 | 67.0 |
| BUY | 211 | 27.5 | 2.96 | 44.5 | 80.6 |
| HOLD | 338 | 21.18 | 1.64 | 38.2 | 67.2 |
| SELL | 197 | 14.41 | -4.28 | 35.5 | 57.4 |
| STRONG_SELL | 101 | 16.41 | -6.93 | 40.6 | 58.4 |

Overall score rank correlation with later out-performance: 0.212 (positive in 71.9% of 32 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.095 | 38 | 92.1 |
| revenue_growth | 0.058 | 26 | 57.7 |
| price_trend | -0.009 | 44 | 43.2 |
| earnings_growth | -0.027 | 26 | 34.6 |
| dividend | -0.029 | 7 | 28.6 |
| profitability | -0.032 | 38 | 39.5 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 2.45 | -3.59 | 6.04 | 48.3 | 0.195 |
| current | 6m | 9.5 | -8.49 | 17.99 | 43.4 | 0.212 |
| original | 3m | -0.52 | -2.42 | 1.9 | 47.0 | 0.139 |
| original | 6m | -1.01 | -5.7 | 4.69 | 37.0 | 0.17 |
| equal | 3m | 1.36 | -2.28 | 3.64 | 45.7 | 0.131 |
| equal | 6m | 3.97 | -5.8 | 9.77 | 38.1 | 0.162 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 87 |
| buy | 76 | 76 |
| hold | 49 | 50 |
| sell | 24 | 24 |
