"""MCP SSE 서버 - HTTP 서버로 실행 (FastMCP)"""
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import mcp

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MCP 서버 (SSE 모드) 시작")
    print("=" * 60)
    print("서버 주소: http://localhost:8001")
    print("SSE 엔드포인트: http://localhost:8001/sse")
    print("\nCtrl+C를 눌러 서버를 종료할 수 있습니다.\n")
    
    # FastMCP의 내장 SSE 서버 실행 (포트 8001)
    mcp.run(transport="sse", port=8001)
