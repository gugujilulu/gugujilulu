"""Short-horizon sequential IPW validation in a separate known-state world.

This compact experiment demonstrates estimator identification independently of the
richer queue simulator. Behavioral policy randomizes low/high with probability .5.
"""

import numpy as np
import pandas as pd


def action(policy, state, step):
    if policy == "fixed_low":
        return 0
    if policy == "fixed_high":
        return 1
    return int(state > 1.0)


def transition(state, a, noise):
    reward = 3.0 - 1.8 * state - 0.65 * a + 1.2 * a * state
    return max(0.0, 0.65 * state + 0.70 - 0.65 * a + noise), reward


def run(seed, repetitions=60, n=2200, horizon=4):
    rows = []
    logs = []
    # Large independent on-policy reference supplies known-DGP value.
    truth = {}
    for policy in ["fixed_low", "fixed_high", "adaptive"]:
        r = np.random.default_rng(seed + 77)
        state = r.uniform(0.5, 1.8, 100000)
        value = np.zeros(len(state))
        for t in range(horizon):
            a = (
                np.zeros(len(state))
                if policy == "fixed_low"
                else (
                    np.ones(len(state))
                    if policy == "fixed_high"
                    else (state > 1.0).astype(int)
                )
            )
            value += 3.0 - 1.8 * state - 0.65 * a + 1.2 * a * state
            state = np.maximum(
                0, 0.65 * state + 0.70 - 0.65 * a + r.normal(0, 0.12, len(state))
            )
        truth[policy] = value.mean()
    for rep in range(repetitions):
        r = np.random.default_rng(seed + rep)
        states = r.uniform(0.5, 1.8, n)
        total = np.zeros(n)
        matches = {k: np.ones(n, dtype=bool) for k in truth}
        for t in range(horizon):
            a = r.binomial(1, 0.5, n)
            reward = 3.0 - 1.8 * states - 0.65 * a + 1.2 * a * states
            total += reward
            for policy in truth:
                target = np.array([action(policy, s, t) for s in states])
                matches[policy] &= a == target
            if rep == 0:
                logs.extend(
                    dict(
                        episode=i,
                        step=t,
                        state=float(states[i]),
                        action=int(a[i]),
                        propensity=0.5,
                        reward=float(reward[i]),
                    )
                    for i in range(n)
                )
            states = np.maximum(
                0, 0.65 * states + 0.70 - 0.65 * a + r.normal(0, 0.12, n)
            )
        for policy in truth:
            weighted = matches[policy] * 2**horizon * total
            estimate = weighted.mean()
            se = weighted.std(ddof=1) / np.sqrt(n)
            rows.append(
                dict(
                    repetition=rep,
                    policy=policy,
                    truth=truth[policy],
                    estimate=estimate,
                    lower=estimate - 1.96 * se,
                    upper=estimate + 1.96 * se,
                    covered=abs(estimate - truth[policy]) <= 1.96 * se,
                    effective_sample=int(matches[policy].sum()),
                )
            )
    return pd.DataFrame(rows), pd.DataFrame(logs)
