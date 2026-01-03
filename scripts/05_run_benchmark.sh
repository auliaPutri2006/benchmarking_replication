#!/bin/bash
set -e

MODE="$1"      
DURATION="${2:-120}"
CLIENTS="${3:-10}"
THREADS="${4:-2}"
PROGRESS="${5:-5}"   

mkdir -p results

echo "==> Benchmark mode=$MODE dur=$DURATION clients=$CLIENTS threads=$THREADS progress=$PROGRESS"


docker exec -u postgres pg_primary pgbench \
  -d marketplace \
  -c "$CLIENTS" -j "$THREADS" -T "$DURATION" \
  --progress="$PROGRESS" \
  -f /scripts/../pgbench/read_only.sql \
  | tee "results/${MODE}_read_only.txt"


docker exec -u postgres pg_primary pgbench \
  -d marketplace \
  -c "$CLIENTS" -j "$THREADS" -T "$DURATION" \
  --progress="$PROGRESS" \
  -f /scripts/../pgbench/mixed_rw.sql \
  | tee "results/${MODE}_mixed_rw.txt"

echo "==> Benchmark selesai. Sekarang generate grafik..."
python scripts/06_generate_plots.py

echo "==> Selesai. Cek results/plots/"
