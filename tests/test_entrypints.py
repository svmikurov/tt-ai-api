"""API entrypoints tests."""

from fastapi.testclient import TestClient

from sd.api.main import app

client = TestClient(app)


def test_sse_stream() -> None:
    """Test that SSE endpoint returns success status code."""
    with client.stream(
        'POST',
        '/predict',
        json={'query': 'Hi'},
    ) as response:
        assert response.status_code == 200
