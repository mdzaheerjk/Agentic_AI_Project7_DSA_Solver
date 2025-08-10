'''
litrev_backend.py
=================
Core logic for the multi‑agent literature‑review assistant built with the
**AutoGen** AgentChat stack (⩾ v0.4).  It exposes a single public coroutine
`run_litrev()` that drives a two‑agent team:

* **search_agent** – crafts an arXiv query and fetches papers via the provided
  `arxiv_search` tool.
* **summarizer** – writes a short Markdown literature review from the selected
  papers.

The module is deliberately self‑contained so it can be reused in CLI apps,
Streamlit, FastAPI, Gradio, etc.
'''

from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Dict, List

import arxiv  # type: ignore
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import (
    TextMessage,
    ToolCallExecutionEvent,
    ToolCallRequestEvent,
)
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# ---------------------------------------------------------------------------
# 1. Tool definition ---------------------------------------------------------
# ---------------------------------------------------------------------------

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """Return a compact list of arXiv papers matching *query*.

    Each element contains: ``title``, ``authors``, ``published``, ``summary`` and
    ``pdf_url``.  The helper is wrapped as an AutoGen *FunctionTool* below so it
    can be invoked by agents through the normal tool‑use mechanism.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers: List[Dict] = []
    for result in client.results(search):
        papers.append(
            {
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "published": result.published.strftime("%Y-%m-%d"),
                "summary": result.summary,
                "pdf_url": result.pdf_url,
            }
        )
    return papers


arxiv_tool = FunctionTool(
    arxiv_search,
    description=(
        "Searches arXiv and returns up to *max_results* papers, each containing "
        "title, authors, publication date, abstract, and pdf_url."
    ),
)

# ---------------------------------------------------------------------------
# 2. Agent & team factory -----------------------------------------------------
# ---------------------------------------------------------------------------

def build_team(model: str = "gpt-4o-mini") -> RoundRobinGroupChat:
    """Create and return a two‑agent *RoundRobinGroupChat* team."""
    llm_client = OpenAIChatCompletionClient(model=model,api_key='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')

    # Agent that **only** calls the arXiv tool and forwards top‑N papers
    search_agent = AssistantAgent(
        name="search_agent",
        description="Crafts arXiv queries and retrieves candidate papers.",
        system_message=(
            "Given a user topic, think of the best arXiv query and call the "
            "provided tool. Always fetch five‑times the papers requested so "
            "that you can down‑select the most relevant ones. When the tool "
            "returns, choose exactly the number of papers requested and pass "
            "them as concise JSON to the summarizer."
        ),
        tools=[arxiv_tool],
        model_client=llm_client,
        reflect_on_tool_use=True,
    )

    # Agent that writes the final literature review
    summarizer = AssistantAgent(
        name="summarizer",
        description="Produces a short Markdown review from provided papers.",
        system_message=(
            "You are an expert researcher. When you receive the JSON list of "
            "papers, write a literature‑review style report in Markdown:\n" \
            "1. Start with a 2–3 sentence introduction of the topic.\n" \
            "2. Then include one bullet per paper with: title (as Markdown "
            "link), authors, the specific problem tackled, and its key "
            "contribution.\n" \
            "3. Close with a single‑sentence takeaway."
        ),
        model_client=llm_client,
    )

    return RoundRobinGroupChat(
        participants=[search_agent, summarizer],
        max_turns=2,
    )


# ---------------------------------------------------------------------------
# 3. Orchestrator -------------------------------------------------------------
# ---------------------------------------------------------------------------

async def run_litrev(
    topic: str,
    num_papers: int = 5,
    model: str = "gpt-4o-mini",
) -> AsyncGenerator[str, None]:
    """Yield strings representing the conversation in real‑time."""

    team = build_team(model=model)
    task_prompt = (
        f"Conduct a literature review on **{topic}** and return exactly {num_papers} papers."
    )

    async for msg in team.run_stream(task=task_prompt):
        if isinstance(msg, TextMessage):
            yield f"{msg.source}: {msg.content}"

# ---------------------------------------------------------------------------
# 4. CLI testing -------------------------------------------------------------
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    async def _demo() -> None:
        async for line in run_litrev("graph neural networks for chemistry", num_papers=5):
            print(line)

    asyncio.run(_demo())
