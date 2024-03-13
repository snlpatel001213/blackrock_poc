import json
import os
import re
import argparse

def case_fix_missing_value(data):
    # Assuming data is a dictionary with 'output' key containing the list of triplets
    fixed_triplets = []
    for triplet in data.get('output', []):
        # Remove empty strings from the triplet
        cleaned_triplet = [item for item in triplet if item != '']
        # Ensure the triplet has exactly 5 elements, padding with 'NA' if necessary
        while len(cleaned_triplet) < 5:
            cleaned_triplet.append('NA')
        # Trim the triplet to 5 elements if it has more
        fixed_triplets.append(cleaned_triplet[:5])
    data['output'] = fixed_triplets
    return data

def special_case_fix(data):
    # Custom fixes for specific issues
    # Example: Inserting missing commas or correcting value formatting
    # These are placeholders and should be adjusted based on the actual issues in your files
    data = re.sub(r'(\w+)(\s*{)', r'\1,\2', data)  # Attempt to insert missing commas
    data = data.replace('IncorrectValue', '"CorrectValue"')  # Correcting specific value formatting
    return data

def cleanse_json(source_file_path, target_directory):
    target_file_path = os.path.join(target_directory, os.path.basename(source_file_path))
    os.makedirs(target_directory, exist_ok=True)  # Ensure the target directory exists

    with open(source_file_path, 'r', encoding='utf-8') as file:
        data = file.read().strip()

    # Replace Python's None with JSON's null
    data = data.replace("None", "null")

    # Ensure property names are enclosed in double quotes
    data = re.sub(r'([{,]\s*)(\w+)(\s*:\s*)', r'\1"\2"\3', data)

    # Attempt to insert missing commas between JSON object members
    data = re.sub(r'(\}|\])(\s*)(\{|\[)', r'\1,\2\3', data)

    # Attempt to insert missing commas between array elements
    data = re.sub(r'(\")(\s*)(\{|\[)', r'\1,\2\3', data)

    # Correctly handle single quotes within strings
    data = re.sub(r"(\W)'([^']+)'(\W)", r'\1"\2"\3', data)

    try:
        # Parse the string as JSON
        parsed_data = json.loads(data)

        # Write the fixed content to a new file in the target directory
        with open(target_file_path, 'w', encoding='utf-8') as target_file:
            json.dump(parsed_data, target_file, indent=4)

        print(f"Successfully cleansed and saved to {target_file_path}")
    except json.JSONDecodeError as e:
        print(f"Error processing {source_file_path}: {e}")
        # Apply special case fixes for known issues
        fixed_data = special_case_fix(data)
        try:
            # Try parsing the fixed data
            parsed_data = json.loads(fixed_data)
            with open(target_file_path, 'w', encoding='utf-8') as target_file:
                json.dump(parsed_data, target_file, indent=4)
            print(f"Successfully applied special fixes and saved to {target_file_path}")
        except json.JSONDecodeError as e:
            print(f"Failed to fix JSON in {source_file_path}: {e}")
            # If JSON is still invalid, write an empty JSON object to the file
            with open(target_file_path, 'w', encoding='utf-8') as target_file:
                target_file.write('{}')
    except Exception as e:
        print(f"An unexpected error occurred while processing {source_file_path}: {e}")

def process_directory(source_directory, target_directory):
    for filename in os.listdir(source_directory):
        if filename.endswith(".txt"):  # Adjusted to process .txt files
            source_file_path = os.path.join(source_directory, filename)
            cleanse_json(source_file_path, target_directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanse JSON content in .txt files in a directory and save the corrected files to a new directory.")
    parser.add_argument("source_directory", help="Directory containing the original .txt files with JSON content")
    parser.add_argument("target_directory", help="Directory to save the cleansed .txt files")
    args = parser.parse_args()

    process_directory(args.source_directory, args.target_directory)
