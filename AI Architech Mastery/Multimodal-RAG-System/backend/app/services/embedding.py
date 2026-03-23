"""Embedding service — all embedding calls go through Euri API.

Uses the OpenAI SDK with Euri base_url. Model: gemini-embedding-2-preview.
Output: 768-dimensional vectors.
"""

import logging

from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings
from app.services.euri_client import euri_client

logger = logging.getLogger(__name__)

EMBEDDING_DIMENSIONS = 768


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def embed_text(text: str) -> list[float]:
    """Embed a text string. Returns 768-dim vector."""
    response = euri_client.embeddings.create(
        model=settings.euri_embedding_model,
        input=text,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return response.data[0].embedding


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed multiple text strings in a single call. Returns list of 768-dim vectors."""
    response = euri_client.embeddings.create(
        model=settings.euri_embedding_model,
        input=texts,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return [item.embedding for item in response.data]
