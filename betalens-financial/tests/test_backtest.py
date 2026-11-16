from datetime import date, timedelta
from pathlib import Path

from betalens import backtest as bt
from betalens.data import parsers
from betalens.models import CompanyData, YearFigures
from betalens.pipeline import build_company
from betalens.scoring.engine import load_config

FIX = Path(__file__).parent / "fixtures"
read = lambda name: (FIX / name).read_text(encoding="utf-8")
CFG = load_config()


def pso() -> CompanyData:
    index = {p["date"]: p["close"] for p in parsers.parse_eod(read("eod_KSE100.json"))}
    return build_company("PSO", read("company_PSO.html"), read("payouts_PSO.html"), read("eod_PSO.json"),
                         index, {}, {}, {}, date(2026, 11, 16))


def test_results_become_available_after_lag():
    assert bt.year_available_on(2026, 6) == date(2026, 9, 28)
    assert bt.year_available_on(2025, 12) == date(2026, 3, 31)


def test_as_of_has_no_look_ahead():
    full = pso()
    assert full.fiscal_year_end_month == 6
    when = date(2026, 6, 30)
    snap = bt.as_of(full, when)
    assert max(snap.price_dates) <= when and len(snap.closes) < len(full.closes)
    assert [y.year for y in snap.years] == [2025, 2024, 2023]          # FY2026 not yet published
    assert snap.price == snap.closes[-1] and snap.pe_ratio == snap.price / 44.54
    assert all(p["announced"] <= when for p in snap.payouts)
    assert len(full.closes) == 300 and [y.year for y in full.years][0] == 2026   # original untouched
    assert bt.as_of(full, date(2000, 1, 1)) is None


def test_spearman_and_ranks():
    assert bt.spearman([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]) == 1.0
    assert bt.spearman([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == -1.0
    assert bt.spearman([1, 2, 3], [1, 2, 3]) is None and bt.spearman([1] * 5, [1, 2, 3, 4, 5]) is None
    assert bt._ranks([10, 20, 10]) == [0.5, 2, 0.5]


def test_month_ends():
    assert bt.month_ends(date(2025, 12, 15), date(2026, 2, 28)) == [date(2025, 12, 31), date(2026, 1, 31), date(2026, 2, 28)]


def synthetic(symbol: str, daily_growth: float, eps: list[float]) -> CompanyData:
    start = date(2024, 1, 1)
    dates = [start + timedelta(days=i) for i in range(700)]
    years = [YearFigures(2025 - i, sales=100 * (1.1 ** (3 - i)), profit_after_tax=e * 10, eps=e, net_margin_pct=5 + e / 10)
             for i, e in enumerate(eps)]
    return CompanyData(symbol, sector="CEMENT", years=years, closes=[100 * (1 + daily_growth) ** i for i in range(700)],
                       price_dates=dates, index_closes=[100 * 1.0003 ** i for i in range(700)], fiscal_year_end_month=12)


def test_observations_and_analysis_reward_the_better_company():
    universe = [synthetic(f"UP{i}", 0.001 + i * 0.0001, [12, 10, 8, 6]) for i in range(4)] + \
               [synthetic(f"DN{i}", -0.001 - i * 0.0001, [2, 4, 6, 8]) for i in range(4)]
    rows = bt.observations(universe, CFG)
    assert rows and all(r["date"] <= date(2025, 12, 1) for r in rows)        # leaves room for forward returns
    up = [r for r in rows if r["symbol"].startswith("UP")]
    dn = [r for r in rows if r["symbol"].startswith("DN")]
    assert min(r["score"] for r in up) > max(r["score"] for r in dn)
    assert all(r["excess_3m"] > 0 for r in up) and all(r["excess_3m"] < 0 for r in dn)
    report = bt.analyse(rows, CFG)
    q = report["horizons"]["3m"]["by_quintile"]
    assert q["Q1"]["avg_excess_pct"] > q["Q5"]["avg_excess_pct"]
    assert report["horizons"]["3m"]["score_ic"]["mean_ic"] > 0.5
    w = report["weightings"]
    assert set(w) == {"current", "value_tilt", "equal"} and w["current"]["3m"]["spread_pct"] > 0
    md = bt.to_markdown(report, CFG)
    assert "Alternative factor weightings" in md
    assert "By signal (current thresholds)" in md and "Which factors predicted" in md


def test_write_report_with_too_little_history(tmp_path):
    report = bt.write_report([pso()], CFG, tmp_path)
    assert (tmp_path / "report.md").exists() and (tmp_path / "report.json").exists()
    assert report["observations"] >= 0


def test_variant_weights_total_matches_configured_six():
    six = sum(CFG["weights"][n] for n in bt.VARIANTS["equal"])
    assert all(sum(v.values()) == six for v in bt.VARIANTS.values())
    rows = [{"factors": {"valuation": 100, "price_trend": 0}, "score": 1, "signal": "BUY"}]
    assert bt.reweighted(rows, {"valuation": 3, "price_trend": 1})[0]["score"] == 75.0
