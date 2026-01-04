#!/usr/bin/env python
"""MCP 서버 독립 실행 스크립트

이 스크립트는 MCP 서버를 독립적으로 실행합니다.
클라이언트는 별도로 실행할 수 있습니다.

사용법:
    python run_mcp_server.py          # stdio 모드 (기본)
    python run_mcp_server.py --sse    # SSE HTTP 서버 모드
"""
import sys
import argparse
from pathlib import Path

# mcp-server 디렉토리를 Python 경로에 추가
mcp_server_dir = Path(__file__).parent / "mcp-server"
sys.path.insert(0, str(mcp_server_dir))


def main():
    parser = argparse.ArgumentParser(description="MCP 서버 실행")
    parser.add_argument(
        "--mode",
        choices=["stdio", "sse"],
        default="stdio",
        help="서버 실행 모드 (기본: stdio)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="SSE 모드 포트 (기본: 8001)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "sse":
        print("SSE 모드로 MCP 서버 시작...")
        import uvicorn
        from mcp_server_sse import app
        
        print("=" * 60)
        print("🚀 MCP 서버 (SSE 모드) 시작")
        print("=" * 60)
        print(f"서버 주소: http://localhost:{args.port}")
        print(f"SSE 엔드포인트: http://localhost:{args.port}/sse")
        print("\nCtrl+C를 눌러 서버를 종료할 수 있습니다.\n")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=args.port,
            log_level="info"
        )
    else:
        print("stdio 모드로 MCP 서버 시작...")
        print("(클라이언트가 이 서버에 연결하기를 기다립니다)")
        from server import mcp
        mcp.run()


if __name__ == "__main__":
    main()
