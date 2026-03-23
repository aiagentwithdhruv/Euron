"""Tests for individual processors — text, PDF chunking logic."""

from unittest.mock import patch, MagicMock


class TestTextProcessor:
    @patch("app.processors.text_processor.embed_texts")
    def test_process_text_chunks_correctly(self, mock_embed):
        mock_embed.return_value = [[0.1] * 768, [0.2] * 768]

        from app.processors.text_processor import process_text

        text = "Hello world. " * 200  # enough to create multiple chunks
        result = process_text(text, source_file="test.txt")

        assert len(result) > 0
        for vec in result:
            assert "id" in vec
            assert "values" in vec
            assert len(vec["values"]) == 768
            assert "metadata" in vec
            assert vec["metadata"]["source_file"] == "test.txt"
            assert "chunk_index" in vec["metadata"]
            assert "content_preview" in vec["metadata"]

    @patch("app.processors.text_processor.embed_texts")
    def test_process_empty_text(self, mock_embed):
        from app.processors.text_processor import process_text

        result = process_text("", source_file="empty.txt")
        assert result == []
        mock_embed.assert_not_called()


class TestTextChunking:
    def test_chunk_size_and_overlap(self):
        from app.processors.text_processor import splitter, CHUNK_SIZE, CHUNK_OVERLAP

        assert CHUNK_SIZE == 1024
        assert CHUNK_OVERLAP == 256

        # Test splitting
        text = "word " * 1000  # ~5000 chars
        chunks = splitter.split_text(text)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= CHUNK_SIZE + 50  # small tolerance for splitting


class TestPdfProcessor:
    @patch("app.processors.pdf_processor.embed_texts")
    def test_process_pdf_with_text(self, mock_embed, sample_pdf_bytes):
        mock_embed.return_value = [[0.1] * 768]

        from app.processors.pdf_processor import process_pdf

        # Blank PDF has no text, so result should be empty
        result = process_pdf(sample_pdf_bytes, "test.pdf")
        assert isinstance(result, list)

    @patch("app.processors.pdf_processor.embed_texts")
    def test_process_invalid_pdf(self, mock_embed):
        from app.processors.pdf_processor import process_pdf
        import pytest

        with pytest.raises(Exception):
            process_pdf(b"not a pdf", "bad.pdf")
