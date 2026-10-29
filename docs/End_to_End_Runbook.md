# End-to-End Runbook

1. **Scope:** read the disclaimer. Treat the challenge as hypothetical.
2. **Reproducibility:** run `python src/generate_synthetic_data.py` to regenerate the CSVs with fixed seed `260079240`; then run the analysis pipeline. Regeneration overwrites `data/raw/`.
3. **GitHub:** create `starbucks-loyalty-strategy-analytics-portfolio`; upload all repository files; review rendered executive artifacts; keep disclosure prominent.
4. **Python/Colab:** install `requirements.txt`, run `python src/run_analysis.py`, then `python -m pytest -q`. In Colab, upload and unzip the repository to `/content/starbucks_loyalty_portfolio`; runtimes are ephemeral, so download generated outputs.
5. **BigQuery:** load CSVs to `raw_*` tables and run SQL in numeric order. Run QA queries individually. Sandbox expiration/restrictions may require reloads.
6. **Dashboard:** follow the Looker Studio guide; if BigQuery billing is unavailable, use the CSV/Sheets route and disclose it is a static extract.
7. **Story:** use generated results, not manually invented numbers. State estimate, uncertainty, discount cost, assumed margin and limitations.
8. **Publish review:** no private/real Starbucks data; tests pass; Python and SQL reconcile; dashboard definitions and date windows are visible.
