import os
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OAI_ENDPOINT")
api_key = os.environ.get("AZURE_OAI_KEY")
deployment = os.environ.get("AZURE_OAI_DEPLOYMENT")

client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-12-01-preview",
)

 # Configure your data source
text = input('\nEnter a question:\n')
    
completion = client.chat.completions.create(
     model=deployment,
     messages=[
         {
             "role": "user",
             "content": text,
         },
     ],
     extra_body={
         "data_sources":[
             {
                 "type": "azure_search",
                 "parameters": {
                     "endpoint": os.environ["AZURE_SEARCH_ENDPOINT"],
                     "index_name": os.environ["AZURE_SEARCH_INDEX"],
                     "authentication": {
                         "type": "api_key",
                         "key": os.environ["AZURE_SEARCH_KEY"],
                     }
                 }
             }
         ],
     }
)


print(completion.model_dump_json(indent=2))