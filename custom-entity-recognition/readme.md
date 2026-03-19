# Custom Entity Recognition with Azure AI Language Services

Extract domain-specific entities from text documents using machine learning-powered Natural Language Processing (NLP) with Azure AI Language Services.

## Overview

This project demonstrates how to use Azure AI's custom entity recognition to:
- Define and recognize custom entity types (specific to your domain)
- Extract entity instances from text documents
- Obtain confidence scores for each recognized entity
- Batch process multiple documents efficiently

## How It Works - Step by Step

### 1. **Setup & Configuration**
   - Load Azure credentials from environment variables (.env file)
   - Connect to Azure AI Language Services using the endpoint and API key
   - Reference a custom-trained model (identified by project name and deployment name)

### 2. **Document Preparation**
   - Read all text files from the `ads/` folder containing sample documents
   - Create a batch of documents for processing

### 3. **Entity Extraction**
   - Submit the batch to Azure AI's `begin_recognize_custom_entities()` API
   - The API uses a trained custom model to identify entities in the text
   - Returns recognized entities with their categories and confidence scores

### 4. **Result Processing**
   - Retrieve the extraction results
   - Display each document name
   - Print all extracted entities with:
     - Entity text (the actual matched text)
     - Entity category (the type of entity)
     - Confidence score (0-1, how confident the model is)

### 5. **Error Handling**
   - Catch and display any API errors that occur during processing

## Project Structure

```
custom-entity-recognition/
├── custom-entities.py      # Main Python script for entity extraction
├── readme.md               # This file
└── ads/                    # Folder containing test documents
    ├── Ad 1.txt
    ├── Ad 2.txt
    └── ... (more test documents)
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure AI Language Service resource
- Custom-trained entity recognition model deployed in Azure Language Studio

### Installation

```bash
pip install azure-ai-textanalytics==5.3.0
```

### Configuration

Create a `.env` file in this directory with:

```
AI_SERVICE_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/
AI_SERVICE_KEY=<your-api-key>
PROJECT=<your-project-name>
DEPLOYMENT=<your-deployment-name>
```

### Running the Script

```bash
python custom-entities.py
```

## Output Example

```
Ad 1.txt
	Entity 'Product X' has category 'PRODUCT' with confidence score of '0.95'
	Entity 'John Smith' has category 'PERSON' with confidence score of '0.87'
Ad 2.txt
	Entity 'Company Inc' has category 'ORGANIZATION' with confidence score of '0.92'
```

## Current Status

⚠️ **Note**: As of 2024, Azure Language Studio is being deprecated in favor of Azure AI Foundry. Custom entity recognition functionality will be available through AI Foundry. Updates to this project are pending migration to the new platform.

