"""
E-Commerce Logistics Network Optimization
MIS Network Optimization Project
Algorithm: Shortest Path (Dijkstra)
Problem: Finding the optimal delivery routes from a warehouse
         in Istanbul to customer zones with minimum cost.
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── 1. Load Data ─────────────────────────────────────────────────────────────

def load_network(csv_path: str) -> nx.DiGraph:
    """
    Load the logistics network from a CSV file.
    Each row represents a directed edge (route) between two locations.
    Edge weight is set to 'cost_tl' which represents the delivery cost
    in Turkish Lira for that route segment.
    """
    df = pd.read_csv(csv_path)
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row["source"],
            row["target"],
            weight=row["cost_tl"],          # primary weight for shortest path
            distance_km=row["distance_km"],
            travel_time_min=row["travel_time_min"],
            cost_tl=row["cost_tl"],
        )
        # Add reverse edge (bidirectional roads)
        G.add_edge(
            row["target"],
            row["source"],
            weight=row["cost_tl"],
            distance_km=row["distance_km"],
            travel_time_min=row["travel_time_min"],
            cost_tl=row["cost_tl"],
        )

    print(f"[INFO] Network loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G, df


# ── 2. Shortest Path Analysis ─────────────────────────────────────────────────

def find_all_shortest_paths(G: nx.DiGraph, source: str) -> dict:
    """
    Use Dijkstra's algorithm to find the shortest (minimum cost) path
    from the source warehouse to every reachable node.

    NetworkX's single_source_dijkstra returns:
      - lengths : dict of {node: total_cost}
      - paths   : dict of {node: [node_list]}
    """
    lengths, paths = nx.single_source_dijkstra(G, source, weight="weight")
    return lengths, paths


def print_results(source: str, lengths: dict, paths: dict, G: nx.DiGraph):
    """Print a formatted summary of optimal delivery routes."""
    customer_nodes = [n for n in G.nodes if n.startswith("Customer_")]

    print("\n" + "=" * 60)
    print(f"  OPTIMAL DELIVERY ROUTES FROM: {source}")
    print("=" * 60)

    total_cost = 0
    for customer in sorted(customer_nodes):
        if customer in paths:
            path = paths[customer]
            cost = lengths[customer]
            total_cost += cost

            # Compute total distance and time along the path
            dist = sum(
                G[path[i]][path[i + 1]].get("distance_km", 0)
                for i in range(len(path) - 1)
            )
            time = sum(
                G[path[i]][path[i + 1]].get("travel_time_min", 0)
                for i in range(len(path) - 1)
            )

            print(f"\n  Destination : {customer}")
            print(f"  Route       : {' → '.join(path)}")
            print(f"  Cost        : {cost} TL")
            print(f"  Distance    : {dist} km")
            print(f"  Travel Time : {time} min")

    print("\n" + "-" * 60)
    print(f"  Total delivery cost to all customers: {total_cost} TL")
    print("=" * 60 + "\n")
    return total_cost


# ── 3. Network Visualization ──────────────────────────────────────────────────

def visualize_network(G: nx.DiGraph, paths: dict, source: str, output_path: str):
    """
    Draw the logistics network.
    - Warehouse node: red
    - Hub nodes     : orange
    - Customer nodes: green
    - Optimal paths : highlighted in blue
    """
    # Collect all edges that belong to at least one optimal path
    optimal_edges = set()
    for path in paths.values():
        for i in range(len(path) - 1):
            optimal_edges.add((path[i], path[i + 1]))

    # Node colors
    node_colors = []
    for node in G.nodes:
        if node == source:
            node_colors.append("#e74c3c")       # red  – warehouse
        elif node.startswith("Hub_"):
            node_colors.append("#f39c12")       # orange – hub
        else:
            node_colors.append("#27ae60")       # green  – customer

    # Edge colors
    edge_colors = [
        "#2980b9" if (u, v) in optimal_edges else "#bdc3c7"
        for u, v in G.edges()
    ]
    edge_widths = [
        3.0 if (u, v) in optimal_edges else 1.0
        for u, v in G.edges()
    ]

    # Layout
    pos = nx.spring_layout(G, seed=42, k=2.5)

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor("#f8f9fa")
    ax.set_facecolor("#f8f9fa")

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1200, ax=ax, alpha=0.95)
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=edge_widths,
        ax=ax,
        arrows=True,
        arrowsize=15,
        connectionstyle="arc3,rad=0.1",
    )

    # Edge labels – show cost in TL
    edge_labels = {(u, v): f"{d['cost_tl']}₺" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, ax=ax)

    # Legend
    legend_handles = [
        mpatches.Patch(color="#e74c3c", label="Warehouse"),
        mpatches.Patch(color="#f39c12", label="Distribution Hub"),
        mpatches.Patch(color="#27ae60", label="Customer Zone"),
        mpatches.Patch(color="#2980b9", label="Optimal Route"),
        mpatches.Patch(color="#bdc3c7", label="Alternative Route"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", fontsize=9)
    ax.set_title(
        "E-Commerce Logistics Network – Shortest Path Optimization (Istanbul)",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Network visualization saved → {output_path}")


# ── 4. Save Text Output ───────────────────────────────────────────────────────

def save_solution_output(source: str, lengths: dict, paths: dict, G: nx.DiGraph, output_path: str):
    """Write the solution summary to a plain-text file."""
    customer_nodes = [n for n in G.nodes if n.startswith("Customer_")]
    lines = []
    lines.append("=" * 60)
    lines.append(f"OPTIMAL DELIVERY ROUTES FROM: {source}")
    lines.append("=" * 60)

    total_cost = 0
    for customer in sorted(customer_nodes):
        if customer in paths:
            path = paths[customer]
            cost = lengths[customer]
            total_cost += cost
            dist = sum(G[path[i]][path[i + 1]].get("distance_km", 0) for i in range(len(path) - 1))
            time = sum(G[path[i]][path[i + 1]].get("travel_time_min", 0) for i in range(len(path) - 1))
            lines.append(f"\nDestination : {customer}")
            lines.append(f"Route       : {' -> '.join(path)}")
            lines.append(f"Cost        : {cost} TL")
            lines.append(f"Distance    : {dist} km")
            lines.append(f"Travel Time : {time} min")

    lines.append("\n" + "-" * 60)
    lines.append(f"Total delivery cost to all customers: {total_cost} TL")
    lines.append("=" * 60)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[INFO] Solution output saved → {output_path}")


# ── 5. Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSV_PATH  = os.path.join(BASE_DIR, "data", "network_data.csv")
    VIZ_PATH  = os.path.join(BASE_DIR, "results", "network_visualization.png")
    OUT_PATH  = os.path.join(BASE_DIR, "results", "solution_output.txt")

    os.makedirs(os.path.join(BASE_DIR, "results"), exist_ok=True)

    SOURCE = "Warehouse_Istanbul"

    # Step 1 – Load
    G, df = load_network(CSV_PATH)

    # Step 2 – Solve
    lengths, paths = find_all_shortest_paths(G, SOURCE)

    # Step 3 – Print
    print_results(SOURCE, lengths, paths, G)

    # Step 4 – Visualize
    visualize_network(G, paths, SOURCE, VIZ_PATH)

    # Step 5 – Save text output
    save_solution_output(SOURCE, lengths, paths, G, OUT_PATH)

    print("\n[DONE] All outputs generated successfully.")
