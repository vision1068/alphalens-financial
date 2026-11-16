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
| `probe/` | Lists portal URLs for the probe workflow to fetch when page layouts need checking |

## How scoring works

Each factor scores 0-100 from plain arithmetic on reported figures. The overall score is the weighted
average of the factors that have data, and `coverage` is the share of total weight they represent.
No Buy/Sell signal is issued below `min_coverage`.

The free portal page supplies sales, profit, EPS, margins, P/E and prices. Cash flow, debt, liquidity and
cash-cycle factors need figures from the full financial statements.

## Run the tests

    pip install -r requirements.txt
    python -m pytest -q
