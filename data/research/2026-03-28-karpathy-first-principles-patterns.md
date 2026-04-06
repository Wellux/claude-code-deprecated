# Research: Karpathy First-Principles Patterns — 2026-03-28

## Core Insight

Andrej Karpathy's philosophy, distilled from nanoGPT, micrograd, llm.c, minGPT, and
build-nanogpt: **understand well enough to rebuild from scratch**. Every abstraction should
be removable — if you cannot implement it in 100 lines, you do not understand it. Start
minimal, make it fast, make it correct, then scale.

The pattern across all his repos is identical:
1. Strip away every dependency until the concept is naked
2. Implement the concept in one file (single-file rule)
3. Train on real data immediately — no toy examples that don't transfer
4. Profile before optimizing — the bottleneck is never where you expect
5. Read the loss curve — it tells you everything about what the model is learning

---

## Key Techniques (by repo)

### micrograd — autograd from 45 lines
- The entire foundation of deep learning fits in one `Value` class with `__add__`, `__mul__`,
  and a `backward()` that walks a topological sort of the compute graph
- **Pattern for this project**: any complex stateful system can be reduced to: node, edges,
  and a traversal order. LogIndex's rebuild_index is this pattern — topological scan of
  `_lines` → rebuild two dicts. The eviction is just truncating the graph.

### nanoGPT — GPT-2 in ~300 lines, competitive performance
- Achieved 85% of GPT-2's performance with 10% of its codebase by cutting:
  - All the abstractions around attention (just write the math directly)
  - All the config inheritance (one dataclass per model)
  - All the "future-proof" hooks (YAGNI — You Aren't Gonna Need It)
- **Pattern for this project**: the routing system's 5 routers are each ~30 lines because they
  follow this principle. No base class for routers. No plugin system. Direct functions.

### llm.c — GPT-2 training in pure C, no ML frameworks
- Key insight: frameworks add latency and obscure the compute. When you write the CUDA kernel
  yourself, you find the actual bottleneck (usually memory bandwidth, not compute).
- The `flash_attention` kernel was 5× faster than PyTorch's naive implementation for the same math.
- **Pattern for this project**: The `AsyncEvalRunner` semaphore pattern is the same idea —
  don't let the framework (asyncio.gather blindly) make scheduling decisions. Control
  concurrency yourself at the resource boundary.

### build-nanogpt / makemore — step-by-step construction
- Every video builds the same model from nothing, adding one piece at a time, running the
  training loop at each step to verify the loss decreases as expected.
- **The checkpoint pattern**: commit after every working state. Never refactor a passing system
  before the next test is green.
- **Pattern for this project**: `ccm eval run --dry-run` is the equivalent of checking the
  loss curve at each step. The smoke eval suite is the "does the gradient flow?" sanity check.

---

## Minimal Implementation (EvalRunner as nanoGPT)

The sync EvalRunner is already Karpathy-style — no abstractions, just a loop:

```python
# This IS the nanoGPT philosophy applied to evals:
def run(self, suite):
    return _aggregate(suite.name, [self._run_case(c) for c in suite])

def _run_case(self, case):
    t0 = time.monotonic()
    try:
        actual = self.llm(case.prompt, max_tokens=case.max_tokens, temperature=case.temperature)
    except Exception as exc:
        return EvalResult(case_id=case.id, verdict=Verdict.ERROR, ..., error=str(exc))
    score, reason = self.scorer(actual, case)
    return EvalResult(case_id=case.id, verdict=..., score=score, latency_ms=...)
```

One function, one responsibility, all state explicit. This is the micrograd Value class.

---

## Applied Karpathy Optimizations (already in this codebase)

| Karpathy pattern | Where applied | Impact |
|-----------------|---------------|--------|
| Single-file truth | `src/version.py` | Version sync across CLI, API, health |
| No-framework logging | `src/utils/log_index.py` | O(1) append, O(k) search, bounded memory |
| Explicit semaphore | `AsyncEvalRunner` | Predictable concurrency vs gather() chaos |
| Circuit layout | `src/llm/claude_client.py` | `_FATAL` vs `_RETRYABLE` — no retry on auth errors |
| Loss-curve evals | `data/evals/smoke.jsonl` | Every deploy verifies the "gradient flows" |

---

## Remaining Optimizations from Karpathy Lens

### 1. The "reading the loss curve" pattern — structured tracing
Karpathy logs everything during training: loss per step, gradient norm, learning rate.
We log api_request events to LogIndex but don't have a `ccm bench` subcommand to read them.
**Suggested**: `ccm logs --summary` is the equivalent of `print(f"step {i}: loss {loss:.4f}")`.
Already done in v0.6.1 — this is complete.

### 2. The "single training loop" pattern — one evaluation path
In nanoGPT there is exactly one path from data → model → loss. No special cases.
Our eval path has two runners (sync + async) and four scorers. The scorers are composable
but the runners are not. A `DryRunLLM` that returns `case.expected` should work with both
runners identically — and it does. This is correct architecture.

### 3. The "no premature optimization" rule — measure first
llm.c only added CUDA after profiling showed the bottleneck was GPU compute.
For this project: profile with `ccm logs --event api_request --summary` before optimizing
latency. The `latency_ms` field is already logged to LogIndex for every request.

### 4. Flash attention analogue — the `asyncio.wait_for` addition
The `wait_for` timeout added to `AsyncEvalRunner._run_case` is the equivalent of
flash attention: same mathematical result (eval case runs), but bounded resource usage.
Without it, a hung LLM call blocks a semaphore slot forever.

---

## Actionable Takeaways

1. **The single-file rule**: every module should be explainable in one read-through.
   If `src/routing/llm_router.py` takes more than 60 seconds to understand, it's too complex.
   Current state: each router is ~30-40 lines. Good.

2. **Verify the gradient flows at every step**: `ccm eval run data/evals/smoke.jsonl --dry-run`
   must pass before every commit. This is the Karpathy "does the loss decrease?" check.
   This is in CI. Good.

3. **The eviction pattern is correct**: LogIndex's FIFO eviction (drop oldest 25%, O(n) rebuild)
   is amortized O(1) — exactly how gradient checkpointing works in llm.c. You pay a one-time
   full-scan cost to free memory, then O(1) appends resume. The math is identical.

---

## Sources
- github.com/karpathy/nanoGPT — ~300 line GPT-2, competitive training
- github.com/karpathy/micrograd — 45-line autograd engine
- github.com/karpathy/llm.c — GPT-2 training in pure C/CUDA
- github.com/karpathy/minGPT — educational GPT-2 implementation
- github.com/karpathy/build-nanogpt — step-by-step nanoGPT video series
- karpathy.ai blog — "The Unreasonable Effectiveness of Recurrent Neural Networks" (first-principles method)
