"""Synthetic worlds with known mechanisms; supplied case evidence stays separate."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import expit


def experiment(n: int, seed: int) -> pd.DataFrame:
    """Finite potential outcomes. Attempt value and strata precede assignment."""
    r = np.random.default_rng(seed)
    missing = r.binomial(1, 0.34, n)
    risk = r.choice(3, n, p=[0.40, 0.42, 0.18])
    amount = np.clip(r.lognormal(5.15, 0.72, n), 15, 2500)
    fraud = r.random(n) < expit(-3.9 + 0.8 * risk + 0.9 * missing)
    completion_u, fraud_u = r.random(n), r.random(n)
    completion0 = completion_u < 0.925
    completion1 = completion_u < (0.903 - 0.02 * missing)
    gross0 = amount * fraud * completion0
    gross1 = amount * fraud * completion1 * (fraud_u > (0.22 + 0.35 * missing))
    net0 = gross0 * 0.89
    net1 = gross1 * 0.74
    d = pd.DataFrame(
        dict(
            attempt_id=np.arange(n),
            amount=amount,
            missing=missing,
            risk=risk,
            completion0=completion0.astype(int),
            completion1=completion1.astype(int),
            gross0=gross0,
            gross1=gross1,
            net0=net0,
            net1=net1,
        )
    )
    d["stratum"] = missing * 3 + risk
    return assign(d, seed + 1)


def assign(d: pd.DataFrame, seed: int, probability: float = 0.2) -> pd.DataFrame:
    """Fixed allocation within strata; probability logs reflect actual fractions."""
    if not 0 < probability < 1:
        raise ValueError(
            "Assignment probability must lie strictly between zero and one"
        )
    out = d.copy()
    r = np.random.default_rng(seed)
    z = np.zeros(len(out), dtype=int)
    propensity = np.zeros(len(out))
    for _, indices in out.groupby("stratum", sort=True).indices.items():
        nt = min(len(indices) - 1, max(1, int(round(probability * len(indices)))))
        if len(indices) < 2:
            raise ValueError("Each stratum requires at least two observations")
        z[r.choice(indices, nt, replace=False)] = 1
        propensity[indices] = nt / len(indices)
    out["assignment"], out["propensity"] = z, propensity
    for metric in ["completion", "gross", "net"]:
        out[metric] = np.where(z, out[metric + "1"], out[metric + "0"])
    return out


def history(n: int, seed: int) -> pd.DataFrame:
    """Merchant B has risky mix; A has an extra route mechanism after day 150."""
    r = np.random.default_rng(seed)
    merchant = r.choice(["A", "B", "Peer"], n, p=[0.25, 0.25, 0.50])
    day = r.integers(0, 210, n)
    recent = day >= 150
    cross = r.random(n) < np.where(merchant == "B", 0.75, 0.25)
    cnp = r.random(n) < 0.78
    route = r.random(n) < np.where((merchant == "A") & recent, 0.65, 0.18)
    missing = r.random(n) < np.where(route, 0.40, 0.06)
    amount = np.clip(r.lognormal(4.9 + 0.3 * cross, 0.7, n), 10, 2200)
    p = expit(
        -5.2
        + 1.5 * cross
        + 0.5 * cnp
        + 0.4 * missing
        + 1.25 * ((merchant == "A") & route)
        + 0.55 * (recent & cnp)
    )
    fraud = r.random(n) < p
    gross = amount * fraud
    liability = gross * np.where(route, 0.90, 0.68)
    recovery = liability * np.where(recent, 0.33, 0.41)
    lag = np.maximum(1, r.gamma(3, 7, n).astype(int))
    return pd.DataFrame(
        dict(
            transaction_id=np.arange(n),
            transaction_day=day,
            report_day=day + np.maximum(1, lag // 2),
            recognition_day=day + lag,
            merchant=merchant,
            cross_border=cross.astype(int),
            cnp=cnp.astype(int),
            route=route.astype(int),
            missing=missing.astype(int),
            recent=recent.astype(int),
            amount=amount,
            fraud=fraud.astype(int),
            gross=gross,
            liability=liability,
            recovery=recovery,
            net=liability - recovery,
        )
    )
