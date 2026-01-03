#!/bin/bash
set -e
echo "==> Set asynchronous replication di primary..."

docker exec -u postgres pg_primary psql -U postgres -c "ALTER SYSTEM SET synchronous_commit = 'off';"
docker exec -u postgres pg_primary psql -U postgres -c "ALTER SYSTEM RESET synchronous_standby_names;"
docker exec -u postgres pg_primary pg_ctl restart -D /var/lib/postgresql/data

echo "==> ASYNC mode aktif."
