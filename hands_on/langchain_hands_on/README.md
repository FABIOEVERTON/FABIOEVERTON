# LangChain Research Analyst — Multi-Agent RAG Pipeline

**4-agent research system using LangChain + Google Gemini. Specialized agents (Researcher → Analyst → Writer → Reviewer) collaborate to produce reports with confidence scoring.**

## What It Does

Takes a research query, dispatches it through a 4-agent pipeline, and produces a structured Markdown report with sources, confidence scores, and PDF export.

## Architecture

```mermaid
graph TD
    subgraph "CLI (Typer + Rich)"
        CLI[cli.py] -->|query| ORC[orchestrator.py]
    end

    subgraph "Pipeline"
        ORC --> R[ResearcherAgent<br/>web search + scrape + summarize]
        R -->|ResearchResult| A[AnalystAgent<br/>insights + comparisons + trends]
        A -->|AnalysisResult| W[WriterAgent<br/>structured report generation]
        W -->|Report| RE[ReviewerAgent<br/>quality scoring + revision]
    end

    subgraph "Tools"
        R --> WS[WebSearchTool<br/>Google Custom Search API]
        R --> SC[WebScraper<br/>Playwright + BeautifulSoup]
        RE -->|quality assessment| ORC
    end

    subgraph "Output"
        RE --> EXP[PDFExporter<br/>Markdown + PDF]
        EXP --> OUT[output/<br/>report.md + sources.md + score.json]
    end
```

## Agent Roles

| Agent | Responsibility | LLM Temp | Input → Output |
|-------|---------------|----------|----------------|
| **Researcher** | Web search, scrape URLs, generate summary | 0.3 | query → `ResearchResult` |
| **Analyst** | Extract insights, comparisons, trends, recommendations | 0.4 | `ResearchResult` → `AnalysisResult` |
| **Writer** | Generate structured report (title, executive summary, intro, analysis, conclusions) | 0.5 | `ResearchResult` + `AnalysisResult` → `Report` |
| **Reviewer** | Quality assessment (structure, evidence, clarity), revision, confidence scoring | 0.2 | `Report` → revised `Report` |

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as CLI
    participant O as Orchestrator
    participant R as Researcher
    participant A as Analyst
    participant W as Writer
    participant V as Reviewer
    participant P as PDF Exporter

    U->>C: research "OCI vs AWS"
    C->>O: run(query)
    O->>R: research_sync(query)
    R->>R: web_search → scrape → llm_summarize
    R-->>O: ResearchResult(sources, summary)
    O->>A: analyze_sync(research)
    A->>A: llm_analyze → parse_json
    A-->>O: AnalysisResult(insights, trends)
    O->>W: write_report_sync(research, analysis)
    W->>W: llm_write → parse_json
    W-->>O: Report(title, sections, confidence)
    O->>V: review_sync(report, research)
    V->>V: llm_review → score + revise
    V-->>O: revised Report(confidence updated)
    O->>P: export_report(report)
    P-->>O: output/report.md
    O-->>C: PipelineResult
```

## Tools

| Tool | Technology | Purpose |
|------|-----------|---------|
| **WebSearchTool** | Google Custom Search API | Find relevant URLs for query |
| **WebScraper** | Playwright + BeautifulSoup + Markdownify | Extract page content as Markdown |
| **PDFExporter** | Markdown → file | Export report to `output/` |

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `GOOGLE_STUDIO_API_KEY` | Required | Gemini API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | LLM model |
| `MAX_SOURCES` | `10` | Max sources per research |
| `SOURCE_TIMEOUT` | `30` | Scrape timeout (seconds) |
| `OUTPUT_DIR` | `output` | Report output directory |

## Usage

```bash
python -m src.cli research "Comparar OCI vs AWS para workloads de IA"
python -m src.cli research "Tendencias de AI em 2026" --verbose
python -m src.cli list-reports
python -m src.cli review ./output/report.md
```

## Project Structure

```
langchain_hands_on/
├── src/
│   ├── cli.py              # Typer CLI
│   ├── config.py           # Pydantic settings
│   ├── orchestrator.py     # Pipeline coordination + progress display
│   ├── workflow.py         # LangGraph wrapper (StateGraph + SQLite + HITL)
│   ├── agents/
│   │   ├── researcher.py   # Web search + scrape + summarize
│   │   ├── analyst.py      # Insights + comparisons + trends
│   │   ├── writer.py       # Structured report generation
│   │   ├── reviewer.py     # Quality scoring + revision
│   │   ├── react_agent.py  # ReAct agent variant
│   │   ├── researcher_v2.py
│   │   └── analyst_v2.py
│   ├── tools/
│   │   ├── web_search.py   # Google Custom Search
│   │   ├── scraper.py      # Playwright + BeautifulSoup
│   │   └── pdf_export.py   # Markdown export
│   ├── models/             # Pydantic schemas (Report, Source, Insight)
│   └── utils/              # Logger
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_orchestrator.py
├── output/                 # Generated reports
├── Dockerfile
└── pyproject.toml
```

## Tech Stack

- **Framework**: LangChain, LangGraph (workflow.py)
- **LLM**: Google Gemini 1.5 Flash
- **Scraping**: Playwright (headless Chromium), BeautifulSoup, Markdownify
- **CLI**: Typer + Rich (progress bars, panels)
- **Models**: Pydantic (schemas, config)
- **Export**: Markdown + PDF
- **Testing**: pytest + coverage
