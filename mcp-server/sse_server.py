"""MCP 서버 - SSE를 통한 HTTP 서버로 실행"""
import asyncio
import sys
import os
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools
from server import app as mcp_app  # 기존 MCP 서버 앱 재사용


# SSE 엔드포인트
async def handle_sse(request):
    """SSE 연결 처리"""
    async with SseServerTransport("/messages") as transport:
        await mcp_app.run(
            transport.read_stream,
            transport.write_stream,
            mcp_app.create_initialization_options()
        )


async def handle_messages(request):
    """메시지 엔드포인트"""
    async with SseServerTransport("/messages") as transport:
        await mcp_app.run(
            transport.read_stream,
            transport.write_stream,
            mcp_app.create_initialization_options()
        )


# Starlette 앱 생성
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]
)


def main():
    """SSE 서버 실행"""
    print("=" * 60)
    print("🚀 MCP 서버 (SSE 모드) 시작")
    print("=" * 60)
    print("서버 주소: http://localhost:8001")
    print("SSE 엔드포인트: http://localhost:8001/sse")
    print("\nCtrl+C를 눌러 서버를 종료할 수 있습니다.\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )


if __name__ == "__main__":
    main()
