#!/bin/bash
set -e

# 1. Force the script to use ONLY the venv binaries
export PATH="/Users/lbaba/job_market_pipeline/venv/bin:$PATH"
unset PYTHONPATH

echo "--- [1/3] Loading Synthetic Baselines ---"
python3 data/generate_data.py

echo "--- [2/3] Executing Live Scraper ---"
python3 ingestion/live_scrape.py

echo "--- [3/3] Running dbt Transformations ---"
cd dbt_project
dbt run
cd ..

echo "--- Pipeline Execution Successfully Completed ---"