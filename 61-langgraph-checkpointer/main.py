# langchain>=1.2, langgraph>=1.1
"""예제 23: MemorySaver 체크포인터로 대화 이력 유지하기."""

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


# 2. 상태 정의 — add_messages Reducer가 메시지를 덮어쓰지 않고 누적한다
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 3. LLM 초기화
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


# 4. 대화 노드 — 현재까지 누적된 messages를 LLM에 전달하고 응답을 추가
def chat_node(state: ChatState) -> dict:
    """대화 노드."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# 5. 그래프 빌드
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# 6. 체크포인터 생성 및 컴파일
#    MemorySaver: 인메모리 저장소 — 프로세스 종료 시 사라짐
#    checkpointer를 붙이면 invoke() 호출마다 상태가 thread_id별로 자동 저장된다
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    print("=== 예제 23: MemorySaver 체크포인터 ===\n")

    # 7. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    # 8. thread-A 연속 대화 — 같은 thread_id면 이전 상태를 이어받는다
    config_a = {"configurable": {"thread_id": "thread-A"}}
    print("─" * 50)
    print("[thread-A] 첫 번째 대화")
    print("─" * 50)

    result = app.invoke(
        {"messages": [HumanMessage(content="안녕! 내 이름은 로버트야.")]},
        config_a,
    )
    print(f"세션 ID : {config_a['configurable']['thread_id']}")
    print("사용자  : 안녕! 내 이름은 로버트야.")
    print(f"AI      : {result['messages'][-1].content}")
    print(f"누적 메시지 수: {len(result['messages'])}개\n")

    result = app.invoke(
        {"messages": [HumanMessage(content="내 이름이 뭐야?")]},
        config_a,
    )
    print("[thread-A] 두 번째 대화 — 이전 맥락 유지 확인")
    print("─" * 50)
    print(f"세션 ID : {config_a['configurable']['thread_id']}")
    print("사용자  : 내 이름이 뭐야?")
    print(f"AI      : {result['messages'][-1].content}")
    print(f"누적 메시지 수: {len(result['messages'])}개\n")

    # 9. thread-B 신규 세션 — 다른 thread_id는 독립된 상태에서 시작한다
    config_b = {"configurable": {"thread_id": "thread-B"}}
    print("[thread-B] 새 세션 — thread-A 기억 없음")
    print("─" * 50)

    result = app.invoke(
        {"messages": [HumanMessage(content="내 이름이 뭐야?")]},
        config_b,
    )
    print(f"세션 ID : {config_b['configurable']['thread_id']}")
    print("사용자  : 내 이름이 뭐야?")
    print(f"AI      : {result['messages'][-1].content}")
    print(f"누적 메시지 수: {len(result['messages'])}개")
