from datetime import date
from pathlib import Path

import pytest

from betalens.data import parsers
from betalens.data.manual import apply_manual, load_manual
from betalens.pipeline import build_company
from betalens.scoring.engine import load_config, score_company

FIX = Path(__file__).parent / "fixtures"
read = lambda name: (FIX / name).read_text(encoding="utf-8")


def test_payouts_hbl():
    rows = parsers.parse_payouts(read("payouts_HBL.html"), face_value=10)
    assert len(rows) == 8
    first = rows[0]
    assert first["kind"] == "cash" and first["stage"] == "interim" and first["percent"] == 60
    assert first["amount_per_share"] == 6.0
    assert first["announced"] == date(2026, 10, 23) and first["period_end"] == date(2026, 9, 30)
    assert first["book_closure_from"] == date(2026, 11, 3) and first["book_closure_to"] == date(2026, 11, 4)
    assert rows[3]["stage"] == "final" and rows[-1]["percent"] == 42.5


def test_payouts_handles_bonus_and_multiple_entries():
    html = ("<table><tr><th>Date</th><th>Financial Results</th><th>Details</th><th>Book Closure</th></tr>"
            "<tr><td>March 1, 2026 4:00 PM</td><td>31/12/2025(YR)</td><td>25%(F) (D) 10%(F) (B)</td>"
            "<td>20/03/2026 - 27/03/2026</td></tr></table>")
    cash, bonus = parsers.parse_payouts(html, face_value=10)
    assert cash["kind"] == "cash" and cash["amount_per_share"] == 2.5
    assert bonus["kind"] == "bonus" and bonus["amount_per_share"] is None


def test_dividend_summary():
    rows = parsers.parse_payouts(read("payouts_HBL.html"), face_value=10)
    s = parsers.dividend_summary(rows, date(2026, 11, 16))
    assert s["ttm_dividend_per_share"] == 24.0  # 6 + 6 + 6 + 6 announced in the last 12 months
    assert s["years_paid"] == 3 and s["window"] == 3


def test_eod_is_oldest_first():
    rows = parsers.parse_eod(read("eod_PSO.json"))
    assert len(rows) == 300 and rows[0]["date"] < rows[-1]["date"]
    assert rows[-1]["close"] == 368.01 and rows[-1]["open"] == 369.4
    assert parsers.parse_eod('{"status":0,"message":"x","data":[]}') == []


def test_manual_statements(tmp_path):
    f = tmp_path / "m.csv"
    f.write_text("symbol,year,equity,total_debt,current_assets,current_liabilities\n"
                 "pso,2026,\"250,000\",100000,900,600\n# note,,,,,\n")
    manual = load_manual(f)
    assert manual == {("PSO", 2026): {"equity": 250000, "total_debt": 100000, "current_assets": 900,
                                      "current_liabilities": 600}}
    c = parsers.parse_company_page(read("company_PSO.html"), "PSO")
    assert apply_manual(c, manual) == 1 and c.years[0].equity == 250000 and c.years[0].sales == 3050025916
    f.write_text("symbol,year,equity\nPSO,twenty,5\n")
    with pytest.raises(ValueError, match="line 2"):
        load_manual(f)
    assert load_manual(tmp_path / "missing.csv") == {}


def test_build_company_end_to_end_reaches_signal_on_free_data():
    index = {p["date"]: p["close"] for p in parsers.parse_eod(read("eod_KSE100.json"))}
    screener = {"PSO": {"sector_code": "0820", "pe_ratio": 5.53, "dividend_yield_pct": 2.7}}
    c = build_company("PSO", read("company_PSO.html"), read("payouts_PSO.html"), read("eod_PSO.json"),
                      index, screener, {"0820": 7.0}, {}, date(2026, 11, 16))
    assert len(c.closes) == len(c.index_closes) >= 200 and c.face_value == 10.0
    assert c.dividend_years_paid == 2 and c.sector_pe_median == 7.0
    card = score_company(c, load_config())
    scored = {f.name for f in card.factors if f.score is not None}
    assert scored == {"revenue_growth", "earnings_growth", "profitability", "valuation", "dividend", "price_trend"}
    assert card.coverage_pct == 62 and card.signal != "INSUFFICIENT_DATA"


def test_signal_log_appends_once_per_day(tmp_path):
    from betalens.pipeline import append_signal_log
    log = tmp_path / "signal_log.csv"
    cards = [{"symbol": "PSO", "score": 71.2, "coverage_pct": 62.0, "signal": "BUY", "price": 368.01},
             {"symbol": "NIL", "score": None, "coverage_pct": 0.0, "signal": "INSUFFICIENT_DATA", "price": 1.0}]
    assert append_signal_log(cards, date(2026, 11, 16), log) == 1
    assert append_signal_log(cards, date(2026, 11, 16), log) == 0
    assert append_signal_log(cards, date(2026, 11, 17), log) == 1
    lines = log.read_text().splitlines()
    assert lines[0].startswith("date,symbol") and lines[1] == "2026-11-16,PSO,71.2,62.0,BUY,368.01" and len(lines) == 3
