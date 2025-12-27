"""MCP 서버 - 메모 관리 도구를 제공하는 MCP 서버"""
import asyncio
import sys
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl
import json

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools


# MCP 서버 인스턴스 생성
app = Server("memo-manager")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록 반환"""
    return [
        Tool(
            name="create_memo",
            description="새로운 메모를 생성합니다. 제목은 필수이며, 내용은 선택사항입니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "메모 제목 (최대 200자)",
                    },
                    "content": {
                        "type": "string",
                        "description": "메모 내용 (최대 5000자, 선택사항)",
                    },
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="list_memos",
            description="메모 목록을 조회합니다. 페이징을 지원합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {
                        "type": "integer",
                        "description": "건너뛸 메모 수 (기본값: 0)",
                        "default": 0,
                    },
                    "limit": {
                        "type": "integer",
                        "description": "조회할 메모 수 (기본값: 10, 최대: 100)",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="get_memo",
            description="특정 메모의 상세 정보를 조회합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "memo_id": {
                        "type": "integer",
                        "description": "조회할 메모 ID",
                    },
                },
                "required": ["memo_id"],
            },
        ),
        Tool(
            name="update_memo",
            description="메모를 수정합니다. 제목이나 내용 중 하나 이상을 제공해야 합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "memo_id": {
                        "type": "integer",
                        "description": "수정할 메모 ID",
                    },
                    "title": {
                        "type": "string",
                        "description": "새 제목 (선택사항)",
                    },
                    "content": {
                        "type": "string",
                        "description": "새 내용 (선택사항)",
                    },
                },
                "required": ["memo_id"],
            },
        ),
        Tool(
            name="delete_memo",
            description="메모를 삭제합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "memo_id": {
                        "type": "integer",
                        "description": "삭제할 메모 ID",
                    },
                },
                "required": ["memo_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """도구 호출 처리"""
    try:
        if name == "create_memo":
            result = await tools.create_memo(
                title=arguments["title"],
                content=arguments.get("content")
            )
        elif name == "list_memos":
            result = await tools.list_memos(
                skip=arguments.get("skip", 0),
                limit=arguments.get("limit", 10)
            )
        elif name == "get_memo":
            result = await tools.get_memo(memo_id=arguments["memo_id"])
        elif name == "update_memo":
            result = await tools.update_memo(
                memo_id=arguments["memo_id"],
                title=arguments.get("title"),
                content=arguments.get("content")
            )
        elif name == "delete_memo":
            result = await tools.delete_memo(memo_id=arguments["memo_id"])
        else:
            raise ValueError(f"알 수 없는 도구: {name}")
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"오류 발생: {str(e)}")]


async def main():
    """MCP 서버 실행"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
