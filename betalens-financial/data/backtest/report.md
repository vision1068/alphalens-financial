# BetaLens back-test

3004 company-month observations, 539 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 26 | 4.55 | 1.24 | 53.8 | 50.0 |
| HOLD | 251 | 4.31 | -1.43 | 37.5 | 51.0 |
| SELL | 183 | 6.21 | -2.13 | 39.3 | 54.6 |
| STRONG_SELL | 43 | 12.87 | 0.16 | 39.5 | 53.5 |
| INSUFFICIENT_DATA | 2465 | 11.26 | -0.43 | 37.4 | 61.3 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 139 | 7.37 | -0.36 | 43.2 | 53.2 |
| Q2 | 96 | 5.19 | -1.09 | 36.5 | 51.0 |
| Q3 | 115 | 5.9 | -1.79 | 38.3 | 52.2 |
| Q4 | 96 | 2.01 | -4.25 | 35.4 | 51.0 |
| Q5 | 93 | 7.19 | 0.31 | 45.2 | 53.8 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 52 | 4.48 | -0.09 | 50.0 | 50.0 |
| BUY | 111 | 3.25 | -1.65 | 38.7 | 47.7 |
| HOLD | 211 | 5.03 | -1.96 | 36.5 | 52.1 |
| SELL | 112 | 7.24 | -0.79 | 42.9 | 58.0 |
| STRONG_SELL | 53 | 11.25 | -0.94 | 39.6 | 52.8 |

Overall score rank correlation with later out-performance: 0.157 (positive in 69.0% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.067 | 41 | 75.6 |
| dividend | 0.047 | 9 | 55.6 |
| revenue_growth | 0.018 | 29 | 51.7 |
| price_trend | 0.013 | 47 | 46.8 |
| earnings_growth | -0.009 | 29 | 41.4 |
| profitability | -0.029 | 41 | 43.9 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 16 | 3.28 | -2.46 | 43.8 | 62.5 |
| HOLD | 172 | 15.31 | 0.08 | 33.7 | 61.6 |
| SELL | 155 | 13.41 | -7.28 | 33.5 | 58.1 |
| STRONG_SELL | 37 | 20.32 | -4.69 | 37.8 | 56.8 |
| INSUFFICIENT_DATA | 2401 | 27.04 | 0.35 | 36.7 | 70.0 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 111 | 21.96 | 2.14 | 44.1 | 67.6 |
| Q2 | 70 | 16.29 | -0.03 | 31.4 | 64.3 |
| Q3 | 89 | 9.82 | -8.33 | 28.1 | 56.2 |
| Q4 | 70 | 8.13 | -8.22 | 31.4 | 57.1 |
| Q5 | 68 | 13.72 | -3.29 | 41.2 | 52.9 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 12.02 | -0.68 | 50.0 | 63.9 |
| BUY | 71 | 11.64 | -2.34 | 33.8 | 59.2 |
| HOLD | 162 | 16.65 | -0.84 | 34.0 | 63.0 |
| SELL | 93 | 11.93 | -8.01 | 34.4 | 59.1 |
| STRONG_SELL | 46 | 19.3 | -5.09 | 37.0 | 52.2 |

Overall score rank correlation with later out-performance: 0.254 (positive in 61.5% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.078 | 38 | 71.1 |
| revenue_growth | 0.019 | 26 | 57.7 |
| price_trend | -0.022 | 44 | 36.4 |
| profitability | -0.026 | 38 | 42.1 |
| earnings_growth | -0.028 | 26 | 38.5 |
| dividend | -0.045 | 6 | 33.3 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.89 | 0.16 | 0.73 | 45.9 | 0.157 |
| current | 6m | 3.74 | -0.89 | 4.63 | 45.3 | 0.254 |
| original | 3m | 0.11 | 1.25 | -1.14 | 43.2 | 0.12 |
| original | 6m | 2.1 | 0.36 | 1.74 | 44.2 | 0.219 |
| equal | 3m | 0.12 | 0.66 | -0.54 | 43.2 | 0.115 |
| equal | 6m | 1.8 | 0.91 | 0.89 | 43.0 | 0.199 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 80 |
| buy | 76 | 64 |
| hold | 49 | 41 |
| sell | 24 | 27 |
