#!/bin/bash
set -e

DB=marketplace
CSV="/dataset/online_sales.csv"

echo "==> Buat table online_sales sesuai kolom CSV..."
docker exec -u postgres pg_primary psql -U postgres -d $DB <<'SQL'
DROP TABLE IF EXISTS online_sales;
CREATE TABLE online_sales (
  transaction_id    INT,
  date              DATE,
  product_category  TEXT,
  product_name      TEXT,
  units_sold        INT,
  unit_price        NUMERIC(12,2),
  total_revenue     NUMERIC(12,2),
  region            TEXT,
  payment_method    TEXT
);
SQL

echo "==> Import CSV ke online_sales..."
docker exec -u postgres pg_primary psql -U postgres -d $DB -c "\copy online_sales FROM '$CSV' WITH (FORMAT csv, HEADER true)"

echo "==> Index ringan untuk bantu query..."
docker exec -u postgres pg_primary psql -U postgres -d $DB -c "CREATE INDEX idx_sales_date ON online_sales(date);"
docker exec -u postgres pg_primary psql -U postgres -d $DB -c "CREATE INDEX idx_sales_region ON online_sales(region);"
docker exec -u postgres pg_primary psql -U postgres -d $DB -c "CREATE INDEX idx_sales_category ON online_sales(product_category);"

echo "==> Cek row count:"
docker exec -u postgres pg_primary psql -U postgres -d $DB -c "SELECT COUNT(*) FROM online_sales;"
