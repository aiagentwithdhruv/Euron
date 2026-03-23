"""Create tables in Supabase using direct PostgreSQL connection via psycopg2."""
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

import httpx
import config

SCHEMA_SQL_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS students (
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
    )""",
    """CREATE TABLE IF NOT EXISTS courses (
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
    )""",
    """CREATE TABLE IF NOT EXISTS transactions (
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
    )""",
    """CREATE TABLE IF NOT EXISTS guardrail_logs (
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
    )""",
    "CREATE INDEX IF NOT EXISTS idx_students_email ON students(email)",
    "CREATE INDEX IF NOT EXISTS idx_students_major ON students(major)",
    "CREATE INDEX IF NOT EXISTS idx_courses_code ON courses(course_code)",
    "CREATE INDEX IF NOT EXISTS idx_courses_dept ON courses(department)",
    "CREATE INDEX IF NOT EXISTS idx_transactions_student ON transactions(student_id)",
    "CREATE INDEX IF NOT EXISTS idx_transactions_course ON transactions(course_id)",
    "CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type)",
    "CREATE INDEX IF NOT EXISTS idx_guardrail_logs_session ON guardrail_logs(session_id)",
    "CREATE INDEX IF NOT EXISTS idx_guardrail_logs_layer ON guardrail_logs(guardrail_layer)",
    "CREATE INDEX IF NOT EXISTS idx_guardrail_logs_ts ON guardrail_logs(timestamp)",
]

RPC_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION execute_readonly_query(query_text TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result JSONB;
BEGIN
    IF NOT (UPPER(TRIM(query_text)) LIKE 'SELECT%') THEN
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


def print_full_sql():
    print("=" * 70)
    print("  COPY ALL SQL BELOW INTO SUPABASE SQL EDITOR AND RUN IT")
    print("  (Dashboard -> SQL Editor -> New Query -> Paste -> Run)")
    print("=" * 70)
    print()
    for stmt in SCHEMA_SQL_STATEMENTS:
        print(stmt + ";")
        print()
    print(RPC_FUNCTION_SQL)
    print("=" * 70)


if __name__ == "__main__":
    print_full_sql()
