"""Full analysis pipeline for synthetic loyalty portfolio. Run: python src/run_analysis.py"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/raw"; OUT=ROOT/"data/processed"; OUT.mkdir(parents=True,exist_ok=True)
def load_data():
    files=["customers","stores","products","transactions","offers","offer_assignments","offer_redemptions"]
    return {f:pd.read_csv(RAW/f"{f}.csv") for f in files}
def clean(d):
    c=d["customers"].copy(); t=d["transactions"].copy(); a=d["offer_assignments"].copy()
    c["signup_date"]=pd.to_datetime(c.signup_date,errors="coerce")
    t["transaction_ts"]=pd.to_datetime(t.transaction_ts,errors="coerce")
    t["transaction_status"]=t.transaction_status.astype(str).str.upper().str.strip()
    for col in ["net_sales","discount_amount","subtotal"]: t[col]=pd.to_numeric(t[col],errors="coerce")
    assert c.customer_id.notna().all() and c.customer_id.is_unique
    assert t.transaction_id.notna().all() and t.transaction_id.is_unique
    assert t.customer_id.isin(c.customer_id).all()
    assert t.transaction_ts.notna().all() and t.net_sales.notna().all()
    assert (t.net_sales>=0).all() and (t.discount_amount>=0).all()
    assert not a[["customer_id","offer_id"]].duplicated().any()
    completed=t[t.transaction_status.eq("COMPLETED")].copy()
    return c,t,completed,a
def welch_ci(x,y,alpha=.05):
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    diff=x.mean()-y.mean(); se=np.sqrt(x.var(ddof=1)/len(x)+y.var(ddof=1)/len(y))
    num=(x.var(ddof=1)/len(x)+y.var(ddof=1)/len(y))**2
    den=(x.var(ddof=1)/len(x))**2/(len(x)-1)+(y.var(ddof=1)/len(y))**2/(len(y)-1)
    df=num/den if den else np.inf; crit=stats.t.ppf(1-alpha/2,df)
    return float(diff),float(diff-crit*se),float(diff+crit*se),float(df)
def build_features(c,t):
    asof=pd.Timestamp("2026-09-30")
    ag=t.groupby("customer_id").agg(last_transaction_date=("transaction_ts","max"),
        lifetime_transactions=("transaction_id","nunique"),lifetime_net_sales=("net_sales","sum"),
        lifetime_discount=("discount_amount","sum"),lifetime_items=("items_count","sum")).reset_index()
    f=c.merge(ag,on="customer_id",how="left",validate="one_to_one")
    for col in ["lifetime_transactions","lifetime_net_sales","lifetime_discount","lifetime_items"]:
        f[col]=f[col].fillna(0)
    f["recency_days"]=(asof-pd.to_datetime(f.last_transaction_date)).dt.days
    f["recency_days"]=f.recency_days.fillna((asof-f.signup_date).dt.days)
    f["avg_order_value"]=np.divide(f.lifetime_net_sales,f.lifetime_transactions,
       out=np.zeros(len(f),dtype=float),where=f.lifetime_transactions.to_numpy()!=0)
    f["customer_tenure_days"]=(asof-f.signup_date).dt.days
    return f
def campaign_itt(a,t):
    start=pd.Timestamp("2026-07-01"); end=pd.Timestamp("2026-10-01")
    post=t[(t.transaction_ts>=start)&(t.transaction_ts<end)]
    agg=post.groupby("customer_id").agg(post_transactions=("transaction_id","nunique"),
        post_net_sales=("net_sales","sum"),post_discount_cost=("discount_amount","sum")).reset_index()
    frame=a[a.offer_id.eq("OFFER_Q3_PERSONALIZED")].merge(agg,on="customer_id",how="left",validate="one_to_one")
    for col in ["post_transactions","post_net_sales","post_discount_cost"]: frame[col]=frame[col].fillna(0)
    frame["assigned_arm"]=frame.assigned_arm.str.title()
    x=frame[frame.assigned_arm.eq("Treatment")]; y=frame[frame.assigned_arm.eq("Control")]
    sales=stats.ttest_ind(x.post_net_sales,y.post_net_sales,equal_var=False)
    tx_test=stats.ttest_ind(x.post_transactions,y.post_transactions,equal_var=False)
    sd,sl,sh,sdf=welch_ci(x.post_net_sales,y.post_net_sales)
    td,tl,th,tdf=welch_ci(x.post_transactions,y.post_transactions)
    mx=x.post_net_sales.mean(); my=y.post_net_sales.mean()
    dx=x.post_discount_cost.mean()-y.post_discount_cost.mean()
    margin=.58
    summary=frame.groupby("assigned_arm").agg(n_customers=("customer_id","nunique"),
      avg_transactions=("post_transactions","mean"),avg_net_sales=("post_net_sales","mean"),
      avg_discount_cost=("post_discount_cost","mean"),total_net_sales=("post_net_sales","sum")).reset_index()
    result={"campaign_id":"OFFER_Q3_PERSONALIZED","window_start":"2026-07-01","window_end":"2026-09-30",
      "analysis_type":"Intention-to-treat randomized assignment; Welch two-sample inference",
      "treatment_customers":int(len(x)),"control_customers":int(len(y)),
      "treatment_avg_net_sales_per_customer":float(mx),"control_avg_net_sales_per_customer":float(my),
      "incremental_net_sales_per_customer":sd,"net_sales_ci95_low":sl,"net_sales_ci95_high":sh,
      "net_sales_welch_p_value":float(sales.pvalue),
      "treatment_avg_transactions_per_customer":float(x.post_transactions.mean()),
      "control_avg_transactions_per_customer":float(y.post_transactions.mean()),
      "incremental_transactions_per_customer":td,"transactions_ci95_low":tl,"transactions_ci95_high":th,
      "transactions_welch_p_value":float(tx_test.pvalue),
      "incremental_discount_cost_per_customer":float(dx),"assumed_contribution_margin_rate":margin,
      "incremental_contribution_proxy_per_customer":float(sd*margin-dx),
      "guardrail":"Synthetic data only; contribution margin is an explicit teaching assumption."}
    return frame,summary,result
def monthly_kpis(t):
    x=t.copy(); x["month_start"]=x.transaction_ts.dt.to_period("M").dt.to_timestamp()
    return x.groupby("month_start").agg(transactions=("transaction_id","nunique"),net_sales=("net_sales","sum"),
      discounts=("discount_amount","sum"),active_customers=("customer_id","nunique"),items=("items_count","sum")).reset_index().assign(
      avg_order_value=lambda z:z.net_sales/z.transactions,
      sales_per_active_customer=lambda z:z.net_sales/z.active_customers)
def main():
    d=load_data(); c,raw,completed,a=clean(d); features=build_features(c,completed)
    frame,summary,result=campaign_itt(a,completed); monthly=monthly_kpis(completed)
    features.to_csv(OUT/"customer_features.csv",index=False)
    frame.to_csv(OUT/"campaign_itt_customer_level.csv",index=False)
    summary.to_csv(OUT/"campaign_itt_summary.csv",index=False)
    (OUT/"campaign_results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    monthly.to_csv(ROOT/"dashboard/dashboard_kpis.csv",index=False)
    (ROOT/"docs/generated_results.md").write_text(
      "# Generated results — synthetic data only\n\n"+
      f"- Customers: {len(c):,}\n- Raw transactions: {len(raw):,}\n- Completed transactions: {len(completed):,}\n"+
      f"- Treatment / control: {len(frame[frame.assigned_arm=='Treatment']):,} / {len(frame[frame.assigned_arm=='Control']):,}\n"+
      f"- Incremental net sales per assigned customer: ${result['incremental_net_sales_per_customer']:.2f}\n"+
      f"- 95% CI: ${result['net_sales_ci95_low']:.2f} to ${result['net_sales_ci95_high']:.2f}\n"+
      f"- Welch p-value: {result['net_sales_welch_p_value']:.4g}\n"+
      f"- Incremental contribution proxy/customer: ${result['incremental_contribution_proxy_per_customer']:.2f}\n\n"+
      "Interpretation: all numbers are generated from synthetic records. Check power, sample-ratio mismatch, pre-period balance, return policy, offer costs and Finance-approved margin before any real decision.\n",encoding="utf-8")
    print(f"PASS: customers={len(c):,}; raw_transactions={len(raw):,}; completed={len(completed):,}")
    print(f"ITT net sales difference/customer=${result['incremental_net_sales_per_customer']:.2f}; p={result['net_sales_welch_p_value']:.4g}")
if __name__=="__main__": main()
