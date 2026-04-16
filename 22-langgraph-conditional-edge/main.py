"""Example 22: route to different nodes with `add_conditional_edges` (no LLM)."""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph


class RouteState(TypedDict):
    """Shared state: one integer the router inspects."""

    n: int


def bump(state: RouteState) -> RouteState:
    """First node: add one so even/odd can split."""
    return {"n": state["n"] + 1}


def pick_branch(state: RouteState) -> Literal["even", "odd"]:
    """Return the next node name based on parity (the conditional edge key)."""
    return "even" if state["n"] % 2 == 0 else "odd"


def on_even(state: RouteState) -> RouteState:
    """Branch A: reward even numbers."""
    return {"n": state["n"] + 100}


def on_odd(state: RouteState) -> RouteState:
    """Branch B: penalize odd numbers."""
    return {"n": state["n"] - 100}


def build_workflow() -> CompiledStateGraph:
    """START -> bump -> (even|odd) -> END."""
    graph = StateGraph(RouteState)
    graph.add_node("bump", bump)
    graph.add_node("even", on_even)
    graph.add_node("odd", on_odd)
    graph.add_edge(START, "bump")
    graph.add_conditional_edges("bump", pick_branch, {"even": "even", "odd": "odd"})
    graph.add_edge("even", END)
    graph.add_edge("odd", END)
    return graph.compile()


def run() -> int:
    """Run twice to show both branches."""
    app = build_workflow()
    cases: list[tuple[str, int]] = [
        ("even branch", 3),  # 3+1=4 -> even -> +100 -> 104
        ("odd branch", 4),  # 4+1=5 -> odd -> -100 -> -95
    ]
    for label, start_n in cases:
        result = app.invoke({"n": start_n})
        print(f"{label}: start n={start_n} -> {result}")
    return 0


def main() -> None:
    """CLI entrypoint."""
    raise SystemExit(run())


if __name__ == "__main__":
    main()
