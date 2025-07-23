RAG Client using local data

Retrieval Augmented Generation (RAG) will be used to build applications that integrate data from custom data sources into a prompt for a generative AI model. RAG is a commonly used pattern for developing generative AI apps - chat-based applications that use a language model to interpret inputs and generate appropriate responses.

Creating an Azure AI Search Index using the travel brochure pdf data.
/data/(*.pdf)


RAG client app
Using the search index, we can use the Azure OpenAI SDK to implement the RAG pattern in a client application. 

Python

```
pip install python-dotenv
pip install openai==1.65.2



`python3 ownData.py`