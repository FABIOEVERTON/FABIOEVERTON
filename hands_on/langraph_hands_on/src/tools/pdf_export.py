"""PDF export tool for reports."""

from pathlib import Path
from typing import Optional

from src.config import get_settings
from src.states import AgentState


class PDFExporter:
    """Export reports to file format."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.output_dir = self.settings.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_report(self, state: AgentState) -> Optional[Path]:
        """Export a report from state to file.

        Args:
            state: AgentState with report data.

        Returns:
            Path to the generated file or None if failed.
        """
        try:
            # Generate filename from title and date
            title = state.get("report_title", "report")
            safe_title = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in title)
            safe_title = safe_title.replace(" ", "_")[:50]
            date_str = __import__("datetime").datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"report_{date_str}_{safe_title}.md"

            # Build markdown content
            content = f"""# {state.get('report_title', 'Research Report')}

**Research Query:** {state.get('query', '')}
**Confidence Score:** {state.get('confidence_score', 0):.1%}
**Sources:** {len(state.get('sources', []))}

---

## Executive Summary

{state.get('executive_summary', '')}

---

## Introduction

{state.get('introduction', '')}

---

## Analysis

{state.get('analysis', '')}

---

## Conclusions

{state.get('conclusions', '')}

---

## Sources

"""
            for i, source in enumerate(state.get("sources", []), 1):
                content += f"{i}. [{source.get('title', 'Unknown')}]({source.get('url', '')})\n"

            output_path = self.output_dir / filename
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            return output_path

        except Exception as e:
            print(f"Error exporting report: {e}")
            return None


__all__ = ["PDFExporter"]
