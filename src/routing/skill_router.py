"""Skill Router — map user intent to the right skill.

Two-stage matching:
1. Keyword match — single compiled-regex scan against all trigger phrases
2. Category match — broader topic → skill category → best skill in category

Each skill entry has:
- triggers: exact phrases that strongly indicate this skill
- categories: broader topic buckets
- priority: higher = preferred when multiple match (0-10)
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SkillMatch:
    skill: str               # skill name (matches .claude/skills/<name>/)
    confidence: float        # 0.0 - 1.0
    reason: str              # why this skill was selected
    category: str
    fallback: str | None = None  # next-best skill if primary unavailable


# ---------------------------------------------------------------------------
# Skill registry — each entry maps skill_name → trigger signals
# ---------------------------------------------------------------------------
_SKILL_REGISTRY: list[dict] = [
    # ── Security ────────────────────────────────────────────────────────────
    {"skill": "ciso",             "category": "security", "priority": 9,
     "triggers": ["security orchestrat", "full security", "run the team", "security strategy", "ciso",
                  "security audit", "security assessment", "security posture"]},
    {"skill": "pen-tester",       "category": "security", "priority": 8,
     "triggers": ["penetration test", "pentest", "red team", "exploit", "adversary emulation",
                  "offensive security", "attack surface", "ethical hacking", "find vulnerabilities"]},
    {"skill": "appsec-engineer",  "category": "security", "priority": 8,
     "triggers": ["owasp", "sql injection", "xss", "csrf", "secure code review", "application security",
                  "appsec", "sast", "input validation", "is this safe"]},
    {"skill": "soc-analyst",      "category": "security", "priority": 7,
     "triggers": ["threat detection", "siem", "alert triage", "incident triage", "blue team", "soc",
                  "threat hunting", "triage this alert", "investigate this log"]},
    {"skill": "incident-response","category": "security", "priority": 9,
     "triggers": ["incident", "breach", "prod is down", "production down", "compromised", "forensic",
                  "containment", "we got breached", "ir plan"]},
    {"skill": "ai-security",      "category": "security", "priority": 8,
     "triggers": ["prompt injection", "jailbreak", "llm security", "agent security",
                  "system prompt leakage", "tool call validation", "llm guardrails",
                  "adversarial inputs", "ai pipeline security"]},
    {"skill": "grc-analyst",      "category": "security", "priority": 6,
     "triggers": ["compliance", "gdpr", "soc2", "hipaa", "compliance audit", "governance",
                  "iso 27001", "regulatory compliance", "compliance check", "grc audit"]},
    {"skill": "iam-engineer",     "category": "security", "priority": 7,
     "triggers": ["sso", "oauth", "mfa", "rbac", "access control", "identity", "permissions", "iam",
                  "least privilege", "service account", "role design"]},
    {"skill": "secrets-mgr",      "category": "security", "priority": 7,
     "triggers": ["secret", "api key", "credential", "vault", "rotate key", "env var leak",
                  "hashicorp vault", "secrets management", "no hardcoded secrets"]},

    # ── Development ─────────────────────────────────────────────────────────
    {"skill": "code-review",      "category": "development", "priority": 8,
     "triggers": ["review this", "review my code", "pr review", "before i merge", "check my code",
                  "lgtm?", "code quality", "look at this implementation", "feedback on code"]},
    {"skill": "debug",            "category": "development", "priority": 9,
     "triggers": ["error", "bug", "broken", "traceback", "exception", "failing", "not working",
                  "fix this", "debug this", "why is this failing", "it crashes"]},
    {"skill": "refactor",         "category": "development", "priority": 7,
     "triggers": ["refactor", "clean up", "restructure", "simplify this code", "too complex",
                  "reduce duplication", "dry this up", "spaghetti code"]},
    {"skill": "architect",        "category": "development", "priority": 8,
     "triggers": ["design this", "architect", "system design", "how should i structure",
                  "design decision", "technical design doc", "scalability design", "architecture review"]},
    {"skill": "test-writer",      "category": "development", "priority": 7,
     "triggers": ["write tests", "add tests", "test coverage", "unit test", "pytest", "jest",
                  "tdd", "improve coverage", "test this function", "missing tests"]},
    {"skill": "api-designer",     "category": "development", "priority": 7,
     "triggers": ["design api", "rest api", "api endpoint", "openapi", "swagger", "api schema",
                  "api spec", "endpoint design", "what endpoints do i need"]},
    {"skill": "type-safety",      "category": "development", "priority": 6,
     "triggers": ["add types", "type annotation", "mypy", "typescript types", "type hints", "typed",
                  "type errors", "any type", "missing types"]},
    {"skill": "perf-profiler",    "category": "development", "priority": 7,
     "triggers": ["slow", "performance", "profil", "bottleneck", "latency", "optimize speed", "p99",
                  "cpu spike", "benchmark performance"]},
    {"skill": "bug-hunter",       "category": "development", "priority": 7,
     "triggers": ["find bugs", "hunt for", "edge case", "vulnerability scan code",
                  "stress test", "off-by-one", "null pointer", "find weaknesses",
                  "adversarial test"]},
    {"skill": "tech-debt",        "category": "development", "priority": 6,
     "triggers": ["tech debt", "technical debt", "cleanup", "legacy code", "modernize",
                  "dead code", "deprecated", "code smells", "cruft"]},

    # ── AI / ML ─────────────────────────────────────────────────────────────
    {"skill": "karpathy-researcher", "category": "research", "priority": 9,
     "triggers": ["research", "deep dive", "first principles", "latest on", "how does x work",
                  "explain from scratch", "deep dive into", "understand x from scratch", "karpathy"]},
    {"skill": "rag-builder",      "category": "ai", "priority": 8,
     "triggers": ["rag", "retrieval", "vector store", "embedding search", "knowledge base retrieval",
                  "lightrag", "semantic search", "document retrieval",
                  "reduce hallucination with retrieval"]},
    {"skill": "prompt-engineer",  "category": "ai", "priority": 8,
     "triggers": ["improve this prompt", "prompt engineering", "optimize prompt", "system prompt",
                  "few-shot", "chain of thought", "better prompt for", "my prompt isn't working"]},
    {"skill": "llm-optimizer",    "category": "ai", "priority": 7,
     "triggers": ["reduce cost", "token cost", "cheaper inference", "latency llm", "optimize inference",
                  "llm cost too high", "reduce tokens", "llm performance", "token optimization"]},
    {"skill": "fine-tuner",       "category": "ai", "priority": 8,
     "triggers": ["fine-tune", "fine tune", "lora", "qlora", "train model", "finetune",
                  "domain adaptation", "custom model", "instruction tuning"]},
    {"skill": "evals-designer",   "category": "ai", "priority": 7,
     "triggers": ["eval", "evaluation", "benchmark", "measure quality", "llm grading",
                  "test prompts at scale", "measure hallucination", "model comparison",
                  "build an eval suite"]},
    {"skill": "agent-orchestrator","category": "ai", "priority": 8,
     "triggers": ["multi-agent", "orchestrat", "agent pipeline", "chain agents", "coordinate agents",
                  "agent workflow", "agent system", "task delegation to agents"]},
    {"skill": "paper-summarizer", "category": "research", "priority": 7,
     "triggers": ["summarize paper", "arxiv", "research paper", "academic paper", "this study",
                  "tldr this", "what does this paper say", "key findings of"]},

    # ── DevOps ──────────────────────────────────────────────────────────────
    {"skill": "ci-cd",            "category": "devops", "priority": 8,
     "triggers": ["ci/cd", "github actions", "pipeline", "deploy pipeline", "build fails", "cicd",
                  "continuous integration", "automated testing pipeline", "deploy on push"]},
    {"skill": "docker",           "category": "devops", "priority": 7,
     "triggers": ["dockerfile", "docker", "container", "image build", "docker-compose",
                  "multi-stage build", "docker optimization", "containerize"]},
    {"skill": "monitoring",       "category": "devops", "priority": 7,
     "triggers": ["monitor", "alert", "dashboard", "observabilit", "metrics", "grafana", "datadog",
                  "prometheus", "alerting", "what should i alert on"]},
    {"skill": "sre",              "category": "devops", "priority": 7,
     "triggers": ["slo", "sla", "error budget", "reliability", "on-call", "sre",
                  "toil", "post-mortem", "site reliability"]},
    {"skill": "deploy-checker",   "category": "devops", "priority": 8,
     "triggers": ["ready to deploy", "pre-deploy", "deployment checklist", "safe to ship",
                  "deployment check", "pre-prod validation", "deployment gate"]},

    # ── Documentation ───────────────────────────────────────────────────────
    {"skill": "readme-writer",    "category": "docs", "priority": 7,
     "triggers": ["write readme", "update readme", "readme", "documentation for this project",
                  "docs are outdated", "improve documentation"]},
    {"skill": "adr-writer",       "category": "docs", "priority": 7,
     "triggers": ["adr", "architecture decision", "decision record", "why did we choose",
                  "write adr", "document this decision", "architecture choice"]},
    {"skill": "runbook-creator",  "category": "docs", "priority": 6,
     "triggers": ["runbook", "operational procedure", "how to operate", "step by step ops",
                  "ops runbook", "document this procedure", "incident runbook"]},
    {"skill": "changelog",        "category": "docs", "priority": 6,
     "triggers": ["changelog", "release notes", "what changed", "git log to changelog",
                  "changelog entry", "commit history summary", "what's new in this release"]},

    # ── Infrastructure ──────────────────────────────────────────────────────
    {"skill": "k8s",              "category": "devops", "priority": 8,
     "triggers": ["kubernetes", "k8s", "helm", "deployment manifest", "pod", "kubectl", "cluster",
                  "hpa", "ingress"]},
    {"skill": "terraform",        "category": "devops", "priority": 8,
     "triggers": ["terraform", "infrastructure as code", "iac", "hcl", "provisioning", "resource plan",
                  "aws terraform", "terraform module"]},
    {"skill": "db-optimizer",     "category": "development", "priority": 7,
     "triggers": ["slow query", "query performance", "missing index", "n+1", "database slow",
                  "explain plan", "add index", "query optimization"]},
    {"skill": "migration",        "category": "development", "priority": 7,
     "triggers": ["database migration", "schema migration", "alembic", "data migration", "migrate db",
                  "upgrade", "breaking change", "version upgrade"]},

    # ── Ecosystem (gstack · Superpowers · Paperclip) ─────────────────────
    {"skill": "gsd",              "category": "meta", "priority": 9,
     "triggers": ["just do it", "get it done", "no interruptions", "gsd",
                  "stay focused", "focus mode", "no more planning", "execute not plan"]},
    {"skill": "swarm",            "category": "meta", "priority": 9,
     "triggers": ["parallel agents", "spin up agents", "swarm", "decompose into subagents",
                  "multiple agents", "break into subagents", "what agents do i need", "build a swarm"]},
    {"skill": "mem",              "category": "meta", "priority": 8,
     "triggers": ["remember this", "save this", "persist", "don't forget", "store this decision",
                  "add to memory", "save to memory", "note this down"]},
    {"skill": "brainstorm",       "category": "meta", "priority": 8,
     "triggers": ["brainstorm", "explore options", "what should i build", "unclear requirements",
                  "not sure what to build", "help me think through", "refine requirements",
                  "explore the design space"]},
    {"skill": "write-plan",       "category": "meta", "priority": 8,
     "triggers": ["write a plan", "plan this out", "break this down", "decompose this task",
                  "create a task plan", "write plan", "task breakdown", "planning phase",
                  "decompose this feature"]},
    {"skill": "superpowers",      "category": "meta", "priority": 9,
     "triggers": ["high agency", "senior engineer mode", "superpowers", "act like a staff engineer",
                  "just figure it out", "full autonomy", "autonomous coding", "superpowers mode"]},
    {"skill": "office-hours",     "category": "meta", "priority": 8,
     "triggers": ["office hours", "debate the approach", "should we build", "before we start",
                  "strategic review", "ceo review", "product review", "pre-build review",
                  "get alignment"]},
    {"skill": "ship",             "category": "meta", "priority": 9,
     "triggers": ["ready to ship", "cut a release", "release checklist", "deploy to production",
                  "ship this feature", "release pipeline", "ship it", "go live",
                  "push to production"]},
    {"skill": "careful",          "category": "meta", "priority": 8,
     "triggers": ["careful mode", "risky change", "be careful", "irreversible", "low-risk mode",
                  "extra confirmation", "don't break anything", "proceed carefully",
                  "sensitive system"]},
    {"skill": "plan-eng-review",  "category": "meta", "priority": 8,
     "triggers": ["eng review", "technical review", "review my plan", "sanity check the design",
                  "is this the right way", "pre-implementation review", "staff review",
                  "check my plan"]},
    {"skill": "paperclip",        "category": "meta", "priority": 8,
     "triggers": ["assign to agents", "multi-agent task", "agent budget", "orchestrate agents",
                  "paperclip", "agent audit trail", "agent org", "agent with budget", "agent company"]},

    # ── Additional Security ──────────────────────────────────────────────────
    {"skill": "network-engineer",  "category": "security", "priority": 7,
     "triggers": ["firewall", "vpn", "zero-trust", "network security", "network segmentation",
                  "port exposure", "dns security", "tls config", "open ports", "network hardening"]},
    {"skill": "cloud-engineer",    "category": "security", "priority": 7,
     "triggers": ["cloud security", "iam policies", "s3 bucket", "cloud config",
                  "infrastructure security", "cloud hardening", "security groups",
                  "aws security", "cloud misconfiguration"]},
    {"skill": "security-engineer", "category": "security", "priority": 7,
     "triggers": ["siem rule", "waf", "detection engineering", "security tooling",
                  "alert rule", "intrusion detection", "sigma rule", "snort rule",
                  "write detection"]},
    {"skill": "purple-team",       "category": "security", "priority": 7,
     "triggers": ["purple team", "detection validation", "mitre att&ck", "test our defenses",
                  "adversary simulation", "does our monitoring catch"]},
    {"skill": "dba",               "category": "security", "priority": 6,
     "triggers": ["database security", "db permissions", "encryption at rest",
                  "connection string security", "database hardening", "query audit",
                  "backup encryption", "db access review"]},
    {"skill": "help-desk",         "category": "security", "priority": 5,
     "triggers": ["access request", "user provisioning", "endpoint hardening",
                  "device compliance", "mfa setup", "password reset policy",
                  "user offboarding", "permissions request"]},
    {"skill": "sysadmin",          "category": "security", "priority": 6,
     "triggers": ["os hardening", "patch status", "cron security",
                  "file permissions audit", "system configuration",
                  "server hardening", "syslog"]},
    {"skill": "devops-engineer",   "category": "security", "priority": 7,
     "triggers": ["pipeline security", "docker security", "secrets in code", "ci/cd review",
                  "container hardening", "dockerfile audit", "secrets scanning",
                  "github actions security", "hardcoded credentials"]},

    # ── Additional Development ───────────────────────────────────────────────
    {"skill": "async-optimizer",   "category": "development", "priority": 7,
     "triggers": ["async issue", "concurrent", "race condition", "await optimization", "run in parallel",
                  "asyncio", "promise.all", "thread safety", "deadlock", "async bottleneck"]},
    {"skill": "error-handler",     "category": "development", "priority": 6,
     "triggers": ["error handling", "exception handling", "retry logic", "circuit breaker",
                  "graceful degradation", "fallback", "resilience", "fault tolerance",
                  "what happens on failure"]},
    {"skill": "algorithm",         "category": "development", "priority": 7,
     "triggers": ["algorithm improvement", "better algorithm", "o(n", "data structure choice",
                  "optimize this loop", "algorithmic complexity", "time complexity"]},
    {"skill": "concurrency",       "category": "development", "priority": 7,
     "triggers": ["concurrency design", "parallel processing", "worker pool", "queue",
                  "producer consumer", "concurrent writes", "data consistency with concurrent"]},
    {"skill": "cache-strategy",    "category": "development", "priority": 7,
     "triggers": ["add caching", "cache this", "redis", "cache invalidation", "ttl", "cache miss",
                  "expensive operation", "repeated computation", "memoize"]},
    {"skill": "bundle-analyzer",   "category": "development", "priority": 6,
     "triggers": ["bundle size", "reduce bundle", "tree shaking", "code splitting",
                  "large dependency", "bundle too big", "import optimization", "lazy loading"]},
    {"skill": "memory-profiler",   "category": "development", "priority": 7,
     "triggers": ["memory leak", "too much memory", "oom", "memory usage", "memory profiling",
                  "garbage collection", "memory keeps growing", "reduce memory footprint"]},
    {"skill": "query-optimizer",   "category": "development", "priority": 7,
     "triggers": ["optimize sql", "full table scan", "slow sql", "sql performance",
                  "query plan", "index suggestion"]},
    {"skill": "db-designer",       "category": "development", "priority": 7,
     "triggers": ["design database schema", "data model", "entity relationship", "er diagram",
                  "normalize tables", "design tables", "create schema", "database design review",
                  "foreign keys", "relational model"]},
    {"skill": "dep-auditor",       "category": "development", "priority": 7,
     "triggers": ["dependency audit", "npm audit", "pip audit", "outdated packages",
                  "cve check", "license compliance", "supply chain security",
                  "vulnerable dependency", "update packages"]},
    {"skill": "pr-reviewer",       "category": "development", "priority": 7,
     "triggers": ["review pr", "pr feedback", "pull request review", "diff review",
                  "code change review", "should i merge this", "lgtm check"]},
    {"skill": "feature-planner",   "category": "development", "priority": 7,
     "triggers": ["plan this feature", "implementation plan",
                  "feature spec", "how do i implement x", "what are the steps",
                  "make a plan for", "i need to build", "feature breakdown"]},

    # ── Additional AI/ML ─────────────────────────────────────────────────────
    {"skill": "ml-debugger",       "category": "ai", "priority": 7,
     "triggers": ["loss not converging", "model not learning", "nan loss", "gradient explosion",
                  "inference error", "model output wrong", "training failed",
                  "why is accuracy so low"]},
    {"skill": "model-benchmarker", "category": "ai", "priority": 7,
     "triggers": ["compare models", "which model is best", "benchmark claude",
                  "model selection", "cost vs quality", "is haiku fast enough"]},
    {"skill": "embeddings",        "category": "ai", "priority": 7,
     "triggers": ["embeddings", "vector similarity", "embed this text",
                  "find similar", "text similarity", "nearest neighbor search", "clustering"]},
    {"skill": "dataset-curator",   "category": "ai", "priority": 7,
     "triggers": ["clean this dataset", "prepare training data", "dataset curation",
                  "deduplicate data", "label this data", "data quality",
                  "prepare eval set", "filter bad examples"]},
    {"skill": "ai-safety",         "category": "ai", "priority": 8,
     "triggers": ["ai safety review", "bias check", "fairness audit", "alignment",
                  "responsible ai", "misuse prevention", "ai ethics", "safety guardrails",
                  "could this ai system be misused"]},
    {"skill": "vision-analyst",    "category": "ai", "priority": 7,
     "triggers": ["analyze this image", "vision ai", "image classification",
                  "object detection", "ocr", "screenshot analysis",
                  "process this image", "image pipeline"]},
    {"skill": "multimodal",        "category": "ai", "priority": 7,
     "triggers": ["multimodal", "text and images", "vision + language",
                  "image + text pipeline", "document understanding",
                  "multimodal embeddings", "cross-modal search"]},

    # ── Additional DevOps ────────────────────────────────────────────────────
    {"skill": "backup",            "category": "devops", "priority": 6,
     "triggers": ["backup strategy", "disaster recovery", "backup verification",
                  "restore test", "rto", "rpo", "data loss prevention", "backup schedule"]},
    {"skill": "scaling",           "category": "devops", "priority": 7,
     "triggers": ["scaling plan", "handle more traffic", "auto-scaling", "load balancing",
                  "capacity planning", "how do i scale this", "handle 10x load"]},
    {"skill": "cost-optimizer",    "category": "devops", "priority": 7,
     "triggers": ["reduce cloud costs", "cost optimization", "aws cost", "cloud bill",
                  "right-sizing", "idle resources", "spot instances", "reserved instances"]},
    {"skill": "pipeline-opt",      "category": "devops", "priority": 7,
     "triggers": ["pipeline too slow", "slow ci", "speed up builds", "pipeline optimization",
                  "cache builds", "parallel jobs", "flaky tests", "pipeline reliability"]},
    {"skill": "rollback",          "category": "devops", "priority": 8,
     "triggers": ["rollback", "revert deployment", "undo deploy", "something broke in prod",
                  "roll back to previous", "deployment failed", "revert to v"]},
    {"skill": "infra-docs",        "category": "devops", "priority": 6,
     "triggers": ["document the infrastructure", "infra diagram", "network diagram",
                  "infrastructure documentation", "how does our infra work",
                  "ops documentation", "infra docs"]},
    {"skill": "logging",           "category": "devops", "priority": 6,
     "triggers": ["logging setup", "structured logs", "log aggregation", "elk stack",
                  "log analysis", "add logging", "logging config", "log format",
                  "how should i log"]},
    {"skill": "metrics-designer",  "category": "devops", "priority": 6,
     "triggers": ["add metrics", "instrument this code", "design metrics", "prometheus metrics",
                  "custom metrics", "application metrics", "observability metrics"]},
    {"skill": "cron-scheduler",    "category": "devops", "priority": 6,
     "triggers": ["schedule this", "run every day", "cron job", "scheduled task",
                  "automation schedule", "run weekly", "cron expression",
                  "set up recurring task"]},

    # ── Documentation ────────────────────────────────────────────────────────
    {"skill": "api-docs",          "category": "docs", "priority": 7,
     "triggers": ["document this api", "api docs", "openapi spec",
                  "endpoint documentation", "api reference",
                  "document these endpoints", "api documentation missing"]},
    {"skill": "changelog-maintainer", "category": "docs", "priority": 5,
     "triggers": ["keep changelog updated", "changelog is stale", "changelog maintenance",
                  "update release history", "automate changelog", "add to changelog"]},
    {"skill": "arch-diagrammer",   "category": "docs", "priority": 6,
     "triggers": ["draw architecture diagram", "system diagram", "architecture overview",
                  "visualize the system", "component diagram", "data flow diagram",
                  "sequence diagram", "c4 diagram"]},
    {"skill": "onboarding",        "category": "docs", "priority": 6,
     "triggers": ["onboarding guide", "new developer guide", "contributor guide",
                  "contributing.md", "how to get started", "new team member setup",
                  "first day guide"]},
    {"skill": "decision-logger",   "category": "docs", "priority": 6,
     "triggers": ["log this decision", "record why we chose", "decision log",
                  "we decided to", "document this choice", "capture this decision"]},
    {"skill": "tutorial-writer",   "category": "docs", "priority": 6,
     "triggers": ["write tutorial", "how-to guide", "tutorial for", "explain how to use",
                  "step-by-step guide", "workshop material", "create a tutorial",
                  "teach someone to use"]},
    {"skill": "knowledge-base",    "category": "docs", "priority": 7,
     "triggers": ["knowledge base", "second brain", "organize notes", "personal wiki",
                  "structured notes", "knowledge management",
                  "organize research into notes"]},

    # ── Web / Optimization ───────────────────────────────────────────────────
    {"skill": "web-vitals",        "category": "web", "priority": 7,
     "triggers": ["web vitals", "page speed", "lcp", "cls", "inp", "lighthouse",
                  "slow page load", "improve page speed", "core web vitals"]},
    {"skill": "seo-auditor",       "category": "web", "priority": 6,
     "triggers": ["seo audit", "improve seo", "search ranking", "meta tags",
                  "structured data", "sitemap", "robots.txt",
                  "keyword optimization", "google ranking", "on-page seo"]},
    {"skill": "a11y-checker",      "category": "web", "priority": 7,
     "triggers": ["accessibility", "a11y", "wcag", "screen reader", "aria labels",
                  "color contrast", "keyboard navigation",
                  "accessibility audit", "ada compliance"]},
    {"skill": "web-scraper",       "category": "web", "priority": 6,
     "triggers": ["scrape this website", "web scraping", "extract data from",
                  "crawl", "collect data from web", "automate data collection",
                  "fetch and parse html"]},

    # ── Project Management ───────────────────────────────────────────────────
    {"skill": "sprint-planner",    "category": "pm", "priority": 7,
     "triggers": ["plan the sprint", "sprint planning", "prioritize backlog",
                  "what should we work on", "sprint goals", "task prioritization",
                  "what's the next sprint"]},
    {"skill": "standup",           "category": "pm", "priority": 6,
     "triggers": ["standup", "daily standup", "what did i do yesterday",
                  "progress report", "status update", "daily update", "what's my update"]},
    {"skill": "retrospective",     "category": "pm", "priority": 6,
     "triggers": ["retrospective", "retro", "what went well", "what could be better",
                  "lessons learned", "sprint review", "team retrospective"]},
    {"skill": "roadmap",           "category": "pm", "priority": 7,
     "triggers": ["roadmap", "build roadmap", "what's the plan", "long-term plan", "6-month roadmap",
                  "product roadmap", "technical roadmap", "what comes after this"]},
    {"skill": "risk-assessor",     "category": "pm", "priority": 7,
     "triggers": ["risk assessment", "what could go wrong", "project risks", "risk register",
                  "mitigation plan", "identify risks", "what are the risks"]},
    {"skill": "scope-definer",     "category": "pm", "priority": 7,
     "triggers": ["define scope", "scope creep", "what's in scope", "mvp definition",
                  "what should we not build", "scope this project", "define boundaries"]},
    {"skill": "estimation",        "category": "pm", "priority": 6,
     "triggers": ["estimate this", "how long will this take", "story points",
                  "effort estimation", "timeline", "when can this be done",
                  "how complex is this"]},
    {"skill": "blocker-resolver",  "category": "pm", "priority": 8,
     "triggers": ["i'm blocked", "this is blocking me", "unblock this",
                  "resolve blocker", "stuck on", "how do i get past this", "blocker"]},
    {"skill": "stakeholder",       "category": "pm", "priority": 6,
     "triggers": ["stakeholder update", "executive summary", "status report",
                  "update the team", "write progress report",
                  "non-technical summary", "management update"]},
    {"skill": "competitive-analyst","category": "pm", "priority": 6,
     "triggers": ["competitive analysis", "compare to competitors", "what are the alternatives",
                  "market analysis", "how does x compare to y", "competitor research", "swot analysis"]},
    {"skill": "kpi-tracker",       "category": "pm", "priority": 6,
     "triggers": ["define kpis", "track metrics", "measure success",
                  "what metrics should we track", "kpi dashboard",
                  "okrs", "success metrics", "how do we know this worked"]},

    # ── Additional Ecosystem ─────────────────────────────────────────────────
    {"skill": "create",            "category": "meta", "priority": 8,
     "triggers": ["make a skill", "create an agent", "turn this into a skill",
                  "automate this", "save this workflow", "i keep doing this",
                  "create skill", "new skill", "create agent"]},
    {"skill": "obsidian",          "category": "meta", "priority": 6,
     "triggers": ["organize in obsidian", "atomic notes", "linked notes",
                  "knowledge graph", "note-taking", "build a wiki",
                  "organize my knowledge", "create linked notes"]},
    {"skill": "ui-ux",             "category": "meta", "priority": 7,
     "triggers": ["design this ui", "build this interface", "ui component",
                  "make this look good", "design system", "ui/ux",
                  "frontend design", "css design", "clean ui"]},
    {"skill": "trend-researcher",  "category": "meta", "priority": 7,
     "triggers": ["what's trending", "latest trends in", "emerging technology",
                  "market trends", "tech radar", "trend analysis",
                  "state of x in 2026"]},
    {"skill": "data-pipeline",     "category": "meta", "priority": 7,
     "triggers": ["data pipeline", "etl", "data ingestion", "process this data",
                  "batch processing", "stream processing",
                  "data transformation", "data workflow"]},

    # ── v0.9.0 — New skills from ecosystem research ───────────────────────────
    {"skill": "preflight",         "category": "meta", "priority": 9,
     "triggers": ["preflight check", "validate this prompt", "is this task clear",
                  "check before running", "prompt quality check", "pre-execution check",
                  "score this prompt", "is my task well defined", "task spec review"]},
    {"skill": "tdd",               "category": "development", "priority": 8,
     "triggers": ["test driven development", "tdd this", "write tests first",
                  "red-green-refactor", "write failing tests", "enforce tdd",
                  "test-first development", "tdd workflow"]},
    {"skill": "self-reflect",      "category": "meta", "priority": 7,
     "triggers": ["self reflect", "extract patterns", "mine learnings",
                  "update lessons from history", "retrospective patterns",
                  "session patterns", "learn from mistakes", "self reflection",
                  "improve from history", "what patterns emerged"]},
    {"skill": "chain-of-draft",    "category": "meta", "priority": 8,
     "triggers": ["chain of draft", "iterative refinement", "improve through drafts",
                  "draft and critique", "structured refinement", "progressive draft",
                  "multi-pass writing", "cod pattern", "draft critique improve"]},
    {"skill": "foresight",         "category": "meta", "priority": 7,
     "triggers": ["foresight", "strategic analysis", "what am i missing strategically",
                  "second order effects", "future risks", "what could blindside",
                  "horizon scanning", "strategic blind spots", "cross-domain analysis",
                  "long term risks", "contextual nudge"]},
    {"skill": "team",              "category": "meta", "priority": 8,
     "triggers": ["team mode", "spawn a team", "agent team", "parallel team review",
                  "multi-agent team", "code review team", "security team review",
                  "debug team", "architecture team", "ship team",
                  "multi-role review", "team of agents"]},
    {"skill": "context-diff",      "category": "meta", "priority": 7,
     "triggers": ["context diff", "what changed since last session", "diff since main",
                  "what's new since", "changes since checkpoint", "session diff",
                  "summarize changes since", "what did i change", "context since"]},
    {"skill": "riper",             "category": "meta", "priority": 9,
     "triggers": ["riper", "riper workflow", "research then innovate",
                  "five phase workflow", "research innovate plan execute review",
                  "structured feature workflow", "riper mode",
                  "phase-gated development", "systematic feature delivery"]},
    {"skill": "memory-bank",       "category": "meta", "priority": 7,
     "triggers": ["memory bank", "update memory bank", "sync memory",
                  "knowledge sync", "update project knowledge", "synchronize memory",
                  "keep memory current", "project memory",
                  "update knowledge base with code changes"]},
]

# Build fast lookup maps
_TRIGGER_INDEX: dict[str, str] = {}  # trigger_phrase → skill_name
_SKILL_MAP: dict[str, dict] = {}

for entry in _SKILL_REGISTRY:
    _SKILL_MAP[entry["skill"]] = entry
    for trigger in entry["triggers"]:
        _TRIGGER_INDEX[trigger] = entry["skill"]

# Compiled trigger pattern — sorted longest-first so "unit test" matches before "test".
# One regex scan replaces O(n) individual `trigger in text` checks.
_TRIGGER_PATTERN: re.Pattern[str] = re.compile(
    "|".join(re.escape(t) for t in sorted(_TRIGGER_INDEX, key=len, reverse=True))
)


def route_skill(user_input: str) -> SkillMatch | None:
    """Return the best matching skill for the given user input, or None.

    Matching priority:
    1. Exact / substring trigger match (highest confidence)
    2. Category-level keyword match (medium confidence)
    3. No match → None (let Claude decide without a skill hint)
    """
    text = user_input.lower()
    matches: list[tuple[int, float, dict]] = []  # (priority, confidence, entry)

    # Stage 1: single regex scan — O(len(text)) instead of O(n_triggers × len(text))
    seen_skills: set[str] = set()
    for m in _TRIGGER_PATTERN.finditer(text):
        skill_name = _TRIGGER_INDEX[m.group(0)]
        if skill_name in seen_skills:
            continue
        seen_skills.add(skill_name)
        entry = _SKILL_MAP[skill_name]
        confidence = 0.7 + (entry["priority"] / 10) * 0.3
        matches.append((entry["priority"], confidence, entry))

    if not matches:
        return None

    # Sort by priority desc, confidence desc
    matches.sort(key=lambda x: (x[0], x[1]), reverse=True)
    best_priority, best_confidence, best_entry = matches[0]

    # Find fallback (second best, different skill)
    fallback = None
    for _, _, entry in matches[1:]:
        if entry["skill"] != best_entry["skill"]:
            fallback = entry["skill"]
            break

    return SkillMatch(
        skill=best_entry["skill"],
        confidence=round(best_confidence, 2),
        reason=f"trigger match in category={best_entry['category']} priority={best_priority}",
        category=best_entry["category"],
        fallback=fallback,
    )


def route_skill_by_category(category: str) -> list[str]:
    """Return all skills in a given category, sorted by priority."""
    skills = [e for e in _SKILL_REGISTRY if e["category"] == category]
    skills.sort(key=lambda e: e["priority"], reverse=True)
    return [e["skill"] for e in skills]


def list_categories() -> list[str]:
    return sorted(set(e["category"] for e in _SKILL_REGISTRY))
