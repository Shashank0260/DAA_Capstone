# Phase 1 – Courier Problem Design and Planning

## 1. Problem Abstraction

We model a single courier vehicle that starts at a central **Depot**, must pick a subset of parcels that fit within its weight capacity, and then deliver them to their respective destinations, returning to the Depot at the end of the trip.

### Decision Variables
- Which parcels to load (0/1 selection)
- In which order to visit the destinations

### Constraints
- Total weight ≤ Vehicle Capacity
- Every selected destination must be visited exactly once (TSP constraint)
- Non-negative travel costs

### Objective
Maximise total parcel value while minimising (or approximating) total travel distance.

## 2. Data Design

### Parcel Schema
```json
{
  "id": "P001",
  "weight": 4,
  "value": 40,
  "priority": 8,
  "deadline": 2,
  "destination": "A"
}
```

### Graph Schema (Adjacency List)
```json
{
  "Depot": [["A", 5], ["B", 8], ...],
  "A": [["Depot", 5], ["B", 4], ...]
}
```

Undirected edges are stored in both directions for convenience.

## 3. Algorithm Selection Rationale

| Sub-problem              | Algorithm                  | Why chosen?                                      |
|--------------------------|----------------------------|--------------------------------------------------|
| Prioritisation           | Timsort (stable)           | O(n log n), stable, handles multi-key sorting easily |
| Capacity-constrained selection | 0/1 Knapsack DP       | Exact optimal, classic CO mapping, easy to show DP table |
| Single-source shortest path | Dijkstra + binary heap | Exact, works with non-negative weights, standard textbook algorithm |
| Multi-destination route  | Nearest-Neighbor TSP       | Simple O(n²) approximation, easy to implement & explain in viva |

## 4. Integration Logic

1. Sort all parcels → early deadlines and high priority appear first (helps human inspection and can be used as a secondary heuristic).
2. Feed sorted list into Knapsack DP → obtain optimal subset under capacity.
3. Extract unique destinations of the selected subset.
4. Run Dijkstra from Depot to obtain distance matrix (or on-demand).
5. Apply Nearest-Neighbor starting from Depot to produce a feasible tour.
6. Record wall-clock time of each stage for Phase 4 analysis.

## 5. Assumptions & Scope

- Vehicle makes only one trip (no multi-trip scheduling).
- All parcels are available at the Depot at time 0.
- Graph is connected and has non-negative edge weights.
- Number of unique delivery points is small (≤ 15) so that NN-TSP is practical.
- Time windows are simplified to a single deadline value used only for prioritisation (not hard constraints).

## 6. Future Extensions (mentioned in Phase 4)

- Soft time windows
- Multiple vehicles (VRP)
- Real-time traffic updates
- Exact TSP solvers (Held-Karp) for tiny instances
- 2-opt / 3-opt improvement after nearest-neighbor
