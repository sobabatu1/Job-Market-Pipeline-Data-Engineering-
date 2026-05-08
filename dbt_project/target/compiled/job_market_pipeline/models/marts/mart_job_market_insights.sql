

SELECT 
    skills.skill_name,
    COUNT(DISTINCT skills.job_id) AS demand_count,
    ROUND(AVG((stg.salary_min + stg.salary_max) / 2), 2) AS avg_market_salary,
    -- This is the line that was failing:
    ROUND(100.0 * COUNT(CASE WHEN stg.is_remote THEN 1 END) / COUNT(*), 2) AS remote_pct
FROM "job_pipeline"."public"."int_job_skills_exploded" AS skills
JOIN "job_pipeline"."public_staging"."stg_job_postings" AS stg 
    ON skills.job_id = stg.job_id
GROUP BY 1
HAVING COUNT(DISTINCT skills.job_id) > 5
ORDER BY demand_count DESC