"""
Phase 2 - Dynamic Programming (0/1 Knapsack) Module
Selects the optimal subset of parcels that maximises total value
without exceeding the vehicle capacity.
"""

from typing import List, Dict, Any, Tuple


def knapsack_dp(parcels: List[Dict[str, Any]], capacity: int) -> Tuple[List[Dict[str, Any]], int, List[List[int]]]:
    """
    Classic 0/1 Knapsack using Dynamic Programming.

    Args:
        parcels: List of parcel dicts (must contain 'weight' and 'value')
        capacity: Maximum weight the vehicle can carry

    Returns:
        selected_parcels : list of chosen parcel dicts
        total_value      : maximum value achieved
        dp_table         : the filled DP table (for evidence/demo)
    """
    n = len(parcels)
    # DP table: dp[i][w] = max value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find which parcels were selected
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= parcels[i - 1]["weight"]

    selected.reverse()  # restore original relative order
    total_value = dp[n][capacity]
    return selected, total_value, dp


def print_knapsack_result(selected: List[Dict[str, Any]], total_value: int, capacity: int) -> None:
    """Pretty-print packing plan."""
    total_weight = sum(p["weight"] for p in selected)
    print("\n=== Optimal Packing Plan (0/1 Knapsack DP) ===")
    print(f"Vehicle Capacity : {capacity}")
    print(f"Selected Parcels : {len(selected)}")
    print(f"Total Weight     : {total_weight}")
    print(f"Total Value      : {total_value}")
    print(f"\n{'ID':<8} {'Weight':<8} {'Value':<8} {'Destination'}")
    print("-" * 40)
    for p in selected:
        print(f"{p['id']:<8} {p['weight']:<8} {p['value']:<8} {p['destination']}")
