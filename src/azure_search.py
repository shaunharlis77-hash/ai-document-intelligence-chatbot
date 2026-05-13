import streamlit as st

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)
from azure.search.documents.models import VectorizedQuery

from src.config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_KEY,
    AZURE_SEARCH_INDEX_NAME,
)
from src.embeddings import get_embedding


def get_search_index_client():
    if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_KEY:
        st.error("Azure AI Search endpoint or key is missing.")
        return None

    try:
        return SearchIndexClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY),
        )
    except Exception as e:
        st.error(f"Error creating SearchIndexClient: {e}")
        return None


def create_search_index():
    index_client = get_search_index_client()
    if index_client is None:
        return

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="source_file", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="chunk_number", type=SearchFieldDataType.Int32, filterable=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="default-vector-profile",
        ),
    ]

    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="default-vector-profile",
                algorithm_configuration_name="default-hnsw",
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(name="default-hnsw")
        ],
    )

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
    )

    try:
        index_client.create_index(index)
        st.success(f"Search index '{AZURE_SEARCH_INDEX_NAME}' created successfully.")
    except Exception as e:
        st.warning(f"Index may already exist or failed to create: {e}")


def get_search_client():
    if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_KEY:
        st.error("Azure AI Search endpoint or key is missing.")
        return None

    try:
        return SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY),
        )
    except Exception as e:
        st.error(f"Error creating SearchClient: {e}")
        return None


def upload_chunks_to_search(chunk_documents):
    search_client = get_search_client()
    if search_client is None:
        return False

    try:
        results = search_client.upload_documents(documents=chunk_documents)
        successful_uploads = sum(1 for result in results if result.succeeded)

        st.success(f"Uploaded {successful_uploads} chunk(s) to Azure AI Search.")
        return True

    except Exception as e:
        st.error(f"Error uploading chunks to Azure AI Search: {e}")
        return False


def ensure_search_index_exists():
    index_client = get_search_index_client()
    if index_client is None:
        return False

    try:
        existing_index_names = [index.name for index in index_client.list_indexes()]

        if AZURE_SEARCH_INDEX_NAME not in existing_index_names:
            create_search_index()

        return True

    except Exception as e:
        st.error(f"Error checking or creating Azure AI Search index: {e}")
        return False


def search_azure_index(query, top_k=5):
    search_client = get_search_client()
    if search_client is None:
        return []

    try:
        query_embedding = get_embedding(query)

        if query_embedding is None:
            return []

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields="embedding",
        )

        results = search_client.search(
            search_text=None,
            vector_queries=[vector_query],
            top=top_k,
        )

        chunks = []

        for result in results:
            chunks.append({
                "content": result["content"],
                "source_file": result["source_file"],
            })

        return chunks

    except Exception as e:
        st.error(f"Error querying Azure AI Search: {e}")
        return []