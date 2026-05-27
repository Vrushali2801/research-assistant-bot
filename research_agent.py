import sys
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
from tools import web_search, read_page, write_report

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search DuckDuckGo for articles relevant to a query. "
                "Returns a list of results with url, title, and snippet fields."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default 5).",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": (
                "Fetch a web page by URL and return its cleaned text content. "
                "Use this to read the full contents of an article."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the page to fetch and read.",
                    },
                    "max_chars": {
                        "type": "integer",
                        "description": "Maximum characters to return (default 8000).",
                    },
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_report",
            "description": (
                "Write the final research report to a markdown file in the reports/ directory. "
                "Call this once you have synthesized all findings into a complete report."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The filename for the report (e.g. 'electric_vehicles_report'). .md will be appended if missing.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The full markdown content of the report.",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a thorough research assistant. When given a topic, you:

1. Use web_search to find 5 relevant articles on the topic.
2. Use read_page to read the full content of at least 3-4 of the most promising sources.
3. Synthesize the information into a well-structured markdown report that includes:
   - A title and brief introduction
   - Key findings organized under clear headings
   - Specific facts, statistics, and insights drawn from the sources
   - A summary/conclusion section
   - A "Sources" section listing the URLs you read
4. Use write_report to save the final report to a file.

Be thorough, accurate, and cite sources within the report where relevant."""


def execute_tool(name: str, inputs: dict):
    if name == "web_search":
        return web_search(**inputs)
    elif name == "read_page":
        return read_page(**inputs)
    elif name == "write_report":
        return write_report(**inputs)
    else:
        raise ValueError(f"Unknown tool: {name}")


def run_research_agent(topic: str):
    client = Groq()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research this topic and write a report: {topic}"},
    ]

    print(f"\nResearching: {topic}\n{'=' * 60}")

    max_iterations = 20
    for iteration in range(max_iterations):
        # Retry up to 3 times on malformed tool-call generation
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=4096,
                    tools=TOOLS,
                    tool_choice="auto",
                    messages=messages,
                )
                break
            except Exception as e:
                if "tool_use_failed" in str(e) and attempt < 2:
                    print(f"  [RETRY] Malformed tool call, retrying... ({attempt + 1}/3)")
                    continue
                raise

        message = response.choices[0].message
        messages.append(message)

        finish_reason = response.choices[0].finish_reason

        if finish_reason == "stop":
            print("\nAgent finished.")
            break

        if finish_reason == "tool_calls" and message.tool_calls:
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                inputs = json.loads(tool_call.function.arguments)

                print(f"  -> {name}({json.dumps(inputs, ensure_ascii=False)[:120]})")

                try:
                    result = execute_tool(name, inputs)
                    result_content = json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result

                    if name == "write_report":
                        print(f"\nReport saved to: {result}")

                except Exception as exc:
                    result_content = f"Error: {exc}"
                    print(f"  [ERROR] {name}: {exc}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_content,
                })
        else:
            print(f"Unexpected finish_reason: {finish_reason}")
            break
    else:
        print("Reached maximum iterations without completing.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python research_agent.py \"<topic>\"")
        sys.exit(1)
    topic = " ".join(sys.argv[1:])
    run_research_agent(topic)
