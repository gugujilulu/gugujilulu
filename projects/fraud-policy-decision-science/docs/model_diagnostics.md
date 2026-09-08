# Information and model diagnostics

`models.py` generates 18,000 ordered records. Training uses the first 60%; the middle 20% is an unused temporal gap; evaluation uses the final 20%. No hyperparameter search uses the holdout. Missingness prevalence and latent risk vary with time.

| Model | Authorization-time information | Training population |
|---|---|---|
| Production proxy | Available internal features + availability indicator | Early full population |
| Same-information challenger | Exactly the same columns as the proxy | Same early full population |
| Additional authorization signal | Internal columns + simulated PSP signal | Same early full population |
| Specialized low-observability | Extended PSP feature set | Early low-observability records |
| Remaining-information diagnostic | Only columns that remain observed | Separate masked-high and natural-low populations |

The specialized model combines a population-specific fit and the extra PSP feature; its comparison with the same-information challenger changes two aspects. Compare it with the global additional-signal model to examine specialization at a common information set. The simulation's specialization uses the early weak-observability subset; the supplied case's specialized model also used recent history. These are recorded as different designs.

ROC-AUC measures ranking. Average precision depends on prevalence; comparing it across populations also compares base rates. Brier score and log loss measure probability quality, and six equal-count calibration bins describe agreement between mean prediction and observed incidence. Bin summaries are descriptive and have sampling variability. `pr_auc` in outputs is scikit-learn's **average precision**, not trapezoidal area under an interpolated PR curve.

The masking diagnostic retrains with the remaining columns in each population. It estimates achievable prediction with that feature set under each generating regime. It is distinct from dropping features only at inference time or applying one identical trained model across both populations. Population-level AUC differences alone cannot uniquely allocate the gap to selection, interactions or unobserved risk.

This version records temporal performance, calibration and mechanism comparisons. Quantifying uncertainty in the AUC differences would require a paired holdout bootstrap or equivalent estimator; the point estimates are presented descriptively. The generated process supplies testable counterexamples to the idea that model complexity alone resolves missing information.
