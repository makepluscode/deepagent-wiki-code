# 예제 21: StateGraph로 첫 번째 워크플로우 만들기

**한 줄 요약:** State · Node · Edge 세 개념으로 구성한 3단계 텍스트 처리 파이프라인.

---

## 배우는 것

- **State (`PipelineState`)**: 모든 노드가 읽고 쓰는 공유 데이터 구조 (TypedDict + Reducer)
- **Node**: 상태를 입력받아 갱신된 값을 반환하는 Python 함수
- **Edge**: `START → summarize → extract_keywords → generate_report → END` 고정 실행 순서
- **add_messages Reducer**: 메시지 이력을 덮어쓰지 않고 누적하는 방법
- **Mock 모드**: API 키 없이 파이프라인 구조를 먼저 확인하는 패턴

---

## 파이프라인 구조

```
원문 입력
  │
  ▼
[summarize]         ← 1단계: 한 문장 요약
  │
  ▼
[extract_keywords]  ← 2단계: 핵심 키워드 추출
  │
  ▼
[generate_report]   ← 3단계: 최종 보고서 생성
  │
  ▼
결과 출력
```

---

## 실행 방법

```bash
# Mock 모드 (기본 — API 키 불필요)
uv run python 21-langgraph-stategraph/main.py

# 실제 LLM 호출 (ANTHROPIC_API_KEY 필요)
DEEPAGENT_EXAMPLE_MOCK=0 uv run python 21-langgraph-stategraph/main.py
```

---

## 예상 출력 (Mock 모드)

```
=== 예제 21: StateGraph 텍스트 파이프라인 [Mock 모드] ===

[원문]
LangGraph는 LLM 애플리케이션을 상태 기반 그래프로 표현하는 프레임워크다. ...

[요약]
[요약] LangGraph는 LLM 애플리케이션을...

[키워드]
['[요약]', 'LangGraph는', 'LLM']

[보고서]
## 분석 보고서

**요약:** [요약] LangGraph는 LLM 애플리케이션을...

**핵심 키워드:** [요약], LangGraph는, LLM

**결론:** 위 내용을 바탕으로 추가 검토가 필요하다.

[처리 메시지 수] 4개
```

---

## 환경 변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DEEPAGENT_EXAMPLE_MOCK` | `1` | `1` = Mock 모드, `0` = 실제 LLM 호출 |
| `ANTHROPIC_API_KEY` | — | LLM 모드에서 필요 |
