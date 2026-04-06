"""Tests for src/prompt_engineering/few_shot.py."""
from src.prompt_engineering.few_shot import FewShotManager


class TestFewShotManager:
    def test_empty_manager_builds_prompt_with_just_query(self):
        mgr = FewShotManager()
        result = mgr.build_prompt("my query")
        assert "my query" in result
        assert "Input:" in result
        assert "Output:" in result

    def test_adds_examples_to_prompt(self):
        mgr = FewShotManager()
        mgr.add("cat", "animal")
        mgr.add("oak", "tree")
        result = mgr.build_prompt("rose")
        assert "cat" in result
        assert "animal" in result
        assert "oak" in result
        assert "tree" in result
        assert "rose" in result

    def test_prefix_included_in_prompt(self):
        mgr = FewShotManager(prefix="Classify the following:")
        result = mgr.build_prompt("query")
        assert "Classify the following:" in result

    def test_max_examples_limits_output(self):
        mgr = FewShotManager()
        for i in range(10):
            mgr.add(f"input{i}", f"output{i}")
        result = mgr.build_prompt("query", max_examples=2)
        # Only last 2 examples should appear
        assert "input8" in result
        assert "input9" in result
        assert "input0" not in result

    def test_len_returns_example_count(self):
        mgr = FewShotManager()
        assert len(mgr) == 0
        mgr.add("a", "b")
        mgr.add("c", "d")
        assert len(mgr) == 2

    def test_get_by_label(self):
        mgr = FewShotManager()
        mgr.add("great product", "positive", label="sentiment")
        mgr.add("terrible service", "negative", label="sentiment")
        mgr.add("select * from users", "sql", label="code")
        sentiment = mgr.get_by_label("sentiment")
        assert len(sentiment) == 2
        assert all(e.label == "sentiment" for e in sentiment)

    def test_to_messages_format(self):
        mgr = FewShotManager()
        mgr.add("hello", "world")
        messages = mgr.to_messages("test")
        assert messages[0] == {"role": "user", "content": "hello"}
        assert messages[1] == {"role": "assistant", "content": "world"}
        assert messages[-1] == {"role": "user", "content": "test"}

    def test_to_messages_no_examples(self):
        mgr = FewShotManager()
        messages = mgr.to_messages("query")
        assert messages == [{"role": "user", "content": "query"}]

    def test_custom_labels(self):
        mgr = FewShotManager(input_label="Q", output_label="A")
        mgr.add("question", "answer")
        result = mgr.build_prompt("new question")
        assert "Q: question" in result
        assert "A: answer" in result
