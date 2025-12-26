# LangGraph + 메모장 API 챗봇 구현 가이드

LangGraph를 활용해서 메모장 API를 MCP(Model Context Protocol) 툴로 만들고, 챗봇이 자연어로 메모를 관리

## 아키텍처 개요
```
사용자 ←→ LangGraph 챗봇 ←→ MCP Tools ←→ 메모장 FastAPI 백엔드 ←→ PostgreSQL
```
