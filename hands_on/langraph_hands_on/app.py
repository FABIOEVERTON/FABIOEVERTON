"""Gradio interface for the LangGraph multi-agent system."""

import json

try:
    import gradio as gr
    HAS_GRADIO = True
except ImportError:
    HAS_GRADIO = False

from src.states import create_initial_state


def research_chat(message: str, history: list, thread_id: str) -> str:
    """Chat function for Gradio interface.

    Args:
        message: User message.
        history: Chat history.
        thread_id: Thread ID for checkpointing.

    Returns:
        Agent response.
    """
    try:
        from src.workflow_persistent import create_persistent_workflow
        from src.utils import get_snapshot

        graph = create_persistent_workflow()
        tid = thread_id.strip() if thread_id and thread_id.strip() else "gradio-default"
        config = {"configurable": {"thread_id": tid}}
        state = create_initial_state(message)

        final_state = graph.invoke(state, config)

        response_parts = []
        response_parts.append(f"**Thread:** `{tid}`")
        response_parts.append(f"**Confidence:** {final_state.get('confidence_score', 0):.1%}")

        title = final_state.get("report_title", "")
        summary = final_state.get("executive_summary", "")
        if title:
            response_parts.append(f"\n**Report:** {title}")
        if summary:
            response_parts.append(f"\n{summary}")

        snap = get_snapshot(graph, config)
        msgs = final_state.get("messages", [])
        if msgs:
            response_parts.append("\n---\n**Pipeline Log:**")
            for m in msgs:
                if hasattr(m, "content"):
                    response_parts.append(f"- {m.content}")
                elif isinstance(m, tuple) and len(m) >= 2:
                    response_parts.append(f"- [{m[0]}] {m[1]}")

        return "\n".join(response_parts) if response_parts else "No response generated."

    except Exception as e:
        return f"Error: {str(e)}"


def create_gradio_interface():
    """Create Gradio interface.

    Returns:
        Gradio Blocks interface.
    """
    if not HAS_GRADIO:
        raise ImportError("Gradio not installed. Run: pip install gradio")

    with gr.Blocks(
        title="AI Research Analyst",
        theme=gr.themes.Soft(),
    ) as demo:
        gr.Markdown("# AI Research Analyst")
        gr.Markdown("Multi-agent research system using LangGraph with checkpointing.")

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Research Chat",
                    height=500,
                )
                msg = gr.Textbox(
                    label="Enter your research query",
                    placeholder="Ex: Comparar OCI vs AWS para workloads de IA",
                )
                thread_input = gr.Textbox(
                    label="Thread ID (optional)",
                    placeholder="auto-generated if empty",
                )
                with gr.Row():
                    submit = gr.Button("Research", variant="primary")
                    clear = gr.Button("Clear")

            with gr.Column(scale=1):
                gr.Markdown("### Examples")
                examples = gr.Examples(
                    examples=[
                        "Comparar n8n vs Make.com para automação de IA",
                        "Tendências de AI em 2026",
                        "Melhores práticas para RAG em produção",
                    ],
                    inputs=msg,
                )

        def respond(message, chat_history, thread_id):
            response = research_chat(message, chat_history, thread_id)
            chat_history.append((message, response))
            return "", chat_history

        msg.submit(respond, [msg, chatbot, thread_input], [msg, chatbot])
        submit.click(respond, [msg, chatbot, thread_input], [msg, chatbot])
        clear.click(lambda: [], None, chatbot)

    return demo


def launch_app(share: bool = False, port: int = 7860):
    """Launch the Gradio app.

    Args:
        share: Create public link.
        port: Port number.
    """
    demo = create_gradio_interface()
    demo.launch(share=share, server_port=port)
