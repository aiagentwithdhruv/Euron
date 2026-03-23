# AI Architect Mastery - Class Notes
## 22 March 2026 - Docker, Kubernetes, vLLM & NVIDIA Triton

---

### Docker Hub — Image Registry

- **hub.docker.com** — like GitHub but for Docker images
- Search for any pre-built image (e.g., Kafka, PostgreSQL, Redis, Nginx)
- Images come from: Official (Docker), Verified Publishers (VMware, Canonical, Adobe), Community
- Example: searching "kafka" shows 34,852 results:
  - `Kafka` (Docker Hardened Image) — 100K+ pulls
  - `bitnami/kafka` (VMware) — 100M+ pulls
  - `apache/kafka` (Apache Foundation) — 10M+ pulls
- Filter by: Images, Helm Charts, Compose, AI Models
- Trusted content: Hardened Images, Official Images, Verified Publishers
- You `docker pull` these images instead of building from scratch

**Key concept:** You don't build everything from scratch — pull pre-built images from Docker Hub and focus on YOUR application code.

---

### Docker + Databases — Swap Easily

A Python app can connect to different databases — Docker lets you swap without installing anything:

```
┌──────────────┐
│  Python App  │──→ MongoDB    (NoSQL / documents)
│              │──→ PostgreSQL (Relational / SQL)
│              │──→ Pinecone   (Vector DB / AI & RAG)
└──────────────┘
```

- Need MongoDB? → `docker pull mongo`
- Need PostgreSQL? → `docker pull postgres:16-alpine`
- Need a vector DB? → `docker pull qdrant/qdrant` (Pinecone is cloud-only, Qdrant is self-hosted alternative)
- **No installation on your machine** — just pull and run
- Switch databases by changing one service in `docker-compose.yml`

---

### Class Summary & Next Week's Agenda

**Today (22 March) — Theory covered:**
- Docker basics, Docker Hub, Docker Compose
- Kubernetes — multi-machine orchestration (Master Node → Worker Nodes)
- vLLM — LLM inference serving (PagedAttention, faster than PyTorch/TF)
- NVIDIA Triton — universal model serving (any model, any framework)
- Docker + databases (MongoDB, PostgreSQL, Pinecone)

**Next Week — Hands-on with all services:**

| Tool | Where | Notes |
|------|-------|-------|
| **Kubernetes** | AWS EKS or Azure AKS (need multiple machines) | New: K8s cluster for scaling |
| **Triton** | Local GPU (already installed) | Local demo with real models |
| **vLLM** | Local GPU + Cloud GPU | Previously shown on single GPU; this time on K8s cluster |
| **vLLM + K8s** | Cloud (EKS/AKS) | **NEW** — serve millions with auto-scaling |

**Key goal for next class:**
> "One system can serve a million on the other side — manage scale and load automatically"

**Instructor note:** vLLM materials already available from previous classes — can get inferencing working in 5 minutes on a single GPU. Next class focuses on K8s cluster deployment for production scale.

---

### Kubernetes — The Multi-Machine Problem

- Docker handles containers on **one machine**
- But for heavy apps (e.g., LLM hosting) with massive traffic, you need **multiple machines**
- Example: Machine 1, Machine 2, Machine 3, Machine 4
- Need a service that identifies which machine is available when traffic comes
- Routes/diverts traffic to the available machine → customer faces zero issues

**Solution: Kubernetes**
- **Master Node (Control Plane)** attached to multiple worker machines
- When traffic comes, master node decides: "which machine should handle this?"
- Routes based on availability, health, and resource usage

```
Traffic → Master Node → m1 (available ✓) → handles request
                      → m2 (busy ✗)
                      → m3 (available ✓)
                      → m4 (available ✓)
```

---

### vLLM — Why It Exists

**The Problem:**
- Training LLMs = one-time job (spin GPU, train, done)
- But after training, you have to **serve** the model to many users
- Real **inferencing** happens here: query → LLM → output

**Traditional Approach (Slow):**
- Using PyTorch, TensorFlow, or HuggingFace libraries directly
- Query goes through these libraries → into LLM → executes → output
- This approach is **very slow** — occupies more resources, more GPU
- Not optimized for serving at scale

**vLLM solves this:**
- Purpose-built for **LLM inference serving** (not training)
- Optimized GPU utilization — does more with less
- Handles concurrent users efficiently
- Much faster than raw PyTorch/TensorFlow serving

---

### NVIDIA Triton Inference Server — Beyond LLMs

**The limitation of vLLM:**
- vLLM is designed **only for LLMs** (as the name suggests)
- What if you have a **vision-based model**?
- What if you have a **core NLP model**?
- What if you have an **ML model** that needs GPU?
- vLLM can't help with these

**Enter NVIDIA Triton:**
- Open-source inference server by NVIDIA
- "Streamlines AI inferencing" — **ALL kinds of models**, not just LLMs
- Can control **multiple models simultaneously** across different categories
- Built-in **model warming** (pre-warm GPU before serving live traffic)
- Runs on top of NVIDIA hardware

**Architecture (from class diagram):**
```
Application
    │
Python/C++ Client Library
    │
    ├── HTTP ──┐        ┌── Model Repository
    └── gRPC ──┤        │   (Persistent Volume)
               │        │
         ┌─────▼────────▼──────┐
         │   TRITON SERVER     │
         │                     │
         │  C API              │
         │    │                │
         │  Inference Request  │
         │    │                │
         │  Per-Model          │   Framework Backends:
         │  Scheduler ────────►│   • TensorRT
         │  Queues             │   • TensorFlow
         │                     │   • ONNX
         │                     │   • PyTorch
         │                     │   • Custom
         │                     │
         │  Status/Health ─────┼──► HTTP (Prometheus)
         └─────────────────────┘
              │  │  │  │  │
            GPU GPU GPU GPU CPU
```

**Key difference from vLLM:**
| | vLLM | Triton |
|---|---|---|
| Model types | LLMs only | ANY model (vision, NLP, ML, LLM) |
| Multi-model | One per instance | Many simultaneously |
| Model warming | Manual | Built-in config |
| Frameworks | HuggingFace | TensorRT, TF, ONNX, PyTorch, Custom |
