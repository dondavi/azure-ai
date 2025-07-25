import os
import openai
import dotenv
# import json
import time
# Set the current Unix epoch time
current_unix_epoch_time = time.time()
unix_epoch = current_unix_epoch_time
# Load environment variables from .env file
dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OAI_ENDPOINT")
api_key = os.environ.get("AZURE_OAI_KEY")
deployment = os.environ.get("AZURE_OAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_API_VERSION")

client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version,
)

 # Configure your data source
text = input('\nEnter a question:\n')
text = text + " " + input('\nEnter a follow-up question:\n')
    

# Parking these for now, as they are not used in the current implementation
  #   top_p = 0.95,
  #   frequency_penalty = 0,
  #   presence_penalty = 0,
  #   response_format = "json",
completion = client.chat.completions.create(
     model=deployment,
     temperature = 0.5,
     max_tokens = 1000,
     messages=[
          {"role": "system", "content": os.environ["SYSTEM_PROMPT"]},
          {"role": "user", "content": text},
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
# Get the completion as a Python dict
completion_dict = completion.model_dump()

# Recursively replace 'content' keys with 'long_text'
def replace_content_key(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == "content":
                new_obj["long_text"] = v
            else:
                new_obj[k] = replace_content_key(v)
        return new_obj
    elif isinstance(obj, list):
        return [replace_content_key(item) for item in obj]
    else:
        return obj

formatted_completion = replace_content_key(completion_dict)

# Generate a random number for the filename
filename = f"Owndata-{unix_epoch}.json"

# Write to a JSON file with the random number in the filename
with open(filename, "w") as f:
    f.write(completion.model_dump_json(indent=2))
# Output to command line
print(completion.model_dump_json(indent=2))