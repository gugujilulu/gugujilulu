# Artifact inventory

## Visual system

Deep navy backgrounds, electric cyan for improvements, coral for loss/friction, purple for policy/state and gold for annotations. Charts use explicit units and direct labels, with evidence populations in subtitles. SVGs preserve text and scale in GitHub. The pipeline exports matching PNGs for sharing.

| Figure | Role | Data source |
|---|---|---|
| `00_hero` | Three research turning points | Supplied case, three distinct populations |
| `01_system_map` | Two causal investigations joining at policy value | Conceptual map |
| `02_merchants` | Raw/standardized A, B and peer incidence | Generated settled history |
| `03_3ds_tradeoff` | Gross, net and completion effects | Supplied 3DS point estimates |
| `04_selection` | Completed-only example and assigned-population result | Separate supplied teaching/experiment populations |
| `05_information` | Equal-information, PSP, specialization and masking | Generated temporal holdout |
| `06_displacement` | Treated, other and total indexed loss | Supplied channel sequence |
| `07_waterfall` | Gross, other-party liability, recovery and net | Exact supplied accounting |
| `08_policy_paths` | Backlog, saturation and value over time | Generated low-arrival scenario, representative seed |
| `09_policy_sensitivity` | Fixed/adaptive/delayed policy comparison | Four generated scenarios × 12 paired seeds |
| `10_cohorts` | Recognition, observed and mature-cohort clocks | Generated transaction history |
| `11_operations_factorial` | Same-dose operations value and interaction | Generated 2×2 factorial × 12 paired seeds |
| `12_calibration` | Predicted probability versus observed incidence | Generated temporal holdout, six calibration bins |

All SVGs are in `results/figures/`; PNGs are reproducible exports. The self-contained `reports/policy_explorer.html` contains 135 exact precomputed combinations from the Python queue engine and displays backlog, intensity, realized recovery and incremental economic value. It supports desktop and narrow-screen layouts with labeled keyboard-operable controls.

## Analysis outputs

| Output group | Files in `results/tables/` |
|---|---|
| Metric and composition | `cohorts.csv`, `payment_type_cohorts.csv`, `merchant.csv`, `routing_diagnostics.csv` |
| Experiment | `itt.csv`, `heterogeneity.csv`, `itt_validation.csv` |
| Information/model | `models.csv`, `calibration.csv` |
| Operational policy | `policies.csv`, `policy_comparisons.csv`, `trajectories.csv` |
| Mechanism/accounting | `factorial.csv`, `uncongested_ablation.csv`, `decomposition.csv`, `saturation_channels.csv` |
| Sequential evaluation | `sequential_validation.csv` |

`assignment_logs.csv` and `sequential_logs.csv` are regenerated and excluded from version control. `results/summary.json` records configuration, environment and selected results; `results/manifest.json` fingerprints source and compact numerical outputs.

## Analysis source and reading paths

| Goal | Entry point |
|---|---|
| Five-minute portfolio review | Root project README and selected figures |
| Follow David's reasoning | `docs/research_narrative.md` |
| Review experimental identification | `docs/experiment.md` |
| Review modeling choices | `docs/model_diagnostics.md` |
| Review queue and sequential identification | `docs/adaptive_evaluation.md` |
| Inspect units and reproducibility | `docs/data_contracts.md` |
| Reconcile source claims | `docs/source_notes.md` and `data/case_inputs/` |
| Reproduce a module | Five notebooks in `notebooks/` |
| Rebuild everything | `run_all.py` |
