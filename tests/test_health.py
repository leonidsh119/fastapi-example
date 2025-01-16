from tests.test_app import client

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    healthcheck = response.json()
    assert healthcheck['status'] == "Healthy"