"""LangGraph 챗봇 노드 구현"""
import os
import sys
import asyncio
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage, HumanMessage
from langchain_core.tools import tool
from dotenv import load_dotenv

# MCP 도구 임포트
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp-server'))
from tools import create_memo, list_memos, get_memo, update_memo, delete_memo

# 환경 변수 로드
load_dotenv()


# MCP 도구를 LangChain 도구로 변환
@tool
async def create_memo_tool(title: str, content: str = None) -> dict:
    """
    새로운 메모를 생성합니다.
    
    Args:
        title: 메모 제목 (필수, 최대 200자)
        content: 메모 내용 (선택, 최대 5000자)
    
    Returns:
        생성된 메모 정보
    """
    return await create_memo(title, content)


@tool
async def list_memos_tool(skip: int = 0, limit: int = 10) -> dict:
    """
    메모 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 메모 수 (기본값: 0)
        limit: 조회할 메모 수 (기본값: 10, 최대: 100)
    
    Returns:
        메모 목록
    """
    return await list_memos(skip, limit)


@tool
async def get_memo_tool(memo_id: int) -> dict:
    """
    특정 메모를 조회합니다.
    
    Args:
        memo_id: 조회할 메모 ID
    
    Returns:
        메모 정보
    """
    return await get_memo(memo_id)


@tool
async def update_memo_tool(memo_id: int, title: str = None, content: str = None) -> dict:
    """
    메모를 수정합니다.
    
    Args:
        memo_id: 수정할 메모 ID
        title: 새 제목 (선택)
        content: 새 내용 (선택)
    
    Returns:
        수정된 메모 정보
    """
    return await update_memo(memo_id, title, content)


@tool
async def delete_memo_tool(memo_id: int) -> dict:
    """
    메모를 삭제합니다.
    
    Args:
        memo_id: 삭제할 메모 ID
    
    Returns:
        삭제 성공 메시지
    """
    return await delete_memo(memo_id)


# 도구 리스트
tools = [
    create_memo_tool,
    list_memos_tool,
    get_memo_tool,
    update_memo_tool,
    delete_memo_tool
]

# OpenAI 모델 초기화 (도구 바인딩)
model = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0
).bind_tools(tools)


def call_model(state):
    """LLM 호출 노드"""
    messages = state["messages"]
    response = model.invoke(messages)
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
    """도구 실행 노드"""
    messages = state["messages"]

    last_message = messages[-1]
    
    tool_messages = []
    
    # 도구 호출 실행
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # 해당 도구 찾기
        selected_tool = None
        for t in tools:
            if t.name == tool_name:
                selected_tool = t
                break
        
        if selected_tool:
            try:
                # 도구 실행
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
