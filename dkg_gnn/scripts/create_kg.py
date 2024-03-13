import argparse
import ast

def read_triplets_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        triplet_dict = ast.literal_eval(file_content)
    return triplet_dict

def write_knowledge_graph_to_file(triplets, output_file_path):
    with open(output_file_path, 'w') as file:
        for triplet in triplets:
            # Ensure that the triplet has exactly 5 elements
            if len(triplet) == 5:
                head, head_type, relation, tail, tail_type = triplet
                file.write(f"{head}, {relation}, {tail}\n")
            else:
                # If the triplet does not have 5 elements, print an error message
                print("Error: Triplet does not have 5 elements and will be skipped.")


def main(input_file, output_file):
    triplets = read_triplets_from_file(input_file)['output']
    write_knowledge_graph_to_file(triplets, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read triplets from a file and write a knowledge graph to another file.")
    parser.add_argument('input_file', type=str, help='Path to the input text file containing the triplet dictionary.')
    parser.add_argument('output_file', type=str, help='Path to the output text file to write the knowledge graph.')
    
    args = parser.parse_args()
    main(args.input_file, args.output_file)
