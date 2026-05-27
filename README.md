# Personal Research Assistant Agent

Autonomous research agent that searches the web, reads articles, and produces structured markdown reports from a single prompt.

---

## Quick Demo

### Terminal Output Example

```bash
$ python research_agent.py "electric vehicles market trends 2025"

Researching: electric vehicles market trends 2025
============================================================
  -> web_search({'query': 'electric vehicles market trends 2025', 'max_results': 5})
  -> read_page({'url': 'https://example.com/ev-trends'})
  -> read_page({'url': 'https://example.com/ev-sales'})
  -> read_page({'url': 'https://example.com/ev-future'})
  -> write_report({'filename': 'ev_market_trends', 'content': '# Electric Vehicles Market Trends 2025\n\n## Overview\n...'})

Report saved to: reports/ev_market_trends.md

Agent finished.
```

### Generated Report Example

**reports/ev_market_trends.md**
```markdown
# Electric Vehicles Market Trends 2025

## Overview
The global EV market continues rapid expansion with significant growth in both 
battery technology and charging infrastructure.

## Key Findings
- Global EV sales reached 14M units in 2024
- Battery costs dropped 20% year-over-year
- Charging networks expanded by 35% globally
- China maintains 60% market share

## Market Segments
### Luxury EVs
- Strong demand from Tesla, BMW i, Mercedes-Benz EQS

### Mass-Market EVs  
- BYD leading in affordable models
- New competitors from traditional automakers

## Technology Advances
- Solid-state batteries entering production phase
- 800V fast charging becoming standard
- Range improvements reaching 500+ miles

## Sources
- https://example.com/ev-trends
- https://example.com/ev-sales
- https://example.com/ev-future
```

---

## How It Works

```
┌─────────────────────────────────────┐
│   User enters research topic        │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Groq AI Agent receives task         │
│  with tool definitions              │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Iteration Loop │
        └────────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│ Search │  │  Read  │  │  Write   │
│ Web    │  │Article │  │  Report  │
└────────┘  └────────┘  └──────────┘
    │            │            │
    └────────────┼────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  All done?      │
        │  (finish_reason │
        │   == "stop")    │
        └────┬────────┬───┘
             │        │
           YES       NO
             │        │
             ▼        └──► Back to loop
        ┌──────────┐
        │  Report  │
        │  Saved!  │
        └──────────┘
```
---

## Setup (5 Minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/Vrushali2801/web-research-bot.git
cd web-research-bot
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Get Your Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free tier available)
3. Generate an API key
4. Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_api_key_here
```

### 4. Run the Agent
```bash
python research_agent.py "your research topic here"
```

**Examples:**
```bash
python research_agent.py "quantum computing breakthroughs"
python research_agent.py "sustainable fashion trends"
python research_agent.py "AI in healthcare 2025"
```

Reports are automatically saved to the `reports/` folder as markdown files.

---

## What Gets Generated

✅ **Comprehensive Research Report** with:
- Clear title and introduction
- Key findings with statistics
- Organized sections and subsections
- Direct citations with source URLs
- Well-structured markdown formatting

The agent:
1. Searches for 5 relevant articles using DuckDuckGo
2. Reads the 3-4 most promising sources
3. Synthesizes findings into a structured report
4. Saves to `reports/` directory with markdown formatting

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **AI Model** | Groq API (Llama 3.3-70B) | Fast, cost-effective, open-source model |
| **Web Search** | DuckDuckGo Search API | Privacy-focused, free, no API key required |
| **Web Scraping** | BeautifulSoup + requests | Parse HTML, extract clean text content |
| **Language** | Python 3.8+ | Simple, readable, great libraries |
| **Package Manager** | uv | Fast Python package manager (replaces pip) |
| **Environment** | python-dotenv | Secure API key management |

---

## Features

- 🔍 **Autonomous Search** - Finds relevant articles without manual curation
- 📖 **Smart Reading** - Extracts content and removes noise (ads, navigation, etc.)
- 📝 **Structured Reports** - Organized markdown with citations and sources
- 🔄 **Agentic Loop** - AI decides when to search, read, and write
- ⚡ **Fast** - Uses Groq's fast inference for quick responses
- 🆓 **Free** - Uses free/low-cost APIs (Groq free tier, DuckDuckGo free)

---

## Project Structure

```
web-research-bot/
├── main.py                 # Entry point
├── research_agent.py       # Main agent logic with Groq API integration
├── tools.py               # Tool implementations (search, read, write)
├── pyproject.toml         # Project metadata and dependencies (uv)
├── uv.lock                # Locked dependencies (uv)
├── .env                   # API keys (create this)
├── README.md             # This file
└── reports/              # Generated research reports (auto-created)
    ├── electric_vehicles.md
    ├── quantum_computing.md
    └── ...
```

## Future Improvements

- [ ] Add support for academic papers (arXiv, Google Scholar)
- [ ] Generate citations in different formats (APA, Chicago, MLA)
- [ ] Add web UI for easier interaction
- [ ] Support for multi-language research
- [ ] Integration with LangGraph for more complex workflows
- [ ] Fact-checking with cross-references
- [ ] Image and data visualization support

---


**Happy researching! 🚀**
