"""Helper functions (save metadata, plot, etc.)"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from torch_geometric.utils import to_networkx
import json


# Plot graph
def plot_graph(graph_data, title):
    graph_nx = to_networkx(graph_data, to_undirected=True) # transform pyG data object to NetworkX first
    plt.figure(figsize=(8, 6))
    nx.draw(graph_nx, node_size=20, edge_color="gray")
    plt.title(title)
    plt.show()

def save_metadata(nodes, edges, path_nodes, path_edges, file_format):
    # Create separate DataFrames for nodes and edges
    node_df = pd.DataFrame(nodes)
    edge_df = pd.DataFrame(edges)

    # Save nodes and edges based on the format
    if file_format == "csv":
        # Save as CSV
        node_df.to_csv(path_nodes, index=False)
        edge_df.to_csv(path_edges, index=False)
    elif file_format == "json":
        # Save as JSON
        with open(path_nodes, 'w') as f_nodes:
            json.dump(nodes, f_nodes, indent=4)
        with open(path_edges, 'w') as f_edges:
            json.dump(edges, f_edges, indent=4)
    else:
        print(f"Error: Unsupported file format '{file_format}'")
