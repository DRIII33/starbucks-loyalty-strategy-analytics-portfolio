# Starbucks-Style Loyalty Strategy Analytics Portfolio

**Disclosure:** Independent portfolio project. All records and campaign outcomes are synthetic. This is not Starbucks internal data and does not claim an actual internal Starbucks problem.

## Business question
Would a hypothetical personalized $2 loyalty offer create incremental member purchasing behavior sufficient to justify incremental discount cost?

## Maps to the supplied job description
- Customer insights from behavioral data: customer, transaction, store, product, offer and assignment tables.
- Performance / future KPIs: recency, frequency, spend, active members, AOV and campaign incrementality.
- Analytics tooling and speed to insight: repeatable Python pipeline, BigQuery SQL views, QA checks and dashboard-ready monthly data.
- Ambiguous issue framing: hypothesis, primary outcome, ITT estimand, assumptions and guardrails.
- Analytical frameworks / metrics: metric definitions, SQL transformations, formula workbook and data dictionary.
- Executive storytelling: executive summary, dashboard narrative and generated result artifact.
- Financial acumen: incremental net sales, incremental discount cost and an assumed contribution proxy.

## Workflow
1. Read `docs/Project_Disclaimer.md` and `docs/Data_Dictionary.md`.
2. Run Python: `pip install -r requirements.txt`, then `python src/run_analysis.py`.
3. Run tests: `python -m pytest -q`.
4. Load CSVs to BigQuery using `docs/BigQuery_Setup.md`; run `sql/01_load_and_clean.sql`, `sql/02_analytics_views.sql`, and `sql/03_quality_checks.sql`.
5. Build dashboard using `dashboard/Looker_Studio_Build_Guide.md`.
6. Use the exact generated numbers from `docs/generated_results.md`; never present synthetic results as Starbucks performance.

For Colab, upload the ZIP, extract to `/content/starbucks_loyalty_portfolio`, run `!pip install -r /content/starbucks_loyalty_portfolio/requirements.txt`, then run the notebook or `!python /content/starbucks_loyalty_portfolio/src/run_analysis.py`. Runtime files are temporary; download outputs after the run.

## Repository contents
- `data/raw/`: deterministic synthetic CSVs
- `data/processed/`: generated feature, ITT and campaign results after pipeline run
- `sql/`: schema, data cleaning, analytical views, QA
- `src/generate_synthetic_data.py`: deterministic synthetic data generator
- `src/run_analysis.py`: full Python pipeline
- `notebooks/`: Colab/Jupyter notebook
- `Starbucks_Loyalty_Portfolio_Workbook.xlsx`: populated workbook with data tables and formulas
- `docs/`: executive narrative, disclaimer, source notes, setup and runbook
- `.github/workflows/validate.yml`: CI workflow

## Reproduce the synthetic data
```bash
python src/generate_synthetic_data.py
```

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/run_analysis.py
python -m pytest -q
```
