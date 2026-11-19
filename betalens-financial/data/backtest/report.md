# BetaLens back-test

3139 company-month observations, 569 with enough data for a signal, from 2022-09-30 to 2026-07-31. Look-back setting: 3 year(s).

Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a total-return index, so out-performance is understated by roughly each share's dividend yield.

## 3m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|

## 6m after the signal

### By signal (current thresholds)

| Signal | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|

### By score rank each month (Q1 = top fifth)

| Quintile | Observations | Avg return % | Avg vs KSE-100 % | Beat index % | Rose % |
|---|---|---|---|---|---|

### Which factors predicted out-performance

| Factor | Rank correlation | Months | Months positive % |
|---|---|---|---|

## Alternative factor weightings

Top fifth and bottom fifth of scores each month, average return vs the KSE-100.

| Weighting | Horizon | Top fifth % | Bottom fifth % | Spread % | Top fifth beat index % | Rank correlation |
|---|---|---|---|---|---|---|

- `original`: valuation 12, revenue_growth 10, dividend 8, earnings_growth 12, profitability 12, price_trend 8
- `equal`: valuation 10, revenue_growth 10, dividend 10, earnings_growth 10, profitability 11, price_trend 11

## Suggested thresholds

Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.

| Band | Current | Suggested |
|---|---|---|
| strong_buy | 87 | 78 |
| buy | 76 | 64 |
| hold | 49 | 43 |
| sell | 24 | 26 |
