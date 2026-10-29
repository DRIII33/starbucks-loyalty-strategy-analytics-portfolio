from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
import run_analysis
def test_keys_and_integrity():
 d=run_analysis.load_data(); c,t,done,a=run_analysis.clean(d)
 assert c.customer_id.is_unique and t.transaction_id.is_unique
 assert t.customer_id.isin(c.customer_id).all()
 assert not a[["customer_id","offer_id"]].duplicated().any()
def test_itt_outputs_finite():
 d=run_analysis.load_data(); c,t,done,a=run_analysis.clean(d)
 frame,summary,result=run_analysis.campaign_itt(a,done)
 assert result["treatment_customers"]>0 and result["control_customers"]>0
 assert result["net_sales_ci95_low"]<=result["incremental_net_sales_per_customer"]<=result["net_sales_ci95_high"]
