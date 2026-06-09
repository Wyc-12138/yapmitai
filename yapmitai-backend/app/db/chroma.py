import chromadb
from chromadb.config import Settings
from pathlib import Path
from tempfile import gettempdir

from app.core.config import get_settings

settings = get_settings()


def _fallback_chroma_path() -> str:
    return str((Path(gettempdir()) / "yapmitai" / "chroma").resolve())


def get_chroma_client(path: str | None = None):
    return chromadb.PersistentClient(
        path=path or settings.chroma_persist_dir,
        settings=Settings(anonymized_telemetry=False),
    )


def collection_name(knowledge_base_id: str) -> str:
    return f"knowledge_{knowledge_base_id.replace('-', '_')}"


def upsert_chunks(
    knowledge_base_id: str,
    document_id: str,
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
) -> None:
    name = collection_name(knowledge_base_id)
    try:
        collection = get_chroma_client().get_or_create_collection(name)
    except Exception:
        collection = get_chroma_client(_fallback_chroma_path()).get_or_create_collection(name)
    collection.upsert(
        ids=[f"{document_id}:{index}" for index in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "document_id": document_id,
                "knowledge_base_id": knowledge_base_id,
                "filename": filename,
                "position": index,
            }
            for index in range(len(chunks))
        ],
    )


def query_chunks(
    knowledge_base_id: str, embedding: list[float], limit: int
) -> list[dict]:
    name = collection_name(knowledge_base_id)
    try:
        collection = get_chroma_client().get_or_create_collection(name)
    except Exception:
        collection = get_chroma_client(_fallback_chroma_path()).get_or_create_collection(name)
    if collection.count() == 0:
        return []
    result = collection.query(
        query_embeddings=[embedding],
        n_results=min(limit, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "content": document,
            "metadata": metadata,
            "distance": distance,
        }
        for document, metadata, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            strict=True,
        )
    ]


def delete_knowledge_base(knowledge_base_id: str) -> None:
    try:
        get_chroma_client().delete_collection(collection_name(knowledge_base_id))
    except Exception:
        try:
            get_chroma_client(_fallback_chroma_path()).delete_collection(collection_name(knowledge_base_id))
        except Exception:
            return
