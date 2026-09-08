"""Six-channel randomized saturation experiment with delayed spillover.

Independent generated mechanism study. Randomized block schedules identify
intention-to-treat contrasts over the schedule distribution; current-saturation
means alone do not identify a steady-state response under carryover.
"""

import numpy as np
import pandas as pd


def run(seed, blocks=12):
    r = np.random.default_rng(seed)
    memory = np.full(6, 0.2)
    rows = []
    for block in range(blocks):
        levels = r.permutation(np.tile([0.2, 0.5, 0.8], 2))
        previous = memory.copy()
        for week in range(4):
            # Potential displaced attempts seek other channels, conserving arrivals.
            memory += 0.3 * (levels - memory)
            displaced = 1000 * 0.5 * memory
            incoming = (displaced.sum() - displaced) / 5
            attempts = 1000 - displaced + incoming
            losses = attempts * (1 - 0.62 * levels) * r.lognormal(-0.005, 0.1, 6)
            for channel in range(6):
                rows.append(
                    dict(
                        block=block,
                        week=4 * block + week,
                        week_in_block=week + 1,
                        channel=channel,
                        saturation=levels[channel],
                        assignment_probability=1 / 3,
                        prior_memory=previous[channel],
                        memory=memory[channel],
                        displaced_out=displaced[channel],
                        displaced_in=incoming[channel],
                        attack_attempts=attempts[channel],
                        indexed_loss=losses[channel],
                    )
                )
    return pd.DataFrame(rows)
