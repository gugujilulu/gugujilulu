"""Shared time split, same-information challengers and masking diagnostics."""

import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)


def run(n, seed):
    r = np.random.default_rng(seed)
    t = np.arange(n) / n
    weak = r.random(n) < (0.13 + 0.25 * t)
    x = r.normal(size=(n, 5))
    hidden = r.normal(size=n)
    # Selection regimes differ in latent risk and in observable signal strength.
    logit = -3.2 + np.where(
        weak,
        0.40 * x[:, 0] + 1.5 * hidden + 1.0 * t,
        1.0 * x[:, 0] + 1.5 * x[:, 1] + 0.9 * x[:, 2],
    )
    y = r.random(n) < expit(logit)
    psp = hidden + r.normal(0, 0.6, n)
    remaining = x[:, [0, 3, 4]]
    available = x.copy()
    available[weak, 1:3] = 0
    base = np.column_stack([available, weak])
    extended = np.column_stack([base, psp])
    train = t < 0.60
    test = t >= 0.80
    results = []
    predictions = []
    scenarios = [
        ("Production proxy", base, LogisticRegression(max_iter=400), train),
        (
            "Same-information challenger",
            base,
            HistGradientBoostingClassifier(
                max_iter=80, max_leaf_nodes=12, l2_regularization=5, random_state=seed
            ),
            train,
        ),
        (
            "Additional authorization signal",
            extended,
            HistGradientBoostingClassifier(
                max_iter=80, max_leaf_nodes=12, l2_regularization=5, random_state=seed
            ),
            train,
        ),
        (
            "Specialized low-observability",
            extended,
            LogisticRegression(max_iter=400),
            train & weak,
        ),
    ]
    for name, features, model, training in scenarios:
        model.fit(features[training], y[training])
        for group, mask in [("High", test & ~weak), ("Low", test & weak)]:
            if name.startswith("Specialized") and group == "High":
                continue
            pred = model.predict_proba(features[mask])[:, 1]
            results.append(
                dict(
                    model=name,
                    population=group,
                    n=int(mask.sum()),
                    roc_auc=roc_auc_score(y[mask], pred),
                    pr_auc=average_precision_score(y[mask], pred),
                    brier=brier_score_loss(y[mask], pred),
                    log_loss=log_loss(y[mask], pred),
                )
            )
            bins = pd.DataFrame({"p": pred, "y": y[mask]}).assign(
                bin=lambda a: pd.qcut(a.p, 6, duplicates="drop")
            )
            for _, g in bins.groupby("bin", observed=True):
                predictions.append(
                    dict(
                        model=name,
                        population=group,
                        predicted=g.p.mean(),
                        observed=g.y.mean(),
                        n=len(g),
                    )
                )
    # Equal observed columns; distinct population-generating mechanisms.
    for group, training, testing in [
        ("Masked high", train & ~weak, test & ~weak),
        ("Natural low", train & weak, test & weak),
    ]:
        m = LogisticRegression(max_iter=400).fit(remaining[training], y[training])
        pred = m.predict_proba(remaining[testing])[:, 1]
        results.append(
            dict(
                model="Remaining-information diagnostic",
                population=group,
                n=int(testing.sum()),
                roc_auc=roc_auc_score(y[testing], pred),
                pr_auc=average_precision_score(y[testing], pred),
                brier=brier_score_loss(y[testing], pred),
                log_loss=log_loss(y[testing], pred),
            )
        )
    return pd.DataFrame(results), pd.DataFrame(predictions)
