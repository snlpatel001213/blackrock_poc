import json
import os
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

def read_triplets_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)['output']
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON content in {file_path}: {e}")
            return []

def process_directory(directory):
    all_triplets = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            triplets = read_triplets_from_file(file_path)
            all_triplets.extend(triplets)
#             print(all_triplets)
    return all_triplets


def create_kg_and_mappings(triplets):
    G = nx.MultiDiGraph()
    entity_to_id = {}
    relation_to_id = {}
    entity_id = 0
    relation_id = 0

    for triplet in triplets:
        if len(triplet) == 5:
            head, head_type, relation, tail, tail_type = triplet
            if head not in entity_to_id:
                entity_to_id[head] = entity_id
                G.add_node(entity_id, label=head, type=head_type)
                entity_id += 1
            if tail not in entity_to_id:
                entity_to_id[tail] = entity_id
                G.add_node(entity_id, label=tail, type=tail_type)
                entity_id += 1
            if relation not in relation_to_id:
                relation_to_id[relation] = relation_id
                relation_id += 1
            G.add_edge(entity_to_id[head], entity_to_id[tail], label=relation)
        else:
            print(f"Skipping triplet due to unexpected format: {triplet}")

    return G, entity_to_id, relation_to_id

def convert_triplets_to_id_mappings(triplets, entity_to_id, relation_to_id):
    kg_data = []
    for triplet in triplets:
        if len(triplet) == 5:
            head, head_type, relation, tail, tail_type = triplet
            head_id = entity_to_id.get(head)
            relation_id = relation_to_id.get(relation)
            tail_id = entity_to_id.get(tail)
            if head_id is not None and relation_id is not None and tail_id is not None:
                kg_data.append((head_id, relation_id, tail_id))
        else:
            print(f"Skipping triplet due to unexpected format: {triplet}")
    return kg_data

def save_mapping_to_file(mapping, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in sorted(mapping.items(), key=lambda item: item[1]):
            # Check if the key is a tuple and unpack accordingly
            if isinstance(item[0], tuple):
                (key, key_type), value = item
                file.write(f"{key}\t{key_type}\t{value}\n")
            else:
                # Handle the case where the key is not a tuple
                key, value = item
                file.write(f"{key}\t{value}\n")
def save_graph_to_file(G, entity_to_id, relation_to_id, file_path):
    """
    Save the Knowledge Graph to a file with entity names and relation names.
    
    Parameters:
    - G: The Knowledge Graph (networkx graph).
    - entity_to_id: A dictionary mapping entity names to IDs.
    - relation_to_id: A dictionary mapping relation names to IDs.
    - file_path: Path to the output file.
    """
    id_to_entity = {v: k for k, v in entity_to_id.items()}
    id_to_relation = {v: k for k, v in relation_to_id.items()}
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for source, target, data in G.edges(data=True):
            source_name = id_to_entity.get(source, "Unknown Entity")
            target_name = id_to_entity.get(target, "Unknown Entity")
            # Debugging line to identify missing relations
            if data['label'] not in id_to_relation:
                print(f"Missing relation ID: {data['label']}")
            relation_name = id_to_relation.get(data['label'], "Unknown Relation")
            f.write(f"{source_name}\t{relation_name}\t{target_name}\n")

def visualize_and_save_kg(G, output_filename='kg_visualization.png'):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.5)  # k regulates the distance between nodes
     # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    
    # Select one edge per (source, target) for labeling
    unique_edges = set((source, target) for source, target, data in G.edges(data=True))
    edge_labels = {(source, target): G.get_edge_data(source, target)[0]['label'] for source, target in unique_edges}
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.axis('off')
    plt.savefig(output_filename)
    plt.close()
# def visualize_and_save_kg(G, entity_to_id, output_filename, top_n=200):
#     # Get top_n entities based on degree
#     top_entities = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:top_n]
#     top_entities_ids = [entity_id for entity_id, _ in top_entities]

#     # Create subgraph for top entities
#     H = G.subgraph(top_entities_ids)

#     # Get top_n relations based on edge count
#     edge_counts = Counter(H.edges())
#     top_relations = [edge for edge, count in edge_counts.most_common(top_n)]

#     # Create subgraph for top relations
#     H = H.edge_subgraph(top_relations)

#     plt.figure(figsize=(12, 12))
#     pos = nx.spring_layout(H, k=0.5)
#     labels = {node_id: node for node, node_id in entity_to_id.items() if node_id in H.nodes()}
#     nx.draw(H, pos, labels=labels, with_labels=True, node_size=50, font_size=8)
#     plt.axis('off')
#     plt.savefig(output_filename)
#     plt.close()
    
def save_kg_to_file(kg_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for head_id, relation_id, tail_id in kg_data:
            file.write(f"{head_id}\t{relation_id}\t{tail_id}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON files to create KG, entity, and relation mappings.")
    parser.add_argument("directory", help="Directory containing JSON files")
    parser.add_argument("entity_output_file", help="File path for the output entity2id.txt")
    parser.add_argument("relation_output_file", help="File path for the output relation2id.txt")
    parser.add_argument("kg_id_output_file", help="File path for the output KG file with entity IDs and relation IDs")
    parser.add_argument("kg_name_output_file", help="File path for the output graph file with original entity names")
    parser.add_argument("output_file", help="File path for the output KG visualization (PNG format)")
    args = parser.parse_args()

    triplets = process_directory(args.directory)
    G, entity_to_id, relation_to_id = create_kg_and_mappings(triplets)

    save_mapping_to_file(entity_to_id, args.entity_output_file)
    save_mapping_to_file(relation_to_id, args.relation_output_file)
    # Convert triplets to KG data
    kg_data = convert_triplets_to_id_mappings(triplets, entity_to_id, relation_to_id)
     # Save KG data to file
    save_kg_to_file(kg_data, args.kg_id_output_file)
    save_graph_to_file(G, entity_to_id, relation_to_id, args.kg_name_output_file)
    visualize_and_save_kg(G,args.output_file)

    print(f"KG created with {len(G.nodes)} entities and {len(G.edges)} relations.")
    print(f"Entity mappings have been saved to {args.entity_output_file}")
    print(f"Relation mappings have been saved to {args.relation_output_file}")
    print(f"KG file with /entity IDs and relation IDs has been saved to {args.kg_id_output_file}")
    print(f"Graph file with original entity names has been saved to {args.kg_name_output_file}")
    print(f"KG visualization saved to {args.output_file}")
