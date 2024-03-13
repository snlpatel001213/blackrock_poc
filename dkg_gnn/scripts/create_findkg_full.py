import json
import argparse

def load_entity_mapping(file_path):
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 4:  # Entity mapping format: name, id, category, and additional info
                name, id, _, _ = parts
                mapping[int(id)] = name  # Convert ID to int for easier lookup
    return mapping

def load_relation_mapping(file_path):
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            name, id = line.strip().split('\t')
            mapping[int(id)] = name  # Convert ID to int for easier lookup
    return mapping


def map_ids_to_names(kg_file, entity_mapping, relation_mapping, output_file):
    with open(kg_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out_f:
        for line in f:
            head_id, relation_id, tail_id = map(int, line.strip().split('\t')[:3])
            head_name = entity_mapping.get(head_id, "Unknown Entity")
            relation_name = relation_mapping.get(relation_id, "Unknown Relation")
            tail_name = entity_mapping.get(tail_id, "Unknown Entity")
            out_f.write(f"{head_name}\t{relation_name}\t{tail_name}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map IDs back to names in the KG and save the output.")
    parser.add_argument("kg_file", help="File path for the KG with IDs")
    parser.add_argument("entity2id_file", help="File path for the entity2id mapping")
    parser.add_argument("relation2id_file", help="File path for the relation2id mapping")
    parser.add_argument("output_file", help="File path for the output KG with names")
    args = parser.parse_args()

    # Load mappings
    entity_mapping = load_entity_mapping(args.entity2id_file)
    relation_mapping = load_relation_mapping(args.relation2id_file)

    # Map IDs to names and save the output
    map_ids_to_names(args.kg_file, entity_mapping, relation_mapping, args.output_file)

    print(f"KG with names has been saved to {args.output_file}")

