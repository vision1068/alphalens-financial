# BetaLens Financial

PSX decision-support system: a 100-point analyst scorecard, a dividend agent, a dashboard and email alerts.
Decision support only. It never places trades and is not financial advice.

## Layout

| Path | What it is |
|---|---|
| `config/scorecard.yaml` | Factor weights, signal thresholds, 1- or 3-year look-back |
| `betalens/scoring/` | The ten factors and the engine that combines them |
| `betalens/data/parsers.py` | Parsers for PSX Data Portal pages |
| `tests/` | Unit tests, including real portal pages as fixtures |
| `betalens/pipeline.py` | Daily run: fetch, score, write `data/latest/*.json` |
| `data/manual_statements.csv` | Your own entries for the four statement-based factors |
| `data/latest/` | Latest scores and dividend records (written by the daily job) |
| `dashboard/` | The website: plain HTML, CSS and JS, no build step |
| `data/signal_log.csv` | Live record of every day's scores and signals |
| `probe/` | One-off script that saves raw portal responses when a page layout needs checking |

## How scoring works

Each factor scores 0-100 from plain arithmetic on reported figures. The overall score is the weighted
average of the factors that have data, and `coverage` is the share of total weight they represent.
No Buy/Sell signal is issued below `min_coverage`.

The free portal page supplies sales, profit, EPS, margins, P/E and prices. Cash flow, debt, liquidity and
cash-cycle factors need figures from the full financial statements.

## Entering statement figures by hand

The free portal has no balance sheet or cash flow data, so four factors (cash flow quality, cash
conversion cycle, debt, liquidity) stay empty until figures are supplied. Add one row per company per
fiscal year to `data/manual_statements.csv`. Money columns are in thousands of rupees, as printed in the
company's annual report; `dividend_per_share` is in rupees. Leave unknown cells blank. Saving the file on
GitHub re-runs the scoring.

| Column | Where to find it in the annual report |
|---|---|
| `equity` | Statement of financial position: total equity |
| `total_debt` | Long-term financing plus short-term borrowings |
| `ebit` | Profit before tax plus finance cost |
| `interest_expense` | Finance cost |
| `operating_cash_flow` | Cash flow statement: net cash from operating activities |
| `capex` | Cash flow statement: purchase of property, plant and equipment |
| `current_assets`, `current_liabilities` | Statement of financial position totals |
| `receivables` | Trade debts |
| `inventory` | Stock-in-trade |
| `payables` | Trade and other payables |
| `cost_of_sales` | Profit and loss: cost of sales |

## Dashboard

`dashboard/` is a static site. It reads `data/latest/*.json` and `data/backtest/report.json` straight from
GitHub at page load, so daily data updates never redeploy the site. Holdings entered under "My portfolio"
are stored in the browser only.

Deploy on Netlify: import this repository, deploy branch `betalens-financial` (change to `main` after the
final merge, and update the branch name in `dashboard/config.js`), base directory
`betalens-financial/dashboard`, no build command. `netlify.toml` skips deploys when the dashboard folder
has not changed.

## Run the tests

    pip install -r requirements.txt
    python -m pytest -q
