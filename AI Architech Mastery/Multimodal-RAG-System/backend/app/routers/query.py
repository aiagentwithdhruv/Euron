"""Query endpoints — JSON response and SSE streaming."""

import asyncio
import logging
from collections.abc import AsyncGenerator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.config import settings
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_pipeline import query, query_stream
from app.rate_limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
@limiter.limit(settings.rate_limit_queries)
async def query_endpoint(request: Request, body: QueryRequest) -> QueryResponse:
    """Ask a question — returns JSON with answer and sources."""
    try:
        loop = asyncio.get_running_loop()
        answer, sources = await loop.run_in_executor(
            None,
            lambda: query(
                question=body.question,
                source_type=body.source_type,
                top_k=body.top_k,
            ),
        )
        return QueryResponse(answer=answer, sources=sources)
    except Exception:
        logger.exception("Query failed")
        raise HTTPException(status_code=500, detail="Query failed. Please try again.")


async def _async_stream(question: str, source_type: str | None, top_k: int) -> AsyncGenerator[str, None]:
    """Wrap the sync generator in an async generator using a queue."""
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _producer() -> None:
        try:
            gen = query_stream(question=question, source_type=source_type, top_k=top_k)
            for chunk in gen:
                loop.call_soon_threadsafe(queue.put_nowait, chunk)
        except Exception:
            logger.exception("Error during streaming generation")
            loop.call_soon_threadsafe(
                queue.put_nowait,
                f'data: {{"content": "\\n\\n[Error generating response]"}}\n\n',
            )
            loop.call_soon_threadsafe(
                queue.put_nowait, "data: [DONE]\n\n"
            )
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel

    loop.run_in_executor(None, _producer)

    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        yield chunk


@router.post("/query/stream")
@limiter.limit(settings.rate_limit_queries)
async def query_stream_endpoint(request: Request, body: QueryRequest):
    """Ask a question — returns SSE stream with tokens and sources."""
    try:
        return StreamingResponse(
            _async_stream(
                question=body.question,
                source_type=body.source_type,
                top_k=body.top_k,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception:
        logger.exception("Stream query failed")
        raise HTTPException(status_code=500, detail="Stream query failed. Please try again.")
