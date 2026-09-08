"""Daily case queue with deadlines, evidence readiness and policy carryover.

Generated scenario, not a fitted payments model. Every liability dollar is charged
once at arrival; recovered dollars are credited once on resolution. Outstanding
cases at the evaluation horizon retain full liability (conservative terminal rule).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Controller:
    on: int = 1200
    off: int = 800
    delay: int = 7
    strong: bool = False
    below_since: int | None = None

    def action(self, day: int, backlog: int, delayed: bool) -> float:
        if backlog > self.on:
            self.strong = True
            self.below_since = None
        if self.strong:
            if backlog < self.off:
                if self.below_since is None:
                    self.below_since = day
                if not delayed or day - self.below_since >= self.delay:
                    self.strong = False
                    self.below_since = None
            else:
                self.below_since = None
        return 0.8 if self.strong else 0.2


def simulate(
    cfg: dict,
    policy: str,
    seed: int,
    extra_capacity: float = 0,
    automation: float = 0,
    nonlinear: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Policy-independent random streams per day enable paired comparisons.

    Daily service includes only evidence-ready cases, earliest deadline first.
    Evidence waiting blocks the case, not the analyst. Automation reduces delay,
    handling workload and incomplete packages. Nonlinear=False is an ablation
    with immediate service of ready cases; it removes capacity congestion only.
    """
    if cfg["threshold_off"] >= cfg["threshold_on"]:
        raise ValueError("Release threshold must be below activation threshold")
    if not 0 <= cfg["displacement_strength"] <= 1:
        raise ValueError("Displacement strength must be in [0,1]")
    if not 0 <= automation <= 1:
        raise ValueError("automation must be in [0,1]")
    if cfg["weekly_capacity"] + extra_capacity < 0:
        raise ValueError("negative capacity")
    ctrl = Controller(
        cfg["threshold_on"], cfg["threshold_off"], cfg["release_delay_days"]
    )
    q = []
    case_rows = []
    daily = []
    cid = 0
    memory = 0.2
    initial_rng = np.random.default_rng(seed + 998)
    for _ in range(cfg["initial_backlog"]):
        age = int(initial_rng.integers(0, 8))
        q.append(
            dict(
                case_id=cid,
                arrival_day=-age,
                ready_day=0,
                deadline=cfg["deadline_days"] - age,
                liability=float(
                    initial_rng.lognormal(np.log(cfg["case_mean_amount"]) - 0.18, 0.6)
                    * 0.85
                ),
                effort=1.0,
                complete=True,
                win_u=float(initial_rng.random()),
                initial=True,
            )
        )
        cid += 1
    for day in range(cfg["days"]):
        start = len(q)
        if policy.startswith("fixed_"):
            saturation = float(policy.split("_")[1])
            if not 0 <= saturation <= 1:
                raise ValueError("Saturation must be in [0,1]")
        elif policy in ["adaptive", "delayed"]:
            saturation = ctrl.action(day, start, policy == "delayed")
        else:
            raise ValueError("Unknown policy")
        # Slower adversary adaptation reduces durable suppression. History matters.
        memory += 0.075 * (saturation - memory)
        efficacy = 0.62 * saturation * (1 - cfg["displacement_strength"] * memory)
        r = np.random.default_rng(np.random.SeedSequence([seed, day, 41]))
        # Initial shock subsides, exposing the cost of maintaining high coverage.
        shock = 1.15 if day < 28 else (0.70 if day < 56 else 1.0)
        n = int(r.poisson(cfg["weekly_arrivals"] / 7 * shock))
        keep = r.random(n) > efficacy
        amounts = r.lognormal(np.log(cfg["case_mean_amount"]) - 0.18, 0.6, n)
        slow = r.random(n) < 0.42
        automated = (r.random(n) < automation) & slow
        delays = np.where(
            slow, r.gamma(2, cfg["evidence_delay_days"] / 2, n), r.uniform(0, 1, n)
        )
        delays = np.where(automated, 0, delays)
        completeness = r.random(n) < np.where(slow & ~automated, 0.67, 0.94)
        wins = r.random(n)
        new_liability = 0.0
        new_gross = 0.0
        arrived = int(keep.sum())
        for i in np.flatnonzero(keep):
            liability = float(amounts[i] * (0.9 - 0.18 * saturation))
            new_liability += liability
            new_gross += float(amounts[i])
            q.append(
                dict(
                    case_id=cid,
                    arrival_day=day,
                    ready_day=day + int(np.ceil(delays[i])),
                    deadline=day + cfg["deadline_days"],
                    liability=liability,
                    effort=0.65 if automated[i] else (1.25 if slow[i] else 1.0),
                    complete=bool(completeness[i]),
                    win_u=float(wins[i]),
                    initial=False,
                )
            )
            cid += 1
        recovered = 0.0
        closed = 0
        expired = 0
        spent = 0.0
        capacity = (cfg["weekly_capacity"] + extra_capacity) / 7
        remaining = []
        for case in sorted(q, key=lambda c: (c["deadline"], c["case_id"])):
            miss = day > case["deadline"]
            ready = case["ready_day"] <= day
            can_process = ready and (
                not nonlinear or spent + case["effort"] <= capacity
            )
            if miss or can_process:
                if not miss:
                    spent += case["effort"]
                won = (not miss) and case["win_u"] < (
                    0.62 if case["complete"] else 0.18
                )
                rec = case["liability"] * 0.85 if won else 0.0
                recovered += rec
                closed += 1
                expired += int(miss)
                case_rows.append(
                    {
                        **case,
                        "resolution_day": day,
                        "missed": int(miss),
                        "recovered": rec,
                        "outstanding": 0,
                        "queue_days": max(0, day - case["ready_day"]),
                    }
                )
            else:
                remaining.append(case)
        q = remaining
        assert len(q) == start + arrived - closed
        legitimate = cfg["weekly_legitimate_attempts"] / 7
        margin = legitimate * (0.925 - 0.045 * saturation) * cfg["margin_per_attempt"]
        auth_cost = legitimate * saturation * cfg["auth_cost"]
        operating = (
            cfg["weekly_capacity"] * 0.9 + extra_capacity * 1.3
        ) / 7 + automation * 1200 / 7
        value = margin - new_liability + recovered - auth_cost - operating
        daily.append(
            dict(
                day=day,
                policy=policy,
                saturation=saturation,
                memory=memory,
                backlog_start=start,
                arrivals=arrived,
                closed=closed,
                backlog=len(q),
                missed=expired,
                gross=new_gross,
                liability=new_liability,
                recovered=recovered,
                legitimate_margin=margin,
                authentication_cost=auth_cost,
                operating_cost=operating,
                value=value,
                service_work=spent,
                capacity=capacity,
            )
        )
    for case in q:
        case_rows.append(
            {
                **case,
                "resolution_day": None,
                "missed": 0,
                "recovered": 0.0,
                "outstanding": 1,
                "queue_days": None,
            }
        )
    return pd.DataFrame(daily), pd.DataFrame(case_rows)


def policy_grid(cfg):
    records = []
    trajectories = []
    for scenario, updates in [
        ("Base", {}),
        ("High displacement", {"displacement_strength": 0.95}),
        ("Low arrivals", {"weekly_arrivals": 1100}),
        ("High friction cost", {"margin_per_attempt": 65.0}),
    ]:
        c = {**cfg, **updates}
        for seed in range(cfg["policy_seeds"]):
            for policy in [
                "fixed_0.2",
                "fixed_0.5",
                "fixed_0.8",
                "adaptive",
                "delayed",
            ]:
                d, cases = simulate(c, policy, cfg["seed"] + seed)
                records.append(
                    dict(
                        scenario=scenario,
                        seed=seed,
                        policy=policy,
                        value=d.value.sum(),
                        ending_backlog=int(d.backlog.iloc[-1]),
                        miss_rate=cases.missed.mean(),
                        average_saturation=d.saturation.mean(),
                    )
                )
                if seed == 0:
                    trajectories.append(d.assign(scenario=scenario))
    return pd.DataFrame(records), pd.concat(trajectories, ignore_index=True)


def factorial(cfg):
    """Same +450/week dose in both capacity and combined cells."""
    rows = []
    for seed in range(cfg["policy_seeds"]):
        values = {}
        for label, cap, auto in [
            ("Baseline", 0, 0),
            ("Capacity", 450, 0),
            ("Automation", 0, 0.7),
            ("Combined", 450, 0.7),
        ]:
            d, _ = simulate(cfg, "fixed_0.2", cfg["seed"] + seed, cap, auto)
            values[label] = d.value.sum()
            rows.append(
                dict(
                    seed=seed,
                    intervention=label,
                    value=values[label],
                    backlog=d.backlog.iloc[-1],
                )
            )
        rows.append(
            dict(
                seed=seed,
                intervention="Interaction",
                value=values["Combined"]
                - values["Capacity"]
                - values["Automation"]
                + values["Baseline"],
                backlog=np.nan,
            )
        )
    return pd.DataFrame(rows)
