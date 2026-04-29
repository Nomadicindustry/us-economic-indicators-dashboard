-- Clean dataset for Power BI consumption

SELECT
    date,
    indicator_name,
    series_id,
    value,
    last_updated
FROM economic_indicators
WHERE value IS NOT NULL
ORDER BY date;