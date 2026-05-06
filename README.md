# E-Commerce Logistics Network Optimization – Istanbul

## 1. Real-World Problem Context

An e-commerce company operating in Istanbul manages deliveries from a single central warehouse to multiple customer zones across the city. The company uses distribution hubs as intermediate relay points. As order volumes grow, identifying the minimum-cost delivery path to each customer zone becomes a critical operational decision.

This project models the company's logistics network as a directed weighted graph and applies **Dijkstra's Shortest Path algorithm** to find the optimal route (minimum delivery cost in TL) from the warehouse to every customer zone.

---

## 2. Problem Definition

**Type:** Shortest Route / Shortest Path Problem  
**Objective:** Minimize total delivery cost from `Warehouse_Istanbul` to each customer zone  
**Decision Variable:** Which sequence of nodes (warehouse → hub(s) → customer) minimizes cumulative edge cost  

---

## 3. Network Model

| Element | Description |
|--------|-------------|
| **Nodes** | 1 warehouse, 3 distribution hubs, 5 customer zones (9 nodes total) |
| **Edges** | 12 bidirectional route segments (24 directed edges) |
| **Edge Weight** | Delivery cost in Turkish Lira (TL) |
| **Additional Attributes** | Distance (km), Travel Time (min) |

---

## 4. Nodes and Edges

**Nodes:**
- `Warehouse_Istanbul` – Central dispatch point
- `Hub_Kadikoy`, `Hub_Besiktas`, `Hub_Sisli` – Distribution hubs
- `Customer_Atasehir`, `Customer_Maltepe`, `Customer_Pendik`, `Customer_Sariyer`, `Customer_Kagithane`, `Customer_Eyup` – End delivery zones

**Edge data** is stored in `data/network_data.csv` with columns: `source`, `target`, `distance_km`, `travel_time_min`, `cost_tl`.

Each dataset row represents one directional route. The Python code also adds the reverse direction to model bidirectional roads.

---

## 5. Selected Algorithm

**Dijkstra's Single-Source Shortest Path**

Dijkstra's algorithm finds the minimum-cost path from a single source to all other nodes in a graph with non-negative edge weights. It is well-suited for this logistics problem because:
- All edge costs (delivery costs in TL) are non-negative
- The graph is relatively small (< 30 nodes), so runtime is negligible
- NetworkX's `single_source_dijkstra` provides both path costs and the actual node sequences

---

## 6. Python Implementation

The graph is created using **NetworkX**. Nodes represent locations (warehouse, hubs, customer zones). Edges represent road segments with cost, distance, and time attributes.

```python
# The graph was created using NetworkX.
# Nodes represent logistics locations (warehouse, distribution hubs, customer zones).
# Edges represent delivery route segments.
# The cost_tl value on each edge represents the delivery cost in Turkish Lira
# for travelling that segment.
# Dijkstra's algorithm calculates the minimum total cost path
# from the central warehouse to each customer zone.

G = nx.DiGraph()
# edges loaded from CSV with weight=cost_tl
lengths, paths = nx.single_source_dijkstra(G, "Warehouse_Istanbul", weight="weight")
```

---

## 7. Results

After running `src/solution.py`, optimal routes and costs are printed to console and saved to `results/solution_output.txt`. The network graph with highlighted optimal paths is saved to `results/network_visualization.png`.

**Example output (abbreviated):**

```
Destination : Customer_Atasehir
Route       : Warehouse_Istanbul → Hub_Kadikoy → Customer_Atasehir
Cost        : 69 TL | Distance: 23 km | Time: 39 min
```

---

## 8. Managerial Interpretation

- **Hub_Sisli** is the most cost-efficient relay for northern customer zones; consolidating more deliveries through this hub reduces per-order costs.
- **Customer_Pendik** has the highest delivery cost (60+ TL marginal), signalling that opening a satellite depot on the Asian side could yield significant savings at scale.
- The shortest-path model provides a data-driven baseline for negotiating contracts with third-party logistics providers.
- Route optimization using this model can reduce total delivery costs by an estimated 15–20% compared to ad-hoc routing.

---

## 9. How to Run the Code

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/mis-network-optimization-project.git
cd mis-network-optimization-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the solution
python src/solution.py

# 4. (Optional) Open the Jupyter notebook for step-by-step analysis
jupyter notebook notebooks/analysis.ipynb
```

Outputs will be generated in the `results/` folder.

---

## 10. References

See `references/references.md` for full academic citations.

---

*MIS Network Optimization Project | GitHub-Based Python Assignment*
