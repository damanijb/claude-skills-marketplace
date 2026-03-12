---
name: memory-router
description: "This skill should be used AUTOMATICALLY before any memory retrieval, document lookup, knowledge query, recall, search, or question that might benefit from stored context. Triggers on ANY request where past knowledge, documents, books, preferences, decisions, or facts could be relevant. Acts as the routing layer between samaritan-memory (persistent knowledge) and PageIndex (uploaded documents)."
---

# Memory Router — Automatic Backend Selection

This skill routes queries to the correct memory backend. Apply this decision tree on EVERY query that could benefit from stored knowledge.

## Decision Tree

```
User query arrives
    │
    ├─ References a specific uploaded PDF/document?
    │   └─► PageIndex (get_document_structure → get_page_content)
    │
    ├─ Asks about a recently uploaded file by name?
    │   └─► PageIndex (recent_documents → read)
    │
    ├─ Asks about past decisions, preferences, or events?
    │   └─► samaritan-memory (recall or memory_search)
    │
    ├─ Asks about concepts from the finance book library?
    │   └─► samaritan-memory (memory_search with book content)
    │
    ├─ Asks about entities, relationships, or structured knowledge?
    │   └─► samaritan-memory (graph_search, graph_get_entity, graph_get_facts)
    │
    ├─ Asks a general question that MIGHT have stored context?
    │   └─► samaritan-memory (recall) FIRST, then answer
    │
    ├─ Asks to analyze/summarize a long document (>20 pages)?
    │   └─► PageIndex (structured page-level retrieval)
    │
    └─ No memory relevance detected
        └─► Skip memory lookup, answer directly
```

## When to Use Each

### samaritan-memory (Persistent Knowledge)

The long-term brain. Use for anything that accumulates over time.

| Signal | Action |
|--------|--------|
| "What did we decide about..." | `recall(query="...")` |
| "Remember that..." / "Don't forget..." | `memory_add(content="...")` |
| Any question about Admin preferences | `memory_search(query="...", memory_type="preference")` |
| Questions about finance/quant concepts | `memory_search(query="...")` (hits book chunks) |
| "What's related to X?" | `graph_get_related(entity_name="X")` |
| "What do we know about X?" | `recall(query="X")` (hybrid: vectors + graph) |
| Before making a decision | `recall()` to check for prior context |
| After making a decision | `memory_add()` to record it |

### PageIndex (Uploaded Documents)

The document desk. Use for specific PDFs and reports uploaded for analysis.

| Signal | Action |
|--------|--------|
| User shares/mentions a PDF | `recent_documents()` → `get_page_content()` |
| "What does page 15 say?" | `get_page_content(doc_id, pages="15")` |
| "Summarize this report" | `get_document_structure()` → targeted `get_page_content()` |
| "Find X in the document" | `find_relevant_documents(query="X")` |
| Earnings reports, legal docs, one-off PDFs | PageIndex for ephemeral analysis |

### Both Together

For deep research, use both:

1. `recall("topic")` — get persistent knowledge and past analysis
2. `find_relevant_documents("topic")` — find any uploaded docs on the topic
3. Synthesize both into a comprehensive answer

## Auto-Trigger Rules

Apply this routing BEFORE responding when:

- The user asks a question (not a command) — check `recall()` first
- The user references "last time", "we discussed", "you said" — always `recall()`
- The user mentions a document name — check PageIndex first
- The user asks about finance/markets/portfolio — check both
- The user asks about system architecture or tools — check `graph_search()`

## RECALL→ACT→RECORD

On every significant interaction:

1. **RECALL**: Route to the correct backend(s) and retrieve context
2. **ACT**: Use retrieved context to inform the response
3. **RECORD**: If new knowledge was generated, store via `memory_add()` or `record()`

Skip RECORD for trivial exchanges (greetings, confirmations, simple commands).
