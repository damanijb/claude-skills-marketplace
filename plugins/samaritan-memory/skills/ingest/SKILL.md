---
name: memory-ingest
description: "This skill should be used when the user asks to \"remember this\", \"store in memory\", \"save this\", \"record this\", \"add to memory\", \"log this decision\", \"note this preference\", or wants to persist information for future recall. Also triggers on \"record\", \"memorize\", \"don't forget\", or any request to store knowledge, decisions, preferences, insights, or events."
---

# Memory Ingest — Store & Record

Store information in the hybrid memory system with automatic semantic embedding, deduplication, and background entity extraction to the knowledge graph.

## Quick Store

For simple memory storage with auto entity extraction:

```
memory_add(
    content="<what to remember>",
    memory_type="insight",
    importance="normal",
    tags=["optional", "tags"]
)
```

The system automatically:
1. Generates a 2048d embedding via Qwen3-VL-Embedding-2B
2. Checks for duplicate memories (similarity > 0.85 → updates existing)
3. Stores the vector in Qdrant
4. Extracts entities, facts, and relationships in the background
5. Adds extracted knowledge to the Neo4j graph

## Full Record (Vector + Graph)

For explicit control over both vector and graph storage:

```
record(
    content="Decided to use SGLang over vLLM for embedding serving due to better CPU offloading",
    memory_type="decision",
    entities=[
        {"name": "SGLang", "type": "Tool"},
        {"name": "vLLM", "type": "Tool"}
    ],
    facts=[
        {"subject": "SGLang", "predicate": "chosen_over", "object": "vLLM"},
        {"subject": "SGLang", "predicate": "advantage", "object": "better CPU offloading"}
    ]
)
```

## Memory Types

| Type | When to Use | Example |
|------|-------------|---------|
| `preference` | User likes/dislikes, style choices | "Prefers concise responses without fluff" |
| `decision` | Choices made with rationale | "Chose Qdrant over Pinecone for self-hosting" |
| `insight` | Learnings, patterns, observations | "Qwen3-VL embeddings score 0.47 avg on finance queries" |
| `event` | Things that happened | "Migrated from Ollama to SGLang on 2026-03-11" |
| `task` | Work items, todos | "Re-ingest books after embedding model change" |

## Importance Levels

| Level | When to Use |
|-------|-------------|
| `low` | Background context, nice-to-know |
| `normal` | Standard information (default) |
| `high` | Important decisions, strong preferences |
| `critical` | Must never forget — core identity, key constraints |

## Deduplication

The system automatically deduplicates:
- New memories are compared against existing ones via embedding similarity
- If similarity > 0.85, the existing memory is **updated** instead of creating a duplicate
- To force a new entry (e.g., superseding), pass `supersedes="<old_memory_id>"`

## RECALL→ACT→RECORD Pattern

Follow this loop on every significant action:
1. **RECALL**: Search memory for relevant context before acting
2. **ACT**: Use retrieved context to inform the response
3. **RECORD**: Store new decisions, insights, or events for future recall

This ensures the memory system stays current and comprehensive.
