# tests/test_products.py
import json
import pytest
from app.models import Product
from datetime import timedelta
from flask_jwt_extended import create_access_token


@pytest.fixture
def access_token(client):
    res = client.post(
        "/auth/login",
        data=json.dumps({"email": "admin@test.com", "password": "123456"}),
        content_type="application/json"
    )
    return res.get_json()["access_token"]


@pytest.fixture
def expired_token(app):
    # Cria um token expirado manualmente
    with app.app_context():
        token = create_access_token(
            identity=1, expires_delta=timedelta(seconds=-1))
        return token


def test_create_product(client, access_token):
    payload = {"nome": "Produto Teste", "marca": "MarcaX", "valor": 99.9}
    res = client.post(
        "/products/",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json"
    )
    assert res.status_code == 202
    data = res.get_json()
    assert data["msg"] == "Produto enfileirado para criação"


def test_update_product(client, access_token):
    # Primeiro cria um produto diretamente no banco
    product_data = {"nome": "Produto Atualizar",
                    "marca": "MarcaY", "valor": 50.0}
    res_create = client.post(
        "/products/",
        data=json.dumps(product_data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json"
    )
    assert res_create.status_code == 202

    # Simula atualização
    update_data = {"nome": "Produto Atualizado",
                   "marca": "MarcaY", "valor": 75.0}
    res_update = client.put(
        "/products/1",
        data=json.dumps(update_data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json"
    )
    assert res_update.status_code == 202
    assert res_update.get_json(
    )["msg"] == "Produto enfileirado para atualização"


def test_delete_product(client, access_token):
    # Primeiro cria um produto
    product_data = {"nome": "Produto Deletar",
                    "marca": "MarcaZ", "valor": 30.0}
    res_create = client.post(
        "/products/",
        data=json.dumps(product_data),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json"
    )
    assert res_create.status_code == 202

    # Simula exclusão
    res_delete = client.delete(
        "/products/1",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res_delete.status_code == 202
    assert res_delete.get_json()["msg"] == "Produto enfileirado para remoção"
