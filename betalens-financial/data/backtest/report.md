# BetaLens back-test

2817 company-month observations, 499 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 26 | 5.12 | 1.8 | 53.8 | 53.8 |
| HOLD | 267 | 5.36 | -1.0 | 37.1 | 50.2 |
| SELL | 141 | 7.87 | 0.42 | 43.3 | 57.4 |
| STRONG_SELL | 29 | 21.11 | 11.0 | 55.2 | 72.4 |
| INSUFFICIENT_DATA | 2318 | 10.74 | -1.0 | 36.0 | 60.5 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 130 | 7.55 | -0.05 | 43.8 | 53.1 |
| Q2 | 94 | 6.75 | 0.29 | 37.2 | 52.1 |
| Q3 | 95 | 6.24 | -0.24 | 40.0 | 48.4 |
| Q4 | 94 | 5.31 | -1.15 | 36.2 | 54.3 |
| Q5 | 86 | 8.75 | 2.77 | 51.2 | 61.6 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 48 | 6.13 | 0.25 | 54.2 | 56.2 |
| BUY | 104 | 3.46 | -1.01 | 38.5 | 49.0 |
| HOLD | 197 | 6.05 | -0.98 | 37.6 | 49.7 |
| SELL | 100 | 8.2 | 0.96 | 40.0 | 56.0 |
| STRONG_SELL | 50 | 15.9 | 6.36 | 56.0 | 72.0 |

Overall score rank correlation with later out-performance: -0.012 (positive in 52.2% of 23 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.062 | 9 | 55.6 |
| valuation | 0.039 | 41 | 68.3 |
| revenue_growth | 0.015 | 29 | 48.3 |
| price_trend | 0.009 | 47 | 34.0 |
| earnings_growth | -0.047 | 29 | 37.9 |
| profitability | -0.055 | 41 | 39.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 16 | 5.29 | -0.45 | 50.0 | 62.5 |
| HOLD | 189 | 17.97 | 1.36 | 34.9 | 61.4 |
| SELL | 116 | 16.39 | -2.26 | 37.9 | 63.8 |
| STRONG_SELL | 23 | 38.6 | 18.55 | 52.2 | 69.6 |
| INSUFFICIENT_DATA | 2262 | 26.24 | -0.39 | 34.9 | 69.5 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 104 | 21.09 | 2.23 | 44.2 | 68.3 |
| Q2 | 69 | 21.34 | 4.82 | 37.7 | 58.0 |
| Q3 | 69 | 14.24 | -2.25 | 31.9 | 65.2 |
| Q4 | 69 | 12.01 | -4.51 | 34.8 | 58.0 |
| Q5 | 61 | 20.18 | 5.55 | 44.3 | 63.9 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 35 | 13.63 | 0.29 | 51.4 | 68.6 |
| BUY | 64 | 9.55 | -2.72 | 32.8 | 57.8 |
| HOLD | 148 | 20.45 | 2.81 | 37.8 | 63.5 |
| SELL | 85 | 16.42 | -3.7 | 36.5 | 62.4 |
| STRONG_SELL | 40 | 29.95 | 12.48 | 47.5 | 67.5 |

Overall score rank correlation with later out-performance: -0.029 (positive in 45.0% of 20 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.033 | 38 | 63.2 |
| revenue_growth | 0.004 | 26 | 46.2 |
| dividend | -0.003 | 6 | 50.0 |
| price_trend | -0.02 | 44 | 38.6 |
| earnings_growth | -0.074 | 26 | 30.8 |
| profitability | -0.086 | 38 | 34.2 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 1.05 | 2.29 | -1.24 | 46.4 | -0.012 |
| current | 6m | 4.33 | 4.59 | -0.26 | 47.1 | -0.029 |
| original | 3m | -0.04 | 4.07 | -4.11 | 41.8 | -0.06 |
| original | 6m | 2.25 | 6.73 | -4.48 | 44.7 | -0.076 |
| equal | 3m | -0.01 | 3.35 | -3.36 | 42.7 | -0.068 |
| equal | 6m | 1.93 | 6.93 | -5.0 | 43.5 | -0.119 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 81 |
| buy | 76 | 66 |
| hold | 49 | 45 |
| sell | 24 | 29 |
