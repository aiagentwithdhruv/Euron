# Docker, Kubernetes, vLLM & Triton — Structured Prompts
## Quick-copy prompts for hands-on practice

---

## 0. Docker Demo — Multi-Container App (CLASS EXERCISE)

### The Prompt Used to Build the Demo
```
Build a simple Docker demo application to understand Docker concepts (NOT complex business logic).
Create 3 containers orchestrated with Docker Compose:

1. Python container (FastAPI) — simple endpoints
2. PostgreSQL container — database
3. Redis container — cache

Requirements:
- Dockerfile with comments explaining each step
- docker-compose.yml connecting all 3 on a shared network
- Health checks on all containers
- Named volume for DB persistence
- depends_on with health conditions
- Endpoints to test each container individually + all together
- .dockerignore
- Keep it Hello World simple — focus on Docker, not Python logic

Docker concepts to demonstrate:
- Custom image (Dockerfile) vs pre-built image (postgres, redis)
- Service networking (containers talking by name)
- Volume persistence
- Port mapping
- Environment variables
- Health checks
- Docker Compose orchestration
```

### Run the Demo
```bash
cd docker-demo
docker compose up -d --build      # Start all 3 containers
docker compose ps                 # Verify all running
curl localhost:8000/               # Test Python
curl localhost:8000/db             # Test PostgreSQL
curl localhost:8000/cache          # Test Redis
curl localhost:8000/both           # Test all 3 together
curl localhost:8000/health         # Health check
docker compose logs -f             # Watch logs
docker compose down -v             # Cleanup everything
```

---

## 1. Docker Basics

### Build & Run a FastAPI App
```
Create a production-ready Dockerfile for a Python FastAPI application with:
- Multi-stage build (builder + production)
- Non-root user
- Health check
- .dockerignore
- pip cache mount for fast rebuilds
Then show me docker build and docker run commands.
```

### Docker Compose Full Stack
```
Create a docker-compose.yml for a full-stack AI application with:
- FastAPI backend (port 8000)
- PostgreSQL database with healthcheck
- Redis cache
- Named volumes for persistence
- Internal network for DB (no external access)
- Environment variables from .env file
Include all best practices: restart policies, resource limits, logging config.
```

### Debug a Failing Container
```
My Docker container keeps crashing. Walk me through a systematic debugging approach:
1. How to check logs
2. How to inspect the container state
3. How to exec into it
4. How to check resource usage (OOM kills)
5. How to check health status
Give me the exact commands for each step.
```

---

## 2. Dockerfile Optimization

### Minimize Image Size
```
I have a Python ML application with PyTorch, transformers, and FastAPI.
The current Docker image is 8GB. Help me reduce it by:
1. Choosing the right base image
2. Multi-stage build to exclude build tools
3. Proper layer ordering for cache
4. BuildKit cache mounts for pip
5. Comprehensive .dockerignore
Show me the before and after Dockerfile.
```

### Security Hardening
```
Review this Dockerfile for security issues and fix them:
- Running as root
- Secrets in ENV
- No resource limits
- Using latest tag
- No health check
Produce a hardened production Dockerfile with all OWASP best practices.
```

---

## 3. Kubernetes

### Deploy an LLM on Kubernetes
```
Create Kubernetes manifests to deploy a Llama-3-8B model using vLLM on a GPU cluster:
1. Deployment with GPU resource requests (nvidia.com/gpu)
2. Service (LoadBalancer) for external access
3. HorizontalPodAutoscaler based on CPU utilization
4. ConfigMap for model configuration
5. Secret for HuggingFace token
6. PersistentVolumeClaim for model cache
7. Readiness and liveness probes
Include the exact kubectl commands to apply everything.
```

### Kubernetes from Scratch Explanation
```
Explain Kubernetes architecture like I'm deploying my first application:
1. What is the Control Plane (Master Node) and what does each component do?
2. What are Worker Nodes and how do Pods run on them?
3. How does a Service route traffic to the right Pod?
4. What happens when a Pod crashes — how does self-healing work?
5. How does HPA auto-scale based on load?
Use the analogy of a restaurant: master = manager, workers = kitchen stations, service = waiter.
```

### Convert Docker Compose to Kubernetes
```
I have this docker-compose.yml running locally. Convert it to Kubernetes manifests:
- Deployment for each service
- Services for networking
- ConfigMaps for environment variables
- PersistentVolumeClaims for volumes
- Ingress for external HTTP routing
Explain each mapping: what Compose concept maps to which K8s object.
```

---

## 4. vLLM

### Set Up vLLM Server
```
Help me deploy vLLM to serve Llama-3.1-8B-Instruct:
1. Install vLLM
2. Start the OpenAI-compatible server with optimal settings
3. Show me curl commands to test chat completions
4. Show me Python client code using the openai library
5. Configure for production: prefix caching, chunked prefill, disable request logging
What GPU do I need and how much VRAM?
```

### vLLM with Docker Compose + Monitoring
```
Create a production docker-compose.yml for vLLM with:
- vLLM server with GPU access and health checks
- Prometheus scraping vLLM metrics
- Grafana for dashboards
- nginx as reverse proxy with streaming support
Include the prometheus.yml config and explain key metrics to monitor:
- Queue depth
- KV cache utilization
- Throughput (tokens/sec)
- TTFT P95/P99
```

### Multi-GPU vLLM for 70B Model
```
I need to serve Llama-3.1-70B on 4x A100 80GB GPUs. Help me:
1. Calculate if 4 GPUs are enough (model size vs VRAM)
2. Configure tensor parallelism (--tensor-parallel-size 4)
3. Docker run command with specific GPU assignment
4. Kubernetes Deployment YAML with 4 GPU resources
5. Key configuration flags for optimal throughput
6. Common issues and fixes (NCCL timeout, shared memory)
```

### Compare vLLM vs Raw HuggingFace Serving
```
Show me side-by-side code for serving a model with:
1. Raw HuggingFace transformers (pipeline or model.generate)
2. vLLM (offline inference + server mode)
Compare: throughput, latency, GPU memory usage, concurrent user handling.
Explain WHY vLLM is faster (PagedAttention, continuous batching).
```

---

## 5. NVIDIA Triton

### Deploy Multiple Models on Triton
```
Set up NVIDIA Triton to serve 3 models simultaneously:
1. ResNet50 (PyTorch) for image classification
2. BERT (ONNX) for text NER
3. Custom Python model for text embeddings
Create:
- Model repository directory structure
- config.pbtxt for each model (with dynamic batching)
- Docker run command
- Python client code to call each model
```

### Triton Model Ensemble Pipeline
```
Build a Triton ensemble pipeline for image classification:
Step 1: Preprocessor (Python backend) — resize + normalize image
Step 2: ResNet50 (TensorRT) — classify
Step 3: Postprocessor (Python backend) — decode to human-readable label
Create:
- All config.pbtxt files (including ensemble DAG)
- Python backend model.py files
- Directory structure
- Client code to call the pipeline end-to-end
```

### Triton on Kubernetes with Auto-scaling
```
Deploy Triton Inference Server on Kubernetes with:
1. Deployment YAML with GPU, shared memory, health probes
2. Service exposing HTTP (8000), gRPC (8001), metrics (8002)
3. HPA based on GPU utilization (custom Prometheus metric)
4. S3-backed model repository
5. Prometheus + Grafana monitoring
Include Helm chart commands as alternative.
```

### Triton vs vLLM — When to Use Which
```
I'm building an AI platform that serves:
- LLM for chat (Llama-3-70B)
- Vision model for image analysis (ResNet/CLIP)
- Embedding model for RAG (all-MiniLM)
- Custom ML model for scoring (XGBoost)

Should I use vLLM, Triton, or both? Design the architecture:
- Which model goes where
- How they communicate
- Docker Compose or Kubernetes setup
- Load balancing strategy
- Cost optimization tips
```

---

## 6. Full Production Pipeline

### End-to-End AI Deployment
```
Design a complete production deployment for an LLM-powered application:

Infrastructure:
- Kubernetes cluster on AWS EKS with GPU nodes (g5.xlarge)
- vLLM for LLM serving (Llama-3-8B)
- Triton for embedding model + reranker
- PostgreSQL + pgvector for vector storage
- Redis for caching

Create:
1. Kubernetes manifests for all services
2. Docker images (Dockerfiles) for custom services
3. Ingress with TLS
4. HPA for auto-scaling vLLM and Triton
5. Prometheus + Grafana monitoring stack
6. CI/CD pipeline (GitHub Actions → build → scan → deploy)

Include cost estimation for running this on AWS.
```

### Dockerize and Deploy an ML Training + Serving Pipeline
```
I have a PyTorch model training script and want to:
1. Dockerize the training (with GPU support)
2. Export to ONNX after training
3. Deploy on Triton for serving
4. Set up A/B testing between model v1 and v2
5. Monitor performance and auto-rollback if latency increases

Create all Dockerfiles, config files, and deployment scripts.
Show the complete workflow from `git push` to production serving.
```

---

## 7. Interview / Flex Prompts

### Explain Docker to a Non-Technical Person
```
Explain Docker using a shipping container analogy in 3 sentences.
Then explain: images vs containers, Dockerfile, Docker Compose.
Keep it simple enough for a product manager to understand.
```

### Kubernetes Architecture Deep Dive
```
Draw the Kubernetes architecture (ASCII) and explain each component:
- Control Plane: API Server, etcd, Scheduler, Controller Manager
- Worker Node: kubelet, kube-proxy, container runtime
- How a Deployment creates ReplicaSets which create Pods
- How a Service discovers and load-balances across Pods
- How Ingress routes external HTTP traffic
Make it interview-ready: concise but technically accurate.
```

### vLLM PagedAttention Explained
```
Explain PagedAttention (vLLM's core innovation) in 5 levels:
1. One sentence for a PM
2. One paragraph for a software engineer
3. Technical explanation for an ML engineer (with OS virtual memory analogy)
4. Implementation details (block tables, copy-on-write, continuous batching)
5. Performance impact with numbers (throughput gains, memory savings)
```

### System Design: LLM Serving at Scale
```
Design a system to serve an LLM to 10,000 concurrent users:
1. Architecture (load balancer → API gateway → vLLM cluster)
2. How many GPUs needed (calculate from expected tokens/sec)
3. Auto-scaling strategy (HPA on queue depth)
4. Caching strategy (prefix caching, response caching)
5. Fallback and circuit breaker patterns
6. Monitoring and alerting
7. Cost optimization (spot instances, quantization, batching)
Draw the architecture diagram (ASCII) and estimate monthly AWS cost.
```
