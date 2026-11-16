"""Daily run: fetch KSE-100 data from the PSX portal, score every company, write JSON for the dashboard.

    python -m betalens.pipeline                 # all KSE-100 companies
    python -m betalens.pipeline --symbols PSO,HBL
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

from betalens.data import parsers
from betalens.data.manual import apply_manual, load_manual
from betalens.models import CompanyData
from betalens.scoring.engine import load_config, score_company

OUT = Path(__file__).resolve().parents[1] / "data" / "latest"
MAX_FAILURE_SHARE = 0.2


def build_company(symbol: str, page_html: str, payouts_html: str, eod_text: str, index_by_date: dict,
                  screener: dict, medians: dict, manual: dict, today: date) -> CompanyData:
    """Assemble one company's inputs from raw portal responses. Pure: no network."""
    c = parsers.parse_company_page(page_html, symbol)
    row = screener.get(c.symbol, {})
    c.pe_ratio = c.pe_ratio if c.pe_ratio is not None else row.get("pe_ratio")
    c.dividend_yield_pct = row.get("dividend_yield_pct")
    c.sector_pe_median = medians.get(row.get("sector_code"))
    c.payouts = parsers.parse_payouts(payouts_html, c.face_value or 10.0)
    if c.payouts:
        summary = parsers.dividend_summary(c.payouts, today)
        c.dividend_years_paid, c.dividend_window = summary["years_paid"], summary["window"]
    prices = [p for p in parsers.parse_eod(eod_text) if p["date"] in index_by_date] if index_by_date \
        else parsers.parse_eod(eod_text)
    c.closes = [p["close"] for p in prices]
    c.price_dates = [p["date"] for p in prices]
    c.index_closes = [index_by_date[p["date"]] for p in prices] if index_by_date else []
    apply_manual(c, manual)
    if (c.pe_ratio and 0 < c.pe_ratio < 4) or (c.dividend_yield_pct and c.dividend_yield_pct > 12):
        c.red_flags.append("Unusually low P/E or high dividend yield: check for a recent bonus issue, "
                           "share split or one-off profit before relying on this score")
    return c


def append_signal_log(cards: list[dict], today: date, path: Path) -> int:
    """Append today's score, signal and price per company, once per day. This is the live track record."""
    day = today.isoformat()
    existing = path.read_text().splitlines() if path.exists() else ["date,symbol,score,coverage_pct,signal,price"]
    if any(line.startswith(day + ",") for line in existing):
        return 0
    new = [f"{day},{k['symbol']},{k['score']},{k['coverage_pct']},{k['signal']},{k['price']}"
           for k in cards if k["score"] is not None]
    path.write_text("\n".join(existing + new) + "\n")
    return len(new)


def run(symbols: list[str] | None = None, backtest: bool = False) -> int:
    from betalens.data.portal import Portal  # imported here so tests need no network stack

    portal, cfg, manual, today = Portal(), load_config(), load_manual(), date.today()
    constituents = parsers.parse_index_constituents(portal.index_page("KSE100"))
    names = {r["symbol"]: r["name"] for r in constituents}
    symbols = symbols or [r["symbol"] for r in constituents]
    screener = parsers.parse_screener(portal.screener())
    medians = parsers.sector_pe_medians(screener)
    index_by_date = {p["date"]: p["close"] for p in parsers.parse_eod(portal.eod("KSE100"))}

    cards, dividends, errors, companies = [], [], {}, []
    for symbol in symbols:
        try:
            c = build_company(symbol, portal.company_page(symbol), portal.payouts(symbol), portal.eod(symbol),
                              index_by_date, screener, medians, manual, today)
            companies.append(c)
            card = asdict(score_company(c, cfg))
            card.update(name=c.name or names.get(symbol, ""), sector=c.sector, price=c.price)
            cards.append(card)
            dividends += [dict(p, symbol=symbol, price=c.price) for p in c.payouts]
        except Exception as e:  # one bad page must not stop the other 99; the run fails below if too many do
            errors[symbol] = f"{type(e).__name__}: {e}"
            print(f"FAILED {symbol}: {errors[symbol]}", file=sys.stderr)

    cards.sort(key=lambda k: (k["score"] is None, -(k["score"] or 0)))
    meta = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "period_years": cfg["period_years"], "companies": len(cards), "errors": errors}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "scores.json").write_text(json.dumps({"meta": meta, "scores": cards}, indent=1, default=str))
    (OUT / "dividends.json").write_text(json.dumps({"meta": meta, "payouts": dividends}, indent=1, default=str))
    from betalens.dividends import run_agent
    agent = run_agent(companies, {k["symbol"]: k for k in cards}, today)
    (OUT / "dividend_agent.json").write_text(json.dumps({"meta": meta, **agent}, indent=1, default=str))
    append_signal_log(cards, today, OUT.parent / "signal_log.csv")
    print(f"Scored {len(cards)} companies, {len(errors)} failed")
    if backtest:
        from betalens.backtest import write_report
        write_report(companies, cfg, OUT.parent / "backtest")
    return 1 if len(errors) > MAX_FAILURE_SHARE * len(symbols) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", help="comma-separated symbols; default is all KSE-100")
    ap.add_argument("--backtest", action="store_true", help="also write data/backtest/report.md and report.json")
    args = ap.parse_args()
    sys.exit(run([s.strip().upper() for s in args.symbols.split(",")] if args.symbols else None, args.backtest))
