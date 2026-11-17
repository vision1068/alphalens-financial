"""Dividend agent: when to buy for a dividend, how far the price usually falls, and how fast it recovers.

For every past cash dividend on record the agent measures the fall on the ex-dividend day (adjusted for
the KSE-100's move that day) and the number of trading days the price took to get back to its
pre-dividend level. Upcoming dividends are then judged against that history and the analyst's signal.

Ex-date rule: a buyer must be on the register before the books close. With next-day settlement
(since 9 Feb 2026) the last day to buy is two trading days before the first book-closure day, and the
share trades ex-dividend on the trading day before the books close. Before that date settlement took
two days, so both fell one day earlier. `diagnostics` in the output tests this rule against prices.
"""
from __future__ import annotations

import bisect
from datetime import date, timedelta

from betalens.models import CompanyData

T1_START = date(2026, 2, 9)
EX_OFFSET_T1 = 1          # ex-date = this many trading days before the first book-closure day
EX_OFFSET_T2 = 2
RECOVERY_WINDOW = 60      # trading days to look for a recovery
QUICK_RECOVERY = 20       # "recovered quickly" threshold, trading days
MIN_EVENTS = 2            # past dividends needed before a company's own history is trusted
MIN_QUICK_SHARE = 0.6     # share of past dividends that must have recovered quickly
BUY_SIGNALS = {"BUY", "STRONG_BUY"}


def ex_offset(book_closure_from: date) -> int:
    return EX_OFFSET_T1 if book_closure_from >= T1_START else EX_OFFSET_T2


def _median(values: list[float]) -> float | None:
    v = sorted(values)
    if not v:
        return None
    mid = len(v) // 2
    return v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2


def _adjusted_drop(c: CompanyData, ex: int) -> float | None:
    """Rupee fall on trading day `ex` versus the prior close, net of the index's move that day."""
    if ex < 1 or ex >= len(c.closes):
        return None
    prior = c.closes[ex - 1]
    market = c.index_closes[ex] / c.index_closes[ex - 1] if len(c.index_closes) > ex else 1.0
    return prior * market - c.closes[ex]


def event_date(payout: dict) -> date | None:
    """The date that decides entitlement: the ex-date where it is published (US), else the book closure (PSX)."""
    return payout.get("ex_date") or payout.get("book_closure_from")


def measure_event(c: CompanyData, payout: dict, offset: int | None = None) -> dict | None:
    """Price behaviour around one past cash dividend. None if it cannot be measured from the price history."""
    amount = payout.get("amount_per_share")
    if payout.get("kind") != "cash" or not amount:
        return None
    if payout.get("ex_date"):                                      # US: ex-date published directly
        ex = bisect.bisect_left(c.price_dates, payout["ex_date"])
        if ex >= len(c.price_dates):
            return None
    else:
        start = payout.get("book_closure_from")
        if not start:
            return None
        first_closed = bisect.bisect_left(c.price_dates, start)   # first trading day on or after books close
        if first_closed >= len(c.price_dates):
            return None
        ex = first_closed - (ex_offset(start) if offset is None else offset)
    drop = _adjusted_drop(c, ex)
    if drop is None:
        return None
    cum_close = c.closes[ex - 1]
    recovery = next((d for d in range(min(RECOVERY_WINDOW, len(c.closes) - ex))
                     if c.closes[ex + d] >= cum_close), None)
    days_observed = len(c.closes) - ex
    event = {"ex_date": c.price_dates[ex], "last_buy_date": c.price_dates[ex - 1], "amount_per_share": amount,
             "cum_close": cum_close, "yield_pct": round(100 * amount / cum_close, 2),
             "drop_ratio": round(drop / amount, 2),            # 1.0 = fell by exactly the dividend
             "recovery_days": recovery,
             "recovery_known": recovery is not None or days_observed >= RECOVERY_WINDOW}
    for d in (5, 10, 20):
        if ex + d < len(c.closes):
            event[f"capture_{d}d_pct"] = round(100 * (c.closes[ex + d] + amount - cum_close) / cum_close, 2)
    return event


def company_history(events: list[dict]) -> dict:
    known = [e for e in events if e["recovery_known"]]
    quick = [e for e in known if e["recovery_days"] is not None and e["recovery_days"] <= QUICK_RECOVERY]
    captures = [e["capture_10d_pct"] for e in events if "capture_10d_pct" in e]
    return {"events": len(events),
            "median_drop_ratio": _median([e["drop_ratio"] for e in events]),
            "median_recovery_days": _median([e["recovery_days"] for e in known if e["recovery_days"] is not None]),
            "quick_recovery_share": round(len(quick) / len(known), 2) if known else None,
            "avg_capture_10d_pct": round(sum(captures) / len(captures), 2) if captures else None}


def add_business_days(day: date, n: int) -> date:
    """Step n weekdays (negative = back). Public holidays are not known in advance and are not skipped."""
    step = 1 if n > 0 else -1
    for _ in range(abs(n)):
        day += timedelta(days=step)
        while day.weekday() >= 5:
            day += timedelta(days=step)
    return day


def upcoming_dates(book_closure_from: date) -> tuple[date, date]:
    """(last buy date, ex-date) for a book closure that has not happened yet."""
    first_closed = book_closure_from
    while first_closed.weekday() >= 5:
        first_closed += timedelta(days=1)
    ex = add_business_days(first_closed, -ex_offset(book_closure_from))
    return add_business_days(ex, -1), ex


def assess(payout: dict, card: dict, history: dict | None, universe_drop_ratio: float | None, today: date) -> dict:
    """Verdict on one upcoming cash dividend."""
    if payout.get("ex_date"):          # US: buy by the close of the trading day before the ex-date
        ex = payout["ex_date"]
        last_buy = add_business_days(ex, -1)
    else:
        last_buy, ex = upcoming_dates(payout["book_closure_from"])
    price = card.get("price")
    amount = payout["amount_per_share"]
    own = history and history["events"] >= MIN_EVENTS
    ratio = history["median_drop_ratio"] if own else universe_drop_ratio
    reasons, ok = [], True
    if last_buy < today:
        ok = False
        reasons.append("The last buying day has passed")
    if card.get("signal") not in BUY_SIGNALS:
        ok = False
        reasons.append(f"Analyst signal is {card.get('signal', 'unknown').replace('_', ' ').title()}, not Buy")
    if card.get("red_flags"):
        ok = False
        reasons.append("Data warning on this company")
    if not own:
        ok = False
        reasons.append("Fewer than two past dividends on record to judge recovery")
    elif history["quick_recovery_share"] is None or history["quick_recovery_share"] < MIN_QUICK_SHARE:
        ok = False
        reasons.append(f"Price recovered within {QUICK_RECOVERY} trading days after only "
                       f"{round(100 * (history['quick_recovery_share'] or 0))}% of past dividends")
    else:
        reasons.append(f"Price recovered within {QUICK_RECOVERY} trading days after "
                       f"{round(100 * history['quick_recovery_share'])}% of {history['events']} past dividends")
    return {"symbol": payout["symbol"], "stage": payout["stage"], "percent": payout["percent"],
            "amount_per_share": amount, "price": price,
            "yield_pct": round(100 * amount / price, 2) if price else None,
            "book_closure_from": payout.get("book_closure_from"), "book_closure_to": payout.get("book_closure_to"),
            "payment_date": payout.get("payment_date"),
            "last_buy_date": last_buy, "ex_date": ex,
            "expected_drop_rs": round(ratio * amount, 2) if ratio is not None else None,
            "expected_drop_basis": "own history" if own else "market average",
            "median_recovery_days": history["median_recovery_days"] if own else None,
            "score": card.get("score"), "signal": card.get("signal"),
            "verdict": "WORTH_A_LOOK" if ok else "SKIP", "reasons": reasons}


def run_agent(companies: list[CompanyData], cards: dict[str, dict], today: date) -> dict:
    histories, all_events, diagnostics = {}, [], {}
    for c in companies:
        events = [e for p in c.payouts if event_date(p) and event_date(p) <= today and (e := measure_event(c, p))]
        if events:
            histories[c.symbol] = dict(company_history(events), recent=events[:6])
            all_events += events
    for regime, in_regime in (("t1_since_feb_2026", lambda d: d >= T1_START), ("t2_before", lambda d: d < T1_START)):
        diagnostics[regime] = {}
        for offset in range(0, 4):
            ratios = [e["drop_ratio"] for c in companies for p in c.payouts
                      if p.get("book_closure_from") and p["book_closure_from"] <= today and in_regime(p["book_closure_from"])
                      and (e := measure_event(c, p, offset))]
            diagnostics[regime][f"ex_{offset}_days_before_closure"] = {"events": len(ratios), "median_drop_ratio": _median(ratios)}
    universe_ratio = _median([e["drop_ratio"] for e in all_events])
    upcoming = [assess(dict(p, symbol=c.symbol), cards.get(c.symbol, {}), histories.get(c.symbol), universe_ratio, today)
                for c in companies for p in c.payouts
                if p["kind"] == "cash" and p.get("amount_per_share") and event_date(p) and event_date(p) > today]
    upcoming.sort(key=lambda u: (u["last_buy_date"], u["symbol"]))
    known = [e for e in all_events if e["recovery_known"]]
    summary = {"events": len(all_events), "median_drop_ratio": universe_ratio,
               "quick_recovery_share": round(sum(1 for e in known if e["recovery_days"] is not None
                                                 and e["recovery_days"] <= QUICK_RECOVERY) / len(known), 2) if known else None,
               "median_recovery_days": _median([e["recovery_days"] for e in known if e["recovery_days"] is not None])}
    return {"summary": summary, "upcoming": upcoming, "companies": histories, "diagnostics": diagnostics}
