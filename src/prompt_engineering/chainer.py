"""Prompt chaining — pipe the output of one LLM call into the next."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..llm.base import CompletionRequest, CompletionResponse, LLMClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ChainStep:
    """One step in a prompt chain."""
    name: str
    prompt_fn: Callable[[dict[str, Any]], str]
    """Receives context dict (previous outputs keyed by step name), returns prompt string."""
    system: str | None = None
    model: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7
    transform: Callable[[str], Any] = field(default=lambda x: x)
    """Post-process the raw LLM output before storing in context."""


@dataclass
class ChainResult:
    """Result of running a full chain."""
    steps: dict[str, Any] = field(default_factory=dict)
    """Keyed by step name → transformed output."""
    responses: dict[str, CompletionResponse] = field(default_factory=dict)
    """Raw CompletionResponse per step for token/cost tracking."""

    @property
    def final(self) -> Any:
        """Return the last step's output."""
        if not self.steps:
            return None
        return list(self.steps.values())[-1]

    @property
    def total_cost_usd(self) -> float:
        return sum(r.cost_usd for r in self.responses.values())

    @property
    def total_tokens(self) -> int:
        return sum(r.input_tokens + r.output_tokens for r in self.responses.values())


class PromptChain:
    """Execute a sequence of LLM calls where each step can use prior outputs.

    Example:
        chain = PromptChain(client)
        chain.add_step("outline", lambda ctx: f"Outline an essay on: {ctx['topic']}")
        chain.add_step("draft", lambda ctx: f"Expand this outline:\\n{ctx['outline']}")
        result = await chain.run({"topic": "RAG systems"})
        print(result.final)
    """

    def __init__(self, client: LLMClient):
        self.client = client
        self._steps: list[ChainStep] = []

    def add_step(
        self,
        name: str,
        prompt_fn: Callable[[dict[str, Any]], str],
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        transform: Callable[[str], Any] = lambda x: x,
    ) -> PromptChain:
        self._steps.append(
            ChainStep(
                name=name,
                prompt_fn=prompt_fn,
                system=system,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                transform=transform,
            )
        )
        return self  # fluent API

    async def run(self, initial_context: dict[str, Any] | None = None) -> ChainResult:
        """Execute all steps sequentially, accumulating context."""
        context: dict[str, Any] = dict(initial_context or {})
        result = ChainResult()

        for step in self._steps:
            prompt = step.prompt_fn(context)
            request = CompletionRequest(
                prompt=prompt,
                system=step.system,
                model=step.model,
                max_tokens=step.max_tokens,
                temperature=step.temperature,
            )
            logger.info("chain_step_start", step=step.name, prompt_len=len(prompt))
            response = await self.client.complete(request)
            transformed = step.transform(response.content)
            context[step.name] = transformed
            result.steps[step.name] = transformed
            result.responses[step.name] = response
            logger.info(
                "chain_step_done",
                step=step.name,
                tokens=response.input_tokens + response.output_tokens,
                cost_usd=response.cost_usd,
            )

        return result

    async def run_parallel_branches(
        self,
        branches: dict[str, PromptChain],
        initial_context: dict[str, Any] | None = None,
    ) -> dict[str, ChainResult]:
        """Run multiple independent chains in parallel and return their results."""
        tasks = {
            name: asyncio.create_task(chain.run(initial_context))
            for name, chain in branches.items()
        }
        results = {}
        for name, task in tasks.items():
            results[name] = await task
        return results
