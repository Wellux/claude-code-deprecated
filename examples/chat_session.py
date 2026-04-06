#!/usr/bin/env python3
"""Multi-turn chat session with streaming output."""
import asyncio
import os
import sys

from src.llm import ClaudeClient, build_request


SYSTEM_PROMPT = """You are a helpful AI assistant that is concise, direct, and technically accurate.
When asked about code, always include working examples. Keep answers under 300 words unless depth is needed."""


async def chat_session() -> None:
    client = ClaudeClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    history: list[str] = []

    print("Claude Code Max — Chat Session")
    print("Type 'quit' or Ctrl+C to exit, 'clear' to reset history.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            history.clear()
            print("[History cleared]\n")
            continue

        # Build context-aware prompt from history
        context = "\n\n".join(history[-6:])  # last 3 turns
        prompt = f"{context}\n\nUser: {user_input}\nAssistant:" if context else user_input

        request = build_request(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            max_tokens=1024,
            temperature=0.7,
        )

        print("Assistant: ", end="", flush=True)
        full_response = []

        async for token in client.stream(request):
            print(token, end="", flush=True)
            full_response.append(token)

        assistant_reply = "".join(full_response)
        print("\n")

        # Append to history (simplified — no full message objects)
        history.append(f"User: {user_input}\nAssistant: {assistant_reply}")


if __name__ == "__main__":
    asyncio.run(chat_session())
