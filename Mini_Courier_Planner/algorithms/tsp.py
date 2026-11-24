"""
Phase 3 - Nearest Neighbor TSP Approximation
Builds a delivery route that visits each required location exactly once
and returns to the depot (approximation of the Travelling Salesman Problem).
"""

from typing import Dict, List, Tuple, Any
from algorithms.dijkstra import dijkstra


def build_distance_matrix(graph: Dict[str, List[Tuple[str, int]]], nodes: List[str]) -> Dict[Tuple[str, str], int]:
    """
    Pre-compute shortest-path distances between every pair of nodes
    using Dijkstra (needed when the graph is not complete).
    """
    dist_matrix = {}
    for src in nodes:
        distances, _ = dijkstra(graph, src)
        for dst in nodes:
            dist_matrix[(src, dst)] = distances.get(dst, float("inf"))
    return dist_matrix


def nearest_neighbor_tsp(
    graph: Dict[str, List[Tuple[str, int]]],
    locations: List[str],
    start: str = "Depot"
) -> Tuple[List[str], int]:
    """
    Nearest-Neighbor heuristic for TSP.

    Args:
        graph      : full road network (adjacency list)
        locations  : list of unique destinations that must be visited
        start      : starting / ending depot

    Returns:
        route      : ordered list of locations (including start at both ends)
        total_cost : total distance of the approximate tour
    """
    if not locations:
        return [start, start], 0

    # Ensure start is present
    nodes = list(set(locations + [start]))
    dist_matrix = build_distance_matrix(graph, nodes)

    unvisited = set(locations)
    route = [start]
    current = start
    total_cost = 0

    while unvisited:
        # Find nearest unvisited neighbor
        nearest = None
        min_dist = float("inf")
        for candidate in unvisited:
            d = dist_matrix.get((current, candidate), float("inf"))
            if d < min_dist:
                min_dist = d
                nearest = candidate

        if nearest is None or min_dist == float("inf"):
            break  # disconnected

        route.append(nearest)
        total_cost += min_dist
        unvisited.remove(nearest)
        current = nearest

    # Return to depot
    return_dist = dist_matrix.get((current, start), float("inf"))
    if return_dist != float("inf"):
        total_cost += return_dist
    route.append(start)

    return route, total_cost


def print_route(route: List[str], total_cost: int) -> None:
    """Pretty-print the final delivery route."""
    print("\n=== Final Delivery Route (Nearest-Neighbor TSP) ===")
    print("Route : " + " → ".join(route))
    print(f"Total Distance : {total_cost}")
