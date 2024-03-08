

import requests
import ast
import json
import os

invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/8f4118ba-60a8-4e6b-8574-e38a4067a4a3"
fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

def normalize_triplet(news_prompt):
    payload = {
      "messages": [
        {
          "content": """
                        Normalize the numbers and  percentage mentioned  in given INPUT_TEXT  so that it helps in comparison mathematically with other documents
                        Preserve output format as input format. DO NOT add extra comments or anything
                        INPUT_TEXT: """+news_prompt+""
                      ,
          "role": "user"
        }
      ],
      "temperature": 0.2,
      "top_p": 0.7,
      "max_tokens": 1024,
      "seed": 42,
      "stream": False
    }

    session = requests.Session()

    response = session.post(invoke_url, headers=headers, json=payload)

    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)

    response.raise_for_status()
    response_body = response.json()


    # Extract content from the JSON
    content = response_body['choices'][0]['message']['content']
    # Evaluate content as a Python object
    python_object = ast.literal_eval(content)

    # Return the result
    return python_object

published_date_added =  "../../data/processed/us-financial-news-articles/output/published_date_added"

triplet_files = [f for f in os.listdir(published_date_added) if f.startswith('news_')]
for each_file in triplet_files[:2]:
    triplet_file_ptr =  open(os.path.join(published_date_added,each_file),"r")
    triplet_file_content = triplet_file_ptr.read()
    normalized_output =  normalize_triplet(triplet_file_content)
    print(normalize_triplet)