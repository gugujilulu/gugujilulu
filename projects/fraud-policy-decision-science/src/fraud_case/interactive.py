"""Offline explorer: precomputed runs of the exact Python case-queue engine."""

import itertools
import json
from importlib.resources import files

from .operations import simulate


def build(root, cfg):
    grid = {}
    for cap, delay, displacement in itertools.product(
        [1280, 1500, 1730], [2, 5, 8], [0.2, 0.65, 0.95]
    ):
        for policy in ["fixed_0.2", "fixed_0.5", "fixed_0.8", "adaptive", "delayed"]:
            c = {
                **cfg,
                "weekly_capacity": cap,
                "evidence_delay_days": delay,
                "displacement_strength": displacement,
            }
            d, _ = simulate(c, policy, cfg["seed"])
            key = f"{cap}|{delay}|{displacement}|{policy}"
            grid[key] = {
                "backlog": d.backlog.tolist(),
                "saturation": d.saturation.tolist(),
                "value": d.value.cumsum().round(2).tolist(),
                "recovery": round(d.recovered.sum(), 2),
                "missed": int(d.missed.sum()),
            }
    template = files("fraud_case").joinpath("explorer.html").read_text()
    payload = json.dumps(grid, separators=(",", ":"))
    (root / "reports/policy_explorer.html").write_text(
        template.replace("__GRID__", payload)
    )
    return len(grid)
