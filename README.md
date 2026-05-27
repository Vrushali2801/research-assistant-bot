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

**See [FLOW_DIAGRAM.md](FLOW_DIAGRAM.md) for detailed architecture**

---

## Setup (5 Minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/research-agent.git
cd research-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
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
research-agent/
├── main.py                 # Entry point
├── research_agent.py       # Main agent logic with Groq API integration
├── tools.py               # Tool implementations (search, read, write)
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this)
├── README.md             # This file
├── FLOW_DIAGRAM.md       # Detailed architecture diagram
└── reports/              # Generated research reports (auto-created)
    ├── electric_vehicles.md
    ├── quantum_computing.md
    └── ...
```

---

## How the Agent Works (Simple Version)

### Tool 1: web_search()
Searches DuckDuckGo for articles matching your topic. Returns URLs, titles, and snippets.

### Tool 2: read_page()
Downloads a webpage, removes junk (ads, navigation), and extracts clean text content.

### Tool 3: write_report()
Synthesizes all gathered information into a well-structured markdown report and saves it.

### The Loop
1. AI reads your topic: _"Research electric vehicles"_
2. AI decides: _"I should search for articles"_ → calls `web_search()`
3. AI reads results: _"These 3 articles look good"_ → calls `read_page()` 3 times
4. AI synthesizes: _"Now I'll write the report"_ → calls `write_report()`
5. AI finishes: _"Report saved, I'm done!"_ → Loop ends

---

## Customization

### Change the Model
Edit `research_agent.py` line 125:
```python
model="llama-3.3-70b-versatile",  # Change to another Groq model
```

Available Groq models: [console.groq.com](https://console.groq.com)

### Adjust Search Results
Edit `tools.py` to change default results:
```python
def web_search(query: str, max_results: int = 5) -> list[dict]:
    # Change 5 to 10 for more results
```

### Customize Report Format
Edit the `SYSTEM_PROMPT` in `research_agent.py` to specify report style:
```python
SYSTEM_PROMPT = """You are a research assistant that writes reports in:
- Academic tone
- Bullet-point format
- Include criticisms and limitations
- (customize as needed)
"""
```

---

## Troubleshooting

**"Error: No API key provided"**
- Create a `.env` file with `GROQ_API_KEY=your_key`
- Make sure you have a valid Groq API key from [console.groq.com](https://console.groq.com)

**"No module named 'groq'"**
- Run `pip install -r requirements.txt`
- Check you're using Python 3.8+

**"requests.exceptions.Timeout"**
- Some websites are slow or blocking scraping. The agent will try different sources.

**Empty report**
- The topic might be too obscure. Try more common topics like "AI trends 2025"

---

## Future Improvements

- [ ] Add support for academic papers (arXiv, Google Scholar)
- [ ] Generate citations in different formats (APA, Chicago, MLA)
- [ ] Add web UI for easier interaction
- [ ] Support for multi-language research
- [ ] Integration with LangGraph for more complex workflows
- [ ] Fact-checking with cross-references
- [ ] Image and data visualization support

---

## License

MIT License - feel free to use and modify

---

## Questions?

- Check [FLOW_DIAGRAM.md](FLOW_DIAGRAM.md) for detailed architecture
- Open an issue for bugs or feature requests
- See comments in code for implementation details

---

**Happy researching! 🚀**
