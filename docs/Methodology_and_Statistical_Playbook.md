# Methodology and Statistical Playbook

## 1. Decision framing
**Decision:** whether to expand a hypothetical personalized $2 offer.  
**Primary estimand:** intention-to-treat (ITT) difference in mean post-period net sales per assigned eligible customer, treatment minus control.  
**Secondary outcome:** ITT difference in completed transactions per assigned customer.  
**Economic guardrail:** incremental contribution proxy after incremental discount cost.  
**Customer guardrails:** opt-outs/complaints, return rates, and tier-level fairness would be required in real data; these are not fully simulated here.

The supplied job description asks for customer insight, performance and lifetime-value methodologies, KPI design, analytical tools, inquiry-driven frameworks, executive communication and cross-functional leadership. The project demonstrates each through an explicit decision question, repeatable pipeline, KPI contracts, causal design, dashboard and executive narrative.

## 2. Why ITT
Analyzing only customers who redeemed an offer conditions on post-assignment behavior. Redeemers are self-selected and likely differ from non-redeemers. ITT preserves the randomized assignment and estimates the effect of being assigned/offered the intervention under the implementation conditions simulated here. It does not estimate the treatment-on-the-treated effect.

## 3. Core analysis methods
| Method | Why use it | What it answers | Implementation |
|---|---|---|---|
| Descriptive KPI trends | Baseline operational context | What changed over time in sales, transactions, active customers, AOV? | SQL `vw_dashboard_kpis`; Python `monthly_kpis`; Looker Studio time series |
| RFM features | Transparent behavioral segmentation | Which customers are recent, frequent and high-spend? | `build_features`; SQL `vw_customer_rfm`; Excel `Customer_KPIs` |
| Welch two-sample t-test | Compares means without equal-variance assumption | Is observed ITT mean difference inconsistent with zero under test assumptions? | `scipy.stats.ttest_ind(..., equal_var=False)` |
| Welch confidence interval | Communicates uncertainty and plausible effect range | How precise is the mean difference? | `welch_ci` function |
| Contribution proxy | Connects behavior to financial decision | Does incremental sales cover incremental discount cost under an assumed rate? | Python result JSON; Excel formula catalog |
| Baseline balance | Checks randomization diagnostics | Are treatment/control groups observably imbalanced before the campaign? | `sql/03_quality_checks.sql`; extend in Python if desired |
| Sample-ratio mismatch | Checks assignment implementation | Does observed assignment split differ from expected ratio beyond chance? | Add a formal binomial/chi-square test before real experimentation |
| Power / minimum detectable effect | Avoids underpowered tests | Can the test detect a commercially meaningful effect? | Before launch, use historical variance, alpha, power and expected allocation |
| Difference-in-differences | Useful for nonrandomized rollout when assumptions are credible | Did treated units change more than a comparison group? | Not the primary method here; requires parallel-trends evidence |
| Survival / time-to-churn | Handles time until inactivity/churn | Does treatment delay churn? | Extension requiring customer event/censoring definition |
| Uplift modeling | Targets heterogeneous treatment response | Which segments benefit incrementally? | Advanced extension; needs sufficiently powered randomized data and out-of-sample validation |

## 4. Statistical interpretation rules
- A p-value is not the probability the hypothesis is true and does not measure business importance.
- A confidence interval crossing zero means the data are compatible with no effect at the chosen confidence level; it does not prove equivalence.
- Statistical significance is not sufficient for rollout. Review effect size, economics, implementation cost and customer guardrails.
- Do not optimize on many segments without controlling multiplicity or labeling exploratory analyses.
- Do not claim causality from pre/post changes alone; seasonality, product mix, prices, store execution and broader marketing can confound trends.
- A 58% contribution rate is a declared placeholder assumption. Replace with approved Finance economics before real decision-making.
- In this generator, the randomized offer primarily changes redemption probability, not baseline transaction propensity. Therefore a null/negative sales ITT result is possible and is a useful teaching case: more redemptions do not guarantee incrementality.

## 5. Edge cases to handle before production
1. Duplicate transaction IDs: deduplicate using a documented source-of-truth rule; never silently remove without audit.
2. Returns/refunds: define whether sales are net of refunds and how return timestamps map to original purchases.
3. Late-arriving transactions: establish event time vs ingestion time and restatement policy.
4. Missing customer ID: distinguish non-member transactions from failed joins; do not automatically drop revenue.
5. Multiple offers on one transaction: allocate discount cost once and document attribution.
6. Exposure mismatch: log assigned, delivered, viewed, eligible, redeemed and expired states separately.
7. Cross-device or account sharing: document identity resolution and household spillover.
8. Sample-ratio mismatch: pause causal interpretation until assignment pipeline is investigated.
9. Overlapping campaigns: predefine exclusion/stratification or factorial design.
10. Seasonality: compare like-for-like periods and include calendar controls where appropriate.
11. Tier migration: freeze baseline tier or model time-varying tier to avoid post-treatment adjustment bias.
12. Privacy/consent: restrict use to approved purposes and honor communication preferences.
13. Small subgroups: suppress unstable estimates and protect privacy.
14. Cost accounting: include discounts, reward liability/redemption costs, cannibalization and variable cost where data are available.
15. Dashboard drift: pin metric definitions and automated reconciliation checks.

## 6. Recommended follow-on models
- Pre-period adjusted OLS: `post_sales ~ treatment + pre_sales + baseline_tier + region`, with robust standard errors; use as precision improvement, not a substitute for correct randomization.
- Count outcome model: Poisson or negative-binomial regression if the transaction-count distribution and diagnostics support it.
- Retention: survival model with censoring defined by last observed activity and observation window.
- LTV: cohort-based discounted contribution forecast; distinguish realized historical value from forecast and validate forecast calibration.
- Segmentation: quantile-based RFM or clustering only after defining a decision use and validating stability.
