# Local performance benchmark

Measured October 18, 2026 against application source `6267e3ac6535633f39132753b8b98a79bc94221f`. The benchmark files and documentation were added afterward; application code was unchanged.

## Workload and scope

50/50 GET/PUT note operations, 8 independent rooms, 2048-character notes, SQLite file database; optimistic revision correctness checked.

Synthetic local loopback HTTP benchmark. Not production capacity, real users, clinical validation or user growth. These measurements describe one short workload on one machine. They do not establish a capacity ceiling, sustained service-level objective, p99 guarantee, production response time or adoption. No historical speedup is claimed unless a comparison is explicitly defined below.

Environment: Darwin 25.2.0, arm64, 12 logical CPUs, Python 3.12.14. Gunicorn 23.0.0, 1 gthread worker, 8 threads.

- 8 concurrent HTTP clients, 40 untimed warmup requests.
- 3 rounds of 800 measured requests: **2,400 total**.
- Requests use persistent local loopback HTTP connections. The client and server share one machine.
- Every response is checked for HTTP success and workload-specific correctness; failures abort without producing a successful report.
- All data is synthetic and isolated in a temporary directory.

## Results

| Round | Requests | Median latency | p95 latency | Requests/second | Failures |
|---|---:|---:|---:|---:|---:|
| 1 | 800 | 2.189 ms | 24.322 ms | 981.14 | 0 |
| 2 | 800 | 2.301 ms | 16.402 ms | 1060.34 | 0 |
| 3 | 800 | 1.890 ms | 22.310 ms | 1120.89 | 0 |

Combined latency: **2.086 ms median**, **22.276 ms p95**. Median round throughput: **1060.34 requests/second**. All **2,400 requests passed** their checks. p95 is the nearest-rank 95th percentile; throughput includes client scheduling and validation.

The workload uses 8 independent rooms per round and checks revision increments and history counts. It does not measure many simultaneous writers to the same room or the latency of SSE delivery to a browser. Each round has 400 reads and 400 writes.

## Reproduce

```sh
python3.12 -m venv .benchmark-venv
.benchmark-venv/bin/python -m pip install -r benchmarks/requirements.txt
.benchmark-venv/bin/python benchmarks/benchmark.py notemesh --output /tmp/notemesh-benchmark.json
```

Health Passport can select a Java executable with `--java /path/to/java`. Other benchmark modes need no Java. The script creates temporary data, starts only a loopback server and stops it after the run. Compare results only under controlled, comparable machine and workload conditions.

[Recorded JSON](results-2026-10-18.json) contains the source revision, environment, per-round results and comparison timings where applicable.
