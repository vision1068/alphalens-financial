# BetaLens back-test

23184 company-month observations, 22871 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 3294 | 3.89 | -0.66 | 44.6 | 56.3 |
| BUY | 5103 | 4.31 | -0.47 | 45.4 | 58.7 |
| HOLD | 7764 | 3.8 | -0.82 | 44.2 | 58.2 |
| SELL | 3616 | 4.33 | -0.4 | 43.8 | 57.8 |
| STRONG_SELL | 3094 | 7.61 | 2.67 | 47.7 | 60.5 |
| INSUFFICIENT_DATA | 313 | 3.76 | -1.06 | 41.9 | 58.8 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 4601 | 4.39 | -0.32 | 45.6 | 57.3 |
| Q2 | 4567 | 3.83 | -0.88 | 44.5 | 58.4 |
| Q3 | 4576 | 3.75 | -0.96 | 44.1 | 58.6 |
| Q4 | 4567 | 4.3 | -0.41 | 44.2 | 58.3 |
| Q5 | 4560 | 6.38 | 1.67 | 46.4 | 58.8 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 2395 | 4.39 | -0.29 | 45.4 | 57.4 |
| BUY | 4579 | 3.92 | -0.67 | 45.2 | 57.3 |
| HOLD | 9200 | 3.92 | -0.77 | 44.2 | 58.5 |
| SELL | 4516 | 4.2 | -0.5 | 43.8 | 57.8 |
| STRONG_SELL | 2181 | 9.18 | 4.11 | 49.1 | 61.5 |

Overall score rank correlation with later out-performance: -0.009 (positive in 53.2% of 47 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| price_to_book | 0.066 | 47 | 57.4 |
| liquidity | 0.051 | 47 | 68.1 |
| price_trend | 0.02 | 47 | 57.4 |
| valuation | 0.011 | 47 | 53.2 |
| revenue_growth | 0.009 | 47 | 55.3 |
| profitability | -0.009 | 47 | 40.4 |
| debt | -0.016 | 47 | 53.2 |
| earnings_growth | -0.024 | 47 | 36.2 |
| cash_flow_quality | -0.03 | 47 | 29.8 |
| dividend | -0.039 | 47 | 40.4 |
| cash_conversion_cycle | -0.044 | 47 | 34.0 |

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 3172 | 7.61 | -2.03 | 41.3 | 59.4 |
| BUY | 4787 | 8.64 | -1.15 | 41.6 | 62.6 |
| HOLD | 7171 | 7.67 | -2.21 | 40.2 | 63.1 |
| SELL | 3345 | 8.7 | -1.26 | 39.6 | 60.2 |
| STRONG_SELL | 2911 | 16.97 | 6.8 | 45.7 | 65.4 |
| INSUFFICIENT_DATA | 301 | 7.33 | -2.89 | 42.2 | 61.1 |

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| Q1 | 4304 | 8.84 | -1.04 | 42.2 | 60.4 |
| Q2 | 4270 | 7.35 | -2.53 | 39.8 | 62.6 |
| Q3 | 4279 | 7.32 | -2.56 | 40.1 | 63.3 |
| Q4 | 4270 | 8.47 | -1.4 | 40.1 | 61.4 |
| Q5 | 4263 | 14.57 | 4.69 | 44.4 | 63.6 |

### By signal (suggested thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|
| STRONG_BUY | 2326 | 8.26 | -1.55 | 42.0 | 60.0 |
| BUY | 4317 | 8.2 | -1.29 | 41.3 | 60.6 |
| HOLD | 8499 | 7.79 | -2.17 | 40.4 | 63.5 |
| SELL | 4179 | 8.86 | -1.05 | 40.3 | 60.6 |
| STRONG_SELL | 2065 | 19.94 | 9.6 | 46.5 | 66.5 |

Overall score rank correlation with later out-performance: -0.019 (positive in 43.2% of 44 months).

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|
| price_to_book | 0.102 | 44 | 54.5 |
| price_trend | 0.077 | 44 | 70.5 |
| liquidity | 0.064 | 44 | 70.5 |
| revenue_growth | 0.022 | 44 | 63.6 |
| valuation | -0.002 | 44 | 40.9 |
| profitability | -0.021 | 44 | 40.9 |
| debt | -0.027 | 44 | 56.8 |
| earnings_growth | -0.047 | 44 | 31.8 |
| cash_flow_quality | -0.051 | 44 | 13.6 |
| cash_conversion_cycle | -0.057 | 44 | 34.1 |
| dividend | -0.058 | 44 | 31.8 |

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|
| current | 3m | -0.37 | 1.75 | -2.12 | 45.8 | -0.007 |
| current | 6m | -1.14 | 4.69 | -5.83 | 42.0 | -0.016 |
| original | 3m | -0.77 | 1.86 | -2.63 | 44.4 | -0.013 |
| original | 6m | -1.94 | 4.8 | -6.74 | 41.2 | -0.018 |
| equal | 3m | -0.71 | 1.8 | -2.51 | 44.4 | -0.015 |
| equal | 6m | -1.68 | 4.65 | -6.33 | 41.5 | -0.013 |

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 74 | 76 |
| buy | 66 | 68 |
| hold | 54 | 54 |
| sell | 44 | 41 |
