import random
import statistics
import time
from pathlib import Path

import pandas as pd
from neo4j import GraphDatabase
from tqdm import tqdm

from config import (
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD,
    MEMGRAPH_URI,
    NUM_USERS,
    NUM_COMPANIES,
)
from queries import BENCHMARK_QUERIES

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

WARMUP_RUNS = 20
MEASURED_RUNS = 200


def get_driver(db_name):
    if db_name == "neo4j":
        return GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
        )

    if db_name == "memgraph":
        return GraphDatabase.driver(
            MEMGRAPH_URI,
            auth=None,
        )

    raise ValueError(f"Unknown database: {db_name}")


def build_params(query_name):
    if query_name == "posts_by_company_employees":
        return {
            "company_id": f"company_{random.randint(0, NUM_COMPANIES - 1)}"
        }

    return {
        "user_id": f"user_{random.randint(0, NUM_USERS - 1)}"
    }


def run_single_query(session, query, params):
    start = time.perf_counter()
    result = session.run(query, params)
    records = list(result)
    end = time.perf_counter()

    latency_ms = (end - start) * 1000

    return latency_ms, len(records)


def percentile(values, p):
    sorted_values = sorted(values)
    index = int((p / 100) * len(sorted_values)) - 1
    index = max(0, min(index, len(sorted_values) - 1))
    return sorted_values[index]


def benchmark_database(db_name):
    print(f"\nBenchmarking {db_name}...")

    driver = get_driver(db_name)
    rows = []

    with driver.session() as session:
        for query_name, query in BENCHMARK_QUERIES.items():
            print(f"Running query: {query_name}")

            # Warmup
            for _ in range(WARMUP_RUNS):
                params = build_params(query_name)
                run_single_query(session, query, params)

            latencies = []
            result_counts = []

            for _ in tqdm(range(MEASURED_RUNS)):
                params = build_params(query_name)
                latency_ms, record_count = run_single_query(session, query, params)

                latencies.append(latency_ms)
                result_counts.append(record_count)

            rows.append({
                "database": db_name,
                "query": query_name,
                "runs": MEASURED_RUNS,
                "avg_latency_ms": statistics.mean(latencies),
                "median_latency_ms": statistics.median(latencies),
                "p95_latency_ms": percentile(latencies, 95),
                "p99_latency_ms": percentile(latencies, 99),
                "min_latency_ms": min(latencies),
                "max_latency_ms": max(latencies),
                "avg_records_returned": statistics.mean(result_counts),
            })

    driver.close()

    return rows


def main():
    all_rows = []

    for db_name in ["neo4j", "memgraph"]:
        rows = benchmark_database(db_name)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    output_path = RESULTS_DIR / "benchmark_results.csv"
    df.to_csv(output_path, index=False)

    print("\nBenchmark complete.")
    print(df.to_string(index=False))
    print(f"\nSaved results to {output_path}")


if __name__ == "__main__":
    main()