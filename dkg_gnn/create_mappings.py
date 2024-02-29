import json
import os
import argparse
import ast
import pandas as pd


def read_triplets_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = file.read()
            # Parse the JSON content directly without converting to a Python literal
            json_data = ast.literal_eval(json.dumps(data))
            x = json_data.replace("'", '"')
            parsed_data = json.loads(x)
            print(parsed_data)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON content: {e}")
            return None
        
def process_directory(directory):
    all_triplets = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming triplet files end with .txt
            file_path = os.path.join(directory, filename)
            triplets = read_triplets_from_file(file_path)
            if triplets:
                all_triplets.extend(triplets)
    return all_triplets

def create_mappings(triplets):
    entity_to_id = {}
    relation_to_id = {}
    entity_id = 0
    relation_id = 0

    for triplet in triplets:
        if len(triplet) >= 5:  # Ensure there are at least five elements
            head, head_type, relation, tail, tail_type = triplet[:5]  # Only use the first five elements
            # Rest of the code remains the same
            if (head, head_type) not in entity_to_id:
                entity_to_id[(head, head_type)] = entity_id
                entity_id += 1

            if (tail, tail_type) not in entity_to_id:
                entity_to_id[(tail, tail_type)] = entity_id
                entity_id += 1

            if relation not in relation_to_id:
                relation_to_id[relation] = relation_id
                relation_id += 1
        else:
            print(f"Skipping triplet due to unexpected format: {triplet}")

    return entity_to_id, relation_to_id


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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create entity2id and relation2id files from all triplets in a directory.")
    parser.add_argument("directory", help="Directory containing triplet files")
    parser.add_argument("entity_output_file", help="File path for the output entity2id.txt")
    parser.add_argument("relation_output_file", help="File path for the output relation2id.txt")
    args = parser.parse_args()

    # Process all triplet files in the directory
    all_triplets = process_directory(args.directory)

    # Create mappings
    entity_to_id, relation_to_id = create_mappings(all_triplets)

    # Save the mappings to files
    save_mapping_to_file(entity_to_id, args.entity_output_file)
    save_mapping_to_file(relation_to_id, args.relation_output_file)

    print(f"Entity mappings have been saved to {args.entity_output_file}")
    print(f"Relation mappings have been saved to {args.relation_output_file}")