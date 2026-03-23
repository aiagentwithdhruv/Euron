"""Tests for ingestion endpoints — file size limits, validation, error handling."""

import io
import pytest


class TestTextIngestion:
    def test_ingest_text_success(self, client, mock_euri_client, mock_pinecone):
        response = client.post(
            "/ingest/text",
            json={"text": "This is a test document about artificial intelligence."},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["source_type"] == "text"
        assert data["chunks_ingested"] > 0

    def test_ingest_empty_text_rejected(self, client):
        response = client.post("/ingest/text", json={"text": ""})
        assert response.status_code == 422  # Pydantic validation error


class TestPdfIngestion:
    def test_ingest_pdf_wrong_extension(self, client):
        response = client.post(
            "/ingest/pdf",
            files={"file": ("test.txt", b"not a pdf", "text/plain")},
        )
        assert response.status_code == 400
        assert "pdf" in response.json()["detail"].lower()

    def test_ingest_pdf_oversized(self, client):
        # Create a file that exceeds 50MB limit
        oversized = b"x" * (51 * 1024 * 1024)
        response = client.post(
            "/ingest/pdf",
            files={"file": ("big.pdf", oversized, "application/pdf")},
        )
        assert response.status_code == 413


class TestImageIngestion:
    def test_ingest_image_wrong_extension(self, client):
        response = client.post(
            "/ingest/image",
            files={"file": ("test.bmp", b"data", "image/bmp")},
        )
        assert response.status_code == 400

    def test_ingest_image_oversized(self, client):
        oversized = b"x" * (21 * 1024 * 1024)
        response = client.post(
            "/ingest/image",
            files={"file": ("big.png", oversized, "image/png")},
        )
        assert response.status_code == 413


class TestAudioIngestion:
    def test_ingest_audio_wrong_extension(self, client):
        response = client.post(
            "/ingest/audio",
            files={"file": ("test.ogg", b"data", "audio/ogg")},
        )
        assert response.status_code == 400


class TestVideoIngestion:
    def test_ingest_video_wrong_extension(self, client):
        response = client.post(
            "/ingest/video",
            files={"file": ("test.avi", b"data", "video/x-msvideo")},
        )
        assert response.status_code == 400

    def test_ingest_video_oversized(self, client):
        oversized = b"x" * (201 * 1024 * 1024)
        response = client.post(
            "/ingest/video",
            files={"file": ("big.mp4", oversized, "video/mp4")},
        )
        assert response.status_code == 413


class TestErrorHandling:
    def test_internal_errors_are_generic(self, client, mock_euri_client):
        """Verify that internal exceptions don't leak details to the client."""
        from unittest.mock import patch

        with patch(
            "app.processors.text_processor.embed_texts",
            side_effect=Exception("API key invalid: euri-abc123"),
        ):
            response = client.post(
                "/ingest/text",
                json={"text": "Test text that will fail embedding"},
            )
            assert response.status_code == 500
            detail = response.json()["detail"]
            # Must NOT contain the actual error message with API key
            assert "euri-abc123" not in detail
            assert "try again" in detail.lower()
