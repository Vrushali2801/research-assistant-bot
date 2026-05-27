# Personal Research Assistant Agent

Autonomous research agent that searches the web, reads articles, and produces structured markdown reports from a single prompt. Built with LangGraph + Groq.

---

## Quick Demo

```bash
$ uv run python research_agent.py "impact of AI on software development"

Researching: impact of AI on software development
============================================================
  -> web_search({'max_results': 5, 'query': 'impact of AI on software development'})
  -> read_page({'max_chars': 3000, 'url': 'https://www.future-processing.com/blog/the-impact-of-ai-on-software-development-opportunitie...'})
  -> read_page({'max_chars': 3000, 'url': 'https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-ai-revolution-in-software...'})
  -> read_page({'max_chars': 3000, 'url': 'https://www.pace.edu/news/ai-software-development'})
  -> read_page({'max_chars': 3000, 'url': 'https://www.morganstanley.com/insights/articles/ai-software-development-industry-growth'})
  -> write_report({'content': '# Impact of AI on Software Development\n...'})

Report saved to: reports\ai_in_software_development.md

Agent finished.
```

### Generated report (`reports/ai_in_software_development.md`)

```markdown
# Impact of AI on Software Development

The impact of AI on software development is a topic of great interest and debate.
According to recent articles, AI is transforming the software development process,
making it more efficient, and enhancing productivity.

## Opportunities

AI-powered code generators can automate the creation of code snippets, modules, and
even entire applications, significantly speeding up development. AI can also assist
in testing and quality assurance by analyzing codebases for patterns associated with
defects or failures.

## Challenges

AI systems are limited to the knowledge and training data they have received, and
they lack the creativity and critical thinking abilities of humans.

## Conclusion

AI will augment and assist developers rather than replace them, making the process
more efficient and enhancing productivity.

## Sources

* https://www.future-processing.com/blog/the-impact-of-ai-on-software-development-opportunities-and-challenges/
* https://www.pace.edu/news/ai-software-development
```

---

## How It Works

The agent runs as a LangGraph `StateGraph`. At each step, the model either calls a tool or decides it has enough information to write the final report.

```
User enters topic
       │
       ▼
  ┌─────────────────────────────────┐
  │         LangGraph Agent         │
  │                                 │
  │  ┌─────────┐    ┌────────────┐  │
  │  │  Agent  │───▶│    Tools   │  │
  │  │  Node   │◀───│    Node    │  │
  │  └────┬────┘    └────────────┘  │
  │       │ stop                    │
  └───────┼─────────────────────────┘
          │
          ▼
    Report saved to reports/
```

**The 3 tools:**

| Tool | What it does |
|---|---|
| `web_search` | Searches DuckDuckGo, returns 5 URLs + snippets |
| `read_page` | Fetches a URL, strips HTML, returns clean text |
| `write_report` | Writes the final report to `reports/*.md` |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vrushali2801/research-assistant-bot.git
cd research-assistant-bot
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure API keys

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here

# Optional — LangSmith tracing (set to false to disable)
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=research-assistant
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

Get your **Groq API key** (free) at [console.groq.com](https://console.groq.com).  
Get your **LangSmith API key** (optional, free) at [smith.langchain.com](https://smith.langchain.com).

### 4. Run the agent

```bash
uv run python research_agent.py "your research topic here"
```

**Examples:**
```bash
uv run python research_agent.py "quantum computing breakthroughs 2025"
uv run python research_agent.py "sustainable fashion trends"
uv run python research_agent.py "AI in healthcare"
```

Reports are saved to the `reports/` folder as markdown files.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Agent Framework** | LangGraph 1.x (StateGraph + ReAct) |
| **LLM** | Groq — `llama-3.3-70b-versatile` |
| **LLM Client** | langchain-groq |
| **Web Search** | DuckDuckGo (`ddgs`) — no API key required |
| **Web Scraping** | requests + BeautifulSoup4 |
| **Observability** | LangSmith (optional) |
| **Package Manager** | uv |
| **Config** | python-dotenv |

---

## Project Structure

```
Personal-Research-Assistant-Agent/
├── research_agent.py   # LangGraph agent — model, tools, streaming loop
├── tools.py            # Tool implementations (web_search, read_page, write_report)
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Locked dependency versions
├── .env                # API keys (create this, never commit)
├── README.md           # This file
└── reports/            # Generated reports (auto-created)
```

---

## Features

- **Autonomous loop** — LangGraph StateGraph decides when to search, read, or write
- **Graceful error handling** — skips pages that 403/timeout, retries malformed tool calls
- **Structured reports** — title, findings, citations, sources all in markdown
- **Optional tracing** — full LangSmith trace of every tool call and LLM step
- **Free to run** — Groq free tier + DuckDuckGo, no paid APIs required

---

## Future Improvements

- [ ] Add support for academic papers (arXiv, Google Scholar)
- [ ] Generate citations in APA / MLA format
- [ ] Web UI for easier interaction
- [ ] Multi-language research support
- [ ] Fact-checking with cross-references
