"""
Monitoring Layer Guardrail
Logs every interaction through the guardrail pipeline to the guardrail_logs
table in Supabase for audit, analysis, and debugging.
"""

import json
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from database.connection import get_client


@dataclass
class MonitoringRecord:
    session_id: str
    user_input: str
    sanitized_input: str | None
    guardrail_layer: str
    guardrail_name: str
    action: str  # "passed", "blocked", "flagged", "filtered"
    details: dict = field(default_factory=dict)
    tool_called: str | None = None
    tool_allowed: bool | None = None
    llm_raw_output: str | None = None
    llm_final_output: str | None = None
    hallucination_flag: bool = False
    blocked: bool = False
    execution_time_ms: float | None = None


class MonitoringGuardrail:

    def __init__(self):
        self._buffer: list[dict] = []

    def log(self, record: MonitoringRecord):
        entry = {
            "session_id": record.session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_input": record.user_input,
            "sanitized_input": record.sanitized_input,
            "guardrail_layer": record.guardrail_layer,
            "guardrail_name": record.guardrail_name,
            "action": record.action,
            "details": json.dumps(record.details) if record.details else None,
            "tool_called": record.tool_called,
            "tool_allowed": record.tool_allowed,
            "llm_raw_output": record.llm_raw_output,
            "llm_final_output": record.llm_final_output,
            "hallucination_flag": record.hallucination_flag,
            "blocked": record.blocked,
            "execution_time_ms": record.execution_time_ms,
        }
        self._buffer.append(entry)

    def flush(self):
        if not self._buffer:
            return
        try:
            client = get_client()
            for entry in self._buffer:
                client.table("guardrail_logs").insert(entry).execute()
            self._buffer.clear()
        except Exception as e:
            print(f"[MonitoringGuardrail] Failed to flush logs: {e}")

    def log_policy_check(self, session_id: str, user_input: str, results: list, blocked: bool):
        for r in results:
            self.log(MonitoringRecord(
                session_id=session_id,
                user_input=user_input,
                sanitized_input=None,
                guardrail_layer="policy",
                guardrail_name=r.policy_name,
                action="blocked" if not r.allowed else "passed",
                details=r.details,
                blocked=not r.allowed,
            ))

    def log_input_check(self, session_id: str, user_input: str, sanitized: str, results: list, blocked: bool):
        for r in results:
            self.log(MonitoringRecord(
                session_id=session_id,
                user_input=user_input,
                sanitized_input=sanitized,
                guardrail_layer="input",
                guardrail_name=r.check_name,
                action="blocked" if not r.passed else "passed",
                details=r.details,
                blocked=not r.passed,
            ))

    def log_instruction_check(self, session_id: str, user_input: str, results: list, blocked: bool):
        for r in results:
            self.log(MonitoringRecord(
                session_id=session_id,
                user_input=user_input,
                sanitized_input=None,
                guardrail_layer="instructional",
                guardrail_name=r.check_name,
                action="blocked" if not r.passed else "passed",
                details=r.details,
                blocked=not r.passed,
            ))

    def log_execution_check(self, session_id: str, user_input: str, tool_name: str,
                            tool_allowed: bool, sql: str | None, sql_results: list | None):
        self.log(MonitoringRecord(
            session_id=session_id,
            user_input=user_input,
            sanitized_input=None,
            guardrail_layer="execution",
            guardrail_name="tool_and_sql_validation",
            action="blocked" if not tool_allowed else "passed",
            details={"sql": sql, "sql_checks": [r.reason for r in (sql_results or [])]},
            tool_called=tool_name,
            tool_allowed=tool_allowed,
            blocked=not tool_allowed,
        ))

    def log_output_check(self, session_id: str, user_input: str, raw_output: str,
                         final_output: str, results: list, hallucination: bool):
        for r in results:
            self.log(MonitoringRecord(
                session_id=session_id,
                user_input=user_input,
                sanitized_input=None,
                guardrail_layer="output",
                guardrail_name=r.check_name,
                action="blocked" if not r.passed else "passed",
                llm_raw_output=raw_output[:2000],
                llm_final_output=final_output[:2000],
                hallucination_flag=hallucination,
                blocked=not r.passed,
            ))

    def log_full_pipeline(self, session_id: str, user_input: str, total_time_ms: float,
                          blocked: bool, block_reason: str | None = None):
        self.log(MonitoringRecord(
            session_id=session_id,
            user_input=user_input,
            sanitized_input=None,
            guardrail_layer="monitoring",
            guardrail_name="pipeline_summary",
            action="blocked" if blocked else "completed",
            details={"block_reason": block_reason},
            blocked=blocked,
            execution_time_ms=total_time_ms,
        ))
        self.flush()
