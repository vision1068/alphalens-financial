# BetaLens back-test

2829 company-month observations, 518 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 19 | 6.89 | 0.4 | 47.4 | 57.9 |
| HOLD | 255 | 5.29 | -0.86 | 37.6 | 50.6 |
| SELL | 179 | 6.54 | -1.76 | 40.2 | 55.9 |
| STRONG_SELL | 29 | 21.11 | 11.0 | 55.2 | 72.4 |
| INSUFFICIENT_DATA | 2311 | 10.36 | -1.14 | 37.6 | 60.8 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 129 | 7.51 | -0.18 | 42.6 | 53.5 |
| Q2 | 94 | 6.05 | -0.42 | 38.3 | 51.1 |
| Q3 | 112 | 6.3 | -1.57 | 37.5 | 50.9 |
| Q4 | 94 | 3.65 | -2.82 | 33.0 | 51.1 |
| Q5 | 89 | 9.56 | 2.97 | 52.8 | 64.0 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 52 | 5.48 | -0.37 | 50.0 | 51.9 |
| BUY | 104 | 3.3 | -1.67 | 39.4 | 48.1 |
| HOLD | 206 | 6.13 | -1.33 | 35.0 | 51.5 |
| SELL | 101 | 8.74 | 1.25 | 45.5 | 59.4 |
| STRONG_SELL | 55 | 12.05 | 1.86 | 47.3 | 65.5 |

Overall score rank correlation with later out-performance: 0.054 (positive in 51.7% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.079 | 41 | 70.7 |
| price_trend | 0.027 | 47 | 46.8 |
| dividend | 0.009 | 8 | 50.0 |
| revenue_growth | 0.001 | 29 | 44.8 |
| earnings_growth | -0.024 | 29 | 37.9 |
| profitability | -0.034 | 41 | 39.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 12 | 1.76 | -5.22 | 33.3 | 50.0 |
| HOLD | 179 | 18.3 | 1.78 | 35.8 | 62.0 |
| SELL | 151 | 14.02 | -6.13 | 34.4 | 59.6 |
| STRONG_SELL | 23 | 38.6 | 18.55 | 52.2 | 69.6 |
| INSUFFICIENT_DATA | 2253 | 25.11 | -1.24 | 36.6 | 70.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 103 | 20.79 | 1.76 | 42.7 | 65.0 |
| Q2 | 69 | 21.06 | 4.54 | 39.1 | 58.0 |
| Q3 | 86 | 13.92 | -4.69 | 29.1 | 62.8 |
| Q4 | 69 | 8.3 | -8.21 | 31.9 | 52.2 |
| Q5 | 66 | 20.83 | 3.85 | 43.9 | 68.2 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 37 | 12.17 | -0.75 | 48.6 | 64.9 |
| BUY | 68 | 12.09 | -2.18 | 35.3 | 55.9 |
| HOLD | 158 | 19.88 | 1.2 | 34.8 | 63.9 |
| SELL | 84 | 14.8 | -4.93 | 36.9 | 61.9 |
| STRONG_SELL | 46 | 23.49 | 3.89 | 41.3 | 58.7 |

Overall score rank correlation with later out-performance: 0.087 (positive in 57.7% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.096 | 38 | 73.7 |
| price_trend | -0.006 | 44 | 40.9 |
| revenue_growth | -0.01 | 26 | 50.0 |
| profitability | -0.033 | 38 | 36.8 |
| earnings_growth | -0.053 | 26 | 30.8 |
| dividend | -0.069 | 5 | 20.0 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.56 | 2.37 | -1.81 | 43.0 | 0.054 |
| current | 6m | 3.29 | 4.78 | -1.49 | 44.0 | 0.087 |
| original | 3m | -0.35 | 2.88 | -3.23 | 41.1 | 0.032 |
| original | 6m | 1.71 | 6.06 | -4.35 | 41.7 | 0.057 |
| equal | 3m | -0.27 | 2.39 | -2.66 | 42.1 | 0.011 |
| equal | 6m | 1.67 | 6.2 | -4.53 | 41.7 | 0.027 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 78 |
| buy | 76 | 62 |
| hold | 49 | 42 |
| sell | 24 | 28 |
