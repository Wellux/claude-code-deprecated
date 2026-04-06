"""Few-shot example manager for prompt construction."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Example:
    """A single input→output demonstration."""
    input: str
    output: str
    label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class FewShotManager:
    """Manage and retrieve few-shot examples for prompt construction.

    Usage:
        mgr = FewShotManager(prefix="Classify sentiment:")
        mgr.add("Great product!", "positive")
        mgr.add("Terrible experience.", "negative")
        prompt = mgr.build_prompt("Works as expected.")
    """

    def __init__(
        self,
        prefix: str = "",
        input_label: str = "Input",
        output_label: str = "Output",
        separator: str = "\n\n",
    ):
        self.prefix = prefix
        self.input_label = input_label
        self.output_label = output_label
        self.separator = separator
        self._examples: list[Example] = []

    def add(self, input_text: str, output_text: str, label: str = "", **metadata: Any) -> None:
        self._examples.append(
            Example(input=input_text, output=output_text, label=label, metadata=metadata)
        )

    def get_by_label(self, label: str) -> list[Example]:
        return [e for e in self._examples if e.label == label]

    def build_prompt(self, query: str, max_examples: int | None = None) -> str:
        """Build a few-shot prompt with all (or up to max_examples) examples."""
        examples = self._examples if max_examples is None else self._examples[-max_examples:]
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        for ex in examples:
            parts.append(f"{self.input_label}: {ex.input}\n{self.output_label}: {ex.output}")
        parts.append(f"{self.input_label}: {query}\n{self.output_label}:")
        return self.separator.join(parts)

    def to_messages(self, query: str, max_examples: int | None = None) -> list[dict]:
        """Return chat-format messages list for API calls."""
        examples = self._examples if max_examples is None else self._examples[-max_examples:]
        messages = []
        for ex in examples:
            messages.append({"role": "user", "content": ex.input})
            messages.append({"role": "assistant", "content": ex.output})
        messages.append({"role": "user", "content": query})
        return messages

    def __len__(self) -> int:
        return len(self._examples)
