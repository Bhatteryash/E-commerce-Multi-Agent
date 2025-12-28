from pymongo import MongoClient
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials and cluster info
username = quote_plus(os.getenv("MONGO_USER", ""))
password = quote_plus(os.getenv("MONGO_PASS", ""))
cluster = os.getenv("MONGO_CLUSTER", "")
db_name = os.getenv("MONGO_DB", "test")

# Build Mongo URI safely
mongo_url = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Personal-Cluster"

# Lazy initialization - don't connect at import time
_client = None
_db = None

def get_client():
    """Get or create the MongoDB client instance."""
    global _client
    if _client is None:
        _client = MongoClient(mongo_url)
    return _client

def get_db():
    """Get the database instance."""
    global _db
    if _db is None:
        client = get_client()
        _db = client[db_name]
    return _db

