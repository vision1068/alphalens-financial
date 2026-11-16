"""Manually entered statement figures for the four factors the free portal cannot supply.

Edit data/manual_statements.csv: one row per company per fiscal year. Money columns are in
thousands of rupees (the unit the PSX portal uses); dividend_per_share is in rupees; npl_ratio_pct and
capital_adequacy_pct (banks only) are percentages.
Leave a cell blank when you do not have the figure.
"""
from __future__ import annotations

import csv
from pathlib import Path

from betalens.models import CompanyData, YearFigures

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "data" / "manual_statements.csv"
FIELDS = ("equity", "total_debt", "ebit", "interest_expense", "operating_cash_flow", "capex",
          "current_assets", "current_liabilities", "receivables", "inventory", "payables",
          "cost_of_sales", "dividend_per_share", "npl_ratio_pct", "capital_adequacy_pct")


def load_manual(path: Path | str = DEFAULT_PATH) -> dict[tuple[str, int], dict[str, float]]:
    """Read the CSV into {(SYMBOL, year): {field: value}}. Raises ValueError naming the bad row."""
    path = Path(path)
    if not path.exists():
        return {}
    out: dict[tuple[str, int], dict[str, float]] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        for line, row in enumerate(csv.DictReader(fh), start=2):
            symbol = (row.get("symbol") or "").strip().upper()
            if not symbol or symbol.startswith("#"):
                continue
            try:
                year = int(row["year"])
                values = {f: float(row[f].replace(",", "")) for f in FIELDS if (row.get(f) or "").strip()}
            except (KeyError, ValueError) as e:
                raise ValueError(f"{path.name} line {line}: {e}") from e
            out[(symbol, year)] = values
    return out


def apply_manual(c: CompanyData, manual: dict[tuple[str, int], dict[str, float]]) -> int:
    """Copy manual figures onto the company's matching years (adding a year if absent). Returns rows applied."""
    applied = 0
    by_year = {y.year: y for y in c.years}
    for (symbol, year), values in manual.items():
        if symbol != c.symbol:
            continue
        y = by_year.get(year)
        if y is None:
            y = by_year[year] = YearFigures(year=year)
            c.years.append(y)
        for name, value in values.items():
            setattr(y, name, value)
        applied += 1
    c.years.sort(key=lambda y: y.year, reverse=True)
    return applied
