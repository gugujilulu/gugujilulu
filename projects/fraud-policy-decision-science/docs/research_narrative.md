# Research narrative: how the question changed

The organizing idea is **form follows function**: the next analysis follows the unresolved decision. This case expands through two connected mechanisms. One explains authorization-time fraud; the other explains the company's loss after liability and recovery.

## 1. Establish the population before explaining the increase

The opening dashboard reports 0.32% → 0.47% fraud loss per transaction value over six weeks. David first asks what the rate measures, when losses enter the numerator and how CNP differs from other payment types. Transaction occurrence, fraud reporting and loss recognition each answer a different question.

Recognition-period losses reconstruct the dashboard. Transaction cohorts diagnose risk faced by a common settled population. Starting from only recognized fraud cases would omit transactions whose losses have yet to mature, so the cohort denominator includes the full settled transaction population. The supplied lag comparison is broadly stable; mature CNP cohorts still rise from 0.44% to 0.78%. That evidence shifts attention toward the mechanism generating fraud.

The executable SQL reproduces the distinction with an explicit extraction date and 42-day outcome window. Its future-label column exists to diagnose immature-cohort bias in the simulator; it is identified as unavailable prospectively for immature cohorts.

## 2. Separate incidence, severity and composition

CNP transaction count grows 3%, confirmed fraudulent transaction count grows 49%, and mean loss per confirmed fraudulent transaction grows 12%. The increase is therefore concentrated in fraudulent incidence, with a secondary severity contribution. Exact rate reconciliation still needs the same cohort definitions and value denominators: multiplying 1.49 × 1.12 gives a loss-amount factor of 1.6688, which alone does not reproduce the mature-cohort rate ratio of 0.78/0.44.

Category, merchant, geography and amount cuts localize the problem. The three highlighted categories account for 57% of incremental CNP loss; two merchants account for 21%. These are overlapping views. The $150–$600 concentration is an exploratory pattern; later evidence supports a smooth relationship rather than a special boundary at those cutoffs.

The early transcript includes a revoked batch of results. The evidence map uses the later, reintroduced findings and preserves the actual order in which the investigation resumed.

## 3. Keep the counterexample: Merchant B

Both merchants initially look risky. Adjusting the comparison for transaction characteristics largely explains Merchant B. Merchant A retains an approximately 1.6× loss-rate gap after a raw 2.8× comparison. This residual points to a mechanism requiring further investigation. Matching narrows the hypothesis space; unmeasured route selection and customer risk remain possible explanations.

David follows Merchant A's transactions through authentication status, server-to-server integration and PSP routing. Successfully authenticated transactions resemble peers more closely. The eligible-but-unused 3DS population has the larger discrepancy. Merchant A's S2S flow accounts for 22% of volume and 61% of incremental loss. On the changed PSP route, exemptions rise 19% → 44%, device missingness stays roughly 33% → 35%, and loss rises 1.9% → 4.6%. Other merchants and an alternative PSP provide additional comparisons.

This supports a route × observability × authentication hypothesis. A universal merchant block would also affect traffic where the comparison looks ordinary. A targeted experiment addresses the proposed mechanism directly.

## 4. Randomize the action and retain every assigned attempt

The case allocates approximately 80,000 eligible attempts over four weeks, with up to 20% assigned to forced 3DS. Pre-assignment risk and routing characteristics define strata. Assignment supplies the comparison; actual successful authentication is a downstream mediator.

The supplied trade-off is economically meaningful: gross loss per attempted value falls 0.87 percentage points, net loss falls 1.09 points and completion falls 2.9 points. The larger net reduction can arise through liability allocation as well as prevented fraud. Missing-device traffic benefits more strongly: net ITT −2.54 points compared with −0.41 for device-present traffic, with greater completion friction as well.

A completed-only analysis changes the population. Authentication affects abandonment, completion, fraud mix and severity; each deserves its own denominator. The project retains the small teaching counterexample separately so its 1,000-per-arm counts cannot be mistaken for the larger experimental sample.

## 5. Ask which information the decision system can use

The next question is whether a better model could replace some authentication friction. The investigation compares three mechanisms:

| Hypothesis | Diagnostic | Reading of the case |
|---|---|---|
| Available signals are poorly represented | Train challengers with exactly the same authorization-time inputs | Modest very-low-observability gains suggest limited improvement from model choice alone |
| Important information is absent | Add PSP authorization-time risk/routing signals | Improvement supports additional signal value |
| Weakly observed traffic is a different population | Mask rich records; compare natural weak-observability traffic; fit regime-specific models | Remaining differences suggest selection, interactions and changing population composition |

The supplied AUC ladder is 0.82/0.76/0.68/0.61 across observability groups. Same-information challengers reach 0.64–0.66 in the weakest group. Masked high-observability traffic reaches 0.70, while PSP information and a specialized recent model reach approximately 0.71 and 0.73. Those values come from related but distinct comparisons. They establish empirical limitations of tested representations, rather than a theoretical ceiling on all possible information.

The generated module makes the comparison executable with a shared temporal holdout, availability indicators, equal feature sets for the main challenger, calibration metrics and a separate masking diagnostic. Its synthetic risk process intentionally changes over time. Predicting the missingness indicator from observed covariates alone would not establish an MNAR mechanism; that depends on what remains unobserved after conditioning.

## 6. Expand from the treated channel to the portfolio

A week-three 53% drop in the treated channel looks large. Other channels have risen 39%, leaving the combined total 7% below baseline. The observational series also contains concurrent velocity-policy and time effects, so the movement motivates a new experiment rather than identifying the causal amount displaced.

The supplied next design randomizes saturation across six channels in four-week blocks. Low, medium and high saturation change total loss and conversion. Previous exposure can influence outcomes for one to three weeks, making a period's current action an incomplete description of treatment.

The executable six-channel mechanism experiment conserves displaced attack attempts across channels. It records current saturation, prior memory and incoming/outgoing exposure. Randomized current-saturation contrasts average over the design's history distribution. A steady-state policy value requires sustained exposure or a model/design that explicitly accounts for that history.

## 7. Follow gross fraud through liability and recovery

Gross fraud rises 100 → 128 indexed units. Company-liable loss rises 68 → 92; realized recovery rises 28 → 33; net company loss rises 40 → 59. Recovery grows in absolute terms while recovering a smaller fraction of the liable amount.

A case-mix decomposition separates composition and liability from recovery-process performance. Exact aggregate fractions yield one accounting bridge; the supplied standardized decomposition of 9.5/6.0/3.5 uses a richer underlying standardization that cannot be recovered from four aggregate totals. The project reports these as separate objects. It also computes Shapley allocations, which absorb interactions into factor contributions.

## 8. Locate the operating bottleneck

Weekly arrivals rise 1,000 → 1,690 while processing capacity rises 1,020 → 1,280. Open backlog rises 420 → 1,870. Queue delay expands much faster than active handling time, and evidence delay contributes additional elapsed time. Deadline misses climb as backlog crosses roughly 900–1,200 cases.

That is a flow-and-stock problem. Hiring increases service capacity; automation can improve evidence readiness, handling effort and package completeness. A case awaiting evidence occupies the case queue without necessarily occupying an analyst. The simulator preserves that distinction.

The supplied capacity, automation and combined scenarios give incremental net values of $740K, $630K and $1.09M. The combined scenario uses less staffing than the capacity-only scenario; comparing these totals does not identify an equal-dose interaction. The project therefore implements a full equal-dose factorial, reports the interaction's sign, and removes congestion in an ablation. Redundant benefits can produce a negative interaction even when the combined policy beats either component.

## 9. Evaluate the rule governing future states

Prevention reduces new liability and changes future recovery congestion. Value now belongs to a sequence of actions and states. The adaptive rule increases saturation above 1,200 open cases and relaxes below 800; delayed release requires seven continuously low-backlog days.

High-backlog periods reflect arrivals, staffing, case mix and past actions. Comparing them with low-backlog periods confounds the action with its trigger. Sequential randomization among eligible actions supplies conditional action effects; estimating the value of a complete rule additionally requires support for the action histories it generates, consistent outcomes and an explicit horizon.

The project provides two complementary demonstrations: a detailed case queue for mechanism and economic comparisons, and a compact randomized state process for validating trajectory-weighted policy-value estimation. The distinction makes the evidence reviewable. Default queue parameters keep the adaptive controller at high intensity throughout; that observed equivalence to fixed high intensity is part of the result. Policy complexity earns its place only when state changes make its actions and economics useful.
