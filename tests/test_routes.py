import pytest 
from app  import create_app, db
from app.routes import User

@pytest.fixture
def client(): 
    # isolated, clean in-memory db configuration for each test function
    app = create_app("testing")
    app.config.update({
        "TESTING": True, 
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory", 
        "WTF_CSRF_ENABLED": False # disables from secruity: JSON API testing
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

    assert  response.status_code == 201
    assert  "id" in response.json
    assert  response.json["username"] == "hooked_4.5"

# login user 
# valid credential entries generate tracking responses correctly
def test_login_user(client): 
    # seed user -> mock db 
    user = User(username="hooked_4.5")
    user.set_password("Stitches123456")
    db.session.add(user)
    db.session.commit()

    # attempt login 
    payload = {
        "username": "hooked_4.5", 
        "password": "Stitches123456"
    }

    response = client.post("/api/login", json=payload)

    assert response.status_code == 200
    assert "Welcome back, hooked_4.5!" in response.json["message"]
    assert "user" in response.json

# logout user
# full integration sequence logic paths for logout actions 
def test_logout_user(client): 
    # seed user -> mock db
    user = User(username="hooked_4.5")
    user.set_password("Stitches123456")
    db.session.add(user)
    db.session.commit()

    # log in, establish session cookie in test client 
    client.post("/login", json={"username": "hooked_4.5", "password": "Stitches123456"})

    # hit logout endpoint 
    response = client.post("/logout")

    assert response.status_code == 200
    assert " sucessfully unstitched from session" in response.json["message"]

# delete user 
# confirm destroy user entries successfully 
def test_delete_user(client): 
    # seed user -> mock db 
    user = User(username="hooked_4.5")
    user.set_password("Stitches123456")
    db.session.add(user)
    db.session.commit()

    # call dynamic delete route 
    response = client.delete("/users/hooked_4.5")

    assert response.status_code == 200
    assert "succesfully unstitched" in response.json["message"]

    # double check db empty 
    delete_user = User.query.filter_by(username="hooked_4.5").first()
    assert delete_user is None