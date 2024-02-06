import os
import json
from tqdm import tqdm

class PreProcessing:
    def __init__(self) -> None:
        self.data_folder_path = '../../data/source/us-financial-news-articles/2018_01_112b52537b67659ad3609a234388c50a'

    def list_news_files(self):
        files_in_folder = [f for f in os.listdir(self.data_folder_path) if f.startswith('news_')]
        return files_in_folder
        
    def extract_text_from_json(self,json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            if 'text' in data:
                return data['text']
            else:
                return None
            
Pre = PreProcessing()
processed_folder_path = "../../data/processed/us-financial-news-articles/input"
json_files = Pre.list_news_files()
for each_file in tqdm(json_files):
    file_name, _ = each_file.split(".")
    relative_file_path = os.path.join(Pre.data_folder_path, each_file)
    text_data = Pre.extract_text_from_json(relative_file_path)
    output_file_path = os.path.join(processed_folder_path, f"{file_name}.txt")
    out_file = open(output_file_path, "w")
    out_file.write(text_data)
    out_file.flush()
    out_file.close()

    

        
