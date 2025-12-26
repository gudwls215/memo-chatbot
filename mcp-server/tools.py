"""메모 관리 MCP 도구 정의"""
import os
import httpx
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# FastAPI 백엔드 URL
MEMO_API_URL = os.getenv("MEMO_API_URL", "http://localhost:8000")
API_BASE = f"{MEMO_API_URL}/api/v1/memos"


async def create_memo(title: str, content: Optional[str] = None) -> Dict[str, Any]:
    """
    새로운 메모를 생성합니다.
    
    Args:
        title: 메모 제목 (필수, 최대 200자)
        content: 메모 내용 (선택, 최대 5000자)
    
    Returns:
        생성된 메모 정보 (id, title, content, created_at, updated_at)
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_BASE,
            json={"title": title, "content": content}
        )
        response.raise_for_status()
        return response.json()


async def list_memos(skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    """
    메모 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 메모 수 (페이징)
        limit: 조회할 메모 수 (최대 100)
    
    Returns:
        메모 목록
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_BASE,
            params={"skip": skip, "limit": limit}
        )
        response.raise_for_status()
        return response.json()


async def get_memo(memo_id: int) -> Dict[str, Any]:
    """
    특정 메모를 조회합니다.
    
    Args:
        memo_id: 조회할 메모 ID
    
    Returns:
        메모 정보
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/{memo_id}")
        response.raise_for_status()
        return response.json()


async def update_memo(
    memo_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None
) -> Dict[str, Any]:
    """
    메모를 수정합니다.
    
    Args:
        memo_id: 수정할 메모 ID
        title: 새 제목 (선택)
        content: 새 내용 (선택)
    
    Returns:
        수정된 메모 정보
    """
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if content is not None:
        update_data["content"] = content
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_BASE}/{memo_id}",
            json=update_data
        )
        response.raise_for_status()
        return response.json()


async def delete_memo(memo_id: int) -> Dict[str, str]:
    """
    메모를 삭제합니다.
    
    Args:
        memo_id: 삭제할 메모 ID
    
    Returns:
        삭제 성공 메시지
    """
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{API_BASE}/{memo_id}")
        response.raise_for_status()
        return {"status": "success", "message": f"메모 {memo_id}가 삭제되었습니다."}
