from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    healthcheck = response.json()
    assert healthcheck['status'] == "Healthy"

def test_publish_message():
    message = "test-message"
    response = client.post("/notification", json = { "message": message })
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == "Message sent"
    assert response_json['message'] == message
