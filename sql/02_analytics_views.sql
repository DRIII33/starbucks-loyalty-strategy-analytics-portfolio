CREATE OR REPLACE VIEW `driiiportfolio.loyalty_portfolio.vw_customer_monthly` AS
WITH tx AS (
 SELECT customer_id,DATE_TRUNC(DATE(transaction_ts),MONTH) month_start,
 COUNTIF(transaction_status='COMPLETED') completed_transactions,
 SUM(IF(transaction_status='COMPLETED',net_sales,0)) net_sales,
 SUM(IF(transaction_status='COMPLETED',discount_amount,0)) discounts,
 SUM(IF(transaction_status='COMPLETED',items_count,0)) items
 FROM `driiiportfolio.loyalty_portfolio.fact_transactions` GROUP BY 1,2
)
SELECT c.customer_id,c.region,c.membership_tier,c.signup_date,tx.month_start,
 COALESCE(tx.completed_transactions,0) completed_transactions,COALESCE(tx.net_sales,0) net_sales,
 COALESCE(tx.discounts,0) discounts,COALESCE(tx.items,0) items
FROM `driiiportfolio.loyalty_portfolio.dim_customers` c LEFT JOIN tx USING(customer_id);

CREATE OR REPLACE VIEW `driiiportfolio.loyalty_portfolio.vw_customer_rfm` AS
WITH t AS (
 SELECT customer_id,DATE_DIFF(DATE '2026-09-30',MAX(DATE(transaction_ts)),DAY) recency_days,
 COUNTIF(transaction_status='COMPLETED') frequency_transactions,
 SUM(IF(transaction_status='COMPLETED',net_sales,0)) monetary_net_sales,
 MAX(DATE(transaction_ts)) last_transaction_date
 FROM `driiiportfolio.loyalty_portfolio.fact_transactions` GROUP BY customer_id
)
SELECT c.customer_id,c.region,c.membership_tier,
 COALESCE(t.recency_days,DATE_DIFF(DATE '2026-09-30',c.signup_date,DAY)) recency_days,
 COALESCE(t.frequency_transactions,0) frequency_transactions,
 COALESCE(t.monetary_net_sales,0) monetary_net_sales,t.last_transaction_date
FROM `driiiportfolio.loyalty_portfolio.dim_customers` c LEFT JOIN t USING(customer_id);

CREATE OR REPLACE VIEW `driiiportfolio.loyalty_portfolio.vw_campaign_itt` AS
WITH customer_outcomes AS (
 SELECT a.customer_id,a.assigned_arm,
 COUNTIF(t.transaction_status='COMPLETED') post_transactions,
 SUM(IF(t.transaction_status='COMPLETED',t.net_sales,0)) post_net_sales,
 SUM(IF(t.transaction_status='COMPLETED',t.discount_amount,0)) post_discount_cost
 FROM `driiiportfolio.loyalty_portfolio.fact_offer_assignments` a
 LEFT JOIN `driiiportfolio.loyalty_portfolio.fact_transactions` t
 ON t.customer_id=a.customer_id AND DATE(t.transaction_ts) BETWEEN DATE '2026-07-01' AND DATE '2026-09-30'
 WHERE a.offer_id='OFFER_Q3_PERSONALIZED'
 GROUP BY 1,2
)
SELECT assigned_arm,COUNT(*) assigned_customers,AVG(post_transactions) avg_transactions_per_customer,
 AVG(post_net_sales) avg_net_sales_per_customer,AVG(post_discount_cost) avg_discount_cost_per_customer,
 AVG(post_net_sales)*0.58-AVG(post_discount_cost) contribution_proxy_per_customer
FROM customer_outcomes GROUP BY assigned_arm;

CREATE OR REPLACE VIEW `driiiportfolio.loyalty_portfolio.vw_dashboard_kpis` AS
SELECT month_start,SUM(completed_transactions) transactions,SUM(net_sales) net_sales,
 COUNTIF(completed_transactions>0) active_customers,
 SAFE_DIVIDE(SUM(net_sales),SUM(completed_transactions)) avg_order_value
FROM `driiiportfolio.loyalty_portfolio.vw_customer_monthly` GROUP BY month_start;
