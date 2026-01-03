#!/bin/bash
set -e

echo "==> Tambah pg_hba rule di primary agar standby bisa connect..."
docker exec -u postgres pg_primary bash -c "echo \"host replication repl 0.0.0.0/0 md5\" >> /var/lib/postgresql/data/pg_hba.conf"
docker exec -u postgres pg_primary bash -c "echo \"host all all 0.0.0.0/0 md5\" >> /var/lib/postgresql/data/pg_hba.conf"
docker exec -u postgres pg_primary pg_ctl reload -D /var/lib/postgresql/data

echo "==> Stop standby untuk prepare basebackup..."
docker stop pg_standby

echo "==> Bersihkan data standby lama..."
docker run --rm -v standby_data:/var/lib/postgresql/data alpine sh -c "rm -rf /var/lib/postgresql/data/*"

echo "==> Jalankan pg_basebackup dari primary ke standby volume..."
docker run --rm --network docker_pgnet \
  -v standby_data:/var/lib/postgresql/data \
  -e PGPASSWORD=replpass \
  postgres:13 bash -c "\
    pg_basebackup -h pg_primary -p 5432 -D /var/lib/postgresql/data \
    -U repl -Fp -Xs -P -R"

echo "==> Start standby..."
docker start pg_standby

echo "==> Selesai setup standby."
