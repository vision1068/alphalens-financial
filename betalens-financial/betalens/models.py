"""Plain data containers passed between the data agent and the scorecard."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class YearFigures:
    """One fiscal year. Portal fields first; statement fields are optional (need full reports)."""
    year: int
    sales: float | None = None
    profit_after_tax: float | None = None
    eps: float | None = None
    gross_margin_pct: float | None = None
    net_margin_pct: float | None = None
    # From full financial statements (not on the free portal page):
    equity: float | None = None
    total_debt: float | None = None
    ebit: float | None = None
    interest_expense: float | None = None
    operating_cash_flow: float | None = None
    capex: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    receivables: float | None = None
    inventory: float | None = None
    payables: float | None = None
    cost_of_sales: float | None = None
    dividend_per_share: float | None = None
    # Banks only, from the annual report:
    npl_ratio_pct: float | None = None          # non-performing loans as % of gross advances
    capital_adequacy_pct: float | None = None   # capital adequacy ratio


@dataclass
class CompanyData:
    symbol: str
    name: str = ""
    sector: str = ""
    price: float | None = None
    pe_ratio: float | None = None
    sector_pe_median: float | None = None
    dividend_yield_pct: float | None = None
    years: list[YearFigures] = field(default_factory=list)   # newest first
    closes: list[float] = field(default_factory=list)        # daily closes, oldest first
    price_dates: list = field(default_factory=list)          # dates matching `closes`
    fiscal_year_end_month: int = 6
    index_closes: list[float] = field(default_factory=list)  # KSE-100, same dates
    dividend_years_paid: int | None = None                   # fiscal years with a cash dividend, of the last `dividend_window`
    dividend_window: int = 5
    face_value: float | None = None
    shares_outstanding: float | None = None
    payouts: list[dict] = field(default_factory=list)        # newest first, see parsers.parse_payouts
    red_flags: list[str] = field(default_factory=list)
    announcements: list[str] = field(default_factory=list)   # recent announcement titles, newest first


@dataclass
class FactorResult:
    name: str
    score: float | None          # 0-100, or None when the data is not available
    weight: float
    reasons: list[str] = field(default_factory=list)


@dataclass
class Scorecard:
    symbol: str
    score: float | None
    coverage_pct: float
    signal: str
    factors: list[FactorResult]
    red_flags: list[str] = field(default_factory=list)
