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
    ("sec_tickers_ua2.json", "https://www.sec.gov/files/company_tickers.json", SEC_UA2),
    ("sec_facts_ua2_AAPL.json", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", SEC_UA2),
    ("nasdaq_hist5_AAPL.json", f"https://api.nasdaq.com/api/quote/AAPL/historical?assetclass=stocks&fromdate={today - timedelta(days=1825)}&todate={today}&limit=2000", WEB_UA),
    ("nasdaq_hist10_AAPL.json", f"https://api.nasdaq.com/api/quote/AAPL/historical?assetclass=stocks&fromdate={today - timedelta(days=3640)}&todate={today}&limit=3000", WEB_UA),
    ("nasdaq_hist5_SPY.json", f"https://api.nasdaq.com/api/quote/SPY/historical?assetclass=etf&fromdate={today - timedelta(days=1825)}&todate={today}&limit=2000", WEB_UA),
    ("nasdaq_fin_AAPL_annual.json", "https://api.nasdaq.com/api/company/AAPL/financials?frequency=1", WEB_UA),
    ("nasdaq_fin_JPM_annual.json", "https://api.nasdaq.com/api/company/JPM/financials?frequency=1", WEB_UA),
    ("nasdaq_summary_AAPL.json", "https://api.nasdaq.com/api/quote/AAPL/summary?assetclass=stocks", WEB_UA),
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
