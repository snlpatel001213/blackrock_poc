import requests
import json

url = 'http://localhost:8001/v2/models/ensemble/generate'

data = {
    'text_input': """[INST] <<SYS>>
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
                    
                    From this text, your output Must be in python lis tof tuple with each tuple made up of ('h', 'type', 'r', 'o', 'type'), where the relationship 'r' must be in the given relation verbs set above. Only output the list. 
                    As an Example, consider the following news excerpt: 
                        Input :'Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month. The product's release is likely to positively impact Apple's stock value.'
                        OUTPUT : ```
                            [('Apple Inc.', 'COMP', 'Introduce', 'iPhone 14', 'PRODUCT'),
                            ('Apple Inc.', 'COMP', 'Operate_In', 'Technology Sector', 'SECTOR'),
                            ('iPhone 14', 'PRODUCT', 'Positive_Impact_On', 'Apple's Stock Value', 'FIN_INSTRUMENT')]
                        ```
                        The output must not be anything apart from above OUTPUT.
                <</SYS>>
                    INPUT_TEXT: "A report that China is considering slowing or halting purchases of U.S. Treasury bonds may be based on erroneous information and could be "fake," the country's foreign exchange regulator said on Thursday..Bloomberg News reported on Wednesday that Chinese officials reviewing the country's vast foreign exchange holdings had recommended slowing or halting purchases of U.S. Treasury bonds amid a less attractive market for them and rising U.S.-China trade tensions. The report sent U.S. Treasury yields to 10-month highs and sent the dollar lower.."The news could quote the wrong source of information, or may be fake news," the State Administration of Foreign Exchange (SAFE) said in a statement published on its website..The U.S. 10-year Treasury yield edged down to 2.5366 percent from Wednesday's close of 2.549 percent, while the dollar gained 0.3 percent to 111.72 yen after the regulator's comment..China has been diversifying its foreign currency reserves investments to help "safeguard the overall safety of foreign exchange assets and preserve and increase their value", the SAFE said..The forex reserves investment in U.S. Treasury bonds is a market activity, with investment professionally managed according to market conditions and investment needs, it said..The regulator added that forex reserves management agencies are responsible investors in international financial markets..The exact composition of China's reserves is a state secret and the subject of intense scrutiny by global investors..According to data from the Treasury Department, the country is the biggest foreign holder of U.S. government debt, with $1.19 trillion in Treasuries as of October 2017..China's foreign exchange reserves, the world's largest, rose $20.2 billion in December to $3.14 trillion, as tight regulations and a strong yuan continued to discourage capital outflows, data from China's central bank showed.[/INST]  Here is the output in the format of tuples, where each tuple consists of ('h', 'type', 'r', 'o', 'type')":
                    [/INST]""",
    'max_tokens': 1024,
    'bad_words': '',
    'stop_words': ''
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.text)