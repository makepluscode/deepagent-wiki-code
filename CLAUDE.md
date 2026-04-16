# CLAUDE.md — deepagent-wiki-code

이 저장소는 LangChain / LangGraph / Deep Agent 예제코드 모음입니다.
[deepagent-wiki](https://github.com/makepluscode/deepagent-wiki)의 `code/` submodule로 연결됩니다.

---

## 역할 분담

| 역할 | 담당 |
|------|------|
| 예제 기획·요청 | 사용자 |
| 예제코드 작성·유지 | Claude (LLM) |
| README, CLAUDE.md 유지 | Claude (LLM) |

---

## 디렉토리 구조

```
deepagent-wiki-code/
├── README.md               # 전체 예제 목록 및 학습 경로
├── CLAUDE.md               # 이 파일 — 코딩 규칙 및 행동 지침
├── .env.example            # 환경변수 템플릿 (실제 키 절대 포함 금지)
├── pyproject.toml          # 공통 의존성 (uv)
├── uv.lock                 # 잠금 파일 (uv sync)
│
├── 11-langchain-helloworld/
│   ├── README.md           # 예제 설명, 실행 방법
│   └── main.py
├── ...
└── 39-deepagent-full-harness/
    ├── README.md
    ├── main.py
    ├── middleware.py
    ├── eval/
    └── AGENTS.md
```

---

## 코딩 규칙

### Python 스타일
- Python **3.11 이상** 기준
- 타입 힌트 **필수** (함수 인자·반환값 모두)
- 함수는 **30줄 이내** — 넘으면 분리
- 클래스 docstring 및 함수 docstring **필수** (한국어 또는 영어)
- `@tool` 데코레이터 사용 시 **docstring 필수** (LLM이 도구 설명으로 사용)
- **린트·포맷:** 저장소 루트에서 `uv run ruff check --fix .`, `uv run ruff format .` (설정은 `pyproject.toml`). 커밋 전 `uv run pre-commit install`로 후크가 Ruff를 실행함.

### 의존성
- 패키지 설치는 **uv**만 사용: `uv sync`, `uv run`, `uv add` (공통 의존성은 `pyproject.toml` / `uv.lock`).
```
langchain>=0.3
langgraph>=0.2
deepagents  (최신 stable)
```
- `provider:model` 형식 사용 (`anthropic:claude-sonnet-4-6`)
- 모델명은 **실제 존재하는 것만** 사용 (가상 모델명 금지)
- 환경변수는 반드시 `.env.example`에 키 이름만 등록

### 파일 구성
- 각 예제는 **독립 실행 가능**해야 함 (이전 예제 의존 금지)
- 진입점은 항상 `main.py`
- 예제별 `README.md`에 다음 포함:
  1. 무엇을 만드는가 (한 줄)
  2. 배우는 것 (bullet)
  3. 실행 방법 (`uv run python main.py`)
  4. 예상 출력 (스크린샷 또는 텍스트)

### 보안
- `.env` 파일, API 키, 시크릿 **절대 커밋 금지**
- 외부 서비스 호출이 필요한 예제는 **mock 모드** 제공
- `FilesystemPermission`은 항상 최소 권한 원칙 적용

---

## 예제 작성 기준

### 31~39번 DeepAgent 예제 특이사항

각 예제는 하네스 4 pillars를 점진적으로 쌓는 구조:

| 예제 | 추가 하네스 요소 |
|------|----------------|
| 31 | 없음 — 바이브코딩 수준 기준선 |
| 32 | Constrain: FilesystemPermission |
| 33 | 미들웨어: 감사·횟수 제한 |
| 34 | Constrain: 서브에이전트 역할 분리 |
| 35 | Inform: MemoryMiddleware + AGENTS.md |
| 36 | Constrain+Verify: interrupt_on |
| 37 | Constrain: StoreBackend 멀티유저 격리 |
| 38 | Verify: EDD, Eval 파이프라인 |
| 39 | 4 pillars 완전 통합 + Ralph Loop |

**39번 README는 31번과의 비교를 반드시 포함** — "하네스 없음 vs 완전 하네스" 대비.

### 코드 주석 규칙
- 로직이 자명하지 않은 부분만 주석
- 하네스 요소가 추가되는 지점에 `# [Constrain]`, `# [Inform]`, `# [Verify]`, `# [Correct]` 태그 표시
- 예시:
  ```python
  permissions=[                               # [Constrain] 파일 접근 제한
      FilesystemPermission(paths=["/workspace/**"], mode="allow"),
      FilesystemPermission(paths=["/**"], mode="deny"),
  ],
  interrupt_on={"delete_file": True},         # [Constrain+Verify] 사람 승인 게이트
  memory=["/AGENTS.md"],                      # [Inform] 영속 컨텍스트
  middleware=[RalphLoopMiddleware()],          # [Correct] 실패 복구
  ```

---

## Git 규칙

### 커밋 컨벤션
```
add:    새 예제 추가      (예: add: 31-deepagent-helloworld)
update: 예제 내용 수정    (예: update: 33 fix middleware import path)
fix:    버그 수정         (예: fix: 36 hitl resume command)
docs:   README/CLAUDE.md  (예: docs: update 39 harness comparison)
```

### 브랜치 전략
```
main          ← 동작하는 예제만
feat/[번호]   ← 새 예제 작성 중
```

### 금지 사항
- `.env` 파일 커밋 절대 금지
- 동작하지 않는 코드 main 브랜치 머지 금지
- `git push --force` 금지

---

## 환경 설정

```bash
# 의존성 동기화 (uv)
uv sync

# .env.example 참고하여 .env 생성
cp .env.example .env

# 필수 환경변수
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here        # 선택 (일부 예제)
LANGCHAIN_API_KEY=your_key_here     # LangSmith 트레이싱 (선택)
LANGCHAIN_TRACING_V2=true           # LangSmith 활성화 (선택)
```

---

## Past Failures (누적)

> 예제 작성 중 발생한 이슈와 방지책을 기록합니다.

<!-- 이슈 발생 시 아래에 추가 -->
