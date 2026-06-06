import os
import logging
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

async def api_get(path: str):
    """Make an asynchronous GET request to the backend API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_BASE}{path}", timeout=8)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning(f"GET {path} failed: {e}")
        return None

async def api_post(path: str, data: dict):
    """Make an asynchronous POST request to the backend API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_BASE}{path}", json=data, timeout=8)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning(f"POST {path} failed: {e}")
        return None

async def api_patch(path: str, data: dict):
    """Make an asynchronous PATCH request to the backend API."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.patch(f"{API_BASE}{path}", json=data, timeout=8)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning(f"PATCH {path} failed: {e}")
        return None

async def get_subscriber(telegram_id: str):
    """Fetch subscriber information by Telegram ID."""
    return await api_get(f"/api/subscribers/{telegram_id}")

async def register_subscriber(user):
    """Register a new subscriber in the system."""
    return await api_post("/api/subscribers", {
        "telegram_id": str(user.id),
        "first_name":  user.first_name,
        "username":    user.username,
    })

async def save_class(telegram_id: str, class_code: str):
    """Associate a class code with a subscriber."""
    return await api_patch(
        f"/api/subscribers/{telegram_id}/class",
        {"telegram_id": telegram_id, "class_code": class_code},
    )

async def save_language(telegram_id: str, language: str):
    """Save the subscriber's language preference."""
    return await api_patch(
        f"/api/subscribers/{telegram_id}/language",
        {"language": language},
    )

async def get_classes():
    """Retrieve all available school classes."""
    return await api_get("/api/classes")

async def get_homework(class_code: str):
    """Retrieve homework for a specific class code."""
    return await api_get(f"/api/homework/{class_code}")

async def get_holidays():
    """Retrieve upcoming holidays."""
    return await api_get("/api/holidays")

async def fetch_file(url: str) -> bytes | None:
    """Fetch file content bytes asynchronously with 15s timeout boundary."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.content
    except Exception as e:
        logger.warning(f"Failed to fetch file from {url}: {e}")
    return None
