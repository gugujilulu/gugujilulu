"""Exact accounting and explicit interaction versus Shapley allocation."""

import itertools
import math
import pandas as pd


def loss(gross, share, recovery):
    return gross * share * (1 - recovery)


def shapley(before, after):
    names = ["gross", "liability_share", "recovery_rate"]
    result = {k: 0.0 for k in names}
    for ordering in itertools.permutations(range(3)):
        state = list(before)
        for j in ordering:
            previous = loss(*state)
            state[j] = after[j]
            result[names[j]] += (loss(*state) - previous) / math.factorial(3)
    return result


def run():
    # Exact fractions preserve the supplied 100 -> 128 / 40 -> 59 accounting.
    before = (100, 68 / 100, 28 / 68)
    after = (128, 92 / 128, 33 / 92)
    baseline = loss(*before)
    # Group gross/liability as structural and recovery as process.
    structural = loss(after[0], after[1], before[2]) - baseline
    process = loss(before[0], before[1], after[2]) - baseline
    interaction = loss(*after) - baseline - structural - process
    components = pd.DataFrame(
        [
            dict(method="Explicit interaction", component=k, value=v)
            for k, v in [
                ("Structure", structural),
                ("Process", process),
                ("Interaction", interaction),
            ]
        ]
        + [
            dict(method="Shapley allocation", component=k, value=v)
            for k, v in shapley(before, after).items()
        ]
    )
    return components
