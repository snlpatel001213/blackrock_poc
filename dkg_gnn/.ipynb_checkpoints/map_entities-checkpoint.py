import json
import argparse
from datetime import datetime
import ast

def load_entity_mapping(file_path):
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 4:  # Expecting 4 columns for entities
                entity, id, _, _ = parts  # Only use the entity and its ID
                mapping[entity] = int(id)
            else:
                print(f"Skipping line due to unexpected format: {line.strip()}")
    return mapping

def load_relation_mapping(file_path):
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:  # Expecting 2 columns for relations
                relation, id = parts
                mapping[relation] = int(id)
            else:
                print(f"Skipping line due to unexpected format: {line.strip()}")
    return mapping

def convert_triplets_to_ids_with_time(triplets, entity_mapping, relation_mapping):
    converted_triplets = []
    for triplet in triplets:
        head, head_type, relation, tail, tail_type, time = triplet
        head_id = entity_mapping.get(head)
        relation_id = relation_mapping.get(relation)
        tail_id = entity_mapping.get(tail)
        # Convert the time to day of the year
        time_day_of_year = datetime.strptime(time, "%Y-%m-%d").timetuple().tm_yday
        if head_id is not None and relation_id is not None and tail_id is not None:
            converted_triplets.append((head_id, relation_id, tail_id, time_day_of_year))
    return converted_triplets

def read_triplets_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        try:
            # Attempt to safely evaluate the string as a Python literal
            data = ast.literal_eval(content)
            # Convert the Python object to a JSON-formatted string and then parse it
            json_content = json.dumps(data)
            parsed_data = json.loads(json_content)
            return parsed_data['output']
        except (SyntaxError, ValueError) as e:
            print(f"Error converting content to JSON: {e}")
            return None

def save_converted_triplets_with_time(converted_triplets, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for triplet in converted_triplets:
            file.write('\t'.join(map(str, triplet)) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert triplets to a temporal KG dataset using entity and relation IDs.")
    parser.add_argument("entity_file", help="File path for entity2id.txt")
    parser.add_argument("relation_file", help="File path for relation2id.txt")
    parser.add_argument("triplets_file", help="File path for the triplets input file")
    parser.add_argument("output_file", help="File path for the output temporal KG dataset")
    args = parser.parse_args()

    # Load the mappings
    entity_mapping = load_entity_mapping(args.entity_file)
    relation_mapping = load_relation_mapping(args.relation_file)

    # Read triplets from the input file
    input_triplets = read_triplets_from_file(args.triplets_file)

    # Convert the triplets to IDs with time
    converted_triplets = convert_triplets_to_ids_with_time(input_triplets, entity_mapping, relation_mapping)

    # Save the converted triplets to an output file
    save_converted_triplets_with_time(converted_triplets, args.output_file)

    print(f"Temporal Knowledge Graph dataset has been saved to {args.output_file}")
