import argparse
import ast
import os

def process_files(input_dir):
    entity2id = {}
    relation2id = {}
    entity_id = 0
    relation_id = 0

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r') as file:
                file_content = file.read().strip()
                
                # Attempt to standardize the file content format
                if not file_content.startswith('{'):
                    file_content = "{'output': " + file_content
                if not file_content.endswith('}'):
                    file_content += '}'
                
                try:
                    # Attempt to evaluate the modified file content
                    data = ast.literal_eval(file_content)
                    
                    # Ensure data is a dictionary with 'output' key and it's a list
                    if isinstance(data, dict) and 'output' in data and isinstance(data['output'], list):
                        triplets = data['output']
                    else:
                        raise ValueError("Unexpected data structure or 'output' key is missing")
                except (SyntaxError, ValueError) as e:
                    print(f"Error processing {filename}: {e}")
                    triplets = []  # Set triplets to an empty list to avoid further errors

                print(f"Processing {len(triplets)} triplets from {filename}")
                for triplet in triplets:
                    # Ensure triplet has exactly 5 elements
                    if len(triplet) == 5:
                        head, head_type, relation, tail, tail_type = triplet

                        # Assign unique IDs to new entities and relations
                        if head not in entity2id:
                            entity2id[head] = entity_id
                            entity_id += 1
                        if tail not in entity2id:
                            entity2id[tail] = entity_id
                            entity_id += 1
                        if relation not in relation2id:
                            relation2id[relation] = relation_id
                            relation_id += 1
                    else:
                        print(f"Skipping invalid triplet in {filename}: {triplet}")

    return entity2id, relation2id



def write_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}\t{value}\n")

def main(input_dir, entity2id_file, relation2id_file):
    entity2id, relation2id = process_files(input_dir)
    write_to_file(entity2id, entity2id_file)
    write_to_file(relation2id, relation2id_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate entity2id and relation2id files from triplet dictionaries.")
    parser.add_argument('input_dir', type=str, help='Directory containing the .txt files with triplet dictionaries.')
    parser.add_argument('entity2id_file', type=str, help='Output file for entity2id mappings.')
    parser.add_argument('relation2id_file', type=str, help='Output file for relation2id mappings.')
    
    args = parser.parse_args()
    main(args.input_dir, args.entity2id_file, args.relation2id_file)
