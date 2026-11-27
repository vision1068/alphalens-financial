# BetaLens back-test

3203 company-month observations, 627 with enough data for a signal, from 2022-09-30 to 2026-08-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 39 | 3.48 | -1.81 | 46.2 | 46.2 |
| BUY | 30 | 3.74 | 0.82 | 53.3 | 50.0 |
| HOLD | 308 | 4.02 | -1.54 | 35.4 | 47.4 |
| SELL | 192 | 5.49 | -2.23 | 38.5 | 53.1 |
| STRONG_SELL | 57 | 9.51 | -0.52 | 40.4 | 52.6 |
| INSUFFICIENT_DATA | 2576 | 10.9 | -0.94 | 36.8 | 60.7 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 153 | 6.62 | -0.57 | 43.1 | 51.0 |
| Q2 | 126 | 5.05 | -1.42 | 34.9 | 51.6 |
| Q3 | 115 | 3.94 | -2.21 | 34.8 | 43.5 |
| Q4 | 126 | 3.38 | -3.07 | 34.9 | 50.8 |
| Q5 | 106 | 5.23 | -0.68 | 43.4 | 50.9 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 63 | 3.76 | -0.81 | 47.6 | 47.6 |
| BUY | 127 | 2.21 | -1.69 | 38.6 | 48.0 |
| HOLD | 246 | 5.0 | -1.94 | 33.7 | 47.6 |
| SELL | 130 | 6.02 | -1.48 | 41.5 | 54.6 |
| STRONG_SELL | 60 | 9.22 | -0.68 | 40.0 | 53.3 |

Overall score rank correlation with later out-performance: 0.145 (positive in 70.0% of 30 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.061 | 42 | 71.4 |
| dividend | 0.046 | 10 | 60.0 |
| revenue_growth | 0.023 | 30 | 60.0 |
| price_trend | 0.015 | 48 | 43.8 |
| earnings_growth | -0.005 | 30 | 43.3 |
| profitability | -0.023 | 42 | 45.2 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 16 | 3.28 | -2.46 | 43.8 | 62.5 |
| HOLD | 192 | 17.66 | 1.24 | 34.4 | 60.9 |
| SELL | 151 | 12.87 | -7.45 | 33.1 | 57.6 |
| STRONG_SELL | 45 | 16.52 | -4.43 | 37.8 | 53.3 |
| INSUFFICIENT_DATA | 2499 | 26.26 | -0.75 | 35.6 | 69.6 |

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
| BUY | 70 | 10.55 | -2.48 | 31.4 | 58.6 |
| HOLD | 172 | 20.17 | 1.45 | 36.0 | 62.2 |
| SELL | 105 | 11.12 | -8.92 | 33.3 | 57.1 |
| STRONG_SELL | 47 | 15.52 | -4.78 | 36.2 | 51.1 |

Overall score rank correlation with later out-performance: 0.237 (positive in 65.4% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.078 | 38 | 73.7 |
| revenue_growth | 0.017 | 26 | 57.7 |
| price_trend | -0.013 | 44 | 38.6 |
| profitability | -0.023 | 38 | 44.7 |
| earnings_growth | -0.031 | 26 | 42.3 |
| dividend | -0.047 | 6 | 33.3 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.1 | -0.67 | 0.77 | 43.5 | 0.145 |
| current | 6m | 3.5 | -0.84 | 4.34 | 44.8 | 0.237 |
| original | 3m | -0.66 | -0.04 | -0.62 | 42.7 | 0.091 |
| original | 6m | 1.84 | -0.59 | 2.43 | 43.7 | 0.202 |
| equal | 3m | -0.77 | -0.33 | -0.44 | 41.9 | 0.08 |
| equal | 6m | 1.58 | -0.09 | 1.67 | 42.5 | 0.168 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 78 |
| buy | 76 | 65 |
| hold | 49 | 42 |
| sell | 24 | 26 |
