from datetime import date, timedelta
from pathlib import Path

from betalens import dividends as dv
from betalens.scoring.engine import load_config, score_company
from betalens.us import parsers
from betalens.us.pipeline import CONFIG, build_us_company, sector_medians, sp500_from_csv

FIX = Path(__file__).parent / "fixtures" / "us"
read = lambda name: (FIX / name).read_text(encoding="utf-8")
CFG = load_config(CONFIG)


def test_sp500_list():
    rows = parsers.parse_sp500(read("wiki_sp500.html"))
    by = {r["symbol"]: r for r in rows}
    assert {"AAPL", "BRK.B", "JPM", "MMM"} <= set(by)
    assert by["AAPL"]["cik"] == 320193 and by["AAPL"]["sector"] == "INFORMATION TECHNOLOGY"
    assert by["JPM"]["sector"] == "FINANCIALS"
    csv_rows = sp500_from_csv("Symbol,Security,GICS Sector,GICS Sub-Industry,Headquarters Location,Date added,CIK,Founded\n"
                              "MMM,3M,Industrials,Industrial Conglomerates,x,1957-03-04,66740,1902\n")
    assert csv_rows == [{"symbol": "MMM", "name": "3M", "sector": "INDUSTRIALS",
                         "sub_industry": "Industrial Conglomerates", "cik": 66740}]


def test_sec_annual_figures():
    import json
    years, shares = parsers.years_from_sec(json.loads(read("sec_facts_AAPL.json")))
    assert shares == 14532182000
    latest = years[0]
    assert latest.year == 2026 and latest.available_on == date(2026, 11, 3)
    assert latest.sales == 478834000 and latest.profit_after_tax > 0      # thousands of USD
    assert latest.eps and latest.current_assets == 173857000 and latest.equity and latest.total_debt
    assert latest.operating_cash_flow and latest.capex and latest.dividend_per_share
    assert 0 < latest.net_margin_pct < 40 and 30 < latest.gross_margin_pct < 60
    assert [y.year for y in years] == sorted({y.year for y in years}, reverse=True) and len(years) >= 6
    prior = years[1]
    assert prior.year == 2025 and prior.sales == 416161000 and prior.available_on == date(2025, 10, 31)   # first filing kept


def test_nasdaq_parsers():
    hist = parsers.parse_nasdaq_history(read("nasdaq_hist_AAPL.json"))
    assert len(hist) == 400 and hist[0]["date"] < hist[-1]["date"] and hist[-1]["close"] == 352.78
    live = parsers.parse_nasdaq_screener(read("nasdaq_screener.json"))
    assert "BRK.B" in live and live["AAPL"]["price"] > 0 and live["AAPL"]["market_cap"] > 1e12
    past = parsers.parse_nasdaq_dividend_history(read("nasdaq_div_AAPL.json"))
    assert past[0]["ex_date"] == date(2026, 11, 12) and past[0]["amount_per_share"] == 0.27
    assert past[0]["announced"] == date(2026, 11, 2) and all(p["kind"] == "cash" for p in past)
    cal = parsers.parse_nasdaq_dividend_calendar(read("nasdaq_divcal.json"))
    apc = next(p for p in cal if p["symbol"] == "APC")
    assert apc["ex_date"] == date(2026, 11, 18) and apc["amount_per_share"] == 0.5 and apc["annual_dividend"] == 2.0
    assert parsers.parse_nasdaq_history('{"data":null}') == []


def _apple():
    import json
    row = {"symbol": "AAPL", "name": "Apple Inc.", "sector": "INFORMATION TECHNOLOGY", "cik": 320193}
    spy = {p["date"]: p["close"] for p in parsers.parse_nasdaq_history(read("nasdaq_hist_SPY.json"))}
    hist = parsers.parse_nasdaq_history(read("nasdaq_hist_AAPL.json"))
    return build_us_company(row, json.loads(read("sec_facts_AAPL.json")), hist, spy, {"price": 350.0})


def test_build_and_score_us_company_with_all_ten_factors():
    c = _apple()
    assert c.market == "US" and c.price == 350.0 and len(c.closes) == len(c.index_closes) >= 300
    assert c.pe_ratio == 350.0 / c.years[0].eps and 0 < c.dividend_yield_pct < 1 and c.dividend_years_paid == 5
    c.sector_pe_median = sector_medians([c])[c.sector]
    card = score_company(c, CFG)
    assert card.coverage_pct == 100 and card.signal != "INSUFFICIENT_DATA"
    assert {f.name for f in card.factors if f.score is not None} == set(CFG["weights"])


def test_us_valuation_scale_is_kinder_to_normal_us_pes():
    c = _apple()
    c.pe_ratio, c.sector_pe_median = 20.0, None
    us = next(f for f in score_company(c, CFG).factors if f.name == "valuation").score
    c.market = "PSX"
    psx = next(f for f in score_company(c, CFG).factors if f.name == "valuation").score
    assert us == 60 and psx == 30


def test_us_financials_use_price_to_book():
    c = _apple()
    c.sector = "FINANCIALS"
    names = {f.name for f in score_company(c, CFG).factors}
    assert "price_to_book" in names and not names & {"debt", "liquidity", "cash_flow_quality", "cash_conversion_cycle"}


def test_us_dividend_agent_uses_published_ex_date():
    c = _apple()
    ex = c.price_dates[-60]
    i = c.price_dates.index(ex)
    past = {"kind": "cash", "stage": "regular", "percent": None, "amount_per_share": 0.27, "ex_date": ex,
            "announced": ex - timedelta(days=10), "book_closure_from": None}
    e = dv.measure_event(c, past)
    assert e["ex_date"] == ex and e["last_buy_date"] == c.price_dates[i - 1]
    future = dict(past, ex_date=date(2026, 11, 23), symbol="AAPL")          # a Monday
    a = dv.assess(future, {"signal": "BUY", "price": 350.0, "red_flags": []}, None, 0.9, date(2026, 11, 18))
    assert a["last_buy_date"] == date(2026, 11, 20) and a["ex_date"] == date(2026, 11, 23)   # the Friday before
    assert a["book_closure_from"] is None and a["expected_drop_rs"] == 0.24


def test_build_us_live():
    from datetime import datetime, timezone

    from betalens.us.live import build_us_live
    screener = parsers.parse_nasdaq_watchlist(read("nasdaq_watchlist.json"))
    cal = [{"symbol": "AAPL", "company": "Apple", "kind": "cash", "stage": "regular", "percent": None,
            "amount_per_share": 0.27, "ex_date": date(2026, 11, 23), "book_closure_from": None},
           {"symbol": "APC", "amount_per_share": 0.5, "ex_date": date(2026, 11, 19), "kind": "cash"}]
    live = build_us_live(screener, cal, {"AAPL", "MSFT"}, datetime(2026, 11, 18, 15, 7, tzinfo=timezone.utc))
    assert set(live["prices"]) == {"AAPL", "MSFT"} and len(live["upcoming"]) == 1 and live["market_status"] == "After Hours"
    u = live["upcoming"][0]
    assert u["last_buy_date"] == date(2026, 11, 20) and u["yield_pct"] == round(27 / screener["AAPL"]["price"], 2)


def test_long_history_is_fetched_in_windows():
    from betalens.us.pipeline import fetch_history

    class Fake:
        calls = []
        variants = staticmethod(lambda s: [s])

        def history(self, symbol, days, assetclass="stocks", end=None):
            self.calls.append((days, end))
            start = end - timedelta(days=days)
            rows = [{"date": (start + timedelta(days=i)).strftime("%m/%d/%Y"), "close": "$1.0"} for i in range(1, days + 1)]
            import json
            return json.dumps({"data": {"tradesTable": {"rows": rows}}})

    f = Fake()
    rows = fetch_history(f, "X", 3650)
    assert [d for d, _ in f.calls] == [1500, 1500, 650] and len(rows) == 3650
    assert rows[0]["date"] < rows[-1]["date"]


def test_watchlist_quotes_are_live_and_measured_from_previous_close():
    q = parsers.parse_nasdaq_watchlist(read("nasdaq_watchlist.json"))
    nvda = q["NVDA"]
    assert nvda["price"] == 155.5601 and nvda["previous_close"] == 156.14 and nvda["market_status"] == "After Hours"
    assert nvda["change"] == round(155.5601 - 156.14, 4) and nvda["change_pct"] == -0.37
    assert "BRK.B" in q and parsers.parse_nasdaq_watchlist('{"data":null}') == {}


def test_older_session_never_replaces_a_newer_price():
    """18 Nov 2026 02:51 UTC: Nasdaq served Monday's NEM ($110.34) after Tuesday's close ($111.26)."""
    saved = {"NEM": {"price": 111.33, "trade_date": "2026-11-17"}, "OLD": {"price": 5.0, "trade_date": None}}
    new = {"NEM": {"price": 110.34, "trade_date": "2026-11-16"}, "OLD": {"price": 6.0, "trade_date": "2026-11-17"},
           "NEW": {"price": 7.0, "trade_date": "2026-11-17"}}
    merged, kept = parsers.keep_fresher(new, saved)
    assert merged["NEM"]["price"] == 111.33 and kept == 1
    assert merged["OLD"]["price"] == 6.0 and merged["NEW"]["price"] == 7.0
    same_day = parsers.keep_fresher({"NEM": {"price": 111.5, "trade_date": "2026-11-17"}}, saved)[0]
    assert same_day["NEM"]["price"] == 111.5          # later trade on the same day still updates
    next_day = parsers.keep_fresher({"NEM": {"price": 112.0, "trade_date": "2026-11-18"}}, saved)[0]
    assert next_day["NEM"]["price"] == 112.0


def test_watchlist_carries_trade_date():
    q = parsers.parse_nasdaq_watchlist(read("nasdaq_watchlist.json"))
    assert q["NVDA"]["trade_date"] == "2026-11-17"
