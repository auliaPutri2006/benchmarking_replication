BEGIN;

SELECT SUM(total_revenue) FROM online_sales WHERE region = 'North America';

UPDATE online_sales
SET unit_price = unit_price
WHERE transaction_id = (SELECT transaction_id FROM online_sales LIMIT 1);

COMMIT;
