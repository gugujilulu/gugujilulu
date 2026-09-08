#!/usr/bin/env python3
"""Regenerate the complete project from explicit configuration."""

from pathlib import Path
import argparse, hashlib, json, platform, sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import pandas as pd
import numpy as np
from fraud_case import (
    data,
    cohorts,
    estimators,
    models,
    operations,
    decomposition,
    sequential,
    figures,
    saturation,
    interactive,
    reporting,
)


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(root / "configs/base.json"))
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    generated = root / "data/generated"
    generated.mkdir(exist_ok=True)
    out = root / "results/tables"
    out.mkdir(parents=True, exist_ok=True)

    def write(name, df):
        df.to_csv(out / f"{name}.csv", index=False, float_format="%.8f")
        return df

    print("1/6: transaction history, SQL cohorts and merchant comparison", flush=True)
    history = data.history(cfg["n_history"], cfg["seed"])
    history.to_csv(generated / "settled_history.csv", index=False)
    cohort = write("cohorts", cohorts.run(history, root))
    merchant = write("merchant", cohorts.merchant_comparison(history))
    write("payment_type_cohorts", cohorts.payment_type_cohorts(history, root))
    write("routing_diagnostics", cohorts.routing_diagnostics(history))
    print(
        "2/6: randomized policy and finite-population estimator validation", flush=True
    )
    trial = data.experiment(cfg["n_transactions"], cfg["seed"])
    trial.to_csv(generated / "experiment_with_potential_outcomes.csv", index=False)
    # Oracle columns are simulation validation only; estimator accepts observed columns.
    observed = trial.drop(
        columns=[f"{m}{z}" for m in ["net", "gross", "completion"] for z in [0, 1]]
    )
    observed.to_csv(out / "assignment_logs.csv", index=False)
    itt = write("itt", estimators.analyze(observed))
    mc = write(
        "itt_validation",
        estimators.validate(trial, cfg["mc_repetitions"], cfg["seed"] + 100),
    )
    print("3/6: temporal model and information diagnostics", flush=True)
    model, calibration = models.run(cfg["n_model"], cfg["seed"])
    write("models", model)
    write("calibration", calibration)
    print("4/6: shared recovery queue, fixed and adaptive policy scenarios", flush=True)
    policies, paths = operations.policy_grid(cfg)
    write("policies", policies)
    write("trajectories", paths)
    write("factorial", operations.factorial(cfg))
    write("decomposition", decomposition.run())
    write("saturation_channels", saturation.run(cfg["seed"]))
    wide = policies.pivot(index=["scenario", "seed"], columns="policy", values="value")
    paired = wide.sub(wide["fixed_0.5"], axis=0).stack().rename("delta").reset_index()
    ps = (
        paired.groupby(["scenario", "policy"])
        .delta.agg(["mean", "std", "count"])
        .reset_index()
    )
    from scipy.stats import t

    ps["half_width"] = t.ppf(0.975, ps["count"] - 1) * ps["std"] / np.sqrt(ps["count"])
    ps["lower"] = ps["mean"] - ps["half_width"]
    ps["upper"] = ps["mean"] + ps["half_width"]
    write("policy_comparisons", ps)
    hetero = itt[itt.metric == "net"].set_index("group")
    contrast = (
        hetero.loc["Device missing", "effect"] - hetero.loc["Device present", "effect"]
    )
    se = float(
        np.hypot(hetero.loc["Device missing", "se"], hetero.loc["Device present", "se"])
    )
    write(
        "heterogeneity",
        pd.DataFrame(
            [
                dict(
                    contrast="Missing minus present net ITT",
                    effect=contrast,
                    se=se,
                    lower=contrast - 1.96 * se,
                    upper=contrast + 1.96 * se,
                )
            ]
        ),
    )
    daily, cases = operations.simulate(cfg, "delayed", cfg["seed"])
    cases.to_csv(generated / "recovery_cases.csv", index=False)
    ablation = []
    for label, cap, auto in [
        ("Baseline", 0, 0),
        ("Capacity", 450, 0),
        ("Automation", 0, 0.7),
        ("Combined", 450, 0.7),
    ]:
        d, _ = operations.simulate(
            cfg, "fixed_0.2", cfg["seed"], cap, auto, nonlinear=False
        )
        ablation.append(
            dict(intervention=label, value=d.value.sum(), backlog=d.backlog.iloc[-1])
        )
    write("uncongested_ablation", pd.DataFrame(ablation))
    print("5/6: sequential randomized-policy value validation", flush=True)
    seq, logs = sequential.run(cfg["seed"])
    write("sequential_validation", seq)
    write("sequential_logs", logs)
    print("6/6: high-contrast figures and reproducibility manifest", flush=True)
    figures.generate(
        root / "results/figures",
        dict(
            merchant=merchant,
            models=model,
            trajectories=paths,
            policies=policies,
            cohorts=cohort,
        ),
    )
    summary = {
        "itt_net": itt[(itt.group == "All") & (itt.metric == "net")].iloc[0].to_dict(),
        "itt_validation": {
            "repetitions": len(mc),
            "bias": float((mc.effect - mc.truth).mean()),
            "coverage": float(mc.covered.mean()),
            "coverage_mc_se": float(
                np.sqrt(mc.covered.mean() * (1 - mc.covered.mean()) / len(mc))
            ),
        },
        "sequential_validation": seq.assign(error=seq.estimate - seq.truth)
        .groupby("policy")
        .agg(
            bias=("error", "mean"),
            coverage=("covered", "mean"),
            mean_effective_sample=("effective_sample", "mean"),
        )
        .to_dict("index"),
        "base_policy_values": policies[policies.scenario == "Base"]
        .groupby("policy")
        .value.mean()
        .to_dict(),
        "configuration": cfg,
        "python": platform.python_version(),
        "libraries": {
            name: __import__(name).__version__
            for name in ["numpy", "pandas", "scipy", "sklearn", "matplotlib"]
        },
    }
    (root / "results/summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("Building 135 offline explorer scenarios", flush=True)
    interactive.build(root, cfg)
    reporting.build(root)
    hashes = {
        str(f.relative_to(root)): hashlib.sha256(f.read_bytes()).hexdigest()
        for folder in ["src", "sql", "configs", "data/case_inputs", "results/tables"]
        for f in sorted((root / folder).rglob("*"))
        if f.is_file()
        and "__pycache__" not in str(f)
        and f.name not in ["assignment_logs.csv", "sequential_logs.csv"]
    }
    hashes.update(
        {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in [
                "run_all.py",
                "check_artifacts.py",
                "requirements-lock.txt",
                "pyproject.toml",
            ]
        }
    )
    (root / "results/manifest.json").write_text(json.dumps(hashes, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
