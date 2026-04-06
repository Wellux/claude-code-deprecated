---
name: data-pipeline
description: >
  Design and build data pipelines for ingestion, transformation, and storage. Invoke for:
  "data pipeline", "ETL", "data ingestion", "process this data", "batch processing",
  "stream processing", "data transformation", "data workflow".
argument-hint: data source and target transformation
allowed-tools: Read, Write, Edit, Glob
---

# Skill: Data Pipeline — ETL & Data Processing
**Category:** Optimization/Research

## Role
Design reliable, observable data pipelines with proper error handling, retry logic, and data validation.

## When to invoke
- "build a pipeline to process X"
- ETL design
- Batch or stream data processing
- Research data ingestion

## Instructions
1. Extract: read from source (files, API, DB), handle pagination/batching
2. Transform: clean, validate, normalize, enrich
3. Load: write to destination with idempotency (safe to retry)
4. Error handling: dead letter queue for failed records, not silent failure
5. Observability: log records processed/failed, processing time, data quality metrics
6. Checkpoint: resumable on failure

## Output format
Complete Python pipeline with:
- Source reader with pagination
- Transformation functions
- Destination writer with idempotency
- Error handling and logging
- Run stats output

## Example
/data-pipeline build pipeline to ingest research papers from data/research/ → embeddings → data/embeddings/
