"""
Mini-Courier Planner
====================
Capstone Project - Design & Analysis of Algorithms (ETCCDA302)

Integrated system that:
  1. Sorts parcels by deadline & priority
  2. Selects optimal subset using 0/1 Knapsack DP
  3. Builds delivery route using Dijkstra + Nearest-Neighbor TSP
  4. Records runtime of major steps for performance analysis
  
"""

import json
import time
import os
from typing import List, Dict, Any

from algorithms.sorting import sort_parcels, print_sorted_parcels
from algorithms.knapsack import knapsack_dp, print_knapsack_result
from algorithms.dijkstra import dijkstra, print_shortest_paths
from algorithms.tsp import nearest_neighbor_tsp, print_route


VEHICLE_CAPACITY = 15          # Maximum weight the courier vehicle can carry
DEPOT = "Depot"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def load_json(filename: str):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)


def run_planner(parcels_file: str = "sample_parcels.json",
                graph_file: str = "sample_graph.json",
                capacity: int = VEHICLE_CAPACITY,
                verbose: bool = True) -> Dict[str, Any]:
    """
    Full end-to-end courier planning pipeline.
    Returns a dictionary with results and timings.
    """
    results = {}
    timings = {}

    parcels = load_json(parcels_file)
    graph = load_json(graph_file)

    if verbose:
        print("=" * 70)
        print("          MINI-COURIER PLANNER  |  Capstone Project")
        print("=" * 70)
        print(f"Loaded {len(parcels)} parcels | Graph nodes: {list(graph.keys())}")
        print(f"Vehicle Capacity: {capacity}")

    # ---------- Phase 2: Sorting ----------
    start = time.perf_counter()
    sorted_parcels = sort_parcels(parcels)
    timings["sorting"] = time.perf_counter() - start

    if verbose:
        print_sorted_parcels(sorted_parcels)

    # ---------- Phase 2: Knapsack DP ----------
    start = time.perf_counter()
    selected, total_value, dp_table = knapsack_dp(sorted_parcels, capacity)
    timings["knapsack"] = time.perf_counter() - start

    if verbose:
        print_knapsack_result(selected, total_value, capacity)

    # Collect unique destinations of selected parcels
    destinations = list({p["destination"] for p in selected})

    # ---------- Phase 3: Dijkstra (from Depot) ----------
    start = time.perf_counter()
    distances, previous = dijkstra(graph, DEPOT)
    timings["dijkstra"] = time.perf_counter() - start

    if verbose:
        print_shortest_paths(distances, previous, DEPOT)

    # ---------- Phase 3: Nearest-Neighbor TSP ----------
    start = time.perf_counter()
    route, total_distance = nearest_neighbor_tsp(graph, destinations, start=DEPOT)
    timings["tsp"] = time.perf_counter() - start

    if verbose:
        print_route(route, total_distance)

    results = {
        "num_parcels_input": len(parcels),
        "num_parcels_selected": len(selected),
        "selected_ids": [p["id"] for p in selected],
        "total_value": total_value,
        "total_weight": sum(p["weight"] for p in selected),
        "destinations": destinations,
        "route": route,
        "route_distance": total_distance,
        "timings": timings,
        "dp_table_rows": len(dp_table),
        "dp_table_cols": len(dp_table[0]) if dp_table else 0,
    }

    if verbose:
        print("\n" + "=" * 70)
        print("PERFORMANCE SUMMARY (seconds)")
        print("-" * 40)
        for step, t in timings.items():
            print(f"  {step:<12}: {t:.6f} s")
        print(f"  {'TOTAL':<12}: {sum(timings.values()):.6f} s")
        print("=" * 70)

    return results


def performance_test():
    """
    Phase 4 - Run on small and larger datasets and compare runtimes.
    """
    print("\n" + "#" * 70)
    print("PHASE 4 – PERFORMANCE TESTING")
    print("#" * 70)

    test_cases = [
        ("sample_parcels.json", 15, "Small (10 parcels)"),
        ("large_parcels.json", 20, "Medium (25 parcels)"),
        ("large_parcels.json", 30, "Medium-Large (25 parcels, higher capacity)"),
    ]

    all_results = []
    for file, cap, label in test_cases:
        print(f"\n>>> Test Case: {label}")
        res = run_planner(parcels_file=file, capacity=cap, verbose=False)
        print(f"    Selected {res['num_parcels_selected']}/{res['num_parcels_input']} parcels")
        print(f"    Value = {res['total_value']} | Route distance = {res['route_distance']}")
        print(f"    Timings → Sorting: {res['timings']['sorting']:.6f}s | "
              f"Knapsack: {res['timings']['knapsack']:.6f}s | "
              f"Dijkstra: {res['timings']['dijkstra']:.6f}s | "
              f"TSP: {res['timings']['tsp']:.6f}s")
        all_results.append((label, res))

    # Save a simple runtime comparison CSV for charts
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_path = os.path.join(OUTPUT_DIR, "runtime_comparison.csv")
    with open(csv_path, "w") as f:
        f.write("TestCase,Sorting,Knapsack,Dijkstra,TSP,Total\n")
        for label, res in all_results:
            t = res["timings"]
            total = sum(t.values())
            f.write(f'"{label}",{t["sorting"]:.6f},{t["knapsack"]:.6f},'
                    f'{t["dijkstra"]:.6f},{t["tsp"]:.6f},{total:.6f}\n')
    print(f"\nRuntime data saved to: {csv_path}")
    return all_results


def generate_runtime_chart():
    """
    Optional: Generate a simple bar chart if matplotlib is available.
    """
    try:
        import matplotlib.pyplot as plt
        import csv

        csv_path = os.path.join(OUTPUT_DIR, "runtime_comparison.csv")
        if not os.path.exists(csv_path):
            print("Run performance_test() first.")
            return

        labels, sorting, knapsack, dijkstra, tsp = [], [], [], [], []
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                labels.append(row["TestCase"])
                sorting.append(float(row["Sorting"]))
                knapsack.append(float(row["Knapsack"]))
                dijkstra.append(float(row["Dijkstra"]))
                tsp.append(float(row["TSP"]))

        x = range(len(labels))
        width = 0.2

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([i - 1.5*width for i in x], sorting, width, label="Sorting")
        ax.bar([i - 0.5*width for i in x], knapsack, width, label="Knapsack DP")
        ax.bar([i + 0.5*width for i in x], dijkstra, width, label="Dijkstra")
        ax.bar([i + 1.5*width for i in x], tsp, width, label="TSP (NN)")

        ax.set_ylabel("Time (seconds)")
        ax.set_title("Runtime Comparison of Algorithmic Components")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, rotation=15, ha="right")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        chart_path = os.path.join(OUTPUT_DIR, "runtime_chart.png")
        plt.tight_layout()
        plt.savefig(chart_path, dpi=120)
        print(f"Runtime chart saved to: {chart_path}")
        plt.close()
    except ImportError:
        print("matplotlib not installed – skipping chart generation.")
        print("You can still use the CSV file to create charts in Excel/Google Sheets.")


if __name__ == "__main__":
    # Main demo with sample data
    run_planner()

    # Phase 4 performance testing
    performance_test()

    # Optional chart
    generate_runtime_chart()
