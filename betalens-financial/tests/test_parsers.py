from pathlib import Path

from betalens.data.parsers import parse_company_page, parse_index_constituents, sector_pe_medians, to_number

FIX = Path(__file__).parent / "fixtures"


def test_to_number():
    assert to_number("3,050,025,916") == 3050025916
    assert to_number("(27.93)") == -27.93
    assert to_number("0.40%") == 0.40
    assert to_number("400.3M") == 400.3e6
    assert to_number("Rs.368.01") == 368.01
    assert to_number("-") is None and to_number("") is None


def test_company_page_pso():
    c = parse_company_page((FIX / "company_PSO.html").read_text(encoding="utf-8"), "pso")
    assert c.symbol == "PSO" and c.price == 368.01 and c.pe_ratio == 5.53
    assert [y.year for y in c.years] == [2026, 2025, 2024, 2023]
    latest = c.years[0]
    assert latest.sales == 3050025916 and latest.profit_after_tax == 15067770 and latest.eps == 32.10
    assert latest.gross_margin_pct == 3.28 and latest.net_margin_pct == 0.49
    assert c.years[-1].eps == 12.06


def test_company_page_bank_uses_total_income():
    c = parse_company_page((FIX / "company_HBL.html").read_text(encoding="utf-8"), "HBL")
    assert c.sector == "COMMERCIAL BANKS" and c.name == "Habib Bank Limited"
    assert c.years[0].year == 2025 and c.years[0].sales == 320648511 and c.years[0].eps == 42.60
    assert c.years[0].gross_margin_pct is None and c.years[0].net_margin_pct == 9.84


def test_index_constituents():
    rows = parse_index_constituents((FIX / "kse100.html").read_text(encoding="utf-8"))
    assert len(rows) == 100
    assert rows[0]["symbol"] == "ABL" and rows[0]["price"] == 172.03 and rows[0]["weight_pct"] == 0.40
    assert all(" " not in r["symbol"] for r in rows)


def test_sector_pe_medians_ignore_missing_and_negative():
    s = {"A": {"sector_code": "1", "pe_ratio": 4.0}, "B": {"sector_code": "1", "pe_ratio": 8.0},
         "C": {"sector_code": "1", "pe_ratio": None}, "D": {"sector_code": "2", "pe_ratio": 9.0}}
    assert sector_pe_medians(s) == {"1": 6.0, "2": 9.0}
