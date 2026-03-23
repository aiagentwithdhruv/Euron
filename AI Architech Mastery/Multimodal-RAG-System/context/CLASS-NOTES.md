# Euron AI Architect Mastery — Class Notes

## Class 3 (Mar 14, 2026) — RAG Architecture & Google Gemini Embedding 2

### What is RAG?
- LLMs have a knowledge cutoff — they don't know YOUR data
- RAG = retrieve relevant context from YOUR documents at query time, inject into prompt
- Instead of fine-tuning (expensive, slow, stale), you retrieve + generate on the fly
- The LLM generates answers grounded in your actual data with source attribution

### RAG Pipeline (Production)
```
INGESTION (offline):
  Documents → Parse → Chunk (512-1024 tokens, 200 overlap)
      → Embed (Gemini Embedding 2) → Store in Pinecone

RETRIEVAL (real-time):
  Query → Embed (RETRIEVAL_QUERY) → Vector search (top_k=10)
      → Hybrid merge (vector + BM25) → Rerank → Top 3-5
      → Context assembly → GPT-4o → Cited answer
```

### Key Decisions
| Decision | Choice | Why |
|----------|--------|-----|
| Chunk size | 1024 tokens | Larger OK with 8K context embeddings |
| Overlap | 200 tokens | Prevent info loss at boundaries |
| Retrieval | Hybrid (0.6 vector + 0.4 BM25) | BM25 catches exact keywords vectors miss |
| Reranker | Cohere Rerank | Precision boost after broad retrieval |
| top_k | 10 → rerank to 3-5 | Wide retrieval, precise final set |

### Google Gemini Embedding 2 (Released March 10, 2026)

**Model:** `gemini-embedding-2-preview`
**Breakthrough:** First natively multimodal embedding model — text, images, audio, video, PDF in ONE vector space.

| Feature | Old Models | Gemini Embedding 2 |
|---------|-----------|-------------------|
| Modalities | Text only | Text + Images + Video + Audio + PDF |
| Context | 2,048 tokens | 8,192 tokens (4x) |
| Dimensions | Fixed | 128 to 3,072 (MRL — truncate without retraining) |
| Cross-modal | Impossible | Native — query text, get images/video/audio |

**Pricing:**
| Model | $/1M tokens | Multimodal |
|-------|------------|-----------|
| Mistral Embed | $0.01 | No |
| text-embedding-3-small (OpenAI) | $0.02 | No |
| Gemini Embedding 001 | Free tier | No |
| text-embedding-3-large (OpenAI) | $0.13 | No |
| **Gemini Embedding 2** | **$0.20** | **Yes** |

**MTEB Leaderboard (text-only):**
| Model | Score | Type |
|-------|-------|------|
| NV-Embed-v2 (NVIDIA) | 72.31 | Open-source |
| Qwen3-Embedding-8B | 70.58 | Open-source |
| Gemini Embedding 001 | 68.32 | Commercial API |
| text-embedding-3-large | 64.6 | OpenAI |

### Best Practices
1. **Always use task_type** — `RETRIEVAL_DOCUMENT` for indexing, `RETRIEVAL_QUERY` for searching
2. **Hybrid search > pure vector** — BM25 catches exact keyword matches
3. **Rerank after retrieval** — 10 candidates → rerank to top 3-5
4. **Chunk with overlap** — 200-token overlap
5. **Store metadata** — source, page, section, timestamp, modality
6. **Evaluate with RAGAS** — faithfulness, relevancy, precision, recall
7. **Larger chunks OK** — with 8K context embeddings, use 1024+ tokens
