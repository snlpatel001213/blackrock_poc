import os
import argparse

def fix_file_format(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read().strip()

    # Check if the file content starts with '{'output':' and ends with '}'
    needs_fixing = False
    if not file_content.startswith("{'output':"):
        file_content = "{'output': " + file_content
        needs_fixing = True
    if not file_content.endswith('}'):
        file_content += '}'
        needs_fixing = True

    # Rewrite the file with the correct format if it was modified
    if needs_fixing:
        with open(file_path, 'w') as file:
            file.write(file_content)
        print(f"{file_path}: File format was fixed.")
    else:
        print(f"{file_path}: File format is already correct.")

def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            fix_file_format(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix file content format in a directory.")
    parser.add_argument("directory", type=str, help="Path to the directory containing the files.")
    args = parser.parse_args()

    process_directory(args.directory)
