"""
LangChain tools for the university database agent.
Each tool queries Supabase and returns structured results.
"""

from langchain.tools import tool
from database.connection import get_client
import config


@tool
def query_students(query_filter: str = "") -> str:
    """Query the students table. Accepts a natural language filter description.
    Returns student records matching the criteria.
    Examples: 'all active students', 'students with GPA above 3.5',
    'students majoring in Computer Science'."""
    client = get_client()
    q = client.table("students").select("*")

    filter_lower = query_filter.lower()
    if "active" in filter_lower:
        q = q.eq("is_active", True)
    if "inactive" in filter_lower:
        q = q.eq("is_active", False)

    for major in config.ALLOWED_TABLES:
        pass

    majors = [
        "Computer Science", "Mathematics", "Physics", "Biology", "Chemistry",
        "English Literature", "History", "Economics", "Business Administration",
        "Psychology", "Mechanical Engineering", "Electrical Engineering",
        "Civil Engineering", "Data Science", "Philosophy",
    ]
    for m in majors:
        if m.lower() in filter_lower:
            q = q.eq("major", m)
            break

    q = q.limit(config.MAX_QUERY_ROWS)
    result = q.execute()
    rows = result.data
    if not rows:
        return "No students found matching the criteria."
    return f"Found {len(rows)} student(s):\n" + "\n".join(
        f"- {r['first_name']} {r['last_name']} | Email: {r['email']} | Major: {r['major']} | GPA: {r['gpa']} | Active: {r['is_active']}"
        for r in rows
    )


@tool
def query_courses(query_filter: str = "") -> str:
    """Query the courses table. Accepts a natural language filter description.
    Returns course records matching the criteria.
    Examples: 'all active courses', 'courses in Engineering department',
    'courses with fee below 2000'."""
    client = get_client()
    q = client.table("courses").select("*")

    filter_lower = query_filter.lower()
    if "active" in filter_lower:
        q = q.eq("is_active", True)

    departments = [
        "Computer Science", "Mathematics", "Natural Sciences", "Humanities",
        "Business", "Engineering", "Social Sciences", "Arts",
    ]
    for d in departments:
        if d.lower() in filter_lower:
            q = q.eq("department", d)
            break

    semesters = ["Fall 2024", "Spring 2025", "Summer 2025", "Fall 2025", "Spring 2026"]
    for s in semesters:
        if s.lower() in filter_lower:
            q = q.eq("semester", s)
            break

    q = q.limit(config.MAX_QUERY_ROWS)
    result = q.execute()
    rows = result.data
    if not rows:
        return "No courses found matching the criteria."
    return f"Found {len(rows)} course(s):\n" + "\n".join(
        f"- {r['course_code']}: {r['course_name']} | Dept: {r['department']} | Credits: {r['credits']} | Fee: ${r['fee']} | Semester: {r['semester']} | Instructor: {r['instructor']}"
        for r in rows
    )


@tool
def query_transactions(query_filter: str = "") -> str:
    """Query the transactions table. Accepts a natural language filter description.
    Returns transaction records matching the criteria.
    Examples: 'all completed payments', 'scholarship transactions',
    'refund transactions', 'pending enrollments'."""
    client = get_client()
    q = client.table("transactions").select("*, students(first_name, last_name), courses(course_code, course_name)")

    filter_lower = query_filter.lower()
    types = ["enrollment", "payment", "refund", "scholarship"]
    for t in types:
        if t in filter_lower:
            q = q.eq("transaction_type", t)
            break

    statuses = ["pending", "completed", "failed", "refunded"]
    for s in statuses:
        if s in filter_lower:
            q = q.eq("status", s)
            break

    q = q.limit(config.MAX_QUERY_ROWS)
    result = q.execute()
    rows = result.data
    if not rows:
        return "No transactions found matching the criteria."
    return f"Found {len(rows)} transaction(s):\n" + "\n".join(
        f"- ID:{r['id']} | Student: {r.get('students', {}).get('first_name', 'N/A')} {r.get('students', {}).get('last_name', '')} | Course: {r.get('courses', {}).get('course_code', 'N/A')} | Type: {r['transaction_type']} | Amount: ${r['amount']} | Status: {r['status']} | Method: {r['payment_method']}"
        for r in rows
    )


@tool
def get_table_schema(table_name: str) -> str:
    """Get the schema/column info for a given table.
    Allowed tables: students, courses, transactions."""
    schemas = {
        "students": (
            "Table: students\n"
            "Columns: id (bigint PK), first_name (text), last_name (text), "
            "email (text unique), date_of_birth (date), enrollment_date (date), "
            "major (text), gpa (numeric 3,2), is_active (boolean), created_at (timestamptz)"
        ),
        "courses": (
            "Table: courses\n"
            "Columns: id (bigint PK), course_code (text unique), course_name (text), "
            "department (text), credits (integer), max_enrollment (integer), "
            "current_enrollment (integer), instructor (text), semester (text), "
            "fee (numeric 10,2), is_active (boolean), created_at (timestamptz)"
        ),
        "transactions": (
            "Table: transactions\n"
            "Columns: id (bigint PK), student_id (bigint FK->students), "
            "course_id (bigint FK->courses), transaction_type (text: enrollment/payment/refund/scholarship), "
            "amount (numeric 10,2), status (text: pending/completed/failed/refunded), "
            "payment_method (text: credit_card/debit_card/bank_transfer/scholarship/cash), "
            "transaction_date (timestamptz), notes (text), created_at (timestamptz)"
        ),
    }
    if table_name.lower() not in schemas:
        return f"Table '{table_name}' not found. Available tables: students, courses, transactions."
    return schemas[table_name.lower()]


@tool
def run_custom_query(sql: str) -> str:
    """Execute a custom SELECT SQL query against the database.
    ONLY SELECT queries with LIMIT are allowed. Maximum LIMIT is 100.
    The query must only reference tables: students, courses, transactions.
    Example: SELECT major, COUNT(*) as count FROM students GROUP BY major LIMIT 20"""
    from guardrails.execution import ExecutionGuardrail

    exec_guard = ExecutionGuardrail()
    checks = exec_guard.validate_sql(sql)
    if exec_guard.is_sql_blocked(checks):
        reasons = [c.reason for c in checks if not c.passed]
        return f"Query blocked by execution guardrail: {'; '.join(reasons)}"

    try:
        client = get_client()
        result = client.rpc("execute_readonly_query", {"query_text": sql}).execute()
        rows = result.data
        if not rows:
            return "Query returned no results."
        header = " | ".join(rows[0].keys())
        lines = [header, "-" * len(header)]
        for r in rows:
            lines.append(" | ".join(str(v) for v in r.values()))
        return f"Query returned {len(rows)} row(s):\n" + "\n".join(lines)
    except Exception as e:
        return f"Query execution error: {str(e)}"


ALL_TOOLS = [query_students, query_courses, query_transactions, get_table_schema, run_custom_query]
