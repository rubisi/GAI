from src import load_config, load_graph_data, add_nodes, modify_nodes, add_edges, delete_edges, plot_graph, save_metadata

# Main function
def inject_anomalies(config_path):
    config = load_config(config_path)
    dataset_name = config["dataset"]
    graph_data = load_graph_data(dataset_name)
    plot_graph(graph_data, "Graph before injection")

    # Inject node anomalies
    node_metadata = []  # to store information about anomalous nodes

    # Inject node anomalies based on the config
    for anomaly in config["anomalies"].get("nodes",
                                           []):  # Loop through each node anomaly spec in the configuration if it exists
        if anomaly["method"] == "add":
            graph, new_nodes = add_nodes(graph_data, anomaly["num_nodes"])

            # Error handling
            if graph is None or graph.feature is None:
                print("Error: Graph or graph.feature is None!")
            else:
                # add metadata about the newly added nodes to the node_metadata list
                node_metadata.extend(
                    [{"node_id": n, "method": "added"} for n in
                     range(len(graph.feature) - new_nodes, len(graph.feature))])

        elif anomaly["method"] == "modify":
            graph, modified_nodes = modify_nodes(graph_data, anomaly["num_nodes"])
            node_metadata.extend(
                [{"node_id": n, "method": "modified"} for n in modified_nodes])
    print("Anomalous Nodes Metadata:", node_metadata)

    # Inject edge anomalies
    edge_metadata = []
    for anomaly in config["anomalies"].get("edges",
                                           []):  # Loop through each edge anomaly spec in the configuration if it exists
        if anomaly["method"] == "add":
            graph, new_edges = add_edges(graph_data, anomaly["num_edges"])
            edge_metadata.extend([{"edge_id": e, "type": "added"} for e in new_edges])

        elif anomaly["method"] == "delete":
            graph, deleted_edges = delete_edges(graph_data, anomaly["num_edges"])
            edge_metadata.extend([{"edge_id": e, "type": "deleted"} for e in deleted_edges])

    # Get the format for saving (CSV or JSON)
    file_format = config["metadata"]["file_format"]
    metadata_path = config["metadata"]["location"]

    # Save node and edge metadata
    save_metadata(node_metadata, edge_metadata,
                  f"{metadata_path}/injected_nodes.{file_format}", f"{metadata_path}/injected_edges.{file_format}",
                  file_format)

    plot_graph(graph_data, "Graph after injection")