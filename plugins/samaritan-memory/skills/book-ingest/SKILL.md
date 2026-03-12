---
name: book-ingest
description: "This skill should be used when the user asks to \"ingest a book\", \"add a book to memory\", \"process a PDF book\", \"embed a book\", \"add to knowledge base\", \"ingest documents\", or wants to chunk and embed long-form documents (books, papers, reports) into the Qdrant vector store. Also triggers on \"re-ingest books\", \"batch ingest\", or \"update book embeddings\"."
---

# Book Ingestion — Chunk, Embed, & Store

Strategically chunk, embed, and store books and long-form documents into the Qdrant vector store for semantic retrieval. Uses SGLang batch embedding for high throughput.

## Architecture

```
PDF/Text → Chunk (overlap) → Batch Embed (SGLang) → Store (Qdrant)
                                                        ↓
                                              samaritan_memory collection
                                              (2048d cosine, tagged as "book")
```

## Ingestion Script

The batch ingestion script is at `/opt/samaritan/scripts/batch_ingest.py`. It handles:
- PDF text extraction
- Overlapping chunk creation (default: 1000 chars, 200 overlap)
- Batched embedding via SGLang (16 chunks per batch)
- Qdrant upsert with metadata

### Run Ingestion

For a single book:
```bash
python /opt/samaritan/scripts/batch_ingest.py /path/to/book.pdf --tag "finance"
```

For all books in the data directory:
```bash
python /opt/samaritan/scripts/batch_ingest.py /opt/samaritan/data/book_chunks/ --batch-all
```

### Performance

With SGLang serving Qwen3-VL-Embedding-2B on RTX PRO 6000:
- ~132 chunks/second
- 3,606 chunks from 10 finance books in 27 seconds
- Batch size of 16 for optimal GPU utilization

## Knowledge Base

Current library (10 finance/quant books):

| Domain | Books |
|--------|-------|
| Regime Detection | Advances in Markov-Switching Models, Detecting Regime Change in Computational Finance, State-Space Models with Regime Switching |
| Market Microstructure | Trades Quotes and Prices, Dynamic Markov Bridges, Liquidity Trading |
| Trading Strategies | Advances in Financial ML (de Prado), Algorithmic Trading (Chan), Machine Trading (Chan) |
| Risk/Volatility | Market Risk Analysis Vol 2 (Alexander) |

Book chunks are stored at: `/opt/samaritan/data/book_chunks/`

## Adding New Books

To add a new book to the knowledge base:

1. Place the PDF in `/opt/samaritan/data/`
2. Verify SGLang embedding server is running on port 8010
3. Run the ingestion script with appropriate tags
4. Verify with `memory_stats()` — count should increase

## Re-Ingestion

When the embedding model changes (e.g., migrating from Ollama to SGLang), all books must be re-ingested:

1. Delete the old Qdrant collection or create a new one
2. Run batch ingestion on all book chunks
3. Verify vector count matches expected chunks

## Chunking Strategy

- **Chunk size**: 1000 characters (balances context vs. retrieval precision)
- **Overlap**: 200 characters (ensures concepts spanning chunk boundaries are captured)
- **Metadata**: Each chunk stores source book, page number, chunk index, and tags
- **Deduplication**: UUID-based point IDs prevent duplicate vectors
