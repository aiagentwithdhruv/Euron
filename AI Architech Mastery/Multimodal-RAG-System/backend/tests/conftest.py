"""Shared test fixtures and mocks."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_euri_client():
    """Mock the Euri OpenAI client for all tests."""
    with patch("app.services.euri_client.euri_client") as mock:
        # Mock embeddings
        embed_response = MagicMock()
        embed_response.data = [MagicMock(embedding=[0.1] * 768)]
        mock.embeddings.create.return_value = embed_response

        # Mock chat completions (non-streaming)
        chat_response = MagicMock()
        chat_response.choices = [MagicMock()]
        chat_response.choices[0].message.content = "Test answer from LLM"
        mock.chat.completions.create.return_value = chat_response

        # Mock audio transcription
        transcription_response = MagicMock()
        transcription_response.text = "Transcribed audio content"
        mock.audio.transcriptions.create.return_value = transcription_response

        yield mock


@pytest.fixture
def mock_pinecone():
    """Mock Pinecone index for all tests."""
    with patch("app.services.vectorstore.index") as mock_index:
        mock_index.upsert.return_value = None
        mock_index.query.return_value = {
            "matches": [
                {
                    "id": "test-id-1",
                    "score": 0.95,
                    "metadata": {
                        "source_type": "text",
                        "source_file": "test.txt",
                        "chunk_index": 0,
                        "content_preview": "Test content preview",
                    },
                }
            ]
        }
        yield mock_index


@pytest.fixture
def client(mock_euri_client, mock_pinecone):
    """FastAPI test client with all external services mocked."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def sample_pdf_bytes():
    """Minimal valid PDF for testing."""
    from PyPDF2 import PdfWriter
    import io

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    # Add text to the page
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()
