"""Stratum-standardized ratio ITT and finite-population Monte Carlo validation."""

import numpy as np
import pandas as pd

from .data import assign


def ratio_itt(d, outcome="net", denominator="amount"):
    """Ratio of standardized means. Delta variance respects stratified assignment.

    Independent-arm Neyman variance is conservative for heterogeneous effects.
    Both arms target the original pre-treatment stratum weights.
    """
    if d.empty or not d.assignment.isin([0, 1]).all():
        raise ValueError("A nonempty binary-assignment sample is required")
    counts = d.groupby(["stratum", "assignment"]).size().unstack(fill_value=0)
    if len(counts.columns) != 2 or (counts < 2).any().any():
        raise ValueError(
            "Each stratum-arm needs at least two observations for variance"
        )
    if denominator and (d[denominator] <= 0).any():
        raise ValueError("Denominators must be positive pre-treatment values")
    numeric = [outcome] + ([denominator] if denominator else [])
    if not np.isfinite(d[numeric].to_numpy()).all():
        raise ValueError("Outcomes and denominators must be finite")
    arm = []
    for z in [0, 1]:
        numerator = denominator_mean = 0.0
        pieces = []
        for _, cell in d.groupby("stratum"):
            a = cell[cell.assignment == z]
            w = len(cell) / len(d)
            den = a[denominator].to_numpy() if denominator else np.ones(len(a))
            y = a[outcome].to_numpy()
            numerator += w * y.mean()
            denominator_mean += w * den.mean()
            pieces.append((w, y, den))
        estimate = numerator / denominator_mean
        variance = (
            sum(
                w * w * np.var(y - estimate * den, ddof=1) / len(y)
                for w, y, den in pieces
            )
            / denominator_mean**2
        )
        arm.append((estimate, variance))
    effect = arm[1][0] - arm[0][0]
    se = np.sqrt(arm[0][1] + arm[1][1])
    return dict(
        control=arm[0][0],
        treatment=arm[1][0],
        effect=effect,
        se=se,
        lower=effect - 1.96 * se,
        upper=effect + 1.96 * se,
    )


def analyze(d):
    rows = []
    for group, frame in [
        ("All", d),
        ("Device present", d[d.missing == 0]),
        ("Device missing", d[d.missing == 1]),
    ]:
        for metric in ["net", "gross", "completion"]:
            rows.append(
                dict(
                    group=group,
                    metric=metric,
                    **ratio_itt(
                        frame, metric, None if metric == "completion" else "amount"
                    ),
                )
            )
    return pd.DataFrame(rows)


def validate(d, repetitions, seed):
    truth = (d.net1.sum() - d.net0.sum()) / d.amount.sum()
    rows = []
    for i in range(repetitions):
        result = ratio_itt(assign(d, seed + i))
        rows.append(
            dict(
                repetition=i,
                truth=truth,
                **result,
                covered=result["lower"] <= truth <= result["upper"],
            )
        )
    return pd.DataFrame(rows)
