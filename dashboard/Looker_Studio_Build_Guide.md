# Looker Studio Build Guide

1. Create a report and select BigQuery connector.
2. Select `driiiportfolio.loyalty_portfolio.vw_dashboard_kpis`.
3. Add scorecards for transactions, net sales, active customers and AOV, then a monthly time series.
4. Add `vw_customer_monthly` as a second source for engagement and region/tier views.
5. Use `vw_campaign_itt` for treatment/control summary. Add confidence intervals and p-values from `data/processed/campaign_results.json` as a separate CSV source or text annotation; do not label means alone as causal proof.
6. Put “Synthetic portfolio data — not Starbucks actual results” prominently on each page.
7. Reconcile every displayed number to SQL/Python before sharing.

BigQuery-connected Looker Studio reports may require billing and can incur charges. If that is unsuitable, upload `dashboard/dashboard_kpis.csv` or use Google Sheets as a source, and label it as a static extract rather than a live connection.
