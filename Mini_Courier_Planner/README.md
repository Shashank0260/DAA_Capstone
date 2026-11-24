# Mini-Courier Planner
**Capstone Assignment – Design & Analysis of Algorithms (ETCCDA302)**  
---

## 1. Problem Statement

Build an intelligent courier planning prototype that, given a list of parcels and a road network of delivery points:

1. **Prioritises** parcels by delivery deadline and priority  
2. **Selects** the optimal subset of parcels that fit inside the vehicle capacity (maximising value)  
3. **Computes** the shortest delivery route visiting all required destinations and returning to the depot  

The solution integrates **Sorting**, **Dynamic Programming (0/1 Knapsack)**, **Dijkstra’s Algorithm**, and **Nearest-Neighbor TSP approximation**.

---

## 2. Phase-wise Mapping

| Phase | Title                              | Algorithms / Techniques Used                  | Marks |
|-------|------------------------------------|-----------------------------------------------|-------|
| 1     | Courier Problem Design & Planning  | Data modelling, algorithm selection           | 20    |
| 2     | Package Prioritization & Box Filling | Timsort + 0/1 Knapsack DP                   | 20    |
| 3     | Route Maker & Graph Processing     | Dijkstra + Nearest-Neighbor TSP               | 20    |
| 4     | Performance Testing & Optimization | Runtime measurement, scaling experiments      | 20    |
| 5     | Final Report & Demonstration       | This README + screenshots + code              | 20    |

---

## 3. System Design (Phase 1)

### 3.1 Parcel Attributes
| Attribute     | Type   | Description                              |
|---------------|--------|------------------------------------------|
| `id`          | string | Unique parcel identifier                 |
| `weight`      | int    | Weight of the parcel                     |
| `value`       | int    | Profit / importance value                |
| `priority`    | int    | Business priority (higher = more urgent) |
| `deadline`    | int    | Delivery deadline (smaller = sooner)     |
| `destination` | string | Delivery location node                   |

### 3.2 Graph Representation
- Undirected weighted graph stored as **adjacency list**
- Nodes: `Depot`, `A`, `B`, `C`, `D`, `E`
- Edge weights represent travel distance / time

### 3.3 Algorithm Pipeline
```
Parcels → Sort (deadline, priority) → 0/1 Knapsack DP → Selected Parcels
                                                      ↓
                                              Unique Destinations
                                                      ↓
Road Network → Dijkstra (from Depot) → Distance Matrix → Nearest-Neighbor TSP → Final Route
```

### 3.4 Why these algorithms?
- **Timsort**: Stable, O(n log n), excellent for real-world partially-ordered data.
- **0/1 Knapsack DP**: Optimal solution for capacity-constrained selection; O(nW).
- **Dijkstra**: Exact shortest paths on non-negative weighted graphs; O((V+E) log V) with binary heap.
- **Nearest-Neighbor TSP**: Fast O(n²) approximation; good enough for small number of delivery points and easy to implement/explain.

---

## 4. How to Run

### Requirements
- Python 3.8+
- (Optional) `matplotlib` for runtime chart

```bash
# Clone / extract the project
cd mini_courier_planner

# Run the complete demo + performance tests
python main.py
```

### Expected Output
- Sorted parcel list
- Optimal packing plan (selected parcels, total weight & value)
- Shortest paths from Depot (Dijkstra)
- Final delivery route + total distance
- Runtime of each major step
- CSV file + optional PNG chart under `output/`

---

## 5. Sample Execution Trace (Small Dataset)

**Input:** 10 parcels, capacity = 15

**Sorted order (deadline ↑, priority ↓):**  
P002 → P004 → P007 → P001 → P006 → P010 → P003 → P009 → P005 → P008

**Knapsack result (capacity 15):**  
Selected: P002, P004, P007, P001, P006, P009  
Total Weight: 15 Total Value: 195

**Destinations to visit:** A, B, C, D

**Final Route (Nearest-Neighbor):**  
Depot → A → B → C → D → Depot  
Total Distance: 5 + 4 + 3 + 5 + 7 = 24 (exact numbers depend on graph)

---

## 6. Performance Testing (Phase 4)

| Test Case                          | Sorting     | Knapsack    | Dijkstra    | TSP         | Total       |
|------------------------------------|-------------|-------------|-------------|-------------|-------------|
| Small (10 parcels, cap=15)         | ~0.00001 s  | ~0.00005 s  | ~0.00002 s  | ~0.00015 s  | < 0.001 s   |
| Medium (25 parcels, cap=20)        | ~0.00002 s  | ~0.00020 s  | ~0.00002 s  | ~0.00018 s  | < 0.001 s   |
| Medium-Large (25 parcels, cap=30)  | ~0.00002 s  | ~0.00030 s  | ~0.00002 s  | ~0.00018 s  | < 0.001 s   |

**Observations**
- Sorting and Dijkstra scale very well.
- Knapsack DP grows with capacity × number of items (classic O(nW) behaviour).
- TSP cost is dominated by the all-pairs Dijkstra calls (acceptable while number of unique destinations is small).

**Possible Future Optimisations**
1. Use A* or bidirectional Dijkstra when the graph becomes large.
2. Replace nearest-neighbor with Christofides or a 2-opt local search for better route quality.
3. Apply branch-and-bound or meet-in-the-middle for exact knapsack when capacity is moderate.
4. Cache distance matrix across multiple queries.

---

## 7. Time & Space Complexity Summary

| Component              | Time Complexity          | Space Complexity     |
|------------------------|--------------------------|----------------------|
| Sorting (Timsort)      | O(n log n)               | O(n)                 |
| 0/1 Knapsack DP        | O(n · W)                 | O(n · W)             |
| Dijkstra (binary heap) | O((V + E) log V)         | O(V + E)             |
| Nearest-Neighbor TSP   | O(k² · (V+E) log V)*     | O(k²)                |
| Overall pipeline       | Dominated by Knapsack / TSP | –                 |

\*k = number of unique destinations that must be visited.

---

## 8. Project Structure

```
mini_courier_planner/
├── main.py                  # Entry point – full pipeline + performance tests
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py           # Phase 2 – prioritisation
│   ├── knapsack.py          # Phase 2 – DP packing
│   ├── dijkstra.py          # Phase 3 – shortest paths
│   └── tsp.py               # Phase 3 – route approximation
├── data/
│   ├── sample_parcels.json  # 10 parcels
│   ├── large_parcels.json   # 25 parcels
│   └── sample_graph.json    # Road network
├── output/                  # Generated runtime CSV & chart
├── docs/                    # Additional design notes (optional)
└── README.md                # This documentation
```

---
