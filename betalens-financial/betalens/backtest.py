"""Point-in-time back-test of the scorecard.

At each month-end the scorecard is rebuilt using only what was known on that date, then compared with
what the share price did over the following 3 and 6 months, against the KSE-100.

Known limits, stated in the report: only companies in today's KSE-100 are tested (survivorship bias),
the portal carries four fiscal years so the test window is about two years, returns exclude dividends,
and monthly samples of 3- and 6-month returns overlap.
"""
from __future__ import annotations

import bisect
import calendar
import copy
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from betalens.data.parsers import dividend_summary
from betalens.models import CompanyData
from betalens.scoring.engine import score_company, signal_for

HORIZONS = {"3m": 63, "6m": 126}   # trading days
RESULTS_LAG_DAYS = 90              # annual results assumed public this long after the fiscal year end
# Alternative weightings of the six portal-data factors, compared in the report. Statement factors keep
# their configured weights. Each set totals 62, the same as the configured weights for these six.
VARIANTS = {
    "value_tilt": {"valuation": 20, "revenue_growth": 12, "dividend": 10, "earnings_growth": 8,
                   "profitability": 6, "price_trend": 6},
    "equal": {"valuation": 10, "revenue_growth": 10, "dividend": 10, "earnings_growth": 10,
              "profitability": 11, "price_trend": 11},
}
SIGNAL_ORDER = ["STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL", "INSUFFICIENT_DATA"]


def year_available_on(year: int, fy_end_month: int) -> date:
    last_day = calendar.monthrange(year, fy_end_month)[1]
    return date(year, fy_end_month, last_day) + timedelta(days=RESULTS_LAG_DAYS)


def as_of(full: CompanyData, when: date) -> CompanyData | None:
    """The company as it could have been known on `when`. None if there is no price by then."""
    cut = bisect.bisect_right(full.price_dates, when)
    if cut == 0:
        return None
    c = copy.copy(full)
    c.closes, c.index_closes, c.price_dates = full.closes[:cut], full.index_closes[:cut], full.price_dates[:cut]
    c.price = c.closes[-1]
    c.years = [y for y in full.years if year_available_on(y.year, full.fiscal_year_end_month) <= when]
    c.red_flags = []
    eps = c.years[0].eps if c.years else None
    c.pe_ratio = c.price / eps if eps else None   # negative EPS gives a negative P/E, scored as no earnings
    c.sector_pe_median = None                     # filled in across the whole universe by the caller
    announced = [p["announced"] for p in full.payouts if p["announced"]]
    c.payouts = [p for p in full.payouts if p["announced"] and p["announced"] <= when]
    if not full.payouts:                          # no payout on record at all: treat as a non-payer
        c.dividend_yield_pct, c.dividend_years_paid, c.dividend_window = 0.0, 0, 2
    elif when >= min(announced) + timedelta(days=330):
        s = dividend_summary(c.payouts, when)
        c.dividend_yield_pct = 100 * s["ttm_dividend_per_share"] / c.price
        c.dividend_years_paid, c.dividend_window = s["years_paid"], s["window"]
    else:                                         # record does not reach back a full year from this date
        c.dividend_yield_pct = c.dividend_years_paid = None
    return c


def _median(values: list[float]) -> float:
    v = sorted(values)
    mid = len(v) // 2
    return v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2


def _ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2
        i = j + 1
    return ranks


def spearman(x: list[float], y: list[float]) -> float | None:
    """Rank correlation, -1 to 1. None with fewer than 5 pairs or no variation."""
    if len(x) < 5:
        return None
    rx, ry = _ranks(x), _ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx, vy = sum((a - mx) ** 2 for a in rx), sum((b - my) ** 2 for b in ry)
    return cov / (vx * vy) ** 0.5 if vx and vy else None


def month_ends(start: date, end: date) -> list[date]:
    out, y, m = [], start.year, start.month
    while True:
        d = date(y, m, calendar.monthrange(y, m)[1])
        if d > end:
            return out
        if d >= start:
            out.append(d)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def observations(companies: list[CompanyData], cfg: dict) -> list[dict]:
    """One row per company per month-end: score, signal, factor scores and forward returns."""
    all_dates = sorted({d for c in companies for d in c.price_dates})
    if len(all_dates) < 260:
        return []
    rows: list[dict] = []
    for when in month_ends(all_dates[200], all_dates[-1 - min(HORIZONS.values())]):
        snaps = [(full, as_of(full, when)) for full in companies]
        snaps = [(full, s) for full, s in snaps if s is not None]
        by_sector: dict[str, list[float]] = defaultdict(list)
        for _, s in snaps:
            if s.pe_ratio and s.pe_ratio > 0:
                by_sector[s.sector].append(s.pe_ratio)
        for full, s in snaps:
            if len(by_sector[s.sector]) >= 3:
                s.sector_pe_median = _median(by_sector[s.sector])
            card = score_company(s, cfg)
            if card.score is None:
                continue
            i = len(s.closes) - 1
            row = {"date": when, "symbol": s.symbol, "score": card.score, "signal": card.signal,
                   "coverage": card.coverage_pct,
                   "factors": {f.name: f.score for f in card.factors if f.score is not None}}
            for label, h in HORIZONS.items():
                if i + h < len(full.closes) and len(full.index_closes) > i + h:
                    stock = 100 * (full.closes[i + h] / full.closes[i] - 1)
                    index = 100 * (full.index_closes[i + h] / full.index_closes[i] - 1)
                    row[f"ret_{label}"], row[f"excess_{label}"] = stock, stock - index
            rows.append(row)
    return rows


def _bucket_stats(rows: list[dict], label: str) -> dict | None:
    r = [x for x in rows if f"ret_{label}" in x]
    if not r:
        return None
    n = len(r)
    return {"n": n,
            "avg_return_pct": round(sum(x[f"ret_{label}"] for x in r) / n, 2),
            "avg_excess_pct": round(sum(x[f"excess_{label}"] for x in r) / n, 2),
            "beat_index_pct": round(100 * sum(1 for x in r if x[f"excess_{label}"] > 0) / n, 1),
            "positive_pct": round(100 * sum(1 for x in r if x[f"ret_{label}"] > 0) / n, 1)}


def _mean_ic(rows: list[dict], label: str, key) -> dict | None:
    by_date: dict[date, list[dict]] = defaultdict(list)
    for x in rows:
        if f"excess_{label}" in x and key(x) is not None:
            by_date[x["date"]].append(x)
    ics = [ic for group in by_date.values()
           if (ic := spearman([key(x) for x in group], [x[f"excess_{label}"] for x in group])) is not None]
    if not ics:
        return None
    return {"mean_ic": round(sum(ics) / len(ics), 3), "months": len(ics),
            "months_positive_pct": round(100 * sum(1 for i in ics if i > 0) / len(ics), 1)}


def percentile(values: list[float], pct: float) -> float:
    v = sorted(values)
    return v[min(len(v) - 1, int(pct / 100 * len(v)))]


def analyse(rows: list[dict], cfg: dict) -> dict:
    signalled = [x for x in rows if x["signal"] != "INSUFFICIENT_DATA"]
    scores = [x["score"] for x in signalled]
    report: dict = {"observations": len(rows), "with_signal": len(signalled),
                    "first_month": str(min(x["date"] for x in rows)) if rows else None,
                    "last_month": str(max(x["date"] for x in rows)) if rows else None,
                    "horizons": {}}
    suggested = None
    if len(scores) >= 100:
        suggested = {"strong_buy": round(percentile(scores, 90)), "buy": round(percentile(scores, 70)),
                     "hold": round(percentile(scores, 30)), "sell": round(percentile(scores, 10))}
    report["suggested_thresholds"] = suggested
    factor_names = sorted({n for x in rows for n in x["factors"]})
    for label in HORIZONS:
        h: dict = {"by_signal": {}, "by_quintile": {}, "by_suggested_signal": {}, "factor_ic": {}}
        for sig in SIGNAL_ORDER:
            if (st := _bucket_stats([x for x in rows if x["signal"] == sig], label)):
                h["by_signal"][sig] = st
        by_date: dict[date, list[dict]] = defaultdict(list)
        for x in signalled:
            if f"ret_{label}" in x:
                by_date[x["date"]].append(x)
        quintiles: dict[int, list[dict]] = defaultdict(list)
        for group in by_date.values():
            group.sort(key=lambda x: -x["score"])
            for rank, x in enumerate(group):
                quintiles[min(4, 5 * rank // len(group)) + 1].append(x)
        for q in sorted(quintiles):
            h["by_quintile"][f"Q{q}"] = _bucket_stats(quintiles[q], label)
        if suggested:
            for sig in SIGNAL_ORDER[:5]:
                if (st := _bucket_stats([x for x in signalled if signal_for(x["score"], suggested) == sig], label)):
                    h["by_suggested_signal"][sig] = st
        h["score_ic"] = _mean_ic(signalled, label, lambda x: x["score"])
        for name in factor_names:
            if (ic := _mean_ic(rows, label, lambda x, n=name: x["factors"].get(n))):
                h["factor_ic"][name] = ic
        report["horizons"][label] = h
    report["weightings"] = variant_comparison(rows, cfg)
    return report


def reweighted(rows: list[dict], weights: dict) -> list[dict]:
    """The same observations re-scored with different weights. Data availability is unchanged."""
    out = []
    for x in rows:
        w = {n: weights[n] for n in x["factors"] if n in weights}
        if not w:
            continue
        score = sum(x["factors"][n] * wt for n, wt in w.items()) / sum(w.values())
        out.append(dict(x, score=round(score, 1)))
    return out


def variant_comparison(rows: list[dict], cfg: dict) -> dict:
    """Top-fifth minus bottom-fifth out-performance and score rank correlation for each weighting."""
    signalled = [x for x in rows if x["signal"] != "INSUFFICIENT_DATA"]
    sets = {"current": dict(cfg["weights"])}
    for name, override in VARIANTS.items():
        sets[name] = {**cfg["weights"], **override}
    out: dict = {}
    for name, weights in sets.items():
        rescored = reweighted(signalled, weights)
        out[name] = {}
        for label in HORIZONS:
            by_date: dict[date, list[dict]] = defaultdict(list)
            for x in rescored:
                if f"excess_{label}" in x:
                    by_date[x["date"]].append(x)
            top, bottom = [], []
            for group in by_date.values():
                group.sort(key=lambda x: -x["score"])
                k = max(1, len(group) // 5)
                top += group[:k]
                bottom += group[-k:]
            if not top:
                continue
            t_stats, b_stats = _bucket_stats(top, label), _bucket_stats(bottom, label)
            ic = _mean_ic(rescored, label, lambda x: x["score"])
            out[name][label] = {"top_fifth_excess_pct": t_stats["avg_excess_pct"],
                                "bottom_fifth_excess_pct": b_stats["avg_excess_pct"],
                                "spread_pct": round(t_stats["avg_excess_pct"] - b_stats["avg_excess_pct"], 2),
                                "top_fifth_beat_index_pct": t_stats["beat_index_pct"],
                                "mean_ic": ic["mean_ic"] if ic else None}
    return out


def _table(header: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    return "\n".join(lines + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def to_markdown(report: dict, cfg: dict) -> str:
    out = ["# BetaLens back-test", "",
           f"{report['observations']} company-month observations, {report['with_signal']} with enough data for a "
           f"signal, from {report['first_month']} to {report['last_month']}. Look-back setting: "
           f"{cfg['period_years']} year(s).", "",
           "Read this as indicative, not proof. Only today's KSE-100 members are tested, the window is a few "
           "years, and monthly samples overlap. Share returns here exclude dividends while the KSE-100 is a "
           "total-return index, so out-performance is understated by roughly each share's dividend yield.", ""]
    cols = ["n", "avg_return_pct", "avg_excess_pct", "beat_index_pct", "positive_pct"]
    head = ["Observations", "Avg return %", "Avg vs KSE-100 %", "Beat index %", "Rose %"]
    for label, h in report["horizons"].items():
        out += [f"## {label} after the signal", "", "### By signal (current thresholds)", "",
                _table(["Signal"] + head, [[k] + [v[c] for c in cols] for k, v in h["by_signal"].items()]), "",
                "### By score rank each month (Q1 = top fifth)", "",
                _table(["Quintile"] + head, [[k] + [v[c] for c in cols] for k, v in h["by_quintile"].items() if v]), ""]
        if h["by_suggested_signal"]:
            out += ["### By signal (suggested thresholds)", "",
                    _table(["Signal"] + head, [[k] + [v[c] for c in cols] for k, v in h["by_suggested_signal"].items()]), ""]
        if h["score_ic"]:
            ic = h["score_ic"]
            out += [f"Overall score rank correlation with later out-performance: {ic['mean_ic']} "
                    f"(positive in {ic['months_positive_pct']}% of {ic['months']} months).", ""]
        out += ["### Which factors predicted out-performance", "",
                _table(["Factor", "Rank correlation", "Months", "Months positive %"],
                       [[k, v["mean_ic"], v["months"], v["months_positive_pct"]]
                        for k, v in sorted(h["factor_ic"].items(), key=lambda kv: -kv[1]["mean_ic"])]), ""]
    if report.get("weightings"):
        out += ["## Alternative factor weightings", "",
                "Top fifth and bottom fifth of scores each month, average return vs the KSE-100.", ""]
        rows = [[name, label, v["top_fifth_excess_pct"], v["bottom_fifth_excess_pct"], v["spread_pct"],
                 v["top_fifth_beat_index_pct"], v["mean_ic"]]
                for name, per in report["weightings"].items() for label, v in per.items()]
        out += [_table(["Weighting", "Horizon", "Top fifth %", "Bottom fifth %", "Spread %", "Top fifth beat index %",
                        "Rank correlation"], rows), ""]
        for name, override in VARIANTS.items():
            out.append(f"- `{name}`: " + ", ".join(f"{k} {v}" for k, v in override.items()))
        out.append("")
    if report["suggested_thresholds"]:
        s, cur = report["suggested_thresholds"], cfg["signals"]
        out += ["## Suggested thresholds", "",
                "Set so that about 10% of scores are Strong Buy, 20% Buy, 40% Hold, 20% Sell, 10% Strong Sell.", "",
                _table(["Band", "Current", "Suggested"], [[k, cur[k], s[k]] for k in ("strong_buy", "buy", "hold", "sell")]), ""]
    return "\n".join(out)


def write_report(companies: list[CompanyData], cfg: dict, out_dir: Path) -> dict:
    rows = observations(companies, cfg)
    report = analyse(rows, cfg) if rows else {"observations": 0, "with_signal": 0, "horizons": {},
                                              "first_month": None, "last_month": None, "suggested_thresholds": None}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(json.dumps(report, indent=1, default=str))
    (out_dir / "report.md").write_text(to_markdown(report, cfg))
    print(f"Back-test: {report['observations']} observations, {report['with_signal']} with a signal")
    return report
