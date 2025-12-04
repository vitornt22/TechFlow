import json
# tests/test_auth.py


def test_login_success(client):
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "admin@test.com", "password": "123456"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_login_wrong_password(client):
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "admin@test.com", "password": "wrong"}),
        content_type="application/json"
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Credenciais inválidas"
