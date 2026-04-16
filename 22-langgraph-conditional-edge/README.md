# 22-langgraph-conditional-edge

**One line:** After one shared node, `add_conditional_edges` picks the next node from state.

## What you learn

- **Conditional routing:** a small function returns a key (`even` / `odd`); the graph maps keys to node names.
- **Same pattern for agents:** route to different tools or subgraphs from LLM output or scores.
- **Still no API:** parity is a stand-in for any runtime decision.

## Run

From the repo root:

```bash
uv run python 22-langgraph-conditional-edge/main.py
```

## Expected output

```text
even branch: start n=3 -> {'n': 104}
odd branch: start n=4 -> {'n': -95}
```

Trace for `n=3`: bump ->4 (even) -> +100 -> 104.  
Trace for `n=4`: bump -> 5 (odd) -> -100 -> -95.
