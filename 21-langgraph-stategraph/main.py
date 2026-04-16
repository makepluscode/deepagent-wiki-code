# langchain>=1.2, langgraph>=1.1
"""예제 21: StateGraph로 첫 번째 워크플로우 만들기.

State → Node → Edge 세 가지 개념으로 구성한
3단계 텍스트 처리 파이프라인을 구현한다.

실행 방법:
    DEEPAGENT_EXAMPLE_MOCK=1 uv run python main.py   # 기본(Mock)
    DEEPAGENT_EXAMPLE_MOCK=0 uv run python main.py   # 실제 LLM 호출
"""

from __future__ import annotations

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()

# 환경변수로 모드 전환 — 기본값은 Mock(API 키 불필요)
USE_MOCK: bool = os.getenv("DEEPAGENT_EXAMPLE_MOCK", "1") == "1"


class PipelineState(TypedDict):
    """파이프라인 전체가 공유하는 상태.

    messages: 대화 이력 (add_messages Reducer로 누적)
    text:     처리할 원문
    summary:  1단계 결과 — 요약문
    keywords: 2단계 결과 — 핵심 키워드 목록
    report:   3단계 결과 — 최종 보고서
    """

    messages: Annotated[list[BaseMessage], add_messages]
    text: str
    summary: str
    keywords: list[str]
    report: str


# ---------------------------------------------------------------------------
# 노드 함수
# ---------------------------------------------------------------------------

def summarize(state: PipelineState) -> dict:
    """1단계 노드: 원문을 한 문장으로 요약한다."""
    text = state["text"]

    if USE_MOCK:
        # Mock 모드 — LLM 호출 없이 고정 응답 반환
        result = f"[요약] {text[:40]}..."
    else:
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
        prompt = f"다음 텍스트를 한 문장으로 요약하라:\n\n{text}"
        response = llm.invoke([HumanMessage(content=prompt)])
        result = str(response.content)

    return {
        "summary": result,
        "messages": [AIMessage(content=f"요약 완료: {result}")],
    }


def extract_keywords(state: PipelineState) -> dict:
    """2단계 노드: 요약문에서 핵심 키워드를 추출한다."""
    summary = state["summary"]

    if USE_MOCK:
        # Mock 모드 — 요약에서 첫 세 단어를 키워드로 사용
        words = summary.replace("[요약]", "").split()
        result = [w.strip(".,") for w in words[:3] if w.strip(".,")]
    else:
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
        prompt = f"다음 요약에서 핵심 키워드 3개를 쉼표로 구분해 추출하라:\n\n{summary}"
        response = llm.invoke([HumanMessage(content=prompt)])
        result = [k.strip() for k in str(response.content).split(",")]

    return {
        "keywords": result,
        "messages": [AIMessage(content=f"키워드 추출 완료: {result}")],
    }


def generate_report(state: PipelineState) -> dict:
    """3단계 노드: 요약과 키워드를 조합해 최종 보고서를 작성한다."""
    summary = state["summary"]
    keywords = state["keywords"]

    if USE_MOCK:
        # Mock 모드 — 템플릿으로 보고서 생성
        kw_str = ", ".join(keywords)
        result = (
            f"## 분석 보고서\n\n"
            f"**요약:** {summary}\n\n"
            f"**핵심 키워드:** {kw_str}\n\n"
            f"**결론:** 위 내용을 바탕으로 추가 검토가 필요하다."
        )
    else:
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
        prompt = (
            f"다음 요약과 키워드를 바탕으로 짧은 분석 보고서를 작성하라.\n\n"
            f"요약: {summary}\n키워드: {', '.join(keywords)}"
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        result = str(response.content)

    return {
        "report": result,
        "messages": [AIMessage(content="보고서 생성 완료")],
    }


# ---------------------------------------------------------------------------
# 그래프 빌더
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    """StateGraph를 조립하고 컴파일해 반환한다.

    구조: START → summarize → extract_keywords → generate_report → END
    """
    graph = StateGraph(PipelineState)

    # 노드 등록
    graph.add_node("summarize", summarize)
    graph.add_node("extract_keywords", extract_keywords)
    graph.add_node("generate_report", generate_report)

    # 엣지 연결 (고정 순서)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "extract_keywords")
    graph.add_edge("extract_keywords", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

def main() -> None:
    """예제 실행 진입점."""
    mode_label = "Mock" if USE_MOCK else "LLM"
    print(f"=== 예제 21: StateGraph 텍스트 파이프라인 [{mode_label} 모드] ===\n")

    # 처리할 원문
    sample_text = (
        "LangGraph는 LLM 애플리케이션을 상태 기반 그래프로 표현하는 프레임워크다. "
        "State, Node, Edge 세 개념으로 복잡한 워크플로우를 선언적으로 정의할 수 있다."
    )

    app = build_graph()
    result = app.invoke(
        {
            "text": sample_text,
            "messages": [HumanMessage(content=sample_text)],
            "summary": "",
            "keywords": [],
            "report": "",
        }
    )

    # 결과 출력
    print(f"[원문]\n{sample_text}\n")
    print(f"[요약]\n{result['summary']}\n")
    print(f"[키워드]\n{result['keywords']}\n")
    print(f"[보고서]\n{result['report']}\n")
    print(f"[처리 메시지 수] {len(result['messages'])}개")


if __name__ == "__main__":
    main()
