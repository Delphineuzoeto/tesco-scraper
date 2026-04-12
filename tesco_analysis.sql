-- Check how many rows have no date
SELECT
	COUNT(*) AS missing_dates
FROM
	tesco_data td
WHERE
	date IS NULL
	OR date = '';

-- Create a clean working table
CREATE TABLE tesco_clean_data AS 
SELECT *
FROM tesco
WHERE date IS NOT NULL
  AND date != '';

-- Verify
SELECT  COUNT (*) FROM tesco_data_clean;

-- Records per category per day
SELECT
    category,
    date,
    COUNT(*) AS product_count
FROM tesco_data_clean
GROUP BY category, date
ORDER BY date, category;


-- Date range
SELECT
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    COUNT(DISTINCT date) AS total_days
FROM tesco_data_clean;


-- How many unique products per category
SELECT
    category,
    COUNT(DISTINCT name) AS unique_products
FROM tesco_data_clean
GROUP BY category
ORDER BY unique_products DESC;


--Average price per category per day
SELECT
    category,
    date,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(MIN(price), 2) AS min_price,
    ROUND(MAX(price), 2) AS max_price,
    COUNT(*) AS num_products
FROM tesco_data_clean
GROUP BY category, date
ORDER BY category, date;


--Products whose price changed across days
SELECT
    name,
    category,
    ROUND(MIN(price), 2) AS lowest_price,
    ROUND(MAX(price), 2) AS highest_price,
    ROUND(MAX(price) - MIN(price), 2) AS price_change,
    COUNT(DISTINCT date) AS days_seen
FROM tesco_data_clean
GROUP BY name, category
HAVING MIN(price) != MAX(price)
ORDER BY price_change DESC
LIMIT 20;


-- SQLite uses date(date, '+1 day') instead of INTERVAL
SELECT
    t1.name,
    t1.category,
    t1.date AS current_date,
    t1.price AS current_price,
    t2.date AS prev_date,
    t2.price AS prev_price,
    ROUND(t1.price - t2.price, 2) AS price_diff,
    ROUND(((t1.price - t2.price) / t2.price) * 100, 1) AS pct_change
FROM tesco_data_clean t1
JOIN tesco_data_clean t2
    ON t1.name = t2.name
    AND t1.date = date(t2.date, '+1 day')
WHERE t1.price != t2.price
ORDER BY ABS(t1.price - t2.price) DESC
LIMIT 30;

--New products that appeared mid-scrape
SELECT
    name,
    category,
    MIN(date) AS first_seen
FROM tesco_data_clean
WHERE name NOT IN (
    SELECT name
    FROM tesco_data_clean
    WHERE date = (SELECT MIN(date) FROM tesco_data_clean)
)
GROUP BY name, category
ORDER BY first_seen;


--products that disappered
SELECT
    name,
    category,
    MAX(date) AS last_seen
FROM tesco_data_clean
WHERE name NOT IN (
    SELECT name
    FROM tesco_data_clean
    WHERE date = (SELECT MAX(date) FROM tesco_data_clean)
)
GROUP BY name, category
ORDER BY last_seen DESC;


--biggest price jump
SELECT
    category,
    name,
    ROUND(MIN(price), 2) AS lowest_price,
    ROUND(MAX(price), 2) AS highest_price,
    ROUND(((MAX(price) - MIN(price)) / MIN(price)) * 100, 1) AS pct_increase
FROM tesco_data_clean
GROUP BY category, name
HAVING MIN(price) != MAX(price)
ORDER BY pct_increase DESC
LIMIT 10;







