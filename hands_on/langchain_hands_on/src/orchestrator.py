"""Orchestrator - coordinates the flow between agents."""

import time
from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.agents.analyst import AnalystAgent
from src.agents.researcher import ResearcherAgent
from src.agents.reviewer import ReviewerAgent
from src.agents.writer import WriterAgent
from src.config import get_settings
from src.models import Report, ResearchResult
from src.tools.pdf_export import PDFExporter


@dataclass
class PipelineResult:
    """Result of the full research pipeline."""

    report: Report
    research: ResearchResult
    elapsed_time: float
    output_path: Optional[str] = None


class Orchestrator:
    """Orchestrates the research pipeline across all agents."""

    def __init__(self, verbose: bool = False) -> None:
        self.settings = get_settings()
        self.verbose = verbose
        self.console = Console()

        # Initialize agents
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent()
        self.exporter = PDFExporter()

    def run(self, query: str, export: bool = True) -> PipelineResult:
        """Execute the full research pipeline.

        Args:
            query: Research query.
            export: Whether to export the report to file.

        Returns:
            PipelineResult with report and metadata.
        """
        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            # Step 1: Research
            task = progress.add_task("[cyan]🔍 Researcher: Buscando informações...", total=None)
            research = self.researcher.research_sync(query)
            progress.update(task, description="[green]✅ Researcher: Coleta concluída")

            # Step 2: Analysis
            task = progress.add_task("[cyan]📊 Analyst: Processando dados...", total=None)
            analysis = self.analyst.analyze_sync(research)
            progress.update(task, description="[green]✅ Analyst: Análise concluída")

            # Step 3: Writing
            task = progress.add_task("[cyan]✍️ Writer: Gerando relatório...", total=None)
            report = self.writer.write_report_sync(research, analysis)
            progress.update(task, description=f"[green]✅ Writer: Relatório gerado ({report.word_count} palavras)")

            # Step 4: Review
            task = progress.add_task("[cyan]✅ Reviewer: Validando qualidade...", total=None)
            report = self.reviewer.review_sync(report, research)
            progress.update(task, description=f"[green]✅ Reviewer: Confidence {report.confidence_score:.0%}")

        elapsed_time = time.time() - start_time

        # Export if requested
        output_path = None
        if export:
            path = self.exporter.export_report(report)
            if path:
                output_path = str(path)

        return PipelineResult(
            report=report,
            research=research,
            elapsed_time=elapsed_time,
            output_path=output_path,
        )

    def print_summary(self, result: PipelineResult) -> None:
        """Print a summary of the pipeline execution.

        Args:
            result: PipelineResult to summarize.
        """
        report = result.report

        summary = f"""[bold]Title:[/bold] {report.title}
[bold]Query:[/bold] {report.query}
[bold]Confidence:[/bold] {report.confidence_score:.1%}
[bold]Word Count:[/bold] {report.word_count}
[bold]Sources:[/bold] {len(report.sources)}
[bold]Time:[/bold] {result.elapsed_time:.1f}s"""

        if result.output_path:
            summary += f"\n[bold]Output:[/bold] {result.output_path}"

        panel = Panel(summary, title="[bold green]Relatório Concluído[/bold green]", border_style="green")
        self.console.print(panel)


__all__ = ["Orchestrator", "PipelineResult"]
