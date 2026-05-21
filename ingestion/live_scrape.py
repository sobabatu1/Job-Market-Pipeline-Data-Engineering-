from jobspy import scrape_jobs
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv() # Loads the .env file
password = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql://user:{password}@localhost:5432/job_pipeline")
##engine = create_engine(f"postgresql://postgres:Olayinka%401@localhost:5432/job_pipeline")

def scrape_and_append():
    # Fetch live data from 3 major platforms
    jobs = scrape_jobs(
        site_name=["linkedin", "indeed", "glassdoor"],
        search_term="Data Engineer",
        location="Indianapolis, USA",
        results_wanted=25
    )
    
    # Align scraper columns to our database schema (The 'Contract')
    live_df = pd.DataFrame({
        'job_id': range(2000000, 2000000 + len(jobs)), # Unique ID range for live data
        'title': jobs['title'],
        'company_name': jobs['company'],
        'location': jobs['location'],
        'salary_min': jobs['min_amount'].fillna(0),
        'salary_max': jobs['max_amount'].fillna(0),
        'posted_date': pd.to_datetime(jobs['date_posted']).dt.date,
        'skills': "" # Placeholder for dbt to process
    })
    
    live_df.to_sql('job_postings', engine, schema='raw', if_exists='append', index=False)
    print(f"🔥 Blended {len(live_df)} live jobs into Bronze Layer.")

if __name__ == "__main__":
    scrape_and_append()