import streamlit as st
from azure.storage.blob import BlobServiceClient

from src.config import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER


def get_blob_service_client():
    if not AZURE_STORAGE_CONNECTION_STRING:
        st.error("Azure Storage connection string is missing.")
        return None

    try:
        return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    except Exception as e:
        st.error(f"Error creating BlobServiceClient: {e}")
        return None


def list_blobs_in_container():
    blob_service_client = get_blob_service_client()
    if blob_service_client is None:
        return []

    try:
        container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)
        blobs = container_client.list_blobs()
        return [blob.name for blob in blobs]
    except Exception as e:
        st.error(f"Error listing blobs: {e}")
        return []


def download_blob_to_bytes(blob_name):
    blob_service_client = get_blob_service_client()
    if blob_service_client is None:
        return None

    try:
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER,
            blob=blob_name
        )
        return blob_client.download_blob().readall()
    except Exception as e:
        st.error(f"Error downloading blob '{blob_name}': {e}")
        return None