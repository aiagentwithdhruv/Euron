"""
Streamlit chat frontend for the University Database Agent.
"""

import streamlit as st
import requests
import json
import time
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="University DB Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #6B7280;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .guardrail-badge-passed {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        background: #D1FAE5;
        color: #065F46;
        margin: 2px 4px;
    }
    .guardrail-badge-blocked {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        background: #FEE2E2;
        color: #991B1B;
        margin: 2px 4px;
    }
    .metric-card {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1F2937;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6B7280;
        text-transform: uppercase;
    }
    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "guardrail_history" not in st.session_state:
    st.session_state.guardrail_history = []
if "total_blocked" not in st.session_state:
    st.session_state.total_blocked = 0
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

with st.sidebar:
    st.markdown("### Settings")
    role = st.selectbox("User Role", ["student", "admin", "viewer"], index=0)

    st.markdown("---")
    st.markdown("### Guardrail Layers")
    layers = [
        ("Policy", "Role access, rate limits, operation policies"),
        ("Input", "SQL injection, prompt injection, PII"),
        ("Instructional", "Topic scope, role deviation"),
        ("Execution", "Tool access, SQL validation"),
        ("Output", "Hallucination, sensitive data, leaks"),
        ("Monitoring", "Full pipeline logging"),
    ]
    for name, desc in layers:
        with st.expander(f"{name} Layer"):
            st.caption(desc)

    st.markdown("---")
    st.markdown("### Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.total_queries)
    with col2:
        st.metric("Blocked", st.session_state.total_blocked)

    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.guardrail_history = []
        st.session_state.total_blocked = 0
        st.session_state.total_queries = 0
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.markdown("### Example Queries")
    examples = [
        "Show me all Computer Science students",
        "What courses are in the Engineering department?",
        "Show me completed payment transactions",
        "What is the average GPA by major?",
        "How many students are enrolled?",
        "List scholarship transactions",
        "Show the schema of the students table",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.pending_example = ex
            st.rerun()

st.markdown('<p class="main-header">University Database Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask questions about students, courses, and transactions — protected by 6 guardrail layers</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "guardrails" in msg:
            with st.expander("Guardrail Details", expanded=False):
                gr = msg["guardrails"]
                for layer_name, checks in gr.items():
                    if not checks:
                        continue
                    st.markdown(f"**{layer_name.title()} Layer:**")
                    for check in checks:
                        passed = check.get("passed", check.get("allowed", True))
                        badge_class = "guardrail-badge-passed" if passed else "guardrail-badge-blocked"
                        status = "PASSED" if passed else "BLOCKED"
                        name = check.get("name", "check")
                        reason = check.get("reason", "")
                        st.markdown(
                            f'<span class="{badge_class}">{status}</span> **{name}**: {reason}',
                            unsafe_allow_html=True,
                        )

                if "tools_called" in msg and msg["tools_called"]:
                    st.markdown("**Tools Called:**")
                    for tool in msg["tools_called"]:
                        allowed = tool.get("allowed", True)
                        badge = "guardrail-badge-passed" if allowed else "guardrail-badge-blocked"
                        st.markdown(
                            f'<span class="{badge}">{"ALLOWED" if allowed else "DENIED"}</span> `{tool["tool"]}` — input: `{tool["input"][:80]}...`',
                            unsafe_allow_html=True,
                        )

                if "execution_time_ms" in msg:
                    st.caption(f"Execution time: {msg['execution_time_ms']:.0f}ms")

pending = st.session_state.pop("pending_example", None)
user_input = st.chat_input("Ask about students, courses, or transactions...")
if pending:
    user_input = pending

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_queries += 1

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing through guardrail pipeline..."):
            try:
                chat_history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                ]

                resp = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": user_input,
                        "session_id": st.session_state.session_id,
                        "chat_history": chat_history[-10:],
                        "role": role,
                    },
                    timeout=60,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    output = data["output"]
                    blocked = data.get("blocked", False)

                    if blocked:
                        st.session_state.total_blocked += 1
                        st.error(output)
                    else:
                        st.markdown(output)

                    with st.expander("Guardrail Details", expanded=blocked):
                        gr = data.get("guardrail_results", {})
                        for layer_name, checks in gr.items():
                            if not checks:
                                continue
                            st.markdown(f"**{layer_name.title()} Layer:**")
                            for check in checks:
                                passed = check.get("passed", check.get("allowed", True))
                                badge_class = "guardrail-badge-passed" if passed else "guardrail-badge-blocked"
                                status = "PASSED" if passed else "BLOCKED"
                                name = check.get("name", "check")
                                reason = check.get("reason", "")
                                st.markdown(
                                    f'<span class="{badge_class}">{status}</span> **{name}**: {reason}',
                                    unsafe_allow_html=True,
                                )

                        if data.get("tools_called"):
                            st.markdown("**Tools Called:**")
                            for tool in data["tools_called"]:
                                allowed = tool.get("allowed", True)
                                badge = "guardrail-badge-passed" if allowed else "guardrail-badge-blocked"
                                st.markdown(
                                    f'<span class="{badge}">{"ALLOWED" if allowed else "DENIED"}</span> `{tool["tool"]}` — input: `{tool.get("input", "")[:80]}...`',
                                    unsafe_allow_html=True,
                                )

                        st.caption(f"Execution time: {data.get('execution_time_ms', 0):.0f}ms")

                    msg_record = {
                        "role": "assistant",
                        "content": output,
                        "guardrails": data.get("guardrail_results", {}),
                        "tools_called": data.get("tools_called", []),
                        "execution_time_ms": data.get("execution_time_ms", 0),
                        "blocked": blocked,
                    }
                    st.session_state.messages.append(msg_record)
                else:
                    error_msg = f"API error (status {resp.status_code}): {resp.text[:200]}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.ConnectionError:
                error_msg = "Cannot connect to the backend API. Make sure the FastAPI server is running on http://localhost:8000"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
