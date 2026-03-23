"""
Policy Layer Guardrail
Strict role-based access control:
  - Student: basic data queries only (own domain), no schema, no sensitive fields, no custom SQL
  - Admin: full access to all tables, schema, custom SQL, monitoring data
  - Viewer: read-only on students (limited) and courses, no transactions, no schema, no custom SQL
"""

import time
import re
from dataclasses import dataclass, field
import config


@dataclass
class PolicyResult:
    allowed: bool
    reason: str
    policy_name: str
    details: dict = field(default_factory=dict)


ROLE_PERMISSIONS = {
    "student": {
        "allowed_tables": {"students", "courses", "transactions"},
        "allowed_ops": {"SELECT"},
        "allowed_tools": {"query_students", "query_courses", "query_transactions"},
        "blocked_tools": {"get_table_schema", "run_custom_query"},
        "can_view_schema": False,
        "can_view_emails": False,
        "can_view_dob": False,
        "can_view_gpa": True,
        "can_view_financial": False,
        "can_access_monitoring": False,
        "description": "Student: can query basic student/course info and own transactions. No schema, no emails, no financial details.",
    },
    "admin": {
        "allowed_tables": {"students", "courses", "transactions", "guardrail_logs"},
        "allowed_ops": {"SELECT"},
        "allowed_tools": {"query_students", "query_courses", "query_transactions", "get_table_schema", "run_custom_query"},
        "blocked_tools": set(),
        "can_view_schema": True,
        "can_view_emails": True,
        "can_view_dob": True,
        "can_view_gpa": True,
        "can_view_financial": True,
        "can_access_monitoring": True,
        "description": "Admin: full access to all data, schema, custom queries, and monitoring logs.",
    },
    "viewer": {
        "allowed_tables": {"students", "courses"},
        "allowed_ops": {"SELECT"},
        "allowed_tools": {"query_students", "query_courses"},
        "blocked_tools": {"query_transactions", "get_table_schema", "run_custom_query"},
        "can_view_schema": False,
        "can_view_emails": False,
        "can_view_dob": False,
        "can_view_gpa": False,
        "can_view_financial": False,
        "can_access_monitoring": False,
        "description": "Viewer: read-only access to student names/majors and course listings. No transactions, no sensitive fields.",
    },
}

SCHEMA_KEYWORDS = [
    "schema", "column", "columns", "structure", "table structure",
    "describe table", "table definition", "field", "fields",
    "data type", "datatype", "primary key", "foreign key",
]

SENSITIVE_DATA_KEYWORDS = {
    "email": ["email", "e-mail", "mail address", "contact info"],
    "dob": ["date of birth", "dob", "birthday", "birth date", "age"],
    "financial": ["amount", "fee", "payment", "refund", "tuition", "cost", "price", "financial", "money", "scholarship amount", "transaction amount"],
    "gpa": ["gpa", "grade point", "grades", "academic score"],
}


class PolicyGuardrail:

    def __init__(self):
        self._request_timestamps: dict[str, list[float]] = {}
        self.rate_limit_window = 60
        self.rate_limit_max = 30

    def get_permissions(self, role: str) -> dict:
        return ROLE_PERMISSIONS.get(role, {})

    def check_all(self, user_input: str, role: str = "student", session_id: str = "") -> list[PolicyResult]:
        results = []
        results.append(self.check_role_permission(role))
        results.append(self.check_rate_limit(session_id))
        results.append(self.check_schema_access(user_input, role))
        results.append(self.check_sensitive_data_access(user_input, role))
        results.append(self.check_table_access(user_input, role))
        results.append(self.check_operation_policy(user_input))
        return results

    def is_blocked(self, results: list[PolicyResult]) -> bool:
        return any(not r.allowed for r in results)

    def check_role_permission(self, role: str) -> PolicyResult:
        if role not in ROLE_PERMISSIONS:
            return PolicyResult(
                allowed=False,
                reason=f"Unknown role '{role}'. Access denied.",
                policy_name="role_permission",
                details={"role": role},
            )
        perms = ROLE_PERMISSIONS[role]
        return PolicyResult(
            allowed=True,
            reason=f"Role '{role}' recognized. {perms['description']}",
            policy_name="role_permission",
            details={"role": role},
        )

    def check_rate_limit(self, session_id: str) -> PolicyResult:
        now = time.time()
        if session_id not in self._request_timestamps:
            self._request_timestamps[session_id] = []

        self._request_timestamps[session_id] = [
            t for t in self._request_timestamps[session_id]
            if now - t < self.rate_limit_window
        ]

        if len(self._request_timestamps[session_id]) >= self.rate_limit_max:
            return PolicyResult(
                allowed=False,
                reason=f"Rate limit exceeded: {self.rate_limit_max} requests per {self.rate_limit_window}s.",
                policy_name="rate_limit",
                details={"count": len(self._request_timestamps[session_id])},
            )

        self._request_timestamps[session_id].append(now)
        return PolicyResult(
            allowed=True,
            reason="Within rate limit.",
            policy_name="rate_limit",
            details={"count": len(self._request_timestamps[session_id])},
        )

    def check_schema_access(self, user_input: str, role: str) -> PolicyResult:
        perms = ROLE_PERMISSIONS.get(role, {})
        if perms.get("can_view_schema", False):
            return PolicyResult(
                allowed=True,
                reason="Schema access permitted for this role.",
                policy_name="schema_access",
                details={"role": role},
            )

        input_lower = user_input.lower()
        for keyword in SCHEMA_KEYWORDS:
            if keyword in input_lower:
                return PolicyResult(
                    allowed=False,
                    reason=f"Schema/structure access denied for role '{role}'. Only admins can view database schema details. Try asking about the data instead.",
                    policy_name="schema_access",
                    details={"role": role, "matched_keyword": keyword},
                )

        return PolicyResult(
            allowed=True,
            reason="No schema access attempted.",
            policy_name="schema_access",
            details={"role": role},
        )

    def check_sensitive_data_access(self, user_input: str, role: str) -> PolicyResult:
        perms = ROLE_PERMISSIONS.get(role, {})
        input_lower = user_input.lower()
        violations = []

        if not perms.get("can_view_emails", False):
            for kw in SENSITIVE_DATA_KEYWORDS["email"]:
                if kw in input_lower:
                    violations.append(f"email data (matched: '{kw}')")
                    break

        if not perms.get("can_view_dob", False):
            for kw in SENSITIVE_DATA_KEYWORDS["dob"]:
                if kw in input_lower:
                    violations.append(f"date of birth data (matched: '{kw}')")
                    break

        if not perms.get("can_view_financial", False):
            for kw in SENSITIVE_DATA_KEYWORDS["financial"]:
                if kw in input_lower:
                    violations.append(f"financial data (matched: '{kw}')")
                    break

        if not perms.get("can_view_gpa", False):
            for kw in SENSITIVE_DATA_KEYWORDS["gpa"]:
                if kw in input_lower:
                    violations.append(f"GPA data (matched: '{kw}')")
                    break

        if violations:
            return PolicyResult(
                allowed=False,
                reason=f"Access denied for role '{role}': cannot view {', '.join(violations)}. This data is restricted to authorized roles only.",
                policy_name="sensitive_data_access",
                details={"role": role, "violations": violations},
            )

        return PolicyResult(
            allowed=True,
            reason="No restricted sensitive data requested.",
            policy_name="sensitive_data_access",
            details={"role": role},
        )

    def check_table_access(self, user_input: str, role: str) -> PolicyResult:
        perms = ROLE_PERMISSIONS.get(role, {})
        allowed_tables = perms.get("allowed_tables", set())
        input_lower = user_input.lower()

        if ("guardrail_logs" in input_lower or "monitoring" in input_lower or "logs" in input_lower) and not perms.get("can_access_monitoring", False):
            return PolicyResult(
                allowed=False,
                reason=f"Access to monitoring/logging data denied for role '{role}'. Only admins can view system logs.",
                policy_name="table_access",
                details={"role": role, "attempted_table": "guardrail_logs"},
            )

        if ("transaction" in input_lower or "payment" in input_lower or "refund" in input_lower or "enrollment" in input_lower) and "transactions" not in allowed_tables:
            return PolicyResult(
                allowed=False,
                reason=f"Access to transaction data denied for role '{role}'. You can only view student and course information.",
                policy_name="table_access",
                details={"role": role, "attempted_table": "transactions"},
            )

        return PolicyResult(
            allowed=True,
            reason="Table access check passed.",
            policy_name="table_access",
            details={"role": role, "allowed_tables": list(allowed_tables)},
        )

    def check_operation_policy(self, user_input: str) -> PolicyResult:
        input_upper = user_input.upper()
        for op in config.BLOCKED_OPERATIONS:
            if re.search(rf"\b{op}\b", input_upper):
                return PolicyResult(
                    allowed=False,
                    reason=f"Operation '{op}' is blocked by policy. Only read operations are allowed.",
                    policy_name="operation_policy",
                    details={"blocked_operation": op},
                )
        return PolicyResult(
            allowed=True,
            reason="No blocked operations detected.",
            policy_name="operation_policy",
            details={},
        )
