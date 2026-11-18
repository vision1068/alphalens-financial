"""US intraday refresh, every 30 minutes in US trading hours: S&P 500 prices and dividends going ex soon.

Real-time quotes in batches of 20 (including pre-market and after-hours trades) plus the dividend calendar.
Writes data/latest/us_live.json; scoring and alerts stay in the once-a-day pipeline.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from betalens.dividends import add_business_days
from betalens.us import parsers

OUT = Path(__file__).resolve().parents[2] / "data" / "latest"
NY = ZoneInfo("America/New_York")
LOOKAHEAD_DAYS = 8


def build_us_live(quotes: dict[str, dict], calendar: list[dict], symbols: set[str], now_utc: datetime) -> dict:
    prices = {s: {k: row.get(k) for k in ("price", "change", "change_pct", "volume", "previous_close", "market_status", "trade_date")}
              for s, row in quotes.items() if s in symbols}
    statuses = [row.get("market_status") for row in prices.values() if row.get("market_status")]
    upcoming = []
    for p in calendar:
        if p["symbol"] not in symbols:
            continue
        price = prices.get(p["symbol"], {}).get("price")
        upcoming.append(dict(p, last_buy_date=add_business_days(p["ex_date"], -1), price=price,
                             yield_pct=round(100 * p["amount_per_share"] / price, 2) if price else None))
    upcoming.sort(key=lambda u: (u["last_buy_date"], u["symbol"]))
    return {"as_of": now_utc.isoformat(timespec="seconds"), "prices": prices, "upcoming": upcoming,
            "market_status": max(set(statuses), key=statuses.count) if statuses else None}


def run() -> int:
    from betalens.us.sources import UsSources

    scores_path = OUT / "us_scores.json"
    if not scores_path.exists():
        print("No US scores yet; run the daily US pipeline first", file=sys.stderr)
        return 1
    symbols = {k["symbol"] for k in json.loads(scores_path.read_text())["scores"]}
    src = UsSources()
    quotes = {}
    for text in src.quotes(sorted(symbols)):
        quotes.update(parsers.parse_nasdaq_watchlist(text))
    live_path = OUT / "us_live.json"
    saved = json.loads(live_path.read_text()).get("prices", {}) if live_path.exists() else {}
    quotes, kept = parsers.keep_fresher(quotes, saved)
    if kept:
        print(f"Kept the saved price for {kept} symbols: Nasdaq returned an older trading session", file=sys.stderr)
    now = datetime.now(timezone.utc)
    today = now.astimezone(NY).date()
    calendar = []
    for i in range(0, LOOKAHEAD_DAYS + 1):
        day = today + timedelta(days=i)
        if day.weekday() < 5:
            try:
                calendar += parsers.parse_nasdaq_dividend_calendar(src.dividend_calendar(day))
            except Exception as e:  # keep going; the daily run covers dividends too
                print(f"Calendar {day} failed: {type(e).__name__}: {e}", file=sys.stderr)
    calendar = [p for p in calendar if p["ex_date"] > today]
    live = build_us_live(quotes, calendar, symbols, now)
    if not live["prices"]:
        print("No US prices parsed; keeping the previous us_live.json", file=sys.stderr)
        return 1
    live_path.write_text(json.dumps(live, indent=1, default=str))
    print(f"US live: {len(live['prices'])} prices, {len(live['upcoming'])} dividends going ex in the next week")
    return 0


if __name__ == "__main__":
    sys.exit(run())
