# FinAI Reference — Patterns to Reuse

> FinAI is Dhruv's working production RAG system (financial domain).
> Path: `/Volumes/Dhruv_SSD/AIwithDhruv/Claude/High Paying Jobs/Acube-AI-Automation/finai/`
> Live: finai.aiwithdhruv.com

## Architecture (Identical Pattern)

```
FinAI Architecture:
  backend/app/
  ├── core/           → config.py, database.py, llm_client.py, logging.py
  ├── pipelines/
  │   ├── ingestion/  → pdf_parser.py, chunker.py, embedder.py, classifier.py, pipeline.py
  │   ├── rag/        → retriever.py, chat.py
  │   └── generation/ → ratios.py, teaser.py, credit_memo.py
  ├── repositories/   → document_repo.py, financial_repo.py, company_repo.py, audit_repo.py, deal_repo.py, material_repo.py, comparable_repo.py
  ├── models/         → Pydantic schemas
  └── utils/          → Shared helpers
```

## What to Reuse (Copy + Adapt)

### 1. core/config.py
- Pydantic BaseSettings pattern
- Env var validation at startup
- **Change:** Add GEMINI_API_KEY, PINECONE_* vars, remove FinAI-specific vars

### 2. core/llm_client.py
- OpenAI AsyncClient wrapper
- **Reuse directly** — same GPT-4o model

### 3. core/database.py
- Supabase connection setup
- **Reuse directly** — same Supabase pattern

### 4. pipelines/ingestion/pdf_parser.py
- PyPDF2 text extraction + table detection
- **Adapt:** Add Gemini native PDF embedding path for ≤6 page docs

### 5. pipelines/ingestion/chunker.py
- RecursiveCharacterTextSplitter with overlap
- **Adapt:** Increase chunk_size from 512 to 1024 (Gemini supports 8K context)

### 6. pipelines/ingestion/embedder.py
- Embedding generation + metadata attachment
- **Major change:** Replace OpenAI embeddings with Gemini Embedding 2
- **Add:** Multimodal support (images, audio, video)

### 7. pipelines/ingestion/classifier.py
- LLM-based document type classification
- **Adapt:** Classify into text/pdf/image/audio/video instead of financial doc types

### 8. pipelines/ingestion/pipeline.py
- End-to-end orchestration: parse → chunk → embed → store
- **Adapt:** Add multimodal routing logic

### 9. pipelines/rag/retriever.py
- Vector similarity search + context assembly
- **Major change:** Replace pgvector queries with Pinecone client
- **Add:** Hybrid search (Pinecone vector + Supabase BM25)

### 10. pipelines/rag/chat.py
- Context assembly + LLM prompt + citation extraction
- **Adapt:** Generic RAG prompt instead of financial-specific

### 11. Repository pattern
- Supabase CRUD via repository classes
- **Adapt:** Different table names (knowledge_documents, knowledge_chunks instead of financial tables)

## Key Differences

| Aspect | FinAI | Multimodal RAG |
|--------|-------|---------------|
| Domain | Financial documents | Any domain (text, images, audio, video) |
| Embedding | OpenAI text-embedding-3-small | Gemini Embedding 2 Preview (multimodal) |
| Vector DB | pgvector (Supabase) | Pinecone (managed) |
| Modalities | Text + PDF only | Text + PDF + Images + Audio + Video |
| Dimensions | 1,536 | 3,072 |
| Context window | 8,191 tokens | 8,192 tokens |
| Generation | Domain-specific (teasers, credit memos) | Generic RAG answers with citations |

## FinAI's CLAUDE.md Rules to Carry Over
- Ratio calculations are CODE, not LLM → **Generalize:** Deterministic operations are code, not LLM
- Source attribution mandatory → Same: every answer cites source
- Human review gate → Same: confidence threshold → escalation
- Audit everything → Same: log prompt, model, sources, output
- No hallucinated numbers → Same: validate LLM output against source data
