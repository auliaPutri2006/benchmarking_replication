#!/bin/bash
set -e
echo "==> Set synchronous replication di primary..."

docker exec -u postgres pg_primary psql -U postgres -c "ALTER SYSTEM SET synchronous_commit = 'on';"
docker exec -u postgres pg_primary psql -U postgres -c "ALTER SYSTEM SET synchronous_standby_names = '1 (pg_standby)';"
docker exec -u postgres pg_primary pg_ctl restart -D /var/lib/postgresql/data

echo "==> SYNC mode aktif."
