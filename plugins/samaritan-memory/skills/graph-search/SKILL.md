---
name: graph-search
description: "This skill should be used when the user asks to \"search the graph\", \"find entities\", \"what entities are related to\", \"show relationships\", \"graph query\", \"knowledge graph\", or wants to explore structured relationships between concepts, people, systems, and tools. Also triggers on \"add entity\", \"add relationship\", \"add fact\", \"get facts about\", or any Neo4j knowledge graph operation."
---

# Graph Search — Neo4j Knowledge Graph

Query and manage the Neo4j knowledge graph containing entities, relationships, and facts extracted from memories and manually added knowledge.

## Graph Stats

Current graph: ~8,140 entities, ~21,517 relationships (auto-extracted from memories + book ingestion)

## Search Operations

### Search Entities and Facts

```
graph_search(query="SGLang", search_type="both", limit=10)
```

Returns matching entities and facts. `search_type` options: `"entities"`, `"facts"`, `"both"`.

### Get Entity Details

```
graph_get_entity(name="Qdrant")
```

Returns the entity with all its outgoing relationships.

### Get Facts About a Subject

```
graph_get_facts(subject="fis_gold_extract", limit=20)
```

Returns all subject-predicate-object triples where the entity is the subject.

### Traverse Relationships

```
graph_get_related(entity_name="Damani", relationship=null, depth=2)
```

Find entities within N hops. Optionally filter by relationship type.

## Write Operations

### Add Entity

```
graph_add_entity(
    name="Qwen3-VL-Embedding-2B",
    entity_type="Model",
    properties={"description": "2048d multimodal embedding model", "vendor": "Qwen"}
)
```

Entity types: `Concept`, `Person`, `Strategy`, `Tool`, `Method`, `Event`, `Organization`, `Metric`, `Model`, `Table`, `System`

### Add Relationship

```
graph_add_relationship(
    from_entity="Samaritan",
    to_entity="Qdrant",
    relationship="USES"
)
```

Relationship types: `RELATES_TO`, `USES`, `DEFINES`, `PART_OF`, `CAUSES`, `PRECEDES`, `CONTRADICTS`, `CONTAINS`, `WORKS_AT`

### Add Fact

```
graph_add_fact(
    subject="fis_gold_extract",
    predicate="is",
    object="month-end book of records for portfolio accounting",
    context="Admin clarification"
)
```

## Auto-Extraction

When `memory_add()` is called, the system automatically:
1. Sends the content to an LLM for entity/fact/relationship extraction
2. Adds extracted entities to Neo4j (merged by name to avoid duplicates)
3. Creates relationships and facts between entities

This runs in the background and does not block memory storage.

## Common Queries

| Intent | Tool Call |
|--------|-----------|
| "What do we know about X?" | `graph_get_entity(name="X")` + `graph_get_facts(subject="X")` |
| "How is X related to Y?" | `graph_get_related(entity_name="X", depth=2)` |
| "Find all tools we use" | `graph_search(query="tool", search_type="entities")` |
| "What facts about the portfolio?" | `graph_get_facts(subject="Portfolio Database")` |
