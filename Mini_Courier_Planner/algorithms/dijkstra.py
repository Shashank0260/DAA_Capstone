"""
Phase 3 - Dijkstra's Shortest Path Module
Computes single-source shortest paths on a weighted undirected graph.
"""

import heapq
from typing import Dict, List, Tuple, Any


def dijkstra(graph: Dict[str, List[Tuple[str, int]]], source: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Dijkstra's algorithm using a binary heap (priority queue).

    Args:
        graph  : adjacency list {node: [(neighbor, weight), ...]}
        source : starting node

    Returns:
        distances : {node: shortest distance from source}
        previous  : {node: previous node in the path}  (for path reconstruction)
    """
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[source] = 0

    # Priority queue: (distance, node)
    pq = [(0, source)]

    while pq:
        current_dist, current = heapq.heappop(pq)

        # Skip outdated entries
        if current_dist > distances[current]:
            continue

        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous


def reconstruct_path(previous: Dict[str, str], source: str, target: str) -> List[str]:
    """Reconstruct the shortest path from source to target."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    if path and path[0] == source:
        return path
    return []  # no path exists


def print_shortest_paths(distances: Dict[str, int], previous: Dict[str, str], source: str) -> None:
    """Pretty-print all shortest paths from source."""
    print(f"\n=== Shortest Paths from '{source}' (Dijkstra) ===")
    print(f"{'Destination':<15} {'Distance':<12} {'Path'}")
    print("-" * 55)
    for node in sorted(distances.keys()):
        if node == source:
            continue
        path = reconstruct_path(previous, source, node)
        path_str = " → ".join(path) if path else "No path"
        dist = distances[node] if distances[node] != float("inf") else "∞"
        print(f"{node:<15} {str(dist):<12} {path_str}")
