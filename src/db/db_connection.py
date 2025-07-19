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

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client[db_name]

def get_db():
    """Get the database instance."""
    return db
