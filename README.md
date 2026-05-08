🚀 Job Market Data Pipeline (500k Scale)
A robust, end-to-end ELT pipeline that ingests, cleans, and transforms half a million job postings to uncover high-demand skills and salary benchmarks.

## The Problem
Modern job market data is often messy, unstructured, and high-volume. Analyzing 500,000+ records in a standard BI tool without a structured data warehouse leads to:

Performance Bottlenecks: Local machines crashing due to memory (RAM) exhaustion.

Data Quality Issues: "Dirty" strings (whitespace, case inconsistencies) and comma-separated "skills" that cannot be aggregated.

Lack of Lineage: No clear path from raw CSV files to final business metrics.

## The Approach: Medallion Architecture
I implemented a Medallion Architecture to ensure data reliability and scalability:

Bronze (Raw): Ingested 500,000 rows into PostgreSQL using a Python-based chunking strategy (50k rows per batch) to maintain a low memory footprint.

Silver (Staging): Used dbt to cast data types, trim strings, and create derived flags like is_remote.

Intermediate: Solved the "Skills" problem by unnesting comma-separated strings into a normalized, long-format table using PostgreSQL UNNEST functions.

Gold (Marts): Aggregated metrics into a final "Insights" table, ranking skills by both demand and average salary.
Graph: ![Graph](<Lineage Graph.png>)

## Tech Stack
Language: Python

Database: PostgreSQL

Transformation: dbt (Data Build Tool)

Infrastructure: Local Dev Environment, VS Code, Virtual Environments

Key Libraries: Pandas, SQLAlchemy, Psycopg2, dbt-utils

Key Engineering Features
Memory-Efficient Ingestion: Used chunksize processing in Pandas to handle large-scale CSVs without crashing the system.

Safe Connection String Handling: Implemented URL encoding for special characters in database credentials.

Surrogate Key Generation: Leveraged dbt_utils to create unique MD5 hashes for many-to-many job-skill relationships.

Idempotent Pipelines: Designed scripts to be "run-ready" at any time without creating duplicate data.

## Sample Insights
Based on the analysis of 500k+ historical records and live scraped data:

| Skill | Demand Rank | Avg Salary | Remote % |
| :--- | :--- | :--- | :--- |
| SQL | 1 | $115,000 | 45% |
| Python | 2 | $128,000 | 52% |
| AWS | 3 | $142,000 | 60% |