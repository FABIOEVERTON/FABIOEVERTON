"""LangGraph workflow wrapper for the research pipeline.

Adds thread_id, SQLite checkpointing, HITL, and snapshot to the existing
multi-agent research pipeline.
"""

import sqlite3
import uuid
from typing import Literal, TypedDict, Annotated

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from src.agents.researcher import ResearcherAgent
from src.agents.analyst import AnalystAgent
from src.agents.writer import WriterAgent
from src.agents.reviewer import ReviewerAgent


def reduce_messages(left: list, right: list) -> list:
    return left + right


class ResearchState(TypedDict):
    query: str
    thread_id: str
    research_summary: str
    analysis_insights: str
    report_title: str
    report_body: str
    review_feedback: str
    confidence_score: float
    current_phase: Literal[
        "researching", "analyzing", "writing", "reviewing", "done"
    ]
    messages: Annotated[list, reduce_messages]


def researcher_node(state: dict) -> dict:
    agent = ResearcherAgent()
    result = agent.research_sync(state["query"])
    return {
        "research_summary": result.summary,
        "current_phase": "analyzing",
        "messages": [f"[Researcher] Collected {len(result.sources)} sources"],
    }


def analyst_node(state: dict) -> dict:
    from src.models import ResearchResult
    agent = AnalystAgent()
    research = ResearchResult(
        query=state["query"],
        summary=state.get("research_summary", ""),
    )
    result = agent.analyze_sync(research)
    insights_text = "\n".join(f"- {i.finding}" for i in result.insights)
    return {
        "analysis_insights": insights_text,
        "current_phase": "writing",
        "messages": [f"[Analyst] Generated {len(result.insights)} insights"],
    }


def writer_node(state: dict) -> dict:
    from src.models import ResearchResult, AnalysisResult
    agent = WriterAgent()
    research = ResearchResult(
        query=state["query"],
        summary=state.get("research_summary", ""),
    )
    analysis = AnalysisResult(
        trends=[state.get("analysis_insights", "")],
    )
    report = agent.write_report_sync(research, analysis)
    return {
        "report_title": report.title,
        "report_body": report.analysis,
        "confidence_score": report.confidence_score,
        "current_phase": "reviewing",
        "messages": [f"[Writer] Report: {report.title} ({report.word_count} words)"],
    }


def reviewer_node(state: dict) -> dict:
    from src.models import Report, ResearchResult
    agent = ReviewerAgent()
    report = Report(
        title=state.get("report_title", ""),
        query=state["query"],
        executive_summary="",
        introduction="",
        analysis=state.get("report_body", ""),
        conclusions="",
        confidence_score=state.get("confidence_score", 0.5),
    )
    research = ResearchResult(query=state["query"])
    reviewed = agent.review_sync(report, research)
    return {
        "review_feedback": f"Confidence: {reviewed.confidence_score:.0%}",
        "confidence_score": reviewed.confidence_score,
        "current_phase": "done",
        "messages": [f"[Reviewer] Confidence: {reviewed.confidence_score:.0%}"],
    }


def route_after_review(state: dict) -> str:
    phase = state.get("current_phase", "done")
    if phase == "done":
        return END
    return phase


def build_research_workflow(db_path: str = ":memory:"):
    graph = StateGraph(ResearchState)

    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("researcher")

    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_conditional_edges("reviewer", route_after_review, {
        END: END,
    })

    conn = sqlite3.connect(db_path, check_same_thread=False)
    memory = SqliteSaver(conn)

    compiled = graph.compile(
        checkpointer=memory,
        interrupt_before=["reviewer"],
    )

    return compiled, memory


def run_research(query: str, thread_id: str | None = None, db_path: str = ":memory:"):
    if thread_id is None:
        thread_id = str(uuid.uuid4())

    graph, memory = build_research_workflow(db_path)
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "query": query,
        "thread_id": thread_id,
        "research_summary": "",
        "analysis_insights": "",
        "report_title": "",
        "report_body": "",
        "review_feedback": "",
        "confidence_score": 0.0,
        "current_phase": "researching",
        "messages": [],
    }

    final_state = graph.invoke(initial_state, config)
    return final_state, memory, graph, config


def get_snapshot(graph, config):
    snapshot = graph.get_state(config)
    return {
        "values": snapshot.values,
        "next": snapshot.next,
        "config": snapshot.config,
        "metadata": snapshot.metadata,
        "created_at": snapshot.created_at,
        "tasks": [str(t) for t in snapshot.tasks],
    }


def human_override(graph, config, updates: dict):
    graph.update_state(config, updates)
    return graph.invoke(None, config)
