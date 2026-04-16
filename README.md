# deepagent-wiki-code

LangChain / LangGraph / Deep Agent 예제코드 저장소.
[deepagent-wiki](https://github.com/makepluscode/deepagent-wiki)의 submodule로 연결됩니다.

---

## 번호 체계

```
10-19  LangChain 기초
20-29  LangGraph 핵심
31-39  DeepAgent 실전 (하네스 4 pillars)
```

---

## 예제 목록

### 10번대 — LangChain 기초

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 11 | `11-langchain-helloworld` | `init_chat_model`, 첫 LLM 호출 | ⭐ |
| 12 | `12-langchain-tools` | `@tool` 데코레이터, ToolNode | ⭐ |
| 13 | `13-langchain-agent` | `create_agent`, tool calling loop | ⭐⭐ |
| 14 | `14-langchain-streaming` | `.stream()`, stream_mode | ⭐⭐ |
| 15 | `15-langchain-tool-runtime` | `ToolRuntime`, state·store 접근 | ⭐⭐ |

### 20번대 — LangGraph 핵심

| 번호 | 디렉토리 | 핵심 개념 | 난이도 |
|------|---------|---------|--------|
| 21 | `21-langgraph-stategraph` | StateGraph, Node, Edge 기본 | ⭐ |
| 22 | `22-langgraph-conditional-edge` | 조건부 엣지, 동적 라우팅 | ⭐⭐ |
| 23 | `23-langgraph-checkpointer` | InMemorySaver, thread_id, 대화 메모리 | ⭐⭐ |
| 24 | `24-langgraph-hitl` | interrupt(), Command(resume=...) | ⭐⭐ |
| 25 | `25-langgraph-memory-store` | InMemoryStore, 의미론적 검색 | ⭐⭐⭐ |
| 26 | `26-langgraph-send-mapreduce` | Send, Map-Reduce 병렬 처리 | ⭐⭐⭐ |
| 27 | `27-langgraph-functional-api` | @entrypoint, @task | ⭐⭐ |
| 28 | `28-langgraph-multi-agent` | Supervisor 패턴, 멀티 에이전트 | ⭐⭐⭐ |

### 30번대 — DeepAgent 실전

> 31 → 39로 갈수록 하네스 요소가 하나씩 추가됩니다.
> 39번은 Constrain·Inform·Verify·Correct 4 pillars가 모두 갖춰진 완전 하네스입니다.

| 번호 | 디렉토리 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|---------|------------|--------|
| 31 | `31-deepagent-helloworld` | `create_deep_agent` 최소 예제 | 없음 | ⭐ |
| 32 | `32-deepagent-filesystem` | 내장 파일시스템 도구 | Constrain 기초 | ⭐ |
| 33 | `33-deepagent-middleware` | 커스텀 미들웨어, 도구 호출 로깅 | Inform (관찰) | ⭐⭐ |
| 34 | `34-deepagent-subagent` | `task` 도구, 전문 서브에이전트 | Constrain (역할 분리) | ⭐⭐ |
| 35 | `35-deepagent-memory` | MemoryMiddleware, 장기 기억 | Inform (메모리) | ⭐⭐ |
| 36 | `36-deepagent-hitl` | `interrupt_on`, 민감 작업 승인 | Constrain + Verify | ⭐⭐ |
| 37 | `37-deepagent-backends` | StoreBackend, 멀티유저 분리 | Constrain (격리) | ⭐⭐⭐ |
| 38 | `38-deepagent-eval` | EDD, Eval 파이프라인 | Verify | ⭐⭐⭐ |
| 39 | `39-deepagent-full-harness` | 4 pillars 완전 통합 | Constrain+Inform+Verify+Correct | ⭐⭐⭐ |

---

## 학습 경로

```
입문   11 → 12 → 13 → 31 → 32
중급   21 → 22 → 23 → 24 → 33 → 34 → 35
고급   25 → 26 → 27 → 28 → 36 → 37 → 38 → 39
```

---

## 실행 환경

```bash
# 의존성 설치·동기화 (uv)
uv sync

# API 키 설정
cp .env.example .env
# .env에 ANTHROPIC_API_KEY 등 입력

# 예제 실행
cd 31-deepagent-helloworld
uv run python main.py
```

---

## 관련 링크

- 위키: [deepagent-wiki](https://github.com/makepluscode/deepagent-wiki)
- 저자: [@makepluscode](https://github.com/makepluscode)
