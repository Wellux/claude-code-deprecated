---
name: dataset-curator
description: >
  Curate, clean, and prepare datasets for AI training and evaluation. Invoke for:
  "clean this dataset", "prepare training data", "dataset curation", "deduplicate data",
  "label this data", "data quality", "prepare eval set", "filter bad examples".
argument-hint: dataset path or description of data to curate
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Skill: Dataset Curator — Training Data Preparation
**Category:** AI/ML Research

## Role
Clean, deduplicate, and structure datasets for AI training, fine-tuning, or evaluation.

## When to invoke
- Preparing training data for fine-tuning
- Building evaluation sets
- Cleaning scraped or collected data
- "this dataset is messy — clean it"

## Instructions
1. Load and profile the dataset: size, format, field distributions
2. Remove duplicates (exact and near-duplicate using hashing or embeddings)
3. Filter quality: remove empty, too-short, or clearly wrong examples
4. Normalize: consistent format, encoding, whitespace
5. Split: train/validation/test (80/10/10)
6. Save cleaned version to `data/prompts/` or `data/outputs/`
7. Document: data card with statistics and filtering decisions

## Output format
```
## Dataset Curation Report — <dataset>
### Before: N examples, X% duplicates, Y% quality issues
### Filters Applied
### After: M examples (split: X train / Y val / Z test)
### Data Card
```

## Example
/dataset-curator data/prompts/code_review_examples.jsonl — deduplicate and quality filter
