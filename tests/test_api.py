from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_api_respuesta_404_no_existe():
    response = client.post("/orders/O999/confirm")
    assert response.status_code == 404