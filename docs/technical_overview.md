# Technical Overview

## Architecture

The system is built using a modular service-oriented architecture.

### Core Modules

```text
src/
├── answer_generation.py
├── azure_search.py
├── azure_storage.py
├── cache.py
├── config.py
├── document_processing.py
├── embeddings.py
├── ingestion.py
├── local_retrieval.py
```

---

## End-to-End Workflow

### Local Document Workspace

1. Upload PDF
2. Save document locally
3. Extract text using Azure Document Intelligence
4. Fallback to PyMuPDF if needed
5. Chunk extracted content
6. Generate embeddings
7. Store chunks locally
8. Perform semantic retrieval
9. Generate grounded response with Azure OpenAI

---

### Enterprise Azure Knowledge Base

1. Documents stored in Azure Blob Storage
2. Content extracted using Azure Document Intelligence
3. Chunked and embedded
4. Indexed into Azure AI Search
5. Queried through vector search
6. Retrieved context passed to Azure OpenAI
7. Grounded response returned to user

---

## Azure Services Used

- Azure OpenAI
- Azure AI Search
- Azure Blob Storage
- Azure Document Intelligence

---

## Environment Variables

```env
OPENAI_API_KEY=

OPENAI_MODEL=
OPENAI_EMBEDDING_MODEL=

AZURE_STORAGE_CONNECTION_STRING=
AZURE_STORAGE_CONTAINER=

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=
AZURE_DOCUMENT_INTELLIGENCE_KEY=

AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=
AZURE_SEARCH_INDEX_NAME=
```

---

## Local Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\\Scripts\\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## Deployment Notes

The application is currently optimized for local development and portfolio demonstration purposes.

Potential deployment targets include:

- Streamlit Community Cloud
- Azure App Service
- Render

---

## Future Improvements

- Authentication and user management
- Persistent chat history
- Multi-user document workspaces
- Real-time ingestion monitoring
- Hybrid retrieval strategies
- LangGraph orchestration
- Agentic workflows