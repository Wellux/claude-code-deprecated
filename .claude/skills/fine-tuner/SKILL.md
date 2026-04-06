---
name: fine-tuner
description: >
  Design fine-tuning pipelines for LLMs on custom data. Invoke for: "fine-tune",
  "train on my data", "custom model", "domain adaptation", "LoRA", "PEFT",
  "instruction tuning", "fine-tuning dataset", "adapt model to my domain".
argument-hint: model to fine-tune and task/domain
allowed-tools: Read, Write, WebSearch
---

# Skill: Fine Tuner — LLM Domain Adaptation
**Category:** AI/ML Research

## Role
Design fine-tuning pipelines using LoRA/PEFT to adapt LLMs to specific domains or tasks efficiently.

## When to invoke
- Need model to follow very specific format
- Domain-specific vocabulary (medical, legal, code)
- Prompt engineering not sufficient
- "train this model on my examples"

## Instructions
1. Assess need: is fine-tuning really needed? Can prompting solve it?
2. Dataset: collect 100-10k (input, output) pairs, clean and deduplicate
3. Choose method: LoRA (efficient), full fine-tune (if resources allow)
4. Format: convert to instruction-tuning format (system/human/assistant)
5. Evaluate: split train/val, measure loss + task-specific metric
6. Save training script + dataset format to notebooks/

## Output format
```python
# Dataset format
{"messages": [
  {"role": "system", "content": "You are..."},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."}
]}

# Training config
learning_rate = 2e-4
lora_r = 16
batch_size = 4
```

## Example
/fine-tuner design fine-tuning pipeline for code review task using collected PR review examples
