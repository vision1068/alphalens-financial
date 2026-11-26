# BetaLens back-test

2952 company-month observations, 490 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 18 | 6.03 | 0.62 | 50.0 | 55.6 |
| HOLD | 245 | 5.15 | -0.6 | 38.4 | 49.8 |
| SELL | 138 | 6.39 | -1.48 | 39.9 | 54.3 |
| STRONG_SELL | 53 | 7.21 | -2.89 | 39.6 | 52.8 |
| INSUFFICIENT_DATA | 2462 | 11.0 | -0.73 | 36.9 | 60.9 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 116 | 5.82 | -1.82 | 44.0 | 54.3 |
| Q2 | 94 | 6.09 | -0.45 | 36.2 | 48.9 |
| Q3 | 94 | 7.2 | 0.74 | 43.6 | 52.1 |
| Q4 | 94 | 3.02 | -3.49 | 31.9 | 48.9 |
| Q5 | 92 | 6.55 | -0.13 | 44.6 | 53.3 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 49 | 4.77 | -0.35 | 51.0 | 51.0 |
| BUY | 100 | 3.78 | -1.43 | 38.0 | 51.0 |
| HOLD | 196 | 6.17 | -0.96 | 36.7 | 50.0 |
| SELL | 97 | 6.65 | -0.77 | 43.3 | 55.7 |
| STRONG_SELL | 48 | 7.19 | -2.13 | 41.7 | 52.1 |

Overall score rank correlation with later out-performance: 0.142 (positive in 58.6% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.071 | 41 | 68.3 |
| price_trend | 0.036 | 47 | 51.1 |
| revenue_growth | 0.03 | 29 | 55.2 |
| profitability | -0.005 | 41 | 53.7 |
| dividend | -0.022 | 8 | 50.0 |
| earnings_growth | -0.023 | 29 | 41.4 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 11 | 2.12 | -4.44 | 36.4 | 54.5 |
| HOLD | 163 | 16.65 | 1.06 | 36.8 | 61.3 |
| SELL | 116 | 12.99 | -6.38 | 34.5 | 54.3 |
| STRONG_SELL | 44 | 14.04 | -6.36 | 36.4 | 52.3 |
| INSUFFICIENT_DATA | 2398 | 26.34 | -0.39 | 35.5 | 69.3 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 90 | 15.14 | -2.84 | 41.1 | 63.3 |
| Q2 | 68 | 21.63 | 4.94 | 36.8 | 60.3 |
| Q3 | 69 | 15.86 | -0.66 | 36.2 | 63.8 |
| Q4 | 68 | 6.42 | -10.31 | 30.9 | 51.5 |
| Q5 | 67 | 13.97 | -3.13 | 40.3 | 50.7 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 35 | 12.01 | -0.99 | 48.6 | 62.9 |
| BUY | 62 | 9.82 | -2.93 | 30.6 | 58.1 |
| HOLD | 145 | 20.04 | 1.54 | 39.3 | 62.8 |
| SELL | 80 | 9.23 | -9.05 | 32.5 | 51.2 |
| STRONG_SELL | 40 | 15.69 | -3.98 | 40.0 | 52.5 |

Overall score rank correlation with later out-performance: 0.224 (positive in 61.5% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.09 | 38 | 73.7 |
| revenue_growth | 0.034 | 26 | 69.2 |
| profitability | 0.015 | 38 | 57.9 |
| price_trend | 0.006 | 44 | 43.2 |
| earnings_growth | -0.032 | 26 | 46.2 |
| dividend | -0.129 | 5 | 0.0 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | -1.54 | -1.3 | -0.24 | 43.8 | 0.142 |
| current | 6m | -2.08 | -5.44 | 3.36 | 42.3 | 0.224 |
| original | 3m | -1.95 | -0.19 | -1.76 | 42.7 | 0.09 |
| original | 6m | -3.88 | -5.03 | 1.15 | 40.8 | 0.192 |
| equal | 3m | -2.25 | -1.33 | -0.92 | 42.7 | 0.087 |
| equal | 6m | -3.88 | -4.52 | 0.64 | 40.8 | 0.157 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 80 |
| buy | 76 | 66 |
| hold | 49 | 42 |
| sell | 24 | 23 |
