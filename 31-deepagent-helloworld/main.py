"""Example 31: minimal Deep Agent using `create_deep_agent` and a single chat turn."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Final

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain.agents import AgentState
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langgraph.graph.state import CompiledStateGraph

# Cheapest current Claude tier (Haiku 4.5); override with DEEPAGENT_ANTHROPIC_MODEL if needed.
LIVE_MODEL_ANTHROPIC_DEFAULT: Final[str] = "anthropic:claude-haiku-4-5"
LIVE_MODEL_GEMINI: Final[str] = "google_genai:gemini-2.0-flash"
USER_PROMPT: Final[str] = (
    "Introduce yourself in one short Korean sentence only. Do not use tools; reply directly."
)


class MockEchoChatModel(BaseChatModel):
    """Tiny chat model for offline runs when no API key is available."""

    @property
    def _llm_type(self) -> str:
        return "mock-echo-chat"

    def _generate(
        self,
        messages: list[Any],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        del messages, stop, run_manager, kwargs
        text = (
            "MOCK: I am a placeholder assistant for example 31. "
            "Set ANTHROPIC_API_KEY, GOOGLE_API_KEY, or GEMINI_API_KEY "
            "(and unset DEEPAGENT_EXAMPLE_MOCK) for a live reply."
        )
        message = AIMessage(content=text)
        return ChatResult(generations=[ChatGeneration(message=message)])

    def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
        """Return self so the agent graph can bind tools without a real provider."""
        del tools, kwargs
        return self


def _is_truthy_env(name: str) -> bool:
    """Return True when an environment variable is a common truthy flag."""
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _looks_like_real_api_key(key: str) -> bool:
    """Return False for empty strings and common placeholder values."""
    if not key:
        return False
    lowered = key.lower()
    return not ("your_" in lowered or "placeholder" in lowered or lowered in {"here", "changeme"})


def _anthropic_key_configured() -> bool:
    """Return True when an Anthropic API key looks present and non-placeholder."""
    return _looks_like_real_api_key(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def _google_key_configured() -> bool:
    """Return True when a Google Gemini API key is set (GOOGLE_API_KEY or GEMINI_API_KEY)."""
    google = os.environ.get("GOOGLE_API_KEY", "").strip()
    gemini = os.environ.get("GEMINI_API_KEY", "").strip()
    return _looks_like_real_api_key(google) or _looks_like_real_api_key(gemini)


def _should_use_mock() -> bool:
    """Use mock LLM when forced, or when no usable provider key is configured."""
    if _is_truthy_env("DEEPAGENT_EXAMPLE_MOCK"):
        return True
    return not (_google_key_configured() or _anthropic_key_configured())


def _anthropic_model_id() -> str:
    """Return provider:model for Anthropic (env override or default Haiku)."""
    raw = os.environ.get("DEEPAGENT_ANTHROPIC_MODEL", "").strip()
    if not raw:
        return LIVE_MODEL_ANTHROPIC_DEFAULT
    if ":" in raw:
        return raw
    return f"anthropic:{raw}"


def _llm_primary_preference() -> str:
    """Return 'google', 'anthropic', or '' for default (Claude first when both keys exist)."""
    raw = os.environ.get("DEEPAGENT_LLM_PRIMARY", "").strip().lower()
    if raw in {"google", "gemini", "google_genai"}:
        return "google"
    if raw in {"anthropic", "claude"}:
        return "anthropic"
    return ""


def _live_model_id() -> str:
    """Pick live model from env preference, then keys (default: cheapest Claude if Anthropic key is set)."""
    primary = _llm_primary_preference()
    has_google = _google_key_configured()
    has_anthropic = _anthropic_key_configured()

    if primary == "anthropic":
        if has_anthropic:
            return _anthropic_model_id()
        if has_google:
            return LIVE_MODEL_GEMINI
    elif primary == "google":
        if has_google:
            return LIVE_MODEL_GEMINI
        if has_anthropic:
            return _anthropic_model_id()
    else:
        if has_anthropic:
            return _anthropic_model_id()
        if has_google:
            return LIVE_MODEL_GEMINI

    return _anthropic_model_id()


def build_agent() -> CompiledStateGraph[AgentState[Any], Any, Any, Any]:
    """Build a Deep Agent graph (live Claude by default, optional Gemini fallback, or mock)."""
    model: str | MockEchoChatModel = MockEchoChatModel() if _should_use_mock() else _live_model_id()
    return create_deep_agent(model=model)


def _load_dotenv_for_example() -> None:
    """Load repo-root `.env`, then optional example-local `.env` (overrides)."""
    example_dir = Path(__file__).resolve().parent
    repo_root = example_dir.parent
    root_env = repo_root / ".env"
    local_env = example_dir / ".env"
    if root_env.is_file():
        load_dotenv(root_env)
    if local_env.is_file():
        load_dotenv(local_env, override=True)


def _last_ai_message(messages: list[BaseMessage]) -> str | None:
    """Return the last AIMessage with string content, if any."""
    for message in reversed(messages):
        if isinstance(message, AIMessage) and isinstance(message.content, str) and message.content:
            return message.content
    return None


def run() -> int:
    """Invoke the agent once and print a short transcript to stdout."""
    _load_dotenv_for_example()
    use_mock = _should_use_mock()
    if use_mock:
        print(
            "Mode: MOCK (DEEPAGENT_EXAMPLE_MOCK=1 or no GOOGLE_API_KEY / GEMINI_API_KEY / "
            "ANTHROPIC_API_KEY)",
        )
    else:
        print(f"Mode: LIVE ({_live_model_id()})")

    agent = build_agent()
    result = agent.invoke({"messages": [HumanMessage(content=USER_PROMPT)]})
    messages = result.get("messages", [])
    reply = _last_ai_message(messages)
    print("\n--- user ---")
    print(USER_PROMPT)
    print("\n--- assistant ---")
    print(reply if reply is not None else "(no assistant text)")
    print(f"\n(total messages: {len(messages)})")
    return 0


def main() -> None:
    """CLI entrypoint with friendly interrupt handling."""
    try:
        raise SystemExit(run())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130) from None


if __name__ == "__main__":
    main()
