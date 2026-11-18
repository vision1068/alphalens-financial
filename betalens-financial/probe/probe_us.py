"""One-off: fetch candidate free US data endpoints and save raw responses."""
import json
import pathlib
import time
from datetime import date, timedelta

import requests

OUT = pathlib.Path(__file__).parent / "out_us"
OUT.mkdir(exist_ok=True)
SEC_UA = {"User-Agent": "BetaLens research betalens-bot@users.noreply.github.com"}
WEB_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
          "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9"}
today = date.today()
SEC_UA2 = {"User-Agent": "BetaLens Financial admin@example.com", "Accept-Encoding": "gzip, deflate"}
CALLS = [
    ("watchlist_closed.json", "https://api.nasdaq.com/api/quote/watchlist?symbol=nem%7cstocks&symbol=nvda%7cstocks&symbol=aapl%7cstocks", WEB_UA),
    ("info_NEM_closed.json", "https://api.nasdaq.com/api/quote/NEM/info?assetclass=stocks", WEB_UA),
    ("hist_NEM_closed.json", f"https://api.nasdaq.com/api/quote/NEM/historical?assetclass=stocks&fromdate={today - timedelta(days=10)}&todate={today}&limit=10", WEB_UA),
]
status = []
for name, url, headers in CALLS:
    try:
        r = requests.get(url, headers=headers, timeout=60)
        (OUT / name).write_bytes(r.content)
        status.append(f"{name} {r.status_code} {len(r.content)}")
    except Exception as e:  # one-off probe: record and continue
        status.append(f"{name} ERROR {type(e).__name__}: {e}")
    time.sleep(1)
(OUT / "_status.txt").write_text("\n".join(status) + "\n")
print("\n".join(status))
