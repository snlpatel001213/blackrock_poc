import json
import os

def validate_json_files(directory):
    invalid_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    json.load(file)  # Attempt to parse JSON
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in file: {filename}")
                print(f"Error: {e}")
                invalid_files.append(filename)
    return invalid_files

if __name__ == "__main__":
    directory = "data/news_articles/processed/us-financial-news-articles/output/output/"  # Replace with your directory path
    invalid_files = validate_json_files(directory)
    
    # If there are invalid files, handle them as needed
    if invalid_files:
        print(f"Found {len(invalid_files)} invalid JSON file(s):")
        for invalid_file in invalid_files:
            print(invalid_file)
        # Here you can decide to move, delete, or log the invalid files
