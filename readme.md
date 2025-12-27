# 메모장 챗봇 (LangGraph + MCP)

LangGraph와 MCP(Model Context Protocol)를 활용한 자연어 메모 관리 챗봇

## 프로젝트 개요

이 프로젝트는 자연어로 메모를 관리할 수 있는 AI 챗봇입니다. LangGraph를 사용한 대화형 워크플로우와 MCP 프로토콜을 통해 FastAPI 백엔드(https://github.com/gudwls215/flab-python-backend) 와 연동됩니다.

## 주요 기능

- 자연어로 메모 생성, 조회, 수정, 삭제
- 대화 히스토리 유지
- MCP 프로토콜 기반 도구 시스템
- FastAPI 백엔드 연동

## 아키텍처 개요
```
사용자 ←→ LangGraph 챗봇 ←→ MCP Tools ←→ 메모장 FastAPI 백엔드 ←→ PostgreSQL
```

## 프로젝트 구조

```
memo-chatbot/
├── mcp-server/           # MCP 서버 (메모 도구 제공)
│   ├── __init__.py
│   ├── server.py         # MCP 서버 구현
│   └── tools.py          # 메모 관련 MCP 도구 정의
├── chatbot/              # LangGraph 챗봇
│   ├── __init__.py
│   ├── graph.py          # LangGraph 워크플로우
│   ├── nodes.py          # 그래프 노드 정의
│   └── main.py           # 챗봇 실행
├── .env                  # 환경 변수
├── requirements.txt      # Python 의존성
└── README.md
```

## 설치 방법

### 1. 사전 요구사항

- Python 3.10+
- FastAPI 메모장 백엔드 실행 중 (http://localhost:8000)
- OpenAI API 키

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일에 OpenAI API 키를 설정하세요:

```env
OPENAI_API_KEY=your-openai-api-key-here
MEMO_API_URL=http://localhost:8000
```

## 실행 방법

### 챗봇 실행

```bash
python .\chatbot\main.py
```

## 사용 예시

```
You: 할 일 목록이라는 제목으로 메모를 만들어줘
Bot: 메모를 생성했습니다. (ID: 1, 제목: 할 일 목록)

You: 모든 메모를 보여줘
Bot: 총 1개의 메모가 있습니다:
     1. 할 일 목록 (생성일: 2025-12-26)

You: 메모 1번을 조회해줘
Bot: 메모 정보:
     제목: 할 일 목록
     내용: (없음)
     생성일: 2025-12-26 15:00:00

You: 메모 1번의 제목을 '완료된 할 일 목록'으로 변경해줘
Bot: 메모를 수정했습니다. (ID: 1, 새 제목: 완료된 할 일 목록)

You: 메모 1번을 삭제해줘
Bot: 메모를 삭제했습니다. (ID: 1)
```

## 기술 스택

- **LangGraph**: 대화형 워크플로우 관리
- **LangChain**: LLM 통합 및 도구 관리
- **OpenAI GPT-5-nano**: 자연어 이해 및 생성
- **MCP (Model Context Protocol)**: 도구 프로토콜
- **FastAPI**: 백엔드 REST API
- **PostgreSQL**: 데이터베이스

## MCP 도구

챗봇이 사용할 수 있는 5가지 메모 관리 도구:

1. `create_memo`: 새 메모 생성
2. `list_memos`: 메모 목록 조회 (페이징 지원)
3. `get_memo`: 특정 메모 조회
4. `update_memo`: 메모 수정
5. `delete_memo`: 메모 삭제
