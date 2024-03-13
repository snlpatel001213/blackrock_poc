import requests
import json
from pprint import pprint
import json
import ast


def get_triplet(news_prompt):
    prompt = """Note that the entities should not be generic, numerical or temporal (like dates or percentages).  Entities must be classified into the following categories:
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
                        The relationships "r" between these entities must be represented by one of the following relation verbs set: Has, Announce, Operate_In, Introduce, Produce, Control, Participates_In, Impact, Positive_Impact_On, Negative_Impact_On, Relate_To, Is_Member_Of, Invests_In, Raise, Decrease.
                        Remember to conduct entity disambiguation, consolidating different phrases or acronyms that refer to the same entity (for instance,  "UK Central Bank", "BOE" and "Bank of England" should be unified as "Bank of England"). Simplify each entity of the triplet to be less than four words.  
                        From this text, your output Must be in  list of list with each list made up of ["h", "type", "r", "o", "type"], each element of the tuple is the string, where the relationship "r" must be in the given relation verbs set above. Only output the list. 
                        From this text, your output Must be in python dict made up of nested list made up of ["h", "type", "r", "o", "type"], where the relationship "r" must be in the given relation verbs set above. Only output the list. 
                            As an Example, consider the following news excerpt: 
                                INPUT_TEXT :"Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month. The product"s release is likely to positively impact Apple"s stock value."
                                {"output":[
                                    ["Apple Inc.", "COMP", "Introduce", "iPhone 14", "PRODUCT"],
                                    ["Apple Inc.", "COMP", "Operate_In", "Technology Sector", "SECTOR"], 
                                    ["iPhone 14", "PRODUCT", "Positive_Impact_On", "Apple"s Stock Value", "FIN_INSTRUMENT"]
                                    ]}
                            Dont use output like "Based on the given input text, here is the output in the required format:"
                            The output MUST be  python dict made up of nested list and MUST not be anything apart from above OUTPUT. Don not include any comment in the output. Do not add \t \n or anyother extra formatting charatcer in the output. only return instances where complete triplet is present.
                            make sure the output is python parsable list of list with each entity double quoted.
                            Do not output invalid non-printable characters. 
                        INPUT_TEXT : """+news_prompt.replace("\n","")


    FINAL_PROMPT =  '"message":"{'+'"role": "user",'+ '"content": ='+prompt.replace("\n", " ")+'}'
    # FINAL_PROMPT = str("""
    #                    {'messages': [{'role': 'system', 'content': 'Note that the entities should not be generic, numerical or temporal (like dates or percentages). Entities must be classified into the following categories:\n ORG: Organizations other than government or regulatory bodies\n ORG/GOV: Government bodies (e.g., "United States Government")\n ORG/REG: Regulatory bodies (e.g., "Federal Reserve")\n PERSON: Individuals (e.g., "Elon Musk")\n GPE: Geopolitical entities such as countries, cities, etc. (e.g., "Germany")\n COMP: Companies (e.g., "Google")\n PRODUCT: Products or services (e.g., "iPhone")\n EVENT: Specific and Material Events (e.g., "Olympic Games", "Covid-19")\n SECTOR: Company sectors or industries (e.g., "Technology sector")\n ECON_INDICATOR: Economic indicators (e.g., "Inflation rate"), numerical value like "10%" is not a ECON_INDICATOR;\n FIN_INSTRUMENT: Financial and market instruments (e.g., "Stocks", "Global Markets")\n CONCEPT: Abstract ideas or notions or themes (e.g., "Inflation", "AI", "Climate Change")\n The relationships "r" between these entities must be represented by one of the following relation verbs set: Has, Announce, Operate_In, Introduce, Produce, Control, Participates_In, Impact, Positive_Impact_On, Negative_Impact_On, Relate_To, Is_Member_Of, Invests_In, Raise, Decrease.\n Remember to conduct entity disambiguation, consolidating different phrases or acronyms that refer to the same entity (for instance, "UK Central Bank", "BOE" and "Bank of England" should be unified as "Bank of England"). Simplify each entity of the triplet to be less than four words. \n From this text, your output Must be in list of list with each list made up of ["h", "type", "r", "o", "type"], each element of the tuple is the string, where the relationship "r" must be in the given relation verbs set above. Only output the list. \n '}, {'role': 'user', 'content': 'INPUT_TEXT : "LONDON (Reuters) - Despite the strongest start for oil prices in four years, the worlds top oil companies are hesitating to accelerate the search for new resources as a determination to retain capital discipline trumps the hope of making bonanza discoveries.Exxon Mobil, Royal Dutch Shell, Total and their peers are set to cut spending on oil and gas exploration for a fifth year in a row in 2018, according to consultancy Wood Mackenzie (WoodMac), despite a growing urgency to replenish reserves after years of reining back investment.Global investment in exploration, vital to increase output and offset the natural decline of existing fields, will reach $37 billion in 2018, down 7 percent from a year earlier and over 60 percent below the 2014 peak, according to WoodMac.For majors, spending will collectively drop by around 4 percent this year to represent about a tenth of investment in oil and gas production, known as upstream."'}]}""")

    url = 'http://0.0.0.0:9999/v1/chat/completions'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "mixtral",
        "messages": FINAL_PROMPT,
    "temperature": 0.9,
    "max_tokens": 1024,
    "seed": 42,
    "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    # print(response)

    output  = response.json()['choices'][0]['message']['content']
    # print(output)
    outputpython_object = ast.literal_eval(output)
    return outputpython_object