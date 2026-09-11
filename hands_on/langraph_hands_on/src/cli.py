"""CLI interface for the LangGraph multi-agent system."""

import json
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

app = typer.Typer(
    name="langgraph-agent",
    help="LangGraph Multi-Agent System - Stateful agent workflows",
    add_completion=False,
)
console = Console()


@app.command()
def research(
    query: str = typer.Argument(..., help="Research query or topic"),
    thread_id: Optional[str] = typer.Option(None, "--thread-id", "-t", help="Thread ID for checkpointing"),
    db_path: str = typer.Option("output/checkpoints.db", "--db", help="SQLite checkpoint DB path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress"),
    no_export: bool = typer.Option(False, "--no-export", help="Don't export report to file"),
) -> None:
    """Conduct research using multi-agent workflow.

    Examples:
        python -m src.cli research "Comparar OCI vs AWS para workloads de IA"
        python -m src.cli research "Tendências de AI em 2026" --thread-id run-001
    """
    from src.workflow_persistent import create_persistent_workflow
    from src.states import create_initial_state
    from src.utils import get_snapshot

    console.print(Panel(f"[bold]Query:[/bold] {query}", title="Iniciando Workflow", border_style="blue"))

    try:
        graph = create_persistent_workflow(db_path)
        tid = thread_id or "default"
        config = {"configurable": {"thread_id": tid}}
        initial_state = create_initial_state(query)

        final_state = graph.invoke(initial_state, config)

        snap = get_snapshot(graph, config)
        console.print(f"\n[bold green]Done![/bold green]")
        console.print(f"[bold]Thread:[/bold] {tid}")
        console.print(f"[bold]Confidence:[/bold] {final_state.get('confidence_score', 0):.1%}")
        console.print(f"[bold]Phase:[/bold] {final_state.get('current_agent', 'done')}")

        title = final_state.get("report_title", "")
        summary = final_state.get("executive_summary", "")
        if title:
            console.print(f"\n[bold]Report:[/bold] {title}")
        if summary:
            console.print(Markdown(summary))
        if verbose and final_state.get("analysis"):
            console.print("\n[bold]Analysis:[/bold]")
            console.print(Markdown(final_state["analysis"]))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def snapshot(
    thread_id: str = typer.Argument(..., help="Thread ID to inspect"),
    db_path: str = typer.Option("output/checkpoints.db", "--db", help="SQLite checkpoint DB path"),
) -> None:
    """Show the checkpoint snapshot for a thread."""
    from src.workflow_persistent import create_persistent_workflow
    from src.utils import get_snapshot, format_snapshot

    try:
        graph = create_persistent_workflow(db_path)
        config = {"configurable": {"thread_id": thread_id}}
        snap = get_snapshot(graph, config)
        console.print_json(format_snapshot(snap))
    except Exception as e:
        console.print(f"[yellow]No checkpoint found for thread '{thread_id}': {e}[/yellow]")


@app.command()
def resume(
    thread_id: str = typer.Argument(..., help="Thread ID to resume from"),
    db_path: str = typer.Option("output/checkpoints.db", "--db", help="SQLite checkpoint DB path"),
    updates: Optional[str] = typer.Option(None, "--updates", "-u", help="JSON updates to inject"),
) -> None:
    """Resume a paused HITL workflow."""
    from src.workflow_hitl import create_hitl_workflow
    from src.utils import get_snapshot

    graph = create_hitl_workflow(db_path)
    config = {"configurable": {"thread_id": thread_id}}

    parsed_updates = {}
    if updates:
        try:
            parsed_updates = json.loads(updates)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON for --updates[/red]")
            raise typer.Exit(1)

    try:
        graph.update_state(config, parsed_updates)
        final = graph.invoke(None, config)
        console.print(f"[bold green]Resumed![/bold green] Phase: {final.get('current_agent', 'done')}")
    except Exception as e:
        console.print(f"[bold red]Error resuming:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def list_reports(
    output_dir: str = typer.Option("output", "--dir", "-d", help="Directory to list"),
) -> None:
    """List generated reports."""
    from pathlib import Path

    path = Path(output_dir)
    if not path.exists():
        console.print(f"[yellow]Directory not found: {output_dir}[/yellow]")
        return

    reports = list(path.glob("*.md"))
    if not reports:
        console.print("[yellow]No reports found[/yellow]")
        return

    console.print(f"[bold]Found {len(reports)} reports:[/bold]\n")
    for report in sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True):
        console.print(f"  {report.name}")


@app.command()
def review(
    file_path: str = typer.Argument(..., help="Path to report file"),
) -> None:
    """Review an existing report."""
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)

    content = path.read_text()
    console.print(Markdown(content))


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
