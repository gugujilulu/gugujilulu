"""Invariant and identification tests; Monte Carlo calibration is a separate report."""

import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from fraud_case import cohorts, data, decomposition, estimators, operations, saturation

ROOT = Path(__file__).resolve().parents[1]


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {
            **json.loads((ROOT / "configs/base.json").read_text()),
            "days": 21,
            "initial_backlog": 100,
            "weekly_arrivals": 250,
            "weekly_capacity": 200,
        }

    def test_assignment_and_observed_outcomes(self):
        d = data.experiment(6000, 12)
        for _, g in d.groupby("stratum"):
            self.assertAlmostEqual(g.assignment.mean(), g.propensity.iloc[0])
        for m in ["gross", "net", "completion"]:
            np.testing.assert_array_equal(
                d[m], np.where(d.assignment, d[m + "1"], d[m + "0"])
            )
        self.assertTrue((d.net <= d.gross).all())

    def test_constant_effect_is_recovered_without_oracle(self):
        rows = [
            dict(stratum=s, assignment=z, amount=100.0, net=5.0 + 2 * z)
            for s in range(2)
            for z in range(2)
            for _ in range(20)
        ]
        e = estimators.ratio_itt(pd.DataFrame(rows))
        self.assertAlmostEqual(e["effect"], 0.02)
        self.assertAlmostEqual(e["se"], 0.0)

    def test_exact_decomposition_reconciles_both_methods(self):
        for _, g in decomposition.run().groupby("method"):
            self.assertAlmostEqual(g.value.sum(), 19.0)
        self.assertAlmostEqual(
            sum(decomposition.shapley((100, 0.68, 0.4), (100, 0.68, 0.4)).values()), 0.0
        )

    def test_sql_maturity_and_denominator(self):
        d = data.history(6000, 3)
        result = cohorts.run(d, ROOT)
        self.assertEqual(int(result.transactions.sum()), len(d))
        self.assertTrue((result.loc[result.week >= 25, "mature"] == 0).all())
        self.assertTrue(
            (
                result.loc[result.mature == 1, "naive_rate"] + 1e-12
                >= result.loc[result.mature == 1, "fixed_window_rate"]
            ).all()
        )

    def test_queue_stock_cash_and_terminal_identity(self):
        d, c = operations.simulate(self.cfg, "fixed_0.5", 12)
        np.testing.assert_array_equal(
            d.backlog, d.backlog_start + d.arrivals - d.closed
        )
        self.assertEqual(int(c.outstanding.sum()), d.backlog.iloc[-1])
        self.assertAlmostEqual(d.recovered.sum(), c.recovered.sum())
        self.assertAlmostEqual(d.liability.sum(), c.loc[~c.initial, "liability"].sum())
        np.testing.assert_allclose(
            d.value,
            d.legitimate_margin
            - d.liability
            + d.recovered
            - d.authentication_cost
            - d.operating_cost,
        )
        self.assertTrue((d.service_work <= d.capacity + 1e-9).all())
        self.assertTrue((c.recovered <= c.liability).all())
        self.assertEqual(c.case_id.nunique(), len(c))

    def test_seed_reproducibility(self):
        a, _ = operations.simulate(self.cfg, "adaptive", 7)
        b, _ = operations.simulate(self.cfg, "adaptive", 7)
        pd.testing.assert_frame_equal(a, b)

    def test_hysteresis_and_continuous_delay(self):
        c = operations.Controller(delay=2)
        self.assertEqual(c.action(0, 1300, True), 0.8)
        self.assertEqual(c.action(1, 700, True), 0.8)
        self.assertEqual(c.action(2, 900, True), 0.8)  # resets the release clock
        self.assertEqual(c.action(3, 700, True), 0.8)
        self.assertEqual(c.action(4, 700, True), 0.8)
        self.assertEqual(c.action(5, 700, True), 0.2)
        self.assertEqual(c.action(6, 1000, True), 0.2)

    def test_no_congestion_capacity_has_only_cost_effect(self):
        a, _ = operations.simulate(self.cfg, "fixed_0.2", 9, nonlinear=False)
        b, _ = operations.simulate(
            self.cfg, "fixed_0.2", 9, extra_capacity=450, nonlinear=False
        )
        self.assertAlmostEqual(a.recovered.sum(), b.recovered.sum())
        self.assertAlmostEqual(
            b.value.sum() - a.value.sum(), -450 * 1.3 / 7 * self.cfg["days"]
        )

    def test_saturation_randomization_and_displacement_conservation(self):
        d = saturation.run(7, blocks=4)
        for _, g in d.groupby("week"):
            self.assertAlmostEqual(g.displaced_out.sum(), g.displaced_in.sum())
            self.assertAlmostEqual(g.attack_attempts.sum(), 6000)
            self.assertEqual(
                sorted(g.saturation.tolist()), [0.2, 0.2, 0.5, 0.5, 0.8, 0.8]
            )
        self.assertTrue((d.assignment_probability > 0).all())

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            data.assign(data.experiment(100, 1), 1, probability=1)
        with self.assertRaises(ValueError):
            operations.simulate(self.cfg, "unknown", 1)
        with self.assertRaises(ValueError):
            operations.simulate(self.cfg, "adaptive", 1, automation=1.2)


if __name__ == "__main__":
    unittest.main()
