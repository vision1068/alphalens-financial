# BetaLens back-test

2642 company-month observations, 494 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 15 | -2.41 | -2.46 | 53.3 | 26.7 |
| BUY | 25 | 5.1 | 1.09 | 48.0 | 48.0 |
| HOLD | 229 | 4.68 | -1.34 | 38.9 | 51.5 |
| SELL | 182 | 6.15 | -2.2 | 39.6 | 54.4 |
| STRONG_SELL | 43 | 12.87 | 0.16 | 39.5 | 53.5 |
| INSUFFICIENT_DATA | 2148 | 11.14 | -0.49 | 37.8 | 61.5 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 133 | 8.62 | 0.48 | 42.9 | 54.1 |
| Q2 | 89 | 4.98 | -1.63 | 36.0 | 48.3 |
| Q3 | 96 | 4.08 | -2.95 | 38.5 | 52.1 |
| Q4 | 89 | 2.11 | -4.48 | 34.8 | 48.3 |
| Q5 | 87 | 7.65 | 0.61 | 47.1 | 55.2 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 48 | 2.02 | -0.83 | 43.8 | 43.8 |
| BUY | 101 | 3.56 | -1.82 | 42.6 | 47.5 |
| HOLD | 197 | 5.22 | -2.3 | 35.5 | 51.8 |
| SELL | 102 | 7.7 | -0.27 | 45.1 | 58.8 |
| STRONG_SELL | 46 | 12.28 | -0.09 | 39.1 | 54.3 |

Overall score rank correlation with later out-performance: 0.129 (positive in 65.5% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.058 | 41 | 68.3 |
| dividend | 0.045 | 9 | 55.6 |
| price_trend | 0.019 | 47 | 48.9 |
| revenue_growth | 0.016 | 29 | 48.3 |
| earnings_growth | -0.026 | 29 | 37.9 |
| profitability | -0.03 | 41 | 46.3 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 9 | 1.66 | -1.46 | 55.6 | 66.7 |
| BUY | 16 | 3.69 | -2.43 | 43.8 | 62.5 |
| HOLD | 159 | 16.67 | 0.67 | 35.2 | 62.3 |
| SELL | 155 | 13.32 | -7.34 | 32.9 | 57.4 |
| STRONG_SELL | 37 | 20.32 | -4.69 | 37.8 | 56.8 |
| INSUFFICIENT_DATA | 2095 | 26.79 | 0.19 | 37.8 | 71.3 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 108 | 25.13 | 4.83 | 44.4 | 68.5 |
| Q2 | 66 | 12.54 | -4.41 | 28.8 | 63.6 |
| Q3 | 71 | 7.18 | -10.14 | 28.2 | 53.5 |
| Q4 | 66 | 8.22 | -8.76 | 28.8 | 54.5 |
| Q5 | 65 | 14.57 | -2.91 | 41.5 | 53.8 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 30 | 2.24 | -2.77 | 43.3 | 56.7 |
| BUY | 67 | 12.85 | -2.93 | 32.8 | 61.2 |
| HOLD | 155 | 17.68 | -1.57 | 33.5 | 60.6 |
| SELL | 85 | 13.34 | -6.29 | 37.6 | 61.2 |
| STRONG_SELL | 39 | 18.92 | -5.09 | 35.9 | 53.8 |

Overall score rank correlation with later out-performance: 0.238 (positive in 65.4% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.085 | 38 | 68.4 |
| revenue_growth | 0.033 | 26 | 61.5 |
| dividend | -0.019 | 6 | 33.3 |
| price_trend | -0.026 | 44 | 40.9 |
| profitability | -0.026 | 38 | 42.1 |
| earnings_growth | -0.042 | 26 | 34.6 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | -0.01 | 0.41 | -0.42 | 41.9 | 0.129 |
| current | 6m | 2.34 | -0.5 | 2.84 | 42.2 | 0.238 |
| original | 3m | -1.13 | 1.17 | -2.3 | 37.1 | 0.088 |
| original | 6m | 1.32 | 0.99 | 0.33 | 39.8 | 0.191 |
| equal | 3m | -1.01 | 0.57 | -1.58 | 39.0 | 0.084 |
| equal | 6m | -0.1 | 1.53 | -1.63 | 37.3 | 0.17 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 75 |
| buy | 76 | 61 |
| hold | 49 | 39 |
| sell | 24 | 26 |
