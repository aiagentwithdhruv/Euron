"""
FastAPI backend serving the guarded LangChain agent.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from agents.agent import GuardedAgent

app = FastAPI(
    title="University DB Agent API",
    description="Agentic chat interface with 6-layer guardrails for university database queries.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = GuardedAgent()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: str | None = Field(None, description="Session ID for conversation continuity")
    chat_history: list[dict] | None = Field(None, description="Previous messages for context")
    role: str = Field("student", description="User role: student, admin, viewer")


class ChatResponse(BaseModel):
    session_id: str
    output: str
    blocked: bool
    block_reason: str | None = None
    guardrail_results: dict
    tools_called: list
    execution_time_ms: float


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        langchain_history = []
        if request.chat_history:
            from langchain_core.messages import HumanMessage, AIMessage
            for msg in request.chat_history:
                if msg.get("role") == "user":
                    langchain_history.append(HumanMessage(content=msg["content"]))
                elif msg.get("role") == "assistant":
                    langchain_history.append(AIMessage(content=msg["content"]))

        result = agent.process(
            user_input=request.message,
            session_id=request.session_id,
            chat_history=langchain_history,
            role=request.role,
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "university-db-agent"}


@app.get("/guardrails/info")
async def guardrails_info():
    return {
        "layers": [
            {
                "name": "Policy Layer",
                "description": "Role-based access, rate limiting, operation policies, data scope enforcement",
            },
            {
                "name": "Input Layer",
                "description": "SQL injection detection, prompt injection detection, PII redaction, input length/empty validation",
            },
            {
                "name": "Instructional Layer",
                "description": "Topic relevance enforcement, role deviation detection, instruction extraction prevention",
            },
            {
                "name": "Execution Layer",
                "description": "Tool access control, SQL validation (type, keywords, tables, row limits, multi-statement)",
            },
            {
                "name": "Output Layer",
                "description": "Sensitive data filtering, hallucination detection, response length control, instruction leak prevention",
            },
            {
                "name": "Monitoring Layer",
                "description": "Full pipeline logging to guardrail_logs table: inputs, outputs, tools, blocks, hallucinations, timing",
            },
        ]
    }


if __name__ == "__main__":
    import uvicorn
    import config
    uvicorn.run(app, host="0.0.0.0", port=config.FASTAPI_PORT)
