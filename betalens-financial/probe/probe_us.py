"""One-off: which Nasdaq requests return the latest session while the US market is closed?"""
import json
import pathlib
import sys
import time

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from betalens.us.sources import BROWSER  # noqa: E402

OUT = pathlib.Path(__file__).parent / "out_us"
syms = sorted(json.loads((OUT.parents[1] / "data" / "latest" / "us_live.json").read_text())["prices"])
W = "https://api.nasdaq.com/api/quote/watchlist?"
q = lambda ss: W + "&".join(f"symbol={s.lower()}%7cstocks" for s in ss)
tests = [("3: nem nvda aapl", q(["NEM", "NVDA", "AAPL"])), ("1: A", q(["A"])), ("3: A AAPL ABBV", q(syms[:3])),
         ("5 first", q(syms[:5])), ("10 first", q(syms[:10])), ("20 first", q(syms[:20])),
         ("20 incl nem", q(["NEM"] + syms[:19])), ("3 again", q(["NEM", "NVDA", "AAPL"]))]
lines = []
for label, url in tests:
    r = requests.get(url, headers=BROWSER, timeout=60)
    rows = r.json().get("data") or []
    lines.append(f"{label}: {len(rows)} rows, " + ", ".join(
        f"{x['symbol']} {x['lastSalePrice']} {(x.get('lastTradeTimestampDateTime') or '')[:10]}" for x in rows[:3]))
    time.sleep(2)
r = requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&download=true", headers=BROWSER, timeout=90)
rows = {x["symbol"]: x for x in r.json()["data"]["rows"]}
lines.append("screener: " + ", ".join(f"{s} {rows[s]['lastsale']} {rows[s]['pctchange']}" for s in ("NEM", "NVDA", "AAPL", "A")))
(OUT / "cache_test.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
