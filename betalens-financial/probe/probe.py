"""Fetch token-gated PSX portal endpoints once and save the raw responses for parser development."""
import pathlib

from psxdata.constants import BASE_URL
from psxdata.scrapers.base import BaseScraper

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)
s = BaseScraper()
CALLS = [
    ("payouts_PSO.html", "POST", "/company/payouts", {"symbol": "PSO"}),
    ("payouts_HBL.html", "POST", "/company/payouts", {"symbol": "HBL"}),
    ("eod_PSO.json", "GET", "/timeseries/eod/PSO", None),
    ("eod_KSE100.json", "GET", "/timeseries/eod/KSE100", None),
    ("reports_PSO.html", "GET", "/company/reports/PSO", None),
    ("calendar.html", "POST", "/calendar", {"from": "2026-11-01", "to": "2026-12-31"}),
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
