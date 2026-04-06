"""Tests for src/prompt_engineering/templates.py."""
import pytest

from src.prompt_engineering.templates import PromptTemplate, TemplateLibrary, default_library


class TestPromptTemplate:
    def test_render_single_variable(self):
        t = PromptTemplate("Hello {{name}}!")
        assert t.render(name="world") == "Hello world!"

    def test_render_multiple_variables(self):
        t = PromptTemplate("{{greeting}} {{name}}, you are {{age}} years old.")
        result = t.render(greeting="Hi", name="Alice", age=30)
        assert result == "Hi Alice, you are 30 years old."

    def test_auto_detects_required_vars(self):
        t = PromptTemplate("{{a}} and {{b}}")
        assert set(t.variables()) == {"a", "b"}

    def test_missing_variable_raises(self):
        t = PromptTemplate("Hello {{name}}!")
        with pytest.raises(ValueError, match="Missing template variables"):
            t.render()

    def test_extra_kwargs_ignored(self):
        t = PromptTemplate("Hello {{name}}!")
        result = t.render(name="Bob", unused="ignored")
        assert result == "Hello Bob!"

    def test_no_variables_renders_as_is(self):
        t = PromptTemplate("No variables here.")
        assert t.render() == "No variables here."

    def test_integer_value_coerced_to_string(self):
        t = PromptTemplate("Count: {{n}}")
        assert t.render(n=42) == "Count: 42"

    def test_explicit_required_vars(self):
        t = PromptTemplate("{{a}} {{b}}", required_vars=["a"])
        with pytest.raises(ValueError):
            t.render()  # missing "a"


class TestTemplateLibrary:
    def test_register_and_render(self):
        lib = TemplateLibrary()
        lib.register("greet", "Hello {{name}}!")
        assert lib.render("greet", **{"name": "Alice"}) == "Hello Alice!"

    def test_get_unknown_raises(self):
        lib = TemplateLibrary()
        with pytest.raises(KeyError, match="not registered"):
            lib.get("nonexistent")

    def test_list_templates(self):
        lib = TemplateLibrary()
        lib.register("t1", "{{x}}")
        lib.register("t2", "{{y}}")
        assert set(lib.list_templates()) == {"t1", "t2"}


class TestDefaultLibrary:
    def test_code_review_template_exists(self):
        result = default_library.render("code_review", language="Python", code="x = 1")
        assert "Python" in result
        assert "x = 1" in result

    def test_summarize_template_exists(self):
        result = default_library.render("summarize", max_words=50, text="some text")
        assert "50" in result
        assert "some text" in result

    def test_research_query_template_exists(self):
        result = default_library.render("research_query", topic="RAG systems")
        assert "RAG systems" in result

    def test_bug_fix_template_exists(self):
        result = default_library.render(
            "bug_fix", language="Python", error="TypeError", code="x = None + 1"
        )
        assert "TypeError" in result
