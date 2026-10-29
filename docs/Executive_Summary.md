# Executive Summary

## Decision question
Should a hypothetical personalized offer be scaled based on incremental purchasing behavior after accounting for discount cost and uncertainty?

## Context
Starbucks publicly announced a reimagined U.S. Rewards program launching March 10, 2026, with Green, Gold and Reserve levels and personalization as a stated program aim. This portfolio uses that public context to frame a hypothetical analytical exercise; it does not diagnose any actual internal Starbucks challenge.

## Hypothesis and method
A customer-level randomized $2 offer may increase transactions and net sales per assigned customer during July–September 2026. The project generates synthetic records, validates keys and joins, then uses intention-to-treat (ITT) to compare all assigned treatment and control customers, regardless of redemption. It reports Welch mean-difference tests and 95% confidence intervals.

Contribution proxy = incremental net sales/customer × assumed 58% contribution rate − incremental discount cost/customer. The 58% is a teaching assumption, not Starbucks financial data.

## Results
Run `python src/run_analysis.py`; the current run writes numeric results to `docs/generated_results.md` and `data/processed/campaign_results.json`. The results are synthetic and should be copied into any executive presentation only with the disclosure intact.

## Recommendations
1. Do not scale based on redemption rate alone.
2. Evaluate effect size, confidence intervals, incremental discount costs, contribution, customer guardrails and operational feasibility together.
3. Before a real test, pre-register primary metrics, perform power analysis, check sample-ratio mismatch and baseline balance, define returns/refunds, and agree with Finance on economics.
4. If results are uncertain, improve the test or gather more data instead of claiming success or failure.
