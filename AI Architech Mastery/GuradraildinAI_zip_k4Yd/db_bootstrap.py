"""
Bootstrap: create all tables and seed data directly via PostgreSQL connection.
Tries multiple Supabase connection methods automatically.
"""
import sys, os
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

import psycopg2
import config

PROJECT_REF = config.SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")

CONNECTION_ATTEMPTS = [
    {
        "desc": "Direct connection (session mode via pooler, port 5432)",
        "host": f"aws-0-ap-south-1.pooler.supabase.com",
        "port": 5432,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Transaction mode pooler (port 6543)",
        "host": f"aws-0-ap-south-1.pooler.supabase.com",
        "port": 6543,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Direct DB host",
        "host": f"db.{PROJECT_REF}.supabase.co",
        "port": 5432,
        "user": "postgres",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Pooler us-east-1 session",
        "host": f"aws-0-us-east-1.pooler.supabase.com",
        "port": 5432,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Pooler us-east-1 transaction",
        "host": f"aws-0-us-east-1.pooler.supabase.com",
        "port": 6543,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Pooler us-west-1 session",
        "host": f"aws-0-us-west-1.pooler.supabase.com",
        "port": 5432,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Pooler eu-west-1 session",
        "host": f"aws-0-eu-west-1.pooler.supabase.com",
        "port": 5432,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Pooler eu-central-1 session",
        "host": f"aws-0-eu-central-1.pooler.supabase.com",
        "port": 5432,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
    {
        "desc": "Pooler ap-southeast-1 session",
        "host": f"aws-0-ap-southeast-1.pooler.supabase.com",
        "port": 5432,
        "user": f"postgres.{PROJECT_REF}",
        "password": config.SUPABASE_SERVICE_KEY,
        "dbname": "postgres",
    },
]

# Also try with the anon key (SUPABASE_KEY) in case it's actually the password
if config.SUPABASE_KEY and not config.SUPABASE_KEY.startswith("ey"):
    for region in ["ap-south-1", "us-east-1"]:
        CONNECTION_ATTEMPTS.append({
            "desc": f"Pooler {region} with publishable key as password",
            "host": f"aws-0-{region}.pooler.supabase.com",
            "port": 5432,
            "user": f"postgres.{PROJECT_REF}",
            "password": config.SUPABASE_KEY,
            "dbname": "postgres",
        })


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

CREATE OR REPLACE FUNCTION execute_readonly_query(query_text TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result JSONB;
BEGIN
    IF NOT (UPPER(TRIM(query_text)) LIKE 'SELECT%%') THEN
        RAISE EXCEPTION 'Only SELECT queries are allowed';
    END IF;
    IF query_text ~* '\\b(DROP|ALTER|TRUNCATE|DELETE|UPDATE|INSERT|CREATE)\\b' THEN
        RAISE EXCEPTION 'Blocked SQL operation detected';
    END IF;
    EXECUTE 'SELECT COALESCE(jsonb_agg(row_to_json(t)), ''[]''::jsonb) FROM (' || query_text || ') t'
    INTO result;
    RETURN result;
END;
$$;
"""


def try_connect():
    """Try all connection methods and return the first working connection."""
    for attempt in CONNECTION_ATTEMPTS:
        desc = attempt.pop("desc")
        print(f"  Trying: {desc} ({attempt['host']}:{attempt['port']})...", end=" ")
        try:
            conn = psycopg2.connect(**attempt, connect_timeout=8, sslmode="require")
            print("CONNECTED!")
            return conn
        except Exception as e:
            err_msg = str(e).strip().split('\n')[0][:80]
            print(f"failed ({err_msg})")
        finally:
            attempt["desc"] = desc
    return None


def create_tables(conn):
    print("\nCreating tables...")
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
    conn.commit()
    print("  All tables and indexes created successfully.")


def verify_tables(conn):
    print("\nVerifying tables...")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('students', 'courses', 'transactions', 'guardrail_logs')
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cur.fetchall()]
    print(f"  Found tables: {tables}")
    return tables


if __name__ == "__main__":
    print(f"Project ref: {PROJECT_REF}")
    print(f"Trying to connect to Supabase PostgreSQL...\n")

    conn = try_connect()
    if conn is None:
        print("\nAll connection attempts failed.")
        print("This likely means the database password is different from the API keys.")
        print("Please provide your Supabase database password, or run the SQL manually.")
        sys.exit(1)

    try:
        create_tables(conn)
        tables = verify_tables(conn)
        if len(tables) == 4:
            print("\nAll 4 tables created. Ready to seed data!")
        else:
            print(f"\nWARNING: Expected 4 tables, found {len(tables)}.")
    finally:
        conn.close()
