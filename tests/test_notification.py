from tests.test_app import client

def test_publish_message():
    message = "test-message"
    response = client.post("/notification", json = { "message": message })
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == "Message sent"
    assert response_json['message'] == message
