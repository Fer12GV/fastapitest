import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    """ Test to create a new user """
    response = client.post("/init_user", json={"username": "testuser", "role": "tester"})
    assert response.status_code == 200
    assert "testuser" in response.json()["message"]


def test_ask_chatbot(mocker):
    """Test for /ask endpoint with mocked OpenAI response."""
    client.post("/init_user", json={"username": "mockuser", "role": "mock role"})

    # 👇 Patch correctly where FastAPI is using it
    mocker.patch("app.api.chatbot_routes.ask_openai", return_value="Mocked response")

    response = client.post("/ask", json={"username": "mockuser", "message": "Hello?"})
    assert response.status_code == 200
    assert response.json()["response"] == "Mocked response"
