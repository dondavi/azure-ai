## Project Overview
This project implements a Retrieval Augmented Generation (RAG) client using Python and Azure OpenAI. It integrates custom data sources (PDFs in `/data/`) into prompts for generative AI models, leveraging Azure AI Search for retrieval.

## Key Components
- **ownData.py**: Main entry point. Handles user input, queries Azure OpenAI with Azure Search as a data source, and writes results to timestamped JSON files (`Owndata-<epoch>.json`).
- **/data/**: Contains source documents (PDFs) used to build the Azure Search index.
- **OwndataViewer.html**: Static HTML/JS file for browsing and rendering JSON output files as readable HTML tables/lists.

## Developer Workflow
- Install dependencies: `pip install python-dotenv openai==1.65.2`
- Run the client: `python3 ownData.py`
- Output is written to a new JSON file per run, named with the current Unix epoch.
- View results: Open `OwndataViewer.html` in a browser and select a JSON file to view its contents.

## Patterns & Conventions
- **Environment Variables**: All Azure credentials and configuration are loaded from `.env` using `python-dotenv`. Required keys: `AZURE_OAI_ENDPOINT`, `AZURE_OAI_KEY`, `AZURE_OAI_DEPLOYMENT`, `AZURE_API_VERSION`, `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX`, `AZURE_SEARCH_KEY`, `SYSTEM_PROMPT`.
- **Data Flow**: User input → Azure OpenAI (with Azure Search grounding) → JSON output file → HTML viewer.
- **Output Formatting**: Before saving, all `"content"` keys in the completion dict are replaced with `"long_text"` for easier downstream rendering.
- **File Naming**: Output JSON files use the format `Owndata-<epoch>.json` for uniqueness and traceability.
- **HTML Viewer**: Renders JSON as HTML tables/lists, not raw JSON. See `OwndataViewer.html` for rendering logic.

## Integration Points
- **Azure OpenAI**: Used via the `openai` Python SDK, with custom data sources configured for Azure Search.
- **Azure Search**: Indexes PDF documents for retrieval. Connection parameters are passed in the API call.

## Example Usage
```python
completion = client.chat.completions.create(
    model=deployment,
    ...
    extra_body={
        "data_sources": [
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
```

## Tips for AI Agents
- Always replace `"content"` keys with `"long_text"` in output JSON.
- Use environment variables for all secrets/configuration.
- Output files should be readable by the HTML viewer (tables/lists, not raw JSON).
- Reference `/data/` for source documents and ensure the index is up-to-date for best results.