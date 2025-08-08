import pytest
from app import app, db, init_db
import jwt
import datetime
from flask import current_app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def generate_expired_token(username, is_refresh=False):
    exp = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)  # 10 detik lalu = expired
    payload = {
        "sub": username,
        "exp": exp,
        "refresh": is_refresh
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def test_login_and_refresh(client):
    resp = client.post("/login", json={"username": "user1", "password": "password123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    assert "refresh_token" in data

    resp2 = client.post("/refresh", json={"refresh_token": data["refresh_token"]})
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert "access_token" in data2
    assert "refresh_token" in data2

def test_login_fail_invalid_user(client):
    resp = client.post("/login", json={"username": "no_such_user", "password": "wrongpass"})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Invalid credentials"


def test_login_fail_wrong_password(client):
    resp = client.post("/login", json={"username": "user1", "password": "wrongpass"})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Invalid credentials"


def test_refresh_fail_invalid_token(client):
    resp = client.post("/refresh", json={"refresh_token": "not_a_jwt"})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Invalid or expired refresh token"


def test_refresh_fail_access_token_given(client):
    resp = client.post("/login", json={"username": "user1", "password": "password123"})
    access_token = resp.get_json()["access_token"]
    resp2 = client.post("/refresh", json={"refresh_token": access_token})
    assert resp2.status_code == 401
    assert resp2.get_json()["error"] == "Invalid or expired refresh token"

def test_refresh_with_expired_token(client):
    with client.application.app_context():
        expired_refresh = generate_expired_token("user1", is_refresh=True)

    resp = client.post("/refresh", json={"refresh_token": expired_refresh})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Invalid or expired refresh token"


