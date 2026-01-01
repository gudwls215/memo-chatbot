"""LangGraph 챗봇 노드 구현 - MCPToolkit 사용"""
import os
import sys
import asyncio
from typing import Literal
from contextlib import AsyncExitStack
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from langchain_mcp import MCPToolkit

# 환경 변수 로드
load_dotenv()

# MCP 연결 모드 설정
MCP_MODE = os.getenv("MCP_MODE", "stdio")  # "stdio" 또는 "sse"
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")

# MCP 서버 경로 (stdio 모드용)
server_script = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'mcp-server', 'server.py')
)

# Python 실행 파일 경로
python_cmd = sys.executable

# 전역 변수
mcp_toolkit = None
mcp_session = None
exit_stack = None
tools = []
model = None


async def initialize_mcp_client():
    """MCP 클라이언트 초기화 및 도구 로드"""
    global mcp_toolkit, mcp_session, exit_stack, tools, model
    
    if mcp_toolkit is not None:
        return
    
    # AsyncExitStack으로 리소스 관리
    exit_stack = AsyncExitStack()
    await exit_stack.__aenter__()
    
    if MCP_MODE == "sse":
        # SSE 모드: 이미 실행 중인 MCP 서버에 연결
        print(f"🔗 SSE 모드로 MCP 서버에 연결 중... ({MCP_SERVER_URL})")
        read_stream, write_stream = await exit_stack.enter_async_context(
            sse_client(MCP_SERVER_URL)
        )
    else:
        # stdio 모드: MCP 서버를 subprocess로 실행
        print("🚀 stdio 모드로 MCP 서버 시작 중...")
        server_params = StdioServerParameters(
            command=python_cmd,
            args=[server_script],
            env=None
        )
        
        read_stream, write_stream = await exit_stack.enter_async_context(
            stdio_client(server_params)
        )
    
    # 세션 생성 및 초기화
    mcp_session = await exit_stack.enter_async_context(
        ClientSession(read_stream, write_stream)
    )
    await mcp_session.initialize()
    
    # MCPToolkit 생성 및 초기화
    mcp_toolkit = MCPToolkit(session=mcp_session)
    await mcp_toolkit.initialize()
    
    # 도구 가져오기
    tools = mcp_toolkit.get_tools()
    
    # 모델 초기화 (도구 바인딩)
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ).bind_tools(tools)
    
    mode_text = "SSE 서버" if MCP_MODE == "sse" else "내장 서버"
    print(f"✅ MCP {mode_text} 연결 완료! 사용 가능한 도구: {[t.name for t in tools]}")


async def cleanup_mcp_client():
    """MCP 클라이언트 정리"""
    global exit_stack
    
    if exit_stack is not None:
        await exit_stack.__aexit__(None, None, None)
        exit_stack = None


async def call_model(state):
    """LLM 호출 노드"""
    global model
    
    # MCP 클라이언트가 초기화되지 않았으면 초기화
    if model is None:
        await initialize_mcp_client()
    
    messages = state["messages"]
    response = await model.ainvoke(messages)
    return {"messages": [response]}


def should_continue(state) -> Literal["continue", "end"]:
    """도구 호출 필요 여부 결정"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 도구 호출이 있으면 계속, 없으면 종료
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"


async def call_tools(state):
    """도구 실행 노드 - MCP 클라이언트를 통해 실행"""
    global tools
    
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_messages = []
    
    # 도구 호출 실행
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # MCP 도구 찾기
        selected_tool = None
        for t in tools:
            if t.name == tool_name:
                selected_tool = t
                break
        
        if selected_tool:
            try:
                # MCP를 통해 도구 실행
                result = await selected_tool.ainvoke(tool_args)
                tool_messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"]
                    )
                )
            except Exception as e:
                tool_messages.append(
                    ToolMessage(
                        content=f"오류 발생: {str(e)}",
                        tool_call_id=tool_call["id"]
                    )
                )
    
    return {"messages": tool_messages}
