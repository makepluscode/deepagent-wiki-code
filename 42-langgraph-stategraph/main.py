# langchain>=1.2, langgraph>=1.1
"""예제 21: StateGraph로 첫 번째 워크플로우 만들기."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

# 1. 환경변수 로드
load_dotenv()


# 2. 상태(State) 정의 — 모든 노드가 읽고 쓰는 공유 데이터 구조
class PipelineState(TypedDict):
    text: str  # 처리할 원문
    summary: str  # 1단계 결과: 요약문
    keywords: list[str]  # 2단계 결과: 핵심 키워드
    report: str  # 3단계 결과: 최종 보고서


# 3. LLM 초기화
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


# 4-1. 첫 번째 노드: 원문을 한 문장으로 요약
def summarize_node(state: PipelineState) -> dict:
    """요약 노드."""
    response = llm.invoke(
        [HumanMessage(content=f"다음 텍스트를 한 문장으로 요약하라:\n\n{state['text']}")]
    )
    return {"summary": str(response.content)}


# 4-2. 두 번째 노드: 요약에서 핵심 키워드 3개 추출
def extract_keywords_node(state: PipelineState) -> dict:
    """키워드 추출 노드."""
    response = llm.invoke(
        [
            HumanMessage(
                content=f"다음 요약에서 핵심 키워드 3개를 쉼표로 구분해 추출하라:\n\n{state['summary']}"
            )
        ]
    )
    return {"keywords": [k.strip() for k in str(response.content).split(",")]}


# 4-3. 세 번째 노드: 요약과 키워드로 보고서 생성
def generate_report_node(state: PipelineState) -> dict:
    """보고서 생성 노드."""
    response = llm.invoke(
        [
            HumanMessage(
                content=(
                    f"요약: {state['summary']}\n"
                    f"키워드: {', '.join(state['keywords'])}\n\n"
                    "위 내용으로 짧은 분석 보고서를 작성하라."
                )
            )
        ]
    )
    return {"report": str(response.content)}


# 5. 그래프 빌드 — 노드 등록과 엣지 연결
graph = StateGraph(PipelineState)

graph.add_node("summarize", summarize_node)
graph.add_node("extract_keywords", extract_keywords_node)
graph.add_node("generate_report", generate_report_node)

graph.add_edge(START, "summarize")
graph.add_edge("summarize", "extract_keywords")
graph.add_edge("extract_keywords", "generate_report")
graph.add_edge("generate_report", END)

app = graph.compile()

if __name__ == "__main__":
    print("=== 예제 21: StateGraph 텍스트 파이프라인 ===\n")

    # 6. 그래프 구조를 PNG로 저장
    with Path("graph.png").open("wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("그래프 구조 저장 완료: graph.png\n")

    # 7. 입력 데이터 준비
    sample_text = (
        "LangGraph는 LLM 애플리케이션을 상태 기반 그래프로 표현하는 프레임워크다. "
        "State, Node, Edge 세 개념으로 복잡한 워크플로우를 선언적으로 정의할 수 있다."
    )

    # 8. 그래프 실행
    result = app.invoke({"text": sample_text, "summary": "", "keywords": [], "report": ""})

    # 9. 결과 출력
    print(f"[원문]\n{sample_text}\n")
    print(f"[요약]\n{result['summary']}\n")
    print(f"[키워드]\n{result['keywords']}\n")
    print(f"[보고서]\n{result['report']}")
