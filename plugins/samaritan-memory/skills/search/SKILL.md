---
name: memory-search
description: "This skill should be used when the user asks to \"search memory\", \"find in memory\", \"search for memories about\", \"what memories match\", or wants to perform targeted semantic search with filters. Also triggers on \"find decisions about\", \"search preferences\", \"search insights\", or any filtered memory retrieval request."
---

# Memory Search — Semantic Vector Search

Perform targeted semantic searches across stored memories in Qdrant with optional filtering by type, importance, and status, plus reranking via Qwen3-VL-Reranker.

## Core Search

```
memory_search(query="<search query>", limit=5, rerank=true)
```

Returns memories ranked by semantic similarity, optionally reranked by the Qwen3-VL-Reranker for higher precision.

## Filtered Search

Filter by memory type to narrow results:

| Type | Use Case |
|------|----------|
| `preference` | User preferences, communication style, tool choices |
| `decision` | Decisions made, rationale, trade-offs |
| `insight` | Learnings, observations, patterns discovered |
| `event` | Things that happened, meetings, incidents |
| `task` | Tasks assigned, in-progress, or completed |

```
memory_search(query="portfolio allocation", memory_type="decision", limit=10)
```

## Search Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `query` | required | Natural language search query |
| `limit` | 5 | Max results to return |
| `memory_type` | None | Filter by type |
| `rerank` | true | Apply Qwen3-VL reranking for better precision |

## Interpreting Results

Each result includes:
- **content**: The stored memory text
- **score**: Embedding cosine similarity (0-1)
- **rerank_score**: Reranker relevance score (when rerank=true)
- **memory_type**: Category of the memory
- **importance**: low / normal / high / critical
- **timestamp**: When the memory was stored
- **tags**: Associated tags

## Recent Memories

To browse chronologically instead of by relevance:

```
memory_recent(limit=10, memory_type="decision")
```

## Tips

- Use natural language queries, not keywords — the embedding model understands semantics
- Enable reranking (default) for precision; disable for speed on large result sets
- Combine with graph search for comprehensive retrieval
- Scores below 0.3 are filtered out automatically
