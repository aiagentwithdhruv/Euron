# Docker — Production-Grade Reference (March 2026)

> Complete reference for developers and AI architects. Covers every layer from core concepts to production deployment patterns.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Architecture](#2-architecture)
3. [Dockerfile — Every Instruction](#3-dockerfile--every-instruction)
4. [Docker CLI — All Important Commands](#4-docker-cli--all-important-commands)
5. [Docker Compose v2](#5-docker-compose-v2)
6. [Networking](#6-networking)
7. [Volumes and Storage](#7-volumes-and-storage)
8. [Docker for AI/ML](#8-docker-for-aiml)
9. [Security](#9-security)
10. [Optimization](#10-optimization)
11. [Registry](#11-registry)
12. [Orchestration Intro](#12-orchestration-intro)
13. [Common Patterns](#13-common-patterns)
14. [Debugging](#14-debugging)
15. [Production Checklist](#15-production-checklist)

---

## 1. Core Concepts

### What is Docker?

Docker is a platform for building, shipping, and running applications in isolated environments called **containers**. It packages code, runtime, system tools, libraries, and settings into a single portable unit that runs identically on any machine.

Key guarantee: "Works on my machine" becomes "works on every machine."

### Containers vs Virtual Machines

| Dimension          | Container                          | Virtual Machine                    |
|--------------------|------------------------------------|------------------------------------|
| Isolation unit     | Process-level (namespaces/cgroups) | Full OS kernel                     |
| Startup time       | Milliseconds                       | Seconds to minutes                 |
| Size               | MB range                           | GB range                           |
| Overhead           | Near-zero (shares host kernel)     | High (emulates hardware)           |
| Portability        | Any OS with Docker Engine          | Hypervisor-specific                |
| Use case           | App packaging + microservices      | Full OS isolation, legacy apps     |

Containers are NOT VMs. They share the host kernel. Linux containers require a Linux kernel — on macOS and Windows, Docker Desktop runs a lightweight Linux VM to provide that kernel.

### Docker Engine

The core runtime installed on a server/laptop. Consists of:
- **dockerd** — the daemon process that manages objects (images, containers, networks, volumes)
- **containerd** — low-level container runtime (OCI-compliant)
- **runc** — creates the actual container process

### Docker Desktop

GUI application for macOS/Windows that bundles Docker Engine inside a lightweight Linux VM (currently using Apple Virtualization.framework on macOS). Includes:
- Docker Engine
- Docker Compose
- Docker Scout (security scanning)
- Docker Extensions marketplace
- BuildKit enabled by default since Engine 23.0

---

## 2. Architecture

### Component Map

```
Developer                 Registry (Docker Hub / ECR / GCR)
    |                              |
    | docker build/push            | docker pull
    v                              v
Docker Client (CLI)  -----REST---> Docker Daemon (dockerd)
                                        |
                              ┌─────────┴──────────┐
                              |                    |
                         containerd            Networks
                              |                Volumes
                             runc
                              |
                         Container
                         (isolated process)
```

### Docker Daemon (`dockerd`)

- Listens on a Unix socket `/var/run/docker.sock` by default
- Can be configured to listen on a TCP port (with TLS for remote access)
- Manages the full lifecycle of containers, images, networks, and volumes
- Delegates low-level container operations to containerd

### Docker Client

- The `docker` CLI binary
- Communicates with `dockerd` via REST API over the Unix socket
- Can connect to remote daemons via DOCKER_HOST env var or Docker contexts

### Images

- **Immutable** read-only templates
- Built from a Dockerfile
- Stored as a stack of **layers** (one layer per Dockerfile instruction that changes the filesystem)
- Each layer is identified by its SHA256 content hash
- Layers are **shared** across images — pulling `python:3.12-slim` once reuses layers for all images built from it

### Containers

- A **running instance** of an image
- Adds a thin **writable layer** on top of the image's read-only layers
- Isolated via Linux namespaces (PID, NET, MNT, UTS, IPC, USER) and cgroups (CPU, memory limits)
- Ephemeral by default — data written to the writable layer is lost when the container is removed

### Union Filesystem (OverlayFS)

Docker uses OverlayFS (overlay2 storage driver) to merge multiple read-only image layers into a single unified view:

```
Container writable layer  (read-write)
        |
Image Layer N              (read-only)
        |
Image Layer N-1            (read-only)
        |
Base image layer           (read-only)
```

When a container modifies a read-only file, OverlayFS performs a **copy-on-write** — it copies the file to the writable layer before modifying it. The original image layer is unchanged.

### Docker Registry

A storage and distribution system for Docker images. Structure:
- `registry/repository:tag`
- Example: `docker.io/library/python:3.12-slim`
  - registry: `docker.io`
  - repository: `library/python`
  - tag: `3.12-slim`

---

## 3. Dockerfile — Every Instruction

### Parser Directives (top of file, before any instructions)

```dockerfile
# syntax=docker/dockerfile:1
# escape=\
```

- `syntax` — pins the BuildKit frontend version (enables latest features)
- `escape` — changes the escape character (useful on Windows where `\` is a path separator)

### FROM

```dockerfile
FROM [--platform=<platform>] <image>[:<tag>][@<digest>] [AS <name>]

# Examples
FROM python:3.12-slim
FROM python:3.12-slim AS builder
FROM --platform=linux/amd64 node:20-alpine AS build
FROM scratch                    # Empty base (for compiled binaries)
FROM ubuntu:22.04@sha256:abc123 # Pinned by digest (immutable)
```

Rules:
- Must be the first instruction (only `ARG` can precede it for build args)
- Every `FROM` starts a new build stage
- `AS <name>` names the stage for `COPY --from=<name>` references
- `scratch` is the empty base — used for statically compiled Go/Rust binaries
- Pin by digest in production for reproducible builds

### RUN

```dockerfile
RUN <command>                                    # Shell form (runs in /bin/sh -c)
RUN ["executable", "param1", "param2"]           # Exec form (no shell, no variable expansion)

# Mount options (BuildKit)
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install
RUN --mount=type=ssh ssh-keyscan github.com >> /etc/ssh/known_hosts
RUN --mount=type=bind,source=.,target=/src ./build.sh

# Network options
RUN --network=none pip install -r requirements.txt  # No network access during build
RUN --network=host apt-get update                   # Use host network

# Best practices
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*    # Clean apt cache in SAME layer
```

Key points:
- Each `RUN` creates a new image layer
- Chain commands with `&&` to keep related operations in one layer
- Always clean up in the same `RUN` instruction (not a later one) — cleanup in a later layer does NOT reduce image size
- Use `--mount=type=cache` to cache package manager downloads across builds without baking them into the image

### COPY

```dockerfile
COPY <src> <dest>
COPY ["<src>", "<dest>"]  # Required if path contains whitespace

# Options
COPY --from=builder /app/dist /app/dist          # From another build stage
COPY --from=nginx:alpine /etc/nginx /etc/nginx   # From an external image
COPY --chown=node:node . /app                    # Set ownership on copy
COPY --chmod=755 scripts/ /usr/local/bin/        # Set permissions on copy
COPY --link . /app                               # Layer linking (better caching)
COPY --parents src/a/b.txt /dest/               # Preserves src/a/ hierarchy

# Glob patterns
COPY *.py /app/
COPY src/ /app/src/
```

Prefer `COPY` over `ADD` for local files. It is explicit, predictable, and auditable.

### ADD

```dockerfile
ADD <src> <dest>

# Special capabilities COPY lacks:
ADD https://example.com/file.tar.gz /tmp/      # Download from URL
ADD archive.tar.gz /app/                       # Auto-extract tar archives
```

Use `ADD` only when you need URL downloads or tar auto-extraction. For everything else, use `COPY`. Never use `ADD` for local files — use `COPY`.

### WORKDIR

```dockerfile
WORKDIR /app

# Creates directory if it doesn't exist
# All subsequent RUN, COPY, ADD, ENTRYPOINT, CMD are relative to WORKDIR
# Can be set multiple times (paths stack)
WORKDIR /app
WORKDIR src
# Now in /app/src

# Always use absolute paths
# WRONG: WORKDIR src
# RIGHT: WORKDIR /app/src
```

### ENV

```dockerfile
ENV NODE_ENV=production
ENV PORT=8080 DEBUG=false

# Multi-line (older syntax, still works)
ENV MY_VAR my-value

# Access in build and at runtime
RUN echo $NODE_ENV
```

`ENV` variables persist into the final image and are available at container runtime. Do NOT use `ENV` for secrets — they are visible in `docker inspect` and image layers. Use build args or runtime secrets instead.

### ARG

```dockerfile
ARG PYTHON_VERSION=3.12
ARG BUILD_DATE
ARG GIT_COMMIT

FROM python:${PYTHON_VERSION}-slim

# Pass at build time
# docker build --build-arg PYTHON_VERSION=3.11 .

# ARG scope is stage-specific — re-declare after each FROM
FROM python:${PYTHON_VERSION}-slim AS final
ARG GIT_COMMIT   # Must re-declare to use in this stage
LABEL git.commit=${GIT_COMMIT}
```

`ARG` values are NOT embedded in the final image by default (unlike `ENV`). They are available only during the build. Exception: if an `ARG` is used in a `FROM` line, it's visible before the first stage.

### EXPOSE

```dockerfile
EXPOSE 8080
EXPOSE 8080/tcp
EXPOSE 8080/udp
EXPOSE 8080 443
```

Documentation only. Does NOT actually publish or open ports. Publishing ports requires `-p` at `docker run` time or `ports:` in Compose. Useful for tooling, documentation, and `docker run -P` (publish all exposed ports to random host ports).

### CMD

```dockerfile
CMD ["python", "app.py"]              # Exec form (preferred)
CMD python app.py                      # Shell form (wraps in /bin/sh -c)
CMD ["param1", "param2"]              # As default args to ENTRYPOINT

# Only the LAST CMD in a Dockerfile takes effect
# CMD is overridden by arguments passed to docker run:
# docker run myimage python other_script.py  <-- overrides CMD
```

`CMD` sets the default command. Users can override it. Use exec form to ensure signals (SIGTERM) are sent directly to your process, not to a shell wrapper.

### ENTRYPOINT

```dockerfile
ENTRYPOINT ["python", "app.py"]                # Exec form (preferred)
ENTRYPOINT python app.py                        # Shell form

# Combined with CMD (CMD provides default args):
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run myimage               → python app.py
# docker run myimage other.py      → python other.py

# Override at runtime:
# docker run --entrypoint /bin/sh myimage
```

`ENTRYPOINT` makes the container behave like an executable. It is NOT overridden by `docker run` arguments — those become additional arguments to the ENTRYPOINT. Override requires `--entrypoint` flag.

### Entrypoint vs CMD Decision Matrix

| Goal | Use |
|------|-----|
| Container IS a command (always runs same binary) | ENTRYPOINT exec form |
| Provide default but allow full override | CMD exec form |
| Fixed binary + configurable default args | ENTRYPOINT + CMD together |
| Shell scripting with variable expansion | Shell form (either) |

### VOLUME

```dockerfile
VOLUME /data
VOLUME ["/data", "/logs"]
```

Declares mount points. Docker creates an anonymous volume for this path when the container starts (if no volume is mounted explicitly). Data written here persists after container removal IF you use `docker run -v`. Note: VOLUME prevents future RUN instructions from persisting changes to that path.

### USER

```dockerfile
# Create user first (in a RUN), then switch
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# Or use numeric IDs (more portable)
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 --ingroup nodejs nextjs
USER 1001

# In multi-stage builds, switch to root for operations, back to non-root at the end
USER root
RUN chmod +x /entrypoint.sh
USER appuser
```

Always run as non-root in production. If the container is compromised, non-root limits the blast radius.

### HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Python health check
HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Disable inherited healthcheck
HEALTHCHECK NONE
```

Options:
- `--interval` — time between checks (default 30s)
- `--timeout` — how long before a check times out (default 30s)
- `--start-period` — grace period before first check counts (default 0s)
- `--retries` — consecutive failures to mark unhealthy (default 3)

Exit codes: 0 = healthy, 1 = unhealthy. Orchestrators (Compose, Swarm, K8s) use this to restart unhealthy containers.

### LABEL

```dockerfile
LABEL maintainer="dhruv@example.com"
LABEL version="1.0.0"
LABEL org.opencontainers.image.title="My App"
LABEL org.opencontainers.image.description="AI service for X"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.created="2026-03-22"
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.revision="abc123"
```

Metadata only. No runtime effect. Use OCI standard labels for tooling compatibility. Query with `docker inspect --format='{{json .Config.Labels}}'`.

### SHELL

```dockerfile
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# After this, RUN commands use bash instead of sh
# Useful for bash-specific syntax in RUN
RUN echo "using bash"

# On Windows:
SHELL ["powershell", "-Command"]
```

Changes the default shell for `RUN`, `CMD`, `ENTRYPOINT` shell form instructions. Useful when you need bash features (`set -e`, `pipefail`, arrays) or on Windows.

### ONBUILD

```dockerfile
# In base image Dockerfile:
ONBUILD COPY . /app
ONBUILD RUN pip install -r requirements.txt

# When someone uses this as a base:
# FROM mybaseimage
# The ONBUILD instructions trigger automatically
```

Deferred instructions that execute when another image uses this image as its base. Useful for creating "template" base images for a specific language/framework. Rarely used in practice — prefer explicit Dockerfiles.

### STOPSIGNAL

```dockerfile
STOPSIGNAL SIGTERM    # Default
STOPSIGNAL SIGINT
STOPSIGNAL 15         # SIGTERM by numeric value
```

The signal sent to the container's main process when `docker stop` is called. After the stop timeout (default 10s), SIGKILL is sent regardless. Your app should handle SIGTERM for graceful shutdown.

### Complete Multi-Stage Dockerfile Example (Python FastAPI)

```dockerfile
# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12

# ── Stage 1: dependency builder ────────────────────────────────────────────
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /build

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cache pip downloads separately from code changes
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/install -r requirements.txt

# ── Stage 2: test runner ───────────────────────────────────────────────────
FROM python:${PYTHON_VERSION}-slim AS test

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

RUN python -m pytest tests/ -v

# ── Stage 3: production image ──────────────────────────────────────────────
FROM python:${PYTHON_VERSION}-slim AS production

LABEL org.opencontainers.image.title="FastAPI Service"
LABEL org.opencontainers.image.version="1.0.0"

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy only application code
COPY --chown=appuser:appgroup app/ ./app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

USER appuser

ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Docker CLI — All Important Commands

### Build

```bash
# Basic build
docker build -t myapp:1.0.0 .
docker build -t myapp:latest -f Dockerfile.prod .

# BuildKit (default since Engine 23.0)
DOCKER_BUILDKIT=1 docker build -t myapp .

# Build args
docker build --build-arg PYTHON_VERSION=3.11 --build-arg DEBUG=false -t myapp .

# Target specific stage
docker build --target builder -t myapp:builder .

# Multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .

# No cache
docker build --no-cache -t myapp .

# Cache from registry
docker build --cache-from myapp:cache -t myapp:latest .

# Output build progress
docker build --progress=plain -t myapp .

# Squash all layers (experimental)
docker build --squash -t myapp .
```

### Run

```bash
# Basic run
docker run myapp
docker run myapp python other_script.py   # Override CMD

# Detached + named
docker run -d --name api-server myapp

# Port mapping (host:container)
docker run -p 8080:8000 myapp               # Specific port
docker run -p 127.0.0.1:8080:8000 myapp    # Bind to localhost only
docker run -P myapp                          # Publish all EXPOSE'd ports

# Environment variables
docker run -e NODE_ENV=production myapp
docker run --env-file .env myapp

# Volumes
docker run -v /host/path:/container/path myapp      # Bind mount
docker run -v myvolume:/data myapp                  # Named volume
docker run --tmpfs /tmp myapp                        # tmpfs

# Resource limits
docker run --memory=512m --cpus=1.5 myapp

# Network
docker run --network mynetwork myapp
docker run --network host myapp               # Host networking

# Auto-remove on exit
docker run --rm myapp

# Interactive + TTY (for shells)
docker run -it ubuntu /bin/bash

# Read-only filesystem
docker run --read-only myapp

# User override
docker run --user 1001:1001 myapp

# Restart policy
docker run --restart=unless-stopped myapp

# Add capabilities / drop capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp

# GPU (NVIDIA)
docker run --gpus all nvidia/cuda:12.3-base nvidia-smi
docker run --gpus '"device=0,1"' myapp   # Specific GPUs
```

### Container Lifecycle

```bash
# List containers
docker ps                        # Running only
docker ps -a                     # All (including stopped)
docker ps -q                     # Just IDs (for scripting)
docker ps --filter status=exited # Filter by state

# Stop / Start / Restart
docker stop mycontainer                    # SIGTERM, then SIGKILL after 10s
docker stop -t 30 mycontainer              # 30s timeout
docker start mycontainer
docker restart mycontainer
docker restart -t 5 mycontainer

# Remove
docker rm mycontainer
docker rm -f mycontainer                   # Force remove running container
docker rm $(docker ps -aq)                 # Remove all stopped containers

# Kill
docker kill mycontainer                    # SIGKILL immediately
docker kill -s SIGUSR1 mycontainer         # Send custom signal

# Pause / Unpause (freeze with SIGSTOP)
docker pause mycontainer
docker unpause mycontainer
```

### Exec and Inspect

```bash
# Execute command in running container
docker exec mycontainer ls /app
docker exec -it mycontainer /bin/bash      # Interactive shell
docker exec -it mycontainer /bin/sh        # If no bash
docker exec -u root mycontainer bash       # As root even if non-root user set
docker exec -e DEBUG=true mycontainer env  # With extra env var

# Logs
docker logs mycontainer
docker logs -f mycontainer                 # Follow (tail -f equivalent)
docker logs --tail=100 mycontainer         # Last 100 lines
docker logs --since=1h mycontainer         # Last 1 hour
docker logs --timestamps mycontainer       # Include timestamps

# Inspect
docker inspect mycontainer                 # Full JSON metadata
docker inspect --format='{{.State.Status}}' mycontainer
docker inspect --format='{{json .NetworkSettings.Networks}}' mycontainer
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mycontainer

# Stats (real-time resource usage)
docker stats
docker stats mycontainer
docker stats --no-stream mycontainer       # One-shot snapshot

# Top (processes inside container)
docker top mycontainer
docker top mycontainer aux

# Copy files
docker cp mycontainer:/app/logs ./logs          # Container → host
docker cp ./config.json mycontainer:/app/       # Host → container

# Diff (what changed vs base image)
docker diff mycontainer
```

### Image Management

```bash
# List images
docker images
docker images -a                            # Include intermediate layers
docker image ls --filter dangling=true      # Untagged images

# Pull
docker pull python:3.12-slim
docker pull python:3.12-slim --platform linux/arm64

# Push
docker push myrepo/myapp:1.0.0

# Tag
docker tag myapp:latest myrepo/myapp:1.0.0
docker tag myapp:latest myrepo/myapp:latest

# Remove images
docker rmi myapp:1.0.0
docker rmi -f myapp:latest                 # Force (even if container using it)
docker image prune                         # Remove dangling images
docker image prune -a                      # Remove all unused images

# Build history (shows layers)
docker history myapp:latest
docker history --no-trunc myapp:latest

# Save / Load (for air-gapped transfers)
docker save myapp:latest | gzip > myapp.tar.gz
docker load < myapp.tar.gz

# Export / Import (single container FS — loses metadata)
docker export mycontainer | gzip > container.tar.gz
docker import container.tar.gz myapp:imported

# Commit (create image from container — avoid in production)
docker commit mycontainer mynewimage:v2
```

### Network Commands

```bash
docker network ls
docker network create mynetwork
docker network create --driver overlay --attachable mynetwork
docker network create --subnet=172.20.0.0/16 --ip-range=172.20.240.0/20 mynetwork
docker network inspect mynetwork
docker network connect mynetwork mycontainer
docker network disconnect mynetwork mycontainer
docker network rm mynetwork
docker network prune                       # Remove unused networks
```

### Volume Commands

```bash
docker volume ls
docker volume create myvolume
docker volume create --driver local myvolume
docker volume inspect myvolume
docker volume rm myvolume
docker volume prune                        # Remove unused volumes
```

### System Commands

```bash
# Disk usage breakdown
docker system df
docker system df -v                        # Verbose (per image/volume)

# Prune everything (careful in production)
docker system prune                        # Stopped containers + unused networks + dangling images
docker system prune -a                     # Also remove all unused images
docker system prune --volumes              # Also remove unused volumes
docker system prune -a --volumes           # Nuclear option (free max space)

# Events (real-time event stream)
docker events
docker events --filter event=die
docker events --since="2026-03-22T00:00:00"

# Version and info
docker version
docker info
docker info --format '{{json .}}' | jq .
```

---

## 5. Docker Compose v2

### Key Changes from v1

- `docker-compose` (Python binary with hyphen) → `docker compose` (Go plugin, space)
- `version:` field is **deprecated and ignored** (remove it from all files)
- Now implements the Compose Specification (merged v2 and v3 specs)
- Full CLI: `docker compose up/down/ps/logs/exec/run/build/pull/push/config/top/events`

### Minimal Example

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

volumes:
  pgdata:
```

### Services — Full Reference

```yaml
services:
  api:
    # Image source: build OR image (not both)
    build:
      context: .                           # Build context path
      dockerfile: Dockerfile.prod          # Custom Dockerfile name
      args:
        PYTHON_VERSION: "3.12"
      target: production                   # Multi-stage target
      cache_from:
        - myrepo/api:cache
      labels:
        com.example.env: production
      platforms:
        - linux/amd64
        - linux/arm64
    image: myrepo/api:1.0.0               # Tag built image with this name

    # Or pull existing image:
    # image: nginx:alpine

    container_name: api-server            # Fixed name (prevents scaling)
    hostname: api

    # Ports: "host:container" or just "container" (random host port)
    ports:
      - "8000:8000"
      - "127.0.0.1:9000:9000"            # Bind to localhost only
      - target: 8080
        published: 80
        protocol: tcp
        mode: host                        # Host mode (bypass ingress in Swarm)

    # Environment
    environment:
      NODE_ENV: production
      PORT: 8000
    env_file:
      - .env
      - .env.production

    # Volumes
    volumes:
      - ./app:/app:ro                     # Bind mount (read-only)
      - pgdata:/data                      # Named volume
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100m

    # Networks
    networks:
      - frontend
      - backend
    network_mode: host                    # Use host networking (or "none")

    # Dependencies
    depends_on:
      db:
        condition: service_healthy        # Wait for healthy (needs healthcheck)
      redis:
        condition: service_started        # Just wait for start (default)
      migrations:
        condition: service_completed_successfully  # Wait for exit 0

    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s

    # Restart policy
    restart: unless-stopped              # no | always | on-failure | unless-stopped

    # Resource limits (deploy section)
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback

    # Command and entrypoint overrides
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
    entrypoint: ["/bin/sh", "-c"]

    # User
    user: "1001:1001"

    # Read-only root FS with tmpfs for writable paths
    read_only: true
    tmpfs:
      - /tmp
      - /run

    # Labels
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.example.com`)"

    # Logging
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

    # Secrets (Docker Swarm secrets or file-based)
    secrets:
      - db_password
      - api_key

    # Profiles (only start this service when profile is active)
    profiles:
      - production

    # Extra hosts (add entries to /etc/hosts)
    extra_hosts:
      - "host.docker.internal:host-gateway"

    # Sysctls
    sysctls:
      net.core.somaxconn: 1024

    # Capabilities
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### Networks — Full Reference

```yaml
networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
    labels:
      env: production

  backend:
    driver: bridge
    internal: true              # No external internet access

  shared:
    external: true              # Use pre-existing network (not managed by Compose)
    name: my-existing-network

  overlay-net:
    driver: overlay             # For Swarm multi-host
    attachable: true            # Allow standalone containers to attach
```

### Volumes — Full Reference

```yaml
volumes:
  pgdata:                       # Named volume (managed by Docker)
    driver: local

  s3-storage:                   # External volume driver
    driver: rclone
    driver_opts:
      remote: s3:mybucket

  existing-vol:
    external: true              # Pre-existing volume, not managed by Compose
    name: my-existing-volume

  nfs-mount:
    driver: local
    driver_opts:
      type: nfs
      o: nfsvers=4,addr=192.168.1.1
      device: ":/exports/data"
```

### Secrets

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt   # File-based (for local dev)

  api_key:
    external: true                     # From Docker Swarm secrets
    name: prod_api_key
```

Secrets are mounted at `/run/secrets/<secret_name>` inside the container.

### Profiles

```yaml
services:
  api:
    image: myapp
    # No profiles = always starts

  db-admin:
    image: adminer
    profiles:
      - tools        # Only starts with: docker compose --profile tools up

  debug-tools:
    image: busybox
    profiles:
      - debug
```

```bash
docker compose --profile tools up
docker compose --profile debug --profile tools up  # Multiple profiles
```

### Compose CLI Commands

```bash
# Up/Down
docker compose up                          # Start all services (foreground)
docker compose up -d                       # Detached
docker compose up --build                  # Always rebuild images
docker compose up --force-recreate         # Recreate containers even if config unchanged
docker compose up api db                   # Start specific services only
docker compose down                        # Stop and remove containers + networks
docker compose down -v                     # Also remove volumes
docker compose down --rmi all              # Also remove images

# Status
docker compose ps
docker compose ps -a                       # Include stopped

# Logs
docker compose logs
docker compose logs -f api                 # Follow specific service
docker compose logs --tail=50 api db

# Exec / Run
docker compose exec api bash              # Exec in running container
docker compose run --rm api python manage.py migrate   # Run one-off command

# Build
docker compose build
docker compose build --no-cache api
docker compose build --push              # Build and push to registry

# Scale
docker compose up -d --scale api=3      # Run 3 replicas (no fixed container_name)

# Config validation
docker compose config                    # Validate and print merged config
docker compose config --quiet            # Just validate (no output)

# Pull / Push
docker compose pull
docker compose push
```

### Override Files Pattern

```bash
# docker-compose.yml          ← base (always loaded)
# docker-compose.override.yml ← auto-merged in dev
# docker-compose.prod.yml     ← explicit: docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

`docker-compose.override.yml` is loaded automatically if present. Use it to add dev-only settings (volume mounts, debug ports) without modifying the base file.

---

## 6. Networking

### Network Driver Summary

| Driver  | Scope  | Use Case                                      |
|---------|--------|-----------------------------------------------|
| bridge  | Local  | Default. Single-host container communication. |
| host    | Local  | Max performance. Container shares host's NIC. |
| overlay | Swarm  | Multi-host communication (Swarm/K8s).         |
| macvlan | Local  | Container needs a real IP on your LAN.        |
| ipvlan  | Local  | Like macvlan but shares MAC (layer 3).        |
| none    | Local  | No networking. Fully isolated.                |

### Bridge Networks

```bash
# Default bridge (docker0)
# Containers communicate by IP only — no DNS
# Avoid for production; use user-defined bridge

# User-defined bridge (recommended)
docker network create myapp-network
docker run --network myapp-network --name api myapi
docker run --network myapp-network --name db postgres

# DNS resolution: containers reach each other by service name
# api container can reach db at hostname "db"

# Inspect
docker network inspect myapp-network
```

### Host Networking

```bash
docker run --network host myapp
# Container uses host's network stack directly
# Port mapping is unnecessary (-p flags are ignored)
# Highest performance (no NAT overhead)
# No network isolation — container can see all host interfaces
# Only works on Linux (not Docker Desktop on macOS/Windows)
```

### Overlay (Multi-host / Swarm)

```bash
# Requires Swarm mode
docker swarm init
docker network create --driver overlay --attachable myoverlay

# All containers on any Swarm node can communicate through overlay
# Uses VXLAN encapsulation
# Built-in load balancing (VIP or DNSRR mode)
```

### Macvlan

```bash
docker network create \
  --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  --opt parent=eth0 \
  mymacvlan

docker run --network mymacvlan --ip 192.168.1.100 myapp
# Container appears as a separate device on your LAN
# Cannot communicate with the host (kernel restriction)
```

### Port Mapping

```bash
# -p host_port:container_port
docker run -p 8080:80 nginx             # All interfaces → port 80
docker run -p 127.0.0.1:8080:80 nginx  # Localhost only (more secure)
docker run -p 8080:80/udp nginx         # UDP

# -P publishes all EXPOSE'd ports to random high ports
docker run -P nginx
docker port nginx_container             # See the actual port mappings
```

### DNS in Docker

User-defined networks get Docker's embedded DNS at `127.0.0.11`. This:
- Resolves container names to their IPs
- Supports service aliases
- Forwards external DNS to host-configured resolvers
- Container names, service names (in Compose), and custom aliases all work

```yaml
services:
  api:
    networks:
      backend:
        aliases:
          - api-service      # Alternative hostname on the network
```

---

## 7. Volumes and Storage

### Decision Matrix

| Need | Solution |
|------|----------|
| Persist database data | Named volume |
| Live-reload code in dev | Bind mount |
| Temporary scratch space | tmpfs |
| Share data between containers | Named volume |
| Access host files/devices | Bind mount |
| Sensitive data not persisted to disk | tmpfs |
| Production app code | Bake into image (don't mount) |

### Named Volumes

```bash
# Create
docker volume create pgdata

# Use
docker run -v pgdata:/var/lib/postgresql/data postgres

# Inspect (find actual host path)
docker volume inspect pgdata
# Location on Linux: /var/lib/docker/volumes/pgdata/_data
# On Docker Desktop (macOS/Windows): inside the Linux VM

# Backup a volume
docker run --rm \
  -v pgdata:/data:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/pgdata_backup.tar.gz /data

# Restore
docker run --rm \
  -v pgdata:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/pgdata_backup.tar.gz -C /
```

### Bind Mounts

```bash
# Absolute path required
docker run -v /absolute/host/path:/container/path myapp

# Read-only bind mount
docker run -v /config:/config:ro myapp

# With SELinux label (on SELinux systems)
docker run -v /data:/data:z myapp     # :z = shared label
docker run -v /data:/data:Z myapp     # :Z = private label
```

### tmpfs

```bash
docker run --tmpfs /tmp myapp
docker run --tmpfs /tmp:rw,size=100m,mode=1777 myapp

# In Compose:
services:
  api:
    tmpfs:
      - /tmp
      - /run
```

### Volume Drivers

```bash
# NFS volume
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=nfsvers=4,addr=192.168.1.10 \
  --opt device=:/exports/data \
  nfs-data

# Third-party drivers: rexray (AWS EBS/EFS), convoy, portworx, etc.
```

---

## 8. Docker for AI/ML

### NVIDIA GPU Support

**Setup (Linux host):**

```bash
# 1. Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit

# 2. Configure Docker daemon
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 3. Test
docker run --rm --gpus all nvidia/cuda:12.3.1-base-ubuntu22.04 nvidia-smi
```

**Run with GPU:**

```bash
docker run --gpus all myml-app              # All GPUs
docker run --gpus 1 myml-app               # First GPU only
docker run --gpus '"device=0,2"' myml-app  # GPUs 0 and 2
docker run --gpus '"device=GPU-3a23c669"' myml-app  # By UUID
```

**Dockerfile for GPU workloads:**

```dockerfile
# Use NVIDIA base images from NGC (https://catalog.ngc.nvidia.com)
FROM nvcr.io/nvidia/pytorch:24.01-py3

# Or CUDA base
FROM nvidia/cuda:12.3.1-cudnn9-runtime-ubuntu22.04

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Docker Compose with GPU:**

```yaml
services:
  ml-trainer:
    image: myml-app:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all        # or specific count: 1
              capabilities: [gpu]
```

### Model Serving

```dockerfile
# FastAPI + vLLM model server
FROM python:3.12-slim

RUN pip install vllm fastapi uvicorn

WORKDIR /app
COPY serve.py .

# Mount model at runtime (don't bake large models into image)
VOLUME /models

ENV MODEL_PATH=/models/llama-3-8b

HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "serve.py"]
```

```yaml
# docker-compose.yml for model server
services:
  vllm:
    image: vllm/vllm-openai:latest
    command: --model /models/llama-3-8b --host 0.0.0.0 --port 8000
    volumes:
      - /data/models:/models          # Mount model from host
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    ports:
      - "8000:8000"
```

### Jupyter in Docker

```dockerfile
FROM jupyter/pytorch-notebook:latest

USER root
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
USER $NB_UID

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /home/jovyan/work
```

```bash
docker run -p 8888:8888 \
  -v $(pwd)/notebooks:/home/jovyan/work \
  --gpus all \
  jupyter/pytorch-notebook
```

### Python ML Project .dockerignore

```
# .dockerignore for ML projects
.git
.gitignore
*.md
*.pyc
__pycache__
.pytest_cache
.mypy_cache
.venv
venv
env
*.egg-info
dist
build

# Large data files (mount these as volumes)
data/raw/
data/processed/
*.csv
*.parquet
*.h5
*.hdf5

# Trained model weights (large)
models/
checkpoints/
*.pt
*.pth
*.onnx
*.pkl
*.bin

# Jupyter checkpoints
.ipynb_checkpoints/

# Logs
logs/
*.log
mlruns/
wandb/

# Secrets
.env
*.pem
*.key
secrets/
```

### Multi-Stage for Python (optimized)

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

FROM base AS builder
RUN pip install uv
WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r pyproject.toml

FROM base AS production
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src/ ./src/

RUN groupadd -r app && useradd -r -g app app
USER app

CMD ["python", "-m", "src.main"]
```

---

## 9. Security

### User Namespaces (Rootless Mode)

```bash
# Run Docker daemon in rootless mode (most secure)
dockerd-rootless-setuptool.sh install

# Even without rootless daemon — always use USER in Dockerfile
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --ingroup app app
USER 1001
```

**Never run application containers as root.** If a process escapes the container, it should not be root on the host.

### Secrets Management

```bash
# WRONG — secrets in ENV are visible in docker inspect and logs
docker run -e DB_PASSWORD=mysecret myapp

# WRONG — secrets baked into image
# ENV DB_PASSWORD=mysecret  ← in Dockerfile

# RIGHT — Docker secrets (Swarm) — mounted as files, not env vars
docker secret create db_password ./password.txt
# In Swarm service: --secret db_password
# Mounted at /run/secrets/db_password

# RIGHT — Pass at runtime from environment (dev/local only)
DB_PASSWORD=$(cat /secure/location/password) docker run -e DB_PASSWORD myapp

# RIGHT — Secret mount at build time (not in final image)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install
```

### Capabilities

```bash
# Drop all capabilities, add only what's needed
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp

# Common capabilities:
# NET_BIND_SERVICE — bind to ports < 1024
# CHOWN            — change file ownership
# SETUID / SETGID  — change process UID/GID
# SYS_ADMIN        — many admin ops (dangerous — avoid)
# KILL             — send signals to processes

# In Compose:
services:
  api:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### Read-Only Filesystem

```bash
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/run \
  myapp

# In Compose:
services:
  api:
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

### Seccomp and AppArmor

```bash
# Seccomp — filter system calls
docker run --security-opt seccomp=./seccomp-profile.json myapp
docker run --security-opt seccomp=unconfined myapp  # Disable (not recommended)

# AppArmor (Linux only)
docker run --security-opt apparmor=docker-default myapp
docker run --security-opt apparmor=unconfined myapp   # Disable

# No new privileges (prevents privilege escalation inside container)
docker run --security-opt no-new-privileges myapp
```

### Image Scanning with Trivy

```bash
# Install Trivy
brew install aquasecurity/trivy/trivy

# Scan image for vulnerabilities
trivy image myapp:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL myapp:latest

# Scan and fail CI on critical vulns
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Scan filesystem
trivy fs /path/to/project

# Generate SBOM
trivy image --format spdx-json --output sbom.json myapp:latest

# Scan Dockerfile for misconfigurations
trivy config ./Dockerfile
trivy config ./docker-compose.yml
```

### CI/CD Security Pipeline

```yaml
# .github/workflows/security.yml
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .

- name: Scan with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH
    exit-code: '1'

- name: Upload results to GitHub Security
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: trivy-results.sarif
```

### Security Checklist

- [ ] Base image from official source
- [ ] No `latest` tag in production
- [ ] `USER` set to non-root
- [ ] `--cap-drop=ALL` + add only needed caps
- [ ] `--read-only` with tmpfs for writable paths
- [ ] `--security-opt no-new-privileges`
- [ ] No secrets in `ENV` or image layers
- [ ] Trivy scan in CI pipeline
- [ ] Multi-stage build (no build tools in production)
- [ ] `.dockerignore` excludes secrets and `.env` files
- [ ] Resource limits (`--memory`, `--cpus`)

---

## 10. Optimization

### Layer Caching Strategy

Docker rebuilds a layer only if its inputs have changed. Order instructions from **least to most frequently changed**:

```dockerfile
# WRONG — code changes invalidate pip install cache
COPY . /app
RUN pip install -r requirements.txt

# RIGHT — pip install cached unless requirements.txt changes
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app          # Only this layer re-runs on code changes
```

### BuildKit Cache Mounts

Cache package manager downloads without including them in the image:

```dockerfile
# Python / pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Node.js / npm
RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline

# Rust / cargo
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release

# Go modules
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

### Image Size Comparison

| Base Image | Size | Use Case |
|------------|------|----------|
| `ubuntu:24.04` | ~78MB | When you need apt and full GNU utils |
| `debian:bookworm-slim` | ~74MB | Default Python/Node base |
| `python:3.12-slim` | ~130MB | Standard Python apps |
| `python:3.12-alpine` | ~55MB | Size-critical Python (musl libc) |
| `node:20-alpine` | ~135MB | Node.js apps |
| `gcr.io/distroless/python3` | ~51MB | Production Python (no shell) |
| `gcr.io/distroless/nodejs20` | ~110MB | Production Node.js |
| `scratch` | 0MB | Compiled binaries (Go, Rust) |

### Alpine vs Debian vs Distroless

**Alpine:**
- Smallest general-purpose base
- Uses musl libc (not glibc) — some C extensions break or behave differently
- Has a shell (ash) + apk package manager
- Good for: size-sensitive apps where Alpine's musl is compatible

**Debian slim:**
- Uses glibc (full compatibility)
- Has bash + apt
- Good for: apps with native C extensions (numpy, Pillow, etc.)

**Distroless:**
- No shell, no package manager, no debugging tools
- Contains only language runtime + app
- Cannot `docker exec` a shell into it (use debug images: `gcr.io/distroless/python3:debug`)
- Good for: maximum security + minimum attack surface in production

### BuildKit Multi-Platform Builds

```bash
# Create and use a multi-platform builder
docker buildx create --name mybuilder --driver docker-container --bootstrap
docker buildx use mybuilder

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t myrepo/myapp:latest \
  --push \
  .

# Build with GitHub Actions cache
docker buildx build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  --platform linux/amd64,linux/arm64 \
  -t myrepo/myapp:${{ github.sha }} \
  --push \
  .
```

### .dockerignore

Critical for: (1) small build context → faster builds, (2) no secrets in image

```
# .dockerignore
.git
.gitignore
.github
.dockerignore
Dockerfile
docker-compose*.yml

# Dependencies (will be installed in Docker)
node_modules
.venv
venv
__pycache__
*.pyc
*.pyo

# Build artifacts
dist
build
*.egg-info
.eggs

# Test and coverage
.pytest_cache
.mypy_cache
.coverage
htmlcov
.tox

# IDE
.idea
.vscode
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.*
*.pem
*.key
*.cert
secrets/

# Logs
*.log
logs/

# Docs
docs/
*.md
```

### Image Reduction Techniques

```dockerfile
# 1. Combine RUN commands
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl wget git && \
    rm -rf /var/lib/apt/lists/*    # Must be in SAME RUN

# 2. Use --no-install-recommends
RUN apt-get install -y --no-install-recommends curl

# 3. Remove apt cache in same layer
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 4. Use pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt
# OR set in ENV (affects all subsequent pip calls)
ENV PIP_NO_CACHE_DIR=1

# 5. npm ci instead of npm install (respects lockfile, no audit writes)
RUN npm ci --only=production

# 6. Use COPY --link for better caching
COPY --link requirements.txt /app/
```

---

## 11. Registry

### Docker Hub

```bash
docker login                          # Login to Docker Hub
docker login -u myuser docker.io      # Explicit

docker pull python:3.12-slim          # Public image (no auth needed)
docker push myuser/myapp:1.0.0        # Requires auth + must own myuser org

# Rate limits (unauthenticated): 100 pulls/6hr
# Rate limits (authenticated free): 200 pulls/6hr
# Pro/Team plans: unlimited pulls
```

### Amazon ECR

```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name myapp --region us-east-1

# Push
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# Pull
docker pull 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# Enable scan on push
aws ecr put-image-scanning-configuration \
  --repository-name myapp \
  --image-scanning-configuration scanOnPush=true

# Enable tag immutability
aws ecr put-image-tag-mutability \
  --repository-name myapp \
  --image-tag-mutability IMMUTABLE
```

### Google Artifact Registry (GCR successor)

```bash
# Auth
gcloud auth configure-docker us-central1-docker.pkg.dev

# Push
docker tag myapp:latest us-central1-docker.pkg.dev/my-project/my-repo/myapp:latest
docker push us-central1-docker.pkg.dev/my-project/my-repo/myapp:latest
```

### Azure Container Registry (ACR)

```bash
# Auth
az acr login --name myregistry

# Push
docker tag myapp:latest myregistry.azurecr.io/myapp:latest
docker push myregistry.azurecr.io/myapp:latest
```

### Self-Hosted Registry

```bash
# Run private registry
docker run -d \
  -p 5000:5000 \
  --name registry \
  -v /data/registry:/var/lib/registry \
  registry:2

# With TLS
docker run -d \
  -p 443:443 \
  -v /certs:/certs \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:2

# Push to self-hosted
docker tag myapp localhost:5000/myapp:1.0.0
docker push localhost:5000/myapp:1.0.0
```

### Image Tagging Strategy (Production)

```
myrepo/myapp:2.1.3           ← Specific version (immutable — never changes)
myrepo/myapp:2.1             ← Minor version (moves to 2.1.4 on patch)
myrepo/myapp:2               ← Major version (moves on any 2.x release)
myrepo/myapp:latest          ← Latest stable (avoid in production deployments)
myrepo/myapp:sha-abc1234     ← Git SHA (most precise, great for CD)
myrepo/myapp:main-20260322   ← Branch + date (useful for staging)
```

**Production rule:** Never deploy `latest`. Always deploy a specific, immutable tag (semver or git SHA).

---

## 12. Orchestration Intro

### Docker Swarm

```bash
# Initialize Swarm (on manager node)
docker swarm init --advertise-addr 192.168.1.10

# Get join token for workers
docker swarm join-token worker
docker swarm join-token manager

# Create a service (replicated across nodes)
docker service create \
  --name api \
  --replicas 3 \
  --publish published=80,target=8000 \
  --update-delay 10s \
  --update-failure-action rollback \
  myapp:1.0.0

# List services
docker service ls
docker service ps api           # Where replicas are running

# Scale
docker service scale api=5

# Rolling update
docker service update --image myapp:1.1.0 api

# Stack deploy (uses docker-compose.yml)
docker stack deploy -c docker-compose.yml mystack
docker stack ls
docker stack services mystack
docker stack rm mystack
```

### Docker Swarm vs Kubernetes

| Dimension | Docker Swarm | Kubernetes |
|-----------|-------------|------------|
| Complexity | Low | High |
| Setup time | Minutes | Hours/days |
| Learning curve | Gentle | Steep |
| Scaling | Moderate | Massive (1000s of nodes) |
| Auto-scaling | Manual only | HPA/VPA/KEDA |
| Self-healing | Basic | Advanced |
| Config maps/secrets | Yes | Yes (more powerful) |
| RBAC | Basic | Fine-grained |
| Storage | Simple | Complex (CSI drivers) |
| Networking | Simple (overlay) | Complex (CNI plugins) |
| Ecosystem | Small | Huge (CNCF) |
| Production support | Through 2030 (Mirantis) | Dominant |

**Choose Swarm when:** Small team, simple workloads, tight deadline, already know Docker.
**Choose Kubernetes when:** Large scale, complex networking, advanced autoscaling, enterprise requirements, growing team.

### Quick K8s Comparison

```yaml
# Compose service
services:
  api:
    image: myapp:1.0.0
    deploy:
      replicas: 3

# Kubernetes equivalent
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: myapp:1.0.0
```

---

## 12.5 Kubernetes Deep Reference

### Why Kubernetes? (The Multi-Machine Problem)

Docker handles containers on **one machine**. But when your app is heavy (e.g., LLM hosting) and expects massive traffic:

```
                    ┌──── Machine 1 (Worker Node) ──── [Pods]
                    │
Traffic ──→ Master Node ──── Machine 2 (Worker Node) ──── [Pods]
            (Control Plane)  │
                    ├──── Machine 3 (Worker Node) ──── [Pods]
                    │
                    └──── Machine 4 (Worker Node) ──── [Pods]
```

The **Master Node (Control Plane)** decides which worker machine gets the traffic based on availability, resource usage, and health. Your customer never faces downtime.

### K8s Architecture

| Component | Role |
|-----------|------|
| **Control Plane (Master)** | Brain — schedules, monitors, decides |
| **kube-apiserver** | Front door — all communication goes through here |
| **etcd** | Key-value store — cluster state database |
| **kube-scheduler** | Decides which node runs a new pod |
| **kube-controller-manager** | Ensures desired state = actual state |
| **Worker Nodes** | Machines that actually run your containers |
| **kubelet** | Agent on each worker — talks to control plane |
| **kube-proxy** | Networking — routes traffic to correct pods |
| **Pod** | Smallest unit — one or more containers together |

### Core Objects

```yaml
# 1. POD — smallest deployable unit
apiVersion: v1
kind: Pod
metadata:
  name: llm-server
spec:
  containers:
    - name: llm
      image: mycompany/llm-server:1.0
      ports:
        - containerPort: 8000
      resources:
        requests:
          memory: "4Gi"
          cpu: "2"
          nvidia.com/gpu: 1
        limits:
          memory: "8Gi"
          cpu: "4"
          nvidia.com/gpu: 1
```

```yaml
# 2. DEPLOYMENT — manages replicas + rolling updates
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-server
spec:
  replicas: 4                    # Run on 4 machines
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0          # Zero downtime
  selector:
    matchLabels:
      app: llm-server
  template:
    metadata:
      labels:
        app: llm-server
    spec:
      containers:
        - name: llm
          image: mycompany/llm-server:1.0
          ports:
            - containerPort: 8000
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 60
            periodSeconds: 30
```

```yaml
# 3. SERVICE — load balancer / traffic router
apiVersion: v1
kind: Service
metadata:
  name: llm-service
spec:
  type: LoadBalancer            # Exposes externally
  selector:
    app: llm-server
  ports:
    - port: 80
      targetPort: 8000
---
# Service types:
# ClusterIP   — internal only (default)
# NodePort    — expose on each node's IP:port
# LoadBalancer — cloud provider LB (AWS ALB, GCP LB)
# ExternalName — DNS alias
```

```yaml
# 4. INGRESS — HTTP routing (like nginx reverse proxy)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: llm-ingress
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
spec:
  rules:
    - host: llm.mycompany.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: llm-service
                port:
                  number: 80
```

```yaml
# 5. HORIZONTAL POD AUTOSCALER — auto-scale based on load
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

```yaml
# 6. CONFIGMAP & SECRET
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-config
data:
  MODEL_NAME: "llama-3-70b"
  MAX_TOKENS: "4096"
  TEMPERATURE: "0.7"
---
apiVersion: v1
kind: Secret
metadata:
  name: llm-secrets
type: Opaque
stringData:
  API_KEY: "sk-..."
  DB_PASSWORD: "supersecret"
```

```yaml
# 7. PERSISTENT VOLUME — storage for model weights
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-storage
spec:
  accessModes:
    - ReadOnlyMany              # Multiple pods read same model
  resources:
    requests:
      storage: 100Gi
  storageClassName: gp3
```

```yaml
# 8. NAMESPACE — isolate environments
apiVersion: v1
kind: Namespace
metadata:
  name: ml-production
```

### Essential kubectl Commands

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl top nodes                        # Resource usage per node

# Deployments
kubectl apply -f deployment.yaml         # Create/update
kubectl get deployments
kubectl rollout status deployment/llm-server
kubectl rollout undo deployment/llm-server  # Rollback
kubectl scale deployment/llm-server --replicas=6

# Pods
kubectl get pods -o wide                 # Show which node each pod runs on
kubectl describe pod <pod-name>          # Detailed info + events
kubectl logs <pod-name> -f               # Stream logs
kubectl exec -it <pod-name> -- bash      # Shell into pod
kubectl top pods                         # CPU/memory per pod

# Services
kubectl get svc
kubectl describe svc llm-service
kubectl port-forward svc/llm-service 8080:80  # Local access

# Debug
kubectl get events --sort-by='.lastTimestamp'
kubectl get pods --field-selector=status.phase=Failed
kubectl describe node <node-name>        # Check node capacity

# Namespaces
kubectl get all -n ml-production
kubectl config set-context --current --namespace=ml-production
```

### LLM Hosting on K8s — Real Pattern

```
Internet → Ingress (nginx) → Service (LoadBalancer)
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
         Node 1 (GPU)       Node 2 (GPU)       Node 3 (GPU)
         [Pod: vLLM]        [Pod: vLLM]        [Pod: vLLM]
         Llama-3-70B        Llama-3-70B        Llama-3-70B
              │                   │                   │
              └───────── Shared PVC (model weights) ──┘
```

- **kube-scheduler** picks node with available GPU
- **Service** load-balances across healthy pods
- **HPA** scales pods up/down based on request queue depth
- **PVC** shares model weights (download once, mount everywhere)
- **Readiness probe** ensures traffic only goes to loaded models

### Managed K8s Services

| Provider | Service | GPU Support |
|----------|---------|------------|
| AWS | EKS | p4d, p5, g5 instances |
| GCP | GKE | A100, H100, TPUs |
| Azure | AKS | NC, ND series |
| Local | minikube, kind, k3s | Limited |

### Docker Compose → Kubernetes Cheat Sheet

| Docker Compose | Kubernetes |
|---------------|------------|
| `services:` | Deployment + Service |
| `replicas:` | `spec.replicas` |
| `ports:` | Service (NodePort/LoadBalancer) |
| `volumes:` | PersistentVolumeClaim |
| `environment:` | ConfigMap / Secret |
| `depends_on:` | Init containers / readiness probes |
| `restart: always` | `restartPolicy: Always` (default) |
| `docker-compose up` | `kubectl apply -f` |
| `docker-compose down` | `kubectl delete -f` |

---

## 13. Common Patterns

### Sidecar Pattern

A second container runs alongside the main container in the same pod/task, sharing network and volumes:

```yaml
# docker-compose.yml — logging sidecar
services:
  api:
    image: myapp
    volumes:
      - logs:/var/log/app

  log-shipper:
    image: fluent/fluent-bit
    volumes:
      - logs:/var/log/app:ro           # Read logs written by api
      - ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
    depends_on:
      - api

volumes:
  logs:
```

Use cases: log shippers, service mesh proxies (Envoy/Linkerd), TLS termination, metrics collectors.

### Init Container Pattern

A container that runs to completion before the main container starts:

```yaml
services:
  db-migrate:
    image: myapp
    command: python manage.py migrate
    environment:
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy

  api:
    image: myapp
    depends_on:
      db-migrate:
        condition: service_completed_successfully   # Wait for migration
      db:
        condition: service_healthy
```

Use cases: database migrations, schema setup, config file generation, waiting for external dependencies.

### Ambassador Pattern

A proxy container that simplifies access to an external service:

```yaml
services:
  api:
    image: myapp
    environment:
      REDIS_URL: redis://redis-ambassador:6379

  redis-ambassador:
    image: haproxy
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    # Proxies to external Redis cluster with retry logic, auth, etc.
```

Use cases: connecting to cloud databases with connection pooling, legacy service adapters, circuit breakers.

### Adapter Pattern

Transforms output of the main container to fit a consumer's expectations:

```yaml
services:
  legacy-app:
    image: my-legacy-app            # Outputs XML logs

  log-adapter:
    image: xml-to-json-converter    # Reads XML, emits JSON
    volumes:
      - logs:/logs
    # Converts to format Elasticsearch expects
```

### One-Off Task Pattern

```yaml
services:
  api:
    image: myapp

  # Run once then exit — NOT a long-running service
  seed-db:
    image: myapp
    command: python seed.py
    profiles:
      - seed                       # Only run explicitly: docker compose --profile seed up
    depends_on:
      db:
        condition: service_healthy
```

```bash
docker compose run --rm api python manage.py shell     # Interactive one-off
docker compose run --rm api python scripts/seed_data.py
```

---

## 14. Debugging

### Container Logs

```bash
# Basic
docker logs mycontainer

# Follow in real time
docker logs -f mycontainer

# Last N lines
docker logs --tail=200 mycontainer

# Since timestamp
docker logs --since=2026-03-22T10:00:00 mycontainer
docker logs --since=30m mycontainer         # Since 30 minutes ago

# With timestamps
docker logs -t mycontainer

# With Compose
docker compose logs -f api db              # Follow multiple services
```

### Exec Into Container

```bash
# Get a shell (if shell exists)
docker exec -it mycontainer /bin/bash
docker exec -it mycontainer /bin/sh         # Alpine/distroless often only has sh

# Run as root (debug only)
docker exec -it -u root mycontainer bash

# Debug distroless (no shell) — use debug variant or copy tools in
# Option 1: Use debug image
# FROM gcr.io/distroless/python3:debug

# Option 2: nsenter to enter container's namespaces from host
PID=$(docker inspect --format '{{.State.Pid}}' mycontainer)
nsenter -t $PID -m -u -i -n -p -- /bin/bash

# Option 3: Docker 23+ debug feature
docker debug mycontainer    # Attaches ephemeral shell without modifying container
```

### Inspect

```bash
# Full metadata (JSON)
docker inspect mycontainer
docker inspect myimage

# Specific fields with Go templates
docker inspect --format='{{.State.Status}}' mycontainer
docker inspect --format='{{.State.ExitCode}}' mycontainer
docker inspect --format='{{.Config.Env}}' mycontainer
docker inspect --format='{{json .NetworkSettings.Ports}}' mycontainer | jq
docker inspect --format='{{range .Mounts}}{{.Source}} → {{.Destination}}{{"\n"}}{{end}}' mycontainer

# Compare image vs running config
docker inspect --format='{{json .Config}}' mycontainer | jq
```

### Docker Events

```bash
# Real-time event stream
docker events

# Filter by type
docker events --filter type=container
docker events --filter event=die
docker events --filter event=oom         # Out-of-memory kills

# Historical
docker events --since=1h
docker events --since=2026-03-22T00:00:00 --until=2026-03-22T12:00:00
```

### Healthcheck Debugging

```bash
# Check current health status
docker inspect --format='{{json .State.Health}}' mycontainer | jq

# Shows last N health check results:
# {
#   "Status": "healthy",
#   "FailingStreak": 0,
#   "Log": [
#     {
#       "Start": "2026-03-22T10:00:00Z",
#       "End": "2026-03-22T10:00:01Z",
#       "ExitCode": 0,
#       "Output": ""
#     }
#   ]
# }

# Override healthcheck for debugging (disable it)
docker run --no-healthcheck myapp

# Run the healthcheck command manually inside the container
docker exec mycontainer curl -f http://localhost:8000/health
```

### Resource Debugging

```bash
# Real-time CPU/memory stats
docker stats
docker stats mycontainer

# Process list inside container
docker top mycontainer

# Check OOM kills
docker events --filter event=oom

# Check resource limits
docker inspect --format='{{json .HostConfig}}' mycontainer | jq '{
  memory: .Memory,
  cpus: .NanoCpus,
  cpuShares: .CpuShares
}'
```

### Network Debugging

```bash
# Test connectivity between containers
docker exec api ping db
docker exec api curl http://db:5432
docker exec api nslookup db            # DNS resolution test

# List container's network info
docker exec mycontainer ip addr
docker exec mycontainer netstat -tlnp

# Check what ports are mapped
docker port mycontainer

# Inspect network
docker network inspect mynetwork

# Capture network traffic (for deep debugging)
docker run --rm \
  --net=container:mycontainer \
  nicolaka/netshoot \
  tcpdump -i eth0 -w /dev/stdout
```

### Image Layer Analysis

```bash
# Show layers and commands
docker history myapp:latest
docker history --no-trunc myapp:latest

# Dive (third-party tool for deep layer analysis)
brew install dive
dive myapp:latest    # Interactive layer explorer showing efficiency score
```

---

## 15. Production Checklist

### Image Build

- [ ] `# syntax=docker/dockerfile:1` at top of Dockerfile (enables latest BuildKit)
- [ ] Base image is official, minimal, and pinned by digest (`@sha256:...`)
- [ ] Multi-stage build — build tools NOT in production image
- [ ] `.dockerignore` exists and excludes `.git`, `*.env`, `node_modules`, test files
- [ ] `COPY requirements.txt` before `COPY .` (layer cache optimization)
- [ ] `--mount=type=cache` for package managers (faster builds)
- [ ] `--no-install-recommends` on apt installs
- [ ] `rm -rf /var/lib/apt/lists/*` in same `RUN` as apt install
- [ ] Image scanned with Trivy (no CRITICAL vulnerabilities)
- [ ] Image size is reasonable (use `docker history` to investigate fat layers)

### Container Configuration

- [ ] `USER` is non-root (never run as root in production)
- [ ] `HEALTHCHECK` defined and tested
- [ ] Resource limits set (`--memory`, `--cpus` or Compose `deploy.resources`)
- [ ] Restart policy set (`restart: unless-stopped` or similar)
- [ ] Secrets passed via environment at runtime or Docker Secrets — NEVER baked in
- [ ] `--read-only` with `tmpfs` for writable paths (if app supports it)
- [ ] `--cap-drop=ALL` + only needed capabilities added back
- [ ] `--security-opt no-new-privileges`
- [ ] Ports bound to `127.0.0.1` if not public-facing (`-p 127.0.0.1:8080:8080`)

### Networking

- [ ] User-defined bridge network (not default `docker0`)
- [ ] Internal services on `internal: true` network (no external access)
- [ ] Services communicate by name (not hardcoded IP)
- [ ] TLS between services in production (or mTLS via service mesh)

### Data and Storage

- [ ] Databases use named volumes (not bind mounts in production)
- [ ] Volume backup strategy defined and tested
- [ ] Logs go to stdout/stderr (not files inside container) — let the runtime collect them
- [ ] Sensitive data in `tmpfs` (never persisted to disk)

### Observability

- [ ] Structured JSON logging (not plain text)
- [ ] Log driver configured (`json-file` with `max-size` + `max-file` limits)
- [ ] Health endpoint (`/health` or `/healthz`) returns useful status
- [ ] Metrics endpoint (Prometheus `/metrics`) if using Prometheus
- [ ] Tracing configured (OpenTelemetry)

### CI/CD

- [ ] Image built and tagged with git SHA in CI
- [ ] Trivy scan fails the pipeline on CRITICAL/HIGH vulnerabilities
- [ ] Docker image pushed to private registry (not Docker Hub free tier)
- [ ] Deployment uses specific immutable tag (never `latest`)
- [ ] Rollback procedure tested (previous image tag available)

### Operational

- [ ] Containers handle SIGTERM gracefully (shutdown within grace period)
- [ ] `STOPSIGNAL` set correctly for your runtime
- [ ] `stop_grace_period` in Compose set appropriately (> app shutdown time)
- [ ] `docker system prune` scheduled (clean up old images/stopped containers)
- [ ] Registry lifecycle policies configured (delete old untagged images)
- [ ] `ulimits` set if app needs high file descriptor limits
- [ ] Time zone configured (`TZ` env var or `/etc/localtime` bind mount)

### Example Production Compose

```yaml
services:
  api:
    image: myrepo/api:${GIT_SHA}      # Never latest
    restart: unless-stopped
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    environment:
      NODE_ENV: production
      PORT: "8000"
    env_file:
      - .env.production
    networks:
      - frontend
      - backend
    ports:
      - "127.0.0.1:8000:8000"         # Localhost only — Nginx proxy in front
    volumes:
      - /var/run:/var/run:ro           # If needed for Unix sockets
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER_FILE: /run/secrets/db_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - backend
    deploy:
      resources:
        limits:
          memory: 1G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    secrets:
      - db_user
      - db_password
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true                    # No internet access for DB network

volumes:
  pgdata:

secrets:
  db_user:
    file: ./secrets/db_user.txt
  db_password:
    file: ./secrets/db_password.txt
```

---

## Quick Reference Card

```bash
# Build
docker build -t myapp:1.0.0 .
docker buildx build --platform linux/amd64,linux/arm64 -t myapp --push .

# Run
docker run -d --name api -p 8080:8000 --restart=unless-stopped myapp:1.0.0
docker run --rm -it myapp /bin/bash                       # One-off interactive

# Debug
docker logs -f mycontainer
docker exec -it mycontainer bash
docker stats mycontainer
docker inspect mycontainer | jq '.[0].State'

# Compose
docker compose up -d --build
docker compose logs -f api
docker compose exec api bash
docker compose down -v                                    # Down + delete volumes

# Cleanup
docker system prune -a --volumes                          # Full cleanup

# Scan
trivy image myapp:1.0.0 --severity CRITICAL,HIGH
```

---

*Reference compiled March 22, 2026. Sources: Docker official docs, NVIDIA Container Toolkit docs, Trivy docs, production best practices from the Docker and cloud-native communities.*

---

## 16. vLLM — High-Performance LLM Serving

> Complete reference for AI architects and engineers deploying LLMs at scale. Covers PagedAttention internals, production configuration, Docker/Kubernetes deployment, multi-GPU parallelism, and monitoring.

---

### What is vLLM

vLLM is an open-source, high-throughput inference and serving engine for large language models. It was created in 2023 by researchers at the **UC Berkeley Sky Computing Lab** (Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, et al.) and has since grown into a community-driven project with contributions from NVIDIA, Meta, Google, Microsoft, and hundreds of open-source contributors.

The core paper — *"Efficient Memory Management for Large Language Model Serving with PagedAttention"* — was published at SOSP 2023.

**Primary purpose:** Serve LLMs to concurrent users at maximum GPU utilization with minimum latency. It is the de-facto standard for self-hosted LLM serving as of 2026.

**GitHub:** https://github.com/vllm-project/vllm (40K+ stars)
**Docs:** https://docs.vllm.ai
**Docker image:** `vllm/vllm-openai`

---

### The Problem vLLM Solves

Serving LLMs with standard frameworks (HuggingFace Transformers, raw PyTorch) has three fundamental inefficiencies:

**1. KV Cache Memory Waste**
During inference, the attention mechanism computes key-value (KV) pairs for every token in the sequence. Standard implementations pre-allocate a contiguous memory block for the maximum possible sequence length — even if the actual sequence is short. Result: 60–80% of GPU memory is wasted on unused space.

**2. Static Batching**
Traditional serving processes one request at a time or bundles fixed-size batches. If a batch of 16 requests starts together, the GPU waits for the longest sequence to finish before starting any new requests — even if 14 of them completed in 100ms.

**3. Memory Fragmentation**
When requests share a common prefix (e.g., the same system prompt), standard implementations recompute those KV vectors for every request. No reuse, no deduplication.

**Quantified impact of these problems:**

| Problem | Waste |
|---------|-------|
| KV cache over-allocation | 60–80% GPU memory unusable |
| Static batching idle time | 40–60% GPU compute wasted |
| Prefix recomputation | Redundant FLOPS on every request |

vLLM solves all three.

---

### PagedAttention — The Core Innovation

PagedAttention applies the operating system concept of **virtual memory paging** to GPU KV cache management.

**Analogy:** Just as an OS divides RAM into fixed-size pages and maps virtual addresses to physical pages on demand, PagedAttention divides the KV cache into fixed-size **blocks** and allocates them to requests only as needed — non-contiguously.

**How it works:**

1. The KV cache is divided into fixed-size blocks (default: 16 tokens per block).
2. A **block table** maps each sequence's logical blocks to physical GPU memory blocks (like a page table in OS virtual memory).
3. When a request needs more KV cache, a free block is allocated from the pool — no pre-allocation required.
4. When a request completes, its blocks are immediately returned to the free pool.
5. Blocks from different requests can be **interleaved** in physical memory without any performance penalty.

**Copy-on-Write for parallel sampling:** When generating multiple completions from the same prompt (beam search, sampling N outputs), vLLM uses copy-on-write semantics — prompt blocks are shared across all branches until a branch diverges, then a private copy is made. This saves significant memory for beam search workloads.

**Memory efficiency result:**

| System | KV Cache Memory Waste |
|--------|-----------------------|
| FasterTransformer | 60–80% wasted |
| Orca | ~20% wasted |
| vLLM (PagedAttention) | <4% wasted |

**Throughput result vs baseline (LLaMA-13B, A100):**
- vs HuggingFace Transformers: **24x higher throughput**
- vs HuggingFace TGI (early versions): **14–24x higher throughput**
- vs FasterTransformer + Orca: **2–4x higher throughput**

---

### Key Features

**Continuous Batching (Iteration-Level Scheduling)**
Unlike static batching where all requests in a batch must finish before new ones join, vLLM's scheduler operates at the token generation step level. After each forward pass, finished sequences are evicted and new requests are inserted into the batch. GPU utilization stays near 100%. Delivers 2–5x improvement over static batching in high-concurrency scenarios.

**Automatic Prefix Caching**
When multiple requests share an identical prefix (system prompt, few-shot examples, RAG context), vLLM detects the hash match and reuses the already-computed KV blocks. The prefix is computed once and served from cache for all subsequent requests. Enabled with `--enable-prefix-caching`.

**Chunked Prefill**
Long prompts (32K+ tokens) block decoding for ongoing requests while they are being processed. Chunked prefill splits the prefill phase into smaller chunks, interleaving prefill and decoding work so ongoing generation is not starved. Enabled with `--enable-chunked-prefill`.

**Speculative Decoding**
Uses a small draft model (or token tree) to propose multiple tokens in one step. The larger target model verifies them in parallel. Accepted tokens are output instantly; rejected tokens are resampled. Net result: 1.5–3x latency reduction for generation-heavy workloads at minimal quality cost. Supports Medusa, Lookahead, and draft-model speculative decoding.

**Multi-LoRA Serving**
Serve hundreds of LoRA adapters simultaneously in a single vLLM instance. Each request specifies which adapter to use (`lora_request` parameter). Adapters are hot-swapped using the same base model weights — no separate deployment per adapter. Overhead is near-zero for adapters already loaded.

**Quantization Support**
- AWQ (Activation-aware Weight Quantization) — 4-bit, high accuracy
- GPTQ — 4-bit, widely available pre-quantized models
- FP8 — 8-bit floating point on H100/A100 with hardware acceleration
- SqueezeLLM — sparse quantization
- BitsAndBytes — for CPU offload scenarios
- Pass `--quantization awq|gptq|fp8|squeezellm` to enable.

**OpenAI-Compatible API**
vLLM's server (`vllm serve`) exposes `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, and `/v1/models` — identical to OpenAI's API. Drop-in replacement: change the `base_url`, keep the same client code.

**Distributed Serving**
- Tensor Parallelism: splits model weights across GPUs on a single node (via NCCL)
- Pipeline Parallelism: splits model layers across nodes (via Ray)
- Combined: common practice for 70B+ models

**Streaming**
Server-Sent Events (SSE) for streaming token-by-token responses. Standard `stream=True` in the OpenAI client or `stream: true` in the request body.

**Multimodal Support**
Vision-language models (LLaVA, InternVL, Qwen-VL, etc.) and audio-language models are supported. Image and audio inputs passed as base64 or URL in the messages payload.

---

### Installation and Quick Start

**Requirements:** Python 3.9+, CUDA 12.1+, 8GB+ VRAM minimum (16GB+ recommended)

```bash
# Standard GPU install
pip install vllm

# Specific CUDA version (if auto-detect fails)
pip install vllm --extra-index-url https://download.pytorch.org/whl/cu121

# From source (for latest features)
git clone https://github.com/vllm-project/vllm.git
cd vllm && pip install -e .
```

**Offline inference (Python):**

```python
from vllm import LLM, SamplingParams

# Load model (downloads from HuggingFace on first run)
llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    dtype="bfloat16",
    gpu_memory_utilization=0.9,
    max_model_len=8192,
)

params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512,
)

prompts = [
    "Explain transformer attention in one paragraph.",
    "What is PagedAttention?",
]

outputs = llm.generate(prompts, params)

for output in outputs:
    print(output.outputs[0].text)
```

**Chat completions (Python):**

```python
from vllm import LLM, SamplingParams
from vllm.entrypoints.openai.protocol import ChatCompletionRequest

llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")

# Using the chat template
outputs = llm.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is vLLM?"},
    ],
    sampling_params=SamplingParams(temperature=0.8, max_tokens=256),
)
print(outputs[0].outputs[0].text)
```

**Start the OpenAI-compatible server (CLI):**

```bash
# Basic server
vllm serve meta-llama/Llama-3.1-8B-Instruct

# With HuggingFace token for gated models
HF_TOKEN=hf_xxx vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192

# With quantization
vllm serve TheBloke/Llama-2-70B-Chat-AWQ \
  --quantization awq \
  --tensor-parallel-size 2

# With LoRA support
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --enable-lora \
  --lora-modules my-adapter=/path/to/lora \
  --max-loras 4

# With prefix caching and chunked prefill
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --enable-prefix-caching \
  --enable-chunked-prefill
```

---

### vLLM as OpenAI-Compatible Server

Once the server is running on port 8000, any code written for the OpenAI API works without changes — just point `base_url` to your vLLM instance.

**curl examples:**

```bash
# List available models
curl http://localhost:8000/v1/models

# Chat completion
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is PagedAttention?"}
    ],
    "max_tokens": 256,
    "temperature": 0.7
  }'

# Text completion
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "prompt": "The capital of France is",
    "max_tokens": 50
  }'

# Streaming
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "Write a haiku."}],
    "stream": true,
    "max_tokens": 100
  }'

# Health check
curl http://localhost:8000/health

# Prometheus metrics
curl http://localhost:8000/metrics
```

**Python client (drop-in replacement):**

```python
from openai import OpenAI

# Point to vLLM — no other code changes needed
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",  # vLLM accepts any non-empty string
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain KV cache in 2 sentences."},
    ],
    max_tokens=200,
    temperature=0.7,
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Count to 5."}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

# With LoRA adapter
response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={"lora_request": {"lora_name": "my-adapter", "lora_int_id": 1,
                                  "lora_local_path": "/path/to/lora"}},
)
```

---

### Docker Deployment

**Single GPU — production-ready:**

```bash
docker run -d \
  --name vllm-server \
  --runtime nvidia \
  --gpus all \
  --ipc=host \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e HF_TOKEN=${HF_TOKEN} \
  --restart unless-stopped \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --enable-prefix-caching
```

Note: `--ipc=host` is mandatory for multi-GPU (NCCL uses shared memory for intra-node GPU communication). Safe to include for single-GPU deployments too.

**Multi-GPU (70B model, tensor parallelism):**

```bash
docker run -d \
  --name vllm-70b \
  --runtime nvidia \
  --gpus '"device=0,1,2,3"' \
  --ipc=host \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e HF_TOKEN=${HF_TOKEN} \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.92
```

**Docker Compose — with Prometheus and Grafana:**

```yaml
# docker-compose.yml
version: "3.8"

services:
  vllm:
    image: vllm/vllm-openai:latest
    runtime: nvidia
    container_name: vllm-server
    ports:
      - "8000:8000"
    volumes:
      - huggingface-cache:/root/.cache/huggingface
    environment:
      - HF_TOKEN=${HF_TOKEN}
    ipc: host
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
        limits:
          memory: 32G
    command: >
      --model meta-llama/Llama-3.1-8B-Instruct
      --host 0.0.0.0
      --port 8000
      --dtype bfloat16
      --gpu-memory-utilization 0.9
      --max-model-len 8192
      --max-num-seqs 256
      --enable-prefix-caching
      --disable-log-requests
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 300s   # Model loading can take 3-5 min
    restart: unless-stopped
    networks:
      - vllm-net

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.retention.time=7d"
    restart: unless-stopped
    networks:
      - vllm-net

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
      - GF_USERS_ALLOW_SIGN_UP=false
    restart: unless-stopped
    networks:
      - vllm-net
    depends_on:
      - prometheus

networks:
  vllm-net:
    driver: bridge

volumes:
  huggingface-cache:
  prometheus-data:
  grafana-data:
```

**Prometheus scrape config (prometheus.yml):**

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "vllm"
    static_configs:
      - targets: ["vllm:8000"]
    metrics_path: /metrics
    scrape_interval: 10s
```

**Custom Dockerfile (build your own vLLM image with model baked in):**

```dockerfile
FROM vllm/vllm-openai:latest

# Set working directory
WORKDIR /app

# Copy model weights (if self-hosting weights instead of HF Hub)
# COPY ./weights /app/weights

# Pre-download model at build time (optional — large layers cache in registry)
ARG HF_TOKEN
RUN python -c "from huggingface_hub import snapshot_download; \
    snapshot_download('meta-llama/Llama-3.1-8B-Instruct', token='${HF_TOKEN}')"

# Default entrypoint from base image calls `python -m vllm.entrypoints.openai.api_server`
# Override default args
CMD ["--model", "meta-llama/Llama-3.1-8B-Instruct", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--dtype", "bfloat16", \
     "--gpu-memory-utilization", "0.9"]
```

---

### Kubernetes Deployment

**GPU Node requirements:**
- Node label: `nvidia.com/gpu.present=true`
- NVIDIA device plugin installed: `kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.16.2/deployments/static/nvidia-device-plugin.yml`
- Shared memory: configure `shmSize` when `requestGPU > 1` (NCCL requirement)

**Single-GPU Deployment + Service + HPA:**

```yaml
# vllm-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-server
  namespace: ai-serving
  labels:
    app: vllm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          args:
            - "--model"
            - "meta-llama/Llama-3.1-8B-Instruct"
            - "--host"
            - "0.0.0.0"
            - "--port"
            - "8000"
            - "--dtype"
            - "bfloat16"
            - "--gpu-memory-utilization"
            - "0.90"
            - "--max-model-len"
            - "8192"
            - "--max-num-seqs"
            - "256"
            - "--enable-prefix-caching"
            - "--disable-log-requests"
          ports:
            - containerPort: 8000
              name: http
          env:
            - name: HF_TOKEN
              valueFrom:
                secretKeyRef:
                  name: hf-secret
                  key: token
          resources:
            requests:
              memory: "24Gi"
              cpu: "4"
              nvidia.com/gpu: "1"
            limits:
              memory: "32Gi"
              cpu: "8"
              nvidia.com/gpu: "1"
          volumeMounts:
            - name: shm
              mountPath: /dev/shm
            - name: hf-cache
              mountPath: /root/.cache/huggingface
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 120   # Model loading time
            periodSeconds: 10
            failureThreshold: 12
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 180
            periodSeconds: 30
            failureThreshold: 3
      volumes:
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: "8Gi"     # Required for NCCL multi-GPU
        - name: hf-cache
          persistentVolumeClaim:
            claimName: hf-cache-pvc
      nodeSelector:
        nvidia.com/gpu.present: "true"
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule

---
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
  namespace: ai-serving
spec:
  selector:
    app: vllm
  ports:
    - name: http
      port: 80
      targetPort: 8000
  type: ClusterIP

---
# HPA based on custom GPU metrics (requires KEDA or custom metrics adapter)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
  namespace: ai-serving
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-server
  minReplicas: 1
  maxReplicas: 4
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**HuggingFace token secret:**

```bash
kubectl create namespace ai-serving
kubectl create secret generic hf-secret \
  --from-literal=token=hf_your_token_here \
  --namespace ai-serving
```

**PersistentVolumeClaim for model cache:**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: hf-cache-pvc
  namespace: ai-serving
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi   # Adjust per model size
  storageClassName: fast-ssd  # Use your cluster's SSD storage class
```

**Multi-GPU pod (70B model, 4 GPUs, tensor parallelism):**

```yaml
# Key differences vs single-GPU
containers:
  - name: vllm
    args:
      - "--model"
      - "meta-llama/Llama-3.1-70B-Instruct"
      - "--tensor-parallel-size"
      - "4"
      - "--dtype"
      - "bfloat16"
      - "--gpu-memory-utilization"
      - "0.92"
    resources:
      limits:
        nvidia.com/gpu: "4"
        memory: "128Gi"
volumes:
  - name: shm
    emptyDir:
      medium: Memory
      sizeLimit: "16Gi"   # Larger shm for 4-GPU NCCL
```

---

### Performance Comparison

Benchmarks on **LLaMA-3.1-8B, A100 80GB SXM, concurrent users = 64:**

| Framework | Throughput (tok/s) | P50 TTFT | P99 TTFT | Notes |
|-----------|--------------------|----------|----------|-------|
| HuggingFace Transformers | ~230 | 850ms | 3200ms | Static batching, no optimization |
| HuggingFace TGI | ~2,200 | 120ms | 580ms | Entered maintenance Dec 2025 |
| vLLM | ~5,500 | 35ms | 180ms | PagedAttention + continuous batching |
| TensorRT-LLM (NVIDIA) | ~7,000 | 25ms | 140ms | Highest raw throughput, complex setup |
| SGLang | ~5,800+ | 32ms | 165ms | Better prefix reuse (RadixAttention) |

*TTFT = Time to First Token. Numbers are representative; exact values depend on model, hardware, batch composition, and sequence length distribution.*

**Key observations:**
- vLLM vs raw HuggingFace: **24x throughput** improvement
- vLLM vs TGI: **2.5x throughput** at the same latency percentile
- TensorRT-LLM beats vLLM on raw GPU throughput by 20–40% on H100 — but requires NVIDIA hardware and complex compilation per model
- SGLang is competitive with vLLM and can outperform it on workloads with heavy prompt prefix reuse (chatbots, RAG systems with shared context)
- TGI entered maintenance mode December 2025; HuggingFace now recommends vLLM or SGLang

**vLLM is the default choice when:** broad model compatibility, ease of deployment, multi-LoRA serving, and active community support matter more than the last 20% of raw throughput.

---

### Configuration Reference

**Engine arguments (most important):**

| Parameter | Default | What it controls |
|-----------|---------|-----------------|
| `--model` | required | Model ID (HuggingFace Hub) or local path |
| `--dtype` | `auto` | Weight precision: `float16`, `bfloat16`, `float32`, `auto` |
| `--gpu-memory-utilization` | `0.9` | Fraction of GPU VRAM reserved for KV cache. Range 0.7–0.95. Higher = more concurrent sequences, higher OOM risk |
| `--max-model-len` | model default | Maximum sequence length (prompt + completion). Lowering reduces KV cache footprint |
| `--max-num-seqs` | `256` | Maximum number of concurrent sequences in a batch. Increase for throughput, decrease for latency |
| `--max-num-batched-tokens` | auto | Maximum tokens processed per forward pass. Auto-set based on model and GPU memory |
| `--tensor-parallel-size` | `1` | Number of GPUs for tensor parallelism (single-node) |
| `--pipeline-parallel-size` | `1` | Number of pipeline stages across nodes (multi-node via Ray) |
| `--quantization` | `None` | `awq`, `gptq`, `fp8`, `squeezellm`, `bitsandbytes` |
| `--enable-prefix-caching` | `False` | Cache KV blocks for shared prefixes across requests |
| `--enable-chunked-prefill` | `False` | Split long prompts across steps, prevents decode starvation |
| `--swap-space` | `4` (GiB) | CPU RAM used as overflow KV cache when GPU is full. Set 0 to disable |
| `--block-size` | `16` | Number of tokens per KV cache block (16 or 32) |
| `--seed` | `0` | Reproducibility seed |
| `--disable-log-requests` | `False` | Set `True` in production to reduce I/O overhead |

**Server arguments:**

| Parameter | Default | What it controls |
|-----------|---------|-----------------|
| `--host` | `localhost` | Bind address. Use `0.0.0.0` for containers |
| `--port` | `8000` | Server port |
| `--api-key` | `None` | Optional API key for basic auth |
| `--max-log-len` | `None` | Truncate logged request/response content |
| `--uvicorn-log-level` | `info` | `debug`, `info`, `warning`, `error` |

**Environment variables:**

```bash
HF_TOKEN=hf_xxx                    # HuggingFace token for gated models
VLLM_WORKER_MULTIPROC_METHOD=spawn # For multi-GPU on some systems
NCCL_DEBUG=WARN                    # NCCL logging verbosity
CUDA_VISIBLE_DEVICES=0,1,2,3       # Which GPUs to use
VLLM_ATTENTION_BACKEND=FLASH_ATTN  # Force Flash Attention backend
```

**Scenario-tuned configurations:**

```bash
# High throughput (batch workloads, offline processing)
vllm serve model \
  --gpu-memory-utilization 0.95 \
  --max-num-seqs 512 \
  --max-model-len 4096 \
  --enable-prefix-caching \
  --enable-chunked-prefill

# Low latency (interactive chat, <200ms TTFT target)
vllm serve model \
  --gpu-memory-utilization 0.85 \
  --max-num-seqs 32 \
  --max-model-len 4096

# Long context (document analysis, 128K tokens)
vllm serve model \
  --max-model-len 131072 \
  --max-num-seqs 16 \
  --max-num-batched-tokens 4096 \
  --enable-chunked-prefill \
  --swap-space 16

# Quantized (limited VRAM, consumer GPU)
vllm serve TheBloke/Llama-2-13B-chat-AWQ \
  --quantization awq \
  --dtype half \
  --max-model-len 4096
```

---

### Multi-GPU and Multi-Node

**Tensor Parallelism (single node, multiple GPUs):**
Splits each weight matrix across GPUs column-wise and row-wise. Each GPU holds a shard of every layer. All GPUs process every forward pass in parallel via NCCL all-reduce. This is the standard approach for models that fit within a single node.

```bash
# 4x A100 for 70B model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.92

# Rule: tensor-parallel-size must divide the number of attention heads evenly
# LLaMA-3.1-70B has 64 heads → valid TP sizes: 1, 2, 4, 8
```

**Pipeline Parallelism (multi-node):**
Assigns consecutive transformer layers to different nodes. Node 0 runs layers 0–15, Node 1 runs layers 16–31, etc. Requires Ray cluster. Higher latency than tensor parallelism due to inter-node communication, but enables serving models larger than a single node's combined VRAM.

```bash
# On head node — start Ray
ray start --head --port=6379

# On worker node
ray start --address=<head-node-ip>:6379

# Launch vLLM with both TP and PP
vllm serve meta-llama/Llama-3.1-405B-Instruct \
  --tensor-parallel-size 8 \
  --pipeline-parallel-size 2 \
  --dtype bfloat16

# With Ray cluster address
RAY_ADDRESS=ray://<head-node-ip>:6379 vllm serve ...
```

**Best practice for model sizing:**

| Model Size | Recommended Config |
|------------|-------------------|
| 7–8B | 1x A100 80GB, `--tensor-parallel-size 1` |
| 13B | 1x A100 80GB (BF16) or 2x A100 40GB |
| 34–40B | 2x A100 80GB, `--tensor-parallel-size 2` |
| 70B | 4x A100 80GB, `--tensor-parallel-size 4` |
| 405B | 8x H100 80GB, `--tensor-parallel-size 8` |
| 405B (multi-node) | 2 nodes × 8 GPUs, TP=8, PP=2 |

---

### Production Patterns

**Health checks:**

vLLM exposes two endpoints for orchestration:
- `GET /health` — returns 200 when the model is loaded and the server is ready; 503 during startup or if engine has failed
- `GET /metrics` — Prometheus-format metrics

Use `/health` for readiness and liveness probes (not `/v1/models` — that returns 200 before the model finishes loading).

**Graceful shutdown:**

vLLM handles SIGTERM gracefully. Docker and Kubernetes send SIGTERM before SIGKILL. To ensure in-flight requests complete:

```yaml
# In Kubernetes deployment
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60   # Wait up to 60s for SIGKILL after SIGTERM
      containers:
        - name: vllm
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sleep", "5"]  # Drain load balancer before SIGTERM
```

```yaml
# In docker-compose
services:
  vllm:
    stop_grace_period: 60s
```

**Prometheus metrics exposed at `/metrics`:**

| Metric | Type | Description |
|--------|------|-------------|
| `vllm:num_requests_running` | Gauge | Requests currently being processed |
| `vllm:num_requests_waiting` | Gauge | Requests in the queue |
| `vllm:num_requests_swapped` | Gauge | Requests swapped to CPU (memory pressure) |
| `vllm:gpu_cache_usage_perc` | Gauge | KV cache GPU utilization (0–1) |
| `vllm:cpu_cache_usage_perc` | Gauge | KV cache CPU (swap) utilization (0–1) |
| `vllm:e2e_request_latency_seconds` | Histogram | End-to-end latency per request |
| `vllm:request_prompt_tokens` | Histogram | Prompt token count distribution |
| `vllm:request_generation_tokens` | Histogram | Generated token count distribution |
| `vllm:request_success_total` | Counter | Successfully completed requests |
| `vllm:request_failure_total` | Counter | Failed requests (with reason labels) |
| `vllm:avg_prompt_throughput_toks_per_s` | Gauge | Prompt processing throughput |
| `vllm:avg_generation_throughput_toks_per_s` | Gauge | Token generation throughput |
| `vllm:time_to_first_token_seconds` | Histogram | TTFT distribution (P50/P95/P99) |
| `vllm:time_per_output_token_seconds` | Histogram | Inter-token latency (TBT) distribution |

**Key alert thresholds:**

```yaml
# prometheus-alerts.yml (example)
groups:
  - name: vllm
    rules:
      - alert: VllmHighQueueDepth
        expr: vllm:num_requests_waiting > 50
        for: 2m
        annotations:
          summary: "vLLM queue depth > 50 — consider scaling up"

      - alert: VllmHighKVCacheUsage
        expr: vllm:gpu_cache_usage_perc > 0.95
        for: 1m
        annotations:
          summary: "KV cache > 95% full — OOM risk"

      - alert: VllmHighP99Latency
        expr: histogram_quantile(0.99, rate(vllm:e2e_request_latency_seconds_bucket[5m])) > 10
        for: 3m
        annotations:
          summary: "P99 latency > 10s — degraded service"

      - alert: VllmDown
        expr: up{job="vllm"} == 0
        for: 1m
        annotations:
          summary: "vLLM instance is down"
```

**Load balancing multiple vLLM instances (nginx):**

```nginx
# nginx.conf
upstream vllm_backend {
    least_conn;                          # Route to least-loaded instance
    server vllm-1:8000 max_fails=2 fail_timeout=30s;
    server vllm-2:8000 max_fails=2 fail_timeout=30s;
    server vllm-3:8000 max_fails=2 fail_timeout=30s;
    keepalive 32;
}

server {
    listen 80;

    location /v1/ {
        proxy_pass http://vllm_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";          # Enable keepalive
        proxy_set_header Host $host;
        proxy_read_timeout 300s;                 # Long timeout for slow generations
        proxy_buffering off;                     # Required for SSE streaming
        proxy_cache off;
    }

    location /health {
        proxy_pass http://vllm_backend;
        proxy_read_timeout 5s;
    }
}
```

**Load balancing with Kubernetes + multiple Deployments (model parallel per pod):**

The recommended production-stack pattern is to deploy one Deployment per GPU count tier (e.g., a Deployment of 1-GPU pods for small models, a Deployment of 4-GPU pods for large models), then route via a Service with a load balancer in front. The vLLM project maintains a production-stack Helm chart at `vllm-project/production-stack` that handles this routing automatically.

**Common production issues and fixes:**

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| OOM on startup | Model too large for VRAM | Use quantization (`--quantization awq`) or reduce `--max-model-len` |
| OOM during serving | KV cache too large | Reduce `--gpu-memory-utilization` to 0.80, enable `--swap-space 16` |
| Slow TTFT (>500ms) | Long prompts blocking decode | Enable `--enable-chunked-prefill` |
| Low throughput | Too few concurrent sequences | Increase `--max-num-seqs` to 256–512 |
| High P99 latency | Request queue buildup | Scale horizontally or increase GPU count |
| NCCL timeout (multi-GPU) | Shared memory too small | Add `--ipc=host` (Docker) or increase `shmSize` (K8s) |
| Model not loading | Gated model without token | Set `HF_TOKEN` environment variable |
| Readiness probe failing | Slow model load | Increase `initialDelaySeconds` to 180–300 |

---

*Reference compiled March 22, 2026. Sources: [vLLM GitHub](https://github.com/vllm-project/vllm), [vLLM Docs](https://docs.vllm.ai), [PagedAttention Paper (SOSP 2023)](https://dl.acm.org/doi/10.1145/3600006.3613165), [vLLM Anatomy Blog](https://vllm.ai/blog/anatomy-of-vllm), [LLM Inference Server Comparison 2026](https://blog.premai.io/llm-inference-servers-compared-vllm-vs-tgi-vs-sglang-vs-triton-2026/), [vLLM Production Guide 2026](https://www.youngju.dev/blog/llm/2026-03-07-llm-vllm-serving-optimization-production.en), [vLLM Docker Deployment](https://inference.net/content/vllm-docker-deployment), [vLLM K8s Docs](https://docs.vllm.ai/en/stable/deployment/k8s/)*

## 17. NVIDIA Triton Inference Server — Universal Model Serving

> Complete reference for deploying **any** AI/ML model (not just LLMs) at production scale using NVIDIA's open-source inference server. Covers architecture, configuration, Docker, Kubernetes, ensembles, and performance tuning.

---

### What is Triton Inference Server?

NVIDIA Triton Inference Server (formerly TensorRT Inference Server) is an **open-source, production-grade inference serving platform** that can host any model from any framework on GPU or CPU. Where vLLM is purpose-built for LLMs only, Triton is a **universal inference server** — it serves TensorRT engines, ONNX models, PyTorch models, TensorFlow SavedModels, Python-based custom models, and even complete multi-model pipelines in a single unified server.

Key distinctions:
- Open source (Apache 2.0) — GitHub: `triton-inference-server/server`
- Supports ALL model types: vision, NLP, ML, classic ML, LLMs
- Can run multiple models simultaneously (different models on different GPUs / CPU)
- Enterprise-grade: used by AWS SageMaker, GCP Vertex AI, Azure ML, NVIDIA DGX
- As of March 2025, Triton is part of the NVIDIA Dynamo Platform (also called NVIDIA Dynamo Triton)

---

### Why Triton Instead of vLLM

| Dimension | vLLM | Triton Inference Server |
|-----------|------|------------------------|
| Model types | LLMs only (HuggingFace-compatible) | ANY: TensorRT, PyTorch, TF, ONNX, custom Python, LLMs via vLLM backend |
| Simultaneous models | One model per instance | Many models, each with its own scheduler queue |
| Primary optimization | PagedAttention KV cache for LLM throughput | Multi-framework, multi-model, GPU/CPU scheduling |
| Batching strategy | Continuous batching (LLM-native) | Dynamic batching (configurable per model), sequence batching, direct pass-through |
| Ensemble / pipelines | Not native | First-class: preprocessing → model → postprocessing as single endpoint |
| Hardware | GPU (NVIDIA, some AMD) | NVIDIA GPU, CPU, AWS Inferentia (via custom backend) |
| Model warming | Manual (send warm-up requests) | Built-in `ModelWarmup` config in config.pbtxt |
| Protocol | OpenAI-compatible HTTP | HTTP/REST, gRPC, C API, shared memory |
| Prometheus metrics | Basic | Rich: latency histograms, queue depth, GPU utilization per model |
| Typical user | Startups, API services needing OpenAI compat | Enterprises, multi-model pipelines, CV + NLP together |

**Rule of thumb:**
- Serving **only LLMs** with OpenAI API compat → use **vLLM**
- Serving **vision models, ML models, NLP pipelines, or LLMs + other models together** → use **Triton**
- Maximum throughput on NVIDIA hardware for LLMs → use **TensorRT-LLM backend inside Triton**

---

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                          │
│  Your App / API Gateway / Load Balancer                             │
└───────────────┬──────────────────────────────┬──────────────────────┘
                │                              │
                ▼                              ▼
   ┌─────────────────────┐        ┌─────────────────────┐
   │  Python Client      │        │  C++ Client         │
   │  tritonclient.http  │        │  tritonclient.grpc  │
   │  tritonclient.grpc  │        │  (low-latency path) │
   └────────┬────────────┘        └──────────┬──────────┘
            │                               │
            ▼                               ▼
   ┌──────────────────────────────────────────────────┐
   │              HTTP/REST  or  gRPC                  │
   │         (port 8000)      (port 8001)              │
   └───────────────────────┬──────────────────────────┘
                           │
   ┌───────────────────────▼──────────────────────────┐
   │                  TRITON SERVER                    │
   │                                                   │
   │  ┌─────────┐   ┌──────────────────────────────┐  │
   │  │  C API  │   │     Inference Request /       │  │
   │  │ (port   │   │      Response Handler         │  │
   │  │  8002)  │   └──────────────┬───────────────┘  │
   │  └─────────┘                  │                   │
   │                               ▼                   │
   │  ┌────────────────────────────────────────────┐   │
   │  │      Per-Model Scheduler Queues             │   │
   │  │                                             │   │
   │  │  model-A queue → Dynamic Batcher           │   │
   │  │  model-B queue → Sequence Batcher          │   │
   │  │  model-C queue → Direct (no batching)      │   │
   │  └──────────────────┬─────────────────────────┘   │
   │                     │                              │
   │                     ▼                              │
   │  ┌────────────────────────────────────────────┐   │
   │  │           Framework Backends                │   │
   │  │                                             │   │
   │  │  TensorRT  │  TF  │  PyTorch  │  ONNX      │   │
   │  │  OpenVINO  │  Python Backend  │  Custom C++ │   │
   │  │  vLLM Backend  │  TensorRT-LLM Backend      │   │
   │  └────────────────────────────────────────────┘   │
   │                                                   │
   │  ┌─────────────────┐   ┌───────────────────────┐  │
   │  │  Model          │   │  Status / Health /    │  │
   │  │  Repository     │   │  Metrics Export       │  │
   │  │  (Persistent    │   │  (port 8002 HTTP)     │  │
   │  │   Volume / S3)  │   │  → Prometheus scrape  │  │
   │  └─────────────────┘   └───────────────────────┘  │
   │                                                   │
   │  Runs on: Multiple GPUs + CPU simultaneously      │
   └──────────────────────────────────────────────────┘
```

**Three ports:**
- `8000` — HTTP/REST inference + management + metrics
- `8001` — gRPC (lower latency, preferred for production)
- `8002` — HTTP metrics only (Prometheus scrape endpoint)

---

### Supported Backends

| Backend | File Format | Use Case |
|---------|------------|----------|
| `tensorrt` | `.plan` / `.engine` | Maximum throughput on NVIDIA GPU. Requires model compilation. |
| `pytorch` | `.pt` (TorchScript) | PyTorch models. No compilation needed. |
| `tensorflow` | `SavedModel/` or `.graphdef` | TensorFlow 1.x + 2.x. |
| `onnxruntime` | `.onnx` | Cross-framework portability. Runs on GPU + CPU. |
| `openvino` | `.xml` + `.bin` | Intel CPU optimization. |
| `python` | `model.py` | ANY Python model: sklearn, XGBoost, custom logic, pre/post-processing. |
| `tensorrtllm` | TensorRT-LLM engine | Maximum-throughput LLM serving on NVIDIA (requires compilation). |
| `vllm` | HuggingFace model | vLLM PagedAttention inside Triton. Adds Triton's multi-model management. |
| `fil` | XGBoost / LightGBM / RF | Gradient-boosted trees and forests. |
| `dali` | DALI pipeline | GPU-accelerated image preprocessing. |
| Custom C++ | `.so` shared library | Low-level custom backends with direct CUDA access. |

Install all backends: use the `nvcr.io/nvidia/tritonserver:<version>-py3` image (includes everything).

---

### Model Repository Structure

Triton loads models from a **model repository** — a directory (local, NFS, or S3) with a strict layout:

```
model_repository/
├── resnet50/                      # Model name
│   ├── config.pbtxt               # Required: model configuration
│   ├── output_labels.txt          # Optional: class labels
│   ├── 1/                         # Version directory (must be integer)
│   │   └── model.plan             # TensorRT engine file
│   └── 2/                         # Newer version
│       └── model.plan
│
├── bert_ner/
│   ├── config.pbtxt
│   └── 1/
│       └── model.onnx             # ONNX model file
│
├── gpt2_inference/
│   ├── config.pbtxt
│   └── 1/
│       ├── model.py               # Python backend entry point
│       └── requirements.txt       # Optional: pip install on load
│
└── full_pipeline/                 # Ensemble model — no model files needed
    ├── config.pbtxt               # Describes the pipeline DAG
    └── 1/                         # Empty version directory (required)
```

Version selection rules (configurable in config.pbtxt):
- `NONE` — No version is available (disabled)
- `LATEST` — Only the highest-numbered version is loaded (default)
- `ALL` — All versions are loaded simultaneously
- `SPECIFIC` — List explicit versions to load

S3 model repository: `tritonserver --model-repository=s3://bucket/model-repo`

---

### config.pbtxt — Configuration Format

config.pbtxt uses Protocol Buffer text format. Every model needs one.

#### Minimal required fields

```protobuf
# Required: one of 'backend' OR 'platform'
backend: "onnxruntime"            # OR platform: "onnxruntime_onnx"

# Required: 0 = unlimited (model handles batch size itself)
max_batch_size: 32

# Required: input tensor specs
input [
  {
    name: "input_ids"
    data_type: TYPE_INT64
    dims: [ 128 ]                 # -1 means variable length
  }
]

# Required: output tensor specs
output [
  {
    name: "logits"
    data_type: TYPE_FP32
    dims: [ 768 ]
  }
]
```

#### PyTorch TorchScript model

```protobuf
# resnet50/config.pbtxt
name: "resnet50"
backend: "pytorch"
max_batch_size: 64

input [
  {
    name: "input__0"
    data_type: TYPE_FP32
    dims: [ 3, 224, 224 ]         # C, H, W — batch dim is implicit
  }
]

output [
  {
    name: "output__0"
    data_type: TYPE_FP32
    dims: [ 1000 ]                # ImageNet classes
  }
]

# Dynamic batching — Triton queues requests and batches them
dynamic_batching {
  preferred_batch_size: [ 8, 16, 32 ]
  max_queue_delay_microseconds: 5000    # Wait up to 5ms to fill a batch
}

# GPU instance group
instance_group [
  {
    kind: KIND_GPU
    count: 2                      # 2 model instances on GPU
    gpus: [ 0 ]                   # Which GPU(s)
  }
]
```

#### ONNX model

```protobuf
# bert_ner/config.pbtxt
name: "bert_ner"
backend: "onnxruntime"
max_batch_size: 16

input [
  {
    name: "input_ids"
    data_type: TYPE_INT64
    dims: [ -1 ]                  # Variable sequence length
  },
  {
    name: "attention_mask"
    data_type: TYPE_INT64
    dims: [ -1 ]
  }
]

output [
  {
    name: "last_hidden_state"
    data_type: TYPE_FP32
    dims: [ -1, 768 ]
  }
]

dynamic_batching {
  preferred_batch_size: [ 4, 8 ]
  max_queue_delay_microseconds: 10000
}

instance_group [
  {
    kind: KIND_GPU
    count: 1
  }
]

# Optimization: use FP16 on GPU
optimization {
  execution_accelerators {
    gpu_execution_accelerator: [
      {
        name: "tensorrt"          # Compile ONNX → TensorRT at load time
        parameters {
          key: "precision_mode"
          value: "FP16"
        }
      }
    ]
  }
}
```

#### TensorFlow SavedModel

```protobuf
# tf_classifier/config.pbtxt
name: "tf_classifier"
platform: "tensorflow_savedmodel"
max_batch_size: 32

input [
  {
    name: "serving_default_input_1:0"
    data_type: TYPE_FP32
    dims: [ 224, 224, 3 ]
  }
]

output [
  {
    name: "StatefulPartitionedCall:0"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]

dynamic_batching {
  preferred_batch_size: [ 16, 32 ]
  max_queue_delay_microseconds: 5000
}
```

#### Python Backend model

```protobuf
# custom_model/config.pbtxt
name: "custom_model"
backend: "python"
max_batch_size: 0                 # Python backend handles batching itself

input [
  {
    name: "text"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]

output [
  {
    name: "embedding"
    data_type: TYPE_FP32
    dims: [ 384 ]
  }
]

instance_group [
  {
    kind: KIND_CPU                # Python backend — can run on CPU
    count: 4                      # 4 parallel Python processes
  }
]
```

The corresponding `model.py` must implement the `TritonPythonModel` interface:

```python
# custom_model/1/model.py
import numpy as np
import triton_python_backend_utils as pb_utils
from sentence_transformers import SentenceTransformer

class TritonPythonModel:
    def initialize(self, args):
        """Called once on model load."""
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def execute(self, requests):
        """Called for each batch of inference requests."""
        responses = []
        for request in requests:
            # Decode input
            text_tensor = pb_utils.get_input_tensor_by_name(request, "text")
            texts = [t.decode("utf-8") for t in text_tensor.as_numpy().flatten()]

            # Run inference
            embeddings = self.model.encode(texts).astype(np.float32)

            # Build output
            output_tensor = pb_utils.Tensor(
                "embedding",
                embeddings
            )
            responses.append(pb_utils.InferenceResponse(output_tensors=[output_tensor]))

        return responses

    def finalize(self):
        """Called on model unload (optional cleanup)."""
        pass
```

#### Model Warmup configuration

```protobuf
# Add inside any config.pbtxt to pre-warm the model
model_warmup [
  {
    name: "warmup_request"
    batch_size: 1
    inputs {
      key: "input_ids"
      value {
        data_type: TYPE_INT64
        dims: [ 128 ]
        zero_data: true          # Send all-zeros tensor as warmup input
      }
    }
  }
]
```

---

### Model Ensemble — Chaining Models

An ensemble is a directed pipeline of models. One HTTP/gRPC request triggers the entire chain. Triton handles all tensor passing internally with zero data copy where possible.

**Example: image classification pipeline**
- Step 1: `preprocessor` (Python backend) — resize + normalize image
- Step 2: `resnet50` (TensorRT) — classify
- Step 3: `postprocessor` (Python backend) — decode class label

```
model_repository/
├── preprocessor/
│   ├── config.pbtxt
│   └── 1/model.py
├── resnet50/
│   ├── config.pbtxt
│   └── 1/model.plan
├── postprocessor/
│   ├── config.pbtxt
│   └── 1/model.py
└── image_pipeline/               # The ensemble
    ├── config.pbtxt
    └── 1/                        # Empty — ensemble has no model files
```

```protobuf
# image_pipeline/config.pbtxt
name: "image_pipeline"
platform: "ensemble"
max_batch_size: 16

input [
  {
    name: "raw_image"
    data_type: TYPE_UINT8
    dims: [ -1, -1, 3 ]           # Variable H x W x C
  }
]

output [
  {
    name: "class_label"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]

# Defines the pipeline DAG
ensemble_scheduling {
  step [
    {
      model_name: "preprocessor"
      model_version: -1           # -1 = latest version
      input_map {
        key: "raw_image"          # ensemble input name
        value: "input_image"      # preprocessor's input name
      }
      output_map {
        key: "normalized"         # preprocessor's output name
        value: "preprocessed_tensor"  # internal pipeline tensor name
      }
    },
    {
      model_name: "resnet50"
      model_version: -1
      input_map {
        key: "preprocessed_tensor"
        value: "input__0"
      }
      output_map {
        key: "output__0"
        value: "class_logits"
      }
    },
    {
      model_name: "postprocessor"
      model_version: -1
      input_map {
        key: "class_logits"
        value: "logits_input"
      }
      output_map {
        key: "label_output"
        value: "class_label"
      }
    }
  ]
}
```

---

### Installation and Quick Start

#### Docker — recommended

```bash
# Pull the Triton server image (NGC)
# Replace YY.MM with release, e.g. 25.01 (January 2025)
docker pull nvcr.io/nvidia/tritonserver:25.01-py3

# Run with GPU, mounting a local model repository
docker run --gpus all \
  -p 8000:8000 \        # HTTP
  -p 8001:8001 \        # gRPC
  -p 8002:8002 \        # Metrics
  -v /path/to/model_repository:/models \
  nvcr.io/nvidia/tritonserver:25.01-py3 \
  tritonserver --model-repository=/models

# CPU-only (no GPU)
docker run \
  -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v /path/to/model_repository:/models \
  nvcr.io/nvidia/tritonserver:25.01-py3 \
  tritonserver --model-repository=/models --backend-config=tensorflow,version=2
```

#### Install Python client library

```bash
pip install tritonclient[all]        # HTTP + gRPC + shared memory
pip install tritonclient[http]       # HTTP only
pip install tritonclient[grpc]       # gRPC only
```

#### Verify server is running

```bash
# Health check
curl http://localhost:8000/v2/health/ready
# → {"ready":true}

# List loaded models
curl http://localhost:8000/v2/models

# Model metadata
curl http://localhost:8000/v2/models/resnet50

# Prometheus metrics
curl http://localhost:8002/metrics
```

---

### Python Client Examples

#### HTTP client

```python
import numpy as np
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException

# Connect
client = httpclient.InferenceServerClient(url="localhost:8000")

# Check server health
print("Server ready:", client.is_server_ready())
print("Model ready:", client.is_model_ready("resnet50"))

# Prepare input
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
input_tensor = httpclient.InferInput("input__0", input_data.shape, "FP32")
input_tensor.set_data_from_numpy(input_data)

# Define expected output
output = httpclient.InferRequestedOutput("output__0")

# Run inference
response = client.infer(
    model_name="resnet50",
    inputs=[input_tensor],
    outputs=[output],
    model_version="1",             # optional: omit for latest
    request_id="req-001",          # optional: for tracing
    timeout=10                     # seconds
)

# Get result
logits = response.as_numpy("output__0")
predicted_class = np.argmax(logits[0])
print("Predicted class:", predicted_class)
```

#### gRPC client (lower latency — preferred for production)

```python
import numpy as np
import tritonclient.grpc as grpcclient
from tritonclient.utils import np_to_triton_dtype

client = grpcclient.InferenceServerClient(
    url="localhost:8001",
    verbose=False,
    ssl=False                      # Enable for TLS in production
)

input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)

input_tensor = grpcclient.InferInput(
    "input__0",
    input_data.shape,
    np_to_triton_dtype(input_data.dtype)
)
input_tensor.set_data_from_numpy(input_data)

output = grpcclient.InferRequestedOutput("output__0")

response = client.infer(
    model_name="resnet50",
    inputs=[input_tensor],
    outputs=[output]
)

logits = response.as_numpy("output__0")
print("Shape:", logits.shape)
```

#### Async HTTP client (batch of requests)

```python
import asyncio
import numpy as np
import tritonclient.http.aio as async_httpclient

async def batch_infer(texts: list[str]):
    client = async_httpclient.InferenceServerClient("localhost:8000")

    tasks = []
    for text in texts:
        data = np.array([[text]], dtype=object)
        inp = async_httpclient.InferInput("text", data.shape, "BYTES")
        inp.set_data_from_numpy(data)
        out = async_httpclient.InferRequestedOutput("embedding")
        tasks.append(client.infer("custom_model", inputs=[inp], outputs=[out]))

    results = await asyncio.gather(*tasks)
    embeddings = [r.as_numpy("embedding") for r in results]
    await client.close()
    return embeddings

embeddings = asyncio.run(batch_infer(["hello world", "triton is fast"]))
```

#### curl example

```bash
# POST inference request (HTTP)
curl -X POST http://localhost:8000/v2/models/resnet50/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "name": "input__0",
        "shape": [1, 3, 224, 224],
        "datatype": "FP32",
        "data": [0.5, 0.5, ...]
      }
    ],
    "outputs": [
      {"name": "output__0"}
    ]
  }'
```

---

### Docker Deployment

#### Standalone docker run

```bash
docker run --gpus '"device=0,1"' \         # Specific GPUs
  --shm-size=10g \                          # Shared memory for large tensors
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v /mnt/models:/models \
  --name triton \
  nvcr.io/nvidia/tritonserver:25.01-py3 \
  tritonserver \
    --model-repository=/models \
    --strict-model-config=false \           # Auto-generate config when possible
    --log-verbose=1 \
    --log-info=true \
    --log-warning=true \
    --exit-on-error=false \                 # Keep server up even if a model fails to load
    --model-control-mode=poll \             # Reload models when repo changes
    --repository-poll-secs=30
```

#### docker-compose with model repository

```yaml
# docker-compose.yml
version: "3.9"

services:
  triton:
    image: nvcr.io/nvidia/tritonserver:25.01-py3
    command: >
      tritonserver
        --model-repository=/models
        --strict-model-config=false
        --log-info=true
        --model-control-mode=poll
        --repository-poll-secs=30
    ports:
      - "8000:8000"    # HTTP
      - "8001:8001"    # gRPC
      - "8002:8002"    # Metrics
    volumes:
      - ./model_repository:/models
      - triton_cache:/tmp/triton_cache
    environment:
      - CUDA_VISIBLE_DEVICES=0,1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/v2/health/ready"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    shm_size: '10g'
    ulimits:
      memlock: -1
      stack: 67108864
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  triton_cache:
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "triton"
    static_configs:
      - targets: ["triton:8002"]    # Triton metrics port
    metrics_path: /metrics
```

---

### Kubernetes Deployment

#### Deployment YAML with GPU

```yaml
# triton-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triton-inference-server
  labels:
    app: triton
spec:
  replicas: 2
  selector:
    matchLabels:
      app: triton
  template:
    metadata:
      labels:
        app: triton
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8002"
        prometheus.io/path: "/metrics"
    spec:
      containers:
        - name: triton
          image: nvcr.io/nvidia/tritonserver:25.01-py3
          command:
            - tritonserver
            - --model-repository=s3://my-bucket/model-repo
            - --strict-model-config=false
            - --log-info=true
            - --exit-on-error=false
          ports:
            - containerPort: 8000
              name: http
            - containerPort: 8001
              name: grpc
            - containerPort: 8002
              name: metrics
          resources:
            limits:
              nvidia.com/gpu: "1"       # 1 GPU per pod
              memory: "32Gi"
              cpu: "8"
            requests:
              nvidia.com/gpu: "1"
              memory: "16Gi"
              cpu: "4"
          readinessProbe:
            httpGet:
              path: /v2/health/ready
              port: 8000
            initialDelaySeconds: 90       # Models need time to load
            periodSeconds: 15
            failureThreshold: 10
          livenessProbe:
            httpGet:
              path: /v2/health/live
              port: 8000
            initialDelaySeconds: 120
            periodSeconds: 30
            failureThreshold: 3
          volumeMounts:
            - mountPath: /dev/shm
              name: shm
          env:
            - name: AWS_DEFAULT_REGION
              value: "us-east-1"
            - name: CUDA_VISIBLE_DEVICES
              value: "0"
      volumes:
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: 10Gi           # Shared memory for large tensor transfers
      nodeSelector:
        accelerator: nvidia-a100     # Target GPU nodes
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule

---
apiVersion: v1
kind: Service
metadata:
  name: triton-service
spec:
  selector:
    app: triton
  ports:
    - name: http
      port: 8000
      targetPort: 8000
    - name: grpc
      port: 8001
      targetPort: 8001
    - name: metrics
      port: 8002
      targetPort: 8002
  type: ClusterIP

---
# Horizontal Pod Autoscaler based on GPU utilization (via custom metrics)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: triton-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: triton-inference-server
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Pods
      pods:
        metric:
          name: triton_gpu_utilization   # Custom metric from Prometheus adapter
        target:
          type: AverageValue
          averageValue: "70"             # Scale when avg GPU util > 70%
```

#### Helm chart (official)

```bash
# Official Triton Helm chart for on-premises K8s
git clone https://github.com/triton-inference-server/server.git
cd server/deploy/k8s-onprem

# Configure values
cat values.yaml                         # Review defaults

# Install
helm install triton . \
  --namespace triton \
  --create-namespace \
  --set replicaCount=3 \
  --set image.tag=25.01-py3 \
  --set modelRepository.path=s3://my-bucket/models \
  --set prometheus.enabled=true \
  --set grafana.enabled=true

# Upgrade
helm upgrade triton . --reuse-values --set replicaCount=5
```

NVIDIA also maintains cloud-specific deployment manifests:
- AWS: `server/deploy/aws/` — EKS + EFS model repository
- GCP: `server/deploy/gcp/` — GKE + GCS model repository

---

### Performance Tooling

#### perf_analyzer — latency and throughput benchmarking

`perf_analyzer` ships inside the Triton server container:

```bash
# Run perf_analyzer from inside the container (or install separately)
docker run --rm --net=host \
  nvcr.io/nvidia/tritonserver:25.01-py3 \
  perf_analyzer \
    -m resnet50 \                         # Model name
    -u localhost:8000 \                   # Server URL
    --concurrency-range 1:16:2 \          # Test concurrency 1, 3, 5, ..., 15
    --measurement-interval 5000 \         # Measure for 5 seconds each
    -b 8 \                                # Batch size
    --percentile=95 \                     # Report P95 latency
    --shape input__0:1,3,224,224

# Output example:
# Concurrency: 4, throughput: 312.5 infer/sec, latency 12774 usec (p95: 15042 usec)
```

Key perf_analyzer flags:
- `--concurrency-range START:END:STEP` — sweep concurrency levels
- `-b N` — batch size
- `--async` — use async API (higher throughput measurement)
- `--streaming` — for streaming models (gRPC)
- `--protocol grpc` — benchmark gRPC path
- `--input-data zero` — use zero tensors (fastest, avoids data prep)

#### Model Analyzer — automatic configuration search

Model Analyzer sweeps config combinations (batch sizes, instance counts, concurrency) to find the optimal configuration:

```bash
pip install triton-model-analyzer

model-analyzer profile \
  --model-repository /models \
  --profile-models resnet50 \
  --triton-launch-mode docker \
  --output-model-repository-path /results/models \
  --export-path /results/reports \
  --gpus all

# Generates a report at /results/reports/resnet50_report.pdf
# with throughput vs latency pareto frontier and recommended config
```

---

### Triton vs vLLM vs TGI — Decision Table

| | **vLLM** | **Triton + TensorRT-LLM** | **Triton (general)** | **TGI** |
|---|---|---|---|---|
| **Best for** | LLM-only API services | Maximum LLM throughput on NVIDIA | Multi-model, CV+NLP pipelines | Legacy HF deployments |
| **Model types** | LLMs only | LLMs only (via TRT-LLM backend) | ANY framework, ANY model type | LLMs + some others |
| **Ease of setup** | Very easy (one command) | Hard (TRT compilation 30min-4hr) | Moderate (config.pbtxt per model) | Easy |
| **Peak LLM throughput** | High | Highest (TRT-LLM ahead at low concurrency) | Depends on backend | Medium |
| **Multi-model serving** | No (one model per instance) | No (TRT-LLM model per server) | Yes — many models simultaneously | No |
| **Model ensembles** | No | Via Triton ensemble | Yes — native DAG pipelines | No |
| **Dynamic batching** | Continuous batching (LLM-native) | Inflight batching | Per-model scheduler queues | Continuous batching |
| **Protocols** | HTTP (OpenAI compat) | HTTP + gRPC + C API | HTTP + gRPC + C API | HTTP (Messages API) |
| **Prometheus metrics** | Basic | Rich (per-model) | Rich (per-model) | Basic |
| **Model warming** | Manual | config.pbtxt ModelWarmup | config.pbtxt ModelWarmup | No |
| **OpenAI compat API** | Yes (native) | Via extra layer | Not native | Yes |
| **Vendor lock-in** | Low (any HF model) | High (NVIDIA TensorRT) | Moderate (NVIDIA recommended) | Low |
| **Status (2026)** | Active, recommended | Active, high performance | Active, enterprise standard | Maintenance mode (Dec 2025) |
| **When to choose** | Default for LLM APIs | When you need max NVIDIA throughput | When serving non-LLM models or pipelines | Avoid for new projects |

---

### Key Features Summary

**Dynamic Batching**
Triton queues incoming requests and combines them into batches server-side. Configured per model via `dynamic_batching {}` in config.pbtxt. Parameters: `preferred_batch_size`, `max_queue_delay_microseconds`, `max_queue_size`. Increases GPU utilization without client changes.

**Concurrent Model Execution**
Multiple models load simultaneously on different GPUs or CPU threads. Instance groups allow multiple copies of the same model (e.g., 4 instances of resnet50 on GPU 0). Triton schedules requests across instances automatically.

**Model Ensemble / DAG**
Chain models as a directed acyclic graph. Tensor passing between steps is zero-copy on same GPU. Single API call runs the entire pipeline. Supports fan-out and fan-in topologies.

**Model Warmup**
Pre-sends tensors to warm up GPU kernels before the server accepts live traffic. Prevents latency spikes on the first production request. Configured in config.pbtxt `model_warmup {}` block.

**Multi-GPU Scheduling**
Assign different models to different GPUs via `instance_group [{ kind: KIND_GPU, gpus: [0, 1] }]`. Or run the same model across multiple GPUs for redundancy.

**Model Control API**
Load, unload, or reload models at runtime without restarting the server:
```bash
# Load a model dynamically
curl -X POST http://localhost:8000/v2/repository/models/resnet50/load

# Unload a model
curl -X POST http://localhost:8000/v2/repository/models/resnet50/unload

# Get all loaded models
curl http://localhost:8000/v2/repository/index
```
Requires `--model-control-mode=explicit` at server start.

**Shared Memory**
For extremely high-throughput scenarios, clients can use POSIX or CUDA shared memory to pass tensors without HTTP/gRPC serialization overhead. Significant latency reduction for large tensors on the same host.

---

### Production Patterns

#### Health checks (liveness vs readiness)

```bash
# Liveness — is the process alive?
GET /v2/health/live
# Returns 200 if server process is running (even if models are loading)

# Readiness — is the server ready to serve?
GET /v2/health/ready
# Returns 200 only when all models are fully loaded

# Model-specific readiness
GET /v2/models/resnet50/ready
# Returns 200 when resnet50 is ready, 503 otherwise
```

**K8s pattern:** Use `livenessProbe` → `/v2/health/live`, `readinessProbe` → `/v2/health/ready`. Increase `initialDelaySeconds` to account for model load time (TensorRT engines can take 2-5 minutes to compile on first load).

#### Prometheus metrics

Key metrics exported at `http://triton:8002/metrics`:

```
# Inference metrics (per model)
nv_inference_request_success{model="resnet50"}          # Total successful requests
nv_inference_request_failure{model="resnet50"}          # Total failed requests
nv_inference_count{model="resnet50"}                    # Total inference samples
nv_inference_exec_count{model="resnet50"}               # Execution count (may differ if batched)
nv_inference_request_duration_us{model="resnet50"}      # Total request time (microseconds)
nv_inference_queue_duration_us{model="resnet50"}        # Time spent in queue
nv_inference_compute_input_duration_us{model="resnet50"}
nv_inference_compute_infer_duration_us{model="resnet50"}
nv_inference_compute_output_duration_us{model="resnet50"}

# GPU metrics
nv_gpu_utilization{gpu_uuid="..."}                     # GPU utilization %
nv_gpu_memory_total_bytes{gpu_uuid="..."}
nv_gpu_memory_used_bytes{gpu_uuid="..."}
nv_gpu_power_usage{gpu_uuid="..."}

# Cache metrics
nv_cache_hit_count
nv_cache_miss_count
```

#### Grafana alert rules

```yaml
# prometheus-alerts.yaml
groups:
  - name: triton
    rules:
      - alert: TritonHighQueueLatency
        expr: |
          rate(nv_inference_queue_duration_us[5m]) /
          rate(nv_inference_exec_count[5m]) > 50000
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Triton queue latency > 50ms — increase replicas or batch size"

      - alert: TritonHighGPUMemory
        expr: |
          nv_gpu_memory_used_bytes / nv_gpu_memory_total_bytes > 0.95
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "GPU memory > 95% — risk of OOM"

      - alert: TritonDown
        expr: up{job="triton"} == 0
        for: 1m
        annotations:
          summary: "Triton instance is down"
```

#### Rate limiting (nginx in front of Triton)

```nginx
# nginx.conf — rate limiting for Triton
limit_req_zone $binary_remote_addr zone=triton_limit:10m rate=100r/s;

upstream triton_backend {
    least_conn;
    server triton-1:8000;
    server triton-2:8000;
    keepalive 64;
}

server {
    listen 80;

    location /v2/models/ {
        limit_req zone=triton_limit burst=200 nodelay;
        proxy_pass http://triton_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_read_timeout 120s;
        proxy_buffering off;
    }

    location /v2/health/ {
        proxy_pass http://triton_backend;
        proxy_read_timeout 5s;
    }
}
```

#### Optimization tips

| Situation | Recommendation |
|-----------|---------------|
| Low GPU utilization | Increase `preferred_batch_size` and `max_queue_delay_microseconds` |
| High P99 latency | Reduce `max_queue_delay_microseconds` to 1000-2000 µs |
| Multiple models, uneven load | Use `instance_group count` to add more copies of hot models |
| Large input tensors | Use CUDA shared memory to bypass gRPC serialization |
| Cold start latency spikes | Add `model_warmup` config to all models |
| ONNX model too slow | Enable TensorRT execution accelerator in config.pbtxt |
| CPU bottleneck for preprocessing | Move preprocessing to Python backend with `KIND_CPU, count: 4` |
| Multi-GPU, single large model | Use TensorRT-LLM backend with tensor parallelism |

---

### Common Server Startup Flags

```bash
tritonserver \
  --model-repository=/models \            # Required: model repo path (local, NFS, S3, GCS)
  --strict-model-config=false \           # Auto-complete partial config.pbtxt
  --log-verbose=1 \                       # Verbose logging level (0-3)
  --log-info=true \                       # INFO level logs
  --exit-on-error=false \                 # Don't crash if one model fails
  --model-control-mode=poll \             # Options: none | poll | explicit
  --repository-poll-secs=30 \             # How often to check for model changes
  --allow-metrics=true \                  # Enable Prometheus metrics
  --metrics-interval-ms=2000 \            # Metrics collection interval
  --allow-gpu-metrics=true \              # Include GPU metrics
  --http-port=8000 \
  --grpc-port=8001 \
  --metrics-port=8002 \
  --min-supported-compute-capability=6.0  # Minimum GPU compute capability
```

---

Sources:
- [NVIDIA Triton Inference Server Documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html)
- [Model Configuration Reference](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html)
- [Triton Server GitHub Releases](https://github.com/triton-inference-server/server/releases)
- [Triton K8s On-Prem Deploy](https://github.com/triton-inference-server/server/blob/main/deploy/k8s-onprem/README.md)
- [LLM Inference Servers Compared 2026 — PremAI](https://blog.premai.io/llm-inference-servers-compared-vllm-vs-tgi-vs-sglang-vs-triton-2026/)
- [GPU Inference Servers Comparison — Niradler](https://blog.niradler.com/gpu-inference-servers-comparison-triton-vs-tgi-vs-vllm-vs-ollama)
- [Triton vs vLLM Comparison — Clarifai](https://www.clarifai.com/blog/model-serving-framework/)
- [Triton Inference Server Performance Tuning](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/performance_tuning.html)

