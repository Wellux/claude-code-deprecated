"""Jinja2-style prompt template engine (no external deps)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PromptTemplate:
    """Simple {{variable}} template with validation.

    Example:
        t = PromptTemplate("Summarize {{text}} in {{language}}.")
        t.render(text="...", language="English")
    """

    template: str
    required_vars: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        found = re.findall(r"\{\{(\w+)\}\}", self.template)
        if not self.required_vars:
            self.required_vars = list(dict.fromkeys(found))  # dedupe, preserve order

    def render(self, **kwargs: Any) -> str:
        """Render template with provided variables.

        Raises ValueError if any required_vars are missing.
        """
        missing = [v for v in self.required_vars if v not in kwargs]
        if missing:
            raise ValueError(f"Missing template variables: {missing}")

        result = self.template
        for key, value in kwargs.items():
            result = result.replace("{{" + key + "}}", str(value))
        return result

    def variables(self) -> list[str]:
        return list(self.required_vars)


class TemplateLibrary:
    """Registry of named prompt templates."""

    def __init__(self) -> None:
        self._templates: dict[str, PromptTemplate] = {}

    def register(self, name: str, template: str, required_vars: list[str] | None = None) -> None:
        self._templates[name] = PromptTemplate(
            template=template,
            required_vars=required_vars or [],
        )

    def get(self, name: str) -> PromptTemplate:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not registered. Available: {list(self._templates)}")
        return self._templates[name]

    def render(self, template_name: str, **kwargs: Any) -> str:
        return self.get(template_name).render(**kwargs)

    def list_templates(self) -> list[str]:
        return list(self._templates)


# Default library pre-loaded with common templates
default_library = TemplateLibrary()
default_library.register(
    "code_review",
    "You are a senior engineer. Review this {{language}} code for bugs, style, and security.\n\n```{{language}}\n{{code}}\n```\n\nProvide: issues found, severity (critical/major/minor), and fixes.",
)
default_library.register(
    "summarize",
    "Summarize the following text in {{max_words}} words or fewer, focusing on key insights:\n\n{{text}}",
)
default_library.register(
    "research_query",
    "Research: {{topic}}\n\nProvide:\n1. Core concept (2-3 sentences)\n2. Latest developments (2026)\n3. Key implementation pattern\n4. Actionable insight for a practitioner\n\nBe direct and technical.",
)
default_library.register(
    "bug_fix",
    "Debug this {{language}} error:\n\nError: {{error}}\n\nCode:\n```{{language}}\n{{code}}\n```\n\nProvide root cause and minimal fix.",
)
