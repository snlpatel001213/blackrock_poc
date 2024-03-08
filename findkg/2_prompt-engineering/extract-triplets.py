import os
from mixtral_api_ngc import get_triplet
from tqdm import tqdm 

class ExtractTripletUtils:
    def __init__(self):
        # self.model = "meta-llama/Llama-2-70b-chat-hf"
        # self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        # self.pipeline = transformers.pipeline(
        #     "text-generation",
        #     model=self.model,
        #     torch_dtype=torch.float16,
        #     device_map="auto",
        # )
        # model_id = "mistralai/Mixtral-8x7B-v0.1"
        # self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        # self.model = AutoModelForCausalLM.from_pretrained(model_id)
        self.preprocessed_folder_path = '../../data/processed/us-financial-news-articles/input'
        
    def get_prompt(self,news_prompt):    
        self.master_prompt = f"""
                <s>[INST] <<SYS>>
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
                    
                    From this text, your output Must be in python lis tof tuple with each tuple made up of ['h', 'type', 'r', 'o', 'type'], each element of the tuple is the string, where the relationship 'r' must be in the given relation verbs set above. Only output the list. 
                    As an Example, consider the following news excerpt: 
                        Input :'Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month. The product's release is likely to positively impact Apple's stock value.'
                        OUTPUT : ```
                            [('Apple Inc.', 'COMP', 'Introduce', 'iPhone 14', 'PRODUCT'),
                            ('Apple Inc.', 'COMP', 'Operate_In', 'Technology Sector', 'SECTOR'),
                            ('iPhone 14', 'PRODUCT', 'Positive_Impact_On', 'Apple's Stock Value', 'FIN_INSTRUMENT')]
                        ```
                        The output structure must not be anything apart from above OUTPUT structure.
                <</SYS>>
                    INPUT_TEXT:
                    """ + news_prompt.replace("\n",".") +"[/INST]"
        return self.master_prompt 

    def list_files(self):
        files_in_folder = os.listdir(self.preprocessed_folder_path)
        return files_in_folder
    
    def read_text_from_files(self,file_path):
        with open(file_path, 'r') as file:
            return file.read()
        

    def execute(self, prompt):
        sequences = self.pipeline(
            prompt,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=2000

        )
        print("sequences :", sequences)
        for seq in sequences:
            print(f"Result: {seq['generated_text']}")
      

Ext = ExtractTripletUtils()
output_folder = "../../data/processed/us-financial-news-articles/output"
preprocessed_files = Ext.list_files()
preprocessed_files.sort()
for each_preprocessed_file in tqdm(preprocessed_files[(3010+1960+216+57+7683+1773+457):]):
    try:
        preprocessed_file = os.path.join(Ext.preprocessed_folder_path, each_preprocessed_file)
        news_text = Ext.read_text_from_files(preprocessed_file)
        # print("news_text", news_text)
        triplet = get_triplet(news_prompt=news_text.replace("\n","."))
        output_file =  os.path.join(output_folder, each_preprocessed_file)
        file_ptr = open(output_file, "w")
        file_ptr.write(str(triplet))
        file_ptr.flush()
        file_ptr.close()
    except SyntaxError as e:
        print("Error in file : ", each_preprocessed_file)