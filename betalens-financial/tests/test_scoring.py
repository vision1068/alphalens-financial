from pathlib import Path

import pytest

from betalens.data.parsers import parse_company_page
from betalens.models import CompanyData, YearFigures
from betalens.scoring.curves import cagr, curve
from betalens.scoring.engine import load_config, score_company, signal_for

CFG = load_config()
FIX = Path(__file__).parent / "fixtures"


def strong_company() -> CompanyData:
    years = [
        YearFigures(2026, sales=200, profit_after_tax=30, eps=15, net_margin_pct=15, equity=100, total_debt=20,
                    ebit=45, interest_expense=3, operating_cash_flow=36, capex=10, current_assets=90,
                    current_liabilities=40, receivables=20, inventory=15, payables=18, cost_of_sales=120,
                    dividend_per_share=6),
        YearFigures(2025, sales=160, profit_after_tax=22, eps=11, net_margin_pct=13.7, operating_cash_flow=25, capex=8),
        YearFigures(2024, sales=130, profit_after_tax=16, eps=8, net_margin_pct=12.3, operating_cash_flow=18, capex=7),
        YearFigures(2023, sales=110, profit_after_tax=12, eps=6, net_margin_pct=10.9),
    ]
    closes = [100 + i * 0.2 for i in range(260)]
    return CompanyData("GOOD", sector="CEMENT", price=152, pe_ratio=6, sector_pe_median=9, dividend_yield_pct=7,
                       years=years, closes=closes, index_closes=[100 + i * 0.05 for i in range(260)],
                       dividend_years_paid=5)


def test_curve_and_cagr():
    pts = [(0, 0), (10, 50), (20, 100)]
    assert curve(-5, pts) == 0 and curve(5, pts) == 25 and curve(99, pts) == 100
    assert cagr(121, 100, 2) == pytest.approx(10.0)
    assert cagr(50, 0, 2) is None and cagr(-5, 100, 2) == -100.0


def test_weights_total_100_and_bands():
    assert sum(CFG["weights"].values()) == 100
    assert [signal_for(s, CFG["signals"]) for s in (80, 65, 50, 30, 10)] == \
        ["STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"]


def test_strong_company_scores_strong_buy_with_full_coverage():
    card = score_company(strong_company(), CFG)
    assert card.coverage_pct == 100 and card.signal == "STRONG_BUY" and card.score > 80
    assert all(f.score is not None and 0 <= f.score <= 100 for f in card.factors)


def test_weak_company_scores_sell_side():
    c = strong_company()
    c.symbol = "BAD"
    c.years[0] = YearFigures(2026, sales=90, profit_after_tax=-8, eps=-4, net_margin_pct=-8.9, equity=30,
                             total_debt=95, ebit=2, interest_expense=9, operating_cash_flow=-5, capex=6,
                             current_assets=30, current_liabilities=55, receivables=40, inventory=45,
                             payables=10, cost_of_sales=85)
    c.pe_ratio, c.dividend_yield_pct, c.dividend_years_paid = -3, 0, 0
    c.closes = list(reversed(c.closes))
    card = score_company(c, CFG)
    assert card.signal in ("SELL", "STRONG_SELL") and card.score < 40


def test_missing_statement_data_lowers_coverage_not_score():
    c = strong_company()
    for y in c.years:
        y.equity = y.total_debt = y.operating_cash_flow = y.current_assets = y.receivables = None
    card = score_company(c, CFG)
    missing = {f.name for f in card.factors if f.score is None}
    assert missing == {"cash_flow_quality", "cash_conversion_cycle", "debt", "liquidity"}
    assert card.coverage_pct == 62 and card.signal != "INSUFFICIENT_DATA"


def test_below_min_coverage_gives_no_signal():
    card = score_company(CompanyData("THIN", pe_ratio=8), CFG)
    assert card.signal == "INSUFFICIENT_DATA" and card.coverage_pct == 12


def test_banks_skip_working_capital_and_leverage_factors():
    c = strong_company()
    c.sector = "Commercial Banks"
    card = score_company(c, CFG)
    names = {f.name for f in card.factors}
    assert not names & {"cash_flow_quality", "cash_conversion_cycle", "debt", "liquidity"}
    assert card.coverage_pct == 100


def test_real_portal_page_scores_end_to_end():
    c = parse_company_page((FIX / "company_PSO.html").read_text(encoding="utf-8"), "PSO")
    card = score_company(c, CFG)
    scored = {f.name for f in card.factors if f.score is not None}
    assert scored == {"revenue_growth", "earnings_growth", "profitability", "valuation"}
    assert card.signal == "INSUFFICIENT_DATA"  # page alone covers 46% of the weight
