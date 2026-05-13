import os
import json

INGESTION_CACHE_FILE = os.path.join("data", "ingestion_cache.json")


def load_ingestion_cache():
    if not os.path.exists(INGESTION_CACHE_FILE):
        return {}

    with open(INGESTION_CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_ingestion_cache(cache_data):
    with open(INGESTION_CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache_data, file, indent=4)