# BetaLens back-test

3093 company-month observations, 546 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 36 | 4.84 | -0.85 | 50.0 | 50.0 |
| BUY | 26 | 4.55 | 1.24 | 53.8 | 50.0 |
| HOLD | 262 | 4.07 | -1.69 | 37.0 | 49.6 |
| SELL | 179 | 6.3 | -1.95 | 39.7 | 55.3 |
| STRONG_SELL | 43 | 12.87 | 0.16 | 39.5 | 53.5 |
| INSUFFICIENT_DATA | 2547 | 10.97 | -0.87 | 36.9 | 60.7 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 140 | 7.72 | -0.14 | 44.3 | 52.9 |
| Q2 | 98 | 4.78 | -1.28 | 34.7 | 53.1 |
| Q3 | 116 | 5.88 | -1.88 | 38.8 | 50.0 |
| Q4 | 98 | 1.74 | -4.31 | 34.7 | 50.0 |
| Q5 | 94 | 6.78 | 0.02 | 44.7 | 53.2 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 54 | 4.63 | -0.15 | 50.0 | 50.0 |
| BUY | 112 | 3.2 | -1.4 | 38.4 | 49.1 |
| HOLD | 211 | 4.93 | -2.2 | 36.0 | 50.2 |
| SELL | 116 | 6.83 | -0.88 | 43.1 | 57.8 |
| STRONG_SELL | 53 | 11.25 | -0.94 | 39.6 | 52.8 |

Overall score rank correlation with later out-performance: 0.167 (positive in 75.9% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.065 | 41 | 73.2 |
| dividend | 0.045 | 9 | 55.6 |
| revenue_growth | 0.021 | 29 | 58.6 |
| price_trend | 0.019 | 47 | 46.8 |
| earnings_growth | -0.011 | 29 | 41.4 |
| profitability | -0.026 | 41 | 41.5 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 28 | 15.62 | 0.77 | 53.6 | 67.9 |
| BUY | 16 | 3.28 | -2.46 | 43.8 | 62.5 |
| HOLD | 180 | 15.23 | -0.19 | 33.3 | 60.6 |
| SELL | 151 | 12.87 | -7.45 | 33.1 | 57.6 |
| STRONG_SELL | 37 | 20.32 | -4.69 | 37.8 | 56.8 |
| INSUFFICIENT_DATA | 2480 | 26.28 | -0.61 | 35.8 | 69.4 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 112 | 21.99 | 2.25 | 43.8 | 67.0 |
| Q2 | 72 | 15.12 | -0.77 | 30.6 | 65.3 |
| Q3 | 88 | 10.2 | -8.19 | 27.3 | 54.5 |
| Q4 | 72 | 7.73 | -8.19 | 31.9 | 55.6 |
| Q5 | 68 | 13.55 | -3.47 | 41.2 | 52.9 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 37 | 11.97 | -0.7 | 48.6 | 64.9 |
| BUY | 71 | 10.68 | -2.33 | 32.4 | 59.2 |
| HOLD | 160 | 17.63 | -0.15 | 35.0 | 61.9 |
| SELL | 98 | 10.39 | -9.2 | 32.7 | 58.2 |
| STRONG_SELL | 46 | 19.3 | -5.09 | 37.0 | 52.2 |

Overall score rank correlation with later out-performance: 0.254 (positive in 61.5% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.079 | 38 | 71.1 |
| revenue_growth | 0.022 | 26 | 61.5 |
| price_trend | -0.014 | 44 | 34.1 |
| profitability | -0.022 | 38 | 44.7 |
| earnings_growth | -0.031 | 26 | 38.5 |
| dividend | -0.049 | 6 | 33.3 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 0.87 | -0.08 | 0.95 | 45.5 | 0.167 |
| current | 6m | 3.74 | -1.03 | 4.77 | 45.3 | 0.254 |
| original | 3m | 0.13 | 1.34 | -1.21 | 43.8 | 0.112 |
| original | 6m | 2.1 | 0.36 | 1.74 | 44.2 | 0.217 |
| equal | 3m | 0.01 | 0.58 | -0.57 | 42.9 | 0.106 |
| equal | 6m | 1.8 | 0.91 | 0.89 | 43.0 | 0.196 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 79 |
| buy | 76 | 65 |
| hold | 49 | 42 |
| sell | 24 | 27 |
