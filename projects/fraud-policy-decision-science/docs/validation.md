# Validation record

Version 2 was checked locally with Python 3.12.13 and the direct dependency versions in `requirements-lock.txt`.

| Check | Result |
|---|---|
| Ten unit tests | Passed: assignment, known treatment effect, accounting, SQL maturity, queue/cash/terminal conservation, repeatability, delayed controller, capacity ablation, channel conservation and invalid inputs |
| Five notebook walkthroughs | Every code cell executed successfully using the shared package modules |
| Full pipeline | Regenerates transaction/cohort analyses, estimators, models, operational and sequential scenarios, figures, results note and explorer |
| Experiment calibration | 160 re-randomizations; bias, coverage and coverage Monte Carlo error in `docs/results.md` |
| Sequential calibration | 60 datasets per policy; reported coverage, bias and effective sample size |
| Static figures | Thirteen SVG/PNG pairs rendered and inspected; margins adjusted for long model and scenario labels |
| Interactive execution | All 135 parameter/rule combinations exercised in Chromium; zero page errors and valid numeric/SVG outputs |
| Responsive layout | Desktop and 390px mobile screenshots inspected; mobile charts resize their coordinate system; no horizontal overflow |
| Artifact integrity | SVG/PNG parsing, local Markdown links, SHA-256 manifest and explorer grid checked by `check_artifacts.py` |
| Formatting | Python source and tests formatted with Black |

The GitHub workflow repeats dependency installation, unit tests, the full pipeline and artifact integrity checks for project changes. Its run status is reported by GitHub after publication. Browser checks were performed locally with Chromium 133 via Playwright; the analysis workflow remains Python-only.

Calibration coverage describes repeated samples from the configured generators. Supplied case aggregates carry their original point estimates, while uncertainty in the new numerical studies is computed from the generated data.
