from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_analyze_inquiry_requires_text() -> None:
    response = client.post(
        "/api/v1/inquiry/analyze",
        headers=headers,
        json={"inquiry_text": "   "},
    )
    assert response.status_code == 400


def test_analyze_inquiry_success(monkeypatch) -> None:
    async def fake_analyze(db, inquiry_text, source, sample_label=None):
        return {
            "id": "inq-test001",
            "inquiryText": inquiry_text,
            "source": source,
            "status": "done",
            "steps": [
                {"agent": "inquiry_analyst", "output": {"intent": "price_inquiry"}},
                {"agent": "smart_cs", "output": {"reply": "Thanks for your inquiry."}},
                {"agent": "follow_up", "output": {"priority": "medium"}},
            ],
            "summary": {
                "intent": "price_inquiry",
                "suggestedReply": "Thanks for your inquiry.",
            },
            "errorMessage": None,
            "createdAt": "2026-01-01T00:00:00+00:00",
            "inquiry": inquiry_text,
        }

    monkeypatch.setattr(
        "app.pages.enterprise.inquiry.service.analyze_inquiry",
        fake_analyze,
    )

    response = client.post(
        "/api/v1/inquiry/analyze",
        headers=headers,
        json={
            "inquiry_text": "Please send price for 500 bottles.",
            "source": "WhatsApp",
        },
    )

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["id"] == "inq-test001"
    assert payload["status"] == "done"
    assert payload["steps"][0]["output"]["intent"] == "price_inquiry"


def test_list_inquiry_history(monkeypatch) -> None:
    async def fake_list(db):
        return {
            "items": [
                {
                    "id": "inq-test001",
                    "inquiryText": "demo",
                    "source": "Email",
                    "status": "done",
                    "summary": {"intent": "product_info"},
                    "createdAt": "2026-01-01T00:00:00+00:00",
                }
            ],
            "total": 1,
        }

    monkeypatch.setattr(
        "app.pages.enterprise.inquiry.service.list_inquiry_history",
        fake_list,
    )

    response = client.get("/api/v1/inquiry/history", headers=headers)

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["total"] == 1
    assert payload["items"][0]["id"] == "inq-test001"


def test_delete_inquiry_history_item(monkeypatch) -> None:
    async def fake_delete(db, record_id):
        return record_id == "inq-test001"

    monkeypatch.setattr(
        "app.pages.enterprise.inquiry.service.delete_inquiry_record",
        fake_delete,
    )

    response = client.delete("/api/v1/inquiry/history/inq-test001", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == "inq-test001"


def test_delete_inquiry_history_batch(monkeypatch) -> None:
    async def fake_delete_many(db, record_ids):
        return {"deleted": len(record_ids), "ids": record_ids}

    monkeypatch.setattr(
        "app.pages.enterprise.inquiry.service.delete_inquiry_records",
        fake_delete_many,
    )

    response = client.post(
        "/api/v1/inquiry/history/delete",
        headers=headers,
        json={"ids": ["inq-a", "inq-b"]},
    )
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["deleted"] == 2
    assert payload["ids"] == ["inq-a", "inq-b"]
