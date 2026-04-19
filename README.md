# deepagent-wiki-code

LangChain / LangGraph / Deep Agent 예제코드 저장소.
[deepagent-wiki](https://github.com/makepluscode/deepagent-wiki)의 submodule로 연결됩니다.

---

## 번호 체계

```
[장번호][장 내 순서]

예)  11 = 1장 첫 번째 예제
     12 = 1장 두 번째 예제
     42 = 4장 두 번째 예제
    101 = 10장 첫 번째 예제
```

장당 최소 2개 · 최대 4개 예제.

---

## 예제 목록

### 1장 — 첫 LangChain 앱 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 11 | `11-langchain-helloworld` | `init_chat_model`, 첫 LLM 호출 | ⭐ |
| 12 | `12-langchain-prompt` | `ChatPromptTemplate`, 프롬프트 구성 | ⭐ |

### 2장 — 도구와 ToolRuntime (3개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 21 | `21-langchain-tools` | `@tool` 데코레이터, 도구 정의와 실행 | ⭐ |
| 22 | `22-langchain-tool-binding` | `bind_tools`, 도구 묶음과 LLM 연결 | ⭐⭐ |
| 23 | `23-langchain-tool-runtime` | `ToolRuntime`, state·store 접근 | ⭐⭐ |

### 3장 — 에이전트와 스트리밍 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 31 | `31-langchain-agent` | `create_agent`, tool calling loop | ⭐⭐ |
| 32 | `32-langchain-streaming` | `.stream()`, 토큰 단위 실시간 출력 | ⭐⭐ |

### 4장 — StateGraph 기초 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 41 | `41-langgraph-stategraph-chat` | StateGraph + 단일 LLM 대화 노드 | ⭐ |
| **42** | **`42-langgraph-stategraph`** ✅ | StateGraph 멀티 노드 파이프라인 | ⭐ |

### 5장 — 엣지와 라우팅 (3개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| **51** | **`51-langgraph-conditional-edge`** ✅ | 조건부 엣지, 동적 라우팅 | ⭐⭐ |
| **52** | **`52-langgraph-tool-node`** ✅ | ToolNode, tools_condition, ReAct 루프 | ⭐⭐ |
| 53 | `53-langgraph-send-mapreduce` | Send, Map-Reduce 병렬 처리 | ⭐⭐⭐ |

### 6장 — Checkpointer와 메모리 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| **61** | **`61-langgraph-checkpointer`** ✅ | MemorySaver, thread_id 세션 격리 | ⭐⭐ |
| 62 | `62-langgraph-memory-store` | InMemoryStore, 장기 메모리 | ⭐⭐⭐ |

### 7장 — Human-in-the-Loop (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 71 | `71-langgraph-hitl` | `interrupt_before`, 사람 승인 게이트 | ⭐⭐ |
| 72 | `72-langgraph-hitl-resume` | `Command(resume=...)`, 재개 패턴 | ⭐⭐ |

### 8장 — 첫 Deep Agent (3개)

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| **81** | **`81-deepagent-helloworld`** ✅ | `create_deep_agent` 최소 예제 | 없음 | ⭐ |
| 82 | `82-deepagent-filesystem` | 내장 파일시스템 도구 | Constrain 기초 | ⭐ |
| 83 | `83-deepagent-hitl` | `interrupt_on`, 민감 작업 승인 | Constrain + Verify | ⭐⭐ |

### 9장 — 미들웨어 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| 91 | `91-deepagent-middleware` | 커스텀 미들웨어, 도구 호출 로깅 | Inform (관찰) | ⭐⭐ |
| 92 | `92-deepagent-audit` | 호출 횟수 제한, 감사 로그 | Inform (제어) | ⭐⭐ |

### 10장 — 파일시스템 백엔드 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| 101 | `101-deepagent-backends` | StoreBackend 기초, 로컬 저장소 | Constrain (격리) | ⭐⭐ |
| 102 | `102-deepagent-multiuser` | 사용자별 StoreBackend 격리 | Constrain (격리) | ⭐⭐⭐ |

### 11장 — 서브에이전트 팀 (3개)

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| 111 | `111-deepagent-subagent` | `task` 도구, 서브에이전트 기초 | Constrain (역할 분리) | ⭐⭐ |
| 112 | `112-deepagent-team` | 3인 에이전트 팀 협업 | Constrain (역할 분리) | ⭐⭐ |
| 113 | `113-langgraph-multi-agent` | Supervisor 패턴 (LangGraph) | Constrain (역할 분리) | ⭐⭐⭐ |

### 12장 — 장기 메모리 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| 121 | `121-deepagent-memory` | MemoryMiddleware, 대화 기억 | Inform (메모리) | ⭐⭐ |
| 122 | `122-deepagent-personal-assistant` | 장기 기억 + 선호도 학습 | Inform (메모리) | ⭐⭐⭐ |

> 13장 (CLI)은 터미널 실습이므로 별도 코드 예제 없음.

### 14장 — LangSmith 관측성 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 141 | `141-deepagent-langsmith` | LangSmith 트레이싱, 비용 대시보드 | ⭐⭐ |
| 142 | `142-deepagent-feedback` | 커스텀 태그, 사용자 피드백 수집 | ⭐⭐ |

### 15장 — FastAPI 배포 (2개)

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 151 | `151-deepagent-fastapi` | FastAPI 에이전트 API 서버, 멀티유저 | ⭐⭐⭐ |
| 152 | `152-deepagent-streaming-api` | SSE 스트리밍, 비동기 응답 | ⭐⭐⭐ |

### 16장 — EDD와 하네스 통합 (3개)

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| 161 | `161-deepagent-eval` | EDD, Eval 파이프라인 | Verify | ⭐⭐⭐ |
| 162 | `162-deepagent-harness-intro` | 4 pillars 개념 통합 입문 | Constrain+Inform+Verify+Correct | ⭐⭐⭐ |
| 163 | `163-deepagent-full-harness` | 완전 하네스 + Ralph Loop | Constrain+Inform+Verify+Correct | ⭐⭐⭐ |

---

## 책 챕터 ↔ 예제 매핑

| 책 장 | 실습 주제 | 예제 번호 | 예제 수 |
|------|---------|---------|--------|
| 1장 | 첫 LangChain 앱 | 11, 12 | 2 |
| 2장 | 도구와 ToolRuntime | 21, 22, 23 | 3 |
| 3장 | 에이전트 + 스트리밍 | 31, 32 | 2 |
| 4장 | StateGraph 기초 | 41, 42 | 2 |
| 5장 | 조건부 엣지·ToolNode·Map-Reduce | 51, 52, 53 | 3 |
| 6장 | Checkpointer + Memory Store | 61, 62 | 2 |
| 7장 | Human-in-the-Loop | 71, 72 | 2 |
| 8장 | 첫 Deep Agent | 81, 82, 83 | 3 |
| 9장 | 미들웨어 | 91, 92 | 2 |
| 10장 | 파일시스템 백엔드 | 101, 102 | 2 |
| 11장 | 서브에이전트 팀 | 111, 112, 113 | 3 |
| 12장 | 장기 메모리 | 121, 122 | 2 |
| 13장 | CLI (터미널 실습) | — | — |
| 14장 | LangSmith 관측성 | 141, 142 | 2 |
| 15장 | FastAPI 배포 | 151, 152 | 2 |
| 16장 | EDD + 하네스 통합 | 161, 162, 163 | 3 |
| **합계** | | | **35** |

---

## 학습 경로

```
입문   11 → 12 → 21 → 31 → 81 → 82
중급   41 → 42 → 51 → 52 → 61 → 91 → 111 → 121
고급   22 → 23 → 32 → 53 → 62 → 71 → 72 → 83 → 92 → 101 → 112 → 113
운영   141 → 142 → 151 → 152 → 161 → 162 → 163
```

---

## 구현 현황

✅ 완료 · 미완료

| 번호 | 상태 | 번호 | 상태 | 번호 | 상태 |
|------|------|------|------|------|------|
| 11 | ☐ | 51 | ✅ | 101 | ☐ |
| 12 | ☐ | 52 | ✅ | 102 | ☐ |
| 21 | ☐ | 53 | ☐ | 111 | ☐ |
| 22 | ☐ | 61 | ✅ | 112 | ☐ |
| 23 | ☐ | 62 | ☐ | 113 | ☐ |
| 31 | ☐ | 71 | ☐ | 121 | ☐ |
| 32 | ☐ | 72 | ☐ | 122 | ☐ |
| 41 | ☐ | 81 | ✅ | 141 | ☐ |
| 42 | ✅ | 82 | ☐ | 142 | ☐ |
| | | 83 | ☐ | 151 | ☐ |
| | | 91 | ☐ | 152 | ☐ |
| | | 92 | ☐ | 161 | ☐ |
| | | | | 162 | ☐ |
| | | | | 163 | ☐ |

---

## 실행 환경

```bash
# 의존성 설치·동기화 (uv)
uv sync

# API 키 설정
cp .env.example .env
# .env에 ANTHROPIC_API_KEY 등 입력

# 예제 실행
cd 42-langgraph-stategraph
uv run python main.py
```

## 린트·포맷 (개발)

```bash
uv run ruff check --fix .
uv run ruff format .
uv run pre-commit install   # 최초 1회 — 커밋 시 Ruff 자동 실행
```

---

## 관련 링크

- 위키: [deepagent-wiki](https://github.com/makepluscode/deepagent-wiki)
- 저자: [@makepluscode](https://github.com/makepluscode)
