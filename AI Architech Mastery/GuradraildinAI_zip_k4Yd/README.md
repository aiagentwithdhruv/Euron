# University Database Agent with 6-Layer Guardrails

An agentic chat system that lets users interact with a university database (students, courses, transactions) via natural language. Built with LangChain, FastAPI, Streamlit, Supabase, and the Euri (OpenAI-compatible) LLM.

## Architecture

```
User (Streamlit) → FastAPI → Guardrail Pipeline → LangChain Agent → Supabase
                                                        ↓
                                              Euri LLM (gpt-4.1-nano)
```

### 6 Guardrail Layers

| Layer | Purpose |
|-------|---------|
| **Policy** | Role-based access control, rate limiting, operation policies, data scope enforcement |
| **Input** | SQL injection detection, prompt injection detection, PII redaction, input validation |
| **Instructional** | Topic relevance, role deviation prevention, instruction extraction blocking |
| **Execution** | Tool access control, SQL validation (type, keywords, tables, row limits) |
| **Output** | Sensitive data filtering, hallucination detection, response length, instruction leak prevention |
| **Monitoring** | Full pipeline logging to `guardrail_logs` table for audit and analysis |

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Create a project at [supabase.com](https://supabase.com)
2. Copy your project URL and keys
3. Update `.env`:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
```

### 3. Create database tables

Run the SQL from `database/setup.py` in your Supabase SQL Editor:

```bash
python -m database.setup
```

This prints the SQL — copy it into **Supabase Dashboard → SQL Editor → New Query** and run it.

### 4. Create the RPC function

Run the SQL in `database/rpc_function.sql` in the Supabase SQL Editor.

### 5. Seed the database (1080 records)

```bash
python -m database.seed
```

### 6. Start the backend

```bash
python -m backend.api
```

The FastAPI server runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### 7. Start the frontend

```bash
streamlit run frontend/app.py
```

Opens at `http://localhost:8501`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/chat` | Send a message to the guarded agent |
| GET | `/health` | Health check |
| GET | `/guardrails/info` | List all guardrail layers and descriptions |

## Monitoring

Every interaction is logged to the `guardrail_logs` table with:
- User input and sanitized input
- Which guardrail layer processed it
- Whether it was blocked and why
- Which tools were called and whether they were allowed
- LLM raw and filtered output
- Hallucination flags
- Execution timing
