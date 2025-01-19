from tests.test_app import client
from app.rabbitmq.publisher import Publisher

def test_publish_message(mocker):
    mock_publish = mocker.patch.object(Publisher, "publish", return_value=None)
    message = "test-message"
    response = client.post("/notification", json = { "message": message })
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == "Message sent"
    assert response_json['message'] == message
    mock_publish.assert_called_once_with(message, 'example-queue-out')