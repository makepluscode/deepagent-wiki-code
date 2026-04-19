# langchain>=1.2, langgraph>=1.1
"""예제 41: StateGraph로 가장 단순한 LLM 대화 노드 만들기."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# 1. 환경변수 로드
load_dotenv()


# 2. 상태(State) 정의
#    add_messages Reducer: invoke() 호출마다 messages를 덮어쓰지 않고 누적한다
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 3. LLM 초기화
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


# 4. 대화 노드 — 누적된 messages를 LLM에 전달하고 응답을 반환
def chat_node(state: ChatState) -> dict:
    """대화 노드."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# 5. 그래프 빌드 — START → chat → END 가장 단순한 구조
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)
app = graph.compile()

if __name__ == "__main__":
    print("=== 예제 41: StateGraph 단일 LLM 대화 노드 ===\n")

    # 6. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    # 7. 질문 목록 준비
    questions = [
        "LangGraph가 뭐야? 한 문장으로 설명해줘.",
        "StateGraph는 어디에 쓰여?",
    ]

    # 8. 질문마다 독립적으로 그래프 실행
    #    체크포인터 없음 → 호출 간 상태가 유지되지 않음 (매번 새 대화)
    print("─" * 50)
    for question in questions:
        result = app.invoke({"messages": [HumanMessage(content=question)]})

        # 9. 결과 출력
        print(f"[질문] {question}")
        print(f"[답변] {result['messages'][-1].content}")
        print(f"[메시지 수] {len(result['messages'])}개\n")
    print("─" * 50)
