# Evidence map and reconciliation

The author supplied `Decision_Scientist_Fraud_Case_Full_Transcript(1).md` and `fraud_case_study_guide(1).html`. The transcript records a simulated research interview and David's analytical responses. The guide summarizes the investigation. [Source hashes](../data/case_inputs/source_manifest.json) identify the reviewed versions; the source files remain with the author. This repository publishes curated case evidence and executable reconstructions.

## Provenance map

Line locations below refer to the supplied Markdown transcript. They let the author trace the case back to the reviewed copy; they are not links to publicly available source data.

| Evidence | Transcript location | Repository representation |
|---|---|---|
| Opening 0.32% → 0.47%, three clocks, mature CNP 0.44% → 0.78% | Opening around 868; metric discussion 953–1072 | `portfolio_metrics.csv`; SQL cohorts |
| Fraud count +49%, severity +12%, CNP volume +3% | Reintroduced at 1330 onward | `portfolio_metrics.csv`; research narrative |
| Categories 57%, merchants 21% | Reintroduced at 1352–1390 | Research narrative; overlapping attribution explained |
| Merchant A raw 2.8×, matched 1.6×; Merchant B counterexample | Around 1749 onward | `merchant_routing.csv`; separate generated standardization |
| Authentication-state and PSP route evidence | Around 1788–1900 | `merchant_routing.csv`; narrative |
| 80,000 eligible, 20% assignment, four weeks | 1990–1998 | Experiment design; separate generated 80,000 attempts |
| Gross/net/completion ITT | Table around 2213–2214 | `3ds_itt.csv`; figure 03 |
| Completed-only frequency and severity; device heterogeneity | Around 2296–2346 | `device_heterogeneity.csv`; experiment note |
| Observability effect gradient | Around 2584 onward | `observability.csv` |
| Model quality, masking, PSP signal, specialized model | 2692–2862 | Model diagnostics; generated temporal holdout |
| Channel displacement | Table 3074–3078 | `displacement.csv`; figure 06 |
| Saturation and carryover | Around 3504–3571 | `saturation_evidence.csv`; generated six-channel schedules |
| Gross → liability → recovery → net | Table around 3828 | `accounting.csv`; figure 07; exact decomposition |
| Standardized structure/process/interaction | Table around 4024 | `standardized_decomposition.csv` |
| Arrivals, capacity, backlog and delays | Around 4172–4183 | `operations.csv`; queue mechanism |
| Operational interventions and combined-dose qualification | 4389–4415 | `operations_interventions.csv`; separate equal-dose factorial |
| Adaptive thresholds, sequential randomization, delayed release | 4667–4802 | Controller, sequential validation, evaluation note |

## Reconciliation decisions

1. **Transcript rollback.** The early all-at-once findings at approximately 1153–1175 were explicitly revoked around 1288–1308. The evidence map uses subsequent reintroduction from 1330 onward. The research narrative preserves David's inquiry sequence rather than treating prematurely supplied results as discoveries already made.
2. **Growth identity.** The count/severity product implies +66.88% loss amount in a common population. The mature CNP rate change implies +77.27%. Complete value denominators and cohort definitions are needed to reconcile them. The +3% volume statistic concerns transaction count and supplies no complete value bridge.
3. **Concentration.** Category and merchant contributions overlap; adding 57% and 21% would double count their intersection.
4. **Merchant measures.** Supplied 2.8×/1.6× values describe loss rates under a richer matched comparison. Generated comparisons measure fraud incidence standardized only on geography and CNP mix. Merchant B has no exact supplied adjusted multiplier; the reconstruction's value belongs to its generated population.
5. **Selection example.** The 1,000-per-arm teaching example and the approximately 80,000-eligible experiment are separate constructions. The completed-only versus ITT panels identify each explicitly.
6. **Model comparisons.** Masked-high and natural-low AUCs compare different populations. The supplied specialized model and the executable specialized model also have different recency designs. Empirical model results establish the performance of tested information/model combinations.
7. **Missingness.** Dependence of missingness on observed variables can support modeling its selection process. MNAR depends on remaining dependence on unobserved values after conditioning and is not established by predictive missingness alone.
8. **Accounting fractions.** The exact bridge uses liability 68/100 → 92/128 and recovery 28/68 → 33/92. Rounded 68%/72% and 41%/36% change the totals. Net loss grows 47.5% (40 → 59), separately from the dashboard's 46.875% rate increase (0.32 → 0.47).
9. **Two decompositions.** Supplied standardized 9.5/6.0/3.5 contributions require case-mix data beyond the aggregate waterfall. The executable aggregate bridge yields its own exact structure/process/interaction values. Shapley allocations distribute interactions among factors; adding a separate interaction to them would over-allocate the total.
10. **Operational interaction.** The supplied combined scenario uses a smaller capacity dose and beats each individual scenario. The narrative says it exceeds the sum of the two *direct* effects; those direct effects are not separately tabulated. The listed total net values $740K + $630K exceed $1.09M. Equal-dose complementarity therefore requires the separately implemented factorial, whose sign is reported as estimated.
11. **Queue endpoints.** Arrivals, processing capacity and backlog endpoints involve workload, evidence waiting, expiry and time-varying conditions. A constant arrival-minus-service extrapolation alone does not reconstruct all supplied endpoints. The simulator supplies an explicit stock identity and produces its own endpoints.
12. **Automation throughput.** Approximately 190–220 weekly cases is the later supplied scenario estimate; 100–150 appears as an earlier hypothetical. Simulator capacity is expressed in work units and automation changes case effort, readiness and completeness.
13. **Adaptive pilot economics.** $310K lower net fraud loss − $95K foregone margin − $40K authentication cost = $175K before other operating costs. A further $70K recovery spillover can be added only if the $310K excludes it. The project retains this as an unresolved decomposition and does not publish an inflated total.
14. **Uncertainty.** Supplied aggregate point estimates do not include sufficient transaction-level data to reconstruct experimental confidence intervals. Generated estimates, paired intervals and validation coverage are labeled accordingly.

## Evidence layers

- **Supplied scenario:** curated CSVs in `data/case_inputs/`, their original point estimates and the research trajectory.
- **Generated reconstruction:** seeded transaction, model, channel and queue mechanisms; all runnable estimates in `results/tables/`.
- **Identification argument:** assumptions and estimands in the experiment and dynamic-evaluation notes.

The generated studies demonstrate estimation and decision logic; their parameters are transparent assumptions rather than fits to the source aggregates.
