-- Preview available economic indicators
SELECT
    indicator_name,
    series_id,
    COUNT(*) AS row_count,
    MIN(date) AS first_date,
    MAX(date) AS latest_date
FROM economic_indicators
GROUP BY
    indicator_name,
    series_id
ORDER BY
    indicator_name;