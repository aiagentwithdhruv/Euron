"""Tests for query endpoints."""


class TestQuery:
    def test_query_success(self, client, mock_euri_client, mock_pinecone):
        response = client.post(
            "/query",
            json={"question": "What is artificial intelligence?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert len(data["answer"]) > 0

    def test_query_with_source_filter(self, client, mock_euri_client, mock_pinecone):
        response = client.post(
            "/query",
            json={"question": "test", "source_type": "pdf", "top_k": 3},
        )
        assert response.status_code == 200

    def test_query_empty_question_rejected(self, client):
        response = client.post("/query", json={"question": ""})
        assert response.status_code == 422

    def test_query_stream_returns_sse(self, client, mock_euri_client, mock_pinecone):
        # Mock streaming response
        from unittest.mock import MagicMock

        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "Hello"

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta.content = " world"

        mock_euri_client.chat.completions.create.return_value = [chunk1, chunk2]

        response = client.post(
            "/query/stream",
            json={"question": "test question"},
        )
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")


class TestQueryErrorHandling:
    def test_query_error_is_generic(self, client, mock_euri_client):
        from unittest.mock import patch

        with patch(
            "app.services.rag_pipeline.embed_text",
            side_effect=Exception("Connection timeout to api.euron.one"),
        ):
            response = client.post(
                "/query",
                json={"question": "test"},
            )
            assert response.status_code == 500
            detail = response.json()["detail"]
            assert "api.euron.one" not in detail
            assert "try again" in detail.lower()
