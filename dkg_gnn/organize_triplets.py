import json
import os
import argparse

# Define your keywords related to financial services, stock market, or economics
financial_keywords = {'financial services', 'stock market', 'economics', 'finance', 'economic', 'stocks', 'trading', 'investment', 'banking', 'fiscal', 'monetary', 'earnings', 'interest rates', 'shares', 'bonds', 'losses', ''}

# Criteria for filtering
entity_types = {'ORG', 'ORG/GOV', 'ORG/REG', 'GPE', 'PERSON', 'COMP', 'PRODUCT', 'EVENT', 'SECTOR', 'ECON_INDICATOR', 'FIN_INSTRUMENT', 'CONCEPT'}
entity_categories = {'FINANCIAL', 'ECONOMIC', 'GOV'}
relationships = {'Has', 'Announce', 'Operate_In', 'Introduce', 'Produce', 'Control', 'Participates_In', 'Impact', 'Positive_Impact_On', 'Negative_Impact_On', 'Relate_To', 'Is_Member_Of', 'Invests_In', 'Raise', 'Decrease'}

def filter_triplets(triplets):
    filtered_triplets = []
    for triplet in triplets:
        # Ensure the triplet has at least 5 elements, padding with 'NA' if necessary
        if len(triplet) < 5:
            triplet += ['NA'] * (5 - len(triplet))
        head, head_type, relation, tail, tail_type = triplet[:5]

        # Convert all parts of the triplet to strings for case-insensitive matching
        head_str = str(head).lower()
        tail_str = str(tail).lower()
        relation_str = str(relation).lower()

        # Check if the triplet matches the filtering criteria
        if (head_type in entity_types and tail_type in entity_types and relation in relationships) and \
           (any(keyword in head_str for keyword in financial_keywords) or \
            any(keyword in tail_str for keyword in financial_keywords) or \
            any(keyword in relation_str for keyword in financial_keywords)):
            filtered_triplets.append(triplet)
    return filtered_triplets



# def filter_triplets(triplets):
#     filtered_triplets = []
#     for triplet in triplets:
#         # Ensure triplet is a list; this is a safeguard and might need adjustment based on your data structure
#         if not isinstance(triplet, list):
#             print(f"Skipping non-list triplet: {triplet}")
#             continue

#         # Ensure the triplet has at least 5 elements, padding with 'NA' if necessary
#         padded_triplet = triplet + ['NA'] * (5 - len(triplet))
#         head, head_type, relation, tail, tail_type = padded_triplet[:5]

#         # Check if the triplet matches the filtering criteria
#         if (head_type in entity_types and tail_type in entity_types and relation in relationships) or \
#            (head in financial_keywords or tail in financial_keywords or relation in financial_keywords):
#             filtered_triplets.append(triplet)
#     return filtered_triplets



def process_directory(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    for filename in os.listdir(source_directory):
        if filename.endswith(".txt"):  # Adjusted to process .json files
            source_file_path = os.path.join(source_directory, filename)
            target_file_path = os.path.join(target_directory, filename)
            
            with open(source_file_path, 'r', encoding='utf-8') as file:
                try:
                    parsed_data = json.load(file)
                    # Check if 'output' key exists in the parsed_data
                    if 'output' in parsed_data:
                        filtered_triplets = filter_triplets(parsed_data['output'])
                        
                        # Save the filtered triplets to a new file in the target directory
                        with open(target_file_path, 'w', encoding='utf-8') as target_file:
                            json.dump({'output': filtered_triplets}, target_file, indent=4)
                    else:
                        print(f"The key 'output' is missing in the file: {filename}")
                            
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON content in {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter triplets based on specific criteria and save to a new directory.")
    parser.add_argument("source_directory", help="Directory containing the original triplet files")
    parser.add_argument("target_directory", help="Directory to save the filtered triplet files")
    args = parser.parse_args()

    process_directory(args.source_directory, args.target_directory)
