# Google Cloud Platform (GCP) for AI/ML Projects -- Exhaustive Reference

> **Last updated:** March 2026
> **Scope:** Everything a 10-year GCP veteran knows -- pricing, architecture, CLI, trade-offs, free tier, and AWS comparisons.
> **Pricing note:** All prices are USD unless stated otherwise. Prices reflect published rates as of early 2026. GCP pricing changes; always verify at cloud.google.com/pricing before committing spend.

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
10. [Pricing Comparisons vs AWS](#10-pricing-comparisons-vs-aws)
11. [Architecture Patterns for AI Projects](#11-architecture-patterns-for-ai-projects)
12. [GCP CLI Commands Reference](#12-gcp-cli-commands-reference)
13. [When to Choose GCP Over AWS/Azure](#13-when-to-choose-gcp-over-awsazure)
14. [Quick Start Templates](#14-quick-start-templates)

---

## 1. AI/ML Services (Deep Dive)

### 1.1 Vertex AI -- The Unified ML Platform

Vertex AI is Google's unified AI/ML platform. It consolidates AutoML, custom training, model deployment, MLOps, and generative AI into a single surface. Think of it as GCP's answer to AWS SageMaker, but with tighter Gemini integration.

**Core Components:**

| Component | What It Does | AWS Equivalent |
|-----------|-------------|----------------|
| Model Garden | 200+ pre-trained models (Gemini, Claude, Llama, Mistral, open-source) | SageMaker JumpStart |
| Feature Store | Centralized feature management for ML | SageMaker Feature Store |
| Pipelines | Kubeflow-based ML workflow orchestration | SageMaker Pipelines |
| AutoML | No-code model training (tabular, image, text, video) | SageMaker Autopilot |
| Custom Training | Bring your own code (PyTorch, TF, JAX) on managed infrastructure | SageMaker Training Jobs |
| Endpoints | Online (real-time) and batch prediction serving | SageMaker Endpoints |
| Experiments | Track hyperparameters, metrics, artifacts | SageMaker Experiments |
| Model Registry | Version and manage models | SageMaker Model Registry |
| Vertex AI Workbench | Managed Jupyter notebooks | SageMaker Studio |

**Pricing (Key Components):**

| Resource | Price | Notes |
|----------|-------|-------|
| Custom Training (e2-standard) | $0.218/hr | Billed in 30-second increments |
| AutoML Training (tabular) | $3.465/node-hour | Minimum 1 hour |
| AutoML Training (image/text/video) | $3.465/node-hour | Higher for edge models |
| Online Prediction (e2-standard) | $0.0456/vCPU-hr | Billed per second after first minute |
| Batch Prediction | $0.0456/vCPU-hr | Same as online but batch-optimized |
| Feature Store (online) | $0.36/GB stored/month | Plus $0.023 per 1M reads |
| Feature Store (offline) | BigQuery pricing applies | Standard BQ rates |
| Vertex AI Workbench | $0.0456/vCPU-hr | Same as Compute Engine pricing |
| Ray on Vertex AI | $0.228/hr | For distributed training |
| Model upload/registration | Free | No charge for model artifacts |

**When to use Vertex AI vs. raw Compute Engine:**
- **Vertex AI:** When you need managed training, auto-scaling endpoints, experiment tracking, or pipeline orchestration. The 15-25% premium over raw compute is worth it for operational overhead savings.
- **Raw Compute Engine:** When you have a dedicated ML infra team, need full control, or are running long-lived training jobs where you can manage your own checkpointing and recovery.

**Critical veteran insight:** Vertex AI Pipelines uses Kubeflow Pipelines v2 under the hood. If you are coming from Airflow, expect a learning curve. The pipeline YAML compilation step is where most teams waste time. Use the `kfp` Python SDK v2 to author pipelines programmatically.

---

### 1.2 Gemini Models

Gemini is Google's frontier multimodal model family. As of March 2026, the lineup is:

| Model | Context Window | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|-------|---------------|----------------------|------------------------|----------|
| **Gemini 2.0 Flash** | 1M tokens | $0.10 | $0.40 | High-throughput, low-cost tasks |
| **Gemini 2.0 Flash-Lite** | 1M tokens | $0.10 | $0.40 | Fastest latency, simplest tasks |
| **Gemini 2.5 Flash** | 1M tokens | $0.30 | $2.50 | Best price/performance for most tasks |
| **Gemini 2.5 Pro** | 1M tokens | $1.25 (<=200K) / $2.50 (>200K) | $10.00 (<=200K) / $15.00 (>200K) | Complex reasoning, code, analysis |
| **Gemini 3 Flash Preview** | 1M tokens | $0.50 | $3.00 | Latest Flash capabilities |
| **Gemini 3 Pro Preview** | 1M tokens | $2.00 (<=200K) / $4.00 (>200K) | $12.00 (<=200K) / $18.00 (>200K) | Frontier reasoning |
| **Gemini Nano** | On-device | Free (on-device) | Free (on-device) | Mobile/edge inference |

**Multimodal Capabilities (all Pro/Flash models):**
- **Text:** Full conversational, coding, reasoning
- **Images:** Up to 3,600 images per request (with context window limits)
- **Video:** Frame-by-frame understanding, temporal reasoning
- **Audio:** Native audio understanding, speech recognition
- **PDF/Docs:** Native document understanding without OCR
- **Code:** Generation, debugging, explanation, multi-file understanding

**When to use which model:**

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| Chatbot / customer support | 2.5 Flash | Best price/performance |
| Complex reasoning / planning | 2.5 Pro or 3 Pro | Highest accuracy |
| High-throughput classification | 2.0 Flash-Lite | Cheapest, fastest |
| Code generation (production) | 2.5 Pro | Best code quality |
| Real-time voice assistant | 2.0 Flash | Lowest latency |
| On-device (mobile) | Nano | Zero API cost |
| Multimodal RAG | 2.5 Flash or Pro | Native multimodal |
| Long-document analysis (>200K) | 2.5 Flash | No price doubling unlike Pro |

**Pro model pricing trap:** Pro models (2.5 Pro, 3 Pro) charge 2x for prompts exceeding 200K tokens. If you regularly process long documents, Flash models have flat pricing at any context length -- often a better deal.

**Vertex AI vs. Google AI Studio pricing:** Identical model pricing. The difference is Vertex AI adds enterprise features (VPC-SC, CMEK, SLA, data residency, IAM). Use Vertex AI for production; Google AI Studio for prototyping.

**Free tier (Google AI Studio only):**
- 2.0 Flash: 15 RPM, 1M TPM, 1500 RPD
- 2.5 Pro: 5 RPM, 250K TPM, 25 RPD

---

### 1.3 Embeddings

**Current Models (March 2026):**

| Model | Dimensions | Max Tokens | Price (per 1M tokens) | MRL Support | Languages |
|-------|-----------|-----------|----------------------|-------------|-----------|
| **Gemini Embedding 2** (gemini-embedding-exp-03-07) | 3072 (default), 1536, 768 | 8,192 | $0.20 (online) / $0.10 (batch) | Yes | 100+ |
| **text-embedding-005** | 768 (default), 256 | 2,048 | $0.025/1K chars | Yes | English-primary |
| **text-multilingual-embedding-002** | 768 | 2,048 | $0.025/1K chars | No | 100+ languages |
| ~~text-embedding-004~~ | ~~768~~ | ~~2,048~~ | ~~$0.025/1K chars~~ | No | **DEPRECATED Jan 2026** |

**Gemini Embedding 2 -- The Game Changer (March 2026):**
- **First multimodal embedding model** from Google
- Maps text, images, video, audio, and PDFs into a single vector space
- Matryoshka Representation Learning (MRL) -- dynamically scale dimensions from 3072 down to 768
- Processes up to 6 images, 120 seconds of video, or native audio per request
- 70% latency reduction vs. running separate text + image embedding pipelines
- MTEB leaderboard competitive (top 5 as of March 2026)

**Normalization:** All GCP embedding models return normalized vectors (L2 norm = 1). You do NOT need to normalize before storing in a vector DB. This is different from OpenAI's `text-embedding-3-*` which also returns normalized vectors, but some older models (ada-002) did not.

**Which embedding to use:**

| Use Case | Model | Why |
|----------|-------|-----|
| Text-only RAG (English) | text-embedding-005 | Cheapest, good quality |
| Text-only RAG (multilingual) | text-multilingual-embedding-002 | Best multilingual retrieval |
| Multimodal RAG (text + images + video) | Gemini Embedding 2 | Only model that does it all |
| Cost-sensitive high-volume | text-embedding-005 at 256 dims | Smallest vectors, lowest storage |
| Highest quality retrieval | Gemini Embedding 2 at 3072 dims | Best MTEB scores |

**AWS comparison:**
- AWS Titan Embeddings v2: 1024 dims, $0.02/1M tokens -- slightly cheaper than Gemini Embedding 2 but text-only
- OpenAI text-embedding-3-large: 3072 dims, $0.13/1M tokens -- more expensive than Gemini Embedding 2

---

### 1.4 Vertex AI Search (Vector Search)

Formerly known as Matching Engine. This is GCP's managed vector database for similarity search.

**Index Types:**

| Type | Best For | Latency | Recall | Cost |
|------|---------|---------|--------|------|
| **TreeAH (Tree-based Approximate Hashing)** | Large datasets (>1M vectors), production | ~5-10ms | 95%+ (tunable) | Lower per-query |
| **Brute Force** | Small datasets (<100K), exact search | Higher | 100% | Higher per-query |

**Pricing:**

| Resource | Price | Notes |
|----------|-------|-------|
| Data processed | $3.00/GiB | Across all regions |
| Streaming updates (inserts) | $0.45/GiB ingested | For real-time updates |
| Deployed index (per node-hour) | Varies by machine type | e2-standard-16: ~$0.54/hr |
| Queries | Included in node cost | No per-query charge |

**Free credits:** $1,000 in trial credits for new Vector Search users (1-year validity).

**Hybrid Search:** Vector Search supports combining vector similarity with metadata filtering (pre-filter and post-filter). For true hybrid (keyword + semantic), combine with Vertex AI Search (the search product) which does BM25 + vector natively.

**Vertex AI Search (the product, not Vector Search):**

| Feature | Price | Free Tier |
|---------|-------|-----------|
| Search queries | Varies by tier | 10,000 queries/month free |
| Generative answers | $6.00/1,000 requests | Not included in free tier |
| Grounding with own data | $2.50/1,000 requests | On top of model costs |
| Grounding with Google Search | Per-query (varies) | Only charged on successful grounding |

**AWS equivalent:** Amazon OpenSearch Serverless (for vector search) + Amazon Kendra (for enterprise search). GCP's Vector Search is generally cheaper for high-QPS workloads because you pay per node-hour, not per query.

---

### 1.5 Vertex AI Agent Builder

The managed platform for building AI agents with grounding, RAG, and conversation capabilities.

**Components:**

| Component | What It Does | Pricing |
|-----------|-------------|---------|
| **Grounding** | Connect Gemini to Google Search or your own data | $2.50/1K requests (own data), per-query (Google Search) |
| **RAG Engine** | Managed retrieval-augmented generation pipeline | Embedding + search + model costs |
| **Agent Engine Runtime** | Host and run agents | Charged since Nov 2025 |
| **Sessions & Memory Bank** | Conversation state management | Charged since Feb 2026 |
| **Code Execution** | Run generated code in sandbox | Charged since Feb 2026 |
| **Conversation** | Multi-turn dialogue management | $6.00/1K requests |

**RAG Engine billing breakdown:**
1. Document ingestion: embedding model cost + storage
2. Retrieval: Vector Search node cost
3. Generation: Gemini model cost
4. Total per RAG query: typically $0.002-0.01 depending on model and document size

**When to use Agent Builder vs. DIY:**
- **Agent Builder:** Quick prototyping, Google Search grounding needed, < 6 months to production
- **DIY (LangChain/LlamaIndex + Cloud Run):** Full control over retrieval, custom ranking, cost optimization at scale, non-Google LLMs

---

### 1.6 Document AI

**Processors:**

| Processor | What It Does | Price (per page) | Free Tier |
|-----------|-------------|-----------------|-----------|
| **Enterprise Document OCR** | High-accuracy text extraction | $0.01 (1-5M pages), $0.004 (>5M) | 1,000 pages/month |
| **Form Parser** | Extract key-value pairs from forms | $0.10 per document (1-10 pages) | 1,000 pages/month |
| **Invoice Parser** | Structured invoice data extraction | $0.10-0.30 per document | Limited free |
| **Receipt Parser** | Receipt data extraction | $0.10-0.30 per document | Limited free |
| **Identity Document Parser** | ID/passport/license extraction | $0.10-0.30 per document | Limited free |
| **Contract Parser** | Legal contract analysis | $0.10-0.30 per document | Limited free |
| **Lending Document Parser** | Mortgage/loan docs | $0.10-0.30 per document | Limited free |
| **Custom Extractor** | Train on your document types | $0.10+ per document | — |

**Pricing model:** Per-document, where 1 document = 1-10 pages at the base price. Documents with 11-20 pages cost 2x.

**AWS equivalent:** Amazon Textract. GCP Document AI is generally cheaper for high-volume OCR ($0.004/page vs Textract's $0.0015/page for detect text, but Document AI includes layout understanding). For form extraction, Document AI Form Parser at $0.10/doc is comparable to Textract Forms at $0.05/page.

**Veteran tip:** For simple OCR, use the Vision API (Cloud Vision) instead of Document AI -- it's cheaper at $1.50/1000 pages and sufficient for clean printed text. Document AI shines on complex layouts, tables, and handwriting.

---

### 1.7 Speech-to-Text / Text-to-Speech

**Speech-to-Text (STT):**

| Model | Price (per minute) | Free Tier | Best For |
|-------|-------------------|-----------|----------|
| **Chirp 2** (latest) | $0.016/min | 60 min/month | Highest accuracy, 100+ languages |
| **Chirp** (v1) | $0.016/min | 60 min/month | Production-grade, 85+ languages |
| **V2 (Long)** | $0.012/min | 60 min/month | Long-form audio (>1 min) |
| **V2 (Short)** | $0.016/min | 60 min/month | Short utterances (<1 min) |
| **V1 (Standard)** | $0.006/min | 60 min/month | Legacy, good enough for English |

**Key features:**
- Real-time streaming transcription
- Speaker diarization (who said what)
- Word-level timestamps
- Automatic punctuation
- Profanity filtering
- Multi-channel recognition
- Medical/phone call enhanced models

**Text-to-Speech (TTS):**

| Voice Type | Price (per 1M chars) | Free Tier (per month) | Quality |
|-----------|---------------------|----------------------|---------|
| **Standard** | $4.00 | 4M chars | Basic, robotic |
| **WaveNet** | $16.00 | 1M chars | Natural, DeepMind |
| **Neural2** | $16.00 | 1M chars | Latest, most natural |
| **Studio** | $160.00 | 100K chars | Premium, voice cloning |
| **Journey** | $16.00 | 1M chars | Conversational style |

- 380+ voices across 75+ languages
- SSML support for pronunciation control
- Custom voice (requires enterprise agreement)

**AWS comparison:** Amazon Transcribe is $0.024/min (standard) vs GCP's $0.016/min -- GCP is 33% cheaper. Amazon Polly Neural is $16.00/1M chars -- same as WaveNet. GCP wins on STT pricing; TTS is roughly equivalent.

---

### 1.8 Vision AI

| Feature | Price (per 1K units) | Free Tier |
|---------|---------------------|-----------|
| Label detection | $1.50 | 1,000 units/month |
| Text detection (OCR) | $1.50 | 1,000 units/month |
| Document text detection | $1.50 (1-5M), $0.60 (>5M) | 1,000 pages/month |
| Face detection | $1.50 | 1,000 units/month |
| Landmark detection | $1.50 | 1,000 units/month |
| Logo detection | $1.50 | 1,000 units/month |
| Object localization | $2.25 | 1,000 units/month |
| Explicit content detection | $1.50 | 1,000 units/month |
| Web detection | $3.50 | — |
| Product search | Setup + $4.50/1K queries | — |

**AWS equivalent:** Amazon Rekognition. Pricing is comparable. GCP's OCR (Vision API text detection) is often preferred for mixed-language documents.

---

### 1.9 Natural Language AI

| Feature | Price (per 1K units) | Free Tier |
|---------|---------------------|-----------|
| Entity analysis | $1.00 | 5,000 units/month |
| Sentiment analysis | $1.00 | 5,000 units/month |
| Syntax analysis | $0.50 | 5,000 units/month |
| Content classification | $2.00 | 30K units/month |
| Entity sentiment analysis | $2.00 | — |
| Custom entity extraction | $5.00/1K (plus training costs) | — |
| Custom classification | $5.00/1K (plus training costs) | — |

**Veteran insight:** For most NLP tasks (entity extraction, sentiment, classification), using Gemini 2.0 Flash with a prompt is now cheaper AND more accurate than the dedicated Natural Language API. The API exists for legacy workloads and batch processing where you need deterministic outputs.

---

### 1.10 Translation AI

| Feature | Price (per 1M chars) | Free Tier |
|---------|---------------------|-----------|
| Neural Machine Translation (NMT) v3 | $20.00 | 500K chars/month (never expires) |
| Basic Translation v2 | $20.00 | 500K chars/month |
| Custom/AutoML Translation | $45.00 | — |
| Document translation | $0.08/page | Not included in free tier |
| Adaptive translation | $40.00/1M chars | — |
| LLM translation | Model pricing applies | — |

**Key advantage over AWS Translate:** GCP's free tier (500K chars/month) never expires. AWS Translate gives 2M chars/month but only for 12 months.

---

## 2. Compute & Deployment

### 2.1 Cloud Run -- Best Serverless Containers in the Industry

Cloud Run is GCP's flagship serverless container platform. It runs any Docker container, scales to zero, and is the recommended deployment target for most GCP workloads (Google themselves now recommends Cloud Run over App Engine).

**Pricing:**

| Resource | Price | Free Tier (per month) |
|----------|-------|----------------------|
| vCPU | $0.00002400/vCPU-second | 180,000 vCPU-seconds |
| Memory | $0.00000250/GiB-second | 360,000 GiB-seconds |
| Requests | $0.40/million | 2 million requests |
| Networking (egress) | $0.12/GB (first 1TB) | 1 GB/month |
| GPU (NVIDIA L4) | $0.000187/second (~$0.67/hr) | None |

**Limits:**

| Limit | Value |
|-------|-------|
| Max vCPUs | 8 (without GPU), 4 (with GPU) |
| Max memory | 32 GiB (without GPU), 24 GiB (with GPU) |
| Max request timeout | 3,600 seconds (60 min) |
| Max instances | 1,000 (adjustable) |
| Min instances | 0 (scale to zero) or configurable |
| Max concurrency | 1,000 per instance |
| Container image size | 32 GB |
| GPU types | NVIDIA L4 (GA) |

**Cold starts:**
- Typical: 0.5-3 seconds (language/image dependent)
- With GPU: ~5 seconds
- Mitigation: Set `min-instances >= 1` (always-on, billed at reduced idle rate)
- Idle instance cost: ~25% of active cost

**GPU support (GA since late 2025):**
- NVIDIA L4 only (24GB VRAM)
- ~$0.67/hr without zonal redundancy
- ~$1.05/hr with zonal redundancy
- Auto-scales GPU instances based on traffic
- Best for: inference (Llama, Whisper, Stable Diffusion), not training

**Scale-to-zero vs. always-on:**

| Mode | When to Use | Cost Impact |
|------|------------|-------------|
| Scale-to-zero (min=0) | Dev/staging, infrequent traffic | $0 when idle |
| Always-on (min>=1) | Production APIs, low-latency required | ~$15-30/month per warm instance |

**Veteran tips:**
1. Set concurrency to 80-250 for web APIs (not 1). Cloud Run can handle multiple requests per instance.
2. Use `--cpu-boost` flag to double CPU during startup (reduces cold starts by 50%).
3. For AI inference: use Cloud Run with GPU + min-instances=1. Cheaper than maintaining a GKE cluster for sporadic inference loads.
4. Cloud Run Jobs (for batch work) have a max timeout of 24 hours and can run up to 10,000 tasks in parallel.

---

### 2.2 Cloud Functions (Cloud Run Functions)

As of 2025, Cloud Functions gen2 IS Cloud Run under the hood. Google rebranded gen2 as "Cloud Run functions."

**Gen1 vs Gen2 comparison:**

| Feature | Gen1 | Gen2 (Cloud Run functions) |
|---------|------|---------------------------|
| Max execution time | 540 seconds (9 min) | 3,600 seconds (60 min) |
| Max memory | 8 GB | 32 GB |
| Max vCPUs | 2 | 8 |
| Concurrency | 1 request/instance | Up to 1,000/instance |
| Triggers | HTTP, Pub/Sub, Storage, Firestore | All gen1 + Eventarc (120+ event types) |
| Min instances | Yes | Yes |
| VPC connector | Yes | Yes + Direct VPC egress |
| Pricing model | Per-invocation + compute | Cloud Run pricing (per-second) |

**Pricing (same as Cloud Run):**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Invocations | $0.40/million | 2 million/month |
| vCPU-second | $0.0000024 | 180,000/month |
| GiB-second | $0.0000025 | 360,000/month |

**When to use Cloud Functions vs Cloud Run:**
- **Cloud Functions:** Simple event handlers (file upload triggers, Pub/Sub consumers, webhook receivers)
- **Cloud Run:** Full applications, APIs, anything needing custom Dockerfiles, GPU, or multiple endpoints

**AWS equivalent:** AWS Lambda. Key difference: Lambda max timeout is 15 minutes vs. Cloud Run functions at 60 minutes. Lambda concurrency is 1 per instance vs. Cloud Run's 1,000. GCP wins on flexibility.

---

### 2.3 GKE (Google Kubernetes Engine)

**Autopilot vs Standard:**

| Feature | Autopilot | Standard |
|---------|-----------|----------|
| Node management | Google manages | You manage |
| Pricing unit | Per-pod (CPU/memory/ephemeral) | Per-node (VM pricing) |
| Cluster fee | $0.10/hr ($72/month) | Free (for zonal), $0.10/hr (regional) |
| GPU support | Yes (node-based billing) | Yes (full control) |
| Scaling | Automatic | Manual or Cluster Autoscaler |
| Security patches | Automatic | Manual or auto-upgrade |
| Best for | Teams without K8s expertise | Teams needing full control |

**GPU Node Pools (Standard mode):**

| GPU | On-Demand (per GPU/hr) | Spot Price | Memory | Best For |
|-----|----------------------|------------|--------|----------|
| NVIDIA T4 | ~$0.35 | ~$0.11 | 16 GB | Inference, light training |
| NVIDIA L4 | ~$0.70 | ~$0.22 | 24 GB | Inference, video processing |
| NVIDIA A100 40GB | ~$1.15 | ~$0.34 | 40 GB | Training, large model inference |
| NVIDIA A100 80GB | ~$1.57 | ~$0.47 | 80 GB | Large model training |
| NVIDIA H100 | ~$2.25 | ~$0.68 | 80 GB | Frontier model training |

**When to use GKE vs Cloud Run:**

| Criteria | Use Cloud Run | Use GKE |
|----------|--------------|---------|
| Team K8s expertise | Low | High |
| Scale-to-zero needed | Yes | No (nodes stay running) |
| GPU training | No | Yes |
| Multi-container pods | No | Yes |
| Service mesh (Istio) | No | Yes |
| Cost (small workloads) | Cheaper | More expensive |
| Cost (large/constant) | More expensive | Cheaper (sustained use) |
| Long-running jobs (>1hr) | Cloud Run Jobs (24hr max) | Yes |

---

### 2.4 Compute Engine (VMs)

**GPU Instances:**

| Machine Type | GPUs | GPU Memory | vCPUs | RAM | On-Demand/hr | Spot/hr |
|-------------|------|-----------|-------|-----|-------------|---------|
| a2-highgpu-1g | 1x A100 40GB | 40 GB | 12 | 85 GB | ~$3.67 | ~$1.10 |
| a2-highgpu-2g | 2x A100 40GB | 80 GB | 24 | 170 GB | ~$7.35 | ~$2.21 |
| a2-highgpu-4g | 4x A100 40GB | 160 GB | 48 | 340 GB | ~$14.69 | ~$4.41 |
| a2-highgpu-8g | 8x A100 40GB | 320 GB | 96 | 680 GB | ~$29.39 | ~$8.82 |
| a2-ultragpu-1g | 1x A100 80GB | 80 GB | 12 | 170 GB | ~$5.00 | ~$1.50 |
| g2-standard-4 | 1x L4 | 24 GB | 4 | 16 GB | ~$0.84 | ~$0.25 |
| n1-standard-4 + T4 | 1x T4 | 16 GB | 4 | 15 GB | ~$0.54 | ~$0.16 |

**Spot (Preemptible) VMs:**
- 60-91% discount off on-demand
- Can be preempted at any time (30-second warning)
- Price changes up to once per day
- Best for: fault-tolerant training, batch inference, CI/CD builds
- No sustained-use discounts (already discounted)

**Sustained-Use Discounts (automatic):**
- Applied automatically after 25% of the month
- Up to 30% discount on on-demand pricing
- GKE Standard mode and Compute Engine only (not Autopilot pods)

**Committed-Use Discounts:**
- 1-year: 37% discount
- 3-year: 55% discount
- Applied to vCPU and memory across a region

---

### 2.5 App Engine

**Standard vs Flexible:**

| Feature | Standard | Flexible |
|---------|----------|----------|
| Runtimes | Python, Java, Node.js, PHP, Ruby, Go | Any Docker container |
| Scaling | Scales to zero | Minimum 1 instance |
| Startup time | Seconds | Minutes |
| Max request timeout | 10 min (automatic scaling) | 60 min |
| Pricing | Per-instance-hour | Per-vCPU-hour + memory |
| Free tier | 28 instance-hours/day | None |
| Best for | Simple web apps, APIs | Custom runtimes, always-on |

**Pricing (Standard):**

| Instance Class | Price/hr |
|---------------|----------|
| F1 (256MB, 600MHz) | $0.05 |
| F2 (512MB, 1.2GHz) | $0.10 |
| F4 (1GB, 2.4GHz) | $0.20 |
| B1-B8 (manual scaling) | $0.05 - $0.40 |

**Veteran advice:** For new projects, use Cloud Run instead of App Engine. Google themselves now recommends this. App Engine Standard is still fine for existing apps, but Flexible is almost never the right choice anymore -- Cloud Run does everything Flex does, better and cheaper.

---

## 3. Storage & Databases

### 3.1 Cloud Storage (GCS)

**Storage Classes:**

| Class | Price/GB/month (US) | Min Duration | Retrieval Cost/GB | Best For |
|-------|-------------------|-------------|-------------------|----------|
| **Standard** | $0.020 | None | Free | Frequently accessed data |
| **Nearline** | $0.010 | 30 days | $0.01 | Monthly access |
| **Coldline** | $0.004 | 90 days | $0.02 | Quarterly access |
| **Archive** | $0.0012 | 365 days | $0.05 | Yearly/never access |

**Operations Pricing:**

| Operation | Standard | Nearline | Coldline | Archive |
|-----------|----------|----------|----------|---------|
| Class A (create, list) per 10K | $0.05 | $0.10 | $0.10 | $0.50 |
| Class B (get, metadata) per 10K | $0.004 | $0.01 | $0.05 | $0.50 |

**Egress (data out to internet):**

| Volume | Price/GB |
|--------|----------|
| 0-1 TB | $0.12 |
| 1-10 TB | $0.11 |
| 10+ TB | $0.08 |
| Intra-region (same region) | Free |
| Cross-region (within GCP) | $0.01-0.08 |

**Free tier:** 5 GB Standard storage (US regions only), 5,000 Class A ops, 50,000 Class B ops, 1 GB egress/month.

**Signed URLs:** Pre-signed URLs for temporary access. Generated via service account key or IAM signBlob. Valid for up to 7 days. Use V4 signing (not V2 -- deprecated).

**Lifecycle policies:** Automatically transition objects between storage classes or delete them based on age, creation date, number of versions, etc. Critical for cost optimization.

**CDN integration:** Cloud CDN can cache GCS objects at edge locations. Set `Cache-Control: public, max-age=3600` on objects.

**AWS comparison:** S3 Standard is $0.023/GB (US East) vs GCS Standard at $0.020/GB. GCS is ~13% cheaper for storage. Egress is similar. S3 has more storage classes (Intelligent-Tiering is very useful -- GCS has Autoclass as equivalent). Overall: GCS is slightly cheaper for storage, S3 is more feature-rich.

---

### 3.2 Firestore

Document database (NoSQL), part of the Firebase ecosystem. Two modes: Native (real-time, mobile SDKs) and Datastore mode (server-side, no real-time).

**Pricing:**

| Resource | Price | Free Tier (per day) |
|----------|-------|-------------------|
| Document reads | $0.06/100K | 50,000 |
| Document writes | $0.18/100K | 20,000 |
| Document deletes | $0.02/100K | 20,000 |
| Storage | $0.18/GB/month | 1 GB total |
| Network egress | $0.12/GB | 10 GiB/month |

**Key details:**
- Queries are charged per document returned (not per query)
- Index reads count toward read charges
- Aggregation queries (COUNT, SUM, AVG) are charged per index entry scanned
- Only 1 free database per project
- Real-time listeners count as reads

**When to use Firestore vs alternatives:**

| Use Case | Use Firestore | Use Instead |
|----------|-------------|-------------|
| Mobile/web apps with real-time sync | Yes | — |
| Complex queries with JOINs | No | Cloud SQL/AlloyDB |
| Full-text search | No | Vertex AI Search / Elasticsearch |
| Vector storage | No | AlloyDB (pgvector) / Vector Search |
| Time-series data | No | Bigtable |
| Analytics/reporting | No | BigQuery |

**Firestore vs MongoDB Atlas:** Similar pricing model. Firestore is cheaper for read-heavy workloads (50K free reads/day). MongoDB Atlas has better aggregation pipeline and indexing. Firestore wins for Firebase integration; MongoDB wins for complex queries.

---

### 3.3 Cloud SQL

Managed relational database. Supports PostgreSQL, MySQL, and SQL Server.

**Editions:**

| Edition | Price Premium | Features |
|---------|-------------|----------|
| **Enterprise** (default) | Base price | Standard HA, backups |
| **Enterprise Plus** | ~30% over Enterprise | Columnar engine, data cache, near-zero downtime maintenance |

**Pricing (PostgreSQL, Enterprise, us-central1):**

| Instance | vCPUs | RAM | Price/hr (on-demand) |
|----------|-------|-----|---------------------|
| db-f1-micro | Shared | 0.6 GB | $0.0150 |
| db-g1-small | Shared | 1.7 GB | $0.0500 |
| db-custom-1-3840 | 1 | 3.75 GB | $0.0500 |
| db-custom-2-7680 | 2 | 7.5 GB | $0.1000 |
| db-custom-4-15360 | 4 | 15 GB | $0.2000 |
| db-custom-8-30720 | 8 | 30 GB | $0.4000 |

**Storage:** $0.17/GB/month (SSD), $0.09/GB/month (HDD)
**Backups:** $0.08/GB/month
**HA (failover replica):** Doubles compute cost

**Cloud SQL Auth Proxy:** Free. Provides IAM-based authentication and encrypted connections without managing SSL certificates. Always use this in production.

**Connection pooling:** Cloud SQL does NOT include built-in connection pooling. Use PgBouncer sidecar or AlloyDB (which has built-in pooling). For Cloud Run -> Cloud SQL, use the built-in Cloud SQL connector library.

**AWS comparison:** RDS PostgreSQL is roughly equivalent pricing. RDS has more instance types. Cloud SQL Auth Proxy is better than RDS IAM auth (simpler setup).

---

### 3.4 AlloyDB

PostgreSQL-compatible, Google-built database with columnar engine and AI-optimized vector search.

**Pricing:**

| Resource | Price | Notes |
|----------|-------|-------|
| vCPU/hr | $0.1386 (1-year CUD) | ~39% more than Cloud SQL Enterprise Plus |
| Storage | $0.339/GB/month | ~2x Cloud SQL SSD |
| Backups | $0.113/GB/month | ~40% more than Cloud SQL |
| Network (cross-region) | $0.12/GB (0-1TB) | Better rates at volume |

**Why AlloyDB over Cloud SQL:**

| Feature | Cloud SQL PostgreSQL | AlloyDB |
|---------|---------------------|---------|
| pgvector performance | Standard PostgreSQL | 10x faster (ScaNN algorithm) |
| Columnar engine | No | Yes (100x faster analytics) |
| Connection pooling | External (PgBouncer) | Built-in |
| AI embeddings | Standard pgvector | Optimized vector indexing |
| Price | Lower | ~39% more |
| Auto-scaling storage | No | Yes |

**When to use AlloyDB:**
- AI/RAG workloads with pgvector (the 10x vector search speedup justifies the cost)
- Mixed OLTP + analytics (columnar engine)
- High-connection workloads (built-in pooling)
- >100K vector searches per day

**When to stick with Cloud SQL:**
- Simple CRUD apps
- Budget-constrained projects
- <100K vectors
- Team already knows Cloud SQL

---

### 3.5 Bigtable

Wide-column NoSQL database for massive scale (petabytes, millions of QPS).

**Pricing:**

| Resource | Price |
|----------|-------|
| Node/hr (SSD) | $0.65 |
| Storage (SSD) | $0.17/GB/month |
| Storage (HDD) | $0.026/GB/month |
| Network egress | Standard GCP rates |

**Minimum:** 1 node ($0.65/hr = ~$468/month). No free tier. No scale-to-zero.

**When to use:** IoT data, time-series, ad-tech, financial tick data, >1TB datasets with sub-10ms latency requirements.

**When NOT to use:** Small datasets, ACID transactions needed, complex queries, SQL needed. Use Firestore or Cloud SQL instead.

**AWS equivalent:** Amazon DynamoDB. DynamoDB has on-demand pricing and scales to zero; Bigtable doesn't. For most workloads, DynamoDB is more cost-effective. Bigtable wins on raw throughput at extreme scale.

---

### 3.6 BigQuery

Serverless data warehouse. One of GCP's crown jewels.

**Pricing:**

| Resource | On-Demand | Capacity (Editions) |
|----------|-----------|-------------------|
| Queries | $6.25/TB scanned | $0.04/slot-hour (Standard) |
| Active storage | $0.020/GB/month | Same |
| Long-term storage (>90 days) | $0.010/GB/month | Same |
| Streaming inserts | $0.012/200MB | Same |
| Free tier | 1 TB queries + 10 GB storage/month | — |

**BigQuery ML (BQML):**
- CREATE MODEL: $250/TB of data processed
- ML.PREDICT: Standard query pricing ($6.25/TB)
- Supports: Linear regression, logistic regression, K-means, XGBoost, DNN, AutoML, imported TF models
- Can call Vertex AI models directly from SQL

**BigQuery Vector Search:**
- VECTOR_SEARCH function: Standard query pricing (bytes scanned)
- Index creation: Free (up to per-org limit)
- Supports: cosine, dot product, euclidean distance
- Can store and search embeddings directly in BQ tables
- Best for analytical workloads where vectors live alongside structured data

**BigQuery Editions (capacity pricing):**

| Edition | Slot Price/hr | Autoscaling | Commitment Options |
|---------|-------------|-------------|-------------------|
| Standard | $0.04 | Baseline only | Pay-as-you-go only |
| Enterprise | $0.06 | Yes (1-year) | 1-year: $0.048, 3-year: $0.036 |
| Enterprise Plus | $0.10 | Yes | 1-year: $0.08, 3-year: $0.06 |

**Veteran tip:** Most teams should start with on-demand pricing. Switch to slots when your monthly query spend exceeds ~$5,000. The first 1 TB/month free is generous -- many analytics teams run entirely on the free tier.

**AWS comparison:** Athena is $5.00/TB scanned (cheaper than BQ's $6.25/TB). But BQ has much richer features (ML, vector search, BI Engine, real-time streaming). Redshift Serverless is $0.375/RPU-hr. Overall: BQ is more feature-rich; Athena is cheaper for pure ad-hoc SQL.

---

### 3.7 Memorystore

Managed Redis/Valkey in-memory cache.

**Pricing (Redis, Basic tier):**

| Instance Size | Price/hr | Monthly |
|--------------|----------|---------|
| 1 GB (M1) | ~$0.049 | ~$35 |
| 5 GB (M2) | ~$0.246 | ~$177 |
| 10 GB (M3) | ~$0.493 | ~$355 |

**Standard tier (HA):** ~2x Basic pricing (includes failover replica).

**Memorystore for Redis Cluster:** Higher throughput, horizontal scaling, starts at ~$0.18/GB-hr.

**Committed-use discounts:** 20% (1-year), 40% (3-year).

**AWS comparison:** ElastiCache is slightly cheaper for equivalent instances. ElastiCache Serverless is a better option for variable workloads (GCP doesn't have a serverless Redis equivalent).

---

### 3.8 Spanner

Globally distributed, strongly consistent, relational database. GCP's most expensive DB option.

**Pricing:**

| Resource | Price |
|----------|-------|
| Compute (per node/hr) | $0.90 |
| Storage | $0.30/GB/month |
| Backup storage | $0.30/GB/month |
| Network egress | Standard rates |

**Minimum:** 100 processing units (~$0.09/hr = ~$65/month for smallest config).

**When to use:** Global consistency requirements, multi-region active-active, financial systems, gaming leaderboards. If you're asking "should I use Spanner?" the answer is probably no -- it's for Google-scale problems.

---

## 4. Networking & CDN

### 4.1 Cloud CDN

| Resource | Price |
|----------|-------|
| Cache egress (North America) | $0.08/GB |
| Cache egress (Europe) | $0.08/GB |
| Cache egress (Asia) | $0.10/GB |
| Cache fill | $0.04/GB (intra-continent) |
| HTTP/HTTPS requests | $0.0075/10K requests |
| Cache invalidation | $0.005/invalidation |

**Cache modes:** USE_ORIGIN_HEADERS, CACHE_ALL_STATIC, FORCE_CACHE_ALL

**Custom domains:** Managed SSL certificates are free. Custom certificates also supported.

**AWS comparison:** CloudFront is $0.085/GB (US) vs Cloud CDN's $0.08/GB -- roughly equivalent. CloudFront has more edge locations (600+ vs ~200). CloudFront has Lambda@Edge; Cloud CDN does not have edge compute.

---

### 4.2 Cloud Load Balancing

| Type | Price | Scope |
|------|-------|-------|
| Forwarding rule | $0.025/hr | Per rule |
| Data processed (inbound) | $0.008/GB | First 1GB free/month |
| Data processed (outbound) | Standard egress | — |

**Types:**
- **Global external HTTP(S)** -- multi-region, Anycast IP, Cloud CDN integration
- **Regional external HTTP(S)** -- single-region, lower cost
- **Internal HTTP(S)** -- VPC-internal only
- **TCP/UDP** (Network Load Balancer) -- pass-through, no proxy
- **SSL Proxy** -- global SSL termination

**AWS comparison:** ALB is $0.0225/hr + $0.008/LCU-hr. GCP's Load Balancer at $0.025/hr + data is comparable but simpler pricing.

---

### 4.3 Cloud DNS

| Resource | Price |
|----------|-------|
| Managed zone | $0.20/zone/month |
| Queries | $0.40/million (first 1B) |

**Features:** DNSSEC, private zones, forwarding zones, peering zones, latency-based routing (via Traffic Director).

**Free tier:** None for Cloud DNS specifically.

---

### 4.4 VPC

| Resource | Price |
|----------|-------|
| VPC creation | Free |
| Subnets | Free |
| Firewall rules | Free |
| Intra-zone traffic | Free |
| Inter-zone traffic (same region) | $0.01/GB |
| Inter-region traffic | $0.01-0.08/GB |
| Private Google Access | Free |
| Cloud NAT | $0.045/hr per gateway + $0.045/GB processed |
| VPN | $0.075/hr per tunnel |

**Private Google Access:** Allows VMs without external IPs to reach Google APIs. Free and essential for security. Always enable this.

---

## 5. Serverless & Event-Driven

### 5.1 Pub/Sub

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Message throughput | $40/TiB | 10 GiB/month |
| Retained acknowledged messages | $0.27/GiB/month | — |
| Snapshots/message backlog | $0.27/GiB/month | — |
| Topic retention | $0.27/GiB/month | — |

**Minimum billing unit:** 1 KB per publish/pull request (even if message is smaller).

**Key features:**
- At-least-once delivery (default)
- Exactly-once delivery (available, use with care -- adds latency)
- Dead-letter topics (configurable max delivery attempts)
- Push subscriptions (HTTP endpoints) and Pull subscriptions
- Message ordering (per-key)
- Schema validation (Avro, Protocol Buffers)
- BigQuery subscriptions (direct write to BQ)

**AWS comparison:** SNS + SQS. Pub/Sub is simpler (single service), supports both push and pull, and has a generous free tier (10 GiB vs SQS's 1M requests). Pricing is comparable at scale.

---

### 5.2 Cloud Tasks

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Task operations | $0.40/million | 1 million/month |

**Key features:**
- HTTP targets (any URL) or App Engine targets
- Rate limiting (max dispatches/second)
- Retry with exponential backoff
- Scheduled delivery (up to 30 days in future)
- Task deduplication
- Max task size: 1 MB

**When to use Cloud Tasks vs Pub/Sub:**
- **Cloud Tasks:** Rate-limited delivery to a specific target, task scheduling, retry control
- **Pub/Sub:** Fan-out (multiple consumers), streaming data, event-driven architecture

---

### 5.3 Cloud Scheduler

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Jobs | $0.10/job/month | 3 jobs free |

**Features:** Cron syntax, HTTP/Pub/Sub/App Engine targets, configurable retry, timezone support, pause/resume.

**AWS comparison:** EventBridge Scheduler is free for first 14M invocations/month. Cloud Scheduler is simpler but costs more at scale.

---

### 5.4 Eventarc

**Pricing:** No direct Eventarc charge. You pay for:
- Pub/Sub transport (standard Pub/Sub rates)
- Cloud Audit Logs (Cloud Logging charges)
- Target service (Cloud Run, Workflows, etc.)

**Supported event sources:** 120+ GCP services, including Cloud Storage, Firestore, BigQuery, custom via Pub/Sub.

**AWS comparison:** Amazon EventBridge. EventBridge is $1.00/million events; Eventarc uses Pub/Sub pricing (generally cheaper for high-volume).

---

### 5.5 Workflows

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Internal steps | $0.01/1,000 steps | 5,000/month |
| External steps (HTTP calls) | $0.025/1,000 steps | 2,000/month |

**Key features:**
- YAML/JSON workflow definition
- Built-in connectors to 200+ GCP APIs
- Conditional logic, loops, parallel branches
- Error handling with retry and catch
- Subworkflows (reusable)
- Max execution: 1 year
- Max 20K concurrent executions per workflow

**AWS comparison:** AWS Step Functions Standard is $0.025/1,000 state transitions. Similar pricing. Step Functions has better visual editor; Workflows has better GCP API integration.

---

## 6. Security & IAM

### 6.1 IAM (Identity and Access Management)

**Price:** Free. No charge for IAM itself.

**Key concepts:**
- **Principals:** Users, service accounts, groups, domains
- **Roles:** Primitive (Owner/Editor/Viewer -- avoid these), Predefined (per-service), Custom
- **Service accounts:** Machine identities. Can have up to 10 keys. Prefer Workload Identity over keys.
- **Workload Identity Federation:** Use external IdP (AWS, Azure AD, OIDC) without service account keys
- **Organization policies:** Guardrails at org/folder/project level
- **IAM Conditions:** Time-based, resource-based access control

**Best practices:**
1. Never use primitive roles in production
2. Use Workload Identity Federation instead of service account keys
3. Grant minimum necessary permissions (principle of least privilege)
4. Use groups for access management, not individual users
5. Rotate service account keys every 90 days (or better: don't use keys at all)

---

### 6.2 Secret Manager

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Active secret versions | $0.06/version/month | 6 active versions |
| Access operations | $0.03/10,000 | 10,000/month |
| Destroy operations | Free | — |

**Features:** Automatic rotation, versioning, IAM integration, regional/multi-regional replication, audit logging.

**AWS comparison:** AWS Secrets Manager is $0.40/secret/month + $0.05/10K API calls. GCP is MUCH cheaper. AWS charges per secret; GCP charges per version. For 10 secrets with 3 versions each: AWS = $4.00/month, GCP = $1.80/month.

---

### 6.3 Cloud KMS (Key Management Service)

**Pricing:**

| Resource | Price |
|----------|-------|
| Software keys (symmetric) | $0.06/key-version/month |
| HSM keys | $1.00-3.00/key-version/month |
| External keys (EKM) | $3.00/key-version/month |
| Crypto operations | $0.03/10,000 operations |

**Features:** Symmetric/asymmetric encryption, digital signing, CMEK (Customer-Managed Encryption Keys) for GCP services, key rotation, import/export.

---

### 6.4 Cloud Armor

**Pricing:**

| Tier | Price |
|------|-------|
| Standard (per policy) | $5/month + $0.75/million requests |
| Managed Protection | $200/month (up to 2 resources) |
| Managed Protection Plus | $3,000/month (first 100 resources) |

**Features:**
- WAF (Web Application Firewall) with preconfigured rules (OWASP Top 10)
- DDoS protection (always on for HTTP(S) Load Balancer)
- Rate limiting (by IP, header, etc.)
- Bot management
- Adaptive protection (ML-based anomaly detection)
- Geographic access control
- Custom WAF rules (CEL expressions)

**AWS comparison:** AWS WAF is $5.00/web ACL + $1.00/rule + $0.60/million requests. Pricing is similar. AWS Shield Advanced ($3,000/month) is comparable to Managed Protection Plus.

---

## 7. CI/CD & DevOps

### 7.1 Cloud Build

**Pricing:**

| Machine Type | Price/min | Free Tier |
|-------------|----------|-----------|
| e2-standard-2 (default) | $0.006 | 2,500 min/day (= ~42 hrs/day) |
| e2-highcpu-8 | $0.016 | — |
| e2-highcpu-32 | $0.064 | — |

**Key features:**
- Build triggers (GitHub, GitLab, Bitbucket, Cloud Source Repos)
- Dockerfile and buildpacks support
- Multi-step builds (cloudbuild.yaml)
- Private pools (for VPC access)
- Build caching
- Vulnerability scanning (on-build)

**Free tier is extremely generous:** 120 build-minutes per day = 2,500 minutes for the cheapest machine. Most small-medium projects build for free.

**AWS comparison:** AWS CodeBuild is $0.005/min (general1.small) with no free tier beyond AWS Free Tier (100 min/month). GCP's 2,500 free min/day is 25x more generous.

---

### 7.2 Artifact Registry

**Pricing:**

| Resource | Price |
|----------|-------|
| Storage | $0.10/GB/month |
| Network (same region) | Free |
| Network (cross-region) | Standard egress rates |

Supports: Docker images, npm, Maven, Python (PyPI), Go, APT, Yum, Helm.

**Free tier:** 500 MB of storage (per billing account).

**AWS comparison:** ECR is $0.10/GB/month (identical pricing). ECR has lifecycle policies built-in; Artifact Registry relies on cleanup policies.

---

### 7.3 Cloud Deploy

**Pricing:** $0.20 per active delivery pipeline per day. Each pipeline can have multiple targets.

**Features:**
- Managed CD pipeline (not CI -- use Cloud Build for CI)
- Supports Cloud Run, GKE, Anthos
- Canary, blue/green, rolling deployments
- Approval gates
- Rollback support
- Integration with Cloud Build

---

## 8. Monitoring & Observability

### 8.1 Cloud Monitoring

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Metrics (per MiB ingested) | $0.258 (first 150 MiB free) | 150 MiB/billing account |
| Custom metrics | $0.258/MiB | Included in 150 MiB |
| GCP metrics | Free | All built-in metrics |
| Uptime checks | Free | Up to 100 checks |
| Alerting policies | Free | — |
| Dashboards | Free | — |

**Key features:**
- Pre-built dashboards for all GCP services
- Custom dashboards (MQL or PromQL)
- Alerting (email, SMS, PagerDuty, Slack, webhooks)
- SLO monitoring
- Managed Prometheus (PromQL compatible)

---

### 8.2 Cloud Logging

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Log ingestion | $0.50/GiB | 50 GiB/project/month |
| Retention (default 30 days) | Included | — |
| Extended retention | $0.01/GiB/month | — |
| Log Analytics (SQL queries) | BigQuery pricing | — |

**Cost optimization tips:**
1. Exclude noisy logs (load balancer health checks, debug logs)
2. Set appropriate log levels in production (INFO, not DEBUG)
3. Use log sinks to route logs to cheaper storage (GCS, BigQuery)
4. Enable _Default log bucket exclusion filters

**AWS comparison:** CloudWatch Logs is $0.50/GB ingested + $0.03/GB stored/month. GCP includes 30 days of retention in the ingestion price; AWS charges separately. GCP is cheaper for short-term logs.

---

### 8.3 Cloud Trace

**Pricing:**

| Resource | Price | Free Tier |
|----------|-------|-----------|
| Spans ingested | $0.20/million | 2.5 million spans/month |

Auto-generated traces from Cloud Run and App Engine Standard are 100% free.

**Features:** Distributed tracing, latency analysis, integration with OpenTelemetry, automatic instrumentation for GCP services.

---

### 8.4 Error Reporting

**Price:** Free. No direct charges.

Automatically groups errors by stack trace, shows error trends, and integrates with Cloud Logging. Supported languages: Go, Java, .NET, Node.js, PHP, Python, Ruby.

---

## 9. Free Tier (Complete List)

### Always-Free Products (Never Expires)

| Service | Free Allowance | Notes |
|---------|---------------|-------|
| **Compute Engine** | 1 e2-micro VM/month (US regions) | Oregon, Iowa, South Carolina |
| | 30 GB standard persistent disk | — |
| | 1 GB egress/month | — |
| **Cloud Run** | 2M requests/month | — |
| | 180,000 vCPU-seconds | — |
| | 360,000 GiB-seconds | — |
| **Cloud Functions** | 2M invocations/month | — |
| | 400,000 GiB-seconds | — |
| | 200,000 GHz-seconds | — |
| **App Engine** | 28 instance-hours/day | Standard environment only |
| **Cloud Storage** | 5 GB Standard (US regions) | 5K Class A, 50K Class B ops |
| | 1 GB egress/month | — |
| **Firestore** | 1 GB storage | — |
| | 50K reads/day, 20K writes/day, 20K deletes/day | 1 free DB per project |
| **BigQuery** | 1 TB queries/month | — |
| | 10 GB storage/month | — |
| **Pub/Sub** | 10 GiB/month | — |
| **Cloud Build** | 2,500 build-min/day (e2-standard-2) | ~42 hours/day |
| **Artifact Registry** | 500 MB storage | — |
| **Secret Manager** | 6 active versions | 10K access operations |
| **Cloud Logging** | 50 GiB ingestion/month | Per project |
| **Cloud Monitoring** | 150 MiB metrics/month | All GCP metrics free |
| **Cloud Trace** | 2.5M spans/month | Cloud Run traces free |
| **Error Reporting** | Unlimited | Fully free |
| **Cloud Scheduler** | 3 jobs | — |
| **Cloud Tasks** | 1M operations/month | — |
| **Workflows** | 5,000 internal steps + 2,000 external steps | Per month |
| **Cloud DNS** | Not free | — |
| **Vision AI** | 1,000 units/month | Per feature |
| **Natural Language AI** | 5,000 units/month | — |
| **Translation AI** | 500K chars/month | Never expires |
| **Speech-to-Text** | 60 min/month | — |
| **Text-to-Speech (Standard)** | 4M chars/month | — |
| **Text-to-Speech (WaveNet/Neural2)** | 1M chars/month | — |
| **Document AI (OCR)** | 1,000 pages/month | — |
| **Video Intelligence** | 1,000 min/month | First 1K for label detection |
| **AutoML Vision** | Not free | — |
| **Vertex AI** | $300 credit (90-day trial) | New accounts only |
| **Vertex AI Search** | 10,000 queries/month | — |
| **Dialogflow CX** | No free tier | — |
| **Dialogflow ES** | 1,000 text queries/day | — |
| **Firebase Auth** | 50K MAU (phone auth: 10K/month) | — |
| **Firebase Hosting** | 10 GB storage, 360 MB/day transfer | — |
| **Firebase Realtime DB** | 1 GB storage, 10 GB download/month | — |

### Free Trial (New Accounts)
- **$300 credit** valid for 90 days
- Available on all GCP services
- No auto-charge after trial ends (unlike AWS)
- Cannot use GPU VMs during trial

---

## 10. Pricing Comparisons vs AWS

### Service-by-Service Comparison

| Service | GCP Price | AWS Equivalent | AWS Price | Winner |
|---------|----------|---------------|----------|--------|
| **Serverless Containers** | Cloud Run: $0.000024/vCPU-sec | Fargate: $0.000011/vCPU-sec | AWS cheaper | AWS (compute), GCP (DX) |
| **Serverless Functions** | Cloud Run functions: 2M free | Lambda: 1M free | Both cheap | GCP (more free) |
| **Object Storage** | GCS: $0.020/GB | S3: $0.023/GB | — | GCP (13% cheaper) |
| **PostgreSQL (managed)** | Cloud SQL: ~$0.05/hr (1vCPU) | RDS: ~$0.045/hr | Similar | Tie |
| **Vector DB (managed)** | AlloyDB pgvector: ~$0.14/hr | RDS pgvector: ~$0.05/hr | — | AWS (cheaper), GCP (10x faster) |
| **Vector Search** | Vertex AI: $3/GiB processed | OpenSearch Serverless: $0.24/OCU-hr | Complex | Depends on scale |
| **Redis** | Memorystore: ~$0.049/hr (1GB) | ElastiCache: ~$0.038/hr | — | AWS (cheaper) |
| **Data Warehouse** | BigQuery: $6.25/TB | Athena: $5.00/TB | — | AWS (pure query), GCP (features) |
| **LLM API (best model)** | Gemini 2.5 Pro: $1.25/1M in | Claude Sonnet via Bedrock: $3/1M in | — | GCP (58% cheaper) |
| **LLM API (cheap model)** | Gemini 2.0 Flash: $0.10/1M in | Claude Haiku via Bedrock: $0.25/1M in | — | GCP (60% cheaper) |
| **Embeddings** | Gemini Embedding 2: $0.20/1M tokens | Titan v2: $0.02/1M tokens | — | AWS (cheaper), GCP (multimodal) |
| **STT** | Chirp: $0.016/min | Transcribe: $0.024/min | — | GCP (33% cheaper) |
| **TTS (neural)** | WaveNet: $16/1M chars | Polly Neural: $16/1M chars | — | Tie |
| **OCR** | Vision API: $1.50/1K pages | Textract: $1.50/1K pages | — | Tie |
| **CI/CD Build** | Cloud Build: 2,500 min/day free | CodeBuild: 100 min/month free | — | GCP (25x more free) |
| **Secrets** | Secret Manager: $0.06/version | Secrets Manager: $0.40/secret | — | GCP (6x cheaper) |
| **CDN** | Cloud CDN: $0.08/GB | CloudFront: $0.085/GB | — | GCP (slightly cheaper) |
| **Logging** | $0.50/GiB (50 GiB free) | CloudWatch: $0.50/GB (5 GB free) | — | GCP (10x more free) |
| **Container Registry** | Artifact Registry: $0.10/GB | ECR: $0.10/GB | — | Tie |
| **Egress (internet)** | $0.12/GB (first 1TB) | $0.09/GB (first 10TB) | — | AWS (25% cheaper) |

### Hidden Costs to Watch

| Cost | GCP | AWS | Notes |
|------|-----|-----|-------|
| **Egress to internet** | $0.12/GB | $0.09/GB | AWS is cheaper. Both have 1GB/100GB free |
| **Cross-region transfer** | $0.01-0.08/GB | $0.01-0.02/GB | AWS generally cheaper |
| **Load balancer** | $0.025/hr + data | $0.0225/hr + LCU | Similar |
| **NAT Gateway** | $0.045/hr + $0.045/GB | $0.045/hr + $0.045/GB | Identical |
| **IP addresses** | $0.004/hr (unused) | $0.005/hr (all) | GCP: only unused IPs charged |
| **Support** | $0-$150K/year | $0-$15K/month | GCP cheaper at enterprise tier |

### Bottom Line for AI Workloads

**GCP is cheaper for:**
1. LLM inference (Gemini is cheapest frontier model)
2. Speech-to-Text (33% cheaper than AWS)
3. Secrets management (6x cheaper)
4. CI/CD builds (25x more free minutes)
5. Logging (10x more free ingestion)
6. Small serverless workloads (more generous free tier)

**AWS is cheaper for:**
1. Data egress (25% cheaper)
2. Managed Redis (ElastiCache cheaper)
3. Container compute (Fargate per-vCPU cheaper)
4. Embeddings (Titan v2 is 10x cheaper than Gemini Embedding 2 for text-only)

**Choose GCP when:** You're Gemini-first, need BigQuery, want simpler pricing, or value the Firebase ecosystem.
**Choose AWS when:** You need more regions, wider service selection, or your team already knows AWS.

---

## 11. Architecture Patterns for AI Projects

### 11.1 RAG on GCP

```
┌─────────────────────────────────────────────────────┐
│                    RAG Pipeline                       │
│                                                       │
│  ┌──────────┐    ┌───────────────┐    ┌───────────┐  │
│  │  Cloud    │───>│  Gemini       │───>│  AlloyDB   │  │
│  │  Storage  │    │  Embedding 2  │    │  pgvector  │  │
│  │  (docs)   │    │               │    │  (vectors) │  │
│  └──────────┘    └───────────────┘    └───────────┘  │
│                                            │          │
│  ┌──────────┐    ┌───────────────┐    ┌────v──────┐  │
│  │  User     │───>│  Cloud Run    │───>│  Gemini   │  │
│  │  Query    │    │  (FastAPI)    │    │  2.5 Pro  │  │
│  └──────────┘    └───────────────┘    └───────────┘  │
└─────────────────────────────────────────────────────┘
```

**Component choices:**

| Layer | Budget Option | Production Option |
|-------|-------------|-------------------|
| Document storage | Cloud Storage Standard | Cloud Storage Standard |
| Embeddings | text-embedding-005 ($0.025/1K chars) | Gemini Embedding 2 ($0.20/1M tokens) |
| Vector store | Firestore (simple) | AlloyDB pgvector (fast) or Vertex AI Vector Search (managed) |
| API server | Cloud Run (scale-to-zero) | Cloud Run (min-instances=2) |
| LLM | Gemini 2.5 Flash ($0.30/1M in) | Gemini 2.5 Pro ($1.25/1M in) |
| Cache | None | Memorystore Redis |

**Monthly cost estimate (1000 RAG queries/day):**
- Budget: ~$15-30/month
- Production: ~$100-300/month

---

### 11.2 Real-Time AI Agent

```
┌─────────────────────────────────────────────────────────┐
│                  Real-Time Agent                          │
│                                                           │
│  ┌────────┐    ┌──────────┐    ┌───────────────────────┐ │
│  │ Client  │───>│ Cloud    │───>│ Gemini 2.5 Pro        │ │
│  │ (WebSocket)  │ Run      │    │ (function calling)    │ │
│  └────────┘    │ (FastAPI) │    └───────────────────────┘ │
│                └──────────┘                               │
│                     │  │  │                                │
│              ┌──────┘  │  └──────┐                        │
│              v         v         v                        │
│  ┌──────────────┐ ┌────────┐ ┌──────────┐               │
│  │  Firestore   │ │Pub/Sub │ │ External │               │
│  │  (state)     │ │(events)│ │ APIs     │               │
│  └──────────────┘ └────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────┘
```

**Key decisions:**
- Use Cloud Run with WebSocket support (max 3600s connection)
- Use Pub/Sub for async tool execution (agent calls tool -> Pub/Sub -> worker -> result)
- Store conversation state in Firestore (real-time sync to client)
- Use Gemini's native function calling (structured tool outputs)

---

### 11.3 Batch ML Pipeline

```
┌─────────────────────────────────────────────────────────┐
│               Batch ML Pipeline                           │
│                                                           │
│  ┌──────────┐    ┌───────────────┐    ┌───────────────┐  │
│  │  Cloud    │───>│  Vertex AI    │───>│  BigQuery     │  │
│  │  Storage  │    │  Pipelines    │    │  (features)   │  │
│  │  (raw data)│   │  (Kubeflow)   │    └───────────────┘  │
│  └──────────┘    │               │                        │
│                  │  Steps:       │    ┌───────────────┐  │
│                  │  1. Preprocess │───>│  Vertex AI    │  │
│                  │  2. Train     │    │  Model        │  │
│                  │  3. Evaluate  │    │  Registry     │  │
│                  │  4. Deploy    │    └───────────────┘  │
│                  └───────────────┘           │            │
│                                              v            │
│                                    ┌───────────────┐     │
│                                    │  Vertex AI    │     │
│                                    │  Endpoint     │     │
│                                    │  (serving)    │     │
│                                    └───────────────┘     │
└─────────────────────────────────────────────────────────┘
```

**Schedule:** Cloud Scheduler -> triggers Vertex AI Pipeline run
**Storage:** Raw data in GCS -> processed features in BigQuery Feature Store
**Training:** Custom training job (PyTorch/TF/JAX) on GPU instances
**Evaluation:** Automated model evaluation with threshold gates
**Deployment:** Canary deployment to Vertex AI Endpoint

---

### 11.4 Multimodal AI Application

```
┌─────────────────────────────────────────────────────────┐
│             Multimodal AI App                             │
│                                                           │
│  ┌────────────┐   ┌──────────┐   ┌────────────────────┐ │
│  │  Upload     │──>│  Cloud   │──>│  Gemini Embed 2    │ │
│  │  (img/vid/  │   │  Storage │   │  (multimodal       │ │
│  │   audio/pdf)│   │          │   │   embeddings)      │ │
│  └────────────┘   └──────────┘   └────────────────────┘ │
│                                           │               │
│  ┌────────────┐   ┌──────────┐   ┌───────v────────────┐ │
│  │  Search     │──>│  Cloud   │──>│  Vertex AI         │ │
│  │  Query      │   │  Run     │   │  Vector Search     │ │
│  │  (any mode) │   │  (API)   │   │  (similarity)      │ │
│  └────────────┘   └──────────┘   └────────────────────┘ │
│                        │                                  │
│                        v                                  │
│              ┌────────────────────┐                       │
│              │  Gemini 2.5 Pro    │                       │
│              │  (multimodal RAG   │                       │
│              │   generation)      │                       │
│              └────────────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

**Key insight:** Gemini Embedding 2 puts text, images, video, and audio into the same vector space. This means a text query can find relevant images, and an image query can find relevant documents -- all through a single index.

---

## 12. GCP CLI Commands Reference

### 12.1 gcloud -- Core CLI

**Authentication & Configuration:**

```bash
# Login
gcloud auth login
gcloud auth application-default login    # For local dev (ADC)

# Set project
gcloud config set project PROJECT_ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# List config
gcloud config list
gcloud config configurations list        # Multiple profiles

# Create new config profile
gcloud config configurations create my-project
gcloud config configurations activate my-project
```

**Compute Engine:**

```bash
# List instances
gcloud compute instances list

# Create VM
gcloud compute instances create my-vm \
  --machine-type=e2-medium \
  --zone=us-central1-a \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=50GB

# Create GPU VM
gcloud compute instances create gpu-vm \
  --machine-type=g2-standard-4 \
  --zone=us-central1-a \
  --accelerator=type=nvidia-l4,count=1 \
  --maintenance-policy=TERMINATE \
  --image-family=common-gpu \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=200GB

# SSH
gcloud compute ssh my-vm --zone=us-central1-a

# Create spot VM
gcloud compute instances create spot-vm \
  --provisioning-model=SPOT \
  --machine-type=n1-standard-4

# Stop/start/delete
gcloud compute instances stop my-vm --zone=us-central1-a
gcloud compute instances start my-vm --zone=us-central1-a
gcloud compute instances delete my-vm --zone=us-central1-a
```

**Cloud Run:**

```bash
# Deploy from source (builds with Cloud Build)
gcloud run deploy my-service \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated

# Deploy from image
gcloud run deploy my-service \
  --image=us-central1-docker.pkg.dev/PROJECT/repo/image:tag \
  --region=us-central1 \
  --memory=1Gi \
  --cpu=2 \
  --min-instances=1 \
  --max-instances=10 \
  --concurrency=250 \
  --timeout=300 \
  --set-env-vars="KEY=value" \
  --set-secrets="SECRET_KEY=my-secret:latest" \
  --allow-unauthenticated

# Deploy with GPU
gcloud run deploy my-gpu-service \
  --image=IMAGE \
  --gpu=1 \
  --gpu-type=nvidia-l4 \
  --cpu=4 \
  --memory=16Gi \
  --region=us-central1

# Update service
gcloud run services update my-service \
  --region=us-central1 \
  --memory=2Gi

# List services
gcloud run services list --region=us-central1

# Get URL
gcloud run services describe my-service --region=us-central1 --format='value(status.url)'

# View logs
gcloud run services logs read my-service --region=us-central1

# Delete
gcloud run services delete my-service --region=us-central1
```

**Cloud Functions:**

```bash
# Deploy gen2 (Cloud Run function)
gcloud functions deploy my-function \
  --gen2 \
  --runtime=python312 \
  --trigger-http \
  --region=us-central1 \
  --entry-point=handler \
  --memory=256MB \
  --timeout=60s \
  --allow-unauthenticated

# Deploy with Pub/Sub trigger
gcloud functions deploy my-function \
  --gen2 \
  --runtime=python312 \
  --trigger-topic=my-topic \
  --entry-point=handler

# Deploy with Cloud Storage trigger
gcloud functions deploy my-function \
  --gen2 \
  --runtime=python312 \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-bucket"
```

**IAM & Service Accounts:**

```bash
# Create service account
gcloud iam service-accounts create my-sa \
  --display-name="My Service Account"

# Grant role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:my-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# Create key (avoid if possible -- use Workload Identity)
gcloud iam service-accounts keys create key.json \
  --iam-account=my-sa@PROJECT_ID.iam.gserviceaccount.com

# List roles
gcloud iam roles list --project=PROJECT_ID
```

**Secret Manager:**

```bash
# Create secret
echo "my-secret-value" | gcloud secrets create my-secret --data-file=-

# Access secret
gcloud secrets versions access latest --secret=my-secret

# Add new version
echo "new-value" | gcloud secrets versions add my-secret --data-file=-

# List secrets
gcloud secrets list
```

**Pub/Sub:**

```bash
# Create topic
gcloud pubsub topics create my-topic

# Create subscription
gcloud pubsub subscriptions create my-sub --topic=my-topic

# Publish message
gcloud pubsub topics publish my-topic --message="hello"

# Pull messages
gcloud pubsub subscriptions pull my-sub --auto-ack --limit=10
```

**Vertex AI:**

```bash
# Enable APIs
gcloud services enable aiplatform.googleapis.com

# Submit custom training job
gcloud ai custom-jobs create \
  --region=us-central1 \
  --display-name="my-training" \
  --python-package-uris=gs://bucket/package.tar.gz \
  --module-name=trainer.task \
  --machine-type=n1-standard-4 \
  --accelerator-type=NVIDIA_TESLA_T4 \
  --accelerator-count=1

# Deploy model to endpoint
gcloud ai endpoints deploy-model ENDPOINT_ID \
  --region=us-central1 \
  --model=MODEL_ID \
  --display-name="v1" \
  --machine-type=n1-standard-4 \
  --min-replica-count=1 \
  --max-replica-count=3
```

### 12.2 gsutil -- Cloud Storage CLI

```bash
# Upload file
gsutil cp local-file.txt gs://my-bucket/

# Upload directory
gsutil -m cp -r local-dir/ gs://my-bucket/prefix/

# Download
gsutil cp gs://my-bucket/file.txt .

# List
gsutil ls gs://my-bucket/
gsutil ls -l gs://my-bucket/   # With size/date

# Sync (like rsync)
gsutil -m rsync -r local-dir/ gs://my-bucket/prefix/

# Make public
gsutil iam ch allUsers:objectViewer gs://my-bucket

# Generate signed URL (1 hour)
gsutil signurl -d 1h key.json gs://my-bucket/file.txt

# Set lifecycle (auto-delete after 30 days)
gsutil lifecycle set lifecycle.json gs://my-bucket/

# Set CORS
gsutil cors set cors.json gs://my-bucket/

# Get bucket size
gsutil du -s gs://my-bucket/

# Create bucket
gsutil mb -l us-central1 gs://my-new-bucket/

# Delete bucket (must be empty)
gsutil rm -r gs://my-bucket/
```

### 12.3 bq -- BigQuery CLI

```bash
# Run query
bq query --use_legacy_sql=false 'SELECT * FROM dataset.table LIMIT 10'

# Create dataset
bq mk --dataset PROJECT_ID:my_dataset

# Create table from schema
bq mk --table my_dataset.my_table schema.json

# Load data from GCS
bq load --source_format=CSV my_dataset.my_table gs://bucket/data.csv schema.json

# Load JSON
bq load --source_format=NEWLINE_DELIMITED_JSON my_dataset.my_table gs://bucket/data.jsonl

# Export to GCS
bq extract my_dataset.my_table gs://bucket/export.csv

# List datasets
bq ls

# List tables
bq ls my_dataset

# Show table schema
bq show --schema my_dataset.my_table

# Delete table
bq rm -t my_dataset.my_table

# Cost estimate (dry run)
bq query --dry_run --use_legacy_sql=false 'SELECT * FROM dataset.table'
```

---

## 13. When to Choose GCP Over AWS/Azure

### Decision Matrix

| Criteria | Choose GCP | Choose AWS | Choose Azure |
|----------|-----------|-----------|-------------|
| **LLM-first application** | Gemini is cheapest frontier LLM | Widest model selection (Bedrock) | OpenAI integration |
| **Data warehouse/analytics** | BigQuery is best-in-class | Redshift if already on AWS | Synapse if MS ecosystem |
| **Serverless containers** | Cloud Run (best DX, scale-to-zero) | Fargate (more mature) | Container Apps |
| **Mobile/web app** | Firebase ecosystem | Amplify | — |
| **Kubernetes** | GKE Autopilot (Google invented K8s) | EKS (if AWS-native) | AKS |
| **Enterprise (existing)** | Rare | Most enterprises | Microsoft shops |
| **ML platform** | Vertex AI (tight Gemini) | SageMaker (most complete) | Azure ML |
| **Cost optimization** | Sustained-use auto-discounts | Savings Plans (manual) | Reserved Instances |
| **Global scale DB** | Spanner | DynamoDB Global Tables | Cosmos DB |
| **Regions** | 40 regions | 33 regions | 60+ regions |
| **Startup credits** | $100K-$200K (Google for Startups) | $100K (AWS Activate) | $150K (Microsoft for Startups) |

### GCP Strengths

1. **Gemini** -- Cheapest frontier LLM API. Gemini 2.0 Flash at $0.10/1M tokens is unbeatable.
2. **BigQuery** -- Best serverless data warehouse. Period. No cluster management, SQL-native ML, vector search built in.
3. **Cloud Run** -- Best serverless container platform. Scale-to-zero, GPU support, 60-min timeout, 1000 concurrent requests per instance.
4. **Firebase** -- Best mobile/web backend platform (auth, database, hosting, analytics).
5. **GKE** -- Google invented Kubernetes. GKE Autopilot is the easiest managed K8s.
6. **Pricing simplicity** -- Sustained-use discounts are automatic (no Savings Plans to manage).
7. **Data analytics** -- BigQuery + Looker + Dataflow + Dataproc is the strongest analytics stack.
8. **Network** -- Google's private fiber backbone means lower latency between regions.

### GCP Weaknesses

1. **Fewer regions** -- 40 vs AWS's 33 but many more edge locations on AWS (CloudFront 600+).
2. **Enterprise adoption** -- Smaller enterprise ecosystem, fewer compliance certifications (catching up).
3. **Service breadth** -- AWS has ~250 services vs GCP's ~150. Missing niche services.
4. **Support** -- AWS support is generally more responsive at lower tiers.
5. **Marketplace** -- AWS Marketplace has 10x more listings.
6. **IAM complexity** -- GCP IAM is powerful but different from AWS IAM; teams switching have a learning curve.
7. **Egress pricing** -- 25-33% more expensive than AWS for internet egress.
8. **No serverless Redis** -- AWS has ElastiCache Serverless; GCP Memorystore always-on only.

---

## 14. Quick Start Templates

### 14.1 Deploy FastAPI to Cloud Run

**Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# Cloud Run uses PORT env var
ENV PORT=8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
```

**requirements.txt:**

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
gunicorn==23.0.0
```

**main.py:**

```python
from fastapi import FastAPI
import os

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
async def root():
    return {"status": "healthy", "service": "my-api"}

@app.get("/health")
async def health():
    return {"status": "ok"}
```

**cloudbuild.yaml:**

```yaml
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-central1-docker.pkg.dev/$PROJECT_ID/apis/my-api:$COMMIT_SHA', '.']

  # Push the container image to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-central1-docker.pkg.dev/$PROJECT_ID/apis/my-api:$COMMIT_SHA']

  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-api'
      - '--image=us-central1-docker.pkg.dev/$PROJECT_ID/apis/my-api:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--memory=512Mi'
      - '--cpu=1'
      - '--min-instances=0'
      - '--max-instances=10'
      - '--concurrency=250'
      - '--allow-unauthenticated'

images:
  - 'us-central1-docker.pkg.dev/$PROJECT_ID/apis/my-api:$COMMIT_SHA'

options:
  logging: CLOUD_LOGGING_ONLY
```

**One-command deploy (no cloudbuild.yaml needed):**

```bash
gcloud run deploy my-api \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10
```

---

### 14.2 Vertex AI Embeddings + Vector Search

**Generate embeddings with Gemini Embedding 2:**

```python
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

# For text-embedding-005
model = TextEmbeddingModel.from_pretrained("text-embedding-005")
embeddings = model.get_embeddings(
    texts=["What is machine learning?", "How does AI work?"],
    output_dimensionality=768,  # MRL: 256, 512, or 768
)
for emb in embeddings:
    print(f"Dimension: {len(emb.values)}, Values: {emb.values[:5]}...")

# For Gemini Embedding 2 (multimodal)
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")

result = genai.embed_content(
    model="models/gemini-embedding-exp-03-07",
    content="What is machine learning?",
    output_dimensionality=3072,  # MRL: 768, 1536, or 3072
)
print(f"Embedding dimension: {len(result['embedding'])}")
```

**Store in AlloyDB with pgvector:**

```python
import asyncpg

async def setup_vector_table():
    conn = await asyncpg.connect(
        host="ALLOYDB_IP",
        database="mydb",
        user="postgres",
        password="PASSWORD",
    )
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding vector(768),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    # Create IVFFlat index (good for < 1M vectors)
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS documents_embedding_idx
        ON documents USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """)
    await conn.close()

async def search_similar(query_embedding: list[float], limit: int = 5):
    conn = await asyncpg.connect(...)
    results = await conn.fetch("""
        SELECT id, content, metadata,
               1 - (embedding <=> $1::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> $1::vector
        LIMIT $2;
    """, str(query_embedding), limit)
    await conn.close()
    return results
```

---

### 14.3 Cloud Storage + Signed URLs

```python
from google.cloud import storage
from datetime import timedelta

def generate_signed_url(
    bucket_name: str,
    blob_name: str,
    expiration_minutes: int = 60,
    method: str = "GET",
) -> str:
    """Generate a V4 signed URL for temporary access."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method=method,
        content_type="application/octet-stream" if method == "PUT" else None,
    )
    return url

# Download URL (GET)
download_url = generate_signed_url("my-bucket", "reports/q1.pdf", 60)

# Upload URL (PUT) -- client can upload directly to GCS
upload_url = generate_signed_url("my-bucket", "uploads/file.pdf", 15, "PUT")
```

**Upload directly from browser (CORS required):**

```json
// cors.json -- apply with: gsutil cors set cors.json gs://my-bucket
[
  {
    "origin": ["https://myapp.com"],
    "method": ["GET", "PUT", "POST"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
```

---

### 14.4 Firestore CRUD Pattern

```python
from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

# CREATE
def create_document(collection: str, data: dict) -> str:
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    doc_ref = db.collection(collection).document()
    doc_ref.set(data)
    return doc_ref.id

# READ (single)
def get_document(collection: str, doc_id: str) -> dict | None:
    doc = db.collection(collection).document(doc_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None

# READ (query)
def query_documents(
    collection: str,
    field: str,
    operator: str,
    value,
    limit: int = 100,
) -> list[dict]:
    query = (
        db.collection(collection)
        .where(field, operator, value)
        .limit(limit)
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in query.stream()]

# UPDATE
def update_document(collection: str, doc_id: str, updates: dict):
    updates["updated_at"] = datetime.utcnow()
    db.collection(collection).document(doc_id).update(updates)

# DELETE
def delete_document(collection: str, doc_id: str):
    db.collection(collection).document(doc_id).delete()

# BATCH WRITE (atomic, up to 500 ops)
def batch_create(collection: str, items: list[dict]):
    batch = db.batch()
    for item in items:
        item["created_at"] = datetime.utcnow()
        ref = db.collection(collection).document()
        batch.set(ref, item)
    batch.commit()

# REAL-TIME LISTENER
def listen_to_collection(collection: str, callback):
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "ADDED":
                callback("added", change.document.id, change.document.to_dict())
            elif change.type.name == "MODIFIED":
                callback("modified", change.document.id, change.document.to_dict())
            elif change.type.name == "REMOVED":
                callback("removed", change.document.id, None)

    db.collection(collection).on_snapshot(on_snapshot)
```

---

### 14.5 Cloud Run + Gemini Quick Pattern

```python
"""Cloud Run service that calls Gemini API."""
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."

class ChatResponse(BaseModel):
    response: str
    usage: dict

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = model.generate_content(
        [request.system_prompt, request.message],
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
        ),
    )
    return ChatResponse(
        response=response.text,
        usage={
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count,
        },
    )
```

**Deploy:**

```bash
gcloud run deploy gemini-chat \
  --source=. \
  --region=us-central1 \
  --set-env-vars="GEMINI_API_KEY=your-key" \
  --allow-unauthenticated \
  --memory=512Mi
```

**Better: Use Secret Manager for the API key:**

```bash
# Store the key
echo "your-api-key" | gcloud secrets create gemini-api-key --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy gemini-chat \
  --source=. \
  --region=us-central1 \
  --set-secrets="GEMINI_API_KEY=gemini-api-key:latest" \
  --allow-unauthenticated
```

---

## Appendix A: GCP Service → AWS Service Mapping

| GCP Service | AWS Equivalent |
|------------|---------------|
| Compute Engine | EC2 |
| Cloud Run | Fargate (closest) / App Runner |
| Cloud Functions | Lambda |
| GKE | EKS |
| App Engine | Elastic Beanstalk |
| Cloud Storage | S3 |
| Firestore | DynamoDB |
| Cloud SQL | RDS |
| AlloyDB | Aurora PostgreSQL |
| Bigtable | DynamoDB (wide-column) |
| BigQuery | Athena + Redshift |
| Memorystore | ElastiCache |
| Spanner | DynamoDB Global Tables / Aurora Global |
| Pub/Sub | SNS + SQS |
| Cloud Tasks | SQS (with delayed messages) |
| Cloud Scheduler | EventBridge Scheduler |
| Eventarc | EventBridge |
| Workflows | Step Functions |
| Vertex AI | SageMaker |
| Gemini API | Bedrock |
| Document AI | Textract |
| Vision AI | Rekognition |
| Natural Language AI | Comprehend |
| Translation AI | Translate |
| Speech-to-Text | Transcribe |
| Text-to-Speech | Polly |
| Cloud CDN | CloudFront |
| Cloud Load Balancing | ALB / NLB |
| Cloud DNS | Route 53 |
| IAM | IAM |
| Secret Manager | Secrets Manager |
| Cloud KMS | KMS |
| Cloud Armor | WAF + Shield |
| Cloud Build | CodeBuild |
| Artifact Registry | ECR |
| Cloud Deploy | CodeDeploy |
| Cloud Monitoring | CloudWatch |
| Cloud Logging | CloudWatch Logs |
| Cloud Trace | X-Ray |
| Error Reporting | (no direct equivalent) |
| Firebase | Amplify |

---

## Appendix B: GCP Regions for AI Workloads

**Best regions for Vertex AI (GPU availability + pricing):**

| Region | GPUs Available | Gemini Access | Latency (US) | Cost Tier |
|--------|---------------|---------------|-------------|-----------|
| us-central1 (Iowa) | All (T4, L4, A100, H100) | Yes | Low | Tier 1 |
| us-east1 (S. Carolina) | T4, L4, A100 | Yes | Low | Tier 1 |
| us-west1 (Oregon) | T4, L4, A100 | Yes | Low | Tier 1 |
| europe-west4 (Netherlands) | T4, L4, A100 | Yes | Medium | Tier 1 |
| asia-southeast1 (Singapore) | T4, L4 | Yes | High (from US) | Tier 2 |
| asia-south1 (Mumbai) | T4, L4 | Limited | High (from US) | Tier 2 |

**Recommendation:** Start with `us-central1` for AI workloads. Best GPU availability, cheapest pricing, and full Gemini access.

---

## Appendix C: Cost Optimization Checklist

- [ ] Enable sustained-use discounts (automatic for Compute Engine, GKE Standard)
- [ ] Use committed-use discounts for steady-state workloads (1-year: 37%, 3-year: 55%)
- [ ] Use Spot VMs for fault-tolerant training (60-91% discount)
- [ ] Set Cloud Run min-instances=0 for dev/staging
- [ ] Use BigQuery on-demand pricing until spend exceeds $5K/month
- [ ] Set Cloud Storage lifecycle policies (Standard -> Nearline -> Coldline -> Archive)
- [ ] Exclude noisy logs from Cloud Logging (save $0.50/GiB)
- [ ] Use Gemini Flash instead of Pro when accuracy difference is <5%
- [ ] Use batch API for embeddings ($0.10/1M vs $0.20/1M)
- [ ] Use text-embedding-005 at 256 dims for cost-sensitive workloads
- [ ] Enable Private Google Access (avoid NAT gateway charges)
- [ ] Use Cloud SQL Auth Proxy (avoid static IPs)
- [ ] Set budget alerts at 50%, 80%, 100% of monthly target
- [ ] Review billing reports weekly (Cloud Billing -> Reports)
- [ ] Use the Pricing Calculator before deploying anything new

---

*This document is a living reference. GCP pricing and features change regularly. Always verify at [cloud.google.com/pricing](https://cloud.google.com/pricing) before making architecture or purchasing decisions.*
