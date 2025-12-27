"""메모장 챗봇 실행 스크립트"""
import asyncio
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

from graph import create_graph

# 환경 변수 로드
load_dotenv()


async def run_chatbot():
    """챗봇 실행"""
    # 그래프 생성
    app = create_graph()
    
    print("=" * 60)
    print("🤖 메모장 챗봇에 오신 것을 환영합니다!")
    print("=" * 60)
    print("\n메모를 관리할 수 있도록 도와드리겠습니다.")
    print("예: '할 일 목록이라는 제목으로 메모를 만들어줘'")
    print("    '모든 메모를 보여줘'")
    print("    '메모 1번을 조회해줘'")
    print("    '메모 1번의 제목을 변경해줘'")
    print("    '메모 1번을 삭제해줘'")
    print("\n종료하려면 'quit', 'exit', 또는 '종료'를 입력하세요.\n")
    
    # 대화 히스토리 (상태로 관리)
    state = {"messages": []}
    
    while True:
        try:
            # 사용자 입력
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # 종료 명령 확인
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("\n챗봇을 종료합니다. 좋은 하루 되세요!")
                break
            
            # 사용자 메시지 추가
            state["messages"].append(HumanMessage(content=user_input))
            
            # 그래프 실행
            print("\n처리 중...")
            result = await app.ainvoke(state)
            
            # 상태 업데이트
            state = result
            
            # 마지막 응답 출력
            last_message = result["messages"][-1]
            
            print(f"\nBot: {last_message.content}\n")
            
        except KeyboardInterrupt:
            print("\n\n챗봇을 종료합니다. 좋은 하루 되세요!")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            print("FastAPI 백엔드가 실행 중인지 확인하세요 (http://localhost:8000)\n")


def main():
    """메인 함수"""
    asyncio.run(run_chatbot())


if __name__ == "__main__":
    main()
