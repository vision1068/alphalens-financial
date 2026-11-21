# BetaLens back-test

3139 company-month observations, 569 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 26 | 4.55 | 1.24 | 53.8 | 50.0 |
| HOLD | 274 | 5.02 | -1.18 | 36.5 | 49.6 |
| SELL | 179 | 6.3 | -1.95 | 39.7 | 55.3 |
| STRONG_SELL | 54 | 10.2 | -0.36 | 40.7 | 53.7 |
| INSUFFICIENT_DATA | 2570 | 10.94 | -0.95 | 36.8 | 60.8 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 141 | 7.71 | -0.06 | 44.7 | 53.2 |
| Q2 | 115 | 5.54 | -1.51 | 33.0 | 51.3 |
| Q3 | 103 | 5.33 | -1.49 | 38.8 | 48.5 |
| Q4 | 115 | 4.04 | -2.99 | 34.8 | 51.3 |
| Q5 | 95 | 6.44 | -0.11 | 46.3 | 54.7 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 56 | 5.03 | -0.07 | 50.0 | 50.0 |
| BUY | 115 | 2.67 | -1.69 | 38.3 | 47.8 |
| HOLD | 227 | 6.16 | -1.53 | 35.2 | 50.7 |
| SELL | 117 | 6.93 | -1.07 | 43.6 | 58.1 |
| STRONG_SELL | 54 | 10.2 | -0.36 | 40.7 | 53.7 |

Overall score rank correlation with later out-performance: 0.148 (positive in 69.0% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.061 | 41 | 70.7 |
| dividend | 0.038 | 9 | 55.6 |
| revenue_growth | 0.023 | 29 | 58.6 |
| price_trend | 0.019 | 47 | 44.7 |
| earnings_growth | -0.01 | 29 | 41.4 |
| profitability | -0.026 | 41 | 43.9 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 16 | 3.28 | -2.46 | 43.8 | 62.5 |
| HOLD | 192 | 17.66 | 1.24 | 34.4 | 60.9 |
| SELL | 151 | 12.87 | -7.45 | 33.1 | 57.6 |
| STRONG_SELL | 45 | 16.52 | -4.43 | 37.8 | 53.3 |
| INSUFFICIENT_DATA | 2503 | 26.2 | -0.81 | 35.6 | 69.5 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 112 | 21.99 | 2.25 | 43.8 | 67.0 |
| Q2 | 87 | 18.97 | 1.53 | 32.2 | 64.4 |
| Q3 | 77 | 9.93 | -6.46 | 29.9 | 53.2 |
| Q4 | 87 | 8.6 | -8.86 | 29.9 | 56.3 |
| Q5 | 69 | 13.64 | -3.19 | 42.0 | 52.2 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 38 | 12.17 | -0.47 | 50.0 | 65.8 |
| BUY | 74 | 10.87 | -2.54 | 32.4 | 58.1 |
| HOLD | 177 | 19.5 | 0.78 | 35.0 | 61.6 |
| SELL | 98 | 11.28 | -8.54 | 33.7 | 57.1 |
| STRONG_SELL | 45 | 16.52 | -4.43 | 37.8 | 53.3 |

Overall score rank correlation with later out-performance: 0.237 (positive in 65.4% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.078 | 38 | 73.7 |
| revenue_growth | 0.017 | 26 | 57.7 |
| price_trend | -0.011 | 44 | 38.6 |
| profitability | -0.023 | 38 | 44.7 |
| earnings_growth | -0.031 | 26 | 42.3 |
| dividend | -0.047 | 6 | 33.3 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.65 | -0.19 | 0.84 | 45.1 | 0.148 |
| current | 6m | 3.5 | -0.84 | 4.34 | 44.8 | 0.237 |
| original | 3m | -0.08 | 0.53 | -0.61 | 43.4 | 0.092 |
| original | 6m | 1.84 | -0.59 | 2.43 | 43.7 | 0.202 |
| equal | 3m | -0.2 | -0.15 | -0.05 | 42.5 | 0.081 |
| equal | 6m | 1.58 | -0.09 | 1.67 | 42.5 | 0.168 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 78 |
| buy | 76 | 64 |
| hold | 49 | 41 |
| sell | 24 | 24 |
