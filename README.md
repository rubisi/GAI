# GAI

This repository contains a simple framework for injecting anomalies into graph datasets. 

## Running the Project

To run the anomaly injection process, execute the `inject_anomalies.py` file. This script will read the configuration from the `config.yaml` file and apply the specified anomalies to the dataset.

### Config File
The configuration file (config.yaml) allows you to customize the anomaly injection process. Here’s an example of what the file might look like:
```
dataset: CORA  # Name of the graph dataset

anomalies:
  nodes:
    - method: add  # Add new anomalous nodes
      num_nodes: 10  # Number of new nodes to add

    - method: modify  # Modify existing nodes
      num_nodes: 15  # Number of nodes to modify


  edges:
    - method: add  # Add new edges
      num_edges: 20  # Number of new edges to add

    - method: delete  # Delete edges
      num_edges: 10  # Number of edges to del

metadata:
  file_format: "csv"  # Supported formats: "csv", "json"
  location: "./metadata/"  # folder to save metadata
```




Feel free to update the config file according to your requirements to control the methods and numbers of anomalies injected.
