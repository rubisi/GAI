"""Define functions for injecting anomalies"""
import torch
from torch_geometric.utils import from_networkx, to_networkx
import random


# Add new nodes to existing graph, and assign random features
def add_nodes(graph_data, num_nodes):
    # Print the number of nodes before the addition
    print(f"Total number of nodes before addition: {graph_data.num_nodes}")

    graph_nx = to_networkx(graph_data, to_undirected=True)  # transform pyG data object to NetworkX first
    num_features = graph_data.x.shape[1]  # get number of features per node

    # Add the new nodes with the correct attributes
    for i in range(num_nodes):
        # Add a new node with the 'feature' attribute
        feature = torch.randn(num_features)  # Generate a tensor with random features
        graph_nx.add_node(len(graph_nx.nodes), feature=feature)

    # Ensure all existing nodes have the 'feature' attribute (in case some are missing)
    for node in graph_nx.nodes():
        if 'feature' not in graph_nx.nodes[node]:
            graph_nx.nodes[node]['feature'] = torch.randn(num_features)

    # Convert NetworkX graph to PyTorch Geometric format
    pyg_graph = from_networkx(graph_nx)
    # Print total number of nodes after the addition
    print(f"Total number of nodes after addition: {pyg_graph.num_nodes}")
    return pyg_graph, num_nodes

# Modify existing node features
def modify_nodes(graph_data, num_nodes):
    graph_nx = to_networkx(graph_data, to_undirected=True)  # Convert PyG to NetworkX

    # Check if graph_data.x exists (to avoid AttributeError)
    if not hasattr(graph_data, 'x'):
        raise ValueError("Error: graph_data has no attribute 'x' (node features missing).") # node features are needed here since this func modifies the features

    # (manually) assign node features from PyG to NetworkX // fix for feature key not existing in graph_nx.nodes[node]["feature"]
    for i, feat in enumerate(graph_data.x):
        graph_nx.nodes[i]["feature"] = feat.clone()

    # Select random nodes to modify
    nodes = list(graph_nx.nodes)
    selected_nodes = random.sample(nodes, min(num_nodes, len(nodes))) #select num_nodes random nodes from the graph

    for node in selected_nodes:
        if "feature" in graph_nx.nodes[node]:  # Ensure feature exists
            graph_nx.nodes[node]["feature"] += torch.randn_like(graph_nx.nodes[node]["feature"])
        else:
            print(f"Warning: Node {node} has no 'feature' attribute!")

    return from_networkx(graph_nx), selected_nodes  # transform back to PyG // selected_nodes are the modified nodes


# Add random edges
def add_edges(graph_data, num_edges):

    # Print the number of edges before the addition
    print(f"Total number of edges before addition: {graph_data.num_edges}")

    graph_nx = to_networkx(graph_data, to_undirected=True) # transform pyG data object to NetworkX first
    nodes = list(graph_nx.nodes) #get list of nodes (to randomly select nodes later)
    new_edges = []
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2) #randomly select two distinct nodes
        if not graph_nx.has_edge(u, v): # make sure the edge does not already exist
            graph_nx.add_edge(u, v) # add the new edge to the NetworkX graph
            new_edges.append((u, v)) #store the added edge to the list

    # transform NetworkX graph to PyTorch Geometric format
    pyg_graph = from_networkx(graph_nx)
    # Print total number of nodes after the addition
    print(f"Total number of nodes after addition: {pyg_graph.num_edges}") # For undirected graphs, this will return the number of bi-directional edges, which is double the amount of unique edges
    return pyg_graph, new_edges

# Delete random edges
def delete_edges(graph_data, num_edges):
    # Print the number of edges before the deletion
    print(f"Total number of edges before deletion: {graph_data.num_edges}")
    graph_nx = to_networkx(graph_data, to_undirected=True)
    edges = list(graph_nx.edges) # get a list of all edges

    deleted_edges = random.sample(edges, min(num_edges, len(edges))) #randomly select num_edges of edges for deletion
    graph_nx.remove_edges_from(deleted_edges)

    # transform NetworkX graph to PyTorch Geometric format
    pyg_graph = from_networkx(graph_nx)

    # Print the number of edges before the deletion
    print(f"Total number of edges after deletion: {pyg_graph.num_edges}") # For undirected graphs, this will return the number of bi-directional edges, which is double the amount of unique edges
    return pyg_graph, deleted_edges