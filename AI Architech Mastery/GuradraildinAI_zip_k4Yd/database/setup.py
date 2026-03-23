"""
Database setup script — run the SQL below in the Supabase SQL Editor
(Dashboard > SQL Editor > New Query) to create all required tables.

This script also prints the SQL for convenience.
"""

SCHEMA_SQL = """
-- Students table
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

-- Courses table
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

-- Transactions table (student course enrollments / payments)
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

-- Monitoring / guardrail logs table
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

-- Indexes for performance
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


def print_schema():
    print("=" * 60)
    print("  Copy and run this SQL in your Supabase SQL Editor:")
    print("=" * 60)
    print(SCHEMA_SQL)


if __name__ == "__main__":
    print_schema()
