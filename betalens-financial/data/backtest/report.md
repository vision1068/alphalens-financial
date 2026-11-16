# BetaLens back-test

4537 company-month observations, 804 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 47 | 0.81 | -2.31 | 38.3 | 38.3 |
| BUY | 83 | 4.68 | 0.44 | 51.8 | 47.0 |
| HOLD | 372 | 5.41 | -0.36 | 40.3 | 50.3 |
| SELL | 222 | 7.06 | -0.62 | 37.8 | 53.2 |
| STRONG_SELL | 80 | 9.57 | -0.13 | 37.5 | 50.0 |
| INSUFFICIENT_DATA | 3733 | 10.73 | -1.19 | 37.6 | 62.0 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 193 | 7.48 | 0.37 | 46.1 | 49.2 |
| Q2 | 153 | 6.12 | 0.37 | 41.8 | 50.3 |
| Q3 | 159 | 7.44 | 0.57 | 40.3 | 54.7 |
| Q4 | 153 | 4.18 | -1.53 | 34.6 | 47.7 |
| Q5 | 146 | 3.9 | -2.33 | 37.7 | 47.9 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 83 | 3.92 | 0.24 | 49.4 | 45.8 |
| BUY | 152 | 4.8 | -0.11 | 42.8 | 50.0 |
| HOLD | 318 | 4.67 | -1.72 | 37.4 | 49.1 |
| SELL | 171 | 8.56 | 1.16 | 40.9 | 53.8 |
| STRONG_SELL | 80 | 9.57 | -0.13 | 37.5 | 50.0 |

Overall score rank correlation with later out-performance: 0.154 (positive in 75.9% of 29 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| dividend | 0.121 | 10 | 60.0 |
| revenue_growth | 0.072 | 29 | 75.9 |
| valuation | 0.072 | 41 | 78.0 |
| price_trend | 0.011 | 47 | 51.1 |
| earnings_growth | 0.005 | 29 | 41.4 |
| profitability | -0.016 | 41 | 41.5 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 39 | 7.48 | -3.68 | 30.8 | 43.6 |
| BUY | 50 | 6.64 | -0.39 | 44.0 | 54.0 |
| HOLD | 251 | 17.31 | 1.5 | 38.2 | 61.0 |
| SELL | 186 | 15.17 | -3.33 | 36.0 | 55.9 |
| STRONG_SELL | 66 | 17.29 | -2.99 | 45.5 | 57.6 |
| INSUFFICIENT_DATA | 3651 | 25.5 | -1.51 | 36.0 | 71.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 149 | 20.84 | 2.81 | 41.6 | 61.1 |
| Q2 | 110 | 13.12 | -1.71 | 38.2 | 56.4 |
| Q3 | 118 | 19.7 | 3.07 | 36.4 | 62.7 |
| Q4 | 110 | 9.3 | -5.47 | 32.7 | 54.5 |
| Q5 | 105 | 9.86 | -5.66 | 41.9 | 49.5 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 60 | 8.87 | -1.27 | 36.7 | 50.0 |
| BUY | 95 | 8.95 | -1.1 | 37.9 | 57.9 |
| HOLD | 226 | 18.43 | 1.25 | 37.6 | 59.3 |
| SELL | 145 | 15.46 | -3.5 | 37.2 | 56.6 |
| STRONG_SELL | 66 | 17.29 | -2.99 | 45.5 | 57.6 |

Overall score rank correlation with later out-performance: 0.211 (positive in 80.8% of 26 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| valuation | 0.098 | 38 | 89.5 |
| dividend | 0.074 | 7 | 42.9 |
| revenue_growth | 0.063 | 26 | 61.5 |
| price_trend | -0.01 | 44 | 47.7 |
| profitability | -0.019 | 38 | 47.4 |
| earnings_growth | -0.025 | 26 | 34.6 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | 1.69 | -2.14 | 3.83 | 47.0 | 0.154 |
| current | 6m | 3.97 | -3.64 | 7.61 | 43.1 | 0.211 |
| original | 3m | 0.11 | 0.02 | 0.09 | 44.5 | 0.113 |
| original | 6m | -0.35 | -2.1 | 1.75 | 39.0 | 0.167 |
| equal | 3m | 0.47 | -1.17 | 1.64 | 44.5 | 0.109 |
| equal | 6m | 0.21 | -1.97 | 2.18 | 40.7 | 0.151 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 81 |
| buy | 76 | 68 |
| hold | 49 | 43 |
| sell | 24 | 24 |
