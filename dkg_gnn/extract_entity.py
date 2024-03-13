import spacy
import os
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def process_article(article_path):
    # Read the article
    with open(article_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Process the text with spaCy
    doc = nlp(text)

    # Extract entities and format as triplets
    triplets = []
    for ent in doc.ents:
        # Example triplet format: [entity text, entity label, "RELATED_TO"]
        # Adjust the logic here based on how you want to define relationships
        triplets.append([ent.text, ent.label_, "RELATED_TO"])

    return triplets

def main(directory_path, output_file):
    # List to hold all articles' entities
    all_entities = []

    # Process each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            article_path = os.path.join(directory_path, filename)
            entities = process_article(article_path)
            all_entities.append({
                'input': article_path,
                'output': entities,
                'category': 'closed_qa'
            })

    # Write the results to a JSONL file
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_entities:
            f.write(json.dumps(item) + '\n')

if __name__ == "__main__":
    directory_path = 'path/to/your/articles'  # Update this path
    output_file = 'entities_output.jsonl'
    main(directory_path, output_file)
