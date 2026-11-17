from datetime import date, datetime, timezone
from pathlib import Path

from betalens.data import parsers
from betalens.live import build_live
from betalens.pipeline import select_universe

FIX = Path(__file__).parent / "fixtures"
read = lambda name: (FIX / name).read_text(encoding="utf-8")
UCFG = {"shariah_only": True, "shariah_index": "KMIALLSHR", "dividend_watch_days": 30}


def test_market_watch_parses_prices_indices_and_strips_suffixes():
    mw = parsers.parse_market_watch(read("shariah_market_watch.html"))
    assert "HUBC" in mw and not any(" " in s for s in mw)                 # 'HUBC XD' -> 'HUBC'
    c = mw["CNERGY"]
    assert c["price"] == 11.45 and c["ldcp"] == 11.71 and c["change"] == -0.26 and c["change_pct"] == -2.22
    assert c["volume"] == 21257359 and "KSE100" in c["indices"] and "KMIALLSHR" in c["indices"]
    shariah = parsers.shariah_symbols(mw)
    assert "CNERGY" in shariah and "MZNPETF" not in shariah             # an ETF listed on the Shariah board but not in KMI


def test_market_payouts():
    rows = parsers.parse_market_payouts(read("market_payouts.html"), {"SNGP": 10.0})
    sngp = next(r for r in rows if r["symbol"] == "SNGP")
    assert sngp["kind"] == "cash" and sngp["percent"] == 30 and sngp["amount_per_share"] == 3.0
    assert sngp["book_closure_from"] == date(2026, 11, 20) and sngp["book_closure_to"] == date(2026, 11, 27)
    assert sngp["announced"] == date(2026, 11, 6) and not sngp["face_value_assumed"]
    thccl = next(r for r in rows if r["symbol"] == "THCCL")
    assert thccl["face_value_assumed"] and thccl["amount_per_share"] == 2.5
    assert not any(r["symbol"] == "ZAL" and r["announced"] == date(2026, 11, 2) for r in rows)   # right-issue text, no payout code


def test_universe_is_shariah_base_index_plus_shariah_dividend_payers():
    mw = parsers.parse_market_watch(read("shariah_market_watch.html"))
    payouts = parsers.parse_market_payouts(read("market_payouts.html"))
    universe, extras = select_universe(["CNERGY", "HBL", "PSO", "MEBL"], mw, payouts, UCFG, date(2026, 11, 17))
    assert universe[:3] == ["CNERGY", "PSO", "MEBL"]                     # HBL is not Shariah-compliant
    assert extras == {"SNGP", "THCCL"} and set(universe) == {"CNERGY", "PSO", "MEBL", "SNGP", "THCCL"}
    everything, none = select_universe(["HBL", "PSO"], mw, payouts, {"shariah_only": False}, date(2026, 11, 17))
    assert everything == ["HBL", "PSO"] and none == set()


def test_build_live_keeps_shariah_prices_and_future_cash_dividends():
    mw = parsers.parse_market_watch(read("shariah_market_watch.html"))
    payouts = parsers.parse_market_payouts(read("market_payouts.html"))
    allowed = parsers.shariah_symbols(mw)
    live = build_live(mw, payouts, allowed, date(2026, 11, 17), datetime(2026, 11, 17, 6, 7, tzinfo=timezone.utc))
    assert live["as_of"] == "2026-11-17T06:07:00+00:00" and "MZNPETF" not in live["prices"]
    assert [(u["symbol"], u["last_buy_date"], u["ex_date"]) for u in live["upcoming"]] == [
        ("THCCL", date(2026, 11, 17), date(2026, 11, 18)), ("SNGP", date(2026, 11, 18), date(2026, 11, 19))]
    sngp = live["upcoming"][1]
    assert sngp["price"] == mw["SNGP"]["price"] and sngp["yield_pct"] == round(300 / mw["SNGP"]["price"], 2)
