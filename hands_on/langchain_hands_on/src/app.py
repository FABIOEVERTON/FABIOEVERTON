"""Gradio UI for the research analyst system."""

import json
import gradio as gr

from src.workflow import run_research, get_snapshot, build_research_workflow


def run_pipeline(query: str, thread_id: str, db_path: str) -> str:
    if not query.strip():
        return "Please enter a research query."
    tid = thread_id.strip() if thread_id.strip() else None
    db = db_path.strip() if db_path.strip() else "output/checkpoints.db"
    try:
        final_state, memory, graph, config = run_research(query, tid, db)
        lines = []
        lines.append(f"**Thread ID:** `{final_state.get('thread_id', 'N/A')}`")
        lines.append(f"**Phase:** {final_state.get('current_phase', 'done')}")
        lines.append(f"**Confidence:** {final_state.get('confidence_score', 0):.1%}")
        lines.append(f"**Report Title:** {final_state.get('report_title', 'N/A')}")
        msgs = final_state.get("messages", [])
        if msgs:
            lines.append("\n### Pipeline Log")
            for m in msgs:
                lines.append(f"- {m}")
        body = final_state.get("report_body", "")
        if body:
            lines.append("\n### Report")
            lines.append(body)
        return "\n".join(lines)
    except Exception as e:
        return f"**Error:** {e}"


def show_snapshot(thread_id: str, db_path: str) -> str:
    if not thread_id.strip():
        return "Enter a thread ID."
    db = db_path.strip() if db_path.strip() else "output/checkpoints.db"
    graph, memory = build_research_workflow(db)
    config = {"configurable": {"thread_id": thread_id.strip()}}
    try:
        snap = get_snapshot(graph, config)
        return json.dumps(snap, indent=2, default=str)
    except Exception as e:
        return f"No checkpoint found: {e}"


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Research Analyst", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# AI Research Analyst")
        gr.Markdown("Multi-agent RAG research pipeline with LangGraph checkpointing.")

        with gr.Tab("Run Research"):
            query_input = gr.Textbox(label="Research Query", placeholder="Comparar OCI vs AWS para workloads de IA")
            thread_input = gr.Textbox(label="Thread ID (optional)", placeholder="auto-generated if empty")
            db_input = gr.Textbox(label="Checkpoint DB", value="output/checkpoints.db")
            run_btn = gr.Button("Run Pipeline", variant="primary")
            output_md = gr.Markdown(label="Result")
            run_btn.click(run_pipeline, inputs=[query_input, thread_input, db_input], outputs=output_md)

        with gr.Tab("Snapshot"):
            snap_thread = gr.Textbox(label="Thread ID")
            snap_db = gr.Textbox(label="Checkpoint DB", value="output/checkpoints.db")
            snap_btn = gr.Button("Get Snapshot")
            snap_output = gr.JSON(label="Snapshot")
            snap_btn.click(show_snapshot, inputs=[snap_thread, snap_db], outputs=snap_output)

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
