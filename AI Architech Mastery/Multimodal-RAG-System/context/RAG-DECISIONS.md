# RAG Architecture Decisions

> Why we chose what we chose. Reference for future changes.

## Decision 1: Gemini Embedding 2 Preview (NOT OpenAI)

**Choice:** `gemini-embedding-2-preview`
**Alternatives considered:** text-embedding-3-large (OpenAI), NV-Embed-v2 (NVIDIA), Cohere Embed v4

**Why Gemini:**
- Only natively multimodal embedding model available (March 2026)
- Text + Images + Audio + Video + PDF in one vector space
- No need for separate CLIP model for images or Whisper for audio
- 8,192 token context (matches OpenAI)
- MRL: flexible dimensions 128-3,072

**Trade-off:** $0.20/MTok vs $0.02 (OpenAI small). Premium justified by multimodal capability.

## Decision 2: Pinecone (NOT pgvector)

**Choice:** Pinecone Serverless
**Alternatives considered:** pgvector (Supabase), Qdrant, Weaviate, FAISS

**Why Pinecone:**
- Managed — zero ops overhead
- Serverless scaling — pay per query, not per server
- Native metadata filtering (tenant_id isolation)
- Supports 3,072 dimensions (Gemini Embedding 2 output)
- Connection string provided by Dhruv

**Trade-off:** Cost ($0.0025/1K queries) vs pgvector (free with Supabase). Worth it for scale + management.

**pgvector role:** Used ONLY for BM25 keyword search (hybrid retrieval complement), NOT for vector search.

## Decision 3: OpenAI GPT-4o (NOT Claude, NOT Gemini for generation)

**Choice:** GPT-4o (latest)
**Alternatives considered:** Claude 4.5 Sonnet, Gemini 2.5 Pro

**Why GPT-4o:**
- Best structured output (JSON mode, function calling)
- Proven RAG answer quality with citations
- Wide LangChain/LangGraph integration
- Cost-effective with GPT-4o-mini for classification tasks

## Decision 4: Hybrid Search (Vector + BM25)

**Choice:** 0.6 vector (Pinecone) + 0.4 keyword (BM25 on Supabase)
**Alternative:** Pure vector search

**Why hybrid:**
- BM25 catches exact keyword/entity matches that embeddings miss
- "Policy #12345" or "Section 4.2.1" are better with keyword search
- 10-15% improvement in retrieval quality per benchmarks

## Decision 5: Cohere Rerank

**Choice:** Cohere Rerank API
**Alternatives:** Cross-encoder (local), no reranking

**Why:**
- Retrieve 10 broad candidates → rerank to precise top 3-5
- 5-10% answer quality improvement
- API-based — no GPU needed
- $1/1K queries — cheap for the quality boost

## Decision 6: Chunk Size 1024 + Overlap 200

**Choice:** 1024 token chunks, 200 token overlap
**Alternatives:** 512 chunks (traditional), 256 chunks (fine-grained)

**Why 1024:**
- Gemini Embedding 2 supports 8,192 token context — can handle larger chunks
- Larger chunks = more coherent context = better answers
- Fewer chunks = cheaper Pinecone storage
- 200 overlap = no information lost at boundaries
