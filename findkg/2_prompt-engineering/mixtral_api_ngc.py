import requests
import ast
import json


invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/8f4118ba-60a8-4e6b-8574-e38a4067a4a3"
fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

def get_triplet(news_prompt):
    payload = {
      "messages": [
        {
          "content": """
                        Note that the entities should not be generic, numerical or temporal (like dates or percentages).  Entities must be classified into the following categories:
                        ORG: Organizations other than government or regulatory bodies
                        ORG/GOV: Government bodies (e.g., "United States Government")
                        ORG/REG: Regulatory bodies (e.g., "Federal Reserve")
                        PERSON: Individuals (e.g., "Elon Musk")
                        GPE: Geopolitical entities such as countries, cities, etc. (e.g., "Germany")
                        COMP: Companies (e.g., "Google")
                        PRODUCT: Products or services (e.g., "iPhone")
                        EVENT: Specific and Material Events (e.g., "Olympic Games", "Covid-19")
                        SECTOR: Company sectors or industries (e.g., "Technology sector")
                        ECON_INDICATOR: Economic indicators (e.g., "Inflation rate"), numerical value like "10%" is not a ECON_INDICATOR;
                        FIN_INSTRUMENT: Financial and market instruments (e.g., "Stocks", "Global Markets")
                        CONCEPT: Abstract ideas or notions or themes (e.g., "Inflation", "AI", "Climate Change")
                        The relationships 'r' between these entities must be represented by one of the following relation verbs set: Has, Announce, Operate_In, Introduce, Produce, Control, Participates_In, Impact, Positive_Impact_On, Negative_Impact_On, Relate_To, Is_Member_Of, Invests_In, Raise, Decrease.
                        Remember to conduct entity disambiguation, consolidating different phrases or acronyms that refer to the same entity (for instance,  "UK Central Bank", "BOE" and "Bank of England" should be unified as "Bank of England"). Simplify each entity of the triplet to be less than four words.  
                        
                        From this text, your output Must be in python dict made up of nested list made up of ['h', 'type', 'r', 'o', 'type'], where the relationship 'r' must be in the given relation verbs set above. Only output the list. 
                        As an Example, consider the following news excerpt: 
                            Input :'Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month. The product's release is likely to positively impact Apple's stock value.'
                            OUTPUT : {"output":[['Apple Inc.', 'COMP', 'Introduce', 'iPhone 14', 'PRODUCT'], ['Apple Inc.', 'COMP', 'Operate_In', 'Technology Sector', 'SECTOR'], ['iPhone 14', 'PRODUCT', 'Positive_Impact_On', 'Apple's Stock Value', 'FIN_INSTRUMENT']]}
                        Dont use output like "Based on the given input text, here is the output in the required format:"
                        The output MUST be  python dict made up of nested list and MUST not be anything apart from above OUTPUT.
                        INPUT_TEXT: """+news_prompt+".[/INST]"
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