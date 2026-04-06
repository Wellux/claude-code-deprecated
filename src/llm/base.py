"""Abstract base class for LLM clients."""
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class CompletionRequest:
    prompt: str
    system: str | None = None
    model: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7
    stream: bool = False


@dataclass
class CompletionResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    stop_reason: str

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def cost_usd(self) -> float:
        """Rough cost estimate — update rates from config."""
        rates = {
            "claude-sonnet-4-6": (3.0, 15.0),
            "claude-opus-4-6": (15.0, 75.0),
            "claude-haiku-4-5-20251001": (0.25, 1.25),
        }
        input_rate, output_rate = rates.get(self.model, (3.0, 15.0))
        return (self.input_tokens * input_rate + self.output_tokens * output_rate) / 1_000_000


class LLMClient(ABC):
    """Abstract LLM client interface. All providers implement this."""

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Generate a completion for the given request."""
        ...  # pragma: no cover — abstract stub

    @abstractmethod
    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...  # pragma: no cover — abstract stub

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text without making an API call."""
        ...  # pragma: no cover — abstract stub
