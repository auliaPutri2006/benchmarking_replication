# PostgreSQL Replication Benchmarking: Synchronous vs Asynchronous

Comparative performance analysis of synchronous and asynchronous replication in PostgreSQL cluster using Docker containerization and pgbench benchmarking tool.

## Research Objective

This study benchmarks the performance differences between synchronous and asynchronous replication modes in PostgreSQL cluster environments, focusing on throughput, latency, and consistency trade-offs using real-world e-commerce dataset.

## Architecture

- **Primary Node**: PostgreSQL 13 (Port 5432)
- **Standby Node**: PostgreSQL 13 (Port 5433) 
- **Containerization**: Docker Compose
- **Network**: Custom Docker network (pgnet)
- **Database**: marketplace with online_sales table

## Dataset

**Online Sales Dataset**: 20,000 transaction records
```
Transaction ID | Date | Product Category | Product Name | Units Sold | Unit Price | Total Revenue | Region | Payment Method
```

## Configuration

### PostgreSQL Settings
- shared_buffers: 512MB
- work_mem: 16MB  
- maintenance_work_mem: 256MB
- effective_cache_size: 4GB
- hot_standby: on

### pgbench Parameters
- Scale Factor: 5
- Concurrent Clients: 10
- Threads: 2
- Duration: 600 seconds (10 minutes)

## Quick Start

1. **Clone Repository**
```bash
git clone <repository-url>
cd postgresql-replication-benchmark
```

2. **Start PostgreSQL Cluster**
```bash
docker-compose up -d
```

3. **Load Dataset**
```bash
./scripts/load_dataset.sh
```

4. **Run Benchmarks**
```bash
# Mixed workload
./scripts/run_benchmark.sh rw_mixed

# Read-heavy workload  
./scripts/run_benchmark.sh rw_read
```

5. **Generate Results**
```bash
./scripts/generate_charts.sh
```

## Workload Patterns

- **rw_mixed**: Balanced read-write operations (50/50)
  - Revenue calculations, regional analysis
  - Product performance queries, inventory updates

- **rw_read**: Read-heavy operations (80/20)
  - Sales reporting, dashboard queries
  - Category analysis, payment method statistics

## Metrics Collected

- **Throughput**: Transactions per second (TPS)
- **Latency**: Response time (avg, 95th, 99th percentile)
- **Consistency**: Replication lag time
- **Resource**: CPU, memory, I/O utilization

## Project Structure

```
├── docker-compose.yml          # Container orchestration
├── primary/postgresql.conf     # Primary node config
├── standby/postgresql.conf     # Standby node config
├── dataset/                    # Online sales data
├── scripts/                    # Benchmark scripts
│   ├── rw_mixed.sql           # Mixed workload
│   ├── rw_read.sql            # Read-heavy workload
│   └── monitoring.sh          # System monitoring
└── results/                   # Output charts and logs
```

## Requirements

- Docker Engine 24.x+
- Docker Compose 2.x+
- 8GB+ RAM recommended
- 20GB+ storage space

## Research Output

Results visualized as bar charts comparing:
- Synchronous vs Asynchronous performance
- rw_mixed vs rw_read workload patterns
- Statistical analysis with confidence intervals

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

*Research conducted as part of Information Systems  project.*
