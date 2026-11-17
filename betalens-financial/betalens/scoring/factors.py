"""The ten scorecard factors. Each returns (score 0-100 or None, reasons)."""
from __future__ import annotations

from betalens.models import CompanyData, YearFigures
from betalens.scoring.curves import avg, cagr, curve

Result = tuple[float | None, list[str]]

# Market-specific scales where normal levels differ: US shares trade on higher P/Es and lower yields than PSX.
PE_ABSOLUTE = {"PSX": [(5, 100), (10, 70), (15, 45), (25, 15), (40, 0)],
               "US": [(10, 100), (15, 80), (20, 60), (30, 30), (50, 0)]}
YIELD_SCALE = {"PSX": [(0, 0), (3, 50), (6, 75), (10, 100)],
               "US": [(0, 0), (1.5, 40), (3, 65), (5, 85), (8, 100)]}


def _window(c: CompanyData, period_years: int) -> tuple[YearFigures, YearFigures, int] | None:
    """Latest year and the year `period_years` earlier (or the oldest available, min 1 year apart)."""
    if len(c.years) < 2:
        return None
    span = min(period_years, len(c.years) - 1)
    return c.years[0], c.years[span], span


def revenue_growth(c: CompanyData, period_years: int) -> Result:
    w = _window(c, period_years)
    if not w:
        return None, ["Fewer than two years of sales data"]
    g = cagr(w[0].sales, w[1].sales, w[2])
    if g is None:
        return None, ["Sales figures missing"]
    s = curve(g, [(-10, 0), (0, 35), (10, 60), (20, 85), (30, 100)])
    return s, [f"Sales grew {g:.1f}% a year over {w[2]} year(s)"]


def earnings_growth(c: CompanyData, period_years: int) -> Result:
    w = _window(c, period_years)
    if not w:
        return None, ["Fewer than two years of earnings data"]
    latest, base, span = w
    if latest.eps is None or base.eps is None:
        return None, ["EPS figures missing"]
    reasons: list[str] = []
    if base.eps <= 0:
        growth_score = 70.0 if latest.eps > 0 else 0.0
        reasons.append("Turned from loss to profit" if latest.eps > 0 else "Loss-making across the period")
    else:
        g = cagr(latest.eps, base.eps, span)
        growth_score = curve(g, [(-20, 0), (0, 35), (10, 60), (20, 85), (30, 100)])
        reasons.append(f"EPS grew {g:.1f}% a year over {span} year(s)")
    window = c.years[: span + 1]
    eps = [y.eps for y in window if y.eps is not None]
    profitable = sum(1 for e in eps if e > 0) / len(eps)
    rising = sum(1 for new, old in zip(eps, eps[1:]) if new >= old) / max(len(eps) - 1, 1)
    consistency = 100 * (0.6 * profitable + 0.4 * rising)
    if profitable < 1:
        reasons.append("At least one loss-making year in the period")
    return 0.6 * growth_score + 0.4 * consistency, reasons


def profitability(c: CompanyData, period_years: int) -> Result:
    if not c.years:
        return None, ["No profitability data"]
    latest = c.years[0]
    reasons: list[str] = []
    parts: list[tuple[float, float]] = []  # (score, weight)
    if latest.equity and latest.equity > 0 and latest.profit_after_tax is not None:
        roe = 100 * latest.profit_after_tax / latest.equity
        parts.append((curve(roe, [(0, 0), (10, 40), (20, 75), (30, 100)]), 0.6))
        reasons.append(f"Return on equity {roe:.1f}%")
    margins = [y.net_margin_pct for y in c.years[: period_years + 1] if y.net_margin_pct is not None]
    if len(margins) >= 2:
        change = margins[0] - margins[-1]
        base = abs(margins[-1]) or 1.0
        parts.append((curve(100 * change / base, [(-50, 0), (0, 50), (50, 100)]), 0.25))
        reasons.append(f"Net margin {margins[0]:.2f}% vs {margins[-1]:.2f}% at the start of the period")
    pats = [y.profit_after_tax for y in c.years[: period_years + 1] if y.profit_after_tax is not None]
    if pats:
        parts.append((100 * sum(1 for p in pats if p > 0) / len(pats), 0.25))
    if not parts:
        return None, ["No profitability data"]
    total_w = sum(w for _, w in parts)
    return sum(s * w for s, w in parts) / total_w, reasons


def cash_flow_quality(c: CompanyData, period_years: int) -> Result:
    ys = [y for y in c.years[:period_years] if y.operating_cash_flow is not None and y.profit_after_tax]
    if not ys:
        return None, ["Needs cash flow statement data (not on the free portal page)"]
    ratio = avg([y.operating_cash_flow / y.profit_after_tax for y in ys if y.profit_after_tax > 0])
    reasons = []
    if ratio is None:
        conv = 0.0
        reasons.append("No profitable year to compare cash flow against")
    else:
        conv = curve(ratio, [(0, 0), (0.5, 40), (1.0, 80), (1.3, 100)])
        reasons.append(f"Operating cash flow is {ratio:.2f}x reported profit")
    fcf = [y.operating_cash_flow - (y.capex or 0) for y in ys]
    fcf_score = 100 * sum(1 for f in fcf if f > 0) / len(fcf)
    if fcf_score < 100:
        reasons.append("Free cash flow negative in at least one year")
    return 0.7 * conv + 0.3 * fcf_score, reasons


def cash_conversion_cycle(c: CompanyData, period_years: int) -> Result:
    y = c.years[0] if c.years else None
    if not y or None in (y.receivables, y.inventory, y.payables, y.cost_of_sales, y.sales) or not y.sales or not y.cost_of_sales:
        return None, ["Needs balance sheet data (not on the free portal page)"]
    days = 365 * (y.receivables / y.sales + y.inventory / y.cost_of_sales - y.payables / y.cost_of_sales)
    return curve(days, [(30, 100), (60, 75), (120, 40), (200, 0)]), [f"Cash conversion cycle {days:.0f} days"]


def debt(c: CompanyData, period_years: int) -> Result:
    y = c.years[0] if c.years else None
    if not y or y.total_debt is None or not y.equity:
        return None, ["Needs balance sheet data (not on the free portal page)"]
    if y.equity <= 0:
        return 0.0, ["Negative equity"]
    de = y.total_debt / y.equity
    score = curve(de, [(0, 100), (0.5, 80), (1, 55), (2, 20), (3, 0)])
    reasons = [f"Debt is {de:.2f}x equity"]
    if y.ebit is not None and y.interest_expense:
        cover = y.ebit / y.interest_expense
        score = 0.6 * score + 0.4 * curve(cover, [(1, 0), (2, 40), (4, 70), (8, 100)])
        reasons.append(f"Profit covers interest {cover:.1f}x")
    return score, reasons


def liquidity(c: CompanyData, period_years: int) -> Result:
    y = c.years[0] if c.years else None
    if not y or y.current_assets is None or not y.current_liabilities:
        return None, ["Needs balance sheet data (not on the free portal page)"]
    cr = y.current_assets / y.current_liabilities
    return curve(cr, [(0.5, 0), (0.7, 20), (1, 50), (1.5, 80), (2, 100)]), [f"Current ratio {cr:.2f}"]


def valuation(c: CompanyData, period_years: int) -> Result:
    if c.pe_ratio is None:
        return None, ["P/E not available"]
    if c.pe_ratio <= 0:
        return 0.0, ["No positive trailing earnings (P/E not meaningful)"]
    absolute = curve(c.pe_ratio, PE_ABSOLUTE.get(c.market, PE_ABSOLUTE["PSX"]))
    reasons = [f"P/E {c.pe_ratio:.1f}"]
    if c.sector_pe_median and c.sector_pe_median > 0:
        rel = c.pe_ratio / c.sector_pe_median
        relative = curve(rel, [(0.5, 100), (0.8, 80), (1, 60), (1.3, 35), (2, 0)])
        reasons.append(f"{rel:.2f}x the sector median P/E of {c.sector_pe_median:.1f}")
        return 0.7 * relative + 0.3 * absolute, reasons
    return absolute, reasons


def dividend(c: CompanyData, period_years: int) -> Result:
    if c.dividend_yield_pct is None and c.dividend_years_paid is None:
        return None, ["Dividend data not available"]
    parts: list[tuple[float, float]] = []
    reasons: list[str] = []
    if c.dividend_yield_pct is not None:
        parts.append((curve(c.dividend_yield_pct, YIELD_SCALE.get(c.market, YIELD_SCALE["PSX"])), 0.5))
        reasons.append(f"Dividend yield {c.dividend_yield_pct:.1f}%")
    if c.dividend_years_paid is not None:
        window = max(c.dividend_window, 1)
        parts.append((100 * min(c.dividend_years_paid, window) / window, 0.3))
        reasons.append(f"Paid a cash dividend in {c.dividend_years_paid} of the last {window} fiscal years on record")
    y = c.years[0] if c.years else None
    if y and y.dividend_per_share is not None and y.eps and y.eps > 0:
        payout = y.dividend_per_share / y.eps
        parts.append((curve(payout, [(0.6, 100), (0.8, 70), (1.0, 40), (1.2, 0)]), 0.2))
        reasons.append(f"Pays out {100 * payout:.0f}% of earnings")
    total_w = sum(w for _, w in parts)
    return sum(s * w for s, w in parts) / total_w, reasons


def price_trend(c: CompanyData, period_years: int) -> Result:
    if len(c.closes) < 200:
        return None, ["Needs at least 200 days of price history"]
    last = c.closes[-1]
    ma50 = sum(c.closes[-50:]) / 50
    ma200 = sum(c.closes[-200:]) / 200
    trend = 50.0 * (last > ma200) + 50.0 * (ma50 > ma200)
    reasons = [f"Price is {'above' if last > ma200 else 'below'} its 200-day average"]
    n = min(250, len(c.closes) - 1)
    stock_ret = 100 * (last / c.closes[-n - 1] - 1)
    if len(c.index_closes) > n:
        rel = stock_ret - 100 * (c.index_closes[-1] / c.index_closes[-n - 1] - 1)
        strength = curve(rel, [(-30, 0), (0, 50), (30, 100)])
        reasons.append(f"{rel:+.1f} points vs KSE-100 over about a year")
        return 0.6 * trend + 0.4 * strength, reasons
    return trend, reasons


def _latest_with(c: CompanyData, attr: str):
    return next((y for y in c.years if getattr(y, attr) is not None), None)


def price_to_book(c: CompanyData, period_years: int) -> Result:
    """Financial companies: market value against book equity (equity entered by hand, in Rs thousands)."""
    y = _latest_with(c, "equity")
    if not y or not c.price or not c.shares_outstanding:
        return None, ["Needs equity from the annual report (manual entry)"]
    if y.equity <= 0:
        return 0.0, ["Negative equity"]
    pb = c.price * c.shares_outstanding / (y.equity * 1000)
    return curve(pb, [(0.5, 100), (1.0, 65), (1.5, 40), (2.5, 10), (3.5, 0)]), [f"Price is {pb:.2f}x book value ({y.year})"]


def asset_quality(c: CompanyData, period_years: int) -> Result:
    """Banks: non-performing loans as a share of gross advances. Lower is better."""
    y = _latest_with(c, "npl_ratio_pct")
    if not y:
        return None, ["Needs the non-performing loan ratio from the annual report (manual entry)"]
    return curve(y.npl_ratio_pct, [(2, 100), (5, 75), (10, 40), (15, 15), (20, 0)]), \
        [f"Non-performing loans {y.npl_ratio_pct:.1f}% of advances ({y.year})"]


def capital_adequacy(c: CompanyData, period_years: int) -> Result:
    """Banks: capital adequacy ratio. The regulatory minimum in Pakistan is roughly 11.5% including buffers."""
    y = _latest_with(c, "capital_adequacy_pct")
    if not y:
        return None, ["Needs the capital adequacy ratio from the annual report (manual entry)"]
    return curve(y.capital_adequacy_pct, [(11.5, 0), (13, 40), (16, 75), (20, 100)]), \
        [f"Capital adequacy ratio {y.capital_adequacy_pct:.1f}% ({y.year})"]


FACTORS = {
    "revenue_growth": revenue_growth,
    "earnings_growth": earnings_growth,
    "profitability": profitability,
    "cash_flow_quality": cash_flow_quality,
    "cash_conversion_cycle": cash_conversion_cycle,
    "debt": debt,
    "liquidity": liquidity,
    "valuation": valuation,
    "dividend": dividend,
    "price_trend": price_trend,
    "price_to_book": price_to_book,
    "asset_quality": asset_quality,
    "capital_adequacy": capital_adequacy,
}
