# Randomized 3DS: estimands, selection and heterogeneity

## Units and outcomes

The supplied experiment contains approximately 80,000 eligible Merchant A S2S attempts over four weeks, assigned about 20% forced 3DS and 80% control. The generated reconstruction creates its own 80,000 potential-outcome records. An attempt's amount, device availability and risk stratum precede assignment. `assignment` denotes the offered policy; `completion` denotes an outcome.

Primary outcome: **net company loss / pre-treatment attempted value**. Secondary outcomes: gross loss / attempted value and completed payments / attempts. Successful 3DS, issuer declines, abandonment and loss severity are mechanism outcomes with stated denominators. Conditioning the primary analysis on completion changes the randomized population.

For stratum weights w_s = N_s/N, estimate each arm's ratio as:

$$\widehat R_z=\frac{\sum_s w_s\bar Y_{sz}}{\sum_s w_s\bar A_{sz}},\qquad \widehat\tau=\widehat R_1-\widehat R_0.$$

`ratio_itt` applies delta-method variance to the residual Y − R_z A within each stratum and arm. Independent-arm Neyman variance omits the unobservable finite-population covariance of potential effects and is conservative under the finite-population design. The ratio estimator has ordinary finite-sample ratio bias; randomization and larger samples give the relevant approximation. Completion uses a constant denominator of one.

Assignment is fixed within strata, so logged propensity equals the actual treated fraction after integer rounding. Both arms must have at least two observations per stratum for the variance calculation. Finite positive attempted amounts are required. Subgroup weights are re-normalized within the pre-treatment subgroup.

## Device availability as effect modification

The supplied net effects are −0.41 pp for device-present and −2.54 pp for device-missing attempts. The executable analysis estimates each subgroup and explicitly computes the difference of treatment effects. For these disjoint pre-treatment strata, the variance is the sum of the subgroup variances. The analysis labels this contrast as pre-specified in the generated demonstration. Broadly searching many feature cuts would instead require a discovery/confirmation split or multiplicity-aware inference.

A stronger missing-device effect can reflect prevented fraud, liability allocation and treatment-induced selection. It supports targeting research; optimal targeting also requires the expected margin and authentication costs for those same attempts.

## The completion example

The separate teaching example has 1,000 attempts per arm, 918 versus 889 completions, and 20 versus 21 completed fraudulent transactions. Completed-only fraud incidence is 2.18% versus 2.36%. That small example illustrates a changed selected population; its counts do not supply the actual larger experiment's loss totals.

The larger supplied case separately reports completed-transaction fraud frequency of 235 versus 249 per 10,000, average gross fraudulent loss of $412 versus $276 and average net fraudulent loss of $367 versus $207. Different amount distributions and denominators connect incidence, severity and loss rates. Aggregate point estimates alone do not supply randomization confidence intervals.

## Validation with potential outcomes

The generator stores `net0/net1`, `gross0/gross1` and `completion0/completion1` for finite-population validation only. The estimator receives observed columns. Across 160 fresh stratified assignments, validation compares the estimate with the exact finite-population net contrast and reports bias, interval coverage and Monte Carlo standard error.

The outcome model fixes compliance and liability mechanisms for transparency. A live analysis would additionally align fraud maturity by assignment cohort, retain propensity and eligibility logs, specify repeated-user clustering if applicable, and estimate long-horizon effects under channel interference separately from this local ITT.
