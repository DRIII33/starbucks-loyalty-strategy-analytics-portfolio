-- First upload CSVs to raw_* tables using BigQuery UI. Run this file next.
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_customers` AS
SELECT * EXCEPT(rn) FROM (
 SELECT CAST(customer_id AS STRING) customer_id, SAFE_CAST(signup_date AS DATE) signup_date,
 NULLIF(TRIM(region),'') region,
 IF(membership_tier IN ('Green','Gold','Reserve'),membership_tier,'Unknown') membership_tier,
 SAFE_CAST(digital_reload_flag AS BOOL) digital_reload_flag,
 SAFE_CAST(email_opt_in_flag AS BOOL) email_opt_in_flag,
 SAFE_CAST(app_active_flag AS BOOL) app_active_flag,
 ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY signup_date DESC) rn
 FROM `driiiportfolio.loyalty_portfolio.raw_customers` WHERE customer_id IS NOT NULL
) WHERE rn=1;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_stores` AS
SELECT * EXCEPT(rn) FROM (
 SELECT CAST(store_id AS STRING) store_id, region, market_type, SAFE_CAST(opened_date AS DATE) opened_date,
 SAFE_CAST(is_company_operated AS BOOL) is_company_operated,
 ROW_NUMBER() OVER(PARTITION BY store_id ORDER BY opened_date DESC) rn
 FROM `driiiportfolio.loyalty_portfolio.raw_stores` WHERE store_id IS NOT NULL
) WHERE rn=1;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_products` AS
SELECT * EXCEPT(rn) FROM (
 SELECT CAST(product_id AS STRING) product_id, category, SAFE_CAST(base_price AS NUMERIC) base_price,
 SAFE_CAST(margin_rate_assumption AS NUMERIC) margin_rate_assumption,
 ROW_NUMBER() OVER(PARTITION BY product_id ORDER BY base_price DESC) rn
 FROM `driiiportfolio.loyalty_portfolio.raw_products` WHERE product_id IS NOT NULL
) WHERE rn=1;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.fact_transactions` AS
SELECT * EXCEPT(rn) FROM (
 SELECT CAST(transaction_id AS STRING) transaction_id, CAST(customer_id AS STRING) customer_id,
 SAFE_CAST(transaction_ts AS TIMESTAMP) transaction_ts, CAST(store_id AS STRING) store_id, channel,
 SAFE_CAST(subtotal AS NUMERIC) subtotal, SAFE_CAST(discount_amount AS NUMERIC) discount_amount,
 SAFE_CAST(tax_amount AS NUMERIC) tax_amount, SAFE_CAST(net_sales AS NUMERIC) net_sales,
 SAFE_CAST(items_count AS INT64) items_count, SAFE_CAST(offer_redeemed_flag AS BOOL) offer_redeemed_flag,
 UPPER(TRIM(transaction_status)) transaction_status,
 ROW_NUMBER() OVER(PARTITION BY transaction_id ORDER BY transaction_ts DESC) rn
 FROM `driiiportfolio.loyalty_portfolio.raw_transactions`
 WHERE transaction_id IS NOT NULL AND SAFE_CAST(transaction_ts AS TIMESTAMP) IS NOT NULL
 AND SAFE_CAST(net_sales AS NUMERIC)>=0
) WHERE rn=1;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.dim_offers` AS
SELECT * EXCEPT(rn) FROM (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY offer_id ORDER BY campaign_start_date DESC) rn FROM (
 SELECT CAST(offer_id AS STRING) offer_id,campaign_name,SAFE_CAST(campaign_start_date AS DATE) campaign_start_date,
 SAFE_CAST(campaign_end_date AS DATE) campaign_end_date,offer_type,SAFE_CAST(offer_value AS NUMERIC) offer_value,
 assignment_unit,SAFE_CAST(randomized_flag AS BOOL) randomized_flag
 FROM `driiiportfolio.loyalty_portfolio.raw_offers` WHERE offer_id IS NOT NULL
 )) WHERE rn=1;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.fact_offer_assignments` AS
SELECT * EXCEPT(rn) FROM (
 SELECT CAST(customer_id AS STRING) customer_id,CAST(offer_id AS STRING) offer_id,UPPER(TRIM(assigned_arm)) assigned_arm,
 SAFE_CAST(assignment_date AS DATE) assignment_date,SAFE_CAST(eligible_flag AS BOOL) eligible_flag,
 ROW_NUMBER() OVER(PARTITION BY customer_id,offer_id ORDER BY assignment_date DESC) rn
 FROM `driiiportfolio.loyalty_portfolio.raw_offer_assignments`
 WHERE customer_id IS NOT NULL AND offer_id IS NOT NULL
) WHERE rn=1;
CREATE OR REPLACE TABLE `driiiportfolio.loyalty_portfolio.fact_offer_redemptions` AS
SELECT * EXCEPT(rn) FROM (
 SELECT CAST(redemption_id AS STRING) redemption_id,CAST(offer_id AS STRING) offer_id,
 CAST(customer_id AS STRING) customer_id,CAST(transaction_id AS STRING) transaction_id,
 SAFE_CAST(transaction_ts AS TIMESTAMP) transaction_ts,SAFE_CAST(discount_amount AS NUMERIC) discount_amount,
 SAFE_CAST(net_sales AS NUMERIC) net_sales,
 ROW_NUMBER() OVER(PARTITION BY redemption_id ORDER BY transaction_ts DESC) rn
 FROM `driiiportfolio.loyalty_portfolio.raw_offer_redemptions` WHERE redemption_id IS NOT NULL
) WHERE rn=1;
