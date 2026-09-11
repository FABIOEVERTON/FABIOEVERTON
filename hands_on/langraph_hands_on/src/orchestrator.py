"""Orchestrator for the LangGraph system."""

import time
from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.config import get_settings
from src.states import AgentState, create_initial_state
from src.tools.pdf_export import PDFExporter
from src.workflow import graph


@dataclass
class PipelineResult:
    """Result of the workflow execution."""

    final_state: AgentState
    elapsed_time: float
    output_path: Optional[str] = None


class Orchestrator:
    """Orchestrates the LangGraph workflow."""

    def __init__(self, verbose: bool = False) -> None:
        self.settings = get_settings()
        self.verbose = verbose
        self.console = Console()
        self.exporter = PDFExporter()

    def run(self, query: str, export: bool = True) -> PipelineResult:
        """Execute the workflow.

        Args:
            query: Research query.
            export: Whether to export the report to file.

        Returns:
            PipelineResult with final state and metadata.
        """
        start_time = time.time()

        # Create initial state
        initial_state = create_initial_state(query)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            # Execute workflow
            task = progress.add_task("[cyan]🔄 Executing workflow...", total=None)

            # Run the graph
            final_state = None
            for step in graph.stream(initial_state, {"recursion_limit": 10}):
                if self.verbose:
                    for node_name, node_output in step.items():
                        progress.update(
                            task,
                            description=f"[cyan]🔄 {node_name}: Processing...",
                        )
                        # Print detailed info if verbose
                        if "messages" in node_output:
                            for msg in node_output["messages"]:
                                if hasattr(msg, "content"):
                                    self.console.print(f"  [dim]{msg.content}[/dim]")

                # Get the last state
                for node_name, node_output in step.items():
                    final_state = node_output

            progress.update(task, description="[green]✅ Workflow complete")

        elapsed_time = time.time() - start_time

        # Merge final state
        if final_state:
            # Merge all updates into initial state
            merged_state = dict(initial_state)
            for key, value in final_state.items():
                if key in merged_state:
                    if key == "messages":
                        merged_state[key].extend(value)
                    else:
                        merged_state[key] = value
            final_state = merged_state
        else:
            final_state = initial_state

        # Export if requested
        output_path = None
        if export:
            path = self.exporter.export_report(final_state)
            if path:
                output_path = str(path)

        return PipelineResult(
            final_state=final_state,
            elapsed_time=elapsed_time,
            output_path=output_path,
        )

    def print_summary(self, result: PipelineResult) -> None:
        """Print a summary of the workflow execution.

        Args:
            result: PipelineResult to summarize.
        """
        state = result.final_state

        summary = f"""[bold]Title:[/bold] {state.get('report_title', 'N/A')}
[bold]Query:[/bold] {state.get('query', 'N/A')}
[bold]Confidence:[/bold] {state.get('confidence_score', 0):.1%}
[bold]Sources:[/bold] {len(state.get('sources', []))}
[bold]Insights:[/bold] {len(state.get('insights', []))}
[bold]Time:[/bold] {result.elapsed_time:.1f}s"""

        if result.output_path:
            summary += f"\n[bold]Output:[/bold] {result.output_path}"

        panel = Panel(summary, title="[bold green]Workflow Concluído[/bold green]", border_style="green")
        self.console.print(panel)


__all__ = ["Orchestrator", "PipelineResult"]
