

WITH raw_data AS (
    SELECT * FROM "job_pipeline"."raw"."job_postings"
),

final AS (
    SELECT
        job_id,
        TRIM(title) AS job_title,
        company_name,
        location,
        skills, 
        CAST(salary_min AS NUMERIC) AS salary_min,
        CAST(salary_max AS NUMERIC) AS salary_max,
        CAST(posted_date AS DATE) AS posted_date,
        -- ADD THIS LOGIC HERE:
        CASE 
            WHEN LOWER(location) LIKE '%remote%' THEN TRUE 
            ELSE FALSE 
        END AS is_remote
    FROM raw_data
)

SELECT * FROM final