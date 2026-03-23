"""
Bootstrap tables via Supabase HTTP SQL endpoints.
Tries multiple API paths that Supabase may expose for SQL execution.
"""
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

import httpx
import config

PROJECT_REF = config.SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")
BASE = config.SUPABASE_URL
SERVICE_KEY = config.SUPABASE_SERVICE_KEY
ANON_KEY = config.SUPABASE_KEY

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    date_of_birth DATE,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    major TEXT,
    gpa NUMERIC(3,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS courses (
    id BIGSERIAL PRIMARY KEY,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    department TEXT NOT NULL,
    credits INTEGER NOT NULL DEFAULT 3,
    max_enrollment INTEGER DEFAULT 50,
    current_enrollment INTEGER DEFAULT 0,
    instructor TEXT,
    semester TEXT NOT NULL,
    fee NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES students(id),
    course_id BIGINT REFERENCES courses(id),
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('enrollment','payment','refund','scholarship')),
    amount NUMERIC(10,2) NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','completed','failed','refunded')),
    payment_method TEXT CHECK (payment_method IN ('credit_card','debit_card','bank_transfer','scholarship','cash')),
    transaction_date TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS guardrail_logs (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    user_input TEXT,
    sanitized_input TEXT,
    guardrail_layer TEXT NOT NULL,
    guardrail_name TEXT NOT NULL,
    action TEXT NOT NULL,
    details JSONB,
    tool_called TEXT,
    tool_allowed BOOLEAN,
    llm_raw_output TEXT,
    llm_final_output TEXT,
    hallucination_flag BOOLEAN DEFAULT FALSE,
    blocked BOOLEAN DEFAULT FALSE,
    execution_time_ms NUMERIC(10,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_students_major ON students(major);
CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(course_code);
CREATE INDEX IF NOT EXISTS idx_courses_dept ON courses(department);
CREATE INDEX IF NOT EXISTS idx_transactions_student ON transactions(student_id);
CREATE INDEX IF NOT EXISTS idx_transactions_course ON transactions(course_id);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_guardrail_logs_session ON guardrail_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_guardrail_logs_layer ON guardrail_logs(guardrail_layer);
CREATE INDEX IF NOT EXISTS idx_guardrail_logs_ts ON guardrail_logs(timestamp);
"""

RPC_SQL = """
CREATE OR REPLACE FUNCTION execute_readonly_query(query_text TEXT)
RETURNS JSONB LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE result JSONB;
BEGIN
    IF NOT (UPPER(TRIM(query_text)) LIKE 'SELECT%%') THEN
        RAISE EXCEPTION 'Only SELECT queries are allowed';
    END IF;
    EXECUTE 'SELECT COALESCE(jsonb_agg(row_to_json(t)), ''[]''::jsonb) FROM (' || query_text || ') t' INTO result;
    RETURN result;
END; $$;
"""


def try_endpoint(client, url, payload, desc):
    print(f"  [{desc}] POST {url[:80]}...", end=" ")
    try:
        r = client.post(url, json=payload, timeout=15)
        print(f"Status: {r.status_code}")
        if r.status_code < 300:
            print(f"    Response: {r.text[:200]}")
            return True
        else:
            print(f"    Error: {r.text[:150]}")
    except Exception as e:
        print(f"Exception: {str(e)[:80]}")
    return False


def main():
    print(f"Project: {PROJECT_REF}")
    print(f"Base URL: {BASE}\n")

    headers_service = {
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json",
    }
    headers_anon = {
        "apikey": ANON_KEY if ANON_KEY else SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json",
    }

    client = httpx.Client(headers=headers_service, follow_redirects=True)

    endpoints = [
        (f"{BASE}/pg/query", {"query": "SELECT 1 as test"}, "pg/query with query key"),
        (f"{BASE}/pg/query", {"sql": "SELECT 1 as test"}, "pg/query with sql key"),
        (f"{BASE}/pg", {"query": "SELECT 1 as test"}, "pg root"),
        (f"{BASE}/rest/v1/rpc/exec_sql", {"sql": "SELECT 1 as test"}, "rpc/exec_sql"),
        (f"{BASE}/sql", {"query": "SELECT 1 as test"}, "sql endpoint"),
        (f"{BASE}/database/query", {"query": "SELECT 1 as test"}, "database/query"),
        (f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query", {"query": "SELECT 1 as test"}, "management API"),
    ]

    working_endpoint = None
    for url, payload, desc in endpoints:
        if try_endpoint(client, url, payload, desc):
            working_endpoint = (url, desc)
            break

    if working_endpoint:
        url, desc = working_endpoint
        print(f"\nWorking endpoint found: {desc}")
        print("Creating tables...")
        key = "query" if "query" in endpoints[0][1] else "sql"
        try_endpoint(client, url, {key: SCHEMA_SQL}, "CREATE TABLES")
        try_endpoint(client, url, {key: RPC_SQL}, "CREATE RPC FUNCTION")
        try_endpoint(client, url, {key: "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"}, "VERIFY")
    else:
        print("\nNo working SQL endpoint found via HTTP.")
        print("Supabase does not expose raw SQL execution through the REST API.")
        print("\nFallback: Will create tables by inserting into them directly.")
        print("(PostgREST auto-creates are not supported, but we can test with existing schema)")

    client.close()


if __name__ == "__main__":
    main()
