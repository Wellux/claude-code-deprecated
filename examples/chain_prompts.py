#!/usr/bin/env python3
"""Prompt chaining example — multi-step research + synthesis pipeline."""
import asyncio
import os

from src.llm import ClaudeClient
from src.prompt_engineering import PromptChain


async def research_pipeline(topic: str) -> None:
    """3-step Karpathy-style research chain: search → distill → action."""
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    chain = (
        PromptChain(client)
        .add_step(
            "overview",
            lambda ctx: (
                f"Give a concise technical overview of: {ctx['topic']}\n\n"
                "Cover: what it is, why it matters, core mechanism. Max 200 words."
            ),
            temperature=0.3,
            max_tokens=512,
        )
        .add_step(
            "deep_dive",
            lambda ctx: (
                f"Topic: {ctx['topic']}\n\nOverview:\n{ctx['overview']}\n\n"
                "Now: identify the single most important technical insight.\n"
                "Explain it from first principles. What would you need to rebuild this from scratch? 150 words."
            ),
            temperature=0.2,
            max_tokens=512,
        )
        .add_step(
            "action_items",
            lambda ctx: (
                f"Topic: {ctx['topic']}\n\nKey insight:\n{ctx['deep_dive']}\n\n"
                "Generate 3 concrete action items for a practitioner to apply this insight this week.\n"
                "Format: numbered list, each item under 30 words, immediately actionable."
            ),
            temperature=0.5,
            max_tokens=256,
        )
    )

    print(f"\n=== Research Pipeline: {topic} ===\n")
    result = await chain.run({"topic": topic})

    print("📋 OVERVIEW")
    print(result.steps["overview"])

    print("\n🔬 DEEP DIVE")
    print(result.steps["deep_dive"])

    print("\n✅ ACTION ITEMS")
    print(result.steps["action_items"])

    print(f"\n📊 TOTAL — tokens: {result.total_tokens} | cost: ${result.total_cost_usd:.4f}")


async def parallel_research(topics: list[str]) -> None:
    """Research multiple topics in parallel."""
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    branches = {}
    for topic in topics:
        branch = PromptChain(client).add_step(
            "summary",
            lambda ctx, t=topic: f"Summarize '{t}' in 3 bullet points. Be technical and specific.",
            max_tokens=256,
            temperature=0.3,
        )
        branches[topic] = branch

    print(f"\n=== Parallel Research: {len(topics)} topics ===\n")
    results = await PromptChain(client).run_parallel_branches(branches, {})

    for topic, result in results.items():
        print(f"### {topic}")
        print(result.final)
        print()


if __name__ == "__main__":
    # Single deep-dive chain
    asyncio.run(research_pipeline("RAG with graph retrieval (LightRAG)"))

    # Parallel research
    asyncio.run(parallel_research([
        "LLM agent frameworks 2026",
        "Prompt caching techniques",
        "Fine-tuning efficiency (LoRA, QLoRA)",
    ]))
