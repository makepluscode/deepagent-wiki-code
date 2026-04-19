# langchain>=1.2, langgraph>=1.1
"""예제 62: InMemoryStore로 thread_id를 넘는 장기 메모리 구현하기."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.store.memory import InMemoryStore

# 1. 환경변수 로드
load_dotenv()


# 2. 상태 정의
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: str  # 사용자 식별자 — store 조회 키


# 3. LLM 초기화
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


# 4. 대화 노드
#    모듈 레벨 store에서 사용자 프로필을 읽어 시스템 메시지에 주입한다
def chat_node(state: ChatState) -> dict:
    """장기 메모리를 활용하는 대화 노드."""
    user_id = state["user_id"]

    # 4-1. store에서 사용자 정보 조회 (namespace: ("users", user_id))
    memories = store.search(("users", user_id))
    user_info = "\n".join(f"- {m.value['fact']}" for m in memories) if memories else "없음"

    # 4-2. 사용자 정보를 시스템 메시지로 구성
    system = SystemMessage(content=f"사용자에 대해 알고 있는 정보:\n{user_info}")
    response = llm.invoke([system, *state["messages"]])
    return {"messages": [response]}


# 5. 기억 저장 노드
#    대화 내용에서 사용자 정보를 추출해 모듈 레벨 store에 저장한다
def save_memory_node(state: ChatState) -> dict:
    """사용자 발화에서 중요 정보를 추출해 store에 저장한다."""
    user_id = state["user_id"]
    last_human = next(
        (m.content for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        None,
    )
    if not last_human:
        return {}

    # 5-1. LLM으로 저장할 사실 추출
    extract_prompt = (
        f"다음 문장에서 사용자 개인 정보(이름, 직업, 취미, 선호 등)가 있으면 "
        f"한 줄로 요약해. 없으면 '없음'이라고만 답해.\n\n문장: {last_human}"
    )
    result = llm.invoke([HumanMessage(content=extract_prompt)])
    fact = str(result.content).strip()

    # 5-2. '없음'이 아니면 store에 저장
    if fact != "없음":
        existing = store.search(("users", user_id))
        store.put(("users", user_id), f"fact_{len(existing)}", {"fact": fact})
        print(f"  [메모리 저장] {fact}")

    return {}


# 6. 그래프 빌드 — chat → save_memory 순서로 실행
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_node("save_memory", save_memory_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", "save_memory")
graph.add_edge("save_memory", END)

# 6-1. MemorySaver: 단기 세션 상태 (thread_id별)
# 6-2. InMemoryStore: 장기 사용자 메모리 (user_id별, thread 초월)
checkpointer = MemorySaver()
store = InMemoryStore()
app = graph.compile(checkpointer=checkpointer, store=store)

if __name__ == "__main__":
    print("=== 예제 62: InMemoryStore 장기 메모리 ===\n")

    # 7. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    # 8. 세션 A — 사용자 정보 입력
    config_a = {"configurable": {"thread_id": "session-A"}}
    user_id = "robert"
    print("─" * 50)
    print("[세션 A] 사용자 정보 입력")
    print("─" * 50)

    for msg in ["안녕, 나는 로버트야. 파이썬 개발자로 일하고 있어.", "취미는 여행이야."]:
        result = app.invoke({"messages": [HumanMessage(content=msg)], "user_id": user_id}, config_a)
        print(f"사용자: {msg}")
        print(f"AI    : {result['messages'][-1].content}\n")

    # 9. 세션 B — 새 thread_id, 같은 user_id → store에서 기억 복원
    config_b = {"configurable": {"thread_id": "session-B"}}
    print("─" * 50)
    print("[세션 B] 새 세션에서 기억 확인 (thread 달라도 user_id 동일)")
    print("─" * 50)

    result = app.invoke(
        {"messages": [HumanMessage(content="내가 어떤 사람인지 알아?")], "user_id": user_id},
        config_b,
    )
    print("사용자: 내가 어떤 사람인지 알아?")
    print(f"AI    : {result['messages'][-1].content}")

    # store 내용 출력
    print("\n[store 저장된 메모리]")
    for m in store.search(("users", user_id)):
        print(f"  - {m.value['fact']}")
