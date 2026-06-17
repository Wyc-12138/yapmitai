"""Demo media service — text-to-image / text-to-video generation."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

import httpx

from app.core.config import get_settings

settings = get_settings()

# In-memory video task store (per REASONIX.md: no database tables)
_video_tasks: dict[str, dict] = {}


def _media_dir(sub: str) -> Path:
    base = Path(settings.generated_media_dir)
    target = base / sub
    target.mkdir(parents=True, exist_ok=True)
    return target


def _save_bytes(data: bytes, sub: str, stem: str, ext: str) -> tuple[str, str]:
    """Save bytes to storage/generated/<sub>/<stem>.<ext>, return (filename, url_path)."""
    filename = f"{stem}.{ext}"
    filepath = _media_dir(sub) / filename
    filepath.write_bytes(data)
    url = f"/generated/{sub}/{filename}"
    return filename, url


def _is_dashscope(url: str) -> bool:
    return "dashscope.aliyuncs.com" in url


async def _fetch_image_openai(prompt: str, size: str, client: httpx.AsyncClient) -> bytes:
    payload = {
        "model": settings.image_model_name,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json",
    }
    resp = await client.post(
        f"{settings.image_api_base_url.rstrip('/')}/images/generations",
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    b64 = data["data"][0]["b64_json"]
    return base64.b64decode(b64)


async def _fetch_image_dashscope(prompt: str, size: str, client: httpx.AsyncClient) -> bytes:
    """DashScope Tongyi Wanxiang (通义万相) — async task → poll → download."""
    # DashScope image API uses /api/v1/ prefix, NOT /compatible-mode/v1/
    base = "https://dashscope.aliyuncs.com/api/v1"

    create_payload = {
        "model": settings.image_model_name or "wan2.1-t2i-turbo",
        "input": {"prompt": prompt},
        "parameters": {"size": size.replace("x", "*"), "n": 1},
    }
    headers = {
        "Authorization": f"Bearer {settings.image_api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    create_resp = await client.post(
        f"{base}/services/aigc/text2image/image-synthesis",
        json=create_payload,
        headers=headers,
    )
    create_resp.raise_for_status()
    create_data = create_resp.json()
    task_id = create_data.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"DashScope did not return task_id: {create_data}")

    # Step 2: Poll until done (max 2 minutes)
    for _ in range(24):
        await asyncio.sleep(5)
        status_resp = await client.get(
            f"{base}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {settings.image_api_key}"},
        )
        status_resp.raise_for_status()
        status_data = status_resp.json()
        output = status_data.get("output", {})
        task_status = output.get("task_status", "RUNNING")

        if task_status == "SUCCEEDED":
            results = output.get("results", [])
            if not results or not results[0].get("url"):
                raise RuntimeError("DashScope returned SUCCEEDED but no image URL")
            image_url = results[0]["url"]
            async with httpx.AsyncClient(timeout=60) as dl_client:
                dl_resp = await dl_client.get(image_url)
                dl_resp.raise_for_status()
            return dl_resp.content

        if task_status == "FAILED":
            raise RuntimeError(output.get("message", "DashScope image generation failed"))

    raise RuntimeError("DashScope image generation timed out after 2 minutes")


async def _fetch_image(prompt: str, size: str) -> bytes:
    """Call external image API. Auto-detects OpenAI vs DashScope (通义万相)."""
    auth_headers = {
        "Authorization": f"Bearer {settings.image_api_key}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(
        timeout=settings.agent_timeout_seconds, headers=auth_headers
    ) as client:
        if _is_dashscope(settings.image_api_base_url):
            return await _fetch_image_dashscope(prompt, size, client)
        else:
            return await _fetch_image_openai(prompt, size, client)


async def text_to_image(prompt: str, size: str = "1024x1024", style: str = "natural", quantity: int = 1) -> list[dict]:
    if not settings.image_api_key:
        raise RuntimeError("IMAGE_API_KEY is not configured — check .env")

    results: list[dict] = []
    for _ in range(quantity):
        image_bytes = await _fetch_image(prompt, size)
        stem = f"{uuid.uuid4().hex[:12]}"
        filename, url = _save_bytes(image_bytes, "images", stem, "png")
        results.append({"url": url, "filename": filename, "size": size, "prompt": prompt})
    return results


async def text_to_video(prompt: str, ratio: str = "16:9", duration: int = 5, style: str = "cinematic") -> dict:
    if not settings.video_api_key:
        raise RuntimeError("VIDEO_API_KEY is not configured — check .env")

    task_id = str(uuid.uuid4())
    _video_tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "prompt": prompt,
        "ratio": ratio,
        "duration": duration,
        "style": style,
        "created_at": datetime.now(UTC).isoformat(),
        "url": None,
        "filename": None,
        "error": None,
    }

    # Kick off async generation
    asyncio.ensure_future(_run_video_task(task_id, prompt, ratio, duration, style))

    return {"task_id": task_id, "status": "pending"}


async def _run_video_task(task_id: str, prompt: str, ratio: str, duration: int, style: str) -> None:
    """Background task: create video via external API, poll until complete, save result."""
    task = _video_tasks.get(task_id)
    if not task:
        return

    try:
        task["status"] = "running"
        is_ds = _is_dashscope(settings.video_api_base_url)

        if is_ds:
            remote_task_id = await _create_video_dashscope(prompt, ratio)
            vid_url = await _poll_video_dashscope(remote_task_id)
        else:
            remote_task_id = await _create_video_openai(prompt, ratio, duration, style)
            vid_url = await _poll_video_openai(remote_task_id)

        # Download and save locally
        async with httpx.AsyncClient(timeout=120) as dl_client:
            dl_resp = await dl_client.get(vid_url)
            dl_resp.raise_for_status()
        stem = task_id.replace("-", "")[:12]
        filename, local_url = _save_bytes(dl_resp.content, "videos", stem, "mp4")
        task["status"] = "completed"
        task["url"] = local_url
        task["filename"] = filename

    except Exception as exc:
        task["status"] = "failed"
        task["error"] = str(exc)


async def _create_video_openai(prompt: str, ratio: str, duration: int, style: str) -> str:
    payload = {
        "model": settings.video_model_name,
        "prompt": prompt,
        "aspect_ratio": ratio,
        "duration": duration,
        "style": style,
    }
    headers = {
        "Authorization": f"Bearer {settings.video_api_key}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=settings.agent_timeout_seconds) as client:
        resp = await client.post(
            f"{settings.video_api_base_url.rstrip('/')}/videos/generations",
            json=payload, headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()
        rid = data.get("id") or data.get("task_id")
        if not rid:
            raise RuntimeError("Video API did not return a task ID")
        return rid


async def _poll_video_openai(remote_task_id: str) -> str:
    headers = {"Authorization": f"Bearer {settings.video_api_key}"}
    async with httpx.AsyncClient(timeout=settings.agent_timeout_seconds) as client:
        for _ in range(60):
            await asyncio.sleep(5)
            resp = await client.get(
                f"{settings.video_api_base_url.rstrip('/')}/videos/generations/{remote_task_id}",
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status", "running")
            if status == "completed":
                url = data.get("video_url") or data.get("url")
                if not url:
                    raise RuntimeError("Video completed but no URL returned")
                return url
            if status == "failed":
                raise RuntimeError(data.get("error", {}).get("message", "Video generation failed"))
    raise RuntimeError("Video generation timed out after 5 minutes")


async def _create_video_dashscope(prompt: str, ratio: str) -> str:
    base = "https://dashscope.aliyuncs.com/api/v1"
    payload = {
        "model": settings.video_model_name or "cogvideox-v1",
        "input": {"prompt": prompt},
        "parameters": {"size": _dashscope_video_size(ratio)},
    }
    headers = {
        "Authorization": f"Bearer {settings.video_api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    async with httpx.AsyncClient(timeout=settings.agent_timeout_seconds) as client:
        resp = await client.post(
            f"{base}/services/aigc/video-generation/video-synthesis",
            json=payload, headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()
        rid = data.get("output", {}).get("task_id")
        if not rid:
            raise RuntimeError(f"DashScope video did not return task_id: {data}")
        return rid


async def _poll_video_dashscope(remote_task_id: str) -> str:
    base = "https://dashscope.aliyuncs.com/api/v1"
    headers = {"Authorization": f"Bearer {settings.video_api_key}"}
    async with httpx.AsyncClient(timeout=30) as client:
        for _ in range(120):
            await asyncio.sleep(5)
            resp = await client.get(f"{base}/tasks/{remote_task_id}", headers=headers)
            resp.raise_for_status()
            data = resp.json()
            output = data.get("output", {})
            status = output.get("task_status", "RUNNING")
            if status == "SUCCEEDED":
                # video_url may be at output level or in results[0]
                vid = output.get("video_url")
                if not vid:
                    results = output.get("results", [])
                    if results:
                        vid = results[0].get("video_url") or results[0].get("url")
                if not vid:
                    raise RuntimeError(f"DashScope video SUCCEEDED but no video_url found")
                return vid
            if status == "FAILED":
                raise RuntimeError(output.get("message", "DashScope video generation failed"))
    raise RuntimeError("DashScope video generation timed out after 10 minutes")


def _dashscope_video_size(ratio: str) -> str:
    return {"16:9": "1280*720", "9:16": "720*1280", "1:1": "720*720"}.get(ratio, "1280*720")


def get_video_status(task_id: str) -> dict | None:
    return _video_tasks.get(task_id)
