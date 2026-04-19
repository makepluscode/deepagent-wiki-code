# langchain>=1.2, langgraph>=1.1
"""예제 24: ToolNode로 LLM 도구 호출 에이전트 만들기."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# 1. 환경변수 로드
load_dotenv()


# 2. 도구 정의 — @tool 데코레이터로 LLM이 호출할 수 있는 함수를 등록
#    docstring이 LLM에게 전달되는 도구 설명이므로 반드시 작성한다
@tool
def add(a: int, b: int) -> int:
    """두 정수를 더한다."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """두 정수를 곱한다."""
    return a * b


tools = [add, multiply]


# 3. 상태 정의
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 4. LLM 초기화 + 도구 바인딩
#    bind_tools()로 LLM에게 사용 가능한 도구 목록을 알려준다
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
llm_with_tools = llm.bind_tools(tools)


# 5. 에이전트 노드 — 도구를 호출할지, 최종 답변을 낼지 LLM이 스스로 결정
def agent_node(state: AgentState) -> dict:
    """에이전트 노드."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 6. 그래프 빌드
#    ToolNode  : LLM이 요청한 도구를 실제로 실행하는 노드
#    tools_condition : LLM 응답에 tool_call이 있으면 tools로, 없으면 END로 분기
#    tools → agent 엣지 : 도구 실행 후 다시 agent로 돌아와 최종 답변 생성 (ReAct 루프)
graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

app = graph.compile()

if __name__ == "__main__":
    print("=== 예제 24: ToolNode 도구 호출 에이전트 ===\n")

    # 7. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    # 8. 도구 호출이 필요한 질문으로 그래프 실행
    #    두 단계 계산 → multiply → add 순서로 도구가 두 번 호출되는 흐름을 보여준다
    question = "3 곱하기 7은 얼마야? 그리고 거기에 15를 더하면?"
    result = app.invoke({"messages": [HumanMessage(content=question)]})

    # 9. 메시지 흐름 출력 — 도구 호출 과정을 단계별로 보여준다
    print(f"질문: {question}\n")
    print("─" * 50)
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"[사용자]      {msg.content}")
        elif isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"[도구 호출]   {tc['name']}({tc['args']})")
        elif isinstance(msg, ToolMessage):
            print(f"[도구 결과]   {msg.name} → {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"[최종 답변]   {msg.content}")
    print("─" * 50)
