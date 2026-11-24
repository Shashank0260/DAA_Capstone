# Execution Steps – Mini-Courier Planner

## Quick Start

1. Open a terminal and navigate to the project folder:
   ```bash
   cd mini_courier_planner
   ```

2. Run the program:
   ```bash
   python main.py
   ```

3. Observe the console output:
   - Sorted parcels
   - Optimal packing plan
   - Dijkstra shortest paths
   - Final TSP route
   - Runtime of each component
   - Performance comparison on multiple dataset sizes

4. Check the `output/` folder for:
   - `runtime_comparison.csv` – data for charts
   - `runtime_chart.png` – visual comparison (if matplotlib is installed)

## Customising Input

- Edit `data/sample_parcels.json` or `data/large_parcels.json` to change parcels.
- Edit `data/sample_graph.json` to change the road network.
- Change `VEHICLE_CAPACITY` at the top of `main.py`.

## Running Only the Planner (no performance tests)

You can import and call the function from another script:

```python
from main import run_planner
result = run_planner(parcels_file="sample_parcels.json", capacity=15, verbose=True)
print(result["route"])
```
