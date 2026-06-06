import chromadb

from app.core.config import get_settings

settings = get_settings()
chroma_client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
