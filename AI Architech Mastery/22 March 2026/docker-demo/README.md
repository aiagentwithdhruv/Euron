# Docker Demo — 3 Containers with Docker Compose

## What This Demonstrates

```
┌──────────────────────────────────────────────────┐
│              Docker Compose                       │
│                                                   │
│  ┌─────────────┐  ┌──────────┐  ┌─────────────┐ │
│  │  Python App  │  │ Postgres │  │   Redis     │ │
│  │  (FastAPI)   │──│   (DB)   │  │  (Cache)    │ │
│  │  port 8000   │  │ port 5432│  │  port 6379  │ │
│  └─────────────┘  └──────────┘  └─────────────┘ │
│         │               │              │          │
│         └───────── demo-network ───────┘          │
│                                                   │
│  Volume: pgdata (persists DB data)                │
└──────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Start all 3 containers
docker compose up -d --build

# Check all containers are running
docker compose ps

# Test the endpoints
curl http://localhost:8000/          # Python container
curl http://localhost:8000/db        # PostgreSQL container
curl http://localhost:8000/cache     # Redis container
curl http://localhost:8000/both      # All 3 talking together
curl http://localhost:8000/health    # Health of all services

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Stop and delete all data
docker compose down -v
```

## Endpoints

| Endpoint | What it tests |
|----------|--------------|
| `/` | Python container is running |
| `/db` | Python ↔ PostgreSQL connection |
| `/cache` | Python ↔ Redis connection |
| `/both` | All 3 containers communicating |
| `/health` | Health status of all services |

## Docker Concepts Demonstrated

1. **Dockerfile** — How to build a custom image
2. **docker-compose.yml** — Orchestrate multiple containers
3. **Services** — Each container is a service (app, db, redis)
4. **Networks** — Containers talk via service names (DNS)
5. **Volumes** — Persist data beyond container lifecycle
6. **Health Checks** — Docker monitors container health
7. **depends_on** — Start order with health conditions
8. **Environment Variables** — Configure containers without code changes
9. **Port Mapping** — Expose container ports to host
10. **Pre-built vs Custom Images** — postgres/redis (pre-built) vs app (custom Dockerfile)
