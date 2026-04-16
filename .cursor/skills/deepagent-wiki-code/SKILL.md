---
name: deepagent-wiki-code
description: >-
  Maintains LangChain, LangGraph, and DeepAgent example code in this repository
  using uv, Ruff, and pre-commit. Use when editing this repo, adding or updating
  numbered examples (11–39), working with CLAUDE.md or AGENTS.md, or when the
  user mentions deepagent-wiki-code, example harness, or submodule code/.
---

# deepagent-wiki-code workflow

## Before changing code

1. Read **CLAUDE.md** at the repository root (canonical Korean rules) and skim **AGENTS.md** (English agent checklist).
2. Confirm the target example folder is **standalone** (no imports from other example dirs).

## Python toolchain (uv only)

- Install/sync: `uv sync`
- Run an example: `uv run python main.py` (from the example directory is fine; uv finds the project root).
- Add deps: `uv add <pkg>`; dev-only: `uv add --dev <pkg>`. Commit `pyproject.toml` and `uv.lock`.

Do **not** use `pip install` or bare `python` for environment setup in this repo.

## Lint and format (Ruff only)

After touching `.py` files:

```bash
uv run ruff check --fix .
uv run ruff format .
```

Optional strict check: `uv run ruff format --check .`

One-time per clone: `uv run pre-commit install`. Manual full run: `uv run pre-commit run --all-files`.

Config lives in `pyproject.toml` (`[tool.ruff]`). Do not add a parallel Black/Flake8/isort stack.

## Example layout

- Entry point: **`main.py`**
- **`README.md`** must include: one-line purpose, learning bullets, how to run (`uv run python main.py`), expected output.
- Type hints on all public functions; docstrings on classes, functions, and every `@tool`.
- Keep functions **≤ ~30 lines** (split if longer).
- New env var names only in **`.env.example`** (never commit `.env` or secrets).

## DeepAgent examples 31–39

Harness builds from 31 (baseline) to 39 (full). When editing that range:

- Tag harness-related lines: `# [Constrain]`, `# [Inform]`, `# [Verify]`, `# [Correct]`, or combined (e.g. `# [Constrain+Verify]`).
- Example **39** `README.md` must **compare with 31** (no harness vs full harness).

## Git commits

- **English** summary line; **≤ 20 words**; prefer **~10–20 words** for normal changes.
- Conventional prefix: `add:`, `update:`, `fix:`, `docs:`, `chore:`, etc.
- Imperative mood (“Add…”, not “Added…”).
- No `git push --force` on `main`.

## Done checklist

- [ ] `uv run ruff check .` clean (use `--fix` where appropriate).
- [ ] `uv run ruff format --check .` passes (or formatted).
- [ ] Example still runs with `uv run python main.py` where applicable.
- [ ] No secrets in repo; harness/README rules satisfied for 31–39 if touched.
