-- BigQuery Standard SQL. Use project ID supplied by user.
CREATE SCHEMA IF NOT EXISTS `driiiportfolio.loyalty_portfolio` OPTIONS(location="US");
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_customers` (
 customer_id STRING, signup_date DATE, region STRING, membership_tier STRING,
 digital_reload_flag BOOL, email_opt_in_flag BOOL, app_active_flag BOOL);
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_stores` (
 store_id STRING, region STRING, market_type STRING, opened_date DATE, is_company_operated BOOL);
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_products` (
 product_id STRING, category STRING, base_price NUMERIC, margin_rate_assumption NUMERIC);
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.fact_transactions` (
 transaction_id STRING, customer_id STRING, transaction_ts TIMESTAMP, store_id STRING, channel STRING,
 subtotal NUMERIC, discount_amount NUMERIC, tax_amount NUMERIC, net_sales NUMERIC, items_count INT64,
 offer_redeemed_flag BOOL, transaction_status STRING)
PARTITION BY DATE(transaction_ts) CLUSTER BY customer_id, store_id;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_offers` (
 offer_id STRING, campaign_name STRING, campaign_start_date DATE, campaign_end_date DATE,
 offer_type STRING, offer_value NUMERIC, assignment_unit STRING, randomized_flag BOOL);
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.fact_offer_assignments` (
 customer_id STRING, offer_id STRING, assigned_arm STRING, assignment_date DATE, eligible_flag BOOL);
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.fact_offer_redemptions` (
 redemption_id STRING, offer_id STRING, customer_id STRING, transaction_id STRING, transaction_ts TIMESTAMP,
 discount_amount NUMERIC, net_sales NUMERIC);
