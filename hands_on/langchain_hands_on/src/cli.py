"""CLI interface for the research analyst system."""

from pathlib import Path
from typing import Optional
import json

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

app = typer.Typer(
    name="research-analyst",
    help="AI Research Analyst - Multi-agent RAG research system",
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
    """Conduct research on a topic and generate a report.

    Examples:
        python -m src.cli research "Comparar OCI vs AWS para workloads de IA"
        python -m src.cli research "Tendências de AI em 2026" --thread-id run-001
    """
    from src.workflow import run_research

    console.print(Panel(f"[bold]Query:[/bold] {query}", title="Iniciando Pesquisa", border_style="blue"))

    try:
        final_state, memory, graph, config = run_research(
            query=query, thread_id=thread_id, db_path=db_path
        )

        console.print(f"\n[bold green]Done![/bold green]")
        console.print(f"[bold]Thread:[/bold] {final_state.get('thread_id', 'N/A')}")
        console.print(f"[bold]Confidence:[/bold] {final_state.get('confidence_score', 0):.1%}")
        console.print(f"[bold]Phase:[/bold] {final_state.get('current_phase', 'done')}")

        report_title = final_state.get("report_title", "")
        report_body = final_state.get("report_body", "")
        if report_title:
            console.print(f"\n[bold]Report:[/bold] {report_title}")
        if report_body and verbose:
            console.print(Markdown(report_body))

        msgs = final_state.get("messages", [])
        if msgs:
            console.print("\n[bold]Pipeline log:[/bold]")
            for m in msgs:
                console.print(f"  {m}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def snapshot(
    thread_id: str = typer.Argument(..., help="Thread ID to inspect"),
    db_path: str = typer.Option("output/checkpoints.db", "--db", help="SQLite checkpoint DB path"),
) -> None:
    """Show the checkpoint snapshot for a thread."""
    from src.workflow import build_research_workflow, get_snapshot

    graph, memory = build_research_workflow(db_path)
    config = {"configurable": {"thread_id": thread_id}}

    try:
        snap = get_snapshot(graph, config)
        console.print_json(json.dumps(snap, indent=2, default=str))
    except Exception as e:
        console.print(f"[yellow]No checkpoint found for thread '{thread_id}': {e}[/yellow]")


@app.command()
def resume(
    thread_id: str = typer.Argument(..., help="Thread ID to resume from"),
    db_path: str = typer.Option("output/checkpoints.db", "--db", help="SQLite checkpoint DB path"),
    updates: Optional[str] = typer.Option(None, "--updates", "-u", help="JSON updates to inject into state"),
) -> None:
    """Resume a paused workflow (e.g. after HITL interrupt)."""
    from src.workflow import build_research_workflow, human_override

    graph, memory = build_research_workflow(db_path)
    config = {"configurable": {"thread_id": thread_id}}

    parsed_updates = {}
    if updates:
        try:
            parsed_updates = json.loads(updates)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON for --updates[/red]")
            raise typer.Exit(1)

    try:
        final_state = human_override(graph, config, parsed_updates)
        console.print(f"[bold green]Resumed![/bold green] Phase: {final_state.get('current_phase', 'done')}")
    except Exception as e:
        console.print(f"[bold red]Error resuming:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def list_reports(
    output_dir: str = typer.Option("output", "--dir", "-d", help="Directory to list"),
) -> None:
    """List generated reports."""
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
