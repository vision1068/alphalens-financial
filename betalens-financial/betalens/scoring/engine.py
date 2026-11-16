"""Combine factor scores into one 0-100 score, a coverage figure and a signal."""
from __future__ import annotations

from pathlib import Path

import yaml

from betalens.models import CompanyData, FactorResult, Scorecard
from betalens.scoring.factors import FACTORS

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "scorecard.yaml"


def load_config(path: Path | str = DEFAULT_CONFIG) -> dict:
    cfg = yaml.safe_load(Path(path).read_text())
    unknown = (set(cfg["weights"]) | set(cfg.get("financial_extra_weights") or {})
               | set(cfg.get("bank_extra_weights") or {})) - set(FACTORS)
    if unknown:
        raise ValueError(f"Unknown factors in config: {sorted(unknown)}")
    if cfg["period_years"] not in (1, 3):
        raise ValueError("period_years must be 1 or 3")
    return cfg


def signal_for(score: float, bands: dict) -> str:
    if score >= bands["strong_buy"]:
        return "STRONG_BUY"
    if score >= bands["buy"]:
        return "BUY"
    if score >= bands["hold"]:
        return "HOLD"
    if score >= bands["sell"]:
        return "SELL"
    return "STRONG_SELL"


def score_company(c: CompanyData, cfg: dict) -> Scorecard:
    weights = dict(cfg["weights"])
    sector = c.sector.upper()
    if sector in {s.upper() for s in cfg.get("financial_sectors", [])}:
        for name in cfg.get("financial_excluded_factors", []):
            weights.pop(name, None)
        weights.update(cfg.get("financial_extra_weights") or {})
        if sector in {s.upper() for s in cfg.get("bank_sectors", [])}:
            weights.update(cfg.get("bank_extra_weights") or {})
    total_weight = sum(weights.values())
    results: list[FactorResult] = []
    for name, weight in weights.items():
        score, reasons = FACTORS[name](c, cfg["period_years"])
        results.append(FactorResult(name, None if score is None else round(score, 1), weight, reasons))
    scored = [r for r in results if r.score is not None]
    covered = sum(r.weight for r in scored)
    coverage = 100 * covered / total_weight if total_weight else 0.0
    if not scored:
        return Scorecard(c.symbol, None, 0.0, "INSUFFICIENT_DATA", results, c.red_flags)
    overall = sum(r.score * r.weight for r in scored) / covered
    signal = signal_for(overall, cfg["signals"]) if coverage >= cfg["min_coverage"] else "INSUFFICIENT_DATA"
    return Scorecard(c.symbol, round(overall, 1), round(coverage, 1), signal, results, c.red_flags)
