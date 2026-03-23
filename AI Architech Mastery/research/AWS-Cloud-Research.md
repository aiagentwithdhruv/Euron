# Amazon Web Services (AWS) for AI/ML Projects -- Exhaustive Reference

> **Last updated:** March 2026
> **Scope:** Everything a 10-year AWS veteran knows -- pricing, architecture, CLI, trade-offs, free tier, and cross-cloud comparisons.
> **Pricing note:** All prices are USD unless stated otherwise. Prices reflect published rates as of early 2026 (US East / N. Virginia region unless noted). AWS pricing changes; always verify at aws.amazon.com/pricing before committing spend.

---

## Table of Contents

1. [AI/ML Services (Deep Dive)](#1-aiml-services-deep-dive)
2. [Compute & Deployment](#2-compute--deployment)
3. [Storage & Databases](#3-storage--databases)
4. [Networking & CDN](#4-networking--cdn)
5. [Serverless & Event-Driven](#5-serverless--event-driven)
6. [Security & IAM](#6-security--iam)
7. [CI/CD & DevOps](#7-cicd--devops)
8. [Monitoring & Observability](#8-monitoring--observability)
9. [Free Tier (Complete List)](#9-free-tier-complete-list)
10. [Pricing Comparisons vs GCP and Azure](#10-pricing-comparisons-vs-gcp-and-azure)
11. [Architecture Patterns for AI Projects](#11-architecture-patterns-for-ai-projects)
12. [AWS CLI Commands Reference](#12-aws-cli-commands-reference)
13. [When to Choose AWS Over GCP/Azure](#13-when-to-choose-aws-over-gcpazure)
14. [Quick Start Templates](#14-quick-start-templates)

---

## 1. AI/ML Services (Deep Dive)

### 1.1 Amazon Bedrock -- The Managed Foundation Model Platform

Amazon Bedrock is AWS's fully managed service for accessing foundation models from multiple providers through a single API. Unlike SageMaker (which requires managing infrastructure), Bedrock is serverless -- you pay per token, never manage endpoints.

**Core Components:**

| Component | What It Does | GCP Equivalent | Azure Equivalent |
|-----------|-------------|----------------|-----------------|
| Model Access | Unified API for Claude, Nova, Llama, Mistral, Cohere, Titan | Vertex AI Model Garden | Azure OpenAI + AI Foundry Model Catalog |
| Knowledge Bases | Managed RAG pipeline (ingest + embed + retrieve + generate) | Vertex AI RAG Engine | Azure AI Search + OpenAI (manual wiring) |
| Agents | Autonomous agents with tools, KB access, code execution | Vertex AI Agent Builder | Azure AI Agents |
| Guardrails | Content filtering, PII, grounding checks on inputs/outputs | Vertex AI Safety | Azure AI Content Safety |
| Fine-Tuning | Custom model training on your data | Vertex AI Tuning | Azure OpenAI Fine-Tuning |
| Model Evaluation | Compare models on your data with built-in metrics | Vertex AI Evaluations | Azure AI Foundry Evaluations |
| Prompt Management | Version, test, and manage prompts | -- | Azure Prompt Flow |
| Intelligent Prompt Routing | Auto-route to cheap or smart model based on complexity | -- | -- |
| Batch Inference | Process large datasets at 50% discount (24hr turnaround) | Vertex AI Batch Prediction | Azure OpenAI Global Batch |

---

### 1.2 Bedrock Foundation Models -- Complete Pricing (Per 1M Tokens)

**Anthropic Claude Models:**

| Model | Input | Output | Cached Input | Context | Best For |
|-------|-------|--------|-------------|---------|----------|
| **Claude Opus 4.6** | $15.00 | $75.00 | $3.75 | 200K | Most complex reasoning, multi-step coding |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | $0.75 | 200K | Production workhorse, computer use, coding |
| **Claude Haiku 4.5** | $0.80 | $4.00 | $0.20 | 200K | Cost-efficient high-volume, agents |
| **Claude 3.5 Sonnet v2** | $3.00 | $15.00 | $0.75 | 200K | Proven production model |
| **Claude 3.5 Haiku** | $0.80 | $4.00 | — | 200K | Budget chatbots, classification |
| **Claude 3 Haiku** | $0.25 | $1.25 | — | 200K | Cheapest Claude, simple tasks |
| **Claude 3 Opus** | $15.00 | $75.00 | — | 200K | Legacy high-accuracy |

**Amazon Nova Models (AWS-native):**

| Model | Input | Output | Context | Best For |
|-------|-------|--------|---------|----------|
| **Nova Premier** | $2.50 | $12.50 | 1M | Most capable Nova, complex reasoning |
| **Nova Pro** | $0.80 | $3.20 | 300K | General purpose, multimodal |
| **Nova Lite** | $0.06 | $0.24 | 300K | Budget multimodal (text + image + video) |
| **Nova Micro** | $0.035 | $0.14 | 128K | Absolute cheapest text-only on AWS |
| **Nova Canvas** | — | $0.04/image (512x) to $0.08/image (2048x) | — | Image generation |
| **Nova Reel** | — | $0.08/second of video | — | Video generation |

**Meta Llama Models:**

| Model | Input | Output | Context | Best For |
|-------|-------|--------|---------|----------|
| **Llama 4 Maverick** | $0.20 | $0.60 | 1M | Open-weight frontier, multimodal |
| **Llama 4 Scout** | $0.15 | $0.45 | 10M | Ultra-long context (10M tokens!) |
| **Llama 3.3 70B** | $0.72 | $0.72 | 128K | Best open-weight quality/cost |
| **Llama 3.1 405B** | $2.40 | $3.20 | 128K | Largest open model on Bedrock |
| **Llama 3.1 70B** | $0.72 | $0.72 | 128K | Production open-weight |
| **Llama 3.1 8B** | $0.22 | $0.22 | 128K | Budget open model |

**Mistral Models:**

| Model | Input | Output | Context | Best For |
|-------|-------|--------|---------|----------|
| **Mistral Large 2** | $2.00 | $6.00 | 128K | Multilingual reasoning, code |
| **Mistral Small** | $0.10 | $0.30 | 32K | Budget European model |
| **Mixtral 8x7B** | $0.45 | $0.70 | 32K | MoE architecture, good throughput |

**Cohere Models:**

| Model | Input | Output | Context | Best For |
|-------|-------|--------|---------|----------|
| **Command R+** | $2.50 | $10.00 | 128K | RAG-optimized, grounded generation |
| **Command R** | $0.50 | $1.50 | 128K | Budget RAG |
| **Command Light** | $0.30 | $0.60 | 4K | Cheapest Cohere |

**AI21 Labs:**

| Model | Input | Output | Context | Best For |
|-------|-------|--------|---------|----------|
| **Jamba 1.5 Large** | $2.00 | $8.00 | 256K | Long-context, SSM architecture |
| **Jamba 1.5 Mini** | $0.20 | $0.40 | 256K | Budget long-context |

**Stability AI:**

| Model | Price | Best For |
|-------|-------|----------|
| SDXL 1.0 | $0.04/image (1024x) | Image generation |
| Stable Image Core | $0.04/image | Quality image gen |
| Stable Image Ultra | $0.08/image | Highest quality |

**Batch Inference:** All models support batch pricing at 50% of on-demand. Process within 24 hours. Ideal for embeddings at ingestion time, bulk classification, document summarization.

---

### 1.3 Embedding Models on Bedrock

| Model | Dimensions | Max Tokens | Price (per 1M tokens) | MRL | Best For |
|-------|-----------|-----------|----------------------|-----|----------|
| **Titan Text Embeddings V2** | 256, 512, 1024 | 8,192 | $0.02 (on-demand), $0.01 (batch) | Yes | English-primary, cheapest AWS option |
| **Titan Multimodal Embeddings** | 256, 384, 1024 | 128 tokens text + images | $0.06 per image, $0.02 per 1K text tokens | No | Text + image in same space |
| **Cohere Embed v3 (English)** | 1024 | 512 | $0.10 | No | Best semantic quality |
| **Cohere Embed v3 (Multilingual)** | 1024 | 512 | $0.10 | No | 100+ languages |

**Reranking Models (Cross-Encoders):**

| Model | Price | Notes |
|-------|-------|-------|
| **Cohere Rerank 3.5** | $1.00 / 1K queries | Up to 100 chunks per query, best quality |
| **Amazon Rerank v1.0** | $1.00 / 1K queries | AWS-native, us-east-1, us-west-2, eu-west-1 |

**MRL (Matryoshka Representation Learning) on Titan V2:** Use 256 dims to save 75% vector storage with only ~3% accuracy loss vs 1024 dims. Critical cost optimization for production RAG.

**Which embedding to use:**

| Use Case | Model | Why |
|----------|-------|-----|
| Text-only RAG (English) | Titan V2 (1024 dims) | Cheapest ($0.02/1M), good quality |
| Text-only RAG (multilingual) | Cohere Embed v3 Multilingual | 100+ languages, superior quality |
| Cost-sensitive high-volume | Titan V2 (256 dims + batch) | $0.01/1M + 75% less storage |
| Highest quality retrieval | Cohere Embed v3 English | Best MTEB scores on Bedrock |
| Multimodal (text + images) | Titan Multimodal | Only multimodal option on Bedrock |

**Cross-cloud comparison:**
- Titan V2 ($0.02/1M) vs GCP Gemini Embedding 2 ($0.20/1M) vs Azure text-embedding-3-small ($0.02/1M)
- AWS wins on embedding cost. GCP wins on multimodal embedding quality. Azure matches AWS on text.

---

### 1.4 Bedrock Knowledge Bases -- Managed RAG

The fastest path from documents to RAG on AWS. Connect data sources, configure chunking, select models, and get a working RAG pipeline without writing retrieval code.

**End-to-End Flow:**
1. Connect data sources: S3, Confluence, SharePoint, Salesforce, Web Crawler
2. Configure chunking strategy (fixed, semantic, hierarchical, or custom Lambda)
3. Select embedding model (Titan V2 or Cohere Embed v3)
4. Select vector store (OpenSearch Serverless by default)
5. Sync triggers ingestion pipeline
6. Query via `RetrieveAndGenerate` (one-call RAG) or `Retrieve` (retrieval only)

**Chunking Strategies:**

| Strategy | Best For | Config |
|----------|---------|--------|
| Fixed | General docs | 300-1024 tokens, configurable overlap |
| Semantic | Dense technical docs | Groups by embedding similarity threshold |
| Hierarchical | Legal docs, manuals, contracts | Parent: 1500t, Child: 300-512t |
| Custom Lambda | Proprietary formats | Your Lambda handles chunking |

**Metadata Filtering (RBAC):**

```python
# Users only see their department's documents
filter={
    "andAll": [
        {"equals": {"key": "department", "value": user_dept}},
        {"in": {"key": "clearance_level", "value": user_clearance_levels}}
    ]
}
```

Works with `.metadata.json` sidecar files in S3. Multi-tenant from a single knowledge base.

**Supported Vector Stores:**
- Amazon OpenSearch Serverless (default)
- Amazon Aurora PostgreSQL (pgvector)
- Amazon Neptune Analytics (GraphRAG)
- Amazon MemoryDB (Redis)
- Pinecone (third-party)
- MongoDB Atlas (third-party)

**Limitations vs Custom RAG:**

| Feature | Bedrock KB | Custom RAG |
|---------|-----------|-----------|
| Setup time | Hours | Days |
| Streaming responses | No (returns full) | Yes (SSE) |
| Hybrid search | Yes (OpenSearch) | Full control |
| Custom chunking | Lambda only | Any code |
| Reranking | Built-in (limited) | Full control |
| Cost at scale | Higher overhead | Lower with tuning |
| Multi-model routing | No | Yes |

**When to use Bedrock KB vs DIY:**
- **Bedrock KB:** Prototyping, <100K documents, non-technical team, speed to market
- **DIY (LangChain/LlamaIndex + Fargate/Lambda):** Full control, custom reranking, cost optimization, streaming, production at scale

---

### 1.5 Bedrock Agents

Autonomous AI agents that can reason, plan, use tools, access knowledge bases, and execute code.

**Core Components:**

| Component | Purpose |
|-----------|---------|
| Foundation Model | Reasoning engine (Claude Sonnet 4.6 recommended) |
| Knowledge Bases | Agent decides when to query RAG |
| Action Groups | Lambda functions with OpenAPI schema for deterministic ops |
| Guardrails | Content filtering on inputs and outputs |
| Memory | Built-in session history (episodic + semantic) |
| Code Interpreter | Sandboxed Python execution for data analysis |

**Multi-Agent Collaboration (GA March 2025):**
- **Supervisor mode:** Supervisor breaks tasks, delegates to specialist sub-agents, synthesizes results
- **Supervisor + routing mode:** Simple requests go directly to a sub-agent (fast); complex requests get full orchestration

**Bedrock AgentCore (GA October 2025):**

Production runtime for agents with enterprise features:

| Feature | Details |
|---------|---------|
| Runtime | Serverless, per-session microVM, 8-hour execution windows |
| Session Isolation | Dedicated CPU/memory/filesystem per user session |
| Memory | Episodic + semantic, self-managed extraction pipelines |
| Gateway | Auto-converts APIs + Lambda into MCP tools |
| Browser | Secure browser runtime for web workflows |
| Code Interpreter | Sandboxed Python execution |
| Policy | Intercept + govern tool calls before execution |
| Protocol | A2A (Agent-to-Agent) support, bidirectional streaming |

**Pricing:** Bedrock Agents themselves are free. You pay for underlying model invocations, KB queries, Lambda executions, and compute.

---

### 1.6 Bedrock Guardrails

Content safety layer that wraps any Bedrock model invocation.

| Filter | What It Blocks | Use Case |
|--------|---------------|----------|
| **Content filters** | Hate, violence, sexual, insults, misconduct, prompt attacks | Block adversarial inputs |
| **Denied topics** | Custom topic blocks you define | "Don't discuss competitor products" |
| **Word filters** | Profanity, custom words/phrases | Industry-specific terms |
| **PII detection** | SSN, DOB, email, phone, address (25+ types) | REDACT or BLOCK sensitive data |
| **Contextual grounding** | Hallucinations, ungrounded responses | Critical for legal/medical/financial |
| **Code security** | Malicious code injection | For code-generation use cases |

**Pricing:**
- Text: $0.75 per 1,000 text units (1 unit = 1,000 characters)
- Image: $1.00 per image
- Grounding check: $0.10 per 1,000 text units (additional)

**Unique to AWS:** Guardrails work across ALL Bedrock models (Claude, Nova, Llama, etc.) -- a single guardrail config applies regardless of model. Azure's content filtering is OpenAI-only. GCP's safety settings are model-specific.

---

### 1.7 Amazon SageMaker AI

Full MLOps platform for custom model training, deployment, and management. Use SageMaker when you need to train your own models or deploy models not available on Bedrock.

**Core Components:**

| Component | What It Does | Bedrock Equivalent |
|-----------|-------------|-------------------|
| Studio | IDE (Jupyter, VS Code) for ML development | — |
| Training Jobs | Managed distributed training | Bedrock Fine-Tuning (limited) |
| Endpoints | Real-time model hosting | Bedrock model invocation |
| Serverless Inference | Auto-scaling, pay-per-use endpoints | Bedrock (always serverless) |
| Batch Transform | Offline batch inference | Bedrock Batch |
| Pipelines | ML workflow orchestration | — |
| Feature Store | Centralized feature management | — |
| Model Registry | Version and manage models | — |
| Model Monitor | Detect data/model drift | — |
| JumpStart | 600+ pre-trained models | Bedrock Model Catalog |
| Canvas | No-code ML (visual) | — |
| HyperPod | Managed GPU cluster for LLM training | — |

**Key Instance Pricing (US East):**

| Instance | vCPUs | RAM | GPU | On-Demand/hr | Use Case |
|----------|-------|-----|-----|-------------|----------|
| ml.t3.medium | 2 | 4 GB | — | $0.05 | Dev notebooks |
| ml.m5.xlarge | 4 | 16 GB | — | $0.23 | Small training/inference |
| ml.m5.4xlarge | 16 | 64 GB | — | $0.92 | Medium training |
| ml.g5.xlarge | 4 | 16 GB | 1x A10G (24GB) | $1.41 | GPU inference |
| ml.g5.2xlarge | 8 | 32 GB | 1x A10G (24GB) | $1.52 | GPU inference |
| ml.g5.12xlarge | 48 | 192 GB | 4x A10G (96GB) | $7.09 | Multi-GPU inference |
| ml.p4d.24xlarge | 96 | 1152 GB | 8x A100 (320GB) | $37.69 | Large model training |
| ml.p5.48xlarge | 192 | 2048 GB | 8x H100 (640GB) | $65.88 | Frontier model training |
| ml.inf2.xlarge | 4 | 16 GB | 1x Inferentia2 | $0.76 | Cost-efficient inference |

**SageMaker costs 20-40% more than equivalent EC2 instances** because it includes managed infrastructure, auto-scaling, and monitoring. For pure training, EC2 with Spot can be cheaper.

**When to use SageMaker vs Bedrock:**

| Criteria | Use Bedrock | Use SageMaker |
|----------|------------|---------------|
| Pre-trained models | Yes | No (use Bedrock) |
| Custom model training | No | Yes |
| Fine-tuning (supported models) | Yes (simpler) | Yes (full control) |
| MLOps pipeline | No | Yes |
| Model monitoring | No | Yes |
| Serverless | Always | Optional |
| GPU management | Never | Required |
| Cost for inference | Per-token | Per-hour (even idle) |

**Veteran tip:** Most teams should start with Bedrock. Move to SageMaker only when you need custom training, specific model architectures, or fine-grained control over inference infrastructure. The operational overhead of SageMaker is significant.

---

### 1.8 Amazon Textract

Document intelligence service for extracting text, tables, forms, and queries from scanned documents and PDFs.

**Pricing (per page):**

| API | First 1M Pages | After 1M Pages |
|-----|----------------|----------------|
| DetectDocumentText (OCR) | $0.0015 | $0.0006 |
| AnalyzeDocument -- Tables | $0.015 | $0.010 |
| AnalyzeDocument -- Forms (K-V pairs) | $0.050 | $0.040 |
| AnalyzeDocument -- Queries (custom extraction) | $0.065 | $0.050 |
| AnalyzeDocument -- Signatures | $0.015 | $0.010 |
| AnalyzeExpense (receipts/invoices) | $0.01 | $0.008 |
| AnalyzeID (identity docs) | $0.10 | $0.10 |
| AnalyzeLending (mortgage docs) | $0.01 | $0.008 |

**Key patterns:**
- Use async `StartDocumentAnalysis` + SNS notification for large PDFs (>5 pages)
- Sync API for single pages in real-time upload flows
- Tables API is critical for contracts with structured clauses

**Cross-cloud comparison:**
- Textract OCR ($0.0015/page) vs GCP Document AI OCR ($0.01/page, but includes layout) vs Azure Document Intelligence Read ($0.001/page)
- Azure wins on pure OCR pricing. Textract wins on form extraction value. GCP wins on layout understanding.

---

### 1.9 Amazon Comprehend

NLP service for entity extraction, sentiment analysis, key phrase extraction, and language detection.

**Pricing (per 100-character unit):**

| Feature | Price per Unit | Free Tier |
|---------|---------------|-----------|
| Entity detection | $0.0001 | 50K units/month (12 months) |
| Sentiment analysis | $0.0001 | 50K units/month (12 months) |
| Key phrase extraction | $0.0001 | 50K units/month (12 months) |
| Language detection | $0.0001 | 50K units/month (12 months) |
| Syntax analysis | $0.00005 | 50K units/month (12 months) |
| PII detection | $0.0001 | — |
| Custom classification | $3.00/hr (training) + $0.0005/unit (inference) | — |
| Custom entity recognition | $3.00/hr (training) + $0.0005/unit (inference) | — |

**RAG use:** Tag chunks with entities (PERSON, ORGANIZATION, DATE, LOCATION) at ingestion time. Filter retrieved chunks by entity type at query time. Adds 30-40% relevancy improvement for entity-heavy domains.

**Veteran insight:** For most NLP tasks, calling Claude 3 Haiku ($0.25/1M tokens) or Nova Micro ($0.035/1M tokens) with a prompt is now cheaper AND more accurate than Comprehend for batch processing. Comprehend is best for streaming/real-time NLP where you need deterministic, structured output without LLM latency.

---

### 1.10 Amazon Transcribe (Speech-to-Text)

**Pricing:**

| Feature | Price (per minute) | Free Tier |
|---------|-------------------|-----------|
| Standard transcription | $0.024 | 60 min/month (12 months) |
| Medical transcription | $0.075 | — |
| Call Analytics | $0.040 | — |
| Streaming (real-time) | $0.024 | — |
| Toxicity detection | $0.020 (on top) | — |

**Key features:**
- Real-time streaming transcription
- Speaker diarization (who said what)
- Custom vocabulary for domain-specific terms
- Automatic language identification (supports 104 languages)
- Call Analytics: sentiment, issues, silence detection for contact centers
- Subtitles: WebVTT and SRT output formats

**Cross-cloud comparison:**
- Transcribe ($0.024/min) vs GCP Chirp 2 ($0.016/min) vs Azure STT ($0.017/min real-time, $0.006/min batch)
- GCP is cheapest for standard STT. Azure wins on batch STT pricing. AWS Transcribe has superior call analytics features.

---

### 1.11 Amazon Polly (Text-to-Speech)

**Pricing (per 1M characters):**

| Voice Type | Price | Free Tier |
|-----------|-------|-----------|
| Standard | $4.00 | 5M chars/month (12 months) |
| Neural | $16.00 | 1M chars/month (12 months) |
| Long-form Neural | $100.00 | — |
| Generative | $30.00 | — |
| Brand Voice | Custom pricing | — |

- 60+ voices across 30+ languages
- SSML support for pronunciation control
- Speech marks for lip-sync animation
- Neural voices: significantly more natural than standard

**Cross-cloud comparison:** AWS Neural ($16/1M) = GCP WaveNet/Neural2 ($16/1M) = Azure Neural ($16/1M). Pricing is identical across all three clouds. AWS wins on number of standard voices; GCP wins on neural voice variety (380+ voices).

---

### 1.12 Amazon Rekognition (Vision AI)

**Pricing (per 1K images):**

| Feature | First 1M images/mo | 1-10M | 10M+ |
|---------|-------------------|-------|------|
| Label detection | $1.00 | $0.80 | $0.60 |
| Face detection | $1.00 | $0.80 | $0.60 |
| Text in image (OCR) | $1.00 | $0.80 | $0.60 |
| Face comparison | $1.00 | $0.80 | $0.60 |
| Content moderation | $1.00 | $0.80 | $0.60 |
| Celebrity recognition | $1.00 | $0.80 | $0.60 |
| Custom Labels (your categories) | $4.00/hr (training) + $4.00/hr (inference) | — | — |
| Video analysis | $0.10/min | $0.08/min | $0.06/min |

**Free tier:** 5,000 images/month (12 months) for image analysis; 1,000 face metadata stores.

---

### 1.13 Amazon Kendra (Enterprise Search)

Managed enterprise search with native connectors to 50+ data sources (S3, SharePoint, Confluence, Salesforce, databases, web crawlers).

**Pricing:**

| Edition | Monthly Base | Document Storage | Queries |
|---------|-------------|-----------------|---------|
| Developer | $810/month | Up to 10K docs | Up to 4K queries/day |
| Enterprise | $1,008/month per index unit | $0.005/doc | $0.0004/query |

**Features:** BM25 + semantic ranking, FAQ extraction, document enrichment, access control, multilingual.

**When to use Kendra vs Bedrock Knowledge Bases:**
- **Kendra:** Enterprise search with pre-built connectors (SharePoint, Confluence), non-technical teams
- **Bedrock KB:** RAG-focused, LLM-powered answers, developer-built pipelines
- **Neither (DIY):** Full control, custom ranking, cost optimization

---

### 1.14 Amazon Translate

**Pricing:**

| Feature | Price (per 1M chars) | Free Tier |
|---------|---------------------|-----------|
| Standard translation | $15.00 | 2M chars/month (12 months) |
| Active Custom Translation | $60.00 | — |
| Real-time document translation | $15.00 + per-page fee | — |
| Batch translation | $15.00 | — |

- 75+ languages
- Custom terminology for domain-specific terms
- Profanity masking
- Formality control (formal/informal)

**Cross-cloud comparison:** AWS Translate ($15/1M) vs GCP Translation ($20/1M) vs Azure Translator ($10/1M). Azure is cheapest. AWS free tier (2M chars/month for 12 months) is more generous than GCP (500K/month forever) for the first year.

---

## 2. Compute & Deployment

### 2.1 AWS Lambda -- Serverless Functions

AWS's flagship serverless compute. Run code without provisioning servers. Pay per invocation and duration.

**Pricing:**

| Resource | Price | Free Tier (per month, always free) |
|----------|-------|-----------------------------------|
| Requests | $0.20/million | 1 million requests |
| Duration (x86) | $0.0000166667/GB-second | 400,000 GB-seconds |
| Duration (ARM/Graviton) | $0.0000133334/GB-second | 400,000 GB-seconds |
| Provisioned Concurrency | $0.0000041667/GB-second (idle) | — |
| Ephemeral Storage | $0.0000000309/GB-second (>512MB) | 512 MB included |

**Limits:**

| Limit | Value |
|-------|-------|
| Max execution time | 15 minutes |
| Max memory | 10,240 MB (10 GB) |
| Max ephemeral storage | 10,240 MB (10 GB) |
| Max deployment package | 250 MB (unzipped), 50 MB (zipped) |
| Max concurrent executions | 1,000 (default, adjustable to 10K+) |
| Max payload (sync) | 6 MB |
| Max payload (async) | 256 KB |
| Cold start (Python) | 100-500ms (no VPC), 1-3s (with VPC) |
| Cold start (Java) | 3-10 seconds |

**Lambda@Edge vs CloudFront Functions:**

| Feature | Lambda@Edge | CloudFront Functions |
|---------|------------|---------------------|
| Runtime | Node.js, Python | JavaScript only |
| Max duration | 30 seconds | 1 ms |
| Max memory | 128-3008 MB | 2 MB |
| Network access | Yes | No |
| Pricing | $0.60/million | $0.10/million |
| Best for | Auth, A/B testing, dynamic routing | URL rewrites, header manipulation |

**SnapStart (Java/Python):** Reduces cold start from seconds to <200ms by pre-initializing and caching function snapshots. Free. Always enable for Java/Python.

**Graviton (ARM):** 20% cheaper than x86, 20% better performance for most workloads. Always use `arm64` architecture unless your code has x86 dependencies.

**Cross-cloud comparison:**
- Lambda (15 min max) vs GCP Cloud Run functions (60 min max) vs Azure Functions (unlimited on Premium)
- Lambda has the strictest timeout. GCP wins on execution duration. Azure wins on always-on premium plan.
- Lambda free tier (1M requests + 400K GB-seconds) vs GCP (2M requests + 400K GB-seconds) vs Azure (1M requests + 400K GB-seconds). GCP is most generous.

---

### 2.2 Amazon ECS Fargate -- Serverless Containers

Run containers without managing servers. AWS's primary container platform.

**Pricing:**

| Resource | Price (Linux x86) | Price (Linux ARM) |
|----------|------------------|------------------|
| vCPU per hour | $0.04048 | $0.03238 |
| GB memory per hour | $0.004445 | $0.003556 |
| Ephemeral storage | $0.000111/GB per hour (>20 GB) | Same |

**No free tier for Fargate.** Minimum billable: 1 minute, billed per second.

**Fargate Spot:** Up to 70% discount, but tasks can be interrupted with 2-minute warning. Best for batch processing, CI/CD, fault-tolerant workloads.

**Task sizing:**

| Configuration | vCPU | Memory Options | Monthly Cost (24/7) |
|--------------|------|---------------|-------------------|
| Micro | 0.25 | 0.5-2 GB | ~$9-12 |
| Small | 0.5 | 1-4 GB | ~$17-21 |
| Medium | 1 | 2-8 GB | ~$33-39 |
| Standard | 2 | 4-16 GB | ~$64-73 |
| Large | 4 | 8-30 GB | ~$127-143 |

**Fargate does NOT scale to zero.** You always pay for at least one running task. For scale-to-zero, use Lambda or consider GCP Cloud Run / Azure Container Apps.

**Veteran tip:** The biggest Fargate cost trap is leaving dev/staging tasks running 24/7. Use ECS Scheduled Tasks or EventBridge to start/stop tasks on a schedule. A task running 8 hours/day costs 1/3 of 24/7.

**Cross-cloud comparison:**
- Fargate ($0.04/vCPU-hr) vs GCP Cloud Run ($0.0864/vCPU-hr but scale-to-zero) vs Azure Container Apps ($0.0864/vCPU-hr + scale-to-zero)
- Fargate is cheapest per-hour for always-on workloads. Cloud Run/ACA win for bursty workloads due to scale-to-zero.

---

### 2.3 Amazon EKS -- Managed Kubernetes

**Pricing:**

| Component | Price |
|-----------|-------|
| EKS cluster (control plane) | $0.10/hour ($73/month) |
| EKS with Fargate | Cluster fee + Fargate pricing |
| EKS with EC2 | Cluster fee + EC2 pricing |
| EKS Auto Mode | Cluster fee + managed node pricing |
| EKS Anywhere (on-prem) | $0.10/hour per cluster |

**EKS Auto Mode (GA 2025):** AWS manages nodes, scaling, patching, and upgrades. Similar concept to GKE Autopilot. Reduces operational burden significantly.

**When to use EKS vs Fargate vs Lambda:**

| Criteria | Lambda | Fargate (ECS) | EKS |
|----------|--------|--------------|-----|
| Team K8s expertise | None needed | None needed | Required |
| Max execution time | 15 minutes | Unlimited | Unlimited |
| Scale-to-zero | Yes | No | No |
| GPU support | No | No (use EC2) | Yes |
| Multi-container pods | No | Yes (task) | Yes |
| Service mesh | No | App Mesh | Istio/Linkerd |
| Cost (small) | Cheapest | Medium | Most expensive |
| Cost (large/constant) | Expensive | Medium | Cheapest |

---

### 2.4 Amazon EC2 -- GPU Instances

**Current GPU Instance Families (March 2026):**

| Family | GPU | GPU Memory | On-Demand/hr (smallest) | Spot/hr | Best For |
|--------|-----|-----------|------------------------|---------|----------|
| **P5en** | NVIDIA H200 | 141 GB HBM3e | ~$55/hr (48xlarge) | ~$16-22 | Frontier LLM training |
| **P5e** | NVIDIA H200 | 141 GB HBM3e | ~$50/hr (48xlarge) | ~$15-20 | Large model training |
| **P5** | NVIDIA H100 | 80 GB HBM3 | ~$33/hr (48xlarge) | ~$10-13 | LLM training, large inference |
| **P4d** | NVIDIA A100 | 40 GB HBM2e | ~$32.77/hr (24xlarge) | ~$10-13 | Training, large model inference |
| **G6e** | NVIDIA L40S | 48 GB GDDR6 | ~$1.86/hr (xlarge) | ~$0.56 | High-quality inference, graphics |
| **G6** | NVIDIA L4 | 24 GB GDDR6 | ~$0.81/hr (xlarge) | ~$0.24 | Inference, video processing |
| **G5** | NVIDIA A10G | 24 GB GDDR6 | ~$1.01/hr (xlarge) | ~$0.30 | Inference, light training |
| **Inf2** | AWS Inferentia2 | 32 GB HBM | ~$0.76/hr (xlarge) | ~$0.23 | Cost-efficient inference |
| **Trn1** | AWS Trainium | 32 GB HBM | ~$1.34/hr (2xlarge) | ~$0.40 | AWS-optimized training |

**Spot Instances:**
- 60-90% discount off on-demand
- 2-minute interruption warning
- Best for: fault-tolerant training (with checkpointing), batch inference, CI/CD
- Use Spot Fleet or EC2 Auto Scaling with multiple instance types for reliability

**Savings Plans:**
- Compute Savings Plans: 1-year (up to 54% discount), 3-year (up to 72%)
- EC2 Instance Savings Plans: Slightly higher discount but locked to instance family
- Apply automatically to EC2, Fargate, and Lambda

**Reserved Instances:**
- 1-year: up to 40% discount
- 3-year: up to 60% discount
- All Upfront gives the biggest discount
- Being phased out in favor of Savings Plans

**Capacity Blocks (for ML):** Reserve GPU instances for a defined period (1 day to 6 months) at a predictable cost. Available for P5, P4d, Trn1. Best for planned training runs.

---

### 2.5 AWS App Runner

Fully managed container service -- simpler than Fargate, more like GCP Cloud Run.

**Pricing:**

| Resource | Price |
|----------|-------|
| vCPU (active) | $0.064/vCPU-hour |
| vCPU (provisioned/idle) | $0.007/vCPU-hour |
| Memory | $0.007/GB-hour |
| Automatic deployments | $1.00/month per connection |

**Limits:** Max 25 vCPUs, max 12 GB memory per instance, max 200 concurrent requests per instance.

**When to use App Runner vs Fargate vs Lambda:**
- **App Runner:** Simple web services, APIs, no container expertise needed
- **Fargate:** Complex architectures, sidecars, service mesh, large deployments
- **Lambda:** Event-driven, short-lived functions

**Cross-cloud comparison:** App Runner is AWS's answer to GCP Cloud Run and Azure Container Apps. It's simpler but less feature-rich (no GPU, no scale-to-zero for compute, limited configuration).

---

### 2.6 AWS Elastic Beanstalk

PaaS for deploying web applications. Manages EC2, load balancers, auto-scaling, and health monitoring.

**Pricing:** No additional charge for Elastic Beanstalk. You pay for underlying AWS resources (EC2, ALB, etc.).

**Supported platforms:** Python, Node.js, Java, .NET, PHP, Ruby, Go, Docker, multi-container Docker.

**When to use:** Legacy applications, teams familiar with PaaS, simple deployments. For new projects, prefer Fargate or App Runner.

---

### 2.7 Amazon Lightsail

Simplified VPS for small projects, personal sites, and dev environments.

**Pricing (Linux):**

| Plan | vCPUs | RAM | Storage | Transfer | Monthly |
|------|-------|-----|---------|----------|---------|
| Nano | 1 (shared) | 512 MB | 20 GB SSD | 1 TB | $3.50 |
| Micro | 1 (shared) | 1 GB | 40 GB SSD | 2 TB | $5.00 |
| Small | 1 | 2 GB | 60 GB SSD | 3 TB | $10.00 |
| Medium | 2 | 4 GB | 80 GB SSD | 4 TB | $20.00 |
| Large | 2 | 8 GB | 160 GB SSD | 5 TB | $40.00 |
| XLarge | 4 | 16 GB | 320 GB SSD | 6 TB | $80.00 |

**Free tier:** 3 months free on select plans (up to the $12/month plan).

**Best for:** WordPress sites, personal projects, dev servers. NOT for production AI workloads.

---

## 3. Storage & Databases

### 3.1 Amazon S3 -- Object Storage

The backbone of AWS storage. Everything from data lakes to static websites to ML training data.

**Storage Classes:**

| Class | Price/GB/month (US East) | Min Duration | Retrieval Cost/GB | Best For |
|-------|------------------------|-------------|-------------------|----------|
| **S3 Standard** | $0.023 | None | Free | Frequently accessed data |
| **S3 Intelligent-Tiering** | $0.023 (frequent) down to $0.00099 (archive) | None | Free (no retrieval charge) | Unknown access patterns |
| **S3 Standard-IA** | $0.0125 | 30 days | $0.01 | Infrequent access, rapid retrieval |
| **S3 One Zone-IA** | $0.01 | 30 days | $0.01 | Infrequent, non-critical (single AZ) |
| **S3 Glacier Instant Retrieval** | $0.004 | 90 days | $0.03 | Archive, millisecond access |
| **S3 Glacier Flexible Retrieval** | $0.0036 | 90 days | $0.01 (expedited: $0.03) | Archive, 1-12 hour retrieval |
| **S3 Glacier Deep Archive** | $0.00099 | 180 days | $0.02 (standard: 12 hrs) | Long-term archive, compliance |
| **S3 Express One Zone** | $0.16 | None | Free | Ultra-low latency (single-digit ms) |

**Request Pricing:**

| Operation | Standard | Standard-IA | Glacier Instant |
|-----------|----------|-------------|-----------------|
| PUT/COPY/POST (per 1K) | $0.005 | $0.01 | $0.02 |
| GET/SELECT (per 1K) | $0.0004 | $0.001 | $0.01 |

**Egress (data out to internet):**

| Volume | Price/GB |
|--------|----------|
| First 100 GB/month | Free |
| 100 GB - 10 TB | $0.09 |
| 10 TB - 50 TB | $0.085 |
| 50 TB - 150 TB | $0.07 |
| 150 TB+ | $0.05 |

**S3 Intelligent-Tiering -- The Smart Default:**

Automatically moves objects between access tiers based on usage patterns. Zero retrieval fees. $0.0025 per 1,000 objects monitoring fee.

Tiers: Frequent Access → Infrequent Access (30 days) → Archive Instant (90 days) → Archive (90 days, opt-in) → Deep Archive (180 days, opt-in).

**Use Intelligent-Tiering for everything** unless you know exactly how your data will be accessed. The monitoring fee is negligible.

**Presigned URLs:** Temporary access to private objects. Valid up to 7 days. Generate with AWS SDK.

**Cross-cloud comparison:**
- S3 Standard ($0.023/GB) vs GCS Standard ($0.020/GB) vs Azure Blob Hot ($0.018/GB)
- Azure is cheapest for storage. GCS is 13% cheaper than S3. S3 has the most features (Intelligent-Tiering, S3 Express One Zone, S3 Vectors).
- S3 egress is now free for first 100 GB/month (since late 2024). GCS egress: first 1 GB free. Azure: 100 GB free.

---

### 3.2 Amazon S3 Vectors (GA December 2025)

Purpose-built vector storage at S3 prices. The newest vector option on AWS.

**Capabilities:**
- 2 billion vectors per index
- 10,000 vector indexes per vector bucket
- Up to 90% cheaper than OpenSearch Serverless for pure storage
- Pay for: PUT (per logical GB), storage (per GB), query processing (per query)

**Architecture pattern:**
```
Hot queries  → OpenSearch Serverless (fast, expensive)
Cold/archive → S3 Vectors (cheap, higher latency)
```

**Best for:** Billion-scale archival, compliance records, historical document stores, cost-optimized RAG.

---

### 3.3 Amazon DynamoDB -- NoSQL

Serverless key-value and document database. Scales to any workload with single-digit millisecond latency.

**Pricing Modes:**

| Mode | Read | Write | Best For |
|------|------|-------|----------|
| **On-Demand** | $1.25/million RRU | $1.25/million WRU | Unpredictable traffic |
| **Provisioned** | $0.00013/RCU-hour | $0.00065/WCU-hour | Predictable traffic |

**Storage:** $0.25/GB/month (Standard), $0.10/GB/month (IA table class)

**Free tier (always free):** 25 GB storage + 25 WCU + 25 RCU (provisioned mode) -- enough for ~200M requests/month.

**Global Tables (multi-region replication):** 1.725x the write cost of single-region. Automatic conflict resolution.

**DynamoDB Streams:** $0.02 per 100K read requests. Powers event-driven architectures (Lambda triggers on table changes).

**Transactions:** 2x the cost of standard reads/writes. ACID across up to 100 items.

**Key features:**
- Single-digit millisecond latency at any scale
- Auto-scaling (on-demand mode)
- TTL (automatic item expiration, free)
- Point-in-time recovery ($0.20/GB/month)
- DAX (in-memory cache, microsecond latency)

**Cross-cloud comparison:**
- DynamoDB vs GCP Firestore vs Azure Cosmos DB
- DynamoDB has the most generous free tier (25 GB always free). Firestore has real-time listeners. Cosmos DB has global distribution + vector search.
- DynamoDB is cheapest for high-throughput key-value workloads. Cosmos DB is most feature-rich. Firestore is best for mobile/web.

---

### 3.4 Amazon RDS -- Managed Relational Databases

Managed relational database service supporting PostgreSQL, MySQL, MariaDB, Oracle, SQL Server.

**PostgreSQL Pricing (US East, Multi-AZ):**

| Instance | vCPUs | RAM | On-Demand/hr | Monthly (730 hrs) |
|----------|-------|-----|-------------|-------------------|
| db.t4g.micro | 2 | 1 GB | $0.024 | ~$18 |
| db.t4g.small | 2 | 2 GB | $0.048 | ~$35 |
| db.t4g.medium | 2 | 4 GB | $0.096 | ~$70 |
| db.r6g.large | 2 | 16 GB | $0.380 | ~$277 |
| db.r6g.xlarge | 4 | 32 GB | $0.760 | ~$555 |
| db.r6g.2xlarge | 8 | 64 GB | $1.520 | ~$1,110 |

**Storage:**
- gp3: $0.08/GB/month (3,000 IOPS baseline, 125 MB/s baseline -- free)
- io2: $0.125/GB/month + $0.065/provisioned-IOPS
- Magnetic: $0.10/GB/month (legacy, avoid)

**Multi-AZ:** Doubles compute cost. Provides automatic failover.
**Read Replicas:** Same price as primary. Up to 15 read replicas per instance.
**Backups:** Free up to 100% of DB storage. Beyond that: $0.095/GB/month.

**pgvector for RAG:**
- FREE extension -- included with RDS PostgreSQL 15+
- Supports HNSW and IVFFlat indexes
- Good for <10M vectors
- HNSW index: 15x faster than IVFFlat but requires more RAM
- Critical: entire HNSW index must fit in memory -- size your instance accordingly

---

### 3.5 Amazon Aurora -- High-Performance Relational

PostgreSQL and MySQL-compatible. Up to 5x PostgreSQL performance, 3x MySQL performance.

**Aurora Serverless v2 Pricing:**

| Resource | Price |
|----------|-------|
| ACU-hour (compute) | $0.12 |
| Storage | $0.10/GB/month |
| I/O | $0.20/million requests |
| Backups (beyond free) | $0.021/GB/month |

**Minimum:** 0.5 ACU (~$0.06/hr = ~$44/month). Scales to 256 ACU.

**Aurora Provisioned (Standard):**

| Instance | vCPUs | RAM | On-Demand/hr |
|----------|-------|-----|-------------|
| db.r6g.large | 2 | 16 GB | $0.260 |
| db.r6g.xlarge | 4 | 32 GB | $0.520 |
| db.r6g.2xlarge | 8 | 64 GB | $1.040 |

**Aurora + pgvector for RAG:**
- 67x faster embedding loads vs standard PostgreSQL (Aurora storage optimization)
- HNSW index support
- Serverless v2 auto-scales with RAG query load
- Fully supported as Bedrock Knowledge Bases vector store
- Best for: <100M vectors, existing PostgreSQL shops, ACID + vectors

**When to use Aurora vs RDS:**

| Feature | RDS PostgreSQL | Aurora PostgreSQL |
|---------|---------------|------------------|
| Price | Lower | 20-30% higher |
| Performance | 1x | 3-5x |
| Auto-scaling storage | Manual | Automatic |
| Serverless option | No | Yes (v2) |
| Read replicas (latency) | Seconds | Milliseconds |
| pgvector performance | Standard | Optimized (67x loads) |
| Failover time | 60-120 seconds | <30 seconds |

**Veteran tip:** For RAG workloads, Aurora Serverless v2 with pgvector is the sweet spot. It auto-scales with query load, costs ~$100-175/month for typical RAG, and the 67x faster embedding loads save hours during ingestion.

---

### 3.6 Amazon OpenSearch Serverless

Managed search and vector database. The default vector store for Bedrock Knowledge Bases.

**Pricing:**
- $0.24 per OCU-hour for both indexing AND search
- Hard minimum: 4 OCUs for first vector collection = ~$350/month floor
- Vector collections cannot share OCUs with other collection types
- GPU acceleration: 10x faster indexing at 1/4 CPU cost (separate charge)

**Performance:**
- 1 OCU = ~500K vectors @ 768 dims at 99% recall
- Hybrid Search: BM25 (lexical) + kNN (vector) native support
- Auto-scales with traffic

**Best for:** 100M+ vectors, unpredictable traffic, hybrid BM25 + vector search, Bedrock KB integration.

**Cross-cloud comparison:**
- OpenSearch Serverless ($350/mo floor) vs GCP Vector Search ($0.54/node-hr) vs Azure AI Search ($74/mo Basic)
- Azure AI Search is cheapest at entry level. OpenSearch is most feature-rich. GCP Vector Search has best raw performance at scale.

---

### 3.7 Amazon ElastiCache / Valkey -- In-Memory Cache

**ElastiCache (Redis/Memcached) and Valkey (Redis fork):**

| Type | Smallest Instance | Price/hr | Monthly |
|------|------------------|----------|---------|
| Valkey t4g.micro (Serverless) | 1 GB | $0.012 | ~$9 |
| Redis cache.t4g.micro | 0.5 GB | $0.016 | ~$12 |
| Redis cache.r6g.large | 13.07 GB | $0.166 | ~$121 |
| Redis cache.r6g.xlarge | 26.32 GB | $0.332 | ~$242 |
| Memcached cache.t4g.micro | 0.5 GB | $0.012 | ~$9 |

**ElastiCache Serverless:** Pay per GB stored ($0.125/GB/hr) + per ECPU processed. Scales to zero compute (but minimum $0.125/GB storage).

**Free tier:** ElastiCache Serverless: 750 hours of t4g.micro equivalent per month (12 months).

**MemoryDB for Redis (Vector Search):**
- Vector search is FREE -- no additional charge
- Fastest sub-ms query AND update latency
- All data persisted to SSD (unlike ElastiCache which is volatile)
- ~$180/month floor for production instance
- Best for: semantic caching layer, real-time RAG with sub-ms requirements

**When to use which:**

| Use Case | Best Choice |
|----------|------------|
| Simple cache (sessions, API responses) | ElastiCache Serverless (Valkey) |
| RAG semantic cache | MemoryDB (vector search, persistent) |
| High-throughput cache | ElastiCache Redis (provisioned) |
| Cost-first cache | ElastiCache Serverless |

---

### 3.8 Amazon DocumentDB -- MongoDB-Compatible

MongoDB-compatible document database managed by AWS.

**Pricing:**

| Resource | Price |
|----------|-------|
| db.r6g.large (2 vCPU, 16 GB) | $0.262/hr |
| Storage | $0.10/GB/month |
| I/O | $0.20/million |
| Elastic Cluster (serverless) | $0.10/vCPU-hr + $0.20/million I/O |

**When to use:** Existing MongoDB workloads migrating to AWS. For new projects, DynamoDB (NoSQL) or Aurora (relational) are usually better choices.

---

### 3.9 Amazon Neptune -- Graph Database

**Pricing:**

| Resource | Price |
|----------|-------|
| db.r6g.large | $0.348/hr |
| Storage | $0.10/GB/month |
| I/O | $0.20/million |
| Neptune Analytics | $0.07/graph-hr + $0.00035/GB-hr memory |

**Neptune Analytics (GraphRAG):**
- Automatically generates vector embeddings + graph representation
- Combines vector similarity with graph traversal in single query
- 30-40% improvement on multi-document reasoning vs standard RAG
- Natively integrated into Bedrock Knowledge Bases
- BYOKG (Bring Your Own Knowledge Graph) support

**Best for:** Knowledge graphs, fraud detection, social networks, legal document networks, recommendation engines.

---

### 3.10 Amazon Timestream

Serverless time-series database.

**Pricing:**
- Writes: $0.50/million writes
- Memory storage: $0.036/GB/hr
- Magnetic storage: $0.03/GB/month
- Queries: $10.00/GB scanned

**Best for:** IoT telemetry, DevOps metrics, financial tick data. For ML experiment tracking, prefer MLflow on SageMaker or W&B.

---

## 4. Networking & CDN

### 4.1 Amazon CloudFront -- CDN

**Pricing (US/Europe):**

| Resource | Price |
|----------|-------|
| Data out (first 10 TB/month) | $0.085/GB |
| Data out (10-50 TB) | $0.080/GB |
| Data out (50-150 TB) | $0.060/GB |
| HTTPS requests (per 10K) | $0.0100 |
| HTTP requests (per 10K) | $0.0075 |
| Real-time log delivery | $0.01/million log lines |
| Custom SSL certificate | Free (ACM managed) |
| Origin Shield | $0.0075/10K requests per region |

**Free tier (always free):** 1 TB data transfer out + 10 million HTTP/HTTPS requests per month.

**Edge locations:** 600+ globally (more than any other CDN).

**CloudFront Functions:** Lightweight JavaScript at the edge, $0.10/million invocations. For URL rewrites, header manipulation, simple auth checks.

**Lambda@Edge:** Full Node.js/Python at the edge, $0.60/million invocations. For A/B testing, bot detection, image transformation.

**Cross-cloud comparison:**
- CloudFront ($0.085/GB US) vs GCP Cloud CDN ($0.08/GB) vs Azure Front Door ($0.087/GB)
- Pricing is nearly identical across clouds. CloudFront has the most edge locations (600+ vs ~200 GCP vs ~200 Azure). CloudFront Functions + Lambda@Edge give the most flexible edge compute.

---

### 4.2 Elastic Load Balancing (ALB / NLB)

**Application Load Balancer (ALB):**

| Resource | Price |
|----------|-------|
| ALB hour | $0.0225/hr (~$16.50/month) |
| LCU-hour | $0.008 |

**Network Load Balancer (NLB):**

| Resource | Price |
|----------|-------|
| NLB hour | $0.0225/hr (~$16.50/month) |
| NLCU-hour | $0.006 |

**Gateway Load Balancer (GWLB):**

| Resource | Price |
|----------|-------|
| GWLB hour | $0.0125/hr |
| GLCU-hour | $0.004 |

**When to use which:**

| Feature | ALB | NLB |
|---------|-----|-----|
| Protocol | HTTP/HTTPS (L7) | TCP/UDP/TLS (L4) |
| Routing | Path, host, header, query string | Port-based |
| WebSocket | Yes | Yes |
| gRPC | Yes | No |
| Static IP | No | Yes |
| Latency | ~1-2ms added | ~100us added |
| Best for | Web APIs, microservices | Real-time, gaming, IoT |

---

### 4.3 Amazon Route 53 -- DNS

**Pricing:**

| Resource | Price |
|----------|-------|
| Hosted zone | $0.50/month |
| Standard queries | $0.40/million |
| Latency-based routing queries | $0.60/million |
| Geo DNS queries | $0.70/million |
| Health checks | $0.50/month (standard), $1.00/month (HTTPS) |
| Domain registration | $9-40/year depending on TLD |

**Features:** Latency-based routing, weighted routing, failover, geolocation, multivalue answer, traffic flow (visual editor).

---

### 4.4 Amazon API Gateway

**REST API Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| API calls | $3.50/million (first 333M) | 1 million calls/month (12 months) |
| Data transfer out | Standard CloudFront rates | — |
| Caching (0.5 GB) | $0.020/hr | — |
| Caching (6.1 GB) | $0.200/hr | — |

**HTTP API Pricing (cheaper, recommended for most use cases):**

| Resource | Price |
|----------|-------|
| API calls | $1.00/million (first 300M) |
| Data transfer out | Standard rates |

**WebSocket API:**

| Resource | Price |
|----------|-------|
| Messages | $1.00/million |
| Connection minutes | $0.25/million |

**Veteran tip:** Use HTTP APIs unless you need REST API features (API keys, request validation, WAF integration, usage plans). HTTP APIs are 71% cheaper and have lower latency.

---

### 4.5 Amazon VPC & PrivateLink

**VPC Pricing:**

| Resource | Price |
|----------|-------|
| VPC | Free |
| NAT Gateway | $0.045/hr + $0.045/GB processed |
| VPC Endpoint (Interface/PrivateLink) | $0.01/hr per AZ + $0.01/GB |
| VPC Endpoint (Gateway -- S3, DynamoDB) | Free |
| VPC Peering | Free (data transfer: $0.01/GB cross-AZ) |
| Transit Gateway | $0.05/hr per attachment + $0.02/GB |

**Cost trap: NAT Gateway.** A NAT Gateway running 24/7 costs ~$33/month PLUS data processing fees. If your Fargate tasks need internet access, this can exceed the compute cost. Mitigations:
1. Use VPC Gateway endpoints for S3 and DynamoDB (free)
2. Use Interface endpoints for AWS services (cheaper than NAT for high-volume)
3. Use `fck-nat` AMI (open-source NAT instance on t4g.nano ~$3/month)

---

## 5. Serverless & Event-Driven

### 5.1 Amazon SQS -- Message Queue

**Pricing:**

| Type | Price per million requests | Free Tier |
|------|--------------------------|-----------|
| Standard | $0.40 | 1 million requests/month (always free) |
| FIFO | $0.50 | 1 million requests/month (always free) |

**Limits:**
- Message size: 256 KB (use S3 for larger payloads)
- Retention: 1 minute to 14 days (default 4 days)
- Standard: unlimited throughput, at-least-once delivery
- FIFO: 300 messages/second (3,000 with batching), exactly-once delivery

---

### 5.2 Amazon SNS -- Pub/Sub Notifications

**Pricing:**

| Delivery Type | Price | Free Tier |
|--------------|-------|-----------|
| Mobile push | $0.50/million | 1 million publishes (always free) |
| Email/Email-JSON | $2.00/100K notifications | 1,000 emails |
| HTTP/HTTPS | $0.60/million | — |
| SQS | Free | — |
| Lambda | Free | — |
| SMS | $0.00645-$0.75/message (varies by country) | — |

---

### 5.3 Amazon EventBridge -- Event Bus

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Custom events | $1.00/million | First 14M events/month (always free) |
| AWS service events | Free | Always free |
| Schema discovery | Free | — |
| Pipes (processing) | $0.40/million events | First 2M events/month |
| Scheduler | Free (up to 14M invocations/month) | Always free |

**EventBridge vs SNS vs SQS:**

| Feature | EventBridge | SNS | SQS |
|---------|------------|-----|-----|
| Pattern | Event bus (routing) | Pub/Sub (fan-out) | Queue (point-to-point) |
| Filtering | Content-based rules | Attribute-based | No |
| Targets | 30+ AWS services | SQS, Lambda, HTTP | Lambda, EC2 |
| Ordering | No (use SQS FIFO) | FIFO topic | FIFO queue |
| Replay | Event archive + replay | No | No |
| Best for | Event-driven architecture | Notifications | Task processing |

---

### 5.4 AWS Step Functions -- Workflow Orchestration

**Pricing:**

| Type | Price | Free Tier |
|------|-------|-----------|
| Standard | $0.025/1K state transitions | 4,000 transitions/month (always free) |
| Express (sync) | $0.000001/request + duration | — |
| Express (async) | $0.000001/request + duration | — |

**Standard vs Express:**

| Feature | Standard | Express |
|---------|----------|---------|
| Max duration | 1 year | 5 minutes |
| Execution history | Yes (viewable in console) | CloudWatch Logs only |
| Max transitions/second | 2,000 | Unlimited |
| Exactly-once | Yes | At-least-once |
| Pricing unit | State transitions | Requests + duration |
| Best for | Long-running workflows, human approval | High-volume, short tasks |

**Step Functions is the glue for AI pipelines on AWS:** Document ingestion (S3 → Textract → chunk → embed → OpenSearch), multi-step agent orchestration, batch ML processing with error handling and retries.

---

### 5.5 Amazon Kinesis -- Real-Time Streaming

**Kinesis Data Streams:**

| Resource | Price |
|----------|-------|
| Shard hour (provisioned) | $0.015/hr |
| PUT payload unit (25KB) | $0.014/million |
| On-demand mode | $0.036/stream-hr + $0.08/GB |

**Kinesis Data Firehose:**
- $0.029/GB (first 500 TB/month)
- Direct delivery to S3, Redshift, OpenSearch, Splunk
- Zero administration

**When to use Kinesis vs SQS:**
- **Kinesis:** Real-time analytics, log aggregation, multiple consumers reading same stream, replay
- **SQS:** Task queues, decoupling microservices, single consumer per message

---

## 6. Security & IAM

### 6.1 AWS IAM -- Identity and Access Management

**Pricing:** Free. IAM itself costs nothing.

**Key concepts:**
- **Users:** Individual accounts with credentials
- **Roles:** Assumed by services (EC2, Lambda, ECS). Always prefer roles over users for services.
- **Policies:** JSON documents defining permissions (Effect, Action, Resource)
- **Groups:** Collections of users (apply policies to groups, not individual users)
- **Identity Center (formerly SSO):** Centralized access management, free

**Best practices for AI projects:**
1. Never put access keys in code or environment variables on EC2/Lambda/ECS
2. Use IAM roles for all AWS service-to-service communication
3. Use least-privilege policies (start with minimal, add as needed)
4. Enable MFA on all human accounts
5. Use Service Control Policies (SCPs) in AWS Organizations for guardrails
6. Rotate credentials every 90 days (or use short-lived credentials via roles)

**Minimal Bedrock IAM Policy:**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:Retrieve",
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
                "arn:aws:bedrock:*::foundation-model/amazon.*",
                "arn:aws:bedrock:*:ACCOUNT:knowledge-base/*"
            ]
        }
    ]
}
```

---

### 6.2 AWS Secrets Manager

**Pricing:**
- $0.40/secret/month
- $0.05/10K API calls

**Features:** Automatic rotation (Lambda-based), cross-account access, versioning, RDS/Redshift/DocumentDB integration.

**Secrets Manager vs SSM Parameter Store:**

| Feature | Secrets Manager | SSM Parameter Store |
|---------|----------------|-------------------|
| Price | $0.40/secret/month | Free (standard), $0.05/advanced/month |
| Auto-rotation | Yes (built-in) | No (manual Lambda) |
| Cross-account | Yes | Limited |
| Max size | 64 KB | 4 KB (standard), 8 KB (advanced) |
| Best for | Database credentials, API keys | Config values, feature flags |

**Veteran tip:** Use SSM Parameter Store (free tier) for non-sensitive config. Use Secrets Manager only for secrets that need rotation (DB passwords, API keys).

---

### 6.3 AWS KMS -- Key Management Service

**Pricing:**
- Customer-managed keys: $1.00/month per key
- API requests: $0.03/10K requests
- AWS-managed keys: Free (for S3, EBS, etc.)

**Free tier:** 20,000 requests/month (always free).

---

### 6.4 AWS WAF -- Web Application Firewall

**Pricing:**
- $5.00/month per Web ACL
- $1.00/month per rule
- $0.60/million requests

**Managed rule groups:** AWS-managed rules for common threats (SQL injection, XSS, bad bots). $1.00-$3.00/month per rule group.

**AWS Shield:**
- Standard: Free (DDoS protection for all AWS resources)
- Advanced: $3,000/month + data transfer (enterprise DDoS protection with 24/7 support)

---

### 6.5 Amazon Cognito -- User Authentication

**Pricing:**

| Tier | MAU (Monthly Active Users) | Price per MAU |
|------|---------------------------|---------------|
| Essentials | First 10,000 | Free |
| Essentials | 10K - 100K | $0.015 |
| Essentials | 100K - 1M | $0.0130 |
| Essentials | 1M - 10M | $0.0100 |
| Plus (advanced security) | First 10,000 | Free |
| Plus | 10K+ | $0.050-$0.080 |

**Features:** User pools, identity pools (federated identity), OAuth 2.0/OIDC, social login (Google, Apple, Facebook), SAML, custom auth flows, MFA.

**Free tier:** 10,000 MAU (always free, Essentials tier).

---

## 7. CI/CD & DevOps

### 7.1 AWS CodeBuild

**Pricing:**

| Instance | Price/min | Free Tier |
|----------|----------|-----------|
| general1.small (3 GB) | $0.005 | 100 build minutes/month |
| general1.medium (7 GB) | $0.010 | — |
| general1.large (15 GB) | $0.020 | — |
| gpu1.large (NVIDIA GPU) | $0.330 | — |
| arm1.small (3 GB) | $0.0034 | — |

**Best practices:**
- Use ARM builds (32% cheaper) for Python/Node.js projects
- Cache Docker layers in S3 to reduce build time by 50-80%
- Use `buildspec.yml` in repo root

---

### 7.2 AWS CodePipeline

**Pricing:**
- $1.00/month per active pipeline (V1)
- V2: Free for first pipeline, then $1.00/month per pipeline

**Free tier:** 1 active pipeline (always free, V2).

---

### 7.3 Amazon ECR -- Container Registry

**Pricing:**
- Storage: $0.10/GB/month
- Data transfer: Standard AWS rates

**Free tier:** 500 MB/month storage (12 months for private repos). 50 GB/month for public repos (always free).

**ECR Lifecycle Policies:** Automatically delete old images based on age or count. Critical for cost control.

---

### 7.4 AWS CodeDeploy

**Pricing:** Free for EC2/Lambda deployments. $0.02 per on-premises instance deployment.

**Deployment strategies:** Rolling, Blue/Green, Canary, All-at-once. Blue/Green is recommended for production.

---

### 7.5 AWS CDK -- Infrastructure as Code

**Pricing:** Free. CDK generates CloudFormation templates.

**Why CDK over CloudFormation/Terraform:**
- Write infrastructure in Python, TypeScript, Java, Go, C#
- L2/L3 constructs provide sane defaults (fewer lines of code)
- Type-safe, IDE autocomplete
- Official AWS support

**Cross-cloud comparison:**
- CDK (AWS-only) vs Terraform (multi-cloud) vs Pulumi (multi-cloud, real code)
- Use CDK for AWS-only projects. Terraform for multi-cloud. Pulumi if you want the CDK experience across clouds.

---

## 8. Monitoring & Observability

### 8.1 Amazon CloudWatch

**Metrics:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Custom metrics | $0.30/metric/month (first 10K) | 10 custom metrics |
| API requests (GetMetricData) | $0.01/1K metrics requested | — |
| Dashboard | $3.00/month per dashboard | 3 dashboards (50 metrics) |
| Alarms | $0.10/alarm/month (standard) | 10 alarms |
| Alarms (high-resolution) | $0.30/alarm/month | — |

**Logs:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Ingestion | $0.50/GB | 5 GB/month |
| Storage | $0.03/GB/month | 5 GB/month |
| Logs Insights queries | $0.005/GB scanned | — |

**Veteran tip:** CloudWatch Logs is a massive hidden cost. A busy Lambda or Fargate service can easily generate 100+ GB/month of logs ($50+). Mitigations:
1. Set log retention (7 or 14 days for dev, 30-90 for prod)
2. Use structured logging (JSON) and filter at query time
3. Sample logs (log 10% of requests in high-throughput services)
4. Use Log Subscription Filters to send only important logs to storage

---

### 8.2 AWS X-Ray -- Distributed Tracing

**Pricing:**
- Traces recorded: $5.00/million
- Traces retrieved: $0.50/million
- Traces scanned: $0.50/million

**Free tier:** 100K traces recorded + 1M traces retrieved per month (always free).

**X-Ray integrates with:** Lambda, API Gateway, ECS, EKS, App Runner, SQS, SNS, EventBridge, Step Functions.

---

### 8.3 AWS CloudTrail -- API Audit Logging

**Pricing:**
- Management events (first trail): Free
- Management events (additional trails): $2.00/100K events
- Data events: $0.10/100K events
- CloudTrail Lake queries: $2.50/GB scanned

**Best practice:** Always have one trail enabled (free). Critical for security auditing and compliance.

---

## 9. Free Tier (Complete List)

### Important: AWS Free Tier Changed in July 2025

As of July 15, 2025, new AWS accounts get the **Free Plan** (credit-based) instead of the legacy 12-month free tier:
- $100 AWS credits on signup
- Up to $100 more by completing onboarding tasks
- Credits expire after 12 months
- Accounts created before July 15, 2025 keep the legacy 12-month free tier

### Always Free (Never Expires)

| Service | Always-Free Limit |
|---------|------------------|
| **Lambda** | 1M requests + 400K GB-seconds/month |
| **DynamoDB** | 25 GB storage + 25 WCU + 25 RCU |
| **S3** | First 100 GB data out/month |
| **CloudFront** | 1 TB data out + 10M requests/month |
| **SNS** | 1M publishes/month |
| **SQS** | 1M requests/month |
| **EventBridge** | 14M custom events/month |
| **Step Functions** | 4,000 state transitions/month |
| **CloudWatch** | 10 custom metrics + 10 alarms + 5 GB logs |
| **X-Ray** | 100K traces recorded + 1M retrieved/month |
| **KMS** | 20,000 requests/month |
| **Cognito** | 10,000 MAU (Essentials) |
| **CodeBuild** | 100 build minutes/month |
| **CodePipeline** | 1 active pipeline (V2) |
| **IAM** | Unlimited |
| **CloudTrail** | 1 management trail |
| **AWS Organizations** | Free |
| **CloudFormation** | Free (you pay for provisioned resources) |
| **Secrets Manager** | 30-day free trial, then $0.40/secret |
| **Amazon Q Developer** | Free tier (code suggestions, chat) |
| **Systems Manager** | Most features free |
| **Trusted Advisor** | Basic checks free |
| **AWS Amplify** | 1,000 build minutes/month |
| **SES** | 62,000 emails/month (from EC2) |
| **ECR Public** | 50 GB storage/month |

### 12-Month Free (Legacy Accounts Created Before July 2025)

| Service | 12-Month Free Limit |
|---------|-------------------|
| **EC2** | 750 hrs/month (t2.micro or t3.micro) |
| **RDS** | 750 hrs/month (db.t2.micro/t3.micro) |
| **S3** | 5 GB storage |
| **ElastiCache** | 750 hrs/month (cache.t2.micro/t3.micro) |
| **OpenSearch** | 750 hrs/month (t2.small.search) |
| **SageMaker** | 250 hrs/month (Studio notebook, ml.t3.medium) |
| **Comprehend** | 50K units/month for most features |
| **Transcribe** | 60 minutes/month |
| **Polly** | 5M chars Standard + 1M chars Neural |
| **Rekognition** | 5,000 images/month |
| **Translate** | 2M characters/month |
| **API Gateway** | 1M REST API calls/month |
| **Lightsail** | 3 months free (select plans) |
| **EBS** | 30 GB/month |
| **CloudFront** | 50 GB data out (in addition to always-free) |
| **ECR Private** | 500 MB storage |
| **SNS** | Additional allowances |

### Short-Term Trials

| Service | Trial |
|---------|-------|
| **Bedrock** | No free tier (pay per token from first use) |
| **SageMaker** | 250 hrs/month ml.t3.medium (2 months) |
| **Kendra** | 750 hours Developer edition (30 days) |
| **Textract** | 1,000 pages/month (3 months) |
| **GuardDuty** | 30-day free trial |
| **Macie** | 30-day free trial |
| **Inspector** | 15-day free trial |

---

## 10. Pricing Comparisons vs GCP and Azure

### AI/ML Model Pricing (Per 1M Tokens, On-Demand)

| Model Category | AWS (Bedrock) | GCP (Vertex AI) | Azure (OpenAI) |
|---------------|---------------|-----------------|----------------|
| **Cheapest text model** | Nova Micro: $0.035/$0.14 | Gemini 2.0 Flash-Lite: $0.10/$0.40 | GPT-4.1-nano: $0.10/$0.40 |
| **Best value mid-tier** | Claude Sonnet 4.6: $3/$15 | Gemini 2.5 Flash: $0.30/$2.50 | GPT-4o: $2.50/$10 |
| **Frontier reasoning** | Claude Opus 4.6: $15/$75 | Gemini 2.5 Pro: $1.25/$10 | o3: $2/$8 |
| **Cheapest embedding** | Titan V2: $0.02 | text-embedding-005: ~$0.05 | text-embedding-3-small: $0.02 |
| **Multimodal embedding** | Titan Multimodal: $0.06/img | Gemini Embedding 2: $0.20 | Azure Vision: included |

**Winner:** GCP is cheapest for mid-tier (Gemini Flash is 10x cheaper than Claude Sonnet). AWS has the cheapest ultra-budget model (Nova Micro). Azure has the best reasoning models (o3/o4-mini).

### Compute Pricing (Per vCPU-Hour)

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Serverless container (active) | Fargate: $0.04048 | Cloud Run: $0.0864 | Container Apps: $0.0864 |
| Serverless function | Lambda: ~$0.06/GB-hr | Cloud Functions: ~$0.06/GB-hr | Functions: ~$0.06/GB-hr |
| GPU (A100 80GB) | EC2 p4d: ~$4.10/GPU-hr | GCE a2-ultragpu: ~$5.00/GPU-hr | NC A100: ~$3.67/GPU-hr |
| GPU (H100) | EC2 p5: ~$4.13/GPU-hr | GCE a3-mega: ~$5.00/GPU-hr | NC H100: ~$3.96/GPU-hr |
| GPU (Spot/Preemptible) | 60-90% off | 60-91% off | ~60% off |

**Winner:** AWS Fargate is cheapest for always-on containers. GCP Cloud Run wins for bursty (scale-to-zero). Azure has competitive GPU pricing.

### Storage Pricing (Per GB/Month)

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Object storage (standard) | S3: $0.023 | GCS: $0.020 | Blob Hot: $0.018 |
| Object storage (archive) | Glacier Deep: $0.00099 | Archive: $0.0012 | Cool: $0.01 / Archive: $0.002 |
| Managed PostgreSQL | RDS: ~$0.115/hr (r6g.large) | Cloud SQL: ~$0.10/hr | Azure DB: ~$0.10/hr |
| In-memory cache (Redis) | ElastiCache: $0.016/hr (micro) | Memorystore: $0.049/hr (1GB) | Azure Cache: $0.022/hr |
| Vector search (managed) | OpenSearch: $350/mo floor | Vector Search: ~$0.54/node-hr | AI Search: $74/mo (Basic) |

**Winner:** Azure is cheapest for blob storage. AWS has the cheapest cold archive (Glacier Deep). Azure AI Search has the lowest vector search entry cost.

### Database Pricing (Monthly, Small Instance)

| Database | AWS | GCP | Azure |
|----------|-----|-----|-------|
| PostgreSQL (small) | RDS db.t4g.micro: ~$18 | Cloud SQL db-f1-micro: ~$11 | Azure DB B1ms: ~$25 |
| NoSQL (serverless) | DynamoDB: ~$0 (free tier) | Firestore: ~$0 (free tier) | Cosmos DB: ~$25 (400 RU) |
| In-memory cache | ElastiCache: ~$12 | Memorystore: ~$35 | Azure Cache: ~$16 |

**Winner:** DynamoDB free tier is the most generous NoSQL option. GCP Cloud SQL micro is cheapest for PostgreSQL. Azure is generally most expensive for databases.

---

## 11. Architecture Patterns for AI Projects

### Pattern 1: Production RAG on AWS

```
INGESTION:
[Documents] → [S3 Bucket] (versioned, KMS encrypted)
    → [EventBridge] → [Step Functions]
        → [Textract] (PDF/image OCR, table extraction)
        → [Lambda: Chunker] (hierarchical: parent 1500t, child 512t)
        → [Comprehend] (entity extraction → metadata)
        → [Bedrock: Titan V2] (1024-dim embeddings, batch API)
        → [OpenSearch Serverless] (kNN + BM25 hybrid index)

QUERY:
[User] → [API Gateway / ALB] → [Lambda / Fargate]
    → [Bedrock: Titan V2] (embed query)
    → [OpenSearch: Hybrid Search] (BM25 + kNN, k=15)
    → [Bedrock: Cohere Rerank 3.5] (top 5)
    → [Bedrock: Claude Sonnet 4.6] (streaming via SSE)
    → [Response + Citations]

COST: ~$400-500/month (small), ~$700-900 (medium), ~$5K (large)
```

---

### Pattern 2: Autonomous Agent with Tools

```
[User] → [Bedrock Agent] (Claude Sonnet 4.6 as orchestrator)
    ├── [Knowledge Base] → OpenSearch (documentation, policies)
    ├── [Action Group: CRM] → Lambda → Salesforce API
    ├── [Action Group: Email] → Lambda → SES
    ├── [Action Group: Calendar] → Lambda → Google Calendar API
    ├── [Code Interpreter] → Sandboxed Python (data analysis)
    └── [Guardrails] (PII redaction, grounding check)

Agent decides which tool to use, chains multiple calls,
maintains conversation memory across sessions.

COST: ~$0.05-0.20 per agent interaction
```

---

### Pattern 3: Batch ML Processing

```
[Training Data] → [S3]
    → [SageMaker Training Job] (ml.p4d.24xlarge, Spot)
        → [Model Artifacts] → [S3]
        → [SageMaker Model Registry]
    → [SageMaker Endpoint] (ml.g5.xlarge)
        → [Auto-scaling: 1-10 instances]

COST: Training = ~$11/hr (Spot). Inference = ~$1.41/hr per instance.
```

---

### Pattern 4: Real-Time AI Pipeline

```
[Client Events] → [Kinesis Data Streams]
    → [Lambda Consumer] (classify, enrich)
    → [Bedrock: Nova Micro] (real-time classification, ~$0.035/1M)
    → [DynamoDB] (store results)
    → [EventBridge] (trigger downstream)
    → [SNS] (alerts for anomalies)

COST: ~$50-100/month for 1M events/day
```

---

### Pattern 5: Serverless Web API

```
[Client] → [CloudFront] (CDN, SSL)
    → [API Gateway HTTP API] ($1/million)
    → [Lambda (Graviton)] (business logic)
    → [DynamoDB] (data store)
    → [S3] (file storage)

COST: ~$5-20/month for 100K requests/day (mostly free tier)
```

---

## 12. AWS CLI Commands Reference

### Authentication & Configuration

```bash
# Configure CLI
aws configure
aws configure --profile production

# Verify identity
aws sts get-caller-identity

# Assume a role
aws sts assume-role --role-arn arn:aws:iam::ACCOUNT:role/MyRole --role-session-name mysession
```

### S3 Operations

```bash
# Create bucket
aws s3 mb s3://my-bucket-name --region us-east-1

# Upload file
aws s3 cp ./file.pdf s3://my-bucket/documents/

# Sync directory
aws s3 sync ./data/ s3://my-bucket/data/ --exclude "*.tmp"

# Generate presigned URL (1 hour)
aws s3 presign s3://my-bucket/file.pdf --expires-in 3600

# List objects
aws s3 ls s3://my-bucket/documents/ --recursive

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled
```

### Lambda Operations

```bash
# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.12 \
  --handler app.handler \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 256 \
  --architectures arm64

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip

# Invoke (sync)
aws lambda invoke --function-name my-function \
  --payload '{"key": "value"}' output.json

# Add S3 trigger
aws lambda add-permission \
  --function-name my-function \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::my-bucket

# View logs (last 5 minutes)
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -d '-5 minutes' +%s000) \
  --limit 50
```

### ECS Fargate Operations

```bash
# Create cluster
aws ecs create-cluster --cluster-name my-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-api \
  --task-definition my-api:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"

# Update service (deploy new version)
aws ecs update-service \
  --cluster my-cluster \
  --service my-api \
  --task-definition my-api:2 \
  --force-new-deployment

# Scale service
aws ecs update-service --cluster my-cluster --service my-api --desired-count 4

# View running tasks
aws ecs list-tasks --cluster my-cluster --service-name my-api
```

### Bedrock Operations

```bash
# List available models
aws bedrock list-foundation-models --query "modelSummaries[].modelId" --output table

# Invoke model (Claude)
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
  --content-type application/json \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}' \
  output.json

# Create knowledge base
aws bedrock-agent create-knowledge-base \
  --name my-kb \
  --role-arn arn:aws:iam::ACCOUNT:role/bedrock-kb-role \
  --knowledge-base-configuration '{"type":"VECTOR","vectorKnowledgeBaseConfiguration":{"embeddingModelArn":"arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0"}}' \
  --storage-configuration file://storage-config.json

# Sync knowledge base data source
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id KB_ID \
  --data-source-id DS_ID

# Query knowledge base
aws bedrock-agent-runtime retrieve \
  --knowledge-base-id KB_ID \
  --retrieval-query '{"text":"What is the refund policy?"}'
```

### DynamoDB Operations

```bash
# Create table
aws dynamodb create-table \
  --table-name my-table \
  --attribute-definitions AttributeName=pk,AttributeType=S \
  --key-schema AttributeName=pk,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Put item
aws dynamodb put-item \
  --table-name my-table \
  --item '{"pk":{"S":"user-1"},"name":{"S":"Dhruv"},"age":{"N":"25"}}'

# Query
aws dynamodb query \
  --table-name my-table \
  --key-condition-expression "pk = :pk" \
  --expression-attribute-values '{":pk":{"S":"user-1"}}'

# Scan (full table -- use sparingly)
aws dynamodb scan --table-name my-table --max-items 10
```

### RDS / Aurora Operations

```bash
# Create Aurora Serverless v2 cluster
aws rds create-db-cluster \
  --db-cluster-identifier my-aurora \
  --engine aurora-postgresql \
  --engine-version 15.4 \
  --serverless-v2-scaling-configuration MinCapacity=0.5,MaxCapacity=16 \
  --master-username postgres \
  --master-user-password "$DB_PASSWORD" \
  --vpc-security-group-ids sg-xxx

# Create instance for the cluster
aws rds create-db-instance \
  --db-instance-identifier my-aurora-instance \
  --db-cluster-identifier my-aurora \
  --db-instance-class db.serverless \
  --engine aurora-postgresql

# Create RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier my-postgres \
  --db-instance-class db.t4g.micro \
  --engine postgres \
  --engine-version 16 \
  --master-username postgres \
  --master-user-password "$DB_PASSWORD" \
  --allocated-storage 20
```

### ECR Operations

```bash
# Create repository
aws ecr create-repository --repository-name my-api

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build, tag, push
docker build -t my-api .
docker tag my-api:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/my-api:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/my-api:latest

# Lifecycle policy (keep last 10 images)
aws ecr put-lifecycle-policy \
  --repository-name my-api \
  --lifecycle-policy-text '{"rules":[{"rulePriority":1,"selection":{"tagStatus":"any","countType":"imageCountMoreThan","countNumber":10},"action":{"type":"expire"}}]}'
```

### CloudWatch Operations

```bash
# Get metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time 2026-03-01T00:00:00Z \
  --end-time 2026-03-15T00:00:00Z \
  --period 3600 \
  --statistics Average

# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name high-errors \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=my-function \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:alerts

# Set log retention
aws logs put-retention-policy \
  --log-group-name /aws/lambda/my-function \
  --retention-in-days 14
```

### Secrets Manager Operations

```bash
# Create secret
aws secretsmanager create-secret \
  --name my-api-key \
  --secret-string '{"api_key":"sk-xxx","db_password":"xxx"}'

# Get secret value
aws secretsmanager get-secret-value --secret-id my-api-key --query SecretString --output text

# Update secret
aws secretsmanager update-secret \
  --secret-id my-api-key \
  --secret-string '{"api_key":"sk-new","db_password":"xxx"}'
```

---

## 13. When to Choose AWS Over GCP/Azure

### AWS Strengths

1. **Broadest service catalog.** 200+ services. If a managed service exists for your use case, AWS probably has it.

2. **Best model selection on Bedrock.** Claude (Anthropic), Nova (Amazon), Llama (Meta), Mistral, Cohere, AI21, Stability -- all through one API. GCP has fewer third-party models. Azure is mostly OpenAI-only.

3. **Enterprise adoption.** ~33% cloud market share (largest). Most enterprise teams already have AWS accounts, IAM policies, and VPCs. Building there reduces friction.

4. **Most regions and availability zones.** 34 regions, 108 AZs. More than GCP (40 regions) or Azure (60+ regions but fewer AZs per region).

5. **Free tier generosity.** Lambda (1M/month forever), DynamoDB (25GB forever), CloudFront (1TB forever). Most startups run their first year on free tier.

6. **Spot instance ecosystem.** Most mature spot market. Spot Fleet, Spot placement, capacity-optimized allocation. 60-90% savings on GPU training.

7. **Container ecosystem maturity.** ECS/Fargate is the most battle-tested serverless container platform. More production experience than Cloud Run or Container Apps.

8. **Inferentia/Trainium.** Custom AI chips that are 50-70% cheaper than NVIDIA GPUs for inference. No equivalent on GCP/Azure.

9. **S3 Intelligent-Tiering.** Automatic storage class optimization with zero retrieval fees. GCP Autoclass is similar but newer. Azure has no direct equivalent.

10. **Step Functions.** Most mature serverless workflow orchestration. Visual debugging, error handling, retries. GCP Workflows and Azure Durable Functions are less feature-rich.

### AWS Weaknesses

1. **No scale-to-zero containers (Fargate).** You always pay for at least one running task. GCP Cloud Run and Azure Container Apps scale to zero. This matters for dev/staging environments.

2. **Bedrock has no free tier.** You pay from the first token. GCP gives free Gemini API calls. Azure OpenAI has no free tier either, but Azure AI Services have free tiers for Cognitive Services.

3. **Lambda 15-minute timeout.** Shortest of all clouds. GCP Cloud Run functions: 60 minutes. Azure Functions Premium: unlimited. This limits Lambda for long-running AI inference.

4. **Console UX.** AWS Console is functional but dated. GCP Console is cleaner. Azure Portal is the slowest.

5. **Pricing complexity.** More pricing dimensions than any other cloud. NAT Gateway, cross-AZ data transfer, and API Gateway costs are common surprises.

6. **No native GPU on Fargate/Lambda.** For GPU inference, you must use EC2, SageMaker, or EKS. GCP Cloud Run has GPU support. Azure Container Apps has GPU support.

7. **OpenSearch Serverless floor ($350/month).** The minimum vector search cost is high for small projects. GCP Vector Search and Azure AI Search have lower entry points.

8. **SageMaker 20-40% premium over EC2.** Managed ML infrastructure is expensive. If you have infra expertise, raw EC2 is much cheaper.

### Decision Matrix

| Scenario | Best Cloud | Why |
|----------|-----------|-----|
| Multi-model AI (Claude + Llama + Mistral) | **AWS** | Bedrock has the broadest model catalog |
| Cheapest LLM inference | **GCP** | Gemini Flash is 10x cheaper than Claude |
| Enterprise with existing Microsoft stack | **Azure** | Office 365, Teams, Entra ID integration |
| RAG system (startup) | **AWS** | Bedrock KB + Aurora pgvector = fastest path |
| RAG system (enterprise) | **Azure** | AI Search has best hybrid search + semantic ranking |
| GPU training (cost-first) | **AWS** | Best spot market, Trainium is cheapest |
| Scale-to-zero containers | **GCP** | Cloud Run is best-in-class |
| Event-driven serverless | **AWS** | Lambda + EventBridge + Step Functions is unmatched |
| Mobile app backend | **GCP** | Firebase is far ahead of Amplify/Azure |
| Data analytics | **GCP** | BigQuery is the industry standard |
| Government/compliance | **AWS/Azure** | GovCloud + FedRAMP. Azure has IL5/IL6. |
| India-based workloads | **AWS** | Mumbai (ap-south-1) has best service coverage in India |

---

## 14. Quick Start Templates

### 14.1 FastAPI on ECS Fargate

**Dockerfile:**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy script:**

```bash
#!/bin/bash
# deploy-fargate.sh

REGION="us-east-1"
CLUSTER="my-cluster"
SERVICE="my-api"
ECR_REPO="ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/my-api"

# 1. Login to ECR
aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin $ECR_REPO

# 2. Build and push
docker build -t my-api .
docker tag my-api:latest $ECR_REPO:latest
docker push $ECR_REPO:latest

# 3. Force new deployment (rolling update)
aws ecs update-service \
  --cluster $CLUSTER \
  --service $SERVICE \
  --force-new-deployment \
  --region $REGION

echo "Deployment started. Monitor with:"
echo "aws ecs describe-services --cluster $CLUSTER --services $SERVICE --query 'services[0].deployments'"
```

**Task Definition (task-definition.json):**

```json
{
    "family": "my-api",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "512",
    "memory": "1024",
    "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
    "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
    "containerDefinitions": [
        {
            "name": "api",
            "image": "ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/my-api:latest",
            "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
            "environment": [
                {"name": "AWS_REGION", "value": "us-east-1"}
            ],
            "secrets": [
                {"name": "API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:my-api-key"}
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/my-api",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs"
                }
            },
            "healthCheck": {
                "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
                "interval": 30,
                "timeout": 5,
                "retries": 3
            }
        }
    ]
}
```

---

### 14.2 Lambda + API Gateway (HTTP API)

**Lambda function (handler.py):**

```python
"""Lambda handler with API Gateway HTTP API."""
import json
import boto3
import os

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def handler(event, context):
    """Handle API Gateway HTTP API event."""
    body = json.loads(event.get("body", "{}"))
    message = body.get("message", "")

    if not message:
        return {"statusCode": 400, "body": json.dumps({"error": "message required"})}

    # Call Claude via Bedrock
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
        contentType="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": message}]
        })
    )

    result = json.loads(response["body"].read())
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "response": result["content"][0]["text"],
            "model": result["model"],
            "usage": result["usage"]
        })
    }
```

**Deploy:**

```bash
# Package
zip function.zip handler.py

# Create function
aws lambda create-function \
  --function-name bedrock-chat \
  --runtime python3.12 \
  --handler handler.handler \
  --role arn:aws:iam::ACCOUNT:role/lambda-bedrock-role \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 256 \
  --architectures arm64

# Create HTTP API
API_ID=$(aws apigatewayv2 create-api \
  --name bedrock-chat-api \
  --protocol-type HTTP \
  --query "ApiId" --output text)

# Create Lambda integration
INTEGRATION_ID=$(aws apigatewayv2 create-integration \
  --api-id $API_ID \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:lambda:us-east-1:ACCOUNT:function:bedrock-chat \
  --payload-format-version 2.0 \
  --query "IntegrationId" --output text)

# Create route
aws apigatewayv2 create-route \
  --api-id $API_ID \
  --route-key "POST /chat" \
  --target "integrations/$INTEGRATION_ID"

# Create deployment
aws apigatewayv2 create-stage --api-id $API_ID --stage-name '$default' --auto-deploy

# Grant API Gateway permission
aws lambda add-permission \
  --function-name bedrock-chat \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:ACCOUNT:$API_ID/*"

echo "API URL: https://$API_ID.execute-api.us-east-1.amazonaws.com/chat"
```

---

### 14.3 S3 + Presigned URLs (Upload & Download)

```python
"""S3 presigned URL pattern for file upload/download."""
import boto3
from botocore.config import Config
from datetime import datetime

s3 = boto3.client("s3", config=Config(signature_version="s3v4"))
BUCKET = "my-app-uploads"


def generate_upload_url(filename: str, content_type: str = "application/pdf", expires: int = 900) -> dict:
    """Generate presigned URL for direct browser upload (15 min default)."""
    key = f"uploads/{datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"

    url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires,
    )
    return {"upload_url": url, "key": key, "expires_in": expires}


def generate_download_url(key: str, expires: int = 3600) -> str:
    """Generate presigned URL for download (1 hour default)."""
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )


# CORS configuration (required for browser uploads)
cors_config = {
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST"],
            "AllowedOrigins": ["https://myapp.com"],
            "MaxAgeSeconds": 3600,
        }
    ]
}
s3.put_bucket_cors(Bucket=BUCKET, CORSConfiguration=cors_config)
```

---

### 14.4 DynamoDB CRUD Pattern

```python
"""DynamoDB CRUD with boto3."""
import boto3
from datetime import datetime, timezone
from uuid import uuid4
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-items")


# CREATE
def create_item(data: dict) -> dict:
    item = {
        "pk": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    table.put_item(Item=item)
    return item


# READ (single)
def get_item(pk: str) -> dict | None:
    response = table.get_item(Key={"pk": pk})
    return response.get("Item")


# READ (query by GSI)
def query_by_status(status: str, limit: int = 50) -> list[dict]:
    response = table.query(
        IndexName="status-index",
        KeyConditionExpression=Key("status").eq(status),
        Limit=limit,
        ScanIndexForward=False,  # newest first
    )
    return response["Items"]


# UPDATE
def update_item(pk: str, updates: dict) -> dict:
    expr_names = {}
    expr_values = {}
    update_parts = []

    for key, value in updates.items():
        safe_key = f"#{key}"
        safe_val = f":{key}"
        expr_names[safe_key] = key
        expr_values[safe_val] = value
        update_parts.append(f"{safe_key} = {safe_val}")

    expr_names["#updated_at"] = "updated_at"
    expr_values[":updated_at"] = datetime.now(timezone.utc).isoformat()
    update_parts.append("#updated_at = :updated_at")

    response = table.update_item(
        Key={"pk": pk},
        UpdateExpression="SET " + ", ".join(update_parts),
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values,
        ReturnValues="ALL_NEW",
    )
    return response["Attributes"]


# DELETE
def delete_item(pk: str):
    table.delete_item(Key={"pk": pk})


# BATCH WRITE (up to 25 items)
def batch_create(items: list[dict]):
    with table.batch_writer() as batch:
        for item in items:
            item["pk"] = str(uuid4())
            item["created_at"] = datetime.now(timezone.utc).isoformat()
            batch.put_item(Item=item)


# CONDITIONAL WRITE (optimistic locking)
def update_if_version_matches(pk: str, updates: dict, expected_version: int):
    try:
        table.update_item(
            Key={"pk": pk},
            UpdateExpression="SET #data = :data, #version = :new_version",
            ConditionExpression="#version = :expected_version",
            ExpressionAttributeNames={"#data": "data", "#version": "version"},
            ExpressionAttributeValues={
                ":data": updates,
                ":new_version": expected_version + 1,
                ":expected_version": expected_version,
            },
        )
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        raise Exception("Version conflict -- item was modified by another process")
```

---

### 14.5 Bedrock Chat with Streaming

```python
"""Bedrock Claude streaming chat with FastAPI SSE."""
import json
import boto3
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    model: str = "anthropic.claude-3-5-haiku-20241022-v1:0"
    max_tokens: int = 2048


@app.post("/chat")
async def chat(request: ChatRequest):
    """Stream Claude response via SSE."""

    response = bedrock.invoke_model_with_response_stream(
        modelId=request.model,
        contentType="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "system": request.system_prompt,
            "messages": [{"role": "user", "content": request.message}],
        }),
    )

    async def generate():
        for event in response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if chunk["type"] == "content_block_delta":
                text = chunk["delta"].get("text", "")
                if text:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            elif chunk["type"] == "message_stop":
                yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

## Appendix A: AWS Service -> GCP -> Azure Mapping

| AWS Service | GCP Equivalent | Azure Equivalent |
|------------|----------------|-----------------|
| EC2 | Compute Engine | Virtual Machines |
| Lambda | Cloud Run Functions | Azure Functions |
| ECS Fargate | Cloud Run | Container Apps |
| EKS | GKE | AKS |
| App Runner | Cloud Run (closest) | Container Apps |
| Elastic Beanstalk | App Engine | App Service |
| Lightsail | -- | -- |
| S3 | Cloud Storage | Blob Storage |
| DynamoDB | Firestore | Cosmos DB |
| RDS | Cloud SQL | Azure Database |
| Aurora | AlloyDB | Azure Database (Hyperscale) |
| OpenSearch | Vertex AI Search | Azure AI Search |
| ElastiCache | Memorystore | Azure Cache for Redis |
| Neptune | -- | Cosmos DB (Gremlin) |
| Timestream | Bigtable (partial) | -- |
| DocumentDB | Firestore (partial) | Cosmos DB (MongoDB API) |
| Bedrock | Vertex AI (Model Garden) | Azure OpenAI + AI Foundry |
| SageMaker | Vertex AI | Azure Machine Learning |
| Textract | Document AI | Document Intelligence |
| Comprehend | Natural Language AI | AI Language |
| Transcribe | Speech-to-Text | AI Speech |
| Polly | Text-to-Speech | AI Speech (TTS) |
| Rekognition | Vision AI | AI Vision |
| Kendra | Vertex AI Search | Azure AI Search |
| Translate | Translation AI | Translator |
| CloudFront | Cloud CDN | Front Door / CDN |
| ALB / NLB | Cloud Load Balancing | Load Balancer |
| Route 53 | Cloud DNS | Azure DNS |
| API Gateway | API Gateway (Apigee) | API Management |
| VPC | VPC | VNet |
| PrivateLink | Private Service Connect | Private Link |
| SQS | Pub/Sub (pull) | Storage Queue / Service Bus |
| SNS | Pub/Sub (push) | Event Grid / Service Bus |
| EventBridge | Eventarc | Event Grid |
| Step Functions | Workflows | Logic Apps / Durable Functions |
| Kinesis | Dataflow | Event Hubs |
| IAM | IAM | Entra ID + RBAC |
| Secrets Manager | Secret Manager | Key Vault |
| KMS | Cloud KMS | Key Vault |
| WAF | Cloud Armor | WAF |
| Shield | Cloud Armor (DDoS) | DDoS Protection |
| Cognito | Firebase Auth / Identity Platform | Entra ID B2C |
| CodeBuild | Cloud Build | Azure Pipelines |
| CodePipeline | Cloud Build (triggers) | Azure Pipelines |
| ECR | Artifact Registry | Container Registry |
| CodeDeploy | Cloud Deploy | Azure DevOps |
| CDK | -- (use Terraform/Pulumi) | Bicep |
| CloudWatch | Cloud Monitoring + Logging | Monitor + Log Analytics |
| X-Ray | Cloud Trace | Application Insights |
| CloudTrail | Cloud Audit Logs | Activity Log |
| Amplify | Firebase | Static Web Apps |
| SES | -- (use SendGrid) | Communication Services |

---

## Appendix B: AWS Regions for AI Workloads

**Best regions for Bedrock + GPU availability:**

| Region | Bedrock Models | GPU (EC2) | Latency (from US) | Notes |
|--------|---------------|-----------|-------------------|-------|
| us-east-1 (N. Virginia) | All | All (P5, G6, Inf2, Trn1) | Low | Primary region, most services |
| us-west-2 (Oregon) | All | All | Low | Second-best, good GPU availability |
| eu-west-1 (Ireland) | Most | P4d, G5 | Medium | EU data residency |
| eu-central-1 (Frankfurt) | Most | G5 | Medium | GDPR compliance |
| ap-south-1 (Mumbai) | Limited | G5, G4dn | High (from US) | India workloads |
| ap-northeast-1 (Tokyo) | Most | P4d, G5 | High (from US) | Japan/APAC |
| ap-southeast-1 (Singapore) | Limited | G5 | High (from US) | Southeast Asia |

**Recommendation:** Start with `us-east-1` for AI workloads. Best model availability, cheapest pricing, most GPU capacity.

---

## Appendix C: Cost Optimization Checklist

- [ ] Use Graviton (ARM) instances everywhere possible (20% cheaper, 20% faster)
- [ ] Enable S3 Intelligent-Tiering for all buckets (zero-effort cost optimization)
- [ ] Use Savings Plans (1-year compute) for steady-state workloads (up to 54% savings)
- [ ] Use Spot instances for fault-tolerant training (60-90% savings)
- [ ] Set Lambda memory to minimum needed (test with AWS Lambda Power Tuning)
- [ ] Use Lambda Graviton (arm64) architecture (20% cheaper)
- [ ] Use API Gateway HTTP API instead of REST API (71% cheaper)
- [ ] Use VPC Gateway endpoints for S3/DynamoDB (free, avoid NAT Gateway costs)
- [ ] Replace NAT Gateway with fck-nat ($3/mo vs $33/mo) where possible
- [ ] Set CloudWatch log retention (7d dev, 30d prod -- avoid infinite retention)
- [ ] Use DynamoDB on-demand mode until traffic is predictable
- [ ] Use Bedrock batch inference for embedding ingestion (50% cheaper)
- [ ] Use Titan V2 at 256 dims (MRL) for cost-sensitive RAG (75% less vector storage)
- [ ] Use Nova Micro ($0.035/1M input) for simple classification instead of Claude
- [ ] Use ElastiCache Serverless instead of provisioned for variable workloads
- [ ] Use Aurora Serverless v2 instead of provisioned for variable DB workloads
- [ ] Set ECR lifecycle policies (keep last 10 images, delete old ones)
- [ ] Schedule dev/staging Fargate tasks to stop nights/weekends (67% savings)
- [ ] Enable S3 data transfer pricing free egress (first 100 GB/month always free)
- [ ] Use Bedrock Intelligent Prompt Routing (auto-route to cheaper model when possible)
- [ ] Set budget alerts at 50%, 80%, 100% of monthly target
- [ ] Review Cost Explorer weekly (AWS Billing -> Cost Explorer)
- [ ] Use the AWS Pricing Calculator before deploying anything new

---

## Appendix D: Python SDK Packages for AI Projects

```bash
# Core
pip install boto3                      # AWS SDK for Python
pip install botocore                   # Low-level AWS SDK (installed with boto3)

# AI / ML
pip install anthropic                  # Claude API (direct, not via Bedrock)
# For Bedrock: use boto3.client("bedrock-runtime")
pip install langchain-aws              # LangChain + Bedrock integration
pip install llama-index-llms-bedrock   # LlamaIndex + Bedrock

# Database
pip install asyncpg                    # PostgreSQL async (Aurora/RDS)
pip install psycopg2-binary            # PostgreSQL sync
pip install pgvector                   # pgvector Python support

# Storage
# S3 access via boto3 (no extra package)

# Search
pip install opensearch-py              # OpenSearch client
pip install requests-aws4auth          # AWS Signature V4 for OpenSearch

# Monitoring
pip install aws-xray-sdk               # X-Ray tracing
pip install watchtower                  # CloudWatch Logs handler for Python logging

# Infrastructure
pip install aws-cdk-lib                 # AWS CDK (Python)
pip install constructs                  # CDK constructs

# Serverless
pip install mangum                      # ASGI adapter for Lambda (FastAPI on Lambda)
pip install aws-lambda-powertools       # Lambda utilities (logging, tracing, metrics)
```

---

*This document is a living reference. AWS pricing and features change regularly. Always verify at [aws.amazon.com/pricing](https://aws.amazon.com/pricing) before making architecture or purchasing decisions. Last updated: March 15, 2026.*
