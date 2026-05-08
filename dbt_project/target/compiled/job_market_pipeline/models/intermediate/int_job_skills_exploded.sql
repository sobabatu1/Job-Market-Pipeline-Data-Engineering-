

-- CTE 1: Get data from staging
WITH staging_data AS (
    SELECT 
        job_id,
        skills 
    FROM "job_pipeline"."public_staging"."stg_job_postings"
    WHERE skills IS NOT NULL 
      AND skills != ''
), -- <-- THIS COMMA IS MANDATORY

-- CTE 2: Break the strings apart
exploded_skills AS (
    SELECT
        job_id,
        TRIM(UNNEST(STRING_TO_ARRAY(skills, ','))) AS skill_name
    FROM staging_data
) -- <-- NO COMMA HERE

-- Final Output
SELECT 
    md5(cast(coalesce(cast(job_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(skill_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS job_skill_id,
    job_id,
    skill_name
FROM exploded_skills