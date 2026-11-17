"""US intraday refresh, every 30 minutes in US trading hours: S&P 500 prices and dividends going ex soon.

One screener request (every US stock's latest price) plus the dividend calendar for the next week.
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


def build_us_live(screener: dict[str, dict], calendar: list[dict], symbols: set[str], now_utc: datetime) -> dict:
    prices = {s: {k: row[k] for k in ("price", "change", "change_pct", "volume")}
              for s, row in screener.items() if s in symbols}
    upcoming = []
    for p in calendar:
        if p["symbol"] not in symbols:
            continue
        price = prices.get(p["symbol"], {}).get("price")
        upcoming.append(dict(p, last_buy_date=add_business_days(p["ex_date"], -1), price=price,
                             yield_pct=round(100 * p["amount_per_share"] / price, 2) if price else None))
    upcoming.sort(key=lambda u: (u["last_buy_date"], u["symbol"]))
    return {"as_of": now_utc.isoformat(timespec="seconds"), "prices": prices, "upcoming": upcoming}


def run() -> int:
    from betalens.us.sources import UsSources

    scores_path = OUT / "us_scores.json"
    if not scores_path.exists():
        print("No US scores yet; run the daily US pipeline first", file=sys.stderr)
        return 1
    symbols = {k["symbol"] for k in json.loads(scores_path.read_text())["scores"]}
    src = UsSources()
    screener = parsers.parse_nasdaq_screener(src.screener())
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
    live = build_us_live(screener, calendar, symbols, now)
    if not live["prices"]:
        print("No US prices parsed; keeping the previous us_live.json", file=sys.stderr)
        return 1
    (OUT / "us_live.json").write_text(json.dumps(live, indent=1, default=str))
    print(f"US live: {len(live['prices'])} prices, {len(live['upcoming'])} dividends going ex in the next week")
    return 0


if __name__ == "__main__":
    sys.exit(run())
