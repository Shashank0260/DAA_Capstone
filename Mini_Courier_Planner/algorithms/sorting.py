"""
Phase 2 - Parcel Sorting Module
Sorts parcels by delivery deadline (ascending) and priority (descending) as tie-breaker.
Uses Python's Timsort (stable, O(n log n)) which is optimal for this use case.
"""

from typing import List, Dict, Any


def sort_parcels(parcels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort parcels primarily by deadline (earlier first),
    secondarily by priority (higher first).

    Args:
        parcels: List of parcel dictionaries with keys:
                 id, weight, value, priority, deadline, destination

    Returns:
        Sorted list of parcels (new list, original not mutated).
    """
    if not parcels:
        return []

    # Timsort is stable and efficient for real-world data
    sorted_parcels = sorted(
        parcels,
        key=lambda p: (p["deadline"], -p["priority"])
    )
    return sorted_parcels


def print_sorted_parcels(parcels: List[Dict[str, Any]]) -> None:
    """Pretty-print sorted parcels for demonstration."""
    print("\n=== Sorted Parcels (by Deadline ↑, Priority ↓) ===")
    print(f"{'ID':<8} {'Weight':<8} {'Value':<8} {'Priority':<10} {'Deadline':<10} {'Destination'}")
    print("-" * 65)
    for p in parcels:
        print(f"{p['id']:<8} {p['weight']:<8} {p['value']:<8} "
              f"{p['priority']:<10} {p['deadline']:<10} {p['destination']}")
