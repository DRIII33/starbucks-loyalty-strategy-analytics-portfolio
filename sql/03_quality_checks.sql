-- Each query should return zero rows unless stated otherwise.
SELECT transaction_id,COUNT(*) n FROM `driiiportfolio.loyalty_portfolio.fact_transactions`
GROUP BY transaction_id HAVING COUNT(*)>1;
SELECT t.customer_id FROM `driiiportfolio.loyalty_portfolio.fact_transactions` t
LEFT JOIN `driiiportfolio.loyalty_portfolio.dim_customers` c USING(customer_id) WHERE c.customer_id IS NULL;
SELECT * FROM `driiiportfolio.loyalty_portfolio.fact_transactions`
WHERE subtotal<0 OR discount_amount<0 OR net_sales<0 OR discount_amount>subtotal;
SELECT * FROM `driiiportfolio.loyalty_portfolio.fact_offer_assignments`
WHERE assigned_arm NOT IN ('TREATMENT','CONTROL');
-- Sample-ratio / baseline balance review: inspect outputs; this is diagnostic, not an automatic pass/fail.
WITH pre AS (
 SELECT a.customer_id,a.assigned_arm,c.membership_tier,c.region,c.app_active_flag,
 COUNTIF(t.transaction_status='COMPLETED') pre_tx
 FROM `driiiportfolio.loyalty_portfolio.fact_offer_assignments` a
 JOIN `driiiportfolio.loyalty_portfolio.dim_customers` c USING(customer_id)
 LEFT JOIN `driiiportfolio.loyalty_portfolio.fact_transactions` t
 ON t.customer_id=a.customer_id AND DATE(t.transaction_ts) BETWEEN DATE '2026-04-01' AND DATE '2026-06-30'
 WHERE a.offer_id='OFFER_Q3_PERSONALIZED' GROUP BY 1,2,3,4,5
)
SELECT assigned_arm,membership_tier,region,app_active_flag,COUNT(*) n,AVG(pre_tx) avg_pre_tx
FROM pre GROUP BY 1,2,3,4;
