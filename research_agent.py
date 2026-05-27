import sys
from dotenv import load_dotenv
from groq import BadRequestError
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()
from tools import web_search, read_page, write_report

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


def run_research_agent(topic: str):
    llm = ChatGroq(model="llama-3.3-70b-versatile", max_tokens=4096)

    agent = create_react_agent(
        llm,
        tools=[web_search, read_page, write_report],
        prompt=SystemMessage(content=SYSTEM_PROMPT),
    )

    print(f"\nResearching: {topic}\n{'=' * 60}")

    inputs = {"messages": [HumanMessage(content=f"Research this topic and write a report: {topic}")]}
    config = {"recursion_limit": 40}

    for attempt in range(3):
        try:
            for chunk in agent.stream(inputs, config=config, stream_mode="updates"):
                if "agent" in chunk:
                    for msg in chunk["agent"]["messages"]:
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                print(f"  -> {tc['name']}({str(tc['args'])[:120]})")
                elif "tools" in chunk:
                    for msg in chunk["tools"]["messages"]:
                        content = str(msg.content)
                        if content.startswith("reports"):
                            print(f"\nReport saved to: {content}")
            break
        except BadRequestError as e:
            if "tool_use_failed" in str(e) and attempt < 2:
                print(f"  [RETRY] Malformed tool call, retrying... ({attempt + 1}/3)")
                continue
            raise

    print("\nAgent finished.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python research_agent.py "<topic>"')
        sys.exit(1)
    topic = " ".join(sys.argv[1:])
    run_research_agent(topic)
