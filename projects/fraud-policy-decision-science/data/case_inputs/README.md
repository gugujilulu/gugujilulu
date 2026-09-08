# Supplied case inputs

All CSVs here contain aggregate evidence from the author's simulated research interview. They are separate from generated transaction-level data and computed results. [Provenance and reconciliation](../../docs/evidence_provenance.md) links each evidence group to the reviewed transcript locations.

| File | Units and population |
|---|---|
| `portfolio_metrics.csv` | Portfolio/CNP rates, shares and count/severity indices; metric-specific denominators |
| `merchant_routing.csv` | Supplied Merchant A relative loss and PSP route measures |
| `3ds_itt.csv` | Percent and percentage-point differences; all eligible attempts |
| `device_heterogeneity.csv` | Percentage-point ITT by pre-assignment device availability |
| `observability.csv` | Percentage-point ITT and descriptive model metrics across observability groups |
| `displacement.csv` | Indexed loss with common 100-unit baseline per channel group |
| `saturation_evidence.csv` | Supplied 20/50/80% saturation results in four-week blocks |
| `accounting.csv` | Indexed monetary gross, liability, recovery and net amounts |
| `operations.csv` | Case arrivals, capacity, backlog, elapsed/active time and miss rates |
| `operations_interventions.csv` | USD incremental values, case backlog and miss percentages; unequal staffing doses |
| `standardized_decomposition.csv` | Supplied standardized contributions to the 19-unit net increase |
| `source_manifest.json` | SHA-256 and byte size of the reviewed attachments |

Blank values mean the supplied table has no earlier/recent counterpart. CSV percentage values are in percent units (2.72 means 2.72%), while generated rate outputs use proportions (0.0272 means 2.72%). `_pp` denotes percentage points. `gross − company liability` is allocated to other parties; `company liability − recovery = net`. The source scenario has no institution-identifying transaction records.
