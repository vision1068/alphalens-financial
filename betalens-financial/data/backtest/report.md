# BetaLens back-test

2910 company-month observations, 531 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 19 | 6.89 | 0.4 | 47.4 | 57.9 |
| HOLD | 254 | 4.02 | -1.66 | 37.8 | 49.2 |
| SELL | 179 | 6.3 | -1.95 | 39.7 | 55.3 |
| STRONG_SELL | 43 | 12.87 | 0.16 | 39.5 | 53.5 |
| INSUFFICIENT_DATA | 2379 | 11.3 | -0.43 | 37.5 | 60.5 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 136 | 7.59 | -0.32 | 41.9 | 52.2 |
| Q2 | 95 | 4.87 | -1.47 | 37.9 | 53.7 |
| Q3 | 113 | 6.01 | -1.97 | 38.9 | 50.4 |
| Q4 | 95 | 1.97 | -4.34 | 33.7 | 50.5 |
| Q5 | 92 | 7.02 | 0.34 | 45.7 | 53.3 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 55 | 5.55 | -0.42 | 49.1 | 52.7 |
| BUY | 103 | 2.54 | -1.92 | 37.9 | 46.6 |
| HOLD | 213 | 5.05 | -2.1 | 36.2 | 50.7 |
| SELL | 107 | 7.18 | -0.64 | 43.9 | 58.9 |
| STRONG_SELL | 53 | 11.25 | -0.94 | 39.6 | 52.8 |

Overall score rank correlation with later out-performance: 0.155 (positive in 69.0% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.08 | 41 | 73.2 |
| price_trend | 0.031 | 47 | 46.8 |
| revenue_growth | 0.025 | 29 | 58.6 |
| dividend | -0.005 | 8 | 50.0 |
| earnings_growth | -0.005 | 29 | 41.4 |
| profitability | -0.015 | 41 | 43.9 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 12 | 1.76 | -5.22 | 33.3 | 50.0 |
| HOLD | 175 | 15.63 | -0.02 | 34.3 | 60.6 |
| SELL | 151 | 12.87 | -7.45 | 33.1 | 57.6 |
| STRONG_SELL | 37 | 20.32 | -4.69 | 37.8 | 56.8 |
| INSUFFICIENT_DATA | 2318 | 27.0 | 0.3 | 36.3 | 69.5 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 110 | 22.2 | 2.25 | 43.6 | 65.5 |
| Q2 | 69 | 15.75 | -0.77 | 30.4 | 65.2 |
| Q3 | 88 | 9.89 | -8.4 | 28.4 | 54.5 |
| Q4 | 69 | 7.98 | -8.57 | 30.4 | 55.1 |
| Q5 | 67 | 14.01 | -3.08 | 41.8 | 53.7 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 40 | 11.46 | -1.03 | 47.5 | 62.5 |
| BUY | 65 | 11.83 | -2.68 | 32.3 | 56.9 |
| HOLD | 163 | 17.21 | -0.72 | 34.4 | 61.3 |
| SELL | 89 | 10.89 | -8.72 | 33.7 | 59.6 |
| STRONG_SELL | 46 | 19.3 | -5.09 | 37.0 | 52.2 |

Overall score rank correlation with later out-performance: 0.247 (positive in 61.5% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.101 | 38 | 78.9 |
| revenue_growth | 0.029 | 26 | 65.4 |
| price_trend | 0.003 | 44 | 47.7 |
| profitability | -0.013 | 38 | 44.7 |
| earnings_growth | -0.025 | 26 | 46.2 |
| dividend | -0.11 | 5 | 0.0 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.57 | 0.19 | 0.38 | 43.6 | 0.155 |
| current | 6m | 3.14 | -0.7 | 3.84 | 43.5 | 0.247 |
| original | 3m | -0.45 | 1.42 | -1.87 | 40.9 | 0.103 |
| original | 6m | 1.52 | 0.71 | 0.81 | 41.2 | 0.211 |
| equal | 3m | -0.31 | 0.83 | -1.14 | 41.8 | 0.097 |
| equal | 6m | 1.43 | 1.27 | 0.16 | 41.2 | 0.191 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 76 |
| buy | 76 | 64 |
| hold | 49 | 41 |
| sell | 24 | 27 |
