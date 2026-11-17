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
CALLS = [
    ("wiki_sp500.html", "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", WEB_UA),
    ("sec_tickers.json", "https://www.sec.gov/files/company_tickers.json", SEC_UA),
    ("sec_facts_AAPL.json", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", SEC_UA),
    ("sec_facts_JPM.json", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000019617.json", SEC_UA),
    ("nasdaq_screener.json", "https://api.nasdaq.com/api/screener/stocks?tableonly=true&download=true", WEB_UA),
    ("nasdaq_hist_AAPL.json", f"https://api.nasdaq.com/api/quote/AAPL/historical?assetclass=stocks&fromdate={today - timedelta(days=3650)}&todate={today}&limit=9999", WEB_UA),
    ("nasdaq_hist_SPY.json", f"https://api.nasdaq.com/api/quote/SPY/historical?assetclass=etf&fromdate={today - timedelta(days=3650)}&todate={today}&limit=9999", WEB_UA),
    ("nasdaq_div_AAPL.json", "https://api.nasdaq.com/api/quote/AAPL/dividends?assetclass=stocks", WEB_UA),
    ("nasdaq_divcal.json", f"https://api.nasdaq.com/api/calendar/dividends?date={today + timedelta(days=1)}", WEB_UA),
    ("stooq_aapl.csv", "https://stooq.com/q/d/l/?s=aapl.us&i=d", WEB_UA),
    ("stooq_spy.csv", "https://stooq.com/q/d/l/?s=spy.us&i=d", WEB_UA),
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
