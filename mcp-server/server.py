"""MCP 서버 - 메모 관리 도구를 제공하는 MCP 서버 (FastMCP)"""
import sys
import os
from typing import Optional
from fastmcp import FastMCP

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools

# FastMCP 서버 인스턴스 생성
mcp = FastMCP("memo-manager")

@mcp.tool()
async def create_memo(title: str, content: Optional[str] = None) -> dict:
    """
    새로운 메모를 생성합니다.
    
    Args:
        title: 메모 제목 (필수, 최대 200자)
        content: 메모 내용 (선택, 최대 5000자)
    
    Returns:
        생성된 메모 정보 (id, title, content, created_at, updated_at)
    """
    return await tools.create_memo(title=title, content=content)


@mcp.tool()
async def list_memos(skip: int = 0, limit: int = 10) -> list:
    """
    메모 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 메모 수 (페이징, 기본값: 0)
        limit: 조회할 메모 수 (기본값: 10, 최대: 100)
    
    Returns:
        메모 목록
    """
    return await tools.list_memos(skip=skip, limit=limit)


@mcp.tool()
async def get_memo(memo_id: int) -> dict:
    """
    특정 메모를 조회합니다.
    
    Args:
        memo_id: 조회할 메모 ID
    
    Returns:
        메모 정보
    """
    return await tools.get_memo(memo_id=memo_id)


@mcp.tool()
async def update_memo(
    memo_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None
) -> dict:
    """
    메모를 수정합니다.
    
    Args:
        memo_id: 수정할 메모 ID
        title: 새 제목 (선택)
        content: 새 내용 (선택)
    
    Returns:
        수정된 메모 정보
    """
    return await tools.update_memo(memo_id=memo_id, title=title, content=content)


@mcp.tool()
async def delete_memo(memo_id: int) -> dict:
    """
    메모를 삭제합니다.
    
    Args:
        memo_id: 삭제할 메모 ID
    
    Returns:
        삭제 성공 메시지
    """
    return await tools.delete_memo(memo_id=memo_id)


if __name__ == "__main__":
    mcp.run()
