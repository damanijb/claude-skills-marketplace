---
name: memory-stats
description: "This skill should be used when the user asks for \"memory stats\", \"memory status\", \"how many memories\", \"system health\", \"memory count\", or wants to check the health and statistics of the memory system. Also triggers on \"is memory working\", \"check qdrant\", \"check neo4j\", \"vector count\", or any diagnostics request for the memory infrastructure."
---

# Memory Stats — System Health & Diagnostics

Check the health and statistics of the hybrid memory system including Qdrant vectors, Neo4j graph, and SGLang embedding servers.

## Quick Status Check

```
memory_stats()
```

Returns:
- **qdrant**: `{count: N, status: "green"}` — vector count and collection health
- **neo4j**: `{entities: N, facts: N, relationships: N}` — graph statistics

## Interpreting Results

### Qdrant Health

| Status | Meaning |
|--------|---------|
| `green` | Collection healthy, all points indexed |
| `yellow` | Indexing in progress (normal after bulk ingest) |
| `red` | Collection error — investigate |
| `not_initialized` | Collection doesn't exist — needs creation |

**Expected counts**:
- ~3,600 book chunks (from 10 finance books)
- Growing count of conversation memories
- `indexed_vectors_count: 0` is normal below 10k points (uses brute-force, not HNSW)

### Neo4j Health

| Metric | Expected Range |
|--------|---------------|
| entities | ~8,000+ (auto-extracted + manual) |
| facts | ~5,000+ (subject-predicate-object triples) |
| relationships | ~21,000+ (entity connections) |

## Infrastructure Dependencies

The memory system requires these services:

| Service | Port | Purpose |
|---------|------|---------|
| Qdrant | 6333 | Vector database |
| SGLang Embedding | 8010 | Qwen3-VL-Embedding-2B (2048d) |
| SGLang Reranker | 8011 | Qwen3-VL-Reranker-2B |
| Neo4j | 7687 | Knowledge graph (bolt protocol) |
| Memory MCP | 8020 | MCP server (streamable HTTP) |

### Systemd Services

```bash
# Check service status
sudo systemctl status sglang-memory.service    # SGLang embedding + reranker
sudo systemctl status memory-mcp.service       # MCP server

# Restart if needed
sudo systemctl restart sglang-memory.service
sudo systemctl restart memory-mcp.service
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| memory_stats returns error | MCP server down | `sudo systemctl restart memory-mcp.service` |
| count: 0 | Collection empty or wrong collection | Check `QDRANT_COLLECTION` env var |
| Neo4j error | Neo4j service down | `sudo systemctl restart neo4j` |
| Search returns no results | SGLang embedding server down | Check port 8010, restart sglang-memory |
| Low search scores | Embedding model mismatch | Verify model matches ingested vectors |
| Reranking not improving results | Reranker server down | Check port 8011 |

## GPU Memory Usage

SGLang servers on RTX PRO 6000 (98GB VRAM):
- Embedding server: ~30GB (`--mem-fraction-static 0.3`)
- Reranker server: ~15GB (`--mem-fraction-static 0.15`)
- Total: ~43GB reserved for memory system
