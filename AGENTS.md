# AGENTS.md — Agent instructions for this repository

**Authoritative human-facing rules (Korean):** [`CLAUDE.md`](CLAUDE.md).  
This file is a concise checklist for coding agents (Claude, Cursor, and similar).

---

## What this repo is

Example code for **LangChain**, **LangGraph**, and **DeepAgent**. It is meant to be linked as the `code/` submodule of [deepagent-wiki](https://github.com/makepluscode/deepagent-wiki).

---

## Roles

| Who | Responsibility |
|-----|----------------|
| Human | Example ideas and requests |
| LLM agent | Implement and maintain examples; keep `README.md` and `CLAUDE.md` accurate |

---

## Per-example requirements

- Each example must run **standalone** (no dependency on other example folders).
- Entry point is always **`main.py`**.
- Each example needs **`README.md`** with: one-line purpose, learning bullets, how to run (`uv run python main.py`), expected output (text or screenshot).
- New env vars: register **names only** in **`.env.example`** (never commit secrets).

---

## Python (3.11+)

- Type hints on all function parameters and return types.
- Keep functions **under ~30 lines**; split if longer.
- Class and function **docstrings required** (Korean or English).
- **`@tool`**: docstring **required** (used as the tool description for the LLM).
- **Lint / format:** **Ruff only** (no Black/Flake8/isort stack). Run `uv run ruff check --fix .` and `uv run ruff format .` after edits. Use `uv run pre-commit install` once per clone so commits run the same checks.

---

## Dependencies and models

- **Install / run with uv only:** `uv sync`, `uv run python …`, `uv add …` (no `pip install` for this repo).
- `langchain>=0.3`, `langgraph>=0.2`, `deepagents` (latest stable); versions live in `pyproject.toml` / `uv.lock`.
- Use `provider:model` strings; use **only real model IDs** (no fake names), e.g. `anthropic:claude-sonnet-4-6`.

---

## Security

- Never commit **`.env`**, API keys, or secrets.
- Examples that call external APIs should offer a **mock mode**.
- **`FilesystemPermission`**: minimum necessary paths (principle of least privilege).

---

## DeepAgent examples 31–39 (harness)

Progressive **four pillars**: Constrain, Inform, Verify, Correct.

| Range | Harness focus |
|-------|----------------|
| 31 | Baseline (minimal) |
| 32 | Constrain: `FilesystemPermission` |
| 33 | Middleware: audit / rate limits |
| 34 | Constrain: subagent role split |
| 35 | Inform: `MemoryMiddleware` + **`AGENTS.md`** |
| 36 | Constrain + Verify: `interrupt_on` |
| 37 | Constrain: `StoreBackend` multi-user isolation |
| 38 | Verify: EDD, eval pipeline |
| 39 | Full harness + Ralph Loop |

- Example **39** `README.md` must **compare with 31** (no harness vs full harness).

### Harness comment tags

At lines where harness behavior is introduced, tag:

- `# [Constrain]`, `# [Inform]`, `# [Verify]`, `# [Correct]`
- Combined example: `# [Constrain+Verify]`

Comment only non-obvious logic.

---

## Git

- Commit messages: **English**, sentence case with conventional prefix: `add:`, `update:`, `fix:`, `docs:` (see `CLAUDE.md`).
- **`main`**: only working examples. **`feat/[number]`**: work in progress for a new example.
- **No** `git push --force`.

---

## Pre-merge / pre-PR checklist

1. Read `CLAUDE.md` and the example `README.md`.
2. Example runs with `uv run python main.py` only; no secrets in code or docs.
3. For 31–39: harness tags and pillar explanation appear in code/README as appropriate.
4. `uv run ruff check .` and `uv run ruff format --check .` pass (or fix with `--fix` / `format`).
5. If you hit a recurring pitfall, append to **Past Failures** in `CLAUDE.md`.

---

## Related docs

- [`README.md`](README.md) — numbering, catalog, learning path
- [`CLAUDE.md`](CLAUDE.md) — full rules (canonical)
