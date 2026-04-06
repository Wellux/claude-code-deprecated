#!/usr/bin/env python3
"""Basic completion example — single prompt → response."""
import asyncio
import os

from src.llm import ClaudeClient, build_request


async def main() -> None:
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    request = build_request(
        prompt="Explain the key insight behind attention mechanisms in transformers in 3 sentences.",
        system="You are a concise AI research assistant.",
        max_tokens=512,
        temperature=0.3,
    )

    print("Sending request...")
    response = await client.complete(request)

    print(f"\n--- Response ---")
    print(response.content)
    print(f"\n--- Stats ---")
    print(f"Model:         {response.model}")
    print(f"Input tokens:  {response.input_tokens}")
    print(f"Output tokens: {response.output_tokens}")
    print(f"Cost:          ${response.cost_usd:.6f}")
    print(f"Stop reason:   {response.stop_reason}")


if __name__ == "__main__":
    asyncio.run(main())
