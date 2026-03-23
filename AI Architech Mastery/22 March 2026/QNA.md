# Docker, Kubernetes, vLLM & Triton — Q&A Reference
## 22 March 2026

---

### Q1: What is the production AI deployment stack for end-to-end scale?

**Docker** → Containerize everything (code + deps = one portable unit)
**Docker Compose** → Orchestrate multi-container apps locally
**Kubernetes** → Multi-machine orchestration, auto-scaling, self-healing
**vLLM** → Fast LLM inference (24x faster than PyTorch, PagedAttention)
**Triton** → Universal model serving (any model, any framework, simultaneously)

```
Training (one-time) → Model Artifact → Serving (the real job)
                                         ├── vLLM (LLMs only)
                                         └── Triton (any model)
```

---

### Q2: When to use vLLM vs Triton?

| Scenario | Use |
|----------|-----|
| Single LLM API (chatbot, RAG) | vLLM |
| LLM + vision + ML together | Triton |
| Multiple models simultaneously | Triton |
| OpenAI-compatible drop-in | vLLM |
| Model ensemble/pipeline (preprocess → infer → postprocess) | Triton |
| Maximum LLM throughput on NVIDIA | Triton + TensorRT-LLM |

---

### Q3: When to use Docker Compose vs Kubernetes?

| Scenario | Use |
|----------|-----|
| Local dev, < 100 users | Docker Compose |
| Multiple machines, auto-scale | Kubernetes |
| Single server production | Docker Compose + restart policies |
| 1M+ users, zero downtime | Kubernetes (EKS/GKE/AKS) |

---

### Q4: What's the production checklist for deploying AI at scale?

1. Dockerize everything (multi-stage, non-root, health checks)
2. Compose for local dev, K8s for production
3. vLLM/Triton for model serving (never raw PyTorch)
4. HPA auto-scales on CPU/GPU/queue depth
5. Prometheus + Grafana for monitoring
6. Readiness probes before routing traffic
7. PVC for model weights (download once, mount everywhere)
8. Secrets via K8s Secrets or Vault (never env vars in images)

---

### Q5: Container vs VM — what's the difference?

| | Container | VM |
|---|-----------|-----|
| Isolation | Process-level (namespaces) | Full OS kernel |
| Startup | Milliseconds | Minutes |
| Size | MBs | GBs |
| Overhead | Near-zero (shares host kernel) | High (emulates hardware) |
| Use case | App packaging, microservices | Full OS isolation, legacy |

---

### Q6: How does Kubernetes handle traffic across multiple machines?

```
Traffic → Master Node (Control Plane) → decides which worker is available
              │
              ├── Worker 1 (available ✓) → handles request
              ├── Worker 2 (busy ✗) → skipped
              ├── Worker 3 (available ✓) → handles request
              └── Worker 4 (available ✓) → handles request
```

- **kube-scheduler** picks the node
- **Service** load-balances across healthy pods
- **HPA** auto-scales pods up/down based on load
- Customer never sees downtime

---

### Q7: What makes vLLM 24x faster than raw PyTorch?

**PagedAttention** — treats GPU KV cache like OS virtual memory:
- Allocates memory blocks on-demand (not pre-allocated)
- < 4% memory waste (vs 60-80% with traditional approach)
- Copy-on-write for beam search

**Continuous Batching** — doesn't wait for entire batch to finish:
- After each token step, finished requests leave, new ones join
- GPU stays near 100% utilization

---

### Q8: What is Docker Compose and why use it?

One YAML file to run multiple containers together:
```yaml
services:
  app:      # Your code
  db:       # PostgreSQL
  redis:    # Cache
```
- Containers talk by service name (DNS)
- One command: `docker compose up -d`
- Volumes persist data
- Health checks + restart policies
- Perfect for local dev and small deployments

---

### Q9: What databases can you swap with Docker?

```
Python App → MongoDB     (docker pull mongo)
           → PostgreSQL  (docker pull postgres:16-alpine)
           → Redis       (docker pull redis:7-alpine)
           → Qdrant      (docker pull qdrant/qdrant)  # vector DB
           → MySQL       (docker pull mysql:8)
```
No installation needed — just change one service in docker-compose.yml.

---

### Q10: One-liner to explain this stack at MSBC?

> "I can take any AI model from training to production — containerize it with Docker, serve it at scale with vLLM or Triton, orchestrate across machines with Kubernetes, and monitor with Prometheus. End to end, zero to production."

---

### Q11: How do you pronounce Kubernetes?

**Kubernetes** = **"koo-ber-NET-eez"**

From Greek κυβερνήτης = "helmsman / pilot" (steers a ship → logo is a ship's wheel).

Short forms:
- **K8s** = "kaytes" (K + 8 letters + s)
- **kube** = "kyoob" (casual)

---

*Add more Q&As below as they come up...*
