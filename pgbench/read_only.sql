\set region_id random(1,3)
SELECT COUNT(*) FROM online_sales;

SELECT product_category, SUM(total_revenue)
FROM online_sales
GROUP BY product_category
ORDER BY 2 DESC
LIMIT 5;

SELECT *
FROM online_sales
WHERE date >= '2024-01-01' AND date <= '2024-12-31'
ORDER BY total_revenue DESC
LIMIT 10;
