"""Tests for health check and app-level endpoints."""


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "running" in data["message"].lower()


def test_ingested_list(client):
    response = client.get("/ingested")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data


def test_cors_headers(client):
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Should not return wildcard
    allow_origin = response.headers.get("access-control-allow-origin", "")
    assert allow_origin != "*" or allow_origin == ""
