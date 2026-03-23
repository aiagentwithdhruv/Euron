"""Tests for Pydantic request/response schemas."""

import pytest
from pydantic import ValidationError
from app.models.schemas import TextIngestRequest, QueryRequest


class TestTextIngestRequest:
    def test_valid_text(self):
        req = TextIngestRequest(text="Hello world")
        assert req.text == "Hello world"

    def test_empty_text_rejected(self):
        with pytest.raises(ValidationError):
            TextIngestRequest(text="")

    def test_max_length_enforced(self):
        with pytest.raises(ValidationError):
            TextIngestRequest(text="x" * 500_001)

    def test_at_max_length_accepted(self):
        req = TextIngestRequest(text="x" * 500_000)
        assert len(req.text) == 500_000


class TestQueryRequest:
    def test_valid_query(self):
        req = QueryRequest(question="What is AI?")
        assert req.question == "What is AI?"
        assert req.top_k == 5
        assert req.source_type is None

    def test_empty_question_rejected(self):
        with pytest.raises(ValidationError):
            QueryRequest(question="")

    def test_max_length_enforced(self):
        with pytest.raises(ValidationError):
            QueryRequest(question="x" * 10_001)

    def test_top_k_bounds(self):
        with pytest.raises(ValidationError):
            QueryRequest(question="test", top_k=0)
        with pytest.raises(ValidationError):
            QueryRequest(question="test", top_k=21)

    def test_source_type_optional(self):
        req = QueryRequest(question="test", source_type="pdf")
        assert req.source_type == "pdf"
