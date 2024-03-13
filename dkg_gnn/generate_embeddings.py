import argparse
from sentence_transformers import SentenceTransformer
import json
import warnings

# Filter out the TypedStorage deprecation warning
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

def generate_embeddings(input_file, output_file, model_name="all-MiniLM-L6-v2"):
    # Load the model
    model = SentenceTransformer(model_name)
    
    # Read sentences from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        sentences = f.read().splitlines()
    
    # Generate embeddings
    embeddings = model.encode(sentences)
    
    # Save embeddings to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding in embeddings:
            # Convert numpy array to list for JSON serialization
            embedding_list = embedding.tolist()
            json.dump(embedding_list, f)
            f.write('\n')

def main():
    parser = argparse.ArgumentParser(description="Generate Sentence-BERT embeddings for sentences stored in a file.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing sentences.")
    parser.add_argument("output_file", type=str, help="Path to the output file to save embeddings.")
    parser.add_argument("--model_name", type=str, default="all-MiniLM-L6-v2", help="Pre-trained Sentence-BERT model name.")
    
    args = parser.parse_args()
    
    generate_embeddings(args.input_file, args.output_file, args.model_name)

if __name__ == "__main__":
    main()
