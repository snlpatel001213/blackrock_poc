import argparse
import ast
import os

def read_triplets_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read().strip()
        print(file_content)

        # Check if the file content starts with '{' and ends with '}'.
        # If not, add 'output' key and braces to make it a dictionary string.
#         if not file_content.startswith('{'):
#             file_content = "{'output': " + file_content
#         if not file_content.endswith('}'):
#             file_content += '}'

        triplet_dict = ast.literal_eval(file_content)
    return triplet_dict


def write_knowledge_graph_to_file(triplets, output_file_path):
    with open(output_file_path, 'w') as file:
        for triplet in triplets:
            # Print the length and content of each triplet for debugging
            print(f"Triplet length: {len(triplet)}, content: {triplet}")
            print()

            # Ensure triplet has exactly 5 elements
            if len(triplet) == 5:
                head, head_type, relation, tail, tail_type = triplet
                # Write the head, relation, and tail to the file
                file.write(f"{head}, {relation}, {tail}\n")
            else:
                # If the triplet does not have 5 elements, print an error message
                print("Skipping invalid triplet with incorrect number of elements.")


def process_directory(input_dir, output_file):
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            print(filename)
            triplets = read_triplets_from_file(file_path)
            write_knowledge_graph_to_file(triplets, output_file)

def main():
    parser = argparse.ArgumentParser(description="Process a directory of text files to extract knowledge graph triplets.")
    parser.add_argument('input_dir', type=str, help='Directory containing the text files with triplet dictionaries.')
    parser.add_argument('output_file', type=str, help='Output file to write the knowledge graph.')
    
    args = parser.parse_args()
    process_directory(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()
