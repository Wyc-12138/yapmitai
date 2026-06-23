from io import BytesIO
from datetime import UTC, datetime
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.db.chroma import delete_knowledge_base, query_chunks, upsert_chunks
from app.models import Conversation, KnowledgeBase, KnowledgeDocument, Message, ModelConfig
from app.shared.external_ai import external_ai_service

settings = get_settings()
WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _time(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S")


def _library_dict(library: KnowledgeBase, document_count: int | None = None) -> dict:
    count = document_count
    if count is None:
        count = len(library.documents) if "documents" in library.__dict__ else 0
    embedding_config = library.__dict__.get("embedding_model_config")
    return {
        "id": library.id,
        "name": library.name,
        "description": library.description,
        "knowledgeType": library.knowledge_type,
        "status": library.status,
        "collectionCount": count,
        "embeddingModelConfigId": library.embedding_model_config_id,
        "embeddingModel": embedding_config.display_name if embedding_config else "",
        "embeddingModelCode": embedding_config.model_code if embedding_config else "",
        "createdAt": _time(library.created_at),
        "updatedAt": _time(library.updated_at),
    }


async def _default_model_config(db: AsyncSession, model_type: str) -> ModelConfig:
    config = await db.scalar(
        select(ModelConfig).where(
            ModelConfig.model_type == model_type,
            ModelConfig.enabled.is_(True),
            ModelConfig.is_default.is_(True),
        )
    )
    if not config:
        config = await db.scalar(
            select(ModelConfig).where(
                ModelConfig.model_type == model_type,
                ModelConfig.enabled.is_(True),
            )
        )
    if not config:
        raise ValueError(f"No enabled {model_type} model config is available")
    return config


async def _model_by_code_or_default(
    db: AsyncSession, model_type: str, model_code: str | None
) -> ModelConfig:
    if model_code:
        config = await db.scalar(
            select(ModelConfig).where(
                ModelConfig.model_type == model_type,
                ModelConfig.enabled.is_(True),
                ModelConfig.model_code == model_code,
            )
        )
        if config:
            return config
    return await _default_model_config(db, model_type)


async def _embedding_config_for_library(
    db: AsyncSession, library: KnowledgeBase
) -> ModelConfig:
    config = (
        await db.get(ModelConfig, library.embedding_model_config_id)
        if library.embedding_model_config_id
        else None
    )
    if config and config.model_type == "embedding" and config.enabled:
        return config
    config = await _default_model_config(db, "embedding")
    library.embedding_model_config_id = config.id
    library.updated_at = datetime.now(UTC)
    await db.commit()
    return config


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        chunks.append(normalized[start:end])
        if end == len(normalized):
            break
        start = end - overlap
    return chunks


def extract_docx_text(content: bytes) -> str:
    try:
        with ZipFile(BytesIO(content)) as archive:
            document_xml = archive.read("word/document.xml")
    except (BadZipFile, KeyError) as exc:
        raise ValueError("无法解析 DOCX 文件，请确认文件未损坏且格式正确") from exc

    root = ElementTree.fromstring(document_xml)
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", WORD_NAMESPACE):
        text = "".join(
            node.text or "" for node in paragraph.findall(".//w:t", WORD_NAMESPACE)
        ).strip()
        if text:
            paragraphs.append(text)
    if not paragraphs:
        raise ValueError("DOCX 文件中未提取到可用文本")
    return "\n".join(paragraphs)


def extract_pdf_text(content: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ValueError("PDF parsing is not available. Install pypdf on the backend.") from exc

    try:
        reader = PdfReader(BytesIO(content))
    except Exception as exc:
        raise ValueError("Unable to parse PDF file. Please verify the file is not corrupted.") from exc

    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)
    if not pages:
        raise ValueError("No extractable text was found in this PDF. Scanned PDFs need OCR first.")
    return "\n".join(pages)


async def status(db: AsyncSession) -> dict:
    bases = await db.scalar(select(func.count()).select_from(KnowledgeBase))
    documents = await db.scalar(select(func.count()).select_from(KnowledgeDocument))
    return {"count": documents or 0, "knowledgeBases": bases or 0, "status": "ready"}


async def get_model_config(
    db: AsyncSession, knowledge_base_id: str | None = None
) -> dict:
    library = (
        await db.scalar(
            select(KnowledgeBase)
            .where(KnowledgeBase.id == knowledge_base_id)
            .options(selectinload(KnowledgeBase.embedding_model_config))
        )
        if knowledge_base_id
        else await db.scalar(
            select(KnowledgeBase)
            .options(selectinload(KnowledgeBase.embedding_model_config))
            .order_by(KnowledgeBase.updated_at.desc())
        )
    )
    embedding_configs = (
        await db.scalars(
            select(ModelConfig).where(ModelConfig.model_type == "embedding", ModelConfig.enabled.is_(True))
        )
    ).all()
    chat_configs = (
        await db.scalars(
            select(ModelConfig).where(ModelConfig.model_type == "chat", ModelConfig.enabled.is_(True))
        )
    ).all()
    default_embedding = await _default_model_config(db, "embedding")
    default_chat = await _default_model_config(db, "chat")
    selected_embedding = library.embedding_model_config if library and library.embedding_model_config else default_embedding
    return {
        **external_ai_service.available_models(),
        "scope": "local-knowledge-base",
        "embeddingModels": [item.model_code for item in embedding_configs],
        "answerModels": [item.model_code for item in chat_configs],
        "embeddingModel": selected_embedding.model_code,
        "answerModel": default_chat.model_code,
    }


async def update_model_config(
    db: AsyncSession,
    knowledge_base_id: str,
    embedding_model: str,
    answer_model: str,
) -> dict:
    library = await db.get(KnowledgeBase, knowledge_base_id)
    if not library:
        raise ValueError("Local knowledge base not found")
    embedding_config = await _model_by_code_or_default(db, "embedding", embedding_model)
    chat_config = await _model_by_code_or_default(db, "chat", answer_model)
    library.embedding_model_config_id = embedding_config.id
    await db.execute(
        ModelConfig.__table__.update()
        .where(ModelConfig.model_type == "chat")
        .values(is_default=False)
    )
    chat_config.is_default = True
    library.updated_at = datetime.now(UTC)
    await db.commit()
    return await get_model_config(db, knowledge_base_id)


async def test_models(
    db: AsyncSession, knowledge_base_id: str, text: str
) -> dict:
    library = await db.get(KnowledgeBase, knowledge_base_id)
    if not library:
        raise ValueError("Local knowledge base not found")
    embedding_config = await _embedding_config_for_library(db, library)
    chat_config = await _default_model_config(db, "chat")
    embeddings = await external_ai_service.embed_with_config([text], embedding_config)
    generated = await external_ai_service.answer_with_config(
        text,
        [f"这是知识库“{library.name}”的模型连通性测试上下文。"],
        chat_config,
    )
    return {
        "knowledgeBaseId": library.id,
        "knowledgeBaseName": library.name,
        "embeddingModel": embedding_config.model_code,
        "embeddingDimensions": len(embeddings[0]),
        "answerModel": chat_config.model_code,
        **generated,
    }


async def list_local_libraries(
    db: AsyncSession,
    keyword: str | None = None,
    knowledge_type: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    document_count = func.count(KnowledgeDocument.id).label("document_count")
    statement = (
        select(KnowledgeBase, document_count)
        .outerjoin(KnowledgeDocument)
        .options(selectinload(KnowledgeBase.embedding_model_config))
        .group_by(KnowledgeBase.id)
    )
    if keyword:
        pattern = f"%{keyword}%"
        statement = statement.where(
            or_(KnowledgeBase.name.ilike(pattern), KnowledgeBase.description.ilike(pattern))
        )
    if knowledge_type:
        statement = statement.where(KnowledgeBase.knowledge_type == knowledge_type)
    total = await db.scalar(select(func.count()).select_from(statement.subquery()))
    rows = (
        await db.execute(
            statement.order_by(KnowledgeBase.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).all()
    return {
        "items": [_library_dict(library, count) for library, count in rows],
        "total": total or 0,
        "page": page,
        "pageSize": page_size,
    }


async def get_local_library(db: AsyncSession, library_id: str) -> dict | None:
    library = await db.scalar(
        select(KnowledgeBase)
        .where(KnowledgeBase.id == library_id)
        .options(
            selectinload(KnowledgeBase.documents),
            selectinload(KnowledgeBase.embedding_model_config),
        )
    )
    if not library:
        return None
    result = _library_dict(library)
    result["documents"] = [
        {
            "id": item.id,
            "filename": item.filename,
            "storagePath": item.storage_path,
            "status": item.processing_status,
            "chunkCount": item.chunk_count,
            "size": item.size,
            "createdAt": _time(item.created_at),
        }
        for item in library.documents
    ]
    return result


async def create_local_library(db: AsyncSession, payload: dict) -> dict:
    embedding_config = await _default_model_config(db, "embedding")
    library = KnowledgeBase(
        id=f"kb-{uuid4().hex[:10]}",
        name=payload["name"],
        description=payload["description"],
        knowledge_type=payload["knowledge_type"],
        status="ready",
        embedding_model_config_id=embedding_config.id,
    )
    db.add(library)
    await db.commit()
    library = await db.scalar(
        select(KnowledgeBase)
        .where(KnowledgeBase.id == library.id)
        .options(selectinload(KnowledgeBase.embedding_model_config))
    )
    return _library_dict(library, 0)


async def update_local_library(
    db: AsyncSession, library_id: str, payload: dict
) -> dict | None:
    library = await db.get(KnowledgeBase, library_id)
    if not library:
        return None
    for field in ("name", "description"):
        if payload.get(field):
            setattr(library, field, payload[field])
    library.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(library)
    count = await db.scalar(
        select(func.count()).select_from(KnowledgeDocument).where(
            KnowledgeDocument.knowledge_base_id == library_id
        )
    )
    return _library_dict(library, count or 0)


async def delete_local_library(db: AsyncSession, library_id: str) -> bool:
    library = await db.get(KnowledgeBase, library_id)
    if not library:
        return False
    paths = (
        await db.scalars(
            select(KnowledgeDocument.storage_path).where(
                KnowledgeDocument.knowledge_base_id == library_id
            )
        )
    ).all()
    await db.delete(library)
    await db.commit()
    delete_knowledge_base(library_id)
    for path in paths:
        Path(path).unlink(missing_ok=True)
    return True


async def add_document(
    db: AsyncSession,
    library_id: str,
    filename: str,
    content_type: str | None,
    content: bytes,
) -> dict | None:
    library = await db.get(KnowledgeBase, library_id)
    if not library:
        return None
    document_id = f"document-{uuid4().hex[:10]}"
    directory = Path(settings.knowledge_storage_dir) / library_id
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        directory = Path(gettempdir()) / "yapmitai" / "knowledge" / library_id
        directory.mkdir(parents=True, exist_ok=True)
    safe_name = Path(filename).name
    storage_path = directory / f"{document_id}-{safe_name}"
    storage_path.write_bytes(content)
    document = KnowledgeDocument(
        id=document_id,
        knowledge_base_id=library_id,
        filename=safe_name,
        storage_path=str(storage_path.resolve()),
        content_type=content_type or "application/octet-stream",
        size=len(content),
        processing_status="processing",
    )
    db.add(document)
    await db.flush()
    embedding_config = await _embedding_config_for_library(db, library)
    chat_config = await _default_model_config(db, "chat")
    try:
        if (content_type or "").startswith("image/"):
            source_kind = "image-description"
            text_content = await external_ai_service.describe_image_with_config(
                content, content_type or "image/jpeg", chat_config
            )
        elif (content_type or "").startswith("text/") or safe_name.lower().endswith((".txt", ".md")):
            source_kind = "text"
            text_content = content.decode("utf-8", errors="ignore")
        elif safe_name.lower().endswith(".docx") or content_type == (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            source_kind = "docx"
            text_content = extract_docx_text(content)
        elif safe_name.lower().endswith(".pdf") or content_type == "application/pdf":
            source_kind = "pdf"
            text_content = extract_pdf_text(content)
        else:
            raise ValueError(
                f"暂不支持解析文件类型：{safe_name}。当前支持 TXT、Markdown、DOCX 和图片"
            )
        chunks = split_text(text_content)
        if not chunks:
            raise ValueError(f"No extractable text was found in {safe_name}.")
        embeddings = await external_ai_service.embed_with_config(chunks, embedding_config)
        upsert_chunks(library_id, document_id, chunks, embeddings, safe_name)
        document.processing_status = "indexed"
        document.chunk_count = len(chunks)
        library.updated_at = datetime.now(UTC)
        await db.commit()
    except Exception as exc:
        document.processing_status = "failed"
        document.error_message = str(exc)
        await db.commit()
        raise
    return {
        "id": document.id,
        "libraryId": library_id,
        "filename": document.filename,
        "storagePath": document.storage_path,
        "contentType": document.content_type,
        "size": document.size,
        "status": document.processing_status,
        "embeddingModel": embedding_config.model_code,
        "answerModel": chat_config.model_code,
        "sourceKind": source_kind,
        "chunkCount": document.chunk_count,
        "createdAt": _time(document.created_at),
    }


async def query(
    db: AsyncSession,
    text: str,
    limit: int,
    answer_model: str | None = None,
    knowledge_base_id: str | None = None,
    conversation_id: str | None = None,
) -> dict:
    statement = select(KnowledgeBase).where(KnowledgeBase.status == "ready")
    if knowledge_base_id:
        statement = statement.where(KnowledgeBase.id == knowledge_base_id)
    libraries = (await db.scalars(statement)).all()
    if not libraries:
        raise ValueError("No local knowledge base is available")
    embedding_config = await _embedding_config_for_library(db, libraries[0])
    chat_config = (
        await _model_by_code_or_default(db, "chat", answer_model)
        if answer_model
        else await _default_model_config(db, "chat")
    )
    query_embedding = (await external_ai_service.embed_with_config(
        [text], embedding_config
    ))[0]
    matches: list[dict] = []
    for library in libraries:
        matches.extend(query_chunks(library.id, query_embedding, limit))
    matches.sort(key=lambda item: item["distance"])
    selected = matches[:limit]
    contexts = [item["content"] for item in selected]
    generated = await external_ai_service.answer_with_config(text, contexts, chat_config)

    conversation = await db.get(Conversation, conversation_id) if conversation_id else None
    if not conversation:
        conversation = Conversation(
            id=f"conversation-{uuid4().hex[:12]}",
            title=text[:80],
        )
        db.add(conversation)
        await db.flush()
    db.add_all(
        [
            Message(
                id=f"message-{uuid4().hex[:12]}",
                conversation_id=conversation.id,
                role="user",
                content=text,
                sources=[],
            ),
            Message(
                id=f"message-{uuid4().hex[:12]}",
                conversation_id=conversation.id,
                role="assistant",
                content=generated["answer"],
                model=chat_config.model_code,
                sources=[item["metadata"] for item in selected],
            ),
        ]
    )
    await db.commit()
    return {
        "query": text,
        "conversationId": conversation.id,
        "contexts": contexts,
        **generated,
    }


async def list_conversations(db: AsyncSession) -> list[dict]:
    rows = (
        await db.scalars(
            select(Conversation).order_by(Conversation.updated_at.desc()).limit(100)
        )
    ).all()
    return [
        {
            "id": item.id,
            "agentId": item.agent_id,
            "title": item.title,
            "createdAt": _time(item.created_at),
            "updatedAt": _time(item.updated_at),
        }
        for item in rows
    ]


async def get_conversation(db: AsyncSession, conversation_id: str) -> dict | None:
    conversation = await db.scalar(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .options(selectinload(Conversation.messages))
    )
    if not conversation:
        return None
    return {
        "id": conversation.id,
        "agentId": conversation.agent_id,
        "title": conversation.title,
        "messages": [
            {
                "id": item.id,
                "role": item.role,
                "content": item.content,
                "model": item.model,
                "sources": item.sources,
                "createdAt": _time(item.created_at),
            }
            for item in sorted(conversation.messages, key=lambda value: value.created_at)
        ],
    }
