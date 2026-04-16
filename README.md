# deepagent-wiki-code

LangChain / LangGraph / Deep Agent 예제코드 저장소.
[deepagent-wiki](https://github.com/makepluscode/deepagent-wiki)의 submodule로 연결됩니다.

---

## 번호 체계

```
10-19  LangChain 기초       (책 1~3장)
20-29  LangGraph 핵심       (책 4~7장)
31-39  DeepAgent 실전       (책 8~12장)
40-49  심화·운영             (책 14~16장)
```

---

## 예제 목록

### 10번대 — LangChain 기초 (책 1~3장)

| 번호 | 디렉토리 | 책 챕터 | 핵심 개념 | 난이도 |
|------|---------|--------|---------|--------|
| 11 | `11-langchain-helloworld` | 1장 1.4 | `init_chat_model`, 첫 LLM 호출 | ⭐ |
| 12 | `12-langchain-tools` | 2장 2.3·2.5 | `@tool` 데코레이터, 도구 묶음 | ⭐ |
| 13 | `13-langchain-agent` | 3장 3.4 | `create_agent`, tool calling loop | ⭐⭐ |
| 14 | `14-langchain-streaming` | 3장 3.3 | `.stream()`, stream_mode | ⭐⭐ |
| 15 | `15-langchain-tool-runtime` | 2장 2.4 | `ToolRuntime`, state·store 접근 | ⭐⭐ |

### 20번대 — LangGraph 핵심 (책 4~7장)

| 번호 | 디렉토리 | 책 챕터 | 핵심 개념 | 난이도 |
|------|---------|--------|---------|--------|
| 21 | `21-langgraph-stategraph` | 4장 4.4 | StateGraph, Node, Edge 기본 | ⭐ |
| 22 | `22-langgraph-conditional-edge` | 5장 5.3 | 조건부 엣지, 동적 라우팅 | ⭐⭐ |
| 23 | `23-langgraph-checkpointer` | 6장 6.1·6.3 | InMemorySaver, thread_id | ⭐⭐ |
| 24 | `24-langgraph-hitl` | 7장 7.5 | interrupt(), Command(resume=...) | ⭐⭐ |
| 25 | `25-langgraph-memory-store` | 6장 6.2·6.5 | InMemoryStore, 의미론적 검색 | ⭐⭐⭐ |
| 26 | `26-langgraph-send-mapreduce` | 5장 5.4·5.6 | Send, Map-Reduce 분석 파이프라인 | ⭐⭐⭐ |
| 27 | `27-langgraph-functional-api` | 5장 5.5 | @entrypoint, @task | ⭐⭐ |
| 28 | `28-langgraph-multi-agent` | 11장 11.4 참고 | Supervisor 패턴 (LangGraph 레벨) | ⭐⭐⭐ |

### 30번대 — DeepAgent 실전 (책 8~12장)

> 31 → 39로 갈수록 하네스 요소가 하나씩 추가됩니다.
> 39번은 Constrain·Inform·Verify·Correct 4 pillars가 모두 갖춰진 완전 하네스입니다.

| 번호 | 디렉토리 | 책 챕터 | 핵심 개념 | 하네스 요소 | 난이도 |
|------|---------|--------|---------|------------|--------|
| 31 | `31-deepagent-helloworld` | 8장 8.4 | `create_deep_agent` 최소 예제 | 없음 | ⭐ |
| 32 | `32-deepagent-filesystem` | 8·10장 | 내장 파일시스템 도구 | Constrain 기초 | ⭐ |
| 33 | `33-deepagent-middleware` | 9장 9.5 | 커스텀 미들웨어, 도구 호출 로깅 | Inform (관찰) | ⭐⭐ |
| 34 | `34-deepagent-subagent` | 11장 11.5 | `task` 도구, 3인 에이전트 팀 | Constrain (역할 분리) | ⭐⭐ |
| 35 | `35-deepagent-memory` | 12장 12.5 | MemoryMiddleware, 개인 비서 | Inform (메모리) | ⭐⭐ |
| 36 | `36-deepagent-hitl` | 7·8장 | `interrupt_on`, 민감 작업 승인 | Constrain + Verify | ⭐⭐ |
| 37 | `37-deepagent-backends` | 10장 10.5 | StoreBackend, 멀티유저 분리 | Constrain (격리) | ⭐⭐⭐ |
| 38 | `38-deepagent-eval` | 16장 16.5 | EDD, Eval 파이프라인 | Verify | ⭐⭐⭐ |
| 39 | `39-deepagent-full-harness` | 16장 16.6 | 4 pillars 완전 통합 | Constrain+Inform+Verify+Correct | ⭐⭐⭐ |

### 40번대 — 심화·운영 (책 14~16장)

| 번호 | 디렉토리 | 책 챕터 | 핵심 개념 | 난이도 |
|------|---------|--------|---------|--------|
| 40 | `40-deepagent-langsmith` | 14장 14.5 | LangSmith 트레이싱, 비용·품질 대시보드 | ⭐⭐ |
| 41 | `41-deepagent-fastapi` | 15장 15.5 | FastAPI 에이전트 API 서버, 멀티유저 | ⭐⭐⭐ |

> 13장 (CLI)은 터미널 실습이므로 별도 코드 예제 없음.

---

## 책 챕터 ↔ 예제 완전 매핑

| 책 장 | 실습 주제 | 예제 번호 |
|------|---------|---------|
| 1장 | 첫 LangChain 앱 | 11 |
| 2장 | 도구 묶음 + ToolRuntime | 12, 15 |
| 3장 | 리서치 에이전트 + 스트리밍 | 13, 14 |
| 4장 | StateGraph 첫 워크플로우 | 21 |
| 5장 | 조건부 엣지·파이프라인·Functional API | 22, 26, 27 |
| 6장 | Checkpointer + Memory Store | 23, 25 |
| 7장 | Human-in-the-Loop | 24 |
| 8장 | 첫 Deep Agent | 31, 32 |
| 9장 | 미들웨어 | 33 |
| 10장 | 파일시스템 백엔드 | 37 |
| 11장 | 서브에이전트 팀 | 34, 28 |
| 12장 | 장기 메모리 | 35 |
| 13장 | CLI (터미널 실습) | — |
| 14장 | LangSmith 관측성 | 40 |
| 15장 | FastAPI 배포 | 41 |
| 16장 | EDD + 하네스 통합 | 38, 39 |

---

## 학습 경로

```
입문   11 → 12 → 13 → 31 → 32
중급   21 → 22 → 23 → 24 → 33 → 34 → 35
고급   25 → 26 → 27 → 28 → 36 → 37 → 38 → 39
운영   40 → 41
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
