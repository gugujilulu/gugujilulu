# Validation

The project checks both analytical identities and the ability to reproduce its outputs from an installed package. Python 3.12 is the tested runtime.

| Check | What it establishes |
|---|---|
| `ruff check .` and `ruff format --check .` | Imports, basic Python errors and consistent formatting |
| `python -m unittest discover -s tests -v` | Assignment, observed/potential-outcome consistency, known effects, accounting, cohort maturity, queue conservation, policy switching and mechanism ablations |
| `python check_notebooks.py` | Every code cell in the five walkthroughs executes through the installed package, with a fresh namespace per notebook |
| `python run_all.py` | Cohorts, experiments, models, queue policies, sequential validation, figures, results and explorer regenerate from configuration |
| `python check_artifacts.py` | Figure parsing, local document links, source/result fingerprints and the 135-scenario grid |

The [GitHub workflow](https://github.com/gugujilulu/gugujilulu/actions/workflows/fraud-case.yml) repeats these checks using `requirements-dev-lock.txt`. Notebook checking executes Python cells; it does not test the Jupyter interface. The self-contained explorer selects precomputed values, with no network data requests.

Estimator calibration is reported as a numerical study: 160 re-randomizations for ratio ITT and 60 datasets per sequential rule. Coverage and its Monte Carlo uncertainty appear in [computed results](results.md). Unit tests check identities and known effects; calibration estimates remain reported outcomes.
