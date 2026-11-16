"""Parsers for PSX Data Portal HTML pages. Pure functions: HTML in, plain data out.

Columns are located by header text, never by position, so a reordered table still parses.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone

from bs4 import BeautifulSoup

from betalens.models import CompanyData, YearFigures

REVENUE_LABELS = ("sales", "total income", "revenue", "net premium")


def to_number(text: str) -> float | None:
    """'1,234.5' -> 1234.5, '(27.93)' -> -27.93, '12.5%' -> 12.5, '' or '-' -> None."""
    t = text.strip().replace(",", "").replace("%", "").replace("Rs.", "")
    if not t or t in {"-", "—", "N/A"}:
        return None
    negative = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(t[-1:].upper())
    if mult:
        t = t[:-1]
    try:
        value = float(t) * (mult or 1)
    except ValueError:
        return None
    return -value if negative else value


def _table_rows(table) -> tuple[list[str], dict[str, list[str]]]:
    """Return (column headers after the first, {row label lowercased: cell texts})."""
    headers = [th.get_text(" ", strip=True) for th in table.find_all("th")][1:]
    rows: dict[str, list[str]] = {}
    for tr in table.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) >= 2:
            rows[cells[0].lower()] = cells[1:]
    return headers, rows


def _year_tables(section) -> list[tuple[list[str], dict[str, list[str]]]]:
    """Tables in a section whose headers are all 4-digit years (annual, not quarterly)."""
    out = []
    for table in section.find_all("table") if section else []:
        headers, rows = _table_rows(table)
        if headers and all(re.fullmatch(r"\d{4}", h) for h in headers):
            out.append((headers, rows))
    return out


def parse_company_page(html: str, symbol: str) -> CompanyData:
    """Parse https://dps.psx.com.pk/company/<SYMBOL> into CompanyData (annual figures, newest first)."""
    soup = BeautifulSoup(html, "lxml")
    c = CompanyData(symbol=symbol.upper())
    for attr, cls in (("name", "quote__name"), ("sector", "quote__sector")):
        el = soup.find(class_=cls)
        if el:
            setattr(c, attr, el.get_text(" ", strip=True))
    close = soup.find(class_="quote__close")
    if close:
        c.price = to_number(close.get_text(strip=True))
    for item in soup.find_all(class_="stats_item"):
        label = item.find(class_="stats_label")
        value = item.find(class_="stats_value")
        if not (label and value):
            continue
        key = label.get_text(strip=True).lower()
        if key.startswith("p/e ratio") and c.pe_ratio is None:
            c.pe_ratio = to_number(value.get_text(strip=True)) or None  # 0.00 means no earnings
        elif key == "face value":
            c.face_value = to_number(value.get_text(strip=True))

    by_year: dict[int, YearFigures] = {}
    for headers, rows in _year_tables(soup.find(id="financials")):
        revenue = next((rows[k] for k in rows if k in REVENUE_LABELS), None)
        pat = rows.get("profit after taxation")
        eps = rows.get("eps")
        for i, h in enumerate(headers):
            y = by_year.setdefault(int(h), YearFigures(year=int(h)))
            y.sales = to_number(revenue[i]) if revenue and i < len(revenue) else None
            y.profit_after_tax = to_number(pat[i]) if pat and i < len(pat) else None
            y.eps = to_number(eps[i]) if eps and i < len(eps) else None
    for headers, rows in _year_tables(soup.find(id="ratios")):
        gross = rows.get("gross profit margin (%)")
        net = rows.get("net profit margin (%)")
        for i, h in enumerate(headers):
            y = by_year.setdefault(int(h), YearFigures(year=int(h)))
            y.gross_margin_pct = to_number(gross[i]) if gross and i < len(gross) else None
            y.net_margin_pct = to_number(net[i]) if net and i < len(net) else None
    c.years = [by_year[k] for k in sorted(by_year, reverse=True)]
    if c.years and c.years[0].profit_after_tax is not None and c.years[0].profit_after_tax < 0:
        c.red_flags.append("Loss in the latest fiscal year")
    return c


def _table_as_dicts(html: str, required: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    for table in soup.find_all("table"):
        headers = [th.get_text(" ", strip=True).upper() for th in table.find_all("th")]
        if required in headers:
            out = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
                if len(cells) == len(headers):
                    out.append(dict(zip(headers, cells)))
            return out
    return []


def parse_index_constituents(html: str) -> list[dict]:
    """Parse https://dps.psx.com.pk/indices/KSE100 into [{symbol, name, weight_pct, price}]."""
    out = []
    for row in _table_as_dicts(html, "SYMBOL"):
        symbol = row["SYMBOL"].split()[0]  # drop status suffixes such as 'XD'
        out.append({
            "symbol": symbol,
            "name": row.get("NAME", ""),
            "weight_pct": to_number(row.get("IDX WTG (%)", "")),
            "price": to_number(row.get("CURRENT", "")),
        })
    return out


def parse_screener(html: str) -> dict[str, dict]:
    """Parse https://dps.psx.com.pk/screener into {symbol: {sector_code, price, pe_ratio, dividend_yield_pct, ...}}."""
    out: dict[str, dict] = {}
    for row in _table_as_dicts(html, "PE RATIO (TTM)"):
        pe = to_number(row.get("PE RATIO (TTM)", ""))
        out[row["SYMBOL"].split()[0]] = {
            "sector_code": row.get("SECTOR", ""),
            "price": to_number(row.get("PRICE", "")),
            "pe_ratio": pe if pe else None,  # the portal shows 0.00 when there are no earnings
            "dividend_yield_pct": to_number(row.get("DIVIDEND YIELD (%)", "")),
            "change_1y_pct": to_number(row.get("1-YEAR CH. (%) *", "")),
            "market_cap": to_number(row.get("MARKET CAP.", "")),
            "volume_avg_30d": to_number(row.get("30D VOLUME AVG.", "")),
        }
    return out


def sector_pe_medians(screener: dict[str, dict]) -> dict[str, float]:
    """Median positive P/E per sector code."""
    groups: dict[str, list[float]] = {}
    for row in screener.values():
        if row["pe_ratio"] and row["pe_ratio"] > 0:
            groups.setdefault(row["sector_code"], []).append(row["pe_ratio"])
    medians = {}
    for code, values in groups.items():
        values.sort()
        mid = len(values) // 2
        medians[code] = values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2
    return medians


_PAYOUT = re.compile(r"([\d.]+)\s*%\s*\(([^)]+)\)\s*\(([A-Z])\)")
_KINDS = {"D": "cash", "B": "bonus", "R": "right"}


def _dmy(text: str) -> date | None:
    try:
        return datetime.strptime(text.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def parse_payouts(html: str, face_value: float | None = 10.0) -> list[dict]:
    """Parse the /company/payouts table. One dict per payout, newest first.

    'Details' reads like '60%(ii) (D)': percent of face value, stage (F final, i/ii/iii interim),
    kind (D cash dividend, B bonus shares, R right shares). A row can list several payouts.
    """
    out: list[dict] = []
    for row in _table_as_dicts(html, "BOOK CLOSURE"):
        closure = [_dmy(p) for p in row.get("BOOK CLOSURE", "").split(" - ")]
        period = re.match(r"(\d{2}/\d{2}/\d{4})\((\w+)\)", row.get("FINANCIAL RESULTS", "").strip())
        try:
            announced = datetime.strptime(row["DATE"].strip(), "%B %d, %Y %I:%M %p").date()
        except ValueError:
            announced = None
        for pct, stage, kind in _PAYOUT.findall(row.get("DETAILS", "")):
            percent = float(pct)
            is_cash = kind == "D"
            out.append({
                "announced": announced,
                "period_end": _dmy(period.group(1)) if period else None,
                "period_type": period.group(2) if period else None,
                "kind": _KINDS.get(kind, kind),
                "stage": "final" if stage.strip().upper() == "F" else "interim",
                "percent": percent,
                "amount_per_share": round(percent * face_value / 100, 4) if is_cash and face_value else None,
                "book_closure_from": closure[0] if closure else None,
                "book_closure_to": closure[1] if len(closure) > 1 else None,
            })
    return out


def parse_eod(text: str) -> list[dict]:
    """Parse /timeseries/eod/<SYMBOL> JSON into [{date, close, volume, open}], oldest first."""
    payload = json.loads(text)
    if payload.get("status") != 1:
        return []
    rows = [
        {"date": datetime.fromtimestamp(ts, tz=timezone.utc).date(), "close": close, "volume": volume, "open": open_}
        for ts, close, volume, open_ in payload["data"]
    ]
    rows.sort(key=lambda r: r["date"])
    return rows


def dividend_summary(payouts: list[dict], today: date) -> dict:
    """Trailing-12-month cash dividend per share and the count of recent fiscal years with a cash payout."""
    cash = [p for p in payouts if p["kind"] == "cash" and p["amount_per_share"] is not None]
    ttm = sum(p["amount_per_share"] for p in cash if p["announced"] and (today - p["announced"]).days <= 365)
    years = {p["period_end"].year for p in cash if p["period_end"]}
    all_years = {p["period_end"].year for p in payouts if p["period_end"]}
    return {"ttm_dividend_per_share": round(ttm, 4), "years_paid": len(years), "window": max(len(all_years), 1)}
