"""Piecewise-linear scoring curves: map a raw metric to 0-100."""
from __future__ import annotations


def curve(x: float, points: list[tuple[float, float]]) -> float:
    """Interpolate x through (metric, score) points sorted by metric; clamp at both ends."""
    if x <= points[0][0]:
        return points[0][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return points[-1][1]


def cagr(latest: float | None, earliest: float | None, years: int) -> float | None:
    """Compound annual growth in %. None when either end is missing or the base is not positive."""
    if latest is None or earliest is None or years <= 0 or earliest <= 0:
        return None
    if latest <= 0:
        return -100.0
    return ((latest / earliest) ** (1 / years) - 1) * 100


def avg(values: list[float | None]) -> float | None:
    v = [x for x in values if x is not None]
    return sum(v) / len(v) if v else None
