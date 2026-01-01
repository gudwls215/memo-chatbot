"""MCP SSE 서버 - HTTP 서버로 실행"""
import asyncio
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
import uvicorn
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import app as mcp_app


# SSE Transport 생성
sse = SseServerTransport("/messages")


async def handle_sse(request):
    """SSE 엔드포인트"""
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp_app.run(
            streams[0], streams[1], mcp_app.create_initialization_options()
        )


# Starlette 앱
# handle_post_message를 직접 ASGI 앱으로 사용
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", app=sse.handle_post_message),
    ]
)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MCP 서버 (SSE 모드) 시작")
    print("=" * 60)
    print("서버 주소: http://localhost:8001")
    print("SSE 엔드포인트: http://localhost:8001/sse")
    print("\nCtrl+C를 눌러 서버를 종료할 수 있습니다.\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
