"""HTTP access to the PSX Data Portal. Uses psxdata's session for retries, rate limiting and the request token."""
from __future__ import annotations

import time

from psxdata.constants import BASE_URL
from psxdata.exceptions import PSXConnectionError, PSXRateLimitError
from psxdata.scrapers.base import BaseScraper

RATE_LIMIT_WAITS = (20, 60, 120)   # seconds to wait after each "too many requests" reply before retrying
DROP_WAITS = (15, 45)              # seconds to wait when the portal drops the connection (seen 19 Nov 2026)


class Portal:
    def __init__(self) -> None:
        self._s = BaseScraper()

    def _text(self, method: str, path: str, data: dict | None = None) -> str:
        kwargs = {"data": data} if data else {}
        busy, drops = list(RATE_LIMIT_WAITS), list(DROP_WAITS)
        while True:
            try:
                return self._s._request(method, BASE_URL + path, **kwargs).text
            except PSXRateLimitError:
                if not busy:
                    raise
                time.sleep(busy.pop(0))
            except PSXConnectionError:   # psxdata already tried 3 times; give the portal a moment and try again
                if not drops:
                    raise
                time.sleep(drops.pop(0))

    def company_page(self, symbol: str) -> str:
        return self._text("GET", f"/company/{symbol}")

    def payouts(self, symbol: str) -> str:
        return self._text("POST", "/company/payouts", {"symbol": symbol})

    def eod(self, symbol: str) -> str:
        return self._text("GET", f"/timeseries/eod/{symbol}")

    def index_page(self, name: str = "KSE100") -> str:
        return self._text("GET", f"/indices/{name}")

    def market_watch(self, shariah: bool = True) -> str:
        """All listed symbols with live prices; the Shariah portal's version lists Shariah-compliant ones."""
        return self._text("GET", "/shariah/market-watch" if shariah else "/market-watch")

    def market_payouts(self, count: int = 300) -> str:
        """Latest payout announcements across all companies, newest first."""
        return self._text("POST", "/payouts", {"symbol": "", "count": count, "offset": 0})

    def screener(self) -> str:
        return self._text("GET", "/screener")
