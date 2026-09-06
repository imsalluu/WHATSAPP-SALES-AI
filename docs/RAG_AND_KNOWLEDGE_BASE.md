# RAG Knowledge Base & pgvector Integration

## 1. Pipeline Overview

The RAG (Retrieval-Augmented Generation) pipeline enables businesses to upload company knowledge (shipping policies, return guidelines, FAQs, brand philosophy, technical manuals) and guarantees grounded, truthful answers.

```mermaid
flowchart LR
    Doc[PDF / Markdown / FAQ Upload] --> Extractor[Text & Metadata Extraction]
    Extractor --> Chunker[Recursive Chunker (500 tokens, 100 overlap)]
    Chunker --> Embedder[Embedding Generator (1536-dim)]
    Embedder --> PGVector[(PostgreSQL pgvector)]
    
    Query[Customer Query] --> QueryEmbed[Embed Query]
    QueryEmbed --> VectorSearch[Cosine Similarity <=> Distance]
    VectorSearch --> Reranker[Relevance Filter]
    Reranker --> LLMContext[Grounded Prompt Context]
```

---

## 2. Chunking & Storage Specification
- **Chunk Size**: 500 characters with 100 character sliding overlap.
- **Vector Distance Metric**: Cosine Distance (`vector_cosine_ops` / `<=>`).
- **Hybrid Retrieval**: Combines semantic embeddings with Postgres Full-Text Search (`tsvector`) for precision on product codes and specific keywords.
