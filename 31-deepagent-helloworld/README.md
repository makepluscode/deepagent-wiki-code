# 31-deepagent-helloworld

DeepAgent 시리즈(31–39)의 **시작점**으로, `deepagents.create_deep_agent` 한 번으로 LangGraph `CompiledStateGraph`를 만들고 **한 턴**만 대화합니다. 이 예제에서는 **추가 하네스**를 `permissions`, `memory`, `interrupt_on`, 사용자 `middleware` 등으로 **코드에서 넣지 않습니다**. “31번 = 시리즈 기준선(바이브코딩에 가장 가까운 최소 호출)”이며, 32번 이후부터 Constrain / Inform / Verify / Correct 요소를 하나씩 쌓아갑니다.

---

## 한 줄 요약

`create_deep_agent`로 기본 Deep Agent 그래프를 만들고, `invoke`로 사용자 메시지 한 번을 처리합니다.

---

## 이 예제에서 배우는 것

- **`create_deep_agent`의 역할**: 모델 문자열(`anthropic:claude-sonnet-4-6`)나 `BaseChatModel` 인스턴스를 받아, 계획·파일·서브에이전트·요약 등 **기본 미들웨어 스택이 포함된** 에이전트 그래프를 반환합니다.
- **LangGraph 관점**: 반환 타입은 `CompiledStateGraph`이며, 이번 `invoke`에서 다루는 상태의 핵심은 `messages`입니다.
- **입력 형태**: `agent.invoke({"messages": [HumanMessage(...)]})` 처럼 **메시지 리스트**를 넣습니다.
- **오프라인(mock) 실행**: API 키가 없을 때도 그래프 조립·호출 경로를 확인할 수 있도록, 아주 작은 `MockEchoChatModel`을 넣었습니다.
- **실운영(live) 실행**: 유효한 `ANTHROPIC_API_KEY`가 있으면 동일 코드로 Claude가 응답합니다(응답 문장은 실행마다 달라질 수 있음).

---

## 사전 준비

레포지토리 루트에서:

```bash
uv sync
cp .env.example .env
```

`.env`에 실제 키를 넣습니다. (이 저장소는 `.env`를 커밋하지 않습니다.)

---

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Live 모드에 필요합니다. |
| `DEEPAGENT_EXAMPLE_MOCK` | `1` / `true` 등이면 **강제 mock** 모드입니다. |

mock이 켜지는 조건:

1. `DEEPAGENT_EXAMPLE_MOCK`가 참으로 설정되었거나
2. `ANTHROPIC_API_KEY`가 비어 있거나, `.env.example`에 있는 것과 비슷한 **placeholder**로 보이는 값인 경우

---

## 실행 방법

```bash
cd 31-deepagent-helloworld
uv run python main.py
```

---

## 코드에서 하는 일 (개요)

- `build_agent()`에서 `create_deep_agent(model=...)` 호출
- `run()`에서 `HumanMessage` 하나를 넣고 `invoke` 한 번
- 표준 출력에 **모드(MOCK/LIVE)**, 사용자 프롬프트, 마지막 AI 응답, 메시지 개수를 출력

프롬프트(`USER_PROMPT`)는 영어 지시문이며, **한국어 한 문장 자기소개**를 요청하고 도구 없이 바로 답하도록 제한해 두었습니다. (Live에서는 모델이 이 지시를 대부분 지키지만 100% 보장은 아닙니다.)

---

## 실행 결과 (실제 출력 복사)

아래는 **2026-04-16**에, 이 저장소에서 **`ANTHROPIC_API_KEY` 없이** `uv run python main.py`를 실행했을 때의 **전체 표준 출력**입니다. (mock 경로)

```text
Mode: MOCK (DEEPAGENT_EXAMPLE_MOCK=1 or ANTHROPIC_API_KEY missing)

--- user ---
Introduce yourself in one short Korean sentence only. Do not use tools; reply directly.

--- assistant ---
MOCK: I am a placeholder assistant for example 31. Set ANTHROPIC_API_KEY (and unset DEEPAGENT_EXAMPLE_MOCK) for a live Claude reply.

(total messages: 2)
```

### Live 모드에서 기대되는 차이

- 첫 줄이 `Mode: LIVE (anthropic:claude-sonnet-4-6)` 형태로 나옵니다.
- `--- assistant ---` 아래에는 보통 **한국어 한 문장** 자기소개가 나옵니다. (모델·온도·프롬프트에 따라 문장은 매번 달라질 수 있습니다.)
- 이 예제는 **한 턴**을 의도했지만, 모델이 도구 호출을 끌어들이면 메시지 수가 2보다 커질 수 있습니다. 그 경우에도 마지막 AI 텍스트를 기준으로 결과를 읽으면 됩니다.

---

## 트러블슈팅

- **`Mode: MOCK`인데 Live를 원한다**: `.env`의 `ANTHROPIC_API_KEY`가 유효한지 확인하고, `DEEPAGENT_EXAMPLE_MOCK`를 끄거나 제거하세요.
- **Live에서 인증 오류**: 키 만료·권한 문제일 수 있습니다. 터미널에 나오는 프로바이더 메시지를 확인하세요.
- **Deep Agent 기본 도구**: 라이브러리 기본 구성에는 할 일 목록(`write_todos`)·파일 조작·서브에이전트·실행(shell 명령·샌드박스 등, 백엔드에 따라 다름) 등이 포함될 수 있습니다. 이 예제는 “최소 호출”을 보여 주기 위해 **추가 하네스를 코드에서 더하지 않았을 뿐**, 기본 스택은 여전히 두껍습니다. (32번부터 이 위에 제약·승인·메모리 등을 **명시적으로** 쌓아갑니다.)

---

## 다음 단계

- `32-deepagent-filesystem`: `FilesystemPermission` 등으로 파일 접근을 **제한**하는 Constrain 기초
- 레포지토리 루트 `README.md`의 학습 경로 참고
