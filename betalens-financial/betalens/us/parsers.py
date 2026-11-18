"""Parsers for free US data: the S&P 500 list, SEC company facts, and Nasdaq's public JSON. Pure functions."""
from __future__ import annotations

import json
from datetime import date, datetime

from bs4 import BeautifulSoup

from betalens.models import YearFigures

# SEC XBRL concepts, in order of preference. Companies switch tags over the years, so a later tag
# fills only the years an earlier one leaves empty.
REVENUE = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
           "RevenueFromContractWithCustomerIncludingAssessedTax", "RevenuesNetOfInterestExpense"]
NET_INCOME = ["NetIncomeLoss", "ProfitLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]
EPS = ["EarningsPerShareDiluted", "EarningsPerShareBasic"]
EQUITY = ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"]
EBIT = ["OperatingIncomeLoss"]
INTEREST = ["InterestExpense", "InterestExpenseNonoperating", "InterestExpenseDebt"]
OCF = ["NetCashProvidedByUsedInOperatingActivities"]
CAPEX = ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"]
CURRENT_ASSETS = ["AssetsCurrent"]
CURRENT_LIABILITIES = ["LiabilitiesCurrent"]
RECEIVABLES = ["AccountsReceivableNetCurrent", "ReceivablesNetCurrent"]
INVENTORY = ["InventoryNet"]
PAYABLES = ["AccountsPayableCurrent", "AccountsPayableAndAccruedLiabilitiesCurrent"]
COST_OF_SALES = ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"]
GROSS_PROFIT = ["GrossProfit"]
DPS = ["CommonStockDividendsPerShareDeclared", "CommonStockDividendsPerShareCashPaid"]
DEBT_PARTS = [["LongTermDebtNoncurrent", "LongTermDebt"], ["LongTermDebtCurrent", "DebtCurrent"],
              ["ShortTermBorrowings"], ["CommercialPaper"]]
YEARS_KEPT = 8


def parse_sp500(html: str) -> list[dict]:
    """Wikipedia's 'List of S&P 500 companies' table: [{symbol, name, sector, sub_industry, cik}]."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id="constituents")
    if table is None:
        return []
    headers = [th.get_text(" ", strip=True).lower() for th in table.find("tr").find_all("th")]
    col = {name: headers.index(name) for name in ("symbol", "security", "gics sector", "gics sub-industry", "cik")
           if name in headers}
    out = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) < len(headers):
            continue
        out.append({"symbol": cells[col["symbol"]], "name": cells[col["security"]],
                    "sector": cells[col["gics sector"]].upper(), "sub_industry": cells[col["gics sub-industry"]],
                    "cik": int(cells[col["cik"]]) if cells[col["cik"]].isdigit() else None})
    return out


def _d(text: str) -> date:
    return date.fromisoformat(text)


def _annual(gaap: dict, concepts: list[str], unit: str, duration: bool) -> dict[date, tuple[float, date]]:
    """{fiscal year end: (value, date first filed)} from 10-K filings, keeping the originally filed value."""
    out: dict[date, tuple[float, date]] = {}
    for concept in concepts:
        found: dict[date, tuple[float, date]] = {}
        for e in (gaap.get(concept) or {}).get("units", {}).get(unit, []):
            if not str(e.get("form", "")).startswith("10-K") or "end" not in e:
                continue
            end = _d(e["end"])
            if duration:
                if "start" not in e or not 350 <= (end - _d(e["start"])).days <= 380:
                    continue
            filed = _d(e["filed"])
            if end not in found or filed < found[end][1]:
                found[end] = (float(e["val"]), filed)
        for end, v in found.items():
            out.setdefault(end, v)
    return out


def years_from_sec(facts: dict) -> tuple[list[YearFigures], float | None]:
    """Annual figures (newest first, money in thousands of USD like the PSX data) and shares outstanding."""
    gaap = facts.get("facts", {}).get("us-gaap", {})
    ni = _annual(gaap, NET_INCOME, "USD", True)
    if not ni:
        return [], None
    series = {
        "sales": _annual(gaap, REVENUE, "USD", True),
        "eps": _annual(gaap, EPS, "USD/shares", True),
        "equity": _annual(gaap, EQUITY, "USD", False),
        "ebit": _annual(gaap, EBIT, "USD", True),
        "interest_expense": _annual(gaap, INTEREST, "USD", True),
        "operating_cash_flow": _annual(gaap, OCF, "USD", True),
        "capex": _annual(gaap, CAPEX, "USD", True),
        "current_assets": _annual(gaap, CURRENT_ASSETS, "USD", False),
        "current_liabilities": _annual(gaap, CURRENT_LIABILITIES, "USD", False),
        "receivables": _annual(gaap, RECEIVABLES, "USD", False),
        "inventory": _annual(gaap, INVENTORY, "USD", False),
        "payables": _annual(gaap, PAYABLES, "USD", False),
        "cost_of_sales": _annual(gaap, COST_OF_SALES, "USD", True),
        "dividend_per_share": _annual(gaap, DPS, "USD/shares", True),
    }
    gross = _annual(gaap, GROSS_PROFIT, "USD", True)
    debt_parts = [_annual(gaap, names, "USD", False) for names in DEBT_PARTS]
    per_share = {"eps", "dividend_per_share"}
    by_year: dict[int, YearFigures] = {}
    for end in sorted(ni, reverse=True):
        if end.year in by_year:          # a changed fiscal year end can give two in one calendar year
            continue
        y = YearFigures(year=end.year, available_on=ni[end][1])
        y.profit_after_tax = ni[end][0] / 1000
        for field, s in series.items():
            if end in s:
                setattr(y, field, s[end][0] if field in per_share else s[end][0] / 1000)
        parts = [p[end][0] for p in debt_parts if end in p]
        y.total_debt = sum(parts) / 1000 if parts else None
        if y.sales:
            y.net_margin_pct = round(100 * y.profit_after_tax / y.sales, 2)
            gp = gross[end][0] / 1000 if end in gross else (y.sales - y.cost_of_sales if y.cost_of_sales else None)
            y.gross_margin_pct = round(100 * gp / y.sales, 2) if gp is not None else None
        by_year[end.year] = y
        if len(by_year) >= YEARS_KEPT:
            break
    shares_entries = facts.get("facts", {}).get("dei", {}).get("EntityCommonStockSharesOutstanding", {}) \
        .get("units", {}).get("shares", [])
    shares = max(shares_entries, key=lambda e: e["end"])["val"] if shares_entries else None
    return [by_year[k] for k in sorted(by_year, reverse=True)], shares


def _money(text) -> float | None:
    if text is None:
        return None
    t = str(text).replace("$", "").replace(",", "").replace("%", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


def _mdy(text: str) -> date | None:
    try:
        return datetime.strptime(text.strip(), "%m/%d/%Y").date()
    except (ValueError, AttributeError):
        return None


def parse_nasdaq_history(text: str) -> list[dict]:
    """Nasdaq /api/quote/{symbol}/historical: [{date, close, volume}], oldest first."""
    data = (json.loads(text) or {}).get("data") or {}
    rows = ((data.get("tradesTable") or {}).get("rows")) or []
    out = [{"date": _mdy(r["date"]), "close": _money(r["close"]), "volume": _money(r.get("volume"))} for r in rows]
    out = [r for r in out if r["date"] and r["close"]]
    out.sort(key=lambda r: r["date"])
    return out


def parse_nasdaq_screener(text: str) -> dict[str, dict]:
    """Nasdaq stock screener (every US-listed stock, one request): {symbol: {price, change, change_pct, ...}}.

    Nasdaq writes share classes with a slash (BRK/B); they are returned with a dot (BRK.B) to match the S&P list.
    """
    rows = ((json.loads(text) or {}).get("data") or {}).get("rows") or []
    out = {}
    for r in rows:
        out[r["symbol"].replace("/", ".")] = {
            "price": _money(r.get("lastsale")), "change": _money(r.get("netchange")),
            "change_pct": _money(r.get("pctchange")), "volume": _money(r.get("volume")),
            "market_cap": _money(r.get("marketCap")), "name": r.get("name", ""), "sector": r.get("sector", ""),
        }
    return out


def parse_nasdaq_watchlist(text: str) -> dict[str, dict]:
    """Nasdaq batch quotes (/api/quote/watchlist): the latest trade per symbol, real time, including
    pre-market and after-hours trades. Change is measured against the previous regular close."""
    rows = (json.loads(text) or {}).get("data") or []
    out = {}
    for r in rows if isinstance(rows, list) else []:
        price, prev = _money(r.get("lastSalePrice")), _money(r.get("previousClosePrice"))
        if price is None:
            continue
        change = round(price - prev, 4) if prev else None
        out[r["symbol"].replace("/", ".")] = {
            "price": price, "previous_close": prev, "change": change,
            "change_pct": round(100 * change / prev, 2) if prev and change is not None else None,
            "volume": _money(r.get("volume")), "market_status": r.get("marketStatus", ""),
            "last_trade": r.get("lastTradeTimestampDateTime") or r.get("lastTradeTimestamp"),
            "trade_date": (r.get("lastTradeTimestampDateTime") or "")[:10] or None,
        }
    return out



def parse_nasdaq_dividend_history(text: str) -> list[dict]:
    """Nasdaq /api/quote/{symbol}/dividends: cash dividends as payout dicts, newest first."""
    data = (json.loads(text) or {}).get("data") or {}
    rows = ((data.get("dividends") or {}).get("rows")) or []
    out = []
    for r in rows:
        if str(r.get("type", "")).lower() != "cash":
            continue
        ex = _mdy(r.get("exOrEffDate", ""))
        amount = _money(r.get("amount"))
        if not ex or not amount:
            continue
        out.append({"kind": "cash", "stage": "regular", "percent": None, "amount_per_share": amount,
                    "ex_date": ex, "announced": _mdy(r.get("declarationDate", "")) or ex,
                    "record_date": _mdy(r.get("recordDate", "")), "payment_date": _mdy(r.get("paymentDate", "")),
                    "book_closure_from": None, "book_closure_to": None})
    out.sort(key=lambda p: p["ex_date"], reverse=True)
    return out


def parse_nasdaq_dividend_calendar(text: str) -> list[dict]:
    """Nasdaq /api/calendar/dividends?date=...: every US stock going ex-dividend that day."""
    rows = ((((json.loads(text) or {}).get("data") or {}).get("calendar") or {}).get("rows")) or []
    out = []
    for r in rows:
        ex = _mdy(r.get("dividend_Ex_Date", ""))
        amount = _money(r.get("dividend_Rate"))
        if not ex or not amount:
            continue
        out.append({"symbol": r["symbol"].replace("/", "."), "company": r.get("companyName", ""), "kind": "cash",
                    "stage": "regular", "percent": None, "amount_per_share": amount, "ex_date": ex,
                    "record_date": _mdy(r.get("record_Date", "")), "payment_date": _mdy(r.get("payment_Date", "")),
                    "announced": _mdy(r.get("announcement_Date", "")),
                    "annual_dividend": _money(r.get("indicated_Annual_Dividend")),
                    "book_closure_from": None, "book_closure_to": None})
    return out

