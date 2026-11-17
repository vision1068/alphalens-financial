"""Daily US run: score the S&P 500 from free data, assess upcoming dividends, email new alerts (no AI notes).

    python -m betalens.us.pipeline                 # all S&P 500 companies
    python -m betalens.us.pipeline --symbols AAPL,KO
    python -m betalens.us.pipeline --backtest      # also a 10-year back-test (slower; run weekly)
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from betalens.dividends import run_agent
from betalens.models import CompanyData
from betalens.scoring.engine import load_config, score_company
from betalens.us import parsers

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "latest"
CONFIG = ROOT / "config" / "scorecard_us.yaml"
DAILY_HISTORY_DAYS = 800          # enough for the 200-day trend, a year of relative strength and past dividends
BACKTEST_HISTORY_DAYS = 3650
DIVIDEND_LOOKAHEAD_DAYS = 30
MAX_FAILURE_SHARE = 0.2


def sp500_from_csv(text: str) -> list[dict]:
    """Fallback list (datasets/s-and-p-500-companies on GitHub), same shape as parsers.parse_sp500."""
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        cik = r.get("CIK", "").strip()
        out.append({"symbol": r["Symbol"].strip(), "name": r.get("Security", ""), "sector": r.get("GICS Sector", "").upper(),
                    "sub_industry": r.get("GICS Sub-Industry", ""), "cik": int(cik) if cik.isdigit() else None})
    return out


def build_us_company(row: dict, facts: dict | None, history: list[dict], index_by_date: dict,
                     live: dict | None) -> CompanyData:
    """Assemble one S&P 500 company from SEC facts and Nasdaq prices. Pure: no network."""
    years, shares = parsers.years_from_sec(facts) if facts else ([], None)
    prices = [p for p in history if p["date"] in index_by_date] if index_by_date else history
    c = CompanyData(row["symbol"], name=row["name"], sector=row["sector"], market="US", years=years,
                    shares_outstanding=shares)
    c.closes = [p["close"] for p in prices]
    c.price_dates = [p["date"] for p in prices]
    c.index_closes = [index_by_date[p["date"]] for p in prices] if index_by_date else []
    c.price = (live or {}).get("price") or (history[-1]["close"] if history else None)
    if years and c.price:
        eps = years[0].eps
        c.pe_ratio = c.price / eps if eps else None
        recent = years[:5]
        dps = recent[0].dividend_per_share
        c.dividend_yield_pct = round(100 * dps / c.price, 2) if dps else 0.0
        c.dividend_years_paid = sum(1 for y in recent if y.dividend_per_share)
        c.dividend_window = len(recent)
    if years and years[0].profit_after_tax is not None and years[0].profit_after_tax < 0:
        c.red_flags.append("Loss in the latest fiscal year")
    if (c.pe_ratio and 0 < c.pe_ratio < 4) or (c.dividend_yield_pct and c.dividend_yield_pct > 12):
        c.red_flags.append("Unusually low P/E or high dividend yield: check for a one-off profit or special dividend "
                           "before relying on this score")
    return c


def sector_medians(companies: list[CompanyData]) -> dict[str, float]:
    groups: dict[str, list[float]] = {}
    for c in companies:
        if c.pe_ratio and c.pe_ratio > 0:
            groups.setdefault(c.sector, []).append(c.pe_ratio)
    out = {}
    for sector, v in groups.items():
        v.sort()
        m = len(v) // 2
        out[sector] = v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2
    return out


HISTORY_WINDOW_DAYS = 1500    # Nasdaq answers long ranges unreliably, so long histories are fetched in pieces


def fetch_history(src, symbol: str, days: int, assetclass: str = "stocks") -> list[dict]:
    for spelling in src.variants(symbol):
        rows: dict = {}
        end, left = date.today(), days
        try:
            while left > 0:
                span = min(left, HISTORY_WINDOW_DAYS)
                part = parsers.parse_nasdaq_history(src.history(spelling, span, assetclass, end))
                if not part:
                    break
                rows.update({r["date"]: r for r in part})
                end, left = end - timedelta(days=span), left - span
        except Exception:   # another spelling of a share-class symbol may still work
            pass
        if rows:
            return [rows[d] for d in sorted(rows)]
    return []


def upcoming_calendar(src, symbols: set[str], today: date, days: int) -> list[dict]:
    out = []
    for i in range(1, days + 1):
        day = today + timedelta(days=i)
        if day.weekday() >= 5:
            continue
        try:
            out += [p for p in parsers.parse_nasdaq_dividend_calendar(src.dividend_calendar(day)) if p["symbol"] in symbols]
        except Exception as e:  # one missing day should not stop the rest
            print(f"Dividend calendar {day} failed: {type(e).__name__}: {e}", file=sys.stderr)
    return out


def append_log(cards: list[dict], today: date, path: Path) -> None:
    day = today.isoformat()
    lines = path.read_text().splitlines() if path.exists() else ["date,symbol,score,coverage_pct,signal,price"]
    if any(line.startswith(day + ",") for line in lines):
        return
    lines += [f"{day},{k['symbol']},{k['score']},{k['coverage_pct']},{k['signal']},{k['price']}"
              for k in cards if k["score"] is not None]
    path.write_text("\n".join(lines) + "\n")


def send_alerts(cards: list[dict], upcoming: list[dict]) -> None:
    import yaml

    from betalens import alerts

    acfg = yaml.safe_load((ROOT / "config" / "alerts.yaml").read_text())
    state_path = ROOT / "data" / "alert_state_us.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    first_run = not state_path.exists()
    pending, new_state = alerts.find_alerts(cards, upcoming, state, acfg, set())
    if first_run:   # do not email the whole current list on the first day; alert on changes from now on
        state_path.write_text(json.dumps(new_state, indent=1))
        print(f"US alerts: first run, recorded {len(new_state)} states without emailing")
        return
    if not pending:
        state_path.write_text(json.dumps(new_state, indent=1))
        print("US alerts: none new")
        return
    try:
        url = (acfg.get("dashboard_url") or "")
        if alerts.send(*alerts.compose(pending, {}, url, market="US", currency="$")):
            state_path.write_text(json.dumps(new_state, indent=1))
            print(f"US alerts: sent {len(pending)}")
    except Exception as e:  # scores must still be saved; retried next run
        print(f"US email failed, will retry next run: {type(e).__name__}: {e}", file=sys.stderr)


def run(symbols: list[str] | None = None, backtest: bool = False) -> int:
    from betalens.us.sources import UsSources

    src, cfg, today = UsSources(), load_config(CONFIG), date.today()
    try:
        universe = parsers.parse_sp500(src.sp500_html())
    except Exception as e:
        print(f"Wikipedia list failed ({type(e).__name__}); using the GitHub copy", file=sys.stderr)
        universe = []
    if len(universe) < 450:
        universe = sp500_from_csv(src.sp500_csv())
    if symbols:
        universe = [r for r in universe if r["symbol"] in symbols]
    days = BACKTEST_HISTORY_DAYS if backtest else DAILY_HISTORY_DAYS
    live = parsers.parse_nasdaq_screener(src.screener())
    index_by_date = {p["date"]: p["close"] for p in fetch_history(src, "SPY", days, "etf")}
    print(f"US benchmark (SPY): {len(index_by_date)} trading days")

    companies, errors = [], {}
    for row in universe:
        try:
            facts = src.sec_facts(row["cik"]) if row.get("cik") else None
        except Exception as e:  # keep the company with prices only; it will show as not enough data
            errors[row["symbol"]] = f"SEC {type(e).__name__}: {e}"
            facts = None
        try:
            history = fetch_history(src, row["symbol"], days)
            companies.append(build_us_company(row, facts, history, index_by_date, live.get(row["symbol"])))
        except Exception as e:
            errors[row["symbol"]] = f"{type(e).__name__}: {e}"
            print(f"FAILED {row['symbol']}: {errors[row['symbol']]}", file=sys.stderr)

    lengths = sorted(len(c.closes) for c in companies)
    if lengths:
        print(f"US price history: median {lengths[len(lengths) // 2]} days, shortest {lengths[0]}, longest {lengths[-1]}")
    medians = sector_medians(companies)
    for c in companies:
        c.sector_pe_median = medians.get(c.sector)

    by_symbol = {c.symbol: c for c in companies}
    calendar = upcoming_calendar(src, set(by_symbol), today, DIVIDEND_LOOKAHEAD_DAYS)
    for symbol in sorted({p["symbol"] for p in calendar}):
        try:
            past = []
            for spelling in src.variants(symbol):
                try:
                    past = parsers.parse_nasdaq_dividend_history(src.dividend_history(spelling))
                except Exception:
                    continue
                if past:
                    break
        except Exception as e:
            print(f"Dividend history {symbol} failed: {type(e).__name__}: {e}", file=sys.stderr)
            past = []
        future = [dict(p) for p in calendar if p["symbol"] == symbol]
        known = {p["ex_date"] for p in future}
        by_symbol[symbol].payouts = future + [p for p in past if p["ex_date"] not in known]

    cards = []
    for c in companies:
        card = asdict(score_company(c, cfg))
        card.update(name=c.name, sector=c.sector, price=c.price, market="US",
                    change_pct=(live.get(c.symbol) or {}).get("change_pct"))
        cards.append(card)
    cards.sort(key=lambda k: (k["score"] is None, -(k["score"] or 0)))
    agent = run_agent(companies, {k["symbol"]: k for k in cards}, today)
    sec_failed = sum(1 for v in errors.values() if v.startswith("SEC"))
    meta = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "market": "US",
            "universe": "S&P 500", "period_years": cfg["period_years"], "companies": len(cards),
            "errors": errors, "sec_failed": sec_failed}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "us_scores.json").write_text(json.dumps({"meta": meta, "scores": cards}, indent=1, default=str))
    (OUT / "us_dividend_agent.json").write_text(json.dumps({"meta": meta, **agent}, indent=1, default=str))
    append_log(cards, today, ROOT / "data" / "signal_log_us.csv")
    if os.environ.get("BETALENS_DAILY_ANALYSIS") == "1":
        send_alerts(cards, agent["upcoming"])
    else:
        print("US alerts skipped: not the scheduled daily analysis run")
    print(f"US: scored {len(cards)} companies, {len(errors)} with errors ({sec_failed} SEC), "
          f"{len(agent['upcoming'])} upcoming dividends")
    if backtest:
        from betalens.backtest import write_report
        write_report(companies, cfg, ROOT / "data" / "backtest_us")
    return 1 if len(errors) > MAX_FAILURE_SHARE * max(len(universe), 1) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", help="comma-separated symbols; default is the whole S&P 500")
    ap.add_argument("--backtest", action="store_true")
    args = ap.parse_args()
    sys.exit(run([s.strip().upper() for s in args.symbols.split(",")] if args.symbols else None, args.backtest))
