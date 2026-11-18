"""One-off: does Nasdaq's watchlist serve a stale cached copy for a repeated URL? Same batch with and
without a cache-busting parameter, plus Cache-Control: no-cache."""
import json
import pathlib
import sys
import time

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from betalens.us.sources import BROWSER  # noqa: E402

OUT = pathlib.Path(__file__).parent / "out_us"
OUT.mkdir(exist_ok=True)
syms = json.loads((OUT.parents[1] / "data" / "latest" / "us_live.json").read_text())["prices"]
batch = sorted(syms)[:20]
base = "https://api.nasdaq.com/api/quote/watchlist?" + "&".join(f"symbol={s.lower()}%7cstocks" for s in batch)
lines = []
for label, url, extra in [("same_url", base, {}), ("cache_buster", f"{base}&_={int(time.time())}", {}),
                          ("no_cache_header", base, {"Cache-Control": "no-cache", "Pragma": "no-cache"}),
                          ("same_url_again", base, {})]:
    r = requests.get(url, headers={**BROWSER, **extra}, timeout=60)
    rows = (r.json().get("data") or [])
    dates = sorted({(x.get("lastTradeTimestampDateTime") or "")[:10] for x in rows})
    lines.append(f"{label}: HTTP {r.status_code}, {len(rows)} rows, trade dates {dates}, "
                 f"age={r.headers.get('Age')} cache={r.headers.get('X-Cache') or r.headers.get('x-akamai-cache')} "
                 f"first={rows[0]['symbol'] if rows else None} {rows[0].get('lastSalePrice') if rows else None}")
    time.sleep(2)
(OUT / "cache_test.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
