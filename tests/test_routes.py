def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Yarn Over" in resp.data


def test_health(client):
    resp = client.get("/health")
    assert resp.get_json() == {"status": "ok"}


def test_404(client):
    assert client.get("/nope").status_code == 404

