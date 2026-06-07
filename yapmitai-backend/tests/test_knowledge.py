from io import BytesIO
from unittest.mock import AsyncMock
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi.testclient import TestClient

from app.main import app
from app.pages.enterprise.knowledge.agent import service

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def make_docx_bytes(paragraphs: list[str]) -> bytes:
    body = "".join(
        f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>" for text in paragraphs
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", document_xml)
    return buffer.getvalue()


def test_local_knowledge_crud_and_upload(monkeypatch) -> None:
    embed_mock = AsyncMock(return_value=[[0.1, 0.2, 0.3]])
    monkeypatch.setattr(service.external_ai_service, "embed_with_config", embed_mock)
    created = client.post(
        "/api/v1/knowledge/local-libraries",
        headers=headers,
        json={
            "name": "测试知识库",
            "knowledge_type": "text",
            "description": "用于验证本地知识库接口",
        },
    )
    assert created.status_code == 200
    library = created.json()["data"]
    library_id = library["id"]
    assert library["knowledgeType"] == "text"

    listed = client.get(
        "/api/v1/knowledge/local-libraries?page_size=100",
        headers=headers,
    )
    assert listed.status_code == 200
    assert any(item["id"] == library_id for item in listed.json()["data"]["items"])

    uploaded = client.post(
        f"/api/v1/knowledge/local-libraries/{library_id}/collections",
        headers=headers,
        files={"file": ("knowledge.txt", b"YAPMITAI knowledge", "text/plain")},
    )
    assert uploaded.status_code == 200
    assert uploaded.json()["data"]["status"] == "indexed"
    assert uploaded.json()["data"]["embeddingModel"] == "text-embedding-3-small"
    embed_mock.assert_awaited_once()

    detail = client.get(
        f"/api/v1/knowledge/local-libraries/{library_id}",
        headers=headers,
    )
    assert detail.status_code == 200
    assert detail.json()["data"]["collectionCount"] == 1

    deleted = client.delete(
        f"/api/v1/knowledge/local-libraries/{library_id}",
        headers=headers,
    )
    assert deleted.status_code == 200
    assert deleted.json()["data"]["deleted"] is True


def test_text_split_uses_500_with_50_overlap() -> None:
    text = "".join(str(index % 10) for index in range(900))
    chunks = service.split_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 2
    assert len(chunks[0]) == 500
    assert chunks[0][-50:] == chunks[1][:50]


def test_extract_docx_text_reads_document_body() -> None:
    content = make_docx_bytes(
        ["人怎样才算不朽？", "胡适《不朽》讨论人的生命价值与持续影响。"]
    )
    extracted = service.extract_docx_text(content)
    assert "人怎样才算不朽" in extracted
    assert "胡适《不朽》" in extracted


def test_docx_upload_embeds_document_body(monkeypatch) -> None:
    embedded_texts: list[str] = []

    async def embed_spy(texts, _config):
        embedded_texts.extend(texts)
        return [[0.1, 0.2, 0.3] for _ in texts]

    monkeypatch.setattr(service.external_ai_service, "embed_with_config", embed_spy)
    created = client.post(
        "/api/v1/knowledge/local-libraries",
        headers=headers,
        json={
            "name": "DOCX 正文解析测试",
            "knowledge_type": "text",
            "description": "验证上传后向量化正文而不是文件名",
        },
    )
    library_id = created.json()["data"]["id"]
    content = make_docx_bytes(
        ["人怎样才算不朽？", "胡适认为，不朽体现为个人对社会留下的持续影响。"]
    )

    uploaded = client.post(
        f"/api/v1/knowledge/local-libraries/{library_id}/collections",
        headers=headers,
        files={
            "file": (
                "人怎样才算不朽.docx",
                content,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert uploaded.status_code == 200
    assert uploaded.json()["data"]["sourceKind"] == "docx"
    assert any("胡适认为" in chunk for chunk in embedded_texts)
    assert not any(chunk == "文件：人怎样才算不朽.docx" for chunk in embedded_texts)
    client.delete(
        f"/api/v1/knowledge/local-libraries/{library_id}",
        headers=headers,
    )


def test_model_config() -> None:
    response = client.get("/api/v1/knowledge/model-config", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "text-embedding-3-small" in data["embeddingModels"]
    assert "gpt-4o-mini" in data["answerModels"]


def test_real_model_test_endpoint(monkeypatch) -> None:
    embed_mock = AsyncMock(return_value=[[0.1, 0.2, 0.3, 0.4]])
    answer_mock = AsyncMock(
        return_value={
            "answer": "模型连接正常",
            "model": "gpt-4o-mini",
            "usage": {"total_tokens": 12},
        }
    )
    monkeypatch.setattr(service.external_ai_service, "embed_with_config", embed_mock)
    monkeypatch.setattr(service.external_ai_service, "answer_with_config", answer_mock)
    created = client.post(
        "/api/v1/knowledge/local-libraries",
        headers=headers,
        json={
            "name": "模型测试知识库",
            "knowledge_type": "text",
            "description": "验证真实模型测试接口",
        },
    )
    library_id = created.json()["data"]["id"]

    configured = client.put(
        "/api/v1/knowledge/model-config",
        headers=headers,
        json={
            "knowledge_base_id": library_id,
            "embedding_model": "text-embedding-3-large",
            "answer_model": "gpt-4.1-mini",
        },
    )
    assert configured.status_code == 200
    assert configured.json()["data"]["embeddingModel"] == "text-embedding-3-large"

    tested = client.post(
        "/api/v1/knowledge/model-test",
        headers=headers,
        json={"knowledge_base_id": library_id, "text": "测试模型"},
    )
    assert tested.status_code == 200
    assert tested.json()["data"]["embeddingDimensions"] == 4
    assert tested.json()["data"]["answer"] == "模型连接正常"
    embed_mock.assert_awaited_once()
    answer_mock.assert_awaited_once()
    client.delete(
        f"/api/v1/knowledge/local-libraries/{library_id}",
        headers=headers,
    )


def test_image_upload_uses_external_vision_and_embedding(monkeypatch) -> None:
    describe_mock = AsyncMock(return_value="一张包含品牌包装的商品图片")
    embed_mock = AsyncMock(return_value=[[0.4, 0.5]])
    monkeypatch.setattr(
        service.external_ai_service,
        "describe_image_with_config",
        describe_mock,
    )
    monkeypatch.setattr(service.external_ai_service, "embed_with_config", embed_mock)

    created = client.post(
        "/api/v1/knowledge/local-libraries",
        headers=headers,
        json={
            "name": "图片测试库",
            "knowledge_type": "image",
            "description": "验证图片外部模型处理",
        },
    )
    library_id = created.json()["data"]["id"]

    uploaded = client.post(
        f"/api/v1/knowledge/local-libraries/{library_id}/collections",
        headers=headers,
        files={"file": ("product.png", b"fake-image", "image/png")},
    )
    assert uploaded.status_code == 200
    data = uploaded.json()["data"]
    assert data["sourceKind"] == "image-description"
    describe_mock.assert_awaited_once()
    embed_mock.assert_awaited_once()
    client.delete(
        f"/api/v1/knowledge/local-libraries/{library_id}",
        headers=headers,
    )
