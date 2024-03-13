import os
import json
from tqdm import tqdm
original_folder = "../../data/2018_01_112b52537b67659ad3609a234388c50a"
triplet_output = "../../data/processed/us-financial-news-articles/output/triplet_output"
published_date_added =  "../../data/processed/us-financial-news-articles/output/published_date_added"

triplet_files = [f for f in os.listdir(triplet_output) if f.startswith('news_')]
print (triplet_files[:5])
for each_triplet_file in tqdm(triplet_files):
    try:
        original_file = os.path.join(original_folder,each_triplet_file.replace(".txt",".json"))
        triplet_file = os.path.join(triplet_output,each_triplet_file)
        original_file_ptr  = open(original_file, "r")
        triplet_file_ptr  = open(triplet_file, "r")
        published_date_added_ptr = open(os.path.join(published_date_added, each_triplet_file),"w")
        original_file_content = json.loads(original_file_ptr.read())
        triplet_file_content = eval(triplet_file_ptr.read())
        published_date = original_file_content["thread"]["published"]
        triplet_file_content["published"] = published_date
        json.dump(triplet_file_content,published_date_added_ptr) 
        original_file_ptr.close()
        triplet_file_ptr.close()
        published_date_added_ptr.close()
    except:
        print("ignored : ", each_triplet_file)