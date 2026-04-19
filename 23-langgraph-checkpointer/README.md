# Example 23: Persisting State with MemorySaver Checkpointer

| Book Chapter | Key APIs | Difficulty |
|---|---|---|
| Chapter 6 · §6.1 & §6.3 | `MemorySaver`, `thread_id`, `add_messages` | ⭐⭐ |

> **Chapter 6** introduces LangGraph persistence. §6.1 explains why stateless graphs lose context between calls, and §6.3 shows how `MemorySaver` (also called `InMemorySaver` in some versions) solves this by checkpointing state after every node — keyed by `thread_id` so multiple sessions stay isolated.

**One line:** Attach a checkpointer to carry conversation history across multiple `invoke()` calls, isolated by `thread_id`.

---

## Why LangGraph, Not LangChain?

LangChain (LCEL chains) has no checkpointer concept. Every `chain.invoke()` is stateless — to persist history you must manually manage a `ChatMessageHistory` object and inject it into the prompt yourself.

LangGraph is different because the graph owns a `State` object, and the checkpointer snapshots that entire state keyed by `thread_id` after every node. Any field — not just messages — is persisted and restored automatically.

> **Checkpointer is a LangGraph-only feature.**

---

## What You Learn

- **`MemorySaver`**: in-memory checkpointer that saves graph state after every node execution
- **`thread_id`**: key that separates independent sessions — same ID continues the conversation, different ID starts fresh
- **`add_messages` reducer**: accumulates messages instead of overwriting, enabling multi-turn context
- **Why it matters**: without a checkpointer every `invoke()` starts from an empty state; with one, the graph remembers

---

## Graph Structure

![graph](graph.png)

---

## How It Works

```
invoke() #1  →  [HumanMessage("My name is Robert")]         thread-A
invoke() #2  →  [HumanMessage("What is my name?")]          thread-A  ← remembers Robert
invoke() #3  →  [HumanMessage("What is my name?")]          thread-B  ← no memory
```

---

## Run

```bash
uv run python main.py
```

---

## Expected Output

```
=== 예제 23: MemorySaver 체크포인터 ===

그래프 구조 저장 완료: graph.png

──────────────────────────────────────────────────
[thread-A] 첫 번째 대화
──────────────────────────────────────────────────
세션 ID : thread-A
사용자  : 안녕! 내 이름은 로버트야.
AI      : 안녕하세요, 로버트씨! 만나서 반가워요. ...
누적 메시지 수: 2개

[thread-A] 두 번째 대화 — 이전 맥락 유지 확인
──────────────────────────────────────────────────
세션 ID : thread-A
사용자  : 내 이름이 뭐야?
AI      : 로버트씨라고 하셨잖아요! ...
누적 메시지 수: 4개

[thread-B] 새 세션 — thread-A 기억 없음
──────────────────────────────────────────────────
세션 ID : thread-B
사용자  : 내 이름이 뭐야?
AI      : 죄송하지만, 저는 당신의 이름을 모릅니다. ...
누적 메시지 수: 2개
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key (required) |
