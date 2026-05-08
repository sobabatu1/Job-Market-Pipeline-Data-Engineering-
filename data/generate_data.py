import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_job_data(num_rows=500000):
    print(f"🚀 Generating {num_rows} job postings...")
    
    # 1. Setup paths
    os.makedirs('data/raw', exist_ok=True)
    
    # 2. Define sample data for randomization
    titles = ['Data Engineer', 'Data Analyst', 'Senior Data Engineer', 'Analytics Engineer', 'BI Analyst']
    companies = [f'Company_{i}' for i in range(1, 51)]
    locations = ['Remote', 'New York, NY', 'Austin, TX', 'San Francisco, CA', 'Chicago, IL', 'London, UK']
    experience_levels = ['Entry', 'Mid', 'Senior', 'Lead']
    skills_list = ['Python', 'SQL', 'AWS', 'Azure', 'dbt', 'Snowflake', 'Spark', 'Airflow', 'Tableau', 'Power BI']

    # 3. Create dummy job postings
    data = {
        'job_id': range(1, num_rows + 1),
        'title': np.random.choice(titles, num_rows),
        'company_name': np.random.choice(companies, num_rows),
        'location': np.random.choice(locations, num_rows),
        'experience_level': np.random.choice(experience_levels, num_rows),
        'salary_min': np.random.randint(60000, 120000, num_rows),
        'salary_max': np.random.randint(120001, 200000, num_rows),
        'posted_date': [(datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_rows)],
        'skills': [','.join(np.random.choice(skills_list, np.random.randint(1, 5), replace=False)) for _ in range(num_rows)]
    }

    df = pd.DataFrame(data)
    df.to_csv('data/raw/job_postings.csv', index=False)
    print(f"✅ Successfully generated data/raw/job_postings.csv ({num_rows} rows)")

    # 4. Create metadata tables (Companies & Skills)
    pd.DataFrame({'company_name': companies, 'industry': np.random.choice(['Tech', 'Finance', 'Healthcare'], 50)}).to_csv('data/raw/companies.csv', index=False)
    pd.DataFrame({'skill_name': skills_list, 'category': 'Data Engineering'}).to_csv('data/raw/skills.csv', index=False)
    print("✅ Successfully generated metadata files (companies.csv, skills.csv)")

if __name__ == "__main__":
    generate_job_data()