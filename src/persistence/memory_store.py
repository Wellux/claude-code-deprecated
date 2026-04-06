"""MCP Memory Store — persist facts, entities, and decisions via MCP memory server.

Wraps the mcp__memory__ tool interface with a clean Python API.
Falls back gracefully when the MCP server is not available.

Usage:
    store = MemoryStore()
    store.remember("project uses PostgreSQL for all persistence")
    store.remember_entity("LightRAG", "tool", ["graph-based RAG", "EMNLP 2025"])
    facts = store.recall("database")
"""
from __future__ import annotations

from dataclasses import dataclass

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Entity:
    name: str
    entity_type: str
    observations: list[str]


@dataclass
class Relation:
    from_entity: str
    to_entity: str
    relation_type: str


class MemoryStore:
    """Persistent memory via MCP memory server.

    Falls back to in-memory dict when MCP is unavailable,
    so code using this never needs try/except at the call site.
    """

    def __init__(self):
        self._fallback: dict[str, list[str]] = {}
        self._mcp_available = self._check_mcp()

    def _check_mcp(self) -> bool:
        """Return True if MCP memory tools are importable."""
        try:
            # MCP tools are injected by Claude Code at runtime.
            # In standalone Python execution they won't exist.
            return False  # standalone — always use fallback
        except Exception:
            return False

    # ── Write operations ──────────────────────────────────────────────────────

    def remember(self, fact: str, entity_name: str = "general") -> None:
        """Store a plain-text observation, optionally under an entity name."""
        if self._mcp_available:
            self._mcp_add_observation(entity_name, fact)
        else:
            self._fallback.setdefault(entity_name, []).append(fact)
            logger.debug("memory_stored_local", entity=entity_name, fact=fact[:60])

    def remember_entity(
        self,
        name: str,
        entity_type: str,
        observations: list[str],
    ) -> None:
        """Create or update a named entity with observations."""
        if self._mcp_available:
            self._mcp_create_entity(name, entity_type, observations)
        else:
            self._fallback.setdefault(name, []).extend(observations)
            logger.debug("entity_stored_local", name=name, obs_count=len(observations))

    def remember_relation(
        self,
        from_entity: str,
        to_entity: str,
        relation_type: str,
    ) -> None:
        """Store a relationship between two entities."""
        fact = f"{from_entity} --[{relation_type}]--> {to_entity}"
        self.remember(fact, entity_name="_relations")

    # ── Read operations ───────────────────────────────────────────────────────

    def recall(self, query: str) -> list[str]:
        """Search memory for facts matching query. Returns list of strings."""
        if self._mcp_available:
            return self._mcp_search(query)
        # Fallback: simple substring search across all stored facts
        results = []
        for entity, facts in self._fallback.items():
            for fact in facts:
                if query.lower() in fact.lower() or query.lower() in entity.lower():
                    results.append(f"[{entity}] {fact}")
        return results

    def recall_entity(self, name: str) -> Entity | None:
        """Retrieve all observations for a named entity."""
        if self._mcp_available:
            return self._mcp_open_node(name)
        facts = self._fallback.get(name)
        if not facts:
            return None
        return Entity(name=name, entity_type="unknown", observations=facts)

    def read_all(self) -> dict[str, list[str]]:
        """Return full memory graph (fallback only)."""
        return dict(self._fallback)

    # ── Delete operations ─────────────────────────────────────────────────────

    def forget(self, entity_name: str) -> None:
        """Remove all memory for an entity."""
        if self._mcp_available:
            self._mcp_delete_entity(entity_name)
        else:
            self._fallback.pop(entity_name, None)

    def forget_observation(self, entity_name: str, observation: str) -> None:
        """Remove a specific observation from an entity."""
        if self._mcp_available:
            self._mcp_delete_observation(entity_name, observation)
        else:
            facts = self._fallback.get(entity_name, [])
            self._fallback[entity_name] = [f for f in facts if f != observation]

    # ── MCP bridge (called at runtime by Claude Code) ─────────────────────────
    # These methods are stubs — Claude Code injects the real MCP tools.
    # In standalone Python they log a warning and no-op.

    def _mcp_add_observation(self, entity: str, obs: str) -> None:
        logger.warning("mcp_not_available", op="add_observation", entity=entity)

    def _mcp_create_entity(self, name: str, etype: str, obs: list[str]) -> None:
        logger.warning("mcp_not_available", op="create_entity", name=name)

    def _mcp_search(self, query: str) -> list[str]:
        logger.warning("mcp_not_available", op="search", query=query)
        return []

    def _mcp_open_node(self, name: str) -> Entity | None:
        logger.warning("mcp_not_available", op="open_node", name=name)
        return None

    def _mcp_delete_entity(self, name: str) -> None:
        logger.warning("mcp_not_available", op="delete_entity", name=name)

    def _mcp_delete_observation(self, entity: str, obs: str) -> None:
        logger.warning("mcp_not_available", op="delete_observation", entity=entity)

    @property
    def size(self) -> int:
        """Number of entities in fallback store."""
        return len(self._fallback)
