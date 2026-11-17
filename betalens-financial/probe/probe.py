"""Fetch PSX portal endpoints once and save the raw responses for parser development."""
import pathlib

from psxdata.constants import BASE_URL
from psxdata.scrapers.base import BaseScraper

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)
s = BaseScraper()
CALLS = [
    ("market_watch.html", "GET", "/market-watch", None),
    ("shariah_market_watch.html", "GET", "/shariah/market-watch", None),
    ("shariah_symbols.json", "GET", "/shariah/symbols", None),
    ("kmiallshr.html", "GET", "/indices/KMIALLSHR", None),
    ("payouts_all.html", "POST", "/payouts", {"symbol": "", "count": 100, "offset": 0}),
]
status = []
for name, method, path, data in CALLS:
    try:
        r = s._request(method, BASE_URL + path, **({"data": data} if data else {}))
        (OUT / name).write_text(r.text, encoding="utf-8")
        status.append(f"{name} {r.status_code} {len(r.text)}")
    except Exception as e:  # record and continue: this is a one-off probe
        status.append(f"{name} ERROR {type(e).__name__}: {e}")
(OUT / "_status.txt").write_text("\n".join(status) + "\n")
print("\n".join(status))
