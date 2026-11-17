"""HTTP access to the free US sources: Wikipedia (S&P 500 list), SEC EDGAR (financials), Nasdaq (prices, dividends)."""
from __future__ import annotations

import os
import time
from datetime import date, timedelta

import requests

WIKI_SP500 = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
SP500_CSV_FALLBACK = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
SEC_FACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
NASDAQ = "https://api.nasdaq.com/api"
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
           "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9"}
# The SEC asks automated users to identify themselves with a name and contact address. Set the
# SEC_USER_AGENT secret to "Your Name you@example.com" to use your own.
SEC_UA = os.environ.get("SEC_USER_AGENT") or "BetaLens Financial admin@example.com"


class UsSources:
    def __init__(self, sec_pause: float = 0.15, nasdaq_pause: float = 0.35) -> None:
        self.s = requests.Session()
        self.sec_pause, self.nasdaq_pause = sec_pause, nasdaq_pause
        self._last: dict[str, float] = {}

    def _get(self, url: str, headers: dict, pace_key: str, pause: float, tries: int = 3) -> requests.Response:
        for attempt in range(tries):
            wait = self._last.get(pace_key, 0) + pause - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last[pace_key] = time.monotonic()
            try:
                r = self.s.get(url, headers=headers, timeout=60)
            except requests.RequestException:
                if attempt == tries - 1:
                    raise
                time.sleep(5 * (attempt + 1))
                continue
            if r.status_code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        raise RuntimeError(f"no response from {url}")

    def sp500_html(self) -> str:
        return self._get(WIKI_SP500, BROWSER, "wiki", 0).text

    def sp500_csv(self) -> str:
        return self._get(SP500_CSV_FALLBACK, BROWSER, "gh", 0).text

    def sec_facts(self, cik: int) -> dict:
        r = self._get(SEC_FACTS.format(cik=cik), {"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"},
                      "sec", self.sec_pause)
        return r.json()

    def _nasdaq(self, path: str) -> str:
        """Nasdaq sometimes answers 200 with an empty payload; retry those once."""
        for attempt in range(2):
            text = self._get(f"{NASDAQ}{path}", BROWSER, "nasdaq", self.nasdaq_pause).text
            if '"data":null' not in text.replace(" ", "") or attempt == 1:
                return text
            time.sleep(3)
        return text

    @staticmethod
    def variants(symbol: str) -> list[str]:
        """Share classes (BRK.B) are written differently across Nasdaq endpoints; try each spelling."""
        return [symbol] if "." not in symbol else [symbol, symbol.replace(".", "%2F"), symbol.replace(".", "")]

    def history(self, symbol: str, days: int, assetclass: str = "stocks", end: date | None = None) -> str:
        today = end or date.today()
        frm = today - timedelta(days=days)
        return self._nasdaq(f"/quote/{symbol}/historical?assetclass={assetclass}&fromdate={frm}&todate={today}"
                            f"&limit={min(int(days * 0.72) + 20, 3000)}")

    def screener(self) -> str:
        return self._nasdaq("/screener/stocks?tableonly=true&download=true")

    def dividend_history(self, symbol: str) -> str:
        return self._nasdaq(f"/quote/{symbol}/dividends?assetclass=stocks")

    def dividend_calendar(self, day: date) -> str:
        return self._nasdaq(f"/calendar/dividends?date={day}")
