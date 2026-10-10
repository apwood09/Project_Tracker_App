def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Yarn Over" in resp.data


def test_health(client):
    resp = client.get("/health")
    assert resp.get_json() == {"status": "ok"}


def test_404(client):
    assert client.get("/nope").status_code == 404


def test_create_and_list_items(client):
    resp = client.post("/api/items", json={"name": "Merino skein"})
    assert resp.status_code == 201

    resp = client.get("/api/items")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Merino skein"


def test_create_item_requires_name(client):
    resp = client.post("/api/items", json={})
    assert resp.status_code == 400
