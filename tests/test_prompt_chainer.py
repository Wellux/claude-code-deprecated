"""Tests for src/prompt_engineering/chainer.py — PromptChain with mock LLM."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.llm.base import CompletionResponse
from src.prompt_engineering.chainer import PromptChain


def make_mock_client(responses: list[str]):
    """Return a mock LLMClient that returns responses in sequence."""
    client = MagicMock()
    resps = [
        CompletionResponse(
            content=r, model="claude-sonnet-4-6",
            input_tokens=10, output_tokens=len(r.split()),
            stop_reason="end_turn",
        )
        for r in responses
    ]
    client.complete = AsyncMock(side_effect=resps)
    return client


@pytest.mark.asyncio
async def test_single_step_chain():
    client = make_mock_client(["step1 output"])
    chain = PromptChain(client).add_step(
        "step1",
        lambda ctx: "prompt",
    )
    result = await chain.run()
    assert result.steps["step1"] == "step1 output"
    assert result.final == "step1 output"


@pytest.mark.asyncio
async def test_two_step_chain_passes_context():
    client = make_mock_client(["outline text", "draft text"])
    chain = (
        PromptChain(client)
        .add_step("outline", lambda ctx: "write outline")
        .add_step("draft", lambda ctx: f"expand: {ctx['outline']}")
    )
    result = await chain.run()
    assert result.steps["outline"] == "outline text"
    assert result.steps["draft"] == "draft text"
    # Verify the second step received the first step's output in its prompt
    second_call_prompt = client.complete.call_args_list[1][0][0].prompt
    assert "outline text" in second_call_prompt


@pytest.mark.asyncio
async def test_initial_context_passed_to_first_step():
    client = make_mock_client(["result"])
    chain = PromptChain(client).add_step(
        "step1",
        lambda ctx: f"topic: {ctx['topic']}",
    )
    await chain.run({"topic": "RAG systems"})
    prompt_used = client.complete.call_args_list[0][0][0].prompt
    assert "RAG systems" in prompt_used


@pytest.mark.asyncio
async def test_transform_applied_to_output():
    client = make_mock_client(["  whitespace  "])
    chain = PromptChain(client).add_step(
        "clean",
        lambda ctx: "prompt",
        transform=str.strip,
    )
    result = await chain.run()
    assert result.steps["clean"] == "whitespace"


@pytest.mark.asyncio
async def test_total_cost_aggregates_steps():
    client = make_mock_client(["a", "b", "c"])
    chain = (
        PromptChain(client)
        .add_step("s1", lambda ctx: "p1")
        .add_step("s2", lambda ctx: "p2")
        .add_step("s3", lambda ctx: "p3")
    )
    result = await chain.run()
    assert result.total_cost_usd >= 0.0
    assert result.total_tokens > 0
    assert len(result.responses) == 3


@pytest.mark.asyncio
async def test_fluent_api_returns_chain():
    client = make_mock_client(["x"])
    chain = PromptChain(client)
    returned = chain.add_step("s", lambda ctx: "p")
    assert returned is chain


@pytest.mark.asyncio
async def test_empty_chain_returns_empty_result():
    client = make_mock_client([])
    result = await PromptChain(client).run()
    assert result.final is None
    assert result.total_cost_usd == 0.0


@pytest.mark.asyncio
async def test_run_parallel_branches_returns_all_results():
    """Cover PromptChain.run_parallel_branches() (lines 127-134)."""
    client_a = make_mock_client(["branch A result"])
    client_b = make_mock_client(["branch B result"])

    chain_a = PromptChain(client_a).add_step("step", lambda ctx: "prompt A")
    chain_b = PromptChain(client_b).add_step("step", lambda ctx: "prompt B")

    orchestrator = PromptChain(make_mock_client([]))
    results = await orchestrator.run_parallel_branches(
        {"branch_a": chain_a, "branch_b": chain_b}
    )

    assert set(results.keys()) == {"branch_a", "branch_b"}
    assert results["branch_a"].final == "branch A result"
    assert results["branch_b"].final == "branch B result"


@pytest.mark.asyncio
async def test_run_parallel_branches_empty():
    orchestrator = PromptChain(make_mock_client([]))
    results = await orchestrator.run_parallel_branches({})
    assert results == {}
