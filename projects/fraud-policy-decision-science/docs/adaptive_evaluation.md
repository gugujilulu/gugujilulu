# Dynamic policy evaluation

## Economic object

For horizon H, the queue simulator records:

$$V_H=\sum_{t=1}^H[\text{legitimate margin}_t-\text{new company liability}_t+\text{realized recovery}_t-\text{authentication cost}_t-\text{operating cost}_t].$$

Gross fraud is reported as a mechanism outcome. Liability is charged once when a new case arrives; realized recovery is credited once when it resolves. Initial backlog liabilities are sunk at the comparison start, while their subsequent recoveries enter every policy's ledger. Remaining cases at the horizon retain full liability and receive zero assumed future recovery. Policy differences therefore have a conservative finite-horizon terminal convention, rather than an extrapolated steady-state claim.

The $0.65 margin, $0.09 authentication cost, $380 case scale and operating-cost function are **generated scenario assumptions**. The lognormal's arithmetic mean differs from its configured scale. Base weekly capacity is 1,280 service-work units; a slow case uses 1.25 units and an automated case 0.65. Case counts and capacity units coincide only for unit-effort cases.

## Case-queue mechanics

Each case has an arrival date, evidence-ready date, filing deadline, handling effort, liability, package-completeness indicator and fixed recovery draw. The daily schedule processes ready cases by earliest deadline and case ID until service capacity is exhausted. Cases awaiting evidence remain in the backlog; they consume service effort only when processed. Cases expire on the day after their deadline. Automation accelerates evidence, reduces effort and improves completeness for a selected fraction of slow-evidence cases.

A common daily random stream provides potential arrivals, amounts and case attributes under each policy. Stronger authentication suppresses some arrivals and lowers retained liability share. An exponentially updating policy memory weakens durable suppression under higher displacement strength. This is a portfolio-level reduced-form adaptation mechanism. The separate six-channel module explicitly redistributes attack attempts and illustrates interference; it is not numerically calibrated to the queue model.

Queue conservation is Q_end = Q_start + arrivals − resolutions, where resolutions include deadline expiry. Tests also reconcile case-level and daily liability/recovery, service capacity, unique case IDs and terminal outstanding counts.

## Policies and comparisons

The policy grid compares fixed 20%, 50% and 80% saturation, immediate adaptive release, and seven-day delayed release across 12 paired seeds. Four scenarios vary arrivals, displacement or legitimate-margin cost. Adaptive intensity rises to 80% above 1,200 cases and falls to 20% below 800; between thresholds it retains its state. The delayed rule resets its release timer whenever backlog returns to 800 or above.

Each policy is compared with fixed 50% within the same seed and scenario. Confidence intervals use the sample standard deviation of paired value differences with a Student-t critical value and 11 degrees of freedom. These intervals describe Monte Carlo uncertainty conditional on the specified generator; parameter uncertainty is examined through scenarios, and structural uncertainty remains a modeling limitation.

The explorer provides 135 combinations of evidence delay, capacity, displacement and policy. Those curves use one paired seed and the identical case engine; the multi-seed table supplies separate uncertainty information.

## Equal-dose operational interaction

The factorial evaluates four cells: baseline, +450 weekly service units, 70% slow-evidence automation, and both at the same doses. The interaction is:

$$I=V_{11}-V_{10}-V_{01}+V_{00}.$$

Positive values represent complementarity in this outcome; negative values represent overlapping or substitutable benefits. The combined policy can outperform either component with a negative interaction. The supplied narrative's operational scenarios use different staffing doses, so the code estimates this separate matched comparison. Removing the capacity constraint supplies a mechanism ablation: adding capacity then changes cost without changing recoveries, as verified by a test.

## Action effects versus complete-policy value

Randomizing escalation or relaxation conditional on a measured decision history identifies the local effect of that action over its defined follow-up. Full-policy value also depends on the distribution of states reached under all preceding actions. Randomizing only near a threshold provides support for rules whose action histories remain within that design; it does not automatically support every candidate threshold.

Required design elements are pre-action state/history logs, action propensities, delayed outcomes, exposure to other channels, policy version, and enough follow-up for recovery and fraud adaptation. If channels interfere, randomization and analysis must use a defensible joint exposure map or larger portfolio clusters. Carryover motivates history-aware estimands or sustained assignments.

The `sequential.py` demonstration uses a separate four-step state process. Behavior randomizes low/high with probability 0.5 at every step. Candidate rules are fixed low, fixed high and a threshold rule. For a deterministic target rule π, the trajectory Horvitz–Thompson estimator is:

$$\widehat V(\pi)=\frac1n\sum_i\left[\prod_{t=1}^{4}\frac{\mathbf1\{A_{it}=\pi(H_{it})\}}{0.5}\right]\sum_{t=1}^{4}R_{it}.$$

Every compatible trajectory receives weight 16 and incompatible ones weight zero. The effective sample size equals the number of compatible trajectories in this constant-weight setting. The implementation reports empirical-standard-error intervals and compares 60 repeated behavior datasets against an independent 100,000-trajectory on-policy Monte Carlo reference. That reference approximates the known-DGP expectation; it is not an analytic exact value. Four steps keep the importance weights manageable; longer horizons need stronger sample sizes or variance-reducing estimators.

This demonstration validates the sequential weighting logic within its randomized state world. Queue policy values are generated by running each full rule forward in the operational simulator. A fitted off-policy evaluation of the full queue from real logs is a future empirical step.

## Decision memo

The case supports a targeted authentication experiment, explicit conversion economics and a joint operations evaluation. Preserve Merchant A's route-level eligibility, collect missing authorization-time signal where it can change action, and assess portfolio loss over sustained exposure. Compare capacity and automation at matched doses. Candidate adaptive rules should earn their value against simpler fixed policies under observed operating states, with mature net-loss outcomes and sufficient history support.
