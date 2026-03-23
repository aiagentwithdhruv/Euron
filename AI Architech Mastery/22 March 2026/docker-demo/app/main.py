"""
Docker Demo — Simple app that connects to PostgreSQL + Redis.
Focus: Understanding Docker, not business logic.
"""

from fastapi import FastAPI
import psycopg2
import redis
import os

app = FastAPI(title="Docker Demo")

# Read config from environment (Docker Compose will inject these)
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "demo")
DB_PASS = os.getenv("DB_PASS", "demo123")
DB_NAME = os.getenv("DB_NAME", "demodb")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")


def get_db():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


@app.on_event("startup")
def setup():
    """Create a simple table on startup."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            visited_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.get("/")
def hello():
    """Simple hello — proves Python container is running."""
    return {"message": "Hello from Docker! 🐳"}


@app.get("/db")
def test_db():
    """Insert + read from PostgreSQL — proves DB container works."""
    conn = get_db()
    cur = conn.cursor()

    # Insert a visitor
    cur.execute("INSERT INTO visitors (name) VALUES ('docker-user') RETURNING id, visited_at")
    row = cur.fetchone()
    conn.commit()

    # Count total visitors
    cur.execute("SELECT COUNT(*) FROM visitors")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "source": "PostgreSQL Container",
        "visitor_id": row[0],
        "visited_at": str(row[1]),
        "total_visitors": count
    }


@app.get("/cache")
def test_redis():
    """Increment a counter in Redis — proves Redis container works."""
    r = get_redis()
    count = r.incr("hit_counter")
    return {
        "source": "Redis Container",
        "hit_count": count,
        "message": f"This page has been visited {count} times"
    }


@app.get("/both")
def test_both():
    """Use both DB and Redis together — proves all 3 containers talk."""
    # Redis: increment and cache
    r = get_redis()
    hits = r.incr("both_counter")

    # DB: insert visitor
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO visitors (name) VALUES (%s) RETURNING id", (f"visitor-{hits}",))
    visitor_id = cur.fetchone()[0]
    conn.commit()

    # Cache the latest visitor in Redis
    r.set("latest_visitor", f"visitor-{hits} (id={visitor_id})")
    latest = r.get("latest_visitor")

    cur.close()
    conn.close()

    return {
        "python_container": "Running ✅",
        "postgres_container": f"Inserted visitor id={visitor_id} ✅",
        "redis_container": f"Hit count={hits}, cached={latest} ✅",
        "docker_compose": "All 3 containers talking to each other ✅"
    }


@app.get("/health")
def health():
    """Health check — Docker uses this to know if container is healthy."""
    status = {"python": "up"}
    try:
        conn = get_db()
        conn.close()
        status["postgres"] = "up"
    except Exception:
        status["postgres"] = "down"
    try:
        r = get_redis()
        r.ping()
        status["redis"] = "up"
    except Exception:
        status["redis"] = "down"
    return status
