# 예제 24: ToolNode로 LLM 도구 호출 에이전트 만들기

**한 줄 요약:** LLM이 필요한 도구를 스스로 선택·호출하고, 결과를 받아 최종 답변을 생성하는 ReAct 루프.

---

## 배우는 것

- **`@tool`**: 일반 Python 함수를 LLM이 호출할 수 있는 도구로 등록하는 데코레이터 (docstring이 LLM에게 전달되는 도구 설명)
- **`llm.bind_tools(tools)`**: LLM에게 사용 가능한 도구 목록을 알려주는 방법
- **`ToolNode`**: LLM이 요청한 도구를 실제로 실행하는 내장 노드
- **`tools_condition`**: LLM 응답에 `tool_call`이 있으면 `tools`로, 없으면 `END`로 자동 분기하는 내장 조건 함수
- **ReAct 루프**: `agent → tools → agent` 순환으로 도구 결과를 보고 다음 행동을 결정하는 패턴

---

## 그래프 구조

![graph](graph.png)

```
START → agent → (tool_call 있음?) → tools → agent → END
                       ↓ 없음
                      END
```

---

## 실행 방법

```bash
uv run python main.py
```

---

## 예상 출력

```
=== 예제 24: ToolNode 도구 호출 에이전트 ===

그래프 구조 저장 완료: graph.png

질문: 3 곱하기 7은 얼마야? 그리고 거기에 15를 더하면?

──────────────────────────────────────────────────
[사용자]      3 곱하기 7은 얼마야? 그리고 거기에 15를 더하면?
[도구 호출]   multiply({'a': 3, 'b': 7})
[도구 결과]   multiply → 21
[도구 호출]   add({'a': 21, 'b': 15})
[도구 결과]   add → 36
[최종 답변]   답변:
              - 3 × 7 = 21
              - 21 + 15 = 36
              따라서 3 곱하기 7은 21이고, 거기에 15를 더하면 36입니다.
──────────────────────────────────────────────────
```

### 출력 흐름 해설

| 단계 | 메시지 타입 | 설명 |
|------|------------|------|
| 1 | `HumanMessage` | 사용자 질문 입력 |
| 2 | `AIMessage (tool_calls)` | LLM이 `multiply` 도구 호출 결정 → `tools_condition`이 tools 노드로 분기 |
| 3 | `ToolMessage` | `ToolNode`가 `multiply(3, 7)` 실제 실행 → 결과 21 반환 |
| 4 | `AIMessage (tool_calls)` | LLM이 결과 21을 보고 `add` 도구 추가 호출 결정 |
| 5 | `ToolMessage` | `ToolNode`가 `add(21, 15)` 실행 → 결과 36 반환 |
| 6 | `AIMessage` | tool_call 없음 → `tools_condition`이 END로 분기, 최종 답변 출력 |

> 2→3→4→5 구간이 **ReAct 루프** (`agent → tools → agent`)가 두 번 반복된 것이다.

---

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 키 (필수) |
