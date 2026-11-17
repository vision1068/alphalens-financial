"""Intraday refresh, every 30 minutes in market hours: live prices and newly announced dividends.

Two portal requests per run. No scoring, AI notes or alerts here; those run once a day in the pipeline.
Writes data/latest/live.json, which the dashboard reads on top of the daily analysis.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from betalens.data import parsers
from betalens.dividends import upcoming_dates

OUT = Path(__file__).resolve().parents[1] / "data" / "latest"
PSX_TZ = ZoneInfo("Asia/Karachi")


def build_live(market_watch: dict[str, dict], market_payouts: list[dict], allowed: set[str] | None,
               today: date, now_utc: datetime) -> dict:
    """Pure: prices for allowed symbols and their upcoming cash dividends with last buy and ex dates."""
    keep = (lambda s: s in allowed) if allowed is not None else (lambda s: True)
    prices = {s: {k: row[k] for k in ("price", "change", "change_pct", "volume", "ldcp", "high", "low")}
              for s, row in market_watch.items() if keep(s)}
    upcoming, seen = [], set()
    for p in market_payouts:
        key = (p["symbol"], p["book_closure_from"], p["percent"], p["stage"])
        if (not keep(p["symbol"]) or p["kind"] != "cash" or not p["book_closure_from"]
                or p["book_closure_from"] <= today or key in seen):
            continue
        seen.add(key)
        last_buy, ex = upcoming_dates(p["book_closure_from"])
        price = prices.get(p["symbol"], {}).get("price")
        upcoming.append(dict(p, last_buy_date=last_buy, ex_date=ex, price=price,
                             yield_pct=round(100 * p["amount_per_share"] / price, 2) if price and p["amount_per_share"] else None))
    upcoming.sort(key=lambda u: (u["last_buy_date"], u["symbol"]))
    return {"as_of": now_utc.isoformat(timespec="seconds"), "prices": prices, "upcoming": upcoming}


def run() -> int:
    import yaml

    from betalens.data.portal import Portal

    ucfg = yaml.safe_load((OUT.parents[1] / "config" / "universe.yaml").read_text())
    portal = Portal()
    market_watch = parsers.parse_market_watch(portal.market_watch(shariah=True))
    scores_path = OUT / "scores.json"
    face_values = {}
    if scores_path.exists():
        face_values = {k["symbol"]: k["face_value"] for k in json.loads(scores_path.read_text())["scores"]
                       if k.get("face_value")}
    payouts = parsers.parse_market_payouts(portal.market_payouts(), face_values)
    allowed = parsers.shariah_symbols(market_watch, ucfg.get("shariah_index", "KMIALLSHR")) \
        if ucfg.get("shariah_only", True) else None
    now = datetime.now(timezone.utc)
    live = build_live(market_watch, payouts, allowed, now.astimezone(PSX_TZ).date(), now)
    if not live["prices"]:
        print("No prices parsed from the market watch; keeping the previous live.json", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "live.json").write_text(json.dumps(live, indent=1, default=str))
    print(f"Live: {len(live['prices'])} prices, {len(live['upcoming'])} upcoming cash dividends")
    return 0


if __name__ == "__main__":
    sys.exit(run())
