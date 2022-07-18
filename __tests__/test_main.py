from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_search_1337x():
    response = client.get(
        "/search/1337x?q=avengers")
    assert response.status_code == 200
    # assert response.json() == {"torrents": [], "totalPages": 0}
