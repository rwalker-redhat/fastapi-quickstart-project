from fastapi.testclient import TestClient

from main import main_app

client = TestClient(main_app)


def test_read_main():
    response = client.get("/api/motd")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello FastAPI!"}
