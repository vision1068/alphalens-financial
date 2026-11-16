# BetaLens back-test

4628 company-month observations, 827 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 47 | 0.81 | -2.31 | 38.3 | 38.3 |
| BUY | 81 | 4.82 | 0.45 | 51.9 | 46.9 |
| HOLD | 391 | 5.32 | -0.67 | 39.4 | 50.1 |
| SELL | 228 | 6.96 | -0.6 | 38.2 | 53.1 |
| STRONG_SELL | 80 | 9.57 | -0.13 | 37.5 | 50.0 |
| INSUFFICIENT_DATA | 3801 | 10.78 | -1.14 | 37.8 | 62.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 193 | 7.48 | 0.37 | 46.1 | 49.2 |
| Q2 | 155 | 6.08 | 0.16 | 41.9 | 51.6 |
| Q3 | 177 | 6.77 | -0.17 | 37.9 | 52.5 |
| Q4 | 155 | 4.51 | -1.37 | 34.8 | 47.7 |
| Q5 | 147 | 3.91 | -2.28 | 38.1 | 48.3 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 83 | 3.92 | 0.24 | 49.4 | 45.8 |
| BUY | 171 | 4.31 | -0.36 | 41.5 | 48.5 |
| HOLD | 322 | 4.87 | -1.95 | 37.0 | 49.7 |
| SELL | 171 | 8.56 | 1.16 | 40.9 | 53.8 |
| STRONG_SELL | 80 | 9.57 | -0.13 | 37.5 | 50.0 |

Overall score rank correlation with later out-performance: 0.146 (positive in 79.3% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.113 | 10 | 60.0 |
| revenue_growth | 0.074 | 29 | 75.9 |
| valuation | 0.069 | 41 | 80.5 |
| price_trend | 0.008 | 47 | 48.9 |
| earnings_growth | 0.007 | 29 | 44.8 |
| profitability | -0.024 | 41 | 39.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 39 | 7.48 | -3.68 | 30.8 | 43.6 |
| BUY | 48 | 6.7 | -0.42 | 43.8 | 54.2 |
| HOLD | 270 | 16.68 | 0.65 | 36.3 | 60.4 |
| SELL | 189 | 15.13 | -3.3 | 36.0 | 56.6 |
| STRONG_SELL | 66 | 17.29 | -2.99 | 45.5 | 57.6 |
| INSUFFICIENT_DATA | 3716 | 25.64 | -1.39 | 36.3 | 71.3 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 149 | 20.84 | 2.81 | 41.6 | 61.1 |
| Q2 | 112 | 12.59 | -2.08 | 35.7 | 56.2 |
| Q3 | 133 | 18.84 | 1.35 | 34.6 | 62.4 |
| Q4 | 112 | 9.58 | -5.05 | 33.0 | 55.4 |
| Q5 | 106 | 9.65 | -5.75 | 41.5 | 49.1 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 60 | 8.87 | -1.27 | 36.7 | 50.0 |
| BUY | 107 | 10.45 | -0.53 | 38.3 | 57.9 |
| HOLD | 234 | 17.45 | 0.12 | 35.0 | 59.4 |
| SELL | 145 | 15.46 | -3.5 | 37.2 | 56.6 |
| STRONG_SELL | 66 | 17.29 | -2.99 | 45.5 | 57.6 |

Overall score rank correlation with later out-performance: 0.206 (positive in 80.8% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.097 | 38 | 92.1 |
| revenue_growth | 0.065 | 26 | 65.4 |
| dividend | 0.042 | 7 | 42.9 |
| price_trend | -0.01 | 44 | 50.0 |
| earnings_growth | -0.023 | 26 | 34.6 |
| profitability | -0.03 | 38 | 44.7 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 1.65 | -2.1 | 3.75 | 46.7 | 0.146 |
| current | 6m | 3.75 | -3.73 | 7.48 | 41.9 | 0.206 |
| original | 3m | 0.07 | 0.3 | -0.23 | 44.2 | 0.106 |
| original | 6m | -0.21 | -1.47 | 1.26 | 39.5 | 0.165 |
| equal | 3m | 0.47 | -0.84 | 1.31 | 44.2 | 0.098 |
| equal | 6m | 0.14 | -1.68 | 1.82 | 40.3 | 0.144 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 81 |
| buy | 76 | 67 |
| hold | 49 | 43 |
| sell | 24 | 24 |
