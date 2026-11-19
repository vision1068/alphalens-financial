"""Choosing a US price we can trust.

Nasdaq's free servers are not always in step. On 18 Nov 2026, after Tuesday's close, the same request
returned Tuesday's prices one minute and Monday's the next, and its trade-date field was wrong too.
So we never trust Nasdaq's labels:

* While the US market is closed the price cannot move, so a closed-market quote is never used: the saved
  price stays, and the daily job replaces it with the official close from Nasdaq's dated daily history.
* While the market is open (pre-market, regular or after-hours) each saved price remembers the trading
  day ("session", New York date) and that day's previous close. A quote whose previous close shows it
  belongs to an older day than the one already saved is rejected, and its batch is asked again.
"""
from __future__ import annotations

import time
from datetime import datetime
from zoneinfo import ZoneInfo

from betalens.us import parsers

NY = ZoneInfo("America/New_York")


def session_of(now_utc: datetime) -> str:
    """The trading day a quote taken now belongs to (New York date)."""
    return now_utc.astimezone(NY).date().isoformat()


def is_closed(q: dict) -> bool:
    return (q.get("market_status") or "").strip().lower() in ("", "closed", "market closed")


def _same(a, b) -> bool:
    return a is not None and b is not None and abs(a - b) < 0.005


def acceptable(q: dict, saved: dict | None, session: str) -> bool:
    """Is this open-market quote at least as new as the saved price?"""
    if is_closed(q) or q.get("price") is None:
        return False
    if not saved or not saved.get("session"):
        return True
    if saved["session"] == session:   # same day: both must measure against the same previous close
        return saved.get("previous_close") is None or _same(q.get("previous_close"), saved["previous_close"])
    if saved["session"] < session:    # a new day: the saved day served again repeats the saved previous close
        return not _same(q.get("previous_close"), saved.get("previous_close"))
    return False


def choose(fresh: dict[str, dict], saved: dict[str, dict], session: str) -> tuple[dict[str, dict], int]:
    """Per symbol: the fresh quote if acceptable, else the saved price. Returns (prices, rejected count)."""
    out, rejected = {}, 0
    for s in set(fresh) | set(saved):
        q, old = fresh.get(s), saved.get(s)
        if q and acceptable(q, old, session):
            out[s] = {**q, "session": session}
        elif old:
            out[s] = {**old, "market_status": (q or old).get("market_status")}
            rejected += q is not None and not is_closed(q)
        elif q:
            out[s] = {**q, "session": None}
    return out, rejected


def fetch(src, symbols: list[str], saved: dict[str, dict], session: str, batch: int = 20,
          retries: int = 3, pause: float = 3.0) -> tuple[dict[str, dict], int]:
    """Quotes for all symbols; batches holding an out-of-date answer are asked again up to `retries` times."""
    batches = [symbols[i:i + batch] for i in range(0, len(symbols), batch)]
    fresh: dict[str, dict] = {}
    for b in batches:
        fresh.update(parsers.parse_nasdaq_watchlist(src.quote_batch(b)))

    def out_of_date(s):
        return s in fresh and not is_closed(fresh[s]) and not acceptable(fresh[s], saved.get(s), session)

    for _ in range(retries):
        behind = [b for b in batches if any(out_of_date(s) for s in b)]
        if not behind:
            break
        time.sleep(pause)
        for b in behind:
            for s, q in parsers.parse_nasdaq_watchlist(src.quote_batch(b)).items():
                if s not in fresh or acceptable(q, saved.get(s), session):
                    fresh[s] = q
    return choose(fresh, saved, session)


def official_close(history: list[dict], saved: dict | None) -> dict | None:
    """The latest official close from dated daily history, unless the saved price is from a later day."""
    if not history:
        return None
    last = history[-1]
    day = last["date"].isoformat() if hasattr(last["date"], "isoformat") else str(last["date"])
    if saved and saved.get("session") and saved["session"] > day:
        return None
    prev = history[-2]["close"] if len(history) > 1 else None
    change = round(last["close"] - prev, 4) if prev else None
    return {"price": last["close"], "previous_close": prev, "change": change,
            "change_pct": round(100 * change / prev, 2) if prev else None, "volume": last.get("volume"),
            "market_status": "Market Closed", "session": day}


def mostly_closed(prices: dict[str, dict]) -> bool:
    statuses = [is_closed(q) for q in prices.values()]
    return not statuses or sum(statuses) > len(statuses) / 2
