# langchain>=1.2, langgraph>=1.1
"""예제 71: interrupt_before로 사람 승인 게이트 구현하기."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# 1. 환경변수 로드
load_dotenv()


# 2. 상태 정의
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    draft: str  # LLM이 작성한 이메일 초안


# 3. LLM 초기화
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


# 4. 초안 작성 노드 — LLM이 이메일 초안을 작성한다
def draft_node(state: AgentState) -> dict:
    """이메일 초안 작성 노드."""
    request = state["messages"][-1].content
    response = llm.invoke(
        [HumanMessage(content=f"다음 요청에 맞는 짧은 이메일 초안을 작성해:\n\n{request}")]
    )
    draft = str(response.content)
    print(f"[초안 작성 완료]\n{draft}")
    return {"draft": draft, "messages": [response]}


# 5. 발송 노드 — 사람이 승인한 후에만 실행된다
def send_node(state: AgentState) -> dict:
    """이메일 발송 노드 — interrupt_before로 보호된다."""
    print("[발송 완료] 이메일이 성공적으로 발송되었습니다.")
    return {"messages": [HumanMessage(content="이메일 발송 완료")]}


# 6. 그래프 빌드
#    interrupt_before=["send"]: send 노드 실행 직전에 그래프가 일시 정지된다
#    재개하려면 같은 thread_id로 다시 invoke(None, config)를 호출한다
graph = StateGraph(AgentState)
graph.add_node("draft", draft_node)
graph.add_node("send", send_node)
graph.add_edge(START, "draft")
graph.add_edge("draft", "send")
graph.add_edge("send", END)

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer, interrupt_before=["send"])

if __name__ == "__main__":
    print("=== 예제 71: interrupt_before 사람 승인 게이트 ===\n")

    # 7. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    config = {"configurable": {"thread_id": "hitl-demo"}}

    # 8. 첫 번째 invoke — draft 노드 실행 후 send 직전에서 자동 중단
    print("─" * 50)
    print("[실행 1] 이메일 초안 작성 요청")
    print("─" * 50)
    app.invoke(
        {"messages": [HumanMessage(content="팀장님께 이번 주 업무 완료 보고 이메일 작성해줘")]},
        config,
    )

    # 그래프 상태 확인 — send 노드 직전에서 멈춘 것을 확인
    state = app.get_state(config)
    print(f"다음 실행 예정 노드: {state.next}")

    # 9. 사람이 직접 승인 여부를 입력 — y면 재개, 그 외면 취소
    print("─" * 50)
    answer = input("초안을 발송하시겠습니까? (y/n): ").strip().lower()
    print("─" * 50)

    if answer == "y":
        app.invoke(None, config)
        state = app.get_state(config)
        print(f"다음 실행 예정 노드: {state.next} (빈 튜플 = 완료)")
    else:
        print("[취소] 발송이 취소되었습니다.")
