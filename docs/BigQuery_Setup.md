# BigQuery Setup — project `driiiportfolio`

## Free-tier and cost cautions
Google's current BigQuery Sandbox documentation lists 10 GiB lifetime storage, 1 TiB/month free query processing, automatic table expiry after 60 days, and feature restrictions including no DML. Google documents a 10 GiB/month storage and 1 TiB/month query-processing free usage tier for standard BigQuery, subject to current terms. Looker Studio's BigQuery connector documentation says a billing account is required and report queries may incur charges. Confirm terms before running; do not enable billing without understanding cost risk.

## Steps
1. Open BigQuery Studio and select project `driiiportfolio`. A project ID in code does not grant access; if inaccessible, create a project you control and replace every occurrence.
2. Use US location consistently.
3. Upload each `data/raw/*.csv` through Create table → Upload, CSV, header rows 1, autodetect schema. Name tables `raw_customers`, `raw_stores`, `raw_products`, `raw_transactions`, `raw_offers`, `raw_offer_assignments`, `raw_offer_redemptions`.
4. Review inferred types. `SAFE_CAST` is used in cleaning SQL.
5. Run `sql/01_load_and_clean.sql`, then `sql/02_analytics_views.sql`, then execute `sql/03_quality_checks.sql` query-by-query.
6. `00_schema.sql` is a schema reference; the cleaning file creates curated tables using CTAS.
7. Check table counts and metric totals against Python outputs.

## Sandbox fallback
Sandbox may not support all writes used by CTAS/CREATE OR REPLACE and tables may expire. If writes are blocked, use Python as the executable baseline and practice supported read-only SQL; do not enable billing merely to force a demo. A CSV/Google Sheets dashboard data source is a no-cost fallback where available.
