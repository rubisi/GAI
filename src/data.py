""" Load graph dataset"""
from torch_geometric.datasets import Planetoid

# Load graph dataset
def load_graph_data(dataset_name):
    dataset = Planetoid(root="./data", name=dataset_name)
    return dataset[0]