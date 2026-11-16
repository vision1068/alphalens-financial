"""HTTP access to the PSX Data Portal. Uses psxdata's session for retries, rate limiting and the request token."""
from __future__ import annotations

from psxdata.constants import BASE_URL
from psxdata.scrapers.base import BaseScraper


class Portal:
    def __init__(self) -> None:
        self._s = BaseScraper()

    def _text(self, method: str, path: str, data: dict | None = None) -> str:
        kwargs = {"data": data} if data else {}
        return self._s._request(method, BASE_URL + path, **kwargs).text

    def company_page(self, symbol: str) -> str:
        return self._text("GET", f"/company/{symbol}")

    def payouts(self, symbol: str) -> str:
        return self._text("POST", "/company/payouts", {"symbol": symbol})

    def eod(self, symbol: str) -> str:
        return self._text("GET", f"/timeseries/eod/{symbol}")

    def index_page(self, name: str = "KSE100") -> str:
        return self._text("GET", f"/indices/{name}")

    def screener(self) -> str:
        return self._text("GET", "/screener")
