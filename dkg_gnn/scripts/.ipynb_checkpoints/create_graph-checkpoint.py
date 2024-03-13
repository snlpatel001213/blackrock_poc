import json
import os, ast
import argparse
import networkx as nx

def read_triplets_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read().strip()
        print(file_content)

        # Check if the file content starts with '{' and ends with '}'.
        # If not, add 'output' key and braces to make it a dictionary string.
        if not file_content.startswith('{'):
            file_content = "{'output': " + file_content
        if not file_content.endswith('}'):
            file_content += '}'

        triplet_dict = ast.literal_eval(file_content)
    return triplet_dict



def process_directory(directory):
    all_triplets = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Adjust the extension as needed
            file_path = os.path.join(directory, filename)
            triplets = read_triplets_from_file(file_path)
            if triplets:  # Only extend if triplets is not empty
                print(triplets)
                all_triplets.extend(triplets)
    return all_triplets

def create_kg_and_mappings(triplets):
    G = nx.MultiDiGraph()
    entity_to_id = {}
    relation_to_id = {}
    entity_id = 0
    relation_id = 0

    for triplet in triplets:
        # Check if the triplet has at least 3 elements (subject, relationship, object)
        if len(triplet) >= 3:
            head, relation, tail = triplet[:3]
            head_type = triplet[1] if len(triplet) > 3 else 'NA'  # Use 'NA' or a default value if missing
            tail_type = triplet[4] if len(triplet) == 5 else 'NA'
            # Add head and tail to entity_to_id if they don't exist
            if head not in entity_to_id:
                entity_to_id[head] = entity_id
                G.add_node(entity_id, label=head, type=head_type)
                entity_id += 1
            if tail not in entity_to_id:
                entity_to_id[tail] = entity_id
                G.add_node(entity_id, label=tail, type=tail_type)
                entity_id += 1
            # Add relation to relation_to_id if it doesn't exist
            if relation not in relation_to_id:
                relation_to_id[relation] = relation_id
                relation_id += 1
            # Add edge to the graph
            G.add_edge(entity_to_id[head], entity_to_id[tail], label=relation)
        else:
            print(f"Skipping incomplete triplet: {triplet}")

    return G, entity_to_id, relation_to_id

def save_graph_to_gml(G, file_path):
    nx.write_gml(G, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GML file from triplets in JSON files.")
    parser.add_argument("triplets_directory", help="Directory containing triplet JSON files")
    parser.add_argument("output_gml_file", help="Path to the output GML file")
    args = parser.parse_args()

    triplets = process_directory(args.triplets_directory)
    G, entity_to_id, relation_to_id = create_kg_and_mappings(triplets)
    save_graph_to_gml(G, args.output_gml_file)

    print(f"Graph has been saved to {args.output_gml_file}")
