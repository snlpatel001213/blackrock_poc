import json
import os
import re
import argparse
import ast



def cleanse_json(source_file_path, target_directory):
    target_file_path = os.path.join(target_directory, os.path.basename(source_file_path))
    os.makedirs(target_directory, exist_ok=True)  # Ensure the target directory exists

    with open(source_file_path, 'r', encoding='utf-8') as file:
        try:
            data = file.read()
            # Replace single quotes with double quotes and remove leading/trailing whitespace
            data = data.strip().replace("'", '"')

            # Attempt to insert missing commas between JSON object members
            data = re.sub(r'(\}|\])(\s*)(\{|\[)', r'\1,\2\3', data)

            # Attempt to insert missing commas between array elements
            data = re.sub(r'(\")(\s*)(\{|\[)', r'\1,\2\3', data)

            # Parse the string as JSON
            parsed_data = json.loads(data)
            
            # Write the fixed content to a new file in the target directory
            with open(target_file_path, 'w', encoding='utf-8') as target_file:
                json.dump(parsed_data, target_file, indent=4)
            print(f"Successfully cleansed and saved to {target_file_path}")
        except json.JSONDecodeError as e:
            print(f"Error processing {source_file_path}: {e}")
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

# def cleanse_json(source_file_path, target_directory):
#     target_file_path = os.path.join(target_directory, os.path.basename(source_file_path))
#     os.makedirs(target_directory, exist_ok=True)  # Ensure the target directory exists

#     with open(source_file_path, 'r', encoding='utf-8') as file:
#         try:
#             data = file.read()
#             # Replace single quotes with double quotes and remove leading/trailing whitespace
#             data = data.strip().replace("'", '"')
#             # Parse the string as JSON
#             parsed_data = json.loads(data)
            
#             # Write the fixed content to a new file in the target directory
#             with open(target_file_path, 'w', encoding='utf-8') as target_file:
#                 json.dump(parsed_data, target_file, indent=4)
#             print(f"Successfully cleansed and saved to {target_file_path}")
#         except json.JSONDecodeError as e:
#             print(f"Error processing {source_file_path}: {e}")
#         except Exception as e:
#             print(f"An unexpected error occurred while processing {source_file_path}: {e}")

# def process_directory(source_directory, target_directory):
#     for filename in os.listdir(source_directory):
#         if filename.endswith(".txt"):  # Adjusted to process .txt files
#             source_file_path = os.path.join(source_directory, filename)
#             cleanse_json(source_file_path, target_directory)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Cleanse JSON content in .txt files in a directory and save the corrected files to a new directory.")
#     parser.add_argument("source_directory", help="Directory containing the original .txt files with JSON content")
#     parser.add_argument("target_directory", help="Directory to save the cleansed .txt files")
#     args = parser.parse_args()

#     process_directory(args.source_directory, args.target_directory)



# def cleanse_json(source_file_path, target_directory):
#     try:
#         with open(source_file_path, 'r', encoding='utf-8') as file:
#             content = file.read().strip()

#         # Check if the file is empty or does not start with a JSON structure
#         if not content:
#             print(f"File is empty: {source_file_path}")
#             return
#         if not (content.startswith('{') or content.startswith('[')):
#             print(f"File does not start with a valid JSON character: {source_file_path}")
#             return

#         # Replace Python's None with JSON's null
#         content = content.replace("None", "null")

#         # Attempt to fix common JSON issues
#         content = re.sub(r"([{\[,]\s*)'([^']+)'(\s*[:\]])", r'\1"\2"\3', content)  # Single quotes to double quotes
#         content = re.sub(r"([{\[,]\s*)'([^']+)'(\s*[:\],])", r'\1"\2"\3', content)  # More single to double quotes
#         content = content.replace("\\'", "'")  # Unescape single quotes
#         content = re.sub(r'(?<!\\)"', r'\"', content)  # Escape double quotes not already escaped

#         # Load and dump to ensure it's valid JSON now
#         data = json.loads(content)

#         # Create the target directory if it doesn't exist
#         os.makedirs(target_directory, exist_ok=True)

#         # Write the fixed content to a new file in the target directory
#         target_file_path = os.path.join(target_directory, os.path.basename(source_file_path))
#         with open(target_file_path, 'w', encoding='utf-8') as file:
#             json.dump(data, file, indent=4)

#         print(f"Successfully cleansed and saved to {target_file_path}")
#     except Exception as e:
#         print(f"Error processing {source_file_path}: {e}")


# def process_directory(source_directory, target_directory):
#     print(f"Processing directory: {source_directory}")
#     for filename in os.listdir(source_directory):
#         if filename.endswith(".txt"):  # Adjusted to process .txt files
#             source_file_path = os.path.join(source_directory, filename)
#             print(f"Processing file: {filename}")
#             cleanse_json(source_file_path, target_directory)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Cleanse JSON content in .txt files in a directory and save the corrected files to a new directory.")
#     parser.add_argument("source_directory", help="Directory containing the original .txt files with JSON content")
#     parser.add_argument("target_directory", help="Directory to save the cleansed .txt files")
#     args = parser.parse_args()

#     process_directory(args.source_directory, args.target_directory)
