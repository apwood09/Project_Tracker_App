import pytest 
from app  import create_app, db

@pytest.fixture
def clinet(): 
    # isolated, clean in-memory db configuration for each test function
    app = create_app("testing")
    app.config.update({
        "TESTING": True, 
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory". 
        "WTF_CRSF_ENABLED": False # disables from secruity: JSON API testing
    })

    with app.test_client() as client: 
        with app.app_context(): 
            db.create_all()
            yield client 
            db.session.remove()
            db.drop_all()

def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Yarn Over" in resp.data


def test_health(client):
    resp = client.get("/health")
    assert resp.get_json() == {"status": "ok"}


def test_404(client):
    assert client.get("/nope").status_code == 404

# create user
# create account with valid credentials 
def test_create_user(client): 
    payload = {
        "username": "hooked_4.5", 
        "password": "Stitches123456"
    }

    response = client.post("/api/users", json=payload)

    assert = response.status_code == 201
    assert = "id" in response.json
    assert = response.json["username"] == "hooked_4.5"

