# Microsoft Azure for AI/ML Projects — Complete Reference

**Researched:** March 15, 2026
**Purpose:** Exhaustive reference for building AI/ML systems on Azure. Course material, consulting reference, and architecture decision guide.
**Companion doc:** `AWS-RAG-Production.md` (for AWS comparison)

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
10. [Pricing Comparisons vs AWS and GCP](#10-pricing-comparisons-vs-aws-and-gcp)
11. [Architecture Patterns for AI Projects](#11-architecture-patterns-for-ai-projects)
12. [Azure CLI Commands Reference](#12-azure-cli-commands-reference)
13. [When to Choose Azure Over AWS/GCP](#13-when-to-choose-azure-over-awsgcp)
14. [Quick Start Templates](#14-quick-start-templates)
15. [Enterprise Features](#15-enterprise-features-why-enterprises-choose-azure)

---

## 1. AI/ML Services (Deep Dive)

### 1A. Azure OpenAI Service

Azure OpenAI provides enterprise-grade access to OpenAI models with Azure's security, compliance, and regional data residency. Unlike the direct OpenAI API, Azure OpenAI offers content filtering, private networking (Private Link), managed identity auth, and enterprise SLAs.

#### Models and Pricing (Per 1M Tokens)

**Flagship Models:**

| Model | Input | Output | Cached Input | Context | Best For |
|-------|-------|--------|-------------|---------|----------|
| GPT-4o | $2.50 | $10.00 | $1.25 | 128K | General-purpose, vision, structured output |
| GPT-4o-mini | $0.15 | $0.60 | $0.075 | 128K | Cost-efficient tasks, high volume |
| GPT-4.1 | $2.00 | $8.00 | $0.50 | 1M | Long-context coding, instruction following |
| GPT-4.1-mini | $0.40 | $1.60 | $0.10 | 1M | Budget long-context |
| GPT-4.1-nano | $0.10 | $0.40 | $0.025 | 1M | Cheapest, classification, extraction |

**Reasoning Models:**

| Model | Input | Output | Context | Best For |
|-------|-------|--------|---------|----------|
| o1 | $15.00 | $60.00 | 200K | Complex reasoning, math, science |
| o3 | $2.00 | $8.00 | 200K | Balanced reasoning (replaced o3-mini-high) |
| o3-mini | $0.55 | $2.20 | 200K | Budget reasoning |
| o4-mini | $1.10 | $4.40 | 200K | Code + tool-use reasoning |

**Embedding Models:**

| Model | Price per 1M Tokens | Dimensions | Max Tokens |
|-------|-------------------|------------|------------|
| text-embedding-3-small | $0.02 | 512-1536 | 8,191 |
| text-embedding-3-large | $0.13 | 256-3072 | 8,191 |
| text-embedding-ada-002 | $0.10 | 1536 | 8,191 |

**Audio Models:**

| Model | Pricing |
|-------|---------|
| Whisper | $0.36/hour (batch) |
| TTS | $15.00 per 1M characters |
| TTS HD | $30.00 per 1M characters |
| GPT-4o Realtime | $5.00 input / $20.00 output (text), $40/$80 (audio) per 1M tokens |

**Image Models:**

| Model | Standard | HD |
|-------|----------|-----|
| DALL-E 3 (1024x1024) | $0.040/image | $0.080/image |
| DALL-E 3 (1792x1024) | $0.080/image | $0.120/image |
| GPT-Image-1 (1024x1024) | $0.040 (low) - $0.167 (high) | - |

#### Deployment Types

| Type | Description | SLA | Best For |
|------|-------------|-----|----------|
| **Global Standard** | Routes to any Azure datacenter globally | Yes | Highest throughput, lowest latency, best default |
| **Standard (Regional)** | Fixed to a specific Azure region | Yes | Data residency requirements |
| **DataZone Standard** | Routes within US or EU zone | Yes | Geo-compliance (GDPR) |
| **Provisioned (PTU)** | Reserved capacity, predictable throughput | Yes | Steady-state production, latency-sensitive |
| **Global Batch** | Async processing, 24hr turnaround | No | Bulk processing at 50% discount |
| **DataZone Batch** | Batch within US/EU zone | No | Geo-compliant batch |

**Provisioned Throughput Units (PTU):**
- Billed hourly, monthly, or annually
- Monthly commitment: ~15% discount vs hourly
- Annual commitment: ~30% discount vs hourly
- Minimum: varies by model (typically 50-100 PTUs)
- 1 PTU for GPT-4o processes ~6 requests/minute at 800 tokens each (varies)

#### Quotas and Limits

| Limit | Value |
|-------|-------|
| Max deployments per resource | 30 |
| Max tokens per request (GPT-4o) | 16,384 output / 128K context |
| Default rate limit (GPT-4o Global) | 450K TPM (tokens per minute) |
| Default rate limit (GPT-4o-mini Global) | 2M TPM |
| Max requests per minute | Varies by tier (Tier 1: 60 RPM, Tier 5: 10K RPM) |
| Regions available | 27+ (East US, West US, Sweden Central, etc.) |

#### Content Filtering

Azure OpenAI includes mandatory content filtering (can be partially customized):
- **Categories:** Hate, Sexual, Violence, Self-harm (4 severity levels: safe, low, medium, high)
- **Prompt Shields:** Detect jailbreak attempts and indirect prompt injection
- **Protected Material Detection:** Detect copyrighted text/code in outputs
- **Groundedness Detection:** Detect hallucinations vs grounding sources
- **Custom filters:** Blocklists for specific terms/phrases
- **Annotation mode:** Returns filter results without blocking (for monitoring)

**When to use content filtering:**
- Enterprise deployments: Always on (compliance requirement)
- Internal tools: Can request reduced filtering via Microsoft form
- Development: Use annotation mode to monitor without blocking

#### When to Use Each Model

| Use Case | Model | Why |
|----------|-------|-----|
| General chatbot / copilot | GPT-4o | Best balance of quality and cost |
| High-volume classification | GPT-4o-mini or GPT-4.1-nano | 15-25x cheaper than GPT-4o |
| RAG with long documents | GPT-4.1 | 1M context, best instruction-following |
| Complex reasoning/math | o3 or o4-mini | Chain-of-thought reasoning |
| Code generation | GPT-4.1 or o4-mini | Top coding benchmarks |
| Embeddings for search | text-embedding-3-small | Best cost/performance for most use cases |
| High-dimensional embeddings | text-embedding-3-large | When you need 3072 dims for fine-grained similarity |
| Audio transcription | Whisper | $0.36/hr batch is very competitive |
| Voice agents | GPT-4o Realtime | Native voice-to-voice, lowest latency |
| Bulk processing | Global Batch | 50% discount, 24hr turnaround |

---

### 1B. Azure AI Search (formerly Cognitive Search)

Enterprise search service with native vector search, hybrid search, and semantic ranking. The go-to choice for RAG on Azure.

#### Core Capabilities

- **Full-text search:** BM25 ranking, analyzers, scoring profiles, facets, filters
- **Vector search:** HNSW and exhaustive KNN algorithms, up to 3072 dimensions
- **Hybrid search:** BM25 + vector in a single query with Reciprocal Rank Fusion (RRF)
- **Semantic ranker:** Microsoft's deep learning re-ranking model (L2 cross-encoder)
- **Integrated vectorization:** Built-in embedding via Azure OpenAI or custom skill
- **Skillsets:** AI enrichment pipeline (OCR, NER, translation, custom skills)
- **Knowledge Store:** Project enriched data to tables/blobs for downstream analytics
- **Security trimming:** Filter results based on user identity/roles

#### Pricing Tiers

| Tier | Monthly Cost | Storage | Indexes | Partitions | Replicas | SLA |
|------|-------------|---------|---------|------------|----------|-----|
| **Free** | $0 | 50 MB | 3 | 1 | 1 | None |
| **Basic** | ~$74 | 2 GB | 15 | 1 | 3 | 99.9% |
| **S1 (Standard)** | ~$245 | 25 GB/partition | 50 | 12 | 12 | 99.9% |
| **S2** | ~$981 | 100 GB/partition | 200 | 12 | 12 | 99.9% |
| **S3** | ~$1,962 | 200 GB/partition | 200 | 12 | 12 | 99.9% |
| **S3 HD** | ~$1,962 | 200 GB/partition | 1000 | 3 | 12 | 99.9% |
| **L1 (Storage Opt)** | ~$980 | 1 TB/partition | 10 | 12 | 12 | 99.9% |
| **L2** | ~$1,962 | 2 TB/partition | 10 | 12 | 12 | 99.9% |

**Semantic Ranker Pricing:**
- Free: 1,000 queries/month (all paid tiers)
- Standard: $1 per 1,000 queries beyond free allowance

**Key Limits:**
- Free tier: 50 MB storage, 3 indexes, no semantic ranker, no replicas
- Basic: 2 GB, 15 indexes, 1 partition (no scaling), up to 3 replicas
- Vector dimensions: up to 3072 per field
- Vector fields per index: up to 500 (S1+)
- Document size: 16 MB max

#### Integrated Vectorization

Azure AI Search can automatically vectorize documents during indexing and queries:

```
Indexer → Skillset → Embedding Skill (Azure OpenAI) → Vector Index
```

This eliminates the need for custom embedding pipelines. Configure once, and new documents are automatically vectorized.

**Supported embedding models:**
- Azure OpenAI (text-embedding-3-small, text-embedding-3-large, ada-002)
- Azure AI Vision (multimodal embeddings)
- Custom Web API skill (bring your own model)

#### AWS Equivalent: Amazon OpenSearch Serverless + Amazon Kendra
#### GCP Equivalent: Vertex AI Search (formerly Enterprise Search)

**Key difference:** Azure AI Search is the only managed search service with native hybrid (BM25 + vector) search AND semantic re-ranking in a single query. OpenSearch requires custom implementation of RRF. Kendra is keyword-only; Vertex AI Search has vector but less mature.

---

### 1C. Azure AI Document Intelligence (formerly Form Recognizer)

Extracts text, structure, key-value pairs, and tables from documents using pre-built and custom models.

#### Models

| Model | What It Extracts | Pricing (S0 per page) |
|-------|-----------------|----------------------|
| **Read (OCR)** | Text, lines, words, language detection | $0.001 (1,000 pages = $1) |
| **Layout** | Text + tables + selection marks + structure | $0.01 (100 pages = $1) |
| **General Document** | Key-value pairs + entities + tables | $0.0125 (80 pages = $1) |
| **Prebuilt: Invoice** | Invoice fields (vendor, total, line items) | $0.01/page |
| **Prebuilt: Receipt** | Receipt fields (merchant, total, date) | $0.001/page |
| **Prebuilt: ID Document** | Name, DOB, address from IDs/passports | $0.10/page |
| **Prebuilt: W-2 / Tax** | Tax form fields | $0.01/page |
| **Custom: Template** | Your own labeled fields (fixed layout) | $0.05/page + $10/hr training |
| **Custom: Neural** | Your own labeled fields (variable layout) | $0.05/page + $10/hr training |
| **Custom: Composed** | Route to multiple custom models | Same as custom |

**Free tier:** 500 pages/month (all prebuilt models), 2 custom model training sessions

**Batch processing:** Up to 2,000 pages per request (async API)

#### When to Use

| Scenario | Model |
|----------|-------|
| Simple text extraction from PDFs | Read |
| Extract tables from reports | Layout |
| Process invoices at scale | Prebuilt: Invoice |
| Extract data from custom forms | Custom: Neural (variable) or Template (fixed) |
| RAG document ingestion | Layout (preserves structure for chunking) |

#### AWS Equivalent: Amazon Textract
#### GCP Equivalent: Document AI

**Key difference:** Azure's Layout model is significantly better at preserving document structure (headers, sections, reading order) which matters for RAG. Textract is cheaper for pure OCR but lacks structure awareness.

---

### 1D. Azure AI Speech

#### Speech-to-Text (STT)

| Feature | Real-time | Batch | Custom |
|---------|-----------|-------|--------|
| **Pricing** | $1.00/hr | $0.36/hr | $1.20/hr (real-time) |
| **Latency** | <500ms | Minutes | <500ms |
| **Languages** | 100+ | 100+ | Your domain |
| **Max audio** | Streaming | 1GB/file | Streaming |
| **Use case** | Live transcription | Meeting recordings | Medical/legal jargon |

**Whisper on Azure OpenAI:** $0.36/hr (batch), identical to batch STT pricing but better for multilingual content.

#### Text-to-Speech (TTS)

| Feature | Neural | Neural HD | Custom Neural |
|---------|--------|-----------|---------------|
| **Pricing** | $16/1M chars | $16/1M chars | $24/1M chars |
| **Long audio** | $100/1M chars | - | - |
| **Voices** | 400+ (140 languages) | - | Clone your voice |
| **SSML** | Yes | Yes | Yes |
| **Streaming** | Yes | Yes | Yes |

**Free tier:** 5 hours STT, 0.5M characters TTS per month

#### AWS Equivalent: Amazon Transcribe (STT), Amazon Polly (TTS)
#### GCP Equivalent: Cloud Speech-to-Text, Cloud Text-to-Speech

**Comparison:**
- STT real-time: Azure $1/hr vs AWS $0.96/hr vs GCP $0.96/hr (nearly identical)
- STT batch: Azure $0.36/hr vs AWS $0.48/hr (Azure cheaper)
- TTS: Azure $16/1M chars vs AWS $16/1M chars vs GCP $16/1M chars (identical for neural)

---

### 1E. Azure AI Vision

| Capability | What It Does | Pricing |
|-----------|-------------|---------|
| **Image Analysis 4.0** | Tags, captions, objects, people, read text | $1.00/1K transactions |
| **OCR (Read)** | Extract text from images | $1.00/1K transactions |
| **Spatial Analysis** | People counting, distance, dwell time (video) | $0.112/hr per camera |
| **Custom Image Classification** | Train on your images | $2/1K train images + $1/1K predictions |
| **Face API** | Detection, verification, identification | $1.00/1K calls (detection) |
| **Multimodal Embeddings** | Image + text in same vector space | Included in Image Analysis |

**Free tier:** 5,000 transactions/month (Image Analysis), 1,000 transactions (Face detection)

#### AWS Equivalent: Amazon Rekognition
#### GCP Equivalent: Cloud Vision AI

---

### 1F. Azure AI Language

| Feature | What It Does | Pricing (S tier) |
|---------|-------------|-----------------|
| **NER** | Named entity recognition (person, org, location) | $1.00/1K text records |
| **Sentiment Analysis** | Positive/negative/neutral + opinion mining | $1.00/1K text records |
| **PII Detection** | SSN, credit card, phone, email, 100+ types | $1.00/1K text records |
| **Key Phrase Extraction** | Important phrases from text | $1.00/1K text records |
| **Language Detection** | Detect language of text | $1.00/1K text records |
| **Summarization** | Extractive + abstractive summaries | $2.00/1K text records |
| **Custom Text Classification** | Train on your labels | $3.50/1K text records + $3/hr training |
| **Custom NER** | Train on your entity types | $5.00/1K text records + $3/hr training |
| **Question Answering** | FAQ-style QA from documents | $1.00/1K text records |

**Free tier:** 5,000 text records/month

**Text record:** Up to 1,000 characters. Larger documents are split into multiple records.

#### AWS Equivalent: Amazon Comprehend
#### GCP Equivalent: Cloud Natural Language API

---

### 1G. Azure AI Content Safety

| Feature | What It Does | Pricing |
|---------|-------------|---------|
| **Text Moderation** | Hate, sexual, violence, self-harm (4 severity levels) | $0.75/1K text records (S0) |
| **Image Moderation** | Same categories for images | $1.50/1K images |
| **Prompt Shields** | Detect jailbreak + indirect prompt injection | Included with text moderation |
| **Groundedness Detection** | Detect hallucinations against source | $2.00/1K text records |
| **Protected Material Detection** | Detect copyrighted text/code | Included with text moderation |
| **Custom Categories** | Define your own content categories | $2.00/1K text records |
| **Blocklists** | Block specific terms/phrases | Included |

**Free tier:** 1,000 text records, 1,000 images per month

**Key insight:** This is the only major cloud provider with built-in prompt injection detection (Prompt Shields) as a standalone API. AWS and GCP rely on Bedrock Guardrails and Vertex AI Safety, respectively, which are model-specific rather than standalone.

---

### 1H. Azure Machine Learning

A complete MLOps platform for training, deploying, and managing ML models.

#### Compute Options

| Compute Type | What It Is | Pricing |
|-------------|-----------|---------|
| **Compute Instance** | Dev VM (Jupyter, VS Code) | Pay for VM (see GPU VMs below) |
| **Compute Cluster** | Auto-scaling training cluster | Pay for VMs only when running |
| **Managed Online Endpoint** | Real-time inference hosting | Pay for VM + $0.20/10K API requests |
| **Batch Endpoint** | Async batch inference | Pay for VM only during processing |
| **Serverless Endpoint** | Pay-per-token for catalog models | Per-token pricing (varies by model) |
| **Kubernetes Endpoint** | Deploy to AKS | Pay for AKS nodes |

**No charge for Azure ML itself** -- you pay only for underlying compute, storage, and networking.

#### AutoML

Automated machine learning for tabular, image, and NLP tasks:
- **Tabular:** Classification, regression, forecasting
- **Image:** Classification, object detection, segmentation
- **NLP:** Text classification, NER, question answering
- **Pricing:** No additional charge beyond compute

#### MLflow Integration

Azure ML has native MLflow support:
- Track experiments with MLflow tracking
- Register models in MLflow model registry
- Deploy MLflow models to managed endpoints
- No additional cost

#### Model Catalog

Access to 1,900+ models including:
- Meta Llama 3.x, Llama 4
- Mistral/Mixtral
- Cohere Command/Embed/Rerank
- Microsoft Phi-3/Phi-4
- NVIDIA NIM microservices
- Stability AI SDXL

**Serverless (pay-per-token) deployment** available for many catalog models -- no VM management needed.

#### AWS Equivalent: Amazon SageMaker
#### GCP Equivalent: Vertex AI

---

### 1I. Azure AI Studio / Azure AI Foundry

Microsoft rebranded Azure AI Studio to "Microsoft AI Foundry" in late 2025. It is the unified portal for building AI applications.

#### Key Features

| Feature | Description |
|---------|-------------|
| **Playground** | Test any model (OpenAI, catalog) with system prompts, parameters, images |
| **Prompt Flow** | Visual DAG editor for LLM pipelines (chain, branch, parallel) |
| **Model Catalog** | Browse, test, deploy 1,900+ models (OpenAI, Meta, Mistral, Cohere, etc.) |
| **Evaluations** | Built-in eval metrics (groundedness, relevance, coherence, fluency) |
| **Fine-tuning** | Fine-tune GPT-4o-mini, GPT-4.1-mini, Phi, Llama on your data |
| **Tracing** | OpenTelemetry-based tracing for prompt flow runs |
| **Content Safety** | Integrated content filtering configuration |
| **Connections** | Manage connections to Azure OpenAI, AI Search, Storage, custom APIs |

**Prompt Flow** is particularly powerful for RAG:
1. Build a flow: Query -> Embedding -> AI Search -> LLM -> Response
2. Test with sample data in the portal
3. Evaluate with built-in metrics
4. Deploy as a managed online endpoint with one click

**Pricing:** No charge for AI Studio/Foundry itself. You pay for the underlying services (Azure OpenAI calls, AI Search, compute for endpoints).

---

## 2. Compute & Deployment

### 2A. Azure Container Apps (ACA)

Serverless container platform with built-in auto-scaling, Dapr integration, and managed ingress. The recommended service for deploying AI APIs on Azure.

#### Pricing Plans

| Plan | vCPU | Memory | Pricing | Idle Charges |
|------|------|--------|---------|-------------|
| **Consumption** | 0-4 vCPU | 0-8 GB | $0.000024/vCPU-sec + $0.000003/GiB-sec | Scale to zero, no idle charge |
| **Dedicated (D4)** | 4 vCPU | 16 GB | ~$245/month per instance | Always-on, billed even idle |
| **Dedicated (D8)** | 8 vCPU | 32 GB | ~$490/month per instance | Always-on |
| **Dedicated (D16)** | 16 vCPU | 64 GB | ~$980/month per instance | Always-on |
| **GPU (Consumption)** | 1x T4 | 16 GB | ~$0.000376/sec (~$1.35/hr) | Scale to zero |
| **GPU (Consumption)** | 1x A100 | 80 GB | ~$0.001111/sec (~$4.00/hr) | Scale to zero |

**Free allowance (monthly, per subscription):**
- 180,000 vCPU-seconds
- 360,000 GiB-seconds
- 2 million requests

**Key Features:**
- Scale to zero (Consumption plan)
- Scale based on HTTP traffic, KEDA scalers (queue length, CPU, custom metrics)
- Dapr integration for microservice communication
- Built-in ingress with TLS, custom domains
- Revisions for blue/green deployments
- Jobs: run-to-completion tasks (cron, event-triggered)
- GPU support (serverless, no VM management)

**Cold start:** Typically 2-5 seconds for Consumption plan. Mitigate with min replicas = 1 (~$15/month for a 0.25 vCPU / 0.5 GB container).

#### vs AWS ECS Fargate vs GCP Cloud Run

| Feature | Azure Container Apps | AWS ECS Fargate | GCP Cloud Run |
|---------|---------------------|-----------------|---------------|
| **Scale to zero** | Yes | No (min 1 task) | Yes |
| **GPU** | Yes (T4, A100) | No (use EC2) | Yes (L4, A100) |
| **Cold start** | 2-5s | N/A (always running) | 1-3s |
| **Min cost** | $0 (free tier) | ~$10/month (1 task) | $0 (free tier) |
| **Dapr** | Built-in | Manual | Not native |
| **Ingress** | Built-in | Need ALB ($16/mo) | Built-in |
| **Sidecar containers** | Yes | Yes | Yes |
| **Jobs** | Yes | ECS Tasks | Cloud Run Jobs |
| **vCPU pricing** | $0.000024/sec | $0.000011/sec | $0.000024/sec |

**Bottom line:** ACA is comparable in price to Cloud Run and both are cheaper than Fargate for bursty workloads. Fargate wins for steady-state workloads (no cold starts). ACA's GPU support is a major differentiator for AI workloads.

---

### 2B. Azure App Service

Platform-as-a-Service for web apps. Best for simple web APIs, backends, and full-stack apps.

#### Pricing Tiers

| Tier | vCPU | RAM | Storage | Monthly Cost | Key Features |
|------|------|-----|---------|-------------|-------------|
| **F1 (Free)** | Shared | 1 GB | 1 GB | $0 | 60 CPU min/day, no custom domain |
| **B1 (Basic)** | 1 | 1.75 GB | 10 GB | ~$55 | Custom domain, manual scale |
| **B2** | 2 | 3.5 GB | 10 GB | ~$109 | Same as B1 with more resources |
| **S1 (Standard)** | 1 | 1.75 GB | 50 GB | ~$73 | Auto-scale, staging slots, backups |
| **S2** | 2 | 3.5 GB | 50 GB | ~$146 | Same with more resources |
| **P0v3 (Premium)** | 1 | 4 GB | 250 GB | ~$120 | Zone redundancy, VNet integration |
| **P1v3** | 2 | 8 GB | 250 GB | ~$138 | Same with more resources |
| **P2v3** | 4 | 16 GB | 250 GB | ~$275 | Same with more resources |
| **P3v3** | 8 | 32 GB | 250 GB | ~$550 | Same with more resources |

(Linux pricing shown. Windows is ~25% more expensive.)

**Key Features:**
- Deployment slots (staging/production swap)
- Auto-scaling (Standard+)
- Custom domains + managed TLS certificates (Basic+)
- VNet integration (Premium+)
- WebSockets, HTTP/2
- Built-in CI/CD (GitHub Actions, Azure DevOps)

**When to use App Service vs Container Apps:**
- App Service: Simple web apps, .NET/Node/Python/Java, no containers needed
- Container Apps: Microservices, event-driven, need GPU, scale-to-zero, Dapr

#### AWS Equivalent: Elastic Beanstalk / App Runner
#### GCP Equivalent: App Engine / Cloud Run

---

### 2C. Azure Functions

Serverless compute for event-driven code.

#### Pricing Plans

| Plan | Pricing | Cold Start | Max Duration | VNet | Scale |
|------|---------|-----------|-------------|------|-------|
| **Consumption** | $0.20/M executions + $0.000016/GB-s | 1-10s | 5 min (10 min max) | No | 0 to 200 instances |
| **Flex Consumption** | $0.20/M executions + $0.000016/GB-s | <1s (always ready) | Unlimited | Yes | 0 to 1000 instances |
| **Premium (EP1)** | ~$117/month (1 vCPU) | None | Unlimited | Yes | 1 to 100 instances |
| **Dedicated** | App Service plan pricing | None | Unlimited | Yes | Manual/auto-scale |

**Free allowance (Consumption):**
- 1,000,000 executions/month
- 400,000 GB-seconds/month

**Flex Consumption free allowance:**
- 250,000 executions/month
- 100,000 GB-seconds/month

#### Triggers & Bindings

| Trigger | Description |
|---------|-------------|
| HTTP | REST API endpoints |
| Timer | Cron-scheduled execution |
| Queue Storage | Process queue messages |
| Blob Storage | React to new/modified blobs |
| Service Bus | Process Service Bus messages |
| Event Grid | React to events |
| Event Hub | Process streaming data |
| Cosmos DB | React to document changes (change feed) |
| Durable Functions | Stateful workflows, fan-out/fan-in, human interaction |

#### Durable Functions

Stateful orchestrations for complex workflows:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Function Chaining** | Sequential execution | ETL pipelines |
| **Fan-out/Fan-in** | Parallel execution, aggregate results | Batch document processing |
| **Async HTTP APIs** | Long-running operations with status polling | AI model inference |
| **Monitor** | Periodic polling until condition met | Wait for approval |
| **Human Interaction** | Pause workflow for human input | Approval workflows |
| **Aggregator** | Accumulate events over time | Event aggregation |

**Pricing:** Same as the hosting plan (Consumption, Premium, etc.). No additional charge for Durable Functions.

#### AWS Equivalent: AWS Lambda + Step Functions
#### GCP Equivalent: Cloud Functions + Cloud Workflows

**Comparison:**
- Cold start: Azure Flex Consumption < GCP Cloud Functions Gen2 < AWS Lambda (with SnapStart)
- Max duration: Azure Consumption 10 min vs Lambda 15 min vs GCP 60 min
- Free tier: Azure 1M executions vs Lambda 1M vs GCP 2M

---

### 2D. Azure Kubernetes Service (AKS)

Managed Kubernetes with free control plane.

#### Pricing

| Component | Cost |
|-----------|------|
| **Control plane** | Free (Standard tier: $73/month for SLA + uptime guarantees) |
| **Worker nodes** | Pay for VMs (see GPU VMs below) |
| **Node auto-provisioning** | Included (KEDA-based) |
| **Virtual nodes (ACI)** | Per-second billing (ACI pricing) |
| **Managed GPU nodes** | Preview -- auto-install NVIDIA drivers |

**Standard Tier ($73/month):** 99.95% SLA, autoscaler, multiple node pools, up to 5,000 nodes
**Premium Tier ($146/month):** Long-term support, mission-critical workloads

#### GPU Node Pools

| VM Series | GPU | vCPU | RAM | GPU Memory | On-Demand/hr | Spot/hr |
|-----------|-----|------|-----|-----------|-------------|---------|
| **NC6s v3** | 1x V100 | 6 | 112 GB | 16 GB | ~$3.06 | ~$0.92 |
| **NC24s v3** | 4x V100 | 24 | 448 GB | 64 GB | ~$12.24 | ~$3.67 |
| **NC24ads A100 v4** | 1x A100 | 24 | 220 GB | 80 GB | ~$3.67 | ~$1.37 |
| **ND96asr A100 v4** | 8x A100 | 96 | 900 GB | 640 GB | ~$27.20 | ~$8.16 |
| **NC40ads H100 v5** | 1x H100 | 40 | 320 GB | 80 GB | ~$6.98 | ~$2.09 |

**KEDA auto-scaling:** Scale pods based on external metrics (queue length, CPU, HTTP requests, custom). Free and built into AKS.

#### AWS Equivalent: Amazon EKS ($73/month control plane)
#### GCP Equivalent: Google Kubernetes Engine (GKE Autopilot: pay per pod)

---

### 2E. Azure Container Instances (ACI)

Simple container hosting without orchestration. Run a container in seconds.

| Resource | Per-Second Price |
|----------|-----------------|
| vCPU | $0.0000130 (~$34/month for 1 vCPU) |
| Memory | $0.0000014/GB (~$3.70/month for 1 GB) |
| GPU (V100) | $0.00390/sec (~$338/day) |
| GPU (T4) | $0.00022/sec (~$19/day) |

**Use case:** Quick dev/test containers, CI/CD build agents, burstable AKS (virtual nodes), sidecar containers.

**Limits:** No auto-scaling, no ingress management, 240 GB max memory, 4 GPU max.

---

### 2F. Azure Virtual Machines (GPU)

For direct VM access (ML training, fine-tuning, custom inference).

| Series | GPU | Use Case | On-Demand/hr | Spot/hr | 1yr Reserved |
|--------|-----|----------|-------------|---------|-------------|
| **NCv3** | V100 | Training, inference | $3.06-$12.24 | $0.92-$3.67 | ~40% off |
| **NCads A100 v4** | A100 80GB | Large model training | $3.67 | $1.37 | ~40% off |
| **NDm A100 v4** | 8x A100 | Distributed training | $27.20 | $8.16 | ~40% off |
| **NCads H100 v5** | H100 80GB | Frontier model training | $6.98 | $2.09 | ~40% off |
| **NVadsA10 v5** | A10 24GB | Inference, rendering | $0.90 | $0.27 | ~40% off |

**Spot VMs:** Up to 90% discount, can be evicted with 30-second notice. Great for interruptible training jobs.

**Reserved Instances:** 1-year (30-40% off) or 3-year (50-60% off) commitments.

**Azure Savings Plan for Compute:** Commit to a $/hour spend across any VM, App Service, or Container Apps. Flexible across regions and VM types. 1-year or 3-year terms.

---

## 3. Storage & Databases

### 3A. Azure Blob Storage

Object storage for unstructured data (files, images, videos, documents, model artifacts).

#### Access Tiers

| Tier | Storage/GB/month | Read/10K ops | Write/10K ops | Retrieval/GB | Min Duration |
|------|-----------------|-------------|-------------- |-------------|-------------|
| **Hot** | $0.018 (first 50TB) | $0.004 | $0.05 | Free | None |
| **Cool** | $0.010 | $0.01 | $0.10 | $0.01 | 30 days |
| **Cold** | $0.0036 | $0.01 | $0.18 | $0.03 | 90 days |
| **Archive** | $0.00099 | $5.00 | $0.10 | $0.02 (std) / $0.06 (high) | 180 days |

**Egress pricing:**
- First 100 GB/month: Free
- 100 GB - 10 TB: $0.087/GB
- 10 TB - 50 TB: $0.083/GB
- 50 TB+: $0.07/GB

**SAS Tokens (Shared Access Signatures):**
Azure's equivalent to S3 presigned URLs. Generate time-limited, permission-scoped access to specific blobs or containers.

```python
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

sas_token = generate_blob_sas(
    account_name="mystorageaccount",
    container_name="documents",
    blob_name="file.pdf",
    account_key="<key>",
    permission=BlobSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)
url = f"https://mystorageaccount.blob.core.windows.net/documents/file.pdf?{sas_token}"
```

**Lifecycle Management:**
Automatically move blobs between tiers based on age rules. Example: Hot -> Cool after 30 days, Cool -> Archive after 90 days, delete after 365 days.

**CDN Integration:** Azure CDN or Front Door can cache blob content at edge. Enable with one click in portal.

**Free tier:** 5 GB LRS Hot storage, 20K read operations, 10K write operations per month (12 months)

#### vs S3 vs GCS

| Feature | Azure Blob | AWS S3 | GCP GCS |
|---------|-----------|--------|---------|
| Hot storage/GB | $0.018 | $0.023 | $0.020 |
| Cool/Nearline | $0.010 | $0.0125 | $0.010 |
| Archive | $0.00099 | $0.004 | $0.0012 |
| Egress (first 100GB) | Free | Free | Free |
| Egress (100GB-10TB) | $0.087/GB | $0.09/GB | $0.12/GB |
| Free tier | 5 GB (12 months) | 5 GB (always free) | 5 GB (always free) |

**Azure is cheapest for storage, AWS has best tooling, GCS is competitive on price.**

---

### 3B. Azure Cosmos DB

Globally distributed, multi-model NoSQL database with single-digit millisecond latency.

#### Pricing Models

| Model | Pricing | Best For |
|-------|---------|----------|
| **Serverless** | $0.25 per 1M RU (request units) | Dev/test, unpredictable traffic |
| **Provisioned** | $0.008/hr per 100 RU/s (manual) | Predictable, steady workloads |
| **Autoscale** | $0.012/hr per 100 RU/s (auto-adjusts) | Variable but not spiky |

**What is a Request Unit (RU)?**
- 1 RU = reading a single 1KB document by ID
- Point writes: ~5.5 RU per 1KB document
- Query (simple): 3-10 RU
- Query (complex/cross-partition): 50-500+ RU
- Vector search query: 10-50 RU per query (depends on vector dimensions and index type)

#### Free Tier

| Resource | Free Amount | Notes |
|----------|------------|-------|
| **Provisioned throughput** | 1,000 RU/s | Lifetime (one account per subscription) |
| **Storage** | 25 GB | Lifetime |
| **Free account (30 days)** | 400 RU/s + 25 GB | Trial credit |

**Important:** Free tier applies to provisioned throughput only, NOT serverless.

#### Vector Search (DiskANN)

Cosmos DB for NoSQL includes native vector search using Microsoft's DiskANN algorithm:

- **Algorithm:** DiskANN (quantized vectors in memory, full vectors on SSD)
- **Dimensions:** Up to 4096
- **Distance metrics:** Cosine, dot product, Euclidean
- **Index types:** Flat (exact), Quantized Flat, DiskANN (approximate, recommended)
- **Performance:** <20ms latency over 10M vectors
- **Cost:** ~43x lower query cost vs Pinecone, ~12x lower vs Zilliz (Microsoft's benchmarks)
- **Integration:** Native with Azure AI Search (automatic hybrid search)

```python
# Cosmos DB vector search example
container.query_items(
    query="""
    SELECT TOP 5 c.id, c.content,
           VectorDistance(c.embedding, @queryVector) AS score
    FROM c
    ORDER BY VectorDistance(c.embedding, @queryVector)
    """,
    parameters=[{"name": "@queryVector", "value": query_embedding}],
    partition_key="default"
)
```

#### APIs (Multi-Model)

| API | Data Model | Compatibility | Use Case |
|-----|-----------|---------------|----------|
| **NoSQL** | Document (JSON) | SQL-like queries | General purpose, RAG, chat history |
| **MongoDB** | Document (BSON) | MongoDB wire protocol | Migrate existing MongoDB apps |
| **PostgreSQL** | Relational | PostgreSQL wire protocol | Distributed PostgreSQL (Citus) |
| **Cassandra** | Wide-column | Cassandra wire protocol | High-write throughput |
| **Gremlin** | Graph | TinkerPop Gremlin | Knowledge graphs |
| **Table** | Key-value | Azure Table API | Simple key-value lookups |

#### Global Distribution

- Replicate to 60+ Azure regions
- Multi-write (multi-master) for write-anywhere
- Automatic failover
- 5 consistency levels: Strong, Bounded Staleness, Session (default), Consistent Prefix, Eventual
- Reads from nearest replica (low latency globally)

#### AWS Equivalent: DynamoDB (document), Neptune (graph)
#### GCP Equivalent: Firestore / Cloud Spanner

**Key difference:** Cosmos DB is the only database that offers 5 tunable consistency levels (DynamoDB has 2: eventual and strong). The free tier is generous (1,000 RU/s forever). DiskANN vector search is built-in; DynamoDB has no native vector search.

---

### 3C. Azure SQL Database

Managed SQL Server with AI-ready features.

| Tier | Model | Pricing | Best For |
|------|-------|---------|----------|
| **Serverless (Gen Purpose)** | Auto-pause, auto-scale | $0.000145/vCore-second + $0.25/GB storage | Dev/test, intermittent workloads |
| **Provisioned (Gen Purpose)** | Always-on | $0.2529/vCore-hr (2 vCore min) | Predictable workloads |
| **Hyperscale** | 100 TB+, read replicas | $0.3844/vCore-hr | Large databases |
| **Business Critical** | In-memory OLTP, zone redundant | $0.8025/vCore-hr | Mission critical |

**Free tier:** 100,000 vCore-seconds/month serverless (General Purpose), 32 GB storage (12 months)

**Elastic Pools:** Share resources across multiple databases. Save 40-60% vs individual databases.

---

### 3D. Azure Database for PostgreSQL (Flexible Server)

Managed PostgreSQL with pgvector support for AI workloads.

| Tier | vCPU | RAM | Storage | Monthly Cost |
|------|------|-----|---------|-------------|
| **Burstable B1ms** | 1 | 2 GB | 32 GB | ~$25 |
| **Burstable B2s** | 2 | 4 GB | 32 GB | ~$50 |
| **General Purpose D2s v3** | 2 | 8 GB | 128 GB | ~$141 |
| **General Purpose D4s v3** | 4 | 16 GB | 256 GB | ~$282 |
| **Memory Optimized E2s v3** | 2 | 16 GB | 128 GB | ~$173 |
| **Memory Optimized E4s v3** | 4 | 32 GB | 256 GB | ~$346 |

**Storage:** $0.115/GB/month (Premium SSD), $0.05/GB/month (Standard SSD)

**pgvector:** Fully supported. Enable with `CREATE EXTENSION vector;`. Indexes: IVFFlat, HNSW. Up to 16,000 dimensions (HNSW supports up to 2,000).

**Key features:**
- High availability (zone-redundant)
- Read replicas (up to 5)
- Point-in-time restore (up to 35 days)
- Intelligent performance tuning
- Azure AD authentication
- Private Link support

#### vs AWS RDS PostgreSQL vs Cloud SQL

| Feature | Azure Flexible | AWS RDS | Cloud SQL |
|---------|---------------|---------|-----------|
| 2 vCPU / 8 GB | ~$141/month | ~$141/month | ~$116/month |
| pgvector | Yes | Yes | Yes |
| Max dimensions (HNSW) | 2,000 | 2,000 | 2,000 |
| HA (multi-AZ) | Included in price | 2x cost | 2x cost |
| Free tier | Burstable B1ms, 750 hrs (12 months) | db.t3.micro, 750 hrs (12 months) | None |

**Azure wins on HA pricing** (included, not double the cost).

---

### 3E. Azure Cache for Redis

Managed Redis for caching, session store, rate limiting.

| Tier | Size | Monthly Cost | Features |
|------|------|-------------|----------|
| **Basic C0** | 250 MB | ~$16 | No SLA, no replication |
| **Basic C1** | 1 GB | ~$34 | No SLA |
| **Standard C0** | 250 MB | ~$40 | Replication, 99.9% SLA |
| **Standard C1** | 1 GB | ~$68 | Replication |
| **Premium P1** | 6 GB | ~$210 | Clustering, persistence, VNet |
| **Enterprise E10** | 12 GB | ~$673 | Redis modules (JSON, Search, TimeSeries) |

#### vs AWS ElastiCache vs GCP Memorystore

| Feature | Azure Cache for Redis | AWS ElastiCache | GCP Memorystore |
|---------|----------------------|-----------------|-----------------|
| Smallest (250 MB) | ~$16/month | ~$12/month | ~$35/month |
| 1 GB Standard | ~$68/month | ~$48/month | ~$70/month |
| Redis Search/JSON | Enterprise tier only | None | None |
| Free tier | None | None | None |

**AWS is cheapest for Redis. Azure is most feature-rich at Enterprise tier.**

---

### 3F. Azure Table Storage

Simple, cheap key-value NoSQL storage.

| Metric | Price |
|--------|-------|
| Storage | $0.045/GB/month (LRS) |
| Transactions | $0.00036/10K |

**vs DynamoDB:** Table Storage is much cheaper for simple key-value, but DynamoDB has secondary indexes, streams, and better query capabilities. Table Storage is limited to PartitionKey + RowKey lookups.

---

### 3G. Azure Data Lake Storage Gen2

Blob Storage with hierarchical namespace for big data analytics. Optimized for Hadoop, Spark, Databricks workloads.

| Tier | Storage/GB | Read ops/10K | Write ops/10K |
|------|-----------|-------------|--------------|
| Hot | $0.021 | $0.004 | $0.065 |
| Cool | $0.012 | $0.01 | $0.13 |
| Cold | $0.0045 | $0.01 | $0.22 |
| Archive | $0.00099 | $5.50 | $0.13 |

**Key difference from Blob Storage:** Hierarchical namespace enables POSIX-like directory operations (rename, delete directory in O(1) vs O(n)). Required for efficient Spark/Databricks workloads.

---

## 4. Networking & CDN

### 4A. Azure CDN

**Note:** Azure CDN Standard from Microsoft (classic) is retiring October 2025. Migrate to Azure Front Door.

Microsoft, Akamai, and Verizon profiles are available:

| Profile | Base Cost | Data Transfer |
|---------|----------|--------------|
| Microsoft Standard | $0 | $0.081/GB (first 10 TB, North America) |
| Verizon Standard | $0 | $0.081/GB |
| Akamai Standard | $0 | $0.081/GB |
| Verizon Premium | $0 | $0.081/GB + rules engine |

**Recommendation:** Use Azure Front Door instead of CDN for new projects (same pricing, more features).

---

### 4B. Azure Front Door

Global load balancer + CDN + WAF. The recommended edge service.

| Tier | Base Fee/month | Data Transfer (NA/EU) | WAF Requests |
|------|---------------|----------------------|-------------|
| **Standard** | ~$35 | $0.08/GB | $0.60/M custom rules |
| **Premium** | ~$300 | $0.08/GB | Included, plus Bot Manager |

**Key Features:**
- Global HTTP load balancing (anycast)
- SSL offloading with managed certificates
- URL rewrite and redirect rules
- Caching (CDN functionality built-in)
- WAF with managed rule sets (OWASP, bot protection)
- Private Link origin support
- Real-time analytics

---

### 4C. Azure DNS

| Resource | Price |
|----------|-------|
| Hosted zone | $0.50/month per zone |
| DNS queries | $0.40/M queries (first 1B) |
| Private DNS zone | $0.25/month per zone |

---

### 4D. Azure Application Gateway

Regional L7 load balancer with WAF.

| SKU | Base Cost | Capacity Units |
|-----|----------|---------------|
| **Standard v2** | $0.246/hr (~$180/month) | $0.008/CU-hr |
| **WAF v2** | $0.443/hr (~$323/month) | $0.0144/CU-hr |

**Use Application Gateway for:** Regional workloads, AKS ingress, WebSocket support.
**Use Front Door for:** Global workloads, multi-region, CDN.

---

### 4E. Virtual Network (VNet)

**VNet itself:** Free
**Subnets:** Free
**Network Security Groups (NSGs):** Free
**Private Endpoints:** $0.01/hr (~$7.30/month) per endpoint + $0.01/GB data processed

**VNet Peering:**
- Same region: $0.01/GB
- Cross-region: $0.035/GB

---

## 5. Serverless & Event-Driven

### 5A. Azure Service Bus

Enterprise messaging with queues and pub/sub topics.

| Tier | Base Cost | Messages | Features |
|------|----------|----------|----------|
| **Basic** | $0.05/M messages | Up to 256 KB | Queues only |
| **Standard** | $9.81/month + $0.80/M | Up to 256 KB | Queues + Topics + Sessions |
| **Premium (1 MU)** | ~$668/month | Up to 100 MB | Dedicated, VNet, BYOK |

#### vs AWS SQS vs GCP Pub/Sub

| Feature | Service Bus (Standard) | AWS SQS | GCP Pub/Sub |
|---------|----------------------|---------|-------------|
| Base cost | $9.81/month | $0 | $0 |
| Per 1M messages | $0.80 | $0.40 | $0.40 |
| Max message size | 256 KB (std) / 100 MB (premium) | 256 KB | 10 MB |
| FIFO | Yes (sessions) | Yes ($0.50/M) | Yes (ordering key) |
| Dead letter queue | Yes | Yes | Yes |
| Topics (pub/sub) | Yes (Standard+) | SNS ($0.50/M) | Native |

**SQS is cheapest. Pub/Sub is most flexible. Service Bus has best enterprise features (sessions, transactions, scheduled delivery).**

---

### 5B. Azure Event Grid

Reactive event routing (serverless pub/sub for Azure events).

| Resource | Price |
|----------|-------|
| Operations | $0.60/M operations |
| Advanced filtering | $0.30/M |
| Dead-lettering | $0.60/M |

**Free:** First 100,000 operations/month.

**Use case:** React to Azure events (blob created, resource modified, IoT Hub messages) and route to Functions, Logic Apps, webhooks. Think of it as CloudEvents for Azure.

---

### 5C. Azure Event Hubs

High-throughput event streaming (Kafka-compatible).

| Tier | Base Cost | Throughput | Features |
|------|----------|-----------|----------|
| **Basic** | $0.015/hr per TU | 1 MB/s ingress, 2 MB/s egress per TU | 1 consumer group, 1 day retention |
| **Standard** | $0.030/hr per TU | Same | 20 consumer groups, 7 day retention |
| **Premium** | $0.900/hr per PU | 10 MB/s per PU | Dedicated, VNet, BYOK |
| **Dedicated** | ~$5,846/month per CU | 20 MB/s per CU | Single-tenant |

**1 Throughput Unit (TU):** 1 MB/s ingress, 2 MB/s egress, 84 GB storage.
**1 Processing Unit (PU):** ~10 MB/s ingress, 20 MB/s egress.

**Kafka protocol:** Standard tier and above support Kafka protocol. Use Event Hubs as a Kafka broker without managing Kafka clusters.

#### AWS Equivalent: Amazon Kinesis Data Streams
#### GCP Equivalent: Cloud Pub/Sub (streaming mode)

---

### 5D. Azure Queue Storage

Simple, cheap queuing for decoupling components.

| Resource | Price |
|----------|-------|
| Storage | $0.045/GB/month (LRS) |
| Operations | $0.004/10K |

**vs Service Bus:** Queue Storage is 10-50x cheaper but lacks advanced features (ordering, sessions, dead-letter, transactions). Use for simple fire-and-forget messaging.

---

### 5E. Azure Logic Apps

Low-code workflow orchestration with 400+ connectors.

| Plan | Pricing | Best For |
|------|---------|----------|
| **Consumption** | $0.000025/action (built-in), $0.000125/action (standard connector), $0.001/action (enterprise connector) | Simple workflows, low volume |
| **Standard** | ~$151/month (WS1: 1 vCPU, 3.5 GB) | High volume, VNet, stateful |

**Free allowance:** First 4,000 built-in actions/month (Consumption).

**Key connectors:** Office 365, SharePoint, Salesforce, SAP, Oracle, HTTP, SQL, Cosmos DB, Service Bus, Event Grid, custom APIs.

**vs AWS Step Functions:** Logic Apps has 400+ connectors out of the box. Step Functions has better integration with AWS services but fewer third-party connectors.

---

### 5F. Azure Durable Functions

Covered in Section 2C (Azure Functions). Stateful function orchestrations for:
- Long-running workflows
- Fan-out/fan-in patterns
- Human-in-the-loop approvals
- Saga pattern (distributed transactions)

No additional cost beyond the Functions hosting plan.

---

## 6. Security & IAM

### 6A. Azure AD / Microsoft Entra ID

Azure's identity platform. Handles authentication, authorization, and identity management.

| Plan | Monthly Cost | Key Features |
|------|-------------|-------------|
| **Free** | $0 | SSO (unlimited apps), MFA, basic RBAC |
| **P1** | $6/user/month | Conditional Access, dynamic groups, self-service password reset |
| **P2** | $9/user/month | Identity Protection, Privileged Identity Management, access reviews |

**Managed Identities (Free):**
- System-assigned: Auto-created with a resource, deleted with it
- User-assigned: Created independently, attached to multiple resources
- **No credentials to manage** -- Azure handles token rotation automatically
- Works with Azure OpenAI, Key Vault, Blob Storage, Cosmos DB, SQL, etc.

**RBAC (Role-Based Access Control):**
- **Free** -- no additional cost for role assignments
- Built-in roles: Owner, Contributor, Reader, + 500+ service-specific roles
- Custom roles: Define your own permissions
- Scope: Management group, subscription, resource group, or individual resource

```bash
# Assign role to managed identity
az role assignment create \
  --role "Cognitive Services OpenAI User" \
  --assignee <managed-identity-object-id> \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<openai-resource>
```

**Best practice for AI projects:** Always use managed identities instead of API keys. Eliminates secret management entirely.

---

### 6B. Azure Key Vault

Centralized secret, key, and certificate management.

| Operation | Standard | Premium (HSM) |
|-----------|----------|---------------|
| Secrets operations | $0.03/10K | $0.03/10K |
| Key operations (RSA 2048) | $0.03/10K | $1.00/10K |
| Key operations (RSA 3072/4096) | $0.15/10K | $5.00/10K |
| Certificate renewal | $3.00/renewal | $3.00/renewal |
| Storage | Included (up to 25 MB per vault) | Included |

**Free tier:** 10,000 operations/month for RSA 2048-bit keys and secrets (Standard vault).

**Key features:**
- Soft-delete (90-day recovery by default)
- Purge protection (prevent permanent deletion)
- RBAC integration (no more access policies needed)
- Private Link support
- Diagnostic logging
- Automatic key rotation

```bash
# Store a secret
az keyvault secret set --vault-name myVault --name "OpenAI-Key" --value "sk-..."

# Retrieve a secret
az keyvault secret show --vault-name myVault --name "OpenAI-Key" --query value -o tsv
```

#### AWS Equivalent: AWS Secrets Manager ($0.40/secret/month) + KMS ($1/key/month)
#### GCP Equivalent: Secret Manager ($0.06/10K access operations)

**Azure is cheapest for secrets management.** $0.03/10K operations vs $0.05/10K (AWS) vs $0.06/10K (GCP).

---

### 6C. Microsoft Defender for Cloud

Cloud Security Posture Management (CSPM) and threat protection.

| Plan | Cost |
|------|------|
| **Free (Foundational CSPM)** | $0 -- security recommendations, Secure Score |
| **Defender for Servers P1** | $5/server/month |
| **Defender for Servers P2** | $15/server/month |
| **Defender for Containers** | $7/vCore/month |
| **Defender for App Service** | $15/instance/month |
| **Defender for Storage** | $10/storage account/month |
| **Defender for Key Vault** | $0.02/10K transactions |
| **Defender for AI** | Per-resource pricing |

---

### 6D. Azure Private Link

Connect to PaaS services (Azure OpenAI, Cosmos DB, Storage, SQL) over private IP in your VNet.

| Resource | Cost |
|----------|------|
| Private Endpoint | $0.01/hr (~$7.30/month) |
| Data processed | $0.01/GB (inbound + outbound) |

**Critical for AI projects:** Use Private Link to ensure Azure OpenAI traffic never traverses the public internet. Required for many compliance scenarios (HIPAA, PCI-DSS, SOC 2).

---

## 7. CI/CD & DevOps

### 7A. Azure DevOps

| Service | Free Tier | Paid |
|---------|----------|------|
| **Repos** | Unlimited private repos, 5 users | $6/user/month (6th user+) |
| **Pipelines** | 1 parallel job, 1,800 min/month (Microsoft-hosted) | $40/parallel job/month |
| **Boards** | Full access, 5 users | $6/user/month |
| **Artifacts** | 2 GB storage | $2/GB/month |
| **Test Plans** | N/A | $52/user/month |

**Self-hosted agents:** Free unlimited parallel jobs on your own hardware.

---

### 7B. GitHub Actions (Azure Integration)

| Resource | Free (public repos) | Free (private repos) | Paid |
|----------|-------------------|---------------------|------|
| Minutes/month | Unlimited | 2,000 | $0.008/min (Linux) |
| Storage | 500 MB | 500 MB | $0.25/GB/month |

**Azure-specific Actions:**
- `azure/login` -- Authenticate with OIDC (no secrets needed)
- `azure/webapps-deploy` -- Deploy to App Service
- `azure/container-apps-deploy-action` -- Deploy to Container Apps
- `azure/docker-login` -- Login to ACR

---

### 7C. Azure Container Registry (ACR)

| Tier | Monthly Cost | Storage | Webhooks | Geo-Replication |
|------|-------------|---------|----------|----------------|
| **Basic** | ~$5 | 10 GB | 2 | No |
| **Standard** | ~$20 | 100 GB | 10 | No |
| **Premium** | ~$50 | 500 GB | 500 | Yes (multi-region) |

**Additional storage:** $0.003/GB/day (~$0.09/GB/month) beyond included amount.

#### vs AWS ECR vs GCP Artifact Registry

| Feature | Azure ACR (Standard) | AWS ECR | GCP Artifact Registry |
|---------|---------------------|---------|----------------------|
| Monthly base | ~$20 | $0 | $0 |
| Storage/GB | $0.09 | $0.10 | $0.10 |
| Free tier | None | 500 MB (12 months) | 500 MB (always) |
| Geo-replication | Premium only | Manual | Multi-region native |

---

## 8. Monitoring & Observability

### 8A. Azure Monitor

Unified monitoring platform for metrics, logs, and alerts.

| Component | Pricing |
|-----------|---------|
| **Platform metrics** | Free (1-minute granularity, 93-day retention) |
| **Custom metrics** | $0.258/metric time series/month (first 150K free) |
| **Log ingestion (Analytics)** | $2.30/GB (first 5 GB/month free) |
| **Log ingestion (Basic)** | $0.65/GB |
| **Log ingestion (Auxiliary)** | $0.05/GB |
| **Log retention** | Free for 30 days (Analytics), then $0.10/GB/month |
| **Archive** | $0.02/GB/month |
| **Log queries (Basic)** | $0.007/GB scanned |

#### Log Data Plans

| Plan | Ingestion | Query | Retention | Use Case |
|------|-----------|-------|-----------|----------|
| **Analytics** | $2.30/GB | Full KQL, free | 30 days free, up to 2 years | Active investigation, dashboards |
| **Basic** | $0.65/GB | Limited KQL, $0.007/GB | 8 days free, up to 30 days | High-volume, infrequent access |
| **Auxiliary** | $0.05/GB | Very limited | 30 days free, up to 1 year | Compliance, audit logs |

---

### 8B. Application Insights

APM (Application Performance Monitoring) built on Azure Monitor.

| Resource | Price |
|----------|-------|
| **Data ingestion** | $2.30/GB (first 5 GB/month free, shared with Monitor) |
| **Multi-step web tests** | $10/test/month |
| **Ping web tests** | Free (up to 10 per resource) |

**Key Features:**
- Distributed tracing (end-to-end request tracking)
- Live Metrics (real-time telemetry stream)
- Application Map (dependency visualization)
- Smart Detection (ML-based anomaly alerts)
- Custom events and metrics
- OpenTelemetry SDK support
- Snapshot Debugger (production debugging)

**Auto-instrumentation:** Zero-code monitoring for .NET, Java, Node.js, Python. Just add the SDK or enable via portal.

```python
# Python: Add Application Insights
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor(connection_string="InstrumentationKey=...")
```

---

### 8C. Log Analytics (KQL)

Query language for Azure Monitor Logs. Similar to SQL but optimized for log analytics.

```kql
// Find slow API calls in the last hour
requests
| where timestamp > ago(1h)
| where duration > 2000  // > 2 seconds
| summarize avg(duration), count() by name
| order by avg_duration desc
| take 10
```

**Retention:** 30 days free (interactive), then $0.10/GB/month. Up to 12 years with archive tier.

---

### 8D. Azure Alerts

| Alert Type | Price |
|-----------|-------|
| **Metric alerts** | $0.10/metric signal/month |
| **Log alerts** | $0.25-$1.50/log signal/month (depending on frequency) |
| **Activity log alerts** | Free |
| **Smart Detector alerts** | Free (Application Insights) |

**Action Groups:** Email, SMS ($0.01/SMS), voice call ($0.15/call), webhook, Logic App, Azure Function, ITSM connector.

---

## 9. Free Tier (Complete List)

### Always Free (No Expiration)

| Service | Free Allowance |
|---------|---------------|
| **Azure Functions** | 1M executions + 400K GB-seconds/month |
| **Azure Container Apps** | 180K vCPU-sec + 360K GiB-sec + 2M requests/month |
| **Azure Cosmos DB** | 1,000 RU/s + 25 GB (provisioned, one account) |
| **Azure AI Services** | See below per-service breakdown |
| **Azure DevOps** | 5 users + 1 parallel pipeline + 2 GB Artifacts |
| **Azure Monitor** | 5 GB log ingestion/month, 150K custom metrics |
| **Application Insights** | 5 GB/month (shared with Monitor) |
| **Event Grid** | 100K operations/month |
| **Azure Active Directory** | SSO, MFA, basic RBAC (free tier) |
| **Azure Key Vault** | 10K operations/month (RSA 2048 keys, secrets) |
| **Managed Identities** | Unlimited (always free) |
| **RBAC** | Unlimited role assignments (always free) |
| **VNet** | Unlimited VNets, subnets, NSGs (always free) |
| **Azure DNS** | Not free ($0.50/zone) |
| **Azure Advisor** | Free recommendations |
| **Microsoft Defender (Foundational CSPM)** | Free security posture |

### AI Services Free Tier

| AI Service | Monthly Free Allowance |
|-----------|----------------------|
| **Azure OpenAI** | No free tier (pay-per-token from first use) |
| **AI Search** | 1 free index, 50 MB, no SLA, no semantic ranker |
| **Document Intelligence** | 500 pages/month |
| **Speech-to-Text** | 5 hours/month |
| **Text-to-Speech** | 0.5M characters/month |
| **Computer Vision** | 5,000 transactions/month |
| **Language (NER, Sentiment, etc.)** | 5,000 text records/month |
| **Content Safety** | 1,000 text records + 1,000 images/month |
| **Translator** | 2M characters/month |

### 12-Month Free (New Account)

| Service | 12-Month Free Allowance |
|---------|------------------------|
| **Virtual Machines** | 750 hrs B1s (Linux), 750 hrs B1s (Windows) |
| **Blob Storage** | 5 GB LRS Hot |
| **Azure SQL Database** | 100K vCore-seconds/month (serverless, 32 GB) |
| **Azure PostgreSQL** | 750 hrs Burstable B1ms (32 GB) |
| **Azure Cache for Redis** | Not included |
| **Managed Disks** | 2x 64 GB P6 SSD |
| **Bandwidth** | 15 GB outbound |
| **Azure Container Registry** | Not included |

### New Account Credit

- **$200 credit for 30 days** -- use on any service (except Marketplace)
- After 30 days, unused credit expires
- Free and 12-month services continue without credit

---

## 10. Pricing Comparisons vs AWS and GCP

### AI Model APIs

| Service | Azure | AWS (Bedrock) | GCP (Vertex AI) |
|---------|-------|---------------|----------------|
| GPT-4o (input/1M) | $2.50 | N/A (not on Bedrock) | N/A |
| Claude Sonnet 4 (input/1M) | N/A | $3.00 | $3.00 |
| Gemini 2.5 Pro (input/1M) | N/A | N/A | $1.25-$2.50 |
| Llama 4 Maverick (input/1M) | $0.20 (serverless) | $0.40 | $0.20 |
| Embeddings (text-embedding-3-small) | $0.02 | $0.02 (Titan) | $0.00025 (Gemini Embedding) |

**Azure advantage:** Exclusive access to OpenAI models (GPT-4o, o3, o4-mini, DALL-E) with enterprise SLAs. No other cloud offers these.

**GCP advantage:** Gemini models are significantly cheaper for many tasks. Gemini Embedding 2 is 80x cheaper than text-embedding-3-small.

### Compute (Serverless Containers)

| Metric | Azure Container Apps | AWS Fargate | GCP Cloud Run |
|--------|---------------------|-------------|---------------|
| vCPU/second | $0.000024 | $0.000011 | $0.000024 |
| Memory GB/second | $0.000003 | $0.0000012 | $0.0000025 |
| 1 vCPU, 2 GB, 100hr/month | ~$10 | ~$5 + ALB ($16) = $21 | ~$10 |
| Scale to zero | Yes | No | Yes |
| GPU (T4) | ~$1.35/hr | No (use EC2) | ~$0.95/hr |
| Free tier | 180K vCPU-sec | None | 180K vCPU-sec |

**For AI workloads:** ACA and Cloud Run are cheapest due to scale-to-zero and GPU support. Fargate requires always-on minimum.

### Databases

| Service | Azure | AWS | GCP |
|---------|-------|-----|-----|
| PostgreSQL (2 vCPU, 8 GB) | ~$141/month | ~$141/month | ~$116/month |
| Document DB (pay-per-query) | Cosmos DB $0.25/M RU | DynamoDB $1.25/M WCU | Firestore $0.36/100K writes |
| Redis (1 GB standard) | ~$68/month | ~$48/month | ~$70/month |
| Object Storage (Hot, per GB) | $0.018 | $0.023 | $0.020 |

### Hidden Costs

| Cost Type | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| **Egress (100 GB-10 TB)** | $0.087/GB | $0.09/GB | $0.12/GB |
| **Support (Business)** | $100/month min | $100/month or 10% of bill | $100/month or 4% of bill |
| **Load Balancer** | Front Door $35/month | ALB $16/month + $0.008/LCU-hr | Free (Cloud Run) |
| **Private Endpoints** | $7.30/month each | $7.30/month each | Free (Private Service Connect) |
| **Log ingestion** | $2.30/GB | $0.50/GB (CloudWatch) | $0.50/GB (Cloud Logging) |
| **API Management** | $49/month (Basic) | $3.50/M calls (API Gateway) | Free (Cloud Endpoints) |

**Biggest Azure hidden cost:** Log Analytics at $2.30/GB is 4.6x more expensive than AWS CloudWatch ($0.50/GB). Use Basic Logs ($0.65/GB) or Auxiliary Logs ($0.05/GB) for high-volume telemetry.

### Enterprise Discount Programs

| Program | Azure | AWS | GCP |
|---------|-------|-----|-----|
| **Commitment discounts** | Azure Savings Plan (1yr/3yr) | Compute Savings Plans | Committed Use Discounts |
| **Enterprise agreement** | EA (custom pricing, 1-3 year) | Enterprise Discount Program | Enterprise agreements |
| **Pay-as-you-go** | Standard rates | Standard rates | Standard rates |
| **Spot/preemptible** | Up to 90% off | Up to 90% off | Up to 91% off |
| **Reserved instances** | 1yr (30-40% off), 3yr (50-60% off) | Same ranges | Same ranges |
| **Academic/nonprofit** | Azure for Education, $200 credit | AWS Educate | GCP for Education |
| **Startup credits** | $150K (Founders Hub) | $100K (Activate) | $100K-$200K (for Startups) |

---

## 11. Architecture Patterns for AI Projects

### Pattern 1: RAG on Azure

**Components:** Container Apps + Azure OpenAI + AI Search + Blob Storage

```
User Query
    |
    v
Azure Container Apps (FastAPI)
    |
    ├── Embed query (Azure OpenAI text-embedding-3-small)
    |
    ├── Hybrid search (Azure AI Search: BM25 + vector + semantic ranker)
    |
    ├── Retrieve top-K documents
    |
    ├── Generate answer (Azure OpenAI GPT-4o)
    |
    └── Return response with citations

Document Ingestion:
    Blob Storage (PDFs, docs)
        |
        ├── Document Intelligence (Layout model - extract text + tables)
        |
        ├── Chunk (overlapping, section-aware)
        |
        ├── Embed chunks (Azure OpenAI)
        |
        └── Index in AI Search (vector + metadata)
```

**Monthly cost estimate (1,000 queries/day, 10K documents):**

| Component | Monthly Cost |
|-----------|-------------|
| Container Apps (0.5 vCPU, 1 GB, Consumption) | ~$15 |
| Azure OpenAI (GPT-4o, ~30M tokens) | ~$75 |
| Azure OpenAI (embeddings, ~5M tokens) | ~$0.10 |
| AI Search (Basic, 2 GB) | ~$74 |
| Blob Storage (10 GB Hot) | ~$1 |
| Document Intelligence (10K pages, Layout) | ~$100 |
| **Total** | **~$265/month** |

---

### Pattern 2: Enterprise AI Chatbot

**Components:** Azure OpenAI + AI Search + Cosmos DB + App Service

```
User (Teams/Web/Mobile)
    |
    v
App Service (Next.js/React frontend)
    |
    v
Azure Container Apps (API backend)
    |
    ├── Azure OpenAI (GPT-4o) -- chat completions
    |
    ├── Azure AI Search -- knowledge retrieval
    |
    ├── Cosmos DB -- chat history, user preferences, session state
    |
    ├── Azure AI Content Safety -- input/output moderation
    |
    └── Application Insights -- telemetry, usage analytics

Authentication:
    Microsoft Entra ID (SSO with Azure AD)

Security:
    Private Link (all services on private network)
    Key Vault (connection strings, not API keys -- use managed identity)
    Front Door (WAF, DDoS protection, global routing)
```

**Monthly cost estimate (enterprise, 10K users, 50K queries/day):**

| Component | Monthly Cost |
|-----------|-------------|
| App Service (P1v3) | ~$138 |
| Container Apps (2 replicas, Dedicated D4) | ~$490 |
| Azure OpenAI (GPT-4o, ~500M tokens) | ~$1,250 |
| AI Search (S1, 3 replicas for HA) | ~$735 |
| Cosmos DB (10K RU/s provisioned) | ~$584 |
| Content Safety (~1.5M requests) | ~$1,125 |
| Front Door (Standard) | ~$35 |
| Application Insights (50 GB) | ~$115 |
| Key Vault | ~$5 |
| Private Endpoints (5) | ~$37 |
| **Total** | **~$4,514/month** |

---

### Pattern 3: Document Processing Pipeline

**Components:** Document Intelligence + Azure Functions + Blob Storage + AI Search

```
Document Upload (Blob Storage)
    |
    v
Event Grid (blob created trigger)
    |
    v
Azure Functions (Durable - orchestrator)
    |
    ├── Step 1: Document Intelligence (Layout) -- extract text, tables, structure
    |
    ├── Step 2: AI Language (NER, PII detection) -- extract entities, redact PII
    |
    ├── Step 3: Azure OpenAI (summarization) -- generate summary
    |
    ├── Step 4: Azure OpenAI (embedding) -- vectorize chunks
    |
    ├── Step 5: AI Search (index) -- upsert to search index
    |
    └── Step 6: Cosmos DB (metadata) -- store document metadata, status

Monitoring:
    Application Insights -- track processing times, failures
    Azure Alerts -- alert on errors, SLA violations
```

**Monthly cost (10K documents/month, avg 5 pages each):**

| Component | Monthly Cost |
|-----------|-------------|
| Azure Functions (Consumption) | ~$2 |
| Document Intelligence (50K pages, Layout) | ~$500 |
| Azure OpenAI (embeddings + summaries) | ~$50 |
| AI Search (Basic) | ~$74 |
| Blob Storage (50 GB) | ~$1 |
| Event Grid | ~$0.60 |
| Cosmos DB (serverless) | ~$5 |
| Application Insights | ~$5 |
| **Total** | **~$638/month** |

---

### Pattern 4: Real-Time AI Agent

**Components:** Azure OpenAI + Semantic Kernel + Container Apps

```
User Request (HTTP/WebSocket)
    |
    v
Azure Container Apps (FastAPI + Semantic Kernel)
    |
    ├── Planner (Azure OpenAI GPT-4o)
    |     |
    |     ├── Plan: [search_knowledge, query_database, send_email]
    |     |
    |     v
    ├── Tool Execution
    |     ├── search_knowledge() → AI Search
    |     ├── query_database() → Cosmos DB / SQL
    |     ├── send_email() → Microsoft Graph API
    |     ├── get_calendar() → Microsoft Graph API
    |     └── custom_tool() → Any REST API
    |
    ├── Response Generation (GPT-4o with tool results)
    |
    └── Content Safety check → return response

State Management:
    Cosmos DB (conversation history, agent state)
    Azure Cache for Redis (rate limiting, session cache)
```

**Semantic Kernel** is Microsoft's open-source SDK for building AI agents (Python, C#, Java). It integrates natively with Azure OpenAI and supports:
- Function calling / tool use
- Prompt templates with variables
- Memory (chat history, semantic memory)
- Planning (auto-select tools based on user intent)
- Filters (pre/post-execution hooks for logging, safety)

---

## 12. Azure CLI Commands Reference

### Installation and Auth

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux
brew install azure-cli  # macOS

# Login
az login                          # Interactive browser login
az login --service-principal -u <app-id> -p <secret> --tenant <tenant-id>  # CI/CD
az login --identity              # Managed identity (in Azure VMs/containers)

# Set subscription
az account set --subscription <name-or-id>
az account show                  # Current subscription
az account list --output table   # All subscriptions
```

### Resource Group Management

```bash
# Create resource group
az group create --name myRG --location eastus

# List resource groups
az group list --output table

# Delete resource group (and ALL resources in it)
az group delete --name myRG --yes --no-wait
```

### Azure OpenAI (Cognitive Services)

```bash
# Create Azure OpenAI resource
az cognitiveservices account create \
  --name myOpenAI \
  --resource-group myRG \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Deploy a model
az cognitiveservices account deployment create \
  --name myOpenAI \
  --resource-group myRG \
  --deployment-name gpt4o \
  --model-name gpt-4o \
  --model-version "2024-11-20" \
  --model-format OpenAI \
  --sku-capacity 30 \
  --sku-name GlobalStandard

# List deployments
az cognitiveservices account deployment list \
  --name myOpenAI \
  --resource-group myRG \
  --output table

# Get keys
az cognitiveservices account keys list \
  --name myOpenAI \
  --resource-group myRG

# Get endpoint
az cognitiveservices account show \
  --name myOpenAI \
  --resource-group myRG \
  --query properties.endpoint
```

### Container Apps

```bash
# Install extension
az extension add --name containerapp

# Create environment
az containerapp env create \
  --name myEnv \
  --resource-group myRG \
  --location eastus

# Deploy from image
az containerapp create \
  --name myapp \
  --resource-group myRG \
  --environment myEnv \
  --image myregistry.azurecr.io/myapp:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 --memory 1.0Gi \
  --min-replicas 0 \
  --max-replicas 10

# Deploy from source (auto-build)
az containerapp up \
  --name myapp \
  --resource-group myRG \
  --environment myEnv \
  --source . \
  --ingress external \
  --target-port 8000

# Update with new image
az containerapp update \
  --name myapp \
  --resource-group myRG \
  --image myregistry.azurecr.io/myapp:v2

# Scale settings
az containerapp update \
  --name myapp \
  --resource-group myRG \
  --min-replicas 1 \
  --max-replicas 20

# View logs
az containerapp logs show \
  --name myapp \
  --resource-group myRG \
  --follow

# Set secrets
az containerapp secret set \
  --name myapp \
  --resource-group myRG \
  --secrets "openai-key=<value>"

# Set environment variables (reference secret)
az containerapp update \
  --name myapp \
  --resource-group myRG \
  --set-env-vars "OPENAI_API_KEY=secretref:openai-key"

# Create a job (cron)
az containerapp job create \
  --name myjob \
  --resource-group myRG \
  --environment myEnv \
  --image myregistry.azurecr.io/myjob:latest \
  --trigger-type Cron \
  --cron-expression "0 */6 * * *" \
  --cpu 1.0 --memory 2.0Gi
```

### Blob Storage

```bash
# Create storage account
az storage account create \
  --name mystorageacct \
  --resource-group myRG \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --account-name mystorageacct \
  --name documents

# Upload file
az storage blob upload \
  --account-name mystorageacct \
  --container-name documents \
  --file ./report.pdf \
  --name reports/2026/report.pdf

# Upload directory
az storage blob upload-batch \
  --account-name mystorageacct \
  --destination documents \
  --source ./data/

# Download file
az storage blob download \
  --account-name mystorageacct \
  --container-name documents \
  --name reports/2026/report.pdf \
  --file ./downloaded.pdf

# List blobs
az storage blob list \
  --account-name mystorageacct \
  --container-name documents \
  --output table

# Generate SAS URL (1 hour expiry)
az storage blob generate-sas \
  --account-name mystorageacct \
  --container-name documents \
  --name report.pdf \
  --permissions r \
  --expiry $(date -u -d '+1 hour' +%Y-%m-%dT%H:%MZ) \
  --full-uri

# Set tier
az storage blob set-tier \
  --account-name mystorageacct \
  --container-name documents \
  --name old-report.pdf \
  --tier Cool
```

### Azure AI Search

```bash
# Create search service
az search service create \
  --name mysearch \
  --resource-group myRG \
  --sku Basic \
  --location eastus

# Get admin key
az search admin-key show \
  --service-name mysearch \
  --resource-group myRG

# Get query key
az search query-key list \
  --service-name mysearch \
  --resource-group myRG
```

### Key Vault

```bash
# Create vault
az keyvault create \
  --name myVault \
  --resource-group myRG \
  --location eastus

# Set secret
az keyvault secret set \
  --vault-name myVault \
  --name "DatabasePassword" \
  --value "supersecret123"

# Get secret
az keyvault secret show \
  --vault-name myVault \
  --name "DatabasePassword" \
  --query value -o tsv

# List secrets
az keyvault secret list \
  --vault-name myVault \
  --output table

# Grant access to managed identity
az keyvault set-policy \
  --name myVault \
  --object-id <managed-identity-object-id> \
  --secret-permissions get list
```

### Azure Container Registry

```bash
# Create registry
az acr create \
  --name myregistry \
  --resource-group myRG \
  --sku Standard

# Login to registry
az acr login --name myregistry

# Build image in cloud
az acr build \
  --registry myregistry \
  --image myapp:v1 \
  --file Dockerfile .

# List images
az acr repository list --name myregistry --output table

# Show tags
az acr repository show-tags --name myregistry --repository myapp
```

### Azure Functions

```bash
# Create function app
az functionapp create \
  --name myfuncapp \
  --resource-group myRG \
  --storage-account mystorageacct \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11

# Deploy
func azure functionapp publish myfuncapp

# List functions
az functionapp function list \
  --name myfuncapp \
  --resource-group myRG \
  --output table
```

### Cosmos DB

```bash
# Create Cosmos DB account (NoSQL)
az cosmosdb create \
  --name mycosmosdb \
  --resource-group myRG \
  --kind GlobalDocumentDB \
  --enable-free-tier true

# Create database
az cosmosdb sql database create \
  --account-name mycosmosdb \
  --resource-group myRG \
  --name mydb

# Create container with vector policy
az cosmosdb sql container create \
  --account-name mycosmosdb \
  --resource-group myRG \
  --database-name mydb \
  --name items \
  --partition-key-path /partitionKey \
  --throughput 400

# Get connection string
az cosmosdb keys list \
  --name mycosmosdb \
  --resource-group myRG \
  --type connection-strings
```

---

## 13. When to Choose Azure Over AWS/GCP

### Decision Matrix

| Criterion | Choose Azure | Choose AWS | Choose GCP |
|-----------|-------------|-----------|-----------|
| **Need OpenAI models with enterprise SLA** | YES | No (not available) | No (not available) |
| **Microsoft 365 / Teams integration** | YES | No | No |
| **Enterprise (Fortune 500)** | YES (strongest EA) | Strong | Growing |
| **Hybrid cloud (on-prem + cloud)** | YES (Azure Arc, Stack) | Outposts | Anthos |
| **.NET / C# ecosystem** | YES | Supported | Supported |
| **Government / regulated industries** | YES (Azure Gov) | AWS GovCloud | GCP FedRAMP |
| **Best raw AI/ML tooling** | Strong | Strong (SageMaker) | YES (Vertex AI, TPUs) |
| **Cheapest compute** | Sometimes | Usually | Often |
| **Most services (breadth)** | ~200 | ~250 | ~150 |
| **Best Kubernetes** | AKS (free plane) | EKS ($73/mo) | GKE Autopilot (best) |
| **Best serverless containers** | Good (ACA) | Fargate (mature) | YES (Cloud Run) |
| **Largest free tier** | Good | Good | Best (Always Free is generous) |
| **Best for startups** | $150K credits | $100K credits | $100-200K credits |
| **Vector database (native)** | Cosmos DB DiskANN | OpenSearch | AlloyDB, Spanner |
| **Best document AI** | YES (Doc Intelligence) | Textract (close) | Document AI (close) |

### Azure Strengths

1. **Azure OpenAI (exclusive):** Only cloud with GPT-4o, GPT-4.1, o3, o4-mini, DALL-E under enterprise SLA. This alone drives many enterprise AI projects to Azure.

2. **Enterprise ecosystem:** Deep integration with Microsoft 365, Teams, Power Platform, Dynamics 365, Copilot Studio. If a company runs on Microsoft, Azure is the natural cloud.

3. **Hybrid cloud:** Azure Arc (manage on-prem, multi-cloud from Azure), Azure Stack HCI/Hub (run Azure services on-prem). Best hybrid story among the three clouds.

4. **Compliance:** 100+ compliance certifications. Azure Government (IL5, IL6), Azure China (21Vianet). Critical for defense, healthcare, finance.

5. **AI Search:** Best managed search service for RAG (native hybrid search + semantic ranker + integrated vectorization). No equivalent on AWS or GCP.

6. **Cosmos DB:** Only globally distributed NoSQL with 5 consistency levels + DiskANN vector search + multi-model (document, graph, key-value) in one service.

7. **Semantic Kernel:** Microsoft's open-source agent framework (Python, C#, Java) with deep Azure integration. Growing ecosystem.

### Azure Weaknesses

1. **Complex pricing:** More confusing than AWS or GCP. Multiple pricing models per service, unclear cost calculators, surprising egress charges.

2. **Portal UX:** Azure Portal is slower and more complex than AWS Console or GCP Console. Frequent layout changes.

3. **Naming conventions:** Microsoft renames services frequently (Cognitive Search -> AI Search, Form Recognizer -> Document Intelligence, Azure AD -> Entra ID, AI Studio -> AI Foundry). Documentation often references old names.

4. **Log Analytics cost:** $2.30/GB is 4.6x AWS CloudWatch ($0.50/GB). Major hidden cost for observability-heavy workloads.

5. **Service Bus pricing:** 2x more expensive than SQS for equivalent messaging workloads.

6. **Container ecosystem maturity:** Container Apps is newer than Cloud Run and Fargate. Fewer community tutorials, Stack Overflow answers.

7. **Global availability:** Some AI services are limited to specific regions (Azure OpenAI not available in all regions). AWS has broader region coverage.

8. **Open-source community:** GCP has stronger open-source ties (Kubernetes, TensorFlow, JAX). Azure leans proprietary.

---

## 14. Quick Start Templates

### Template 1: Deploy FastAPI to Azure Container Apps

```bash
#!/bin/bash
# deploy-fastapi.sh

RG="ai-project-rg"
LOCATION="eastus"
ENV_NAME="ai-env"
APP_NAME="my-api"
ACR_NAME="myairegistry"

# 1. Create resource group
az group create --name $RG --location $LOCATION

# 2. Create container registry
az acr create --name $ACR_NAME --resource-group $RG --sku Basic
az acr login --name $ACR_NAME

# 3. Build and push image
az acr build --registry $ACR_NAME --image $APP_NAME:v1 --file Dockerfile .

# 4. Create Container Apps environment
az containerapp env create --name $ENV_NAME --resource-group $RG --location $LOCATION

# 5. Deploy
az containerapp create \
  --name $APP_NAME \
  --resource-group $RG \
  --environment $ENV_NAME \
  --image $ACR_NAME.azurecr.io/$APP_NAME:v1 \
  --registry-server $ACR_NAME.azurecr.io \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 --memory 1.0Gi \
  --min-replicas 0 \
  --max-replicas 10

# 6. Get URL
az containerapp show --name $APP_NAME --resource-group $RG \
  --query properties.configuration.ingress.fqdn -o tsv
```

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

---

### Template 2: Azure OpenAI + AI Search RAG Setup

```bash
#!/bin/bash
# setup-rag.sh

RG="rag-rg"
LOCATION="eastus"
OPENAI_NAME="my-openai"
SEARCH_NAME="my-search"
STORAGE_NAME="myragstorage"

# 1. Create OpenAI resource + deploy models
az cognitiveservices account create \
  --name $OPENAI_NAME --resource-group $RG \
  --kind OpenAI --sku S0 --location $LOCATION

az cognitiveservices account deployment create \
  --name $OPENAI_NAME --resource-group $RG \
  --deployment-name gpt4o \
  --model-name gpt-4o --model-version "2024-11-20" \
  --model-format OpenAI --sku-capacity 30 --sku-name GlobalStandard

az cognitiveservices account deployment create \
  --name $OPENAI_NAME --resource-group $RG \
  --deployment-name embedding \
  --model-name text-embedding-3-small --model-version "1" \
  --model-format OpenAI --sku-capacity 120 --sku-name GlobalStandard

# 2. Create AI Search
az search service create \
  --name $SEARCH_NAME --resource-group $RG \
  --sku Basic --location $LOCATION

# 3. Create Storage for documents
az storage account create \
  --name $STORAGE_NAME --resource-group $RG \
  --location $LOCATION --sku Standard_LRS

az storage container create \
  --account-name $STORAGE_NAME --name documents
```

**Python RAG Code:**

```python
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

# Use managed identity (no API keys)
credential = DefaultAzureCredential()

# Azure OpenAI client
openai_client = AzureOpenAI(
    azure_endpoint="https://my-openai.openai.azure.com/",
    azure_ad_token_provider=credential.get_token("https://cognitiveservices.azure.com/.default").token,
    api_version="2024-10-21"
)

# AI Search client
search_client = SearchClient(
    endpoint="https://my-search.search.windows.net",
    index_name="documents",
    credential=credential
)

def rag_query(user_question: str) -> str:
    # 1. Embed the query
    embedding = openai_client.embeddings.create(
        model="embedding",
        input=user_question
    ).data[0].embedding

    # 2. Hybrid search (vector + keyword)
    results = search_client.search(
        search_text=user_question,
        vector_queries=[{
            "vector": embedding,
            "k_nearest_neighbors": 5,
            "fields": "contentVector"
        }],
        query_type="semantic",
        semantic_configuration_name="my-semantic-config",
        top=5
    )

    # 3. Build context from results
    context = "\n\n".join([
        f"[{r['title']}]: {r['content']}"
        for r in results
    ])

    # 4. Generate answer
    response = openai_client.chat.completions.create(
        model="gpt4o",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n{context}"},
            {"role": "user", "content": user_question}
        ]
    )

    return response.choices[0].message.content
```

---

### Template 3: Blob Storage + SAS Tokens Pattern

```python
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
    ContentSettings
)
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import os

# Connect with managed identity
credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageacct.blob.core.windows.net",
    credential=credential
)

# Upload a file
def upload_document(file_path: str, container: str = "documents") -> str:
    blob_name = f"uploads/{datetime.utcnow().strftime('%Y/%m/%d')}/{os.path.basename(file_path)}"
    blob_client = blob_service.get_blob_client(container, blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(
            data,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/pdf")
        )
    return blob_name

# Generate SAS URL for download (1-hour expiry)
def get_download_url(blob_name: str, container: str = "documents") -> str:
    # Note: For SAS, you need the account key (not managed identity)
    account_key = os.getenv("STORAGE_ACCOUNT_KEY")

    sas_token = generate_blob_sas(
        account_name="mystorageacct",
        container_name=container,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return f"https://mystorageacct.blob.core.windows.net/{container}/{blob_name}?{sas_token}"

# Alternative: Use User Delegation SAS (no account key needed)
def get_download_url_delegated(blob_name: str, container: str = "documents") -> str:
    delegation_key = blob_service.get_user_delegation_key(
        key_start_time=datetime.utcnow(),
        key_expiry_time=datetime.utcnow() + timedelta(hours=2)
    )

    sas_token = generate_blob_sas(
        account_name="mystorageacct",
        container_name=container,
        blob_name=blob_name,
        user_delegation_key=delegation_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return f"https://mystorageacct.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
```

---

### Template 4: Cosmos DB CRUD with Vector Search

```python
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid

# Connect with managed identity
credential = DefaultAzureCredential()
client = CosmosClient(
    url="https://mycosmosdb.documents.azure.com:443/",
    credential=credential
)

db = client.get_database_client("mydb")
container = db.get_container_client("items")

# Create item
def create_item(content: str, embedding: list[float], metadata: dict) -> dict:
    item = {
        "id": str(uuid.uuid4()),
        "partitionKey": "default",
        "content": content,
        "embedding": embedding,
        "metadata": metadata,
        "createdAt": datetime.utcnow().isoformat()
    }
    return container.create_item(item)

# Read item by ID
def get_item(item_id: str) -> dict:
    return container.read_item(item=item_id, partition_key="default")

# Update item
def update_item(item_id: str, updates: dict) -> dict:
    item = get_item(item_id)
    item.update(updates)
    return container.replace_item(item=item_id, body=item)

# Delete item
def delete_item(item_id: str):
    container.delete_item(item=item_id, partition_key="default")

# Vector search (requires vector index policy on container)
def vector_search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    query = """
    SELECT TOP @topK c.id, c.content, c.metadata,
           VectorDistance(c.embedding, @queryVector) AS similarity
    FROM c
    ORDER BY VectorDistance(c.embedding, @queryVector)
    """
    results = container.query_items(
        query=query,
        parameters=[
            {"name": "@topK", "value": top_k},
            {"name": "@queryVector", "value": query_embedding}
        ],
        partition_key="default"
    )
    return list(results)

# Hybrid: filter + vector search
def filtered_vector_search(
    query_embedding: list[float],
    category: str,
    top_k: int = 5
) -> list[dict]:
    query = """
    SELECT TOP @topK c.id, c.content, c.metadata,
           VectorDistance(c.embedding, @queryVector) AS similarity
    FROM c
    WHERE c.metadata.category = @category
    ORDER BY VectorDistance(c.embedding, @queryVector)
    """
    results = container.query_items(
        query=query,
        parameters=[
            {"name": "@topK", "value": top_k},
            {"name": "@queryVector", "value": query_embedding},
            {"name": "@category", "value": category}
        ],
        partition_key="default"
    )
    return list(results)
```

**Container creation with vector index policy (via REST/ARM):**

```json
{
  "indexingPolicy": {
    "vectorIndexes": [
      {
        "path": "/embedding",
        "type": "diskANN"
      }
    ]
  },
  "vectorEmbeddingPolicy": {
    "vectorEmbeddings": [
      {
        "path": "/embedding",
        "dataType": "float32",
        "distanceFunction": "cosine",
        "dimensions": 1536
      }
    ]
  }
}
```

---

## 15. Enterprise Features (Why Enterprises Choose Azure)

### Compliance Certifications

Azure holds 100+ compliance certifications, more than any other cloud provider:

| Category | Certifications |
|----------|---------------|
| **Global** | ISO 27001, ISO 27017, ISO 27018, SOC 1/2/3, CSA STAR |
| **US Government** | FedRAMP High, DoD IL2/IL4/IL5/IL6, CJIS, IRS 1075 |
| **Healthcare** | HIPAA, HITRUST, FDA 21 CFR Part 11 |
| **Finance** | PCI DSS, SOX, GLBA, SEC 17a-4 |
| **EU/UK** | GDPR, UK G-Cloud, ENS (Spain), C5 (Germany) |
| **Industry** | GxP, NERC CIP, TISAX |

### Azure Government

Physically isolated datacenters in the US, operated by screened US citizens:
- IL2, IL4, IL5 (Azure Government)
- IL6 (Azure Government Secret)
- Azure Government Top Secret (air-gapped)
- Same services as commercial Azure (250+)
- FedRAMP High authorization

### Azure China (21Vianet)

Operated by 21Vianet (Chinese company), physically and logically separated from global Azure:
- Data stays in China
- Compliant with Chinese data sovereignty laws
- Separate portal (portal.azure.cn)
- Not all services available

### Hybrid Cloud

| Product | Description |
|---------|-------------|
| **Azure Arc** | Manage on-prem servers, Kubernetes, SQL, data services from Azure portal |
| **Azure Stack HCI** | Run Azure services on your own hardware (VMs, AKS, Azure Virtual Desktop) |
| **Azure Stack Hub** | Disconnected/sovereign cloud on your hardware (full Azure on-prem) |
| **Azure Stack Edge** | Edge computing device (GPU/FPGA) for AI inference at edge |

### Microsoft 365 Integration

| Integration | How It Works |
|-------------|-------------|
| **Teams** | Embed AI chatbot in Teams via Bot Framework + Azure OpenAI |
| **SharePoint** | Index SharePoint content in Azure AI Search for RAG |
| **Outlook** | AI email drafting via Microsoft Graph + Azure OpenAI |
| **Power Automate** | Trigger Azure Functions / Logic Apps from Power Automate flows |
| **Power BI** | Visualize data from Cosmos DB, SQL, blob analytics |
| **Copilot Studio** | Build custom copilots with Azure OpenAI backend (no-code) |

### Power Platform / Copilot Studio

Build custom AI assistants without code:
- **Copilot Studio:** Drag-and-drop chatbot builder with Azure OpenAI, AI Search, Dataverse
- **Power Automate:** 800+ connectors, AI Builder (document processing, prediction)
- **Power Apps:** Low-code apps with AI features
- **Dataverse:** Managed database underlying all Power Platform

**Revenue opportunity:** Many enterprises want custom copilots integrated with their Microsoft 365 data. Copilot Studio + Azure OpenAI is the fastest path.

---

## Appendix A: Service Name Changes (Decoder Ring)

Azure renames services frequently. Here is the mapping:

| Old Name | New Name | When Changed |
|----------|----------|-------------|
| Azure Cognitive Search | Azure AI Search | 2023 |
| Azure Form Recognizer | Azure AI Document Intelligence | 2023 |
| Azure Active Directory (AAD) | Microsoft Entra ID | 2023 |
| Azure AI Studio | Microsoft AI Foundry | 2025 |
| Azure Cognitive Services | Azure AI Services | 2023 |
| Azure Bot Service | Azure AI Bot Service | 2023 |
| LUIS (Language Understanding) | CLU (Conversational Language Understanding) | 2023 |
| QnA Maker | Custom Question Answering (in AI Language) | 2022 |
| Azure Machine Learning Studio (classic) | Retired | 2024 |
| Power Virtual Agents | Copilot Studio | 2023 |
| Azure CDN (Microsoft Standard) | Azure Front Door Standard | 2025 (retiring) |

---

## Appendix B: Region Availability for AI Services

Not all AI services are available in all regions. Key regions for AI:

| Region | Azure OpenAI | AI Search | Document Intelligence | Speech |
|--------|-------------|-----------|----------------------|--------|
| **East US** | Yes | Yes | Yes | Yes |
| **East US 2** | Yes | Yes | Yes | Yes |
| **West US** | Yes | Yes | Yes | Yes |
| **West US 3** | Yes | Yes | Yes | Yes |
| **Central US** | Yes | Yes | Yes | Yes |
| **North Central US** | Yes | Yes | Yes | Yes |
| **South Central US** | Yes | Yes | Yes | Yes |
| **Canada East** | Yes | Yes | Yes | Yes |
| **UK South** | Yes | Yes | Yes | Yes |
| **West Europe** | Yes | Yes | Yes | Yes |
| **Sweden Central** | Yes (recommended) | Yes | Yes | Yes |
| **France Central** | Yes | Yes | Yes | Yes |
| **Japan East** | Yes | Yes | Yes | Yes |
| **Australia East** | Yes | Yes | Yes | Yes |
| **Central India** | Limited | Yes | Yes | Yes |

**Tip:** Sweden Central and East US tend to have the highest Azure OpenAI quotas and newest model availability.

---

## Appendix C: Azure SDKs for Python (AI Projects)

```bash
# Core
pip install azure-identity          # Authentication (managed identity, DefaultCredential)
pip install azure-mgmt-resource     # Resource management

# AI Services
pip install openai                  # Azure OpenAI (use AzureOpenAI class)
pip install azure-search-documents  # AI Search
pip install azure-ai-formrecognizer # Document Intelligence (v3+: azure-ai-documentintelligence)
pip install azure-cognitiveservices-speech  # Speech SDK
pip install azure-ai-contentsafety  # Content Safety
pip install azure-ai-textanalytics  # Language (NER, sentiment, PII)
pip install azure-ai-vision-imageanalysis  # Vision

# Storage & Databases
pip install azure-storage-blob      # Blob Storage
pip install azure-cosmos            # Cosmos DB
pip install azure-data-tables       # Table Storage

# Messaging
pip install azure-servicebus        # Service Bus
pip install azure-eventhub          # Event Hubs

# Monitoring
pip install azure-monitor-opentelemetry  # Application Insights + OpenTelemetry

# Key Vault
pip install azure-keyvault-secrets  # Secrets
pip install azure-keyvault-keys     # Keys
pip install azure-keyvault-certificates  # Certificates
```

---

**End of document. Last updated: March 15, 2026.**
**Total services covered: 45+ | Pricing data points: 200+ | Architecture patterns: 4 | CLI commands: 80+**
