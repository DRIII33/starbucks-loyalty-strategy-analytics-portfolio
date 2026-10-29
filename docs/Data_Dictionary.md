# Data Dictionary

All records in `data/raw/` are synthetic.

| File | Grain / key | Main fields |
|---|---|---|
| customers.csv | one/customer; customer_id | signup date, region, tier, app/reload/opt-in flags |
| stores.csv | one/store; store_id | region, market type, open date, operating type |
| products.csv | one/product; product_id | category, base price, assumed margin rate |
| transactions.csv | one/transaction; transaction_id | customer, timestamp, store, channel, subtotal, discount, tax, net sales, item count, redemption flag, status |
| offers.csv | one/offer; offer_id | campaign dates/type/value, assignment unit, randomized flag |
| offer_assignments.csv | one customer-offer; composite key | assigned arm, date, eligibility |
| offer_redemptions.csv | one redemption; redemption_id | offer/customer/transaction, timestamp, discount and net sales |

## Metric contract
- Completed transaction: status `COMPLETED`; returned rows are retained but excluded from primary outcome.
- Net sales: subtotal less discount before tax in this synthetic model.
- Active customer: at least one completed transaction in period.
- AOV: completed net sales / completed transaction count.
- Recency: 2026-09-30 minus latest completed purchase date; customers without purchases use signup date and should be flagged separately.
- ITT: compare all customers by assigned arm, regardless of redemption.
- Incremental contribution proxy: incremental net sales × assumed 58% contribution rate − incremental discount cost. Not actual profit or Starbucks margin.
