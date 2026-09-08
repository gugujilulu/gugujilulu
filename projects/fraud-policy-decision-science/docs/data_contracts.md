# Data and execution contracts

## Generated tables

| Table | Grain and required fields | Interpretation |
|---|---|---|
| `settled_history.csv` | One settled transaction; ID, amount, transaction/report/recognition day, merchant, geography, CNP, route, fraud, liability, recovery | Full denominator population, days 0–209; recognition may occur later |
| `experiment_with_potential_outcomes.csv` | One eligible attempt; pre-action amount/stratum, assignment, propensity, observed outcomes and suffix-0/1 potential outcomes | Potential outcomes are available solely for simulation validation |
| `assignment_logs.csv` | Same attempt grain with observed outcomes only | Estimation inputs; all assigned attempts retained |
| `recovery_cases.csv` | One unique case including initial backlog; arrival/ready/deadline, effort, liability, resolution, recovered, outstanding | One representative delayed-policy run; initial liability treated as sunk |
| `saturation_channels.csv` | One channel-week; randomized block/saturation, marginal probability, prior memory, incoming/outgoing displacement, losses | Six channels per week and four weeks per block; constrained joint randomization |
| `sequential_logs.csv` | One episode-step; pre-action state, action, propensity, reward | Independent four-step randomized state world; first validation replicate |

Large generated datasets and assignment logs are regenerated locally. Committed tables contain compact estimates, validation summaries and trajectories. `results/manifest.json` records SHA-256 for analysis code, configuration, supplied inputs and compact result tables. It excludes itself, generated microdata and large logs.

## Five analysis modules

1. **Metrics and maturity:** `data.history` → SQLite `cohorts.sql` / `recognition.sql` → `cohorts.csv`.
2. **Merchant comparison:** recent full settled history → pre-routing direct standardization → `merchant.csv`.
3. **Randomized intervention:** potential-outcome generator → stratified assignment → observed-data ITT and heterogeneity → Monte Carlo validation.
4. **Model/information diagnostics:** temporal split → equal-information challengers, PSP addition, specialization, masking → ranking/calibration tables.
5. **System policy:** case engine + channel saturation experiment + matched factorial + full-policy scenarios; separate sequential-estimator calibration.

`run_all.py` is the authoritative orchestration entry. Notebooks import these same functions and add interpretation. The explorer reads precomputed results from the same operational engine. It selects a discrete grid and provides no interpolated or browser-generated economic estimates.

## Reproducibility

The configuration records all main sample sizes, seeds, queue costs and controller settings. Small design constants (time split, model complexity, recovery probabilities, memory update) are documented in source and versioned in the manifest. The explorer grid and sensitivity scenarios are fixed in source. NumPy random generators and scikit-learn model seeds are explicit. Pinned direct dependencies record the tested environment; indirect dependencies may differ across platforms. SVG text remains selectable and metadata dates are removed; PNG files are rendered by the same plotting code.

Outcome scaling: generated loss estimators are proportions; multiply by 100 for percentage points. Queue economic values are generated USD amounts, not estimates from the supplied operational table. Backlog is case count; capacity is service-work units per week. The `case_mean_amount` key is a lognormal scale parameter, so its arithmetic mean also depends on the fixed dispersion/offset.

## Execution checks

Run `python -m unittest discover -s tests -v`. Tests cover randomization logs, observed-outcome consistency, a known constant treatment effect, accounting/Shapley reconciliation, SQL maturity and full denominators, case/ledger/terminal conservation, reproducibility, controller hysteresis and delayed release, capacity ablation, randomized channel exposure conservation, and invalid inputs. Monte Carlo interval calibration is a computed analysis output rather than a brittle pass/fail coverage threshold.
