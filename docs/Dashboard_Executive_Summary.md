# Dashboard Executive Summary

## Dashboard pages
1. **Executive pulse:** completed transactions, net sales, active customers, AOV, monthly trends.
2. **Member engagement:** active members, transactions per active member, sales per active member, recency/RFM, tier and region mix.
3. **Campaign incrementality:** treatment/control counts, average sales and transactions per assigned customer, effect estimates, confidence intervals, p-values, discount cost and contribution proxy.
4. **Measurement health:** duplicates, null keys, orphan records, status validity, assignment ratio and baseline balance.

## Design controls
- Show date window, denominator, metric definition and exclusions beside every KPI.
- Separate descriptive program metrics from causal estimates.
- Add persistent text: “Synthetic portfolio data — not Starbucks actual results.”
- Do not show p-values without effect size and confidence interval.
- Reconcile dashboard totals to SQL and Python before sharing.

## Executive narration
“Redemption is a behavior metric, not proof of incrementality. The decision is whether randomized assignment changes customer behavior and creates enough incremental contribution to justify the offer cost.”
