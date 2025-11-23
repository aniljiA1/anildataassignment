-- sql/analysis.sql

-- 1) Year-over-Year growth (Total Value, Duty Paid, Grand Total)
WITH yearly AS (
  SELECT year,
         SUM(total_value_inr) AS total_value,
         SUM(duty_paid_inr) AS duty_paid,
         SUM(grand_total_inr) AS grand_total
  FROM trade_clean
  GROUP BY year
)
SELECT y.year,
       y.total_value,
       LAG(y.total_value) OVER (ORDER BY y.year) AS prev_total_value,
       CASE WHEN LAG(y.total_value) OVER (ORDER BY y.year) IS NULL THEN NULL
            ELSE 100.0*(y.total_value - LAG(y.total_value) OVER (ORDER BY y.year)) / NULLIF(LAG(y.total_value) OVER (ORDER BY y.year),0)
       END AS yoy_total_value_pct,
       y.duty_paid,
       CASE WHEN LAG(y.duty_paid) OVER (ORDER BY y.year) IS NULL THEN NULL
            ELSE 100.0*(y.duty_paid - LAG(y.duty_paid) OVER (ORDER BY y.year)) / NULLIF(LAG(y.duty_paid) OVER (ORDER BY y.year),0)
       END AS yoy_duty_paid_pct,
       y.grand_total,
       CASE WHEN LAG(y.grand_total) OVER (ORDER BY y.year) IS NULL THEN NULL
            ELSE 100.0*(y.grand_total - LAG(y.grand_total) OVER (ORDER BY y.year)) / NULLIF(LAG(y.grand_total) OVER (ORDER BY y.year),0)
       END AS yoy_grand_total_pct
FROM yearly y
ORDER BY y.year;


-- 2) Pareto: Top 25 HSN codes by value + Others
WITH hsn_sum AS (
  SELECT COALESCE(hsn_code,'UNKNOWN') AS hsn_code,
         SUM(total_value_inr) AS hsn_value
  FROM trade_clean
  GROUP BY COALESCE(hsn_code,'UNKNOWN')
), ranked AS (
  SELECT hsn_code, hsn_value,
         ROW_NUMBER() OVER (ORDER BY hsn_value DESC) AS rn,
         SUM(hsn_value) OVER () AS total_value
  FROM hsn_sum
)
SELECT CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END AS hsn_code_group,
       SUM(hsn_value) AS group_value,
       ROUND(SUM(hsn_value)*100.0 / MAX(total_value),2) AS pct_of_total
FROM ranked
GROUP BY CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END, rn
ORDER BY group_value DESC;


-- 3) Supplier longevity & status in 2025
WITH supplier_years AS (
  SELECT supplier_name,
         MIN(year) AS first_year,
         MAX(year) AS last_year,
         COUNT(DISTINCT year) AS active_years,
         SUM(total_value_inr) AS lifetime_value
  FROM trade_clean
  GROUP BY supplier_name
)
SELECT supplier_name, first_year, last_year, active_years, lifetime_value,
       CASE WHEN last_year = 2025 THEN 'active_2025' ELSE 'not_active_2025' END AS status_2025
FROM supplier_years
ORDER BY lifetime_value DESC
LIMIT 200;


-- 4) Model-level price comparison across suppliers (example)
SELECT model_number, supplier_name, year,
       SUM(quantity_num) AS total_qty,
       ROUND(AVG(unit_price_inr),2) AS avg_unit_price,
       ROUND(MIN(unit_price_inr),2) AS min_unit_price,
       ROUND(MAX(unit_price_inr),2) AS max_unit_price
FROM trade_clean
WHERE model_number IS NOT NULL
GROUP BY model_number, supplier_name, year
ORDER BY model_number, year;
