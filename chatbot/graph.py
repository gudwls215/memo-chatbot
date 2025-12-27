"""LangGraph 상태 정의 및 워크플로우 구조"""
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class ChatbotState(TypedDict):
    """챗봇 상태 정의"""
    # 메시지 히스토리 (자동으로 메시지를 추가)
    messages: Annotated[Sequence[BaseMessage], add_messages]


def create_graph():
    """LangGraph 워크플로우 생성"""
    from nodes import call_model, should_continue, call_tools
    
    # 그래프 생성
    workflow = StateGraph(ChatbotState)
    
    # 노드 추가
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)
    
    # 진입점 설정
    workflow.set_entry_point("agent")
    
    # 조건부 엣지 추가
    # agent 노드 실행 후 도구 호출이 필요한지 확인
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",  # 도구 호출 필요
            "end": END  # 대화 종료
        }
    )
    
    # tools 노드 실행 후 다시 agent로
    workflow.add_edge("tools", "agent")
    
    # 그래프 컴파일
    return workflow.compile()
