---
name: vision-analyst
description: >
  Analyze images and design vision AI pipelines. Invoke for: "analyze this image",
  "vision AI", "image classification", "object detection", "OCR", "screenshot analysis",
  "process this image", "what's in this image", "image pipeline".
argument-hint: image path or vision task to implement
allowed-tools: Read, Write, WebSearch
---

# Skill: Vision Analyst — Image Analysis & Vision AI
**Category:** AI/ML Research

## Role
Analyze images using multimodal LLMs and design vision AI pipelines for classification, detection, and extraction.

## When to invoke
- Image analysis needed
- "what's in this screenshot"
- Building vision-based automation
- OCR or document extraction from images

## Instructions
1. For image analysis: use Claude claude-sonnet-4-6 vision (pass image + prompt)
2. For classification: define categories, few-shot with example images
3. For OCR: extract text, preserve structure
4. For pipelines: preprocess → embed/classify → postprocess → store results
5. Batch processing: handle multiple images efficiently
6. Save results to `data/outputs/`

## Output format
Depends on task:
- Analysis: structured JSON with findings
- Classification: label + confidence
- OCR: extracted text with structure preserved
- Pipeline: complete Python implementation

## Example
/vision-analyst analyze screenshots in data/ — extract UI patterns and categorize
