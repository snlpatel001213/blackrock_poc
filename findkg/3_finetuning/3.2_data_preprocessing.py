import os
from tqdm import tqdm

def list_files(folder_path):
    files_in_folder = os.listdir(folder_path)
    return files_in_folder
def read_text_from_files(file_path):
    with open(file_path, 'r') as file:
        return file.read()

output_folder = "../../data/processed/us-financial-news-articles/output"
input_folder = "../../data/processed/us-financial-news-articles/input"
sft_date = "../../data/processed/us-financial-news-articles/SFT_training"
output_preprocessed_files = list_files(output_folder)
sft_file = open(os.path.join(sft_date,"sft_data.json1"),"w")
for each_preprocessed_file in tqdm(output_preprocessed_files):
    try:
        preprocessed_file = os.path.join(output_folder, each_preprocessed_file)
        triplet_text = eval(read_text_from_files(preprocessed_file))
        triplets = triplet_text['output']
        input_file = os.path.join(input_folder, each_preprocessed_file)
        news_text = read_text_from_files(input_file).replace("\n",".").replace('"','').replace("'","")
        final_training_sample = {"input":news_text, "output":str(triplets), "category":"closed_qa"}
        sft_file.write(str(final_training_sample)+"\n")
    except TypeError as e:
        print("Error in file : ", each_preprocessed_file)