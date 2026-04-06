# Warm Memory: Patterns
<!-- L1: recurring code patterns, idioms, and anti-patterns in this codebase -->

**Last Updated**: 2026-04-05

---

## Routing Pattern

All 5 routers follow the same interface: `route_*(task: str) -> Result`.
Composed by `route()` in `src/routing/__init__.py` → `RoutingDecision` dataclass.

```python
from src.routing import route
d = route("security audit of src/api/")
print(d.model)      # "opus"
print(d.skill)      # SkillMatch(skill="ciso", confidence=0.9, ...)
print(d.summary())  # formatted box
```

## Skill Registry Pattern

```python
{"skill": "name", "category": "category", "priority": 7,
 "triggers": ["exact phrase 1", "exact phrase 2"]}
```
- Triggers: lowercase exact-substring match against lowercased input
- Priority: 0–10 (higher wins when multiple skills match)
- **No duplicates**: enforced by `test_no_duplicate_trigger_phrases`

## Tiered Memory Pattern

```python
from src.persistence import TieredMemory
mem = TieredMemory()                                # uses .claude/memory/ by default
mem.write_hot("key", "value")                      # hot: auto-evict at 50 lines
mem.write_warm("domain", "# Header\ncontent")      # warm: full domain file
path = mem.archive_glacier("slug", "body",         # glacier: YAML frontmatter
                           tags=["arch"])
results = mem.search_glacier("keyword")            # full-text + tag search
```

## Logger Pattern

```python
from src.utils.logger import get_logger
log = get_logger("component")
log.info("event", key="value", count=42)   # structured JSON output
log.error("failed", error=str(e))          # exc_info NOT passed as kwarg — set on record
```
**Anti-pattern**: `log.error("msg", exc_info=True)` — use `log.error("msg")` inside except block instead; the formatter reads `sys.exc_info()` automatically.

## EvalCase/EvalSuite Pattern

```python
from src.evals import EvalCase, EvalSuite, EvalRunner

suite = (EvalSuite("name")
    .add(EvalCase("id", "prompt", contains=["expected"], tags=["fast"]))
)
report = EvalRunner(llm_fn).run(suite)
print(report.summary())
```
**Anti-pattern**: `EvalResult("id", Verdict.PASS, [], 1.0, 0, ["tag"])` — use keyword args to avoid positional mapping errors.

## Middleware Order (outermost → innermost)

```
CorrelationIDMiddleware  →  attach request ID first
TimingMiddleware         →  time the full handler
Application routes
```
**Rule**: `ContextVar.reset(token)` MUST be in a `finally` block to avoid leaking context across requests.

## Test Structure Pattern

```python
class TestFeatureName:
    def test_happy_path(self, tmp_path: Path) -> None:
        ...
    def test_failure_case(self, tmp_path: Path) -> None:
        ...
```
- One assertion focus per test
- Use `tmp_path` fixture for filesystem tests
- No `@pytest.mark.asyncio` needed (asyncio_mode = auto)
- Mock at the boundary: `unittest.mock.patch`, `AsyncMock`

## Hook Exit Codes

- `exit 0` → allow the operation to proceed
- `exit 2` → block the operation (print reason to stderr first)
- All hooks use `|| true` in settings.json to prevent hook crashes from breaking Claude
