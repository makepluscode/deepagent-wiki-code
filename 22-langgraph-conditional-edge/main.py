# langchain>=1.2, langgraph>=1.1
"""예제 22: add_conditional_edges로 조건 분기 라우팅."""

from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


# 1. 상태(State) 정의 — 라우터가 검사할 정수 하나
class RouteState(TypedDict):
    n: int


# 2-1. 공통 노드: n에 1을 더해 짝/홀 분기의 기준값 생성
def bump_node(state: RouteState) -> dict:
    """증가 노드."""
    return {"n": state["n"] + 1}


# 2-2. 짝수 분기 노드: n에 100을 더함
def even_node(state: RouteState) -> dict:
    """짝수 처리 노드."""
    return {"n": state["n"] + 100}


# 2-3. 홀수 분기 노드: n에서 100을 뺌
def odd_node(state: RouteState) -> dict:
    """홀수 처리 노드."""
    return {"n": state["n"] - 100}


# 3. 조건 라우팅 함수 — 반환값이 다음 노드 이름을 결정
def pick_branch(state: RouteState) -> Literal["even", "odd"]:
    """짝수면 even, 홀수면 odd 노드로 라우팅."""
    return "even" if state["n"] % 2 == 0 else "odd"


# 4. 그래프 빌드 — 노드 등록, 고정 엣지, 조건 엣지 연결
graph = StateGraph(RouteState)

graph.add_node("bump", bump_node)
graph.add_node("even", even_node)
graph.add_node("odd", odd_node)

graph.add_edge(START, "bump")
graph.add_conditional_edges("bump", pick_branch, {"even": "even", "odd": "odd"})
graph.add_edge("even", END)
graph.add_edge("odd", END)

app = graph.compile()

if __name__ == "__main__":
    print("=== 예제 22: 조건 엣지(Conditional Edge) 라우팅 ===\n")

    # 5. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    # 6. 두 가지 케이스로 그래프 실행
    # n=3 → bump → 4(짝수) → even → 104
    result_even = app.invoke({"n": 3})
    # n=4 → bump → 5(홀수) → odd → -95
    result_odd = app.invoke({"n": 4})

    # 7. 결과 출력
    print(f"[짝수 분기] n=3 시작 → {result_even}")
    print(f"[홀수 분기] n=4 시작 → {result_odd}")
