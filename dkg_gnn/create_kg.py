import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import json

def load_triplets_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        triplets_json = file.read()
        triplets = json.loads(triplets_json)
    return triplets

def create_graph(triplets):
    G = nx.MultiDiGraph()
    for h, h_type, r, o, o_type in triplets:
        G.add_node(h, title=h_type)
        G.add_node(o, title=o_type)
        G.add_edge(h, o, title=r)
    return G

def visualize_graph_networkx(G):
    # ... (same as before)

def visualize_graph_pyvis(G, output_filename='knowledge_graph.html'):
    # ... (same as before)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a knowledge graph from triplets.")
    parser.add_argument("triplets_file", help="Text file containing the triplets in JSON format")
    args = parser.parse_args()

    # Load triplets from the provided file
    triplets = load_triplets_from_file(args.triplets_file)

    # Create the graph
    G = create_graph(triplets)

    # Visualize using NetworkX and Matplotlib
    visualize_graph_networkx(G)

    # Visualize using PyVis (Interactive HTML)
    visualize_graph_pyvis(G)
