---
name: memory-recall
description: "This skill should be used when the user asks to \"recall\", \"remember\", \"what do you know about\", \"check memory\", \"look up in memory\", or wants to retrieve context from past conversations, decisions, or stored knowledge. Also triggers on \"hybrid search\", \"search memory and graph\", or any request combining semantic and graph recall."
---

# Memory Recall — Hybrid Retrieval

Perform hybrid recall across both semantic vector memory (Qdrant) and the knowledge graph (Neo4j) to retrieve the most relevant context for a query.

## When to Use

- Before answering questions that may have been discussed previously
- When the user references past decisions, preferences, or events
- When context from prior conversations would improve the response
- As the first step in the RECALL→ACT→RECORD loop

## Workflow

### 1. Hybrid Recall

Use the `recall` MCP tool for combined semantic + graph search:

```
recall(query="<user's question or topic>", limit=5)
```

This returns three result sets:
- **memories**: Semantic matches from Qdrant (scored by embedding similarity + reranking)
- **entities**: Matching entities from Neo4j graph
- **facts**: Subject-predicate-object triples from the graph

### 2. Evaluate Results

Assess the quality of returned results:
- **High confidence** (rerank_score > 0.6): Use directly in response
- **Medium confidence** (0.4-0.6): Cross-reference with graph results
- **Low confidence** (< 0.4): Mention uncertainty, consider falling back to general knowledge

### 3. Synthesize Response

Combine vector memory (what was said/decided) with graph knowledge (structured relationships) to form a complete answer. Prioritize:
1. Direct memory matches (explicit stored content)
2. Graph entity relationships (structured connections)
3. Graph facts (subject-predicate-object triples)

## Targeted Recall

For more specific retrieval, use individual tools:

- **Semantic only**: `memory_search(query="...", limit=5, rerank=true)`
- **Graph entities only**: `graph_search(query="...", search_type="entities")`
- **Graph facts only**: `graph_search(query="...", search_type="facts")`
- **Entity relationships**: `graph_get_related(entity_name="...", depth=2)`

## Best Practices

- Always recall before answering from training data when the question could involve stored context
- Use specific queries — "Damani's preference for report formatting" retrieves better than "preferences"
- Chain recalls: start broad, then narrow based on initial results
- If recall returns nothing relevant, state that clearly rather than guessing
