"""
Deterministic synthetic dataset generator for the loyalty strategy portfolio.
Run from repository root: python src/generate_synthetic_data.py
No network access or real Starbucks data are used.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 260079240
rng = np.random.default_rng(SEED)
N_CUSTOMERS, N_STORES, N_PRODUCTS = 2500, 45, 18
START, END = pd.Timestamp("2025-04-01"), pd.Timestamp("2026-09-30")
regions = np.array(["West", "South", "Midwest", "Northeast"])
customer_ids = np.array([f"C{i:06d}" for i in range(1, N_CUSTOMERS + 1)])
store_ids = np.array([f"S{i:04d}" for i in range(1, N_STORES + 1)])
product_ids = np.array([f"P{i:03d}" for i in range(1, N_PRODUCTS + 1)])

signup = pd.to_datetime(
    rng.integers(pd.Timestamp("2023-01-01").value // 10**9,
                 pd.Timestamp("2026-09-01").value // 10**9,
                 size=N_CUSTOMERS), unit="s").normalize()
latent = rng.normal(size=N_CUSTOMERS)
tiers = np.where(latent > 1.05, "Reserve", np.where(latent > -.25, "Gold", "Green"))
arms = rng.choice(["Treatment", "Control"], N_CUSTOMERS)
customers = pd.DataFrame({
    "customer_id": customer_ids, "signup_date": signup.strftime("%Y-%m-%d"),
    "region": rng.choice(regions, N_CUSTOMERS, p=[.30,.30,.22,.18]),
    "membership_tier": tiers,
    "digital_reload_flag": rng.choice([True,False], N_CUSTOMERS, p=[.38,.62]),
    "email_opt_in_flag": rng.choice([True,False], N_CUSTOMERS, p=[.68,.32]),
    "app_active_flag": rng.choice([True,False], N_CUSTOMERS, p=[.73,.27])
})
customers.to_csv(OUT/"customers.csv", index=False)

stores = pd.DataFrame({
    "store_id": store_ids, "region": rng.choice(regions,N_STORES),
    "market_type": rng.choice(["Urban","Suburban","Rural"],N_STORES,p=[.4,.45,.15]),
    "opened_date": rng.choice(pd.date_range("2010-01-01","2024-01-01",freq="D"),N_STORES).astype(str),
    "is_company_operated": rng.choice([True,False],N_STORES,p=[.82,.18])
})
stores.to_csv(OUT/"stores.csv",index=False)
prices = np.round(rng.uniform(2.25,11.5,N_PRODUCTS),2)
products = pd.DataFrame({
    "product_id":product_ids,
    "category":rng.choice(["Beverage","Food","Merchandise"],N_PRODUCTS,p=[.62,.34,.04]),
    "base_price":prices,"margin_rate_assumption":np.round(rng.uniform(.48,.72,N_PRODUCTS),3)
})
products.to_csv(OUT/"products.csv",index=False)
offers = pd.DataFrame([
    {"offer_id":"OFFER_Q3_PERSONALIZED","campaign_name":"Q3 Personalized $2 Offer",
     "campaign_start_date":"2026-07-01","campaign_end_date":"2026-09-30",
     "offer_type":"Personalized Discount","offer_value":2.0,"assignment_unit":"Customer","randomized_flag":True},
    {"offer_id":"OFFER_WINBACK","campaign_name":"Illustrative Win-back Offer",
     "campaign_start_date":"2026-07-01","campaign_end_date":"2026-09-30",
     "offer_type":"Win-back","offer_value":2.0,"assignment_unit":"Customer","randomized_flag":True}
])
offers.to_csv(OUT/"offers.csv",index=False)
assignments = pd.DataFrame({"customer_id":customer_ids,"assigned_arm":arms,
    "assignment_date":"2026-07-01","eligible_flag":True,"offer_id":"OFFER_Q3_PERSONALIZED"})
assignments.to_csv(OUT/"offer_assignments.csv",index=False)

# Draw counts and transaction details vectorially for reproducibility and speed.
eligible_days = np.maximum(1,(END-signup).days+1)
activity_rate = np.clip(.18+.12*(latent+.2),.03,.55) * np.where(customers.app_active_flag.to_numpy(),1.18,.70)
counts = rng.poisson(activity_rate*eligible_days*.52)
customer_index = np.repeat(np.arange(N_CUSTOMERS),counts)
m = len(customer_index)
signup_seconds = signup.values.astype("datetime64[s]").astype("int64")
end_seconds = END.value // 10**9
sample_seconds = signup_seconds[customer_index] + (
    rng.random(m)*(end_seconds-signup_seconds[customer_index])).astype("int64")
transaction_ts = pd.to_datetime(sample_seconds,unit="s")
store_choice = rng.choice(store_ids,m)
channel = rng.choice(["InStore","MobileOrder","DriveThru"],m,p=[.43,.38,.19])
items = rng.choice([1,2,3,4],m,p=[.43,.35,.17,.05])
product_index = rng.integers(0,N_PRODUCTS,size=(m,4))
subtotal = np.array([prices[product_index[i,:items[i]]].sum() for i in range(m)])
in_campaign = transaction_ts >= pd.Timestamp("2026-07-01")
redeem_probability = np.where((arms[customer_index]=="Treatment") & in_campaign,.23,
                              np.where(in_campaign,.025,0))
redeemed = rng.random(m) < redeem_probability
discount = np.where(redeemed,np.minimum(2.0,subtotal),0.0)
status = rng.choice(["COMPLETED","RETURNED"],m,p=[.99,.01])
transactions = pd.DataFrame({
    "transaction_id":[f"T{i:09d}" for i in range(1,m+1)],
    "customer_id":customer_ids[customer_index],
    "transaction_ts":transaction_ts.strftime("%Y-%m-%d %H:%M:%S"),
    "store_id":store_choice,"channel":channel,"subtotal":np.round(subtotal,2),
    "discount_amount":np.round(discount,2),
    "tax_amount":np.round((subtotal-discount)*.0825,2),
    "net_sales":np.round(subtotal-discount,2),"items_count":items,
    "offer_redeemed_flag":redeemed,"transaction_status":status
})
transactions.to_csv(OUT/"transactions.csv",index=False)
red = transactions[transactions.offer_redeemed_flag].copy()
redemptions = pd.DataFrame({
    "redemption_id":[f"R{i:08d}" for i in range(1,len(red)+1)],
    "offer_id":"OFFER_Q3_PERSONALIZED","customer_id":red.customer_id,
    "transaction_id":red.transaction_id,"transaction_ts":red.transaction_ts,
    "discount_amount":red.discount_amount,"net_sales":red.net_sales
})
redemptions.to_csv(OUT/"offer_redemptions.csv",index=False)
print(f"Generated {N_CUSTOMERS:,} customers, {N_STORES} stores, {N_PRODUCTS} products, "
      f"{len(transactions):,} transactions, {len(assignments):,} assignments and "
      f"{len(redemptions):,} redemption records in {OUT}")
