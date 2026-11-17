from datetime import date, timedelta

from betalens import dividends as dv
from betalens.models import CompanyData


def weekdays(start: date, n: int) -> list[date]:
    out, d = [], start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def company(closes: list[float], start=date(2026, 3, 2)) -> CompanyData:
    return CompanyData("TEST", closes=closes, index_closes=[100.0] * len(closes), price_dates=weekdays(start, len(closes)))


def payout(book_from: date, amount=5.0, kind="cash") -> dict:
    return {"kind": kind, "stage": "final", "percent": amount * 10, "amount_per_share": amount if kind == "cash" else None,
            "book_closure_from": book_from, "book_closure_to": book_from + timedelta(days=2), "announced": book_from - timedelta(days=20)}


def test_ex_offset_follows_settlement_regime():
    assert dv.ex_offset(date(2026, 2, 9)) == 1 and dv.ex_offset(date(2026, 2, 6)) == 2


def test_measure_event_drop_and_recovery():
    # 10 flat days at 100, ex-day falls to 95 (the Rs 5 dividend), recovers to 100 three trading days later
    closes = [100.0] * 10 + [95.0, 96.0, 98.0, 100.0] + [101.0] * 70
    c = company(closes)
    book_from = c.price_dates[11]                       # books close the trading day after the ex-day (T+1)
    e = dv.measure_event(c, payout(book_from))
    assert e["ex_date"] == c.price_dates[10] and e["last_buy_date"] == c.price_dates[9]
    assert e["drop_ratio"] == 1.0 and e["recovery_days"] == 3 and e["recovery_known"]
    assert e["yield_pct"] == 5.0 and e["capture_5d_pct"] == 6.0      # 101 + 5 - 100
    assert dv.measure_event(c, payout(book_from, kind="bonus")) is None


def test_drop_is_adjusted_for_the_market():
    c = company([100.0] * 10 + [95.0] * 80)
    c.index_closes = [100.0] * 10 + [95.0] * 80           # whole market fell 5% the same day
    e = dv.measure_event(c, payout(c.price_dates[11]))
    assert e["drop_ratio"] == 0.0 and e["recovery_days"] is None and e["recovery_known"]


def test_unrecovered_recent_event_is_not_counted_as_known():
    c = company([100.0] * 10 + [95.0] * 5)
    e = dv.measure_event(c, payout(c.price_dates[11]))
    assert e["recovery_days"] is None and not e["recovery_known"]
    h = dv.company_history([e])
    assert h["quick_recovery_share"] is None and h["events"] == 1


def test_upcoming_dates_skip_weekends():
    # Books close Monday 23 Nov 2026: ex-date Friday 20 Nov, last buy Thursday 19 Nov
    assert dv.upcoming_dates(date(2026, 11, 23)) == (date(2026, 11, 19), date(2026, 11, 20))
    # Books close Thursday 19 Nov: ex-date Wednesday 18, last buy Tuesday 17
    assert dv.upcoming_dates(date(2026, 11, 19)) == (date(2026, 11, 17), date(2026, 11, 18))


def test_assess_verdicts():
    p = dict(payout(date(2026, 11, 26)), symbol="TEST")
    good_history = {"events": 4, "median_drop_ratio": 0.8, "median_recovery_days": 6, "quick_recovery_share": 0.75}
    buy = {"signal": "BUY", "score": 80, "price": 100.0, "red_flags": []}
    a = dv.assess(p, buy, good_history, 0.9, date(2026, 11, 16))
    assert a["verdict"] == "WORTH_A_LOOK" and a["expected_drop_rs"] == 4.0 and a["yield_pct"] == 5.0
    assert a["last_buy_date"] == date(2026, 11, 24) and a["expected_drop_basis"] == "own history"
    assert dv.assess(p, dict(buy, signal="HOLD"), good_history, 0.9, date(2026, 11, 16))["verdict"] == "SKIP"
    slow = dict(good_history, quick_recovery_share=0.25)
    assert dv.assess(p, buy, slow, 0.9, date(2026, 11, 16))["verdict"] == "SKIP"
    none = dv.assess(p, buy, None, 0.9, date(2026, 11, 16))
    assert none["verdict"] == "SKIP" and none["expected_drop_rs"] == 4.5 and none["expected_drop_basis"] == "market average"
    assert dv.assess(p, buy, good_history, 0.9, date(2026, 11, 25))["verdict"] == "SKIP"   # last buy day passed
    assert dv.assess(p, dict(buy, red_flags=["x"]), good_history, 0.9, date(2026, 11, 16))["verdict"] == "SKIP"


def test_run_agent_end_to_end():
    closes = [100.0] * 10 + [95.0, 96.0, 98.0, 100.0] + [101.0] * 30 + [96.0, 99.0, 101.0] + [102.0] * 70
    c = company(closes)
    c.payouts = [payout(date(2027, 1, 20)), payout(c.price_dates[45]), payout(c.price_dates[11])]
    today = c.price_dates[-1]
    out = dv.run_agent([c], {"TEST": {"signal": "BUY", "score": 80, "price": 102.0, "red_flags": []}}, today)
    assert out["companies"]["TEST"]["events"] == 2 and out["companies"]["TEST"]["quick_recovery_share"] == 1.0
    assert len(out["upcoming"]) == 1 and out["upcoming"][0]["verdict"] == "WORTH_A_LOOK"
    assert out["diagnostics"]["t1_since_feb_2026"]["ex_1_days_before_closure"]["median_drop_ratio"] == 1.0
    assert out["summary"]["events"] == 2


def test_expected_drop_is_capped_for_tiny_dividends():
    p = dict(payout(date(2026, 11, 26)), symbol="TEST")
    wild = {"events": 4, "median_drop_ratio": 6.6, "median_recovery_days": 1, "quick_recovery_share": 0.9}
    a = dv.assess(p, {"signal": "BUY", "score": 80, "price": 100.0, "red_flags": []}, wild, 0.9, date(2026, 11, 16))
    assert a["expected_drop_rs"] == 7.5          # 1.5 x the Rs 5 dividend
    negative = dict(wild, median_drop_ratio=-0.4)
    assert dv.assess(p, {"signal": "BUY", "price": 100.0, "red_flags": []}, negative, 0.9, date(2026, 11, 16))["expected_drop_rs"] == 0.0
