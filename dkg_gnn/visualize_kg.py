import os
import json,ast
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


# from jinja2 import Environment, FileSystemLoader, select_autoescape

# env = Environment(
#     loader=FileSystemLoader('.'),
#     autoescape=select_autoescape(['html', 'xml'])
# )

# template = env.get_template('my_template.html')

def load_mapping(file_path):
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                key, value = parts
                mapping[int(value)] = key  # Map ID to entity/relation
            else:
                print(f"Skipping line due to unexpected format: {line.strip()}")
    return mapping


def process_directory(directory, entity_mapping, relation_mapping):
    G = nx.MultiDiGraph()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming triplet files end with .txt
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = file.read()
                    # Parse the JSON content directly without converting to a Python literal
                    json_data = ast.literal_eval(json.dumps(data))
                    x = json_data.replace("'", '"')
                    parsed_data = json.loads(x)
                    for item in parsed_data:
                        if len(item) >= 5:
                            head, _, relation, tail, _ = item[:5]  # Focus on the first 5 elements
                            # Proceed with processing using head, relation, and tail
                            head_id = entity_mapping.get(head)
                            relation_id = relation_mapping.get(relation)
                            tail_id = entity_mapping.get(tail)
                            if head_id is not None and relation_id is not None and tail_id is not None:
                                G.add_edge(head_id, tail_id, label=relation_id)
                        else:
                            print(f"Skipping item due to unexpected format: {item}")
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON content in {filename}: {e}")
    return G

def draw_graph(G, entity_mapping, relation_mapping):
    pos = nx.spring_layout(G)
    labels = {node: entity_mapping[node] for node in G.nodes()}
    edge_labels = {(source, target): relation_mapping[data['label']] for source, target, data in G.edges(data=True)}
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
        # Remove axes and save the figure
    plt.axis('off')
    plt.savefig('kg_visualization.png', format='png', bbox_inches='tight')
    plt.close()

def visualize_graph_pyvis(G, entity_mapping, relation_mapping, output_filename='kg_visualization.html'):
    nt = Network('100%', '100%', directed=True)
    for node in G.nodes:
        nt.add_node(node, label=entity_mapping[node])
    for source, target, data in G.edges(data=True):
        nt.add_edge(source, target, label=relation_mapping[data['label']])
    nt.show(output_filename)
    plt.show()
        # Remove axes and save the figure
    plt.axis('off')
    plt.savefig('kg_visualization', format='png', bbox_inches='tight')
    plt.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize a Knowledge Graph from triplets.")
    parser.add_argument("directory", help="Directory containing triplet files")
    parser.add_argument("entity_file", help="File path for the entity2id mapping file")
    parser.add_argument("relation_file", help="File path for the relation2id mapping file")
    args = parser.parse_args()

    # Load mappings
    entity_mapping = load_mapping(args.entity_file)
    relation_mapping = load_mapping(args.relation_file)

    # Process all triplet files in the directory and create a graph
    G = process_directory(args.directory, entity_mapping, relation_mapping)

    # Draw the graph using matplotlib
    draw_graph(G, entity_mapping, relation_mapping)

    # Visualize the graph using PyVis (Interactive HTML)
#     visualize_graph_pyvis(G, entity_mapping, relation_mapping)
