# BetaLens back-test

3090 company-month observations, 563 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 26 | 4.55 | 1.24 | 53.8 | 50.0 |
| HOLD | 269 | 4.98 | -1.24 | 36.4 | 49.8 |
| SELL | 178 | 6.22 | -2.07 | 39.3 | 55.1 |
| STRONG_SELL | 54 | 10.2 | -0.36 | 40.7 | 53.7 |
| INSUFFICIENT_DATA | 2527 | 10.87 | -1.03 | 36.5 | 60.6 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 140 | 7.72 | -0.14 | 44.3 | 52.9 |
| Q2 | 112 | 5.89 | -1.29 | 33.0 | 52.7 |
| Q3 | 104 | 4.55 | -1.99 | 38.5 | 48.1 |
| Q4 | 112 | 4.36 | -2.8 | 35.7 | 51.8 |
| Q5 | 95 | 6.18 | -0.37 | 45.3 | 53.7 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 56 | 5.03 | -0.07 | 50.0 | 50.0 |
| BUY | 110 | 2.97 | -1.47 | 38.2 | 49.1 |
| HOLD | 227 | 5.9 | -1.72 | 35.2 | 50.2 |
| SELL | 116 | 6.81 | -1.24 | 43.1 | 57.8 |
| STRONG_SELL | 54 | 10.2 | -0.36 | 40.7 | 53.7 |

Overall score rank correlation with later out-performance: 0.148 (positive in 69.0% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.047 | 41 | 70.7 |
| dividend | 0.037 | 9 | 55.6 |
| revenue_growth | 0.025 | 29 | 51.7 |
| price_trend | 0.021 | 47 | 44.7 |
| earnings_growth | -0.011 | 29 | 41.4 |
| profitability | -0.033 | 41 | 43.9 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 16 | 3.28 | -2.46 | 43.8 | 62.5 |
| HOLD | 190 | 17.7 | 1.19 | 34.2 | 60.5 |
| SELL | 150 | 12.88 | -7.54 | 32.7 | 57.3 |
| STRONG_SELL | 45 | 16.52 | -4.43 | 37.8 | 53.3 |
| INSUFFICIENT_DATA | 2460 | 25.99 | -1.05 | 35.1 | 69.4 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 112 | 21.99 | 2.25 | 43.8 | 67.0 |
| Q2 | 86 | 18.77 | 1.2 | 31.4 | 64.0 |
| Q3 | 76 | 10.1 | -6.38 | 30.3 | 52.6 |
| Q4 | 86 | 8.75 | -8.86 | 30.2 | 57.0 |
| Q5 | 69 | 13.48 | -3.35 | 40.6 | 50.7 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 38 | 12.17 | -0.47 | 50.0 | 65.8 |
| BUY | 70 | 10.55 | -2.48 | 31.4 | 58.6 |
| HOLD | 179 | 19.49 | 0.63 | 35.2 | 60.9 |
| SELL | 97 | 11.28 | -8.7 | 33.0 | 56.7 |
| STRONG_SELL | 45 | 16.52 | -4.43 | 37.8 | 53.3 |

Overall score rank correlation with later out-performance: 0.239 (positive in 65.4% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.069 | 38 | 68.4 |
| revenue_growth | 0.031 | 26 | 53.8 |
| price_trend | -0.008 | 44 | 40.9 |
| earnings_growth | -0.028 | 26 | 42.3 |
| profitability | -0.032 | 38 | 44.7 |
| dividend | -0.042 | 6 | 33.3 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.65 | -0.4 | 1.05 | 45.1 | 0.148 |
| current | 6m | 3.5 | -0.96 | 4.46 | 44.8 | 0.239 |
| original | 3m | -0.08 | 0.53 | -0.61 | 43.4 | 0.092 |
| original | 6m | 1.84 | -0.59 | 2.43 | 43.7 | 0.203 |
| equal | 3m | -0.2 | -0.15 | -0.05 | 42.5 | 0.083 |
| equal | 6m | 1.58 | -0.09 | 1.67 | 42.5 | 0.169 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 78 |
| buy | 76 | 65 |
| hold | 49 | 41 |
| sell | 24 | 24 |
