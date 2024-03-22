import os
from chromadb.config import Settings

CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=os.path.join(os.path.dirname(__file__), "db"),
)
