from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import redis_client
import json

products_bp = Blueprint("products_bp", __name__)


@products_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    from app.models import Product
    from app import db
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "nome": p.nome,
        "marca": p.marca,
        "valor": str(p.valor)
    } for p in products])


@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()

    # Validação
    nome = data.get("nome", "").strip()
    marca = data.get("marca", "").strip()
    valor = data.get("valor")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400
    if not marca:
        return jsonify({"error": "Marca é obrigatória"}), 400
    if valor is None or str(valor).strip() == "":
        return jsonify({"error": "Valor é obrigatório"}), 400

    # Enfileira
    message = {"operation": "create", "data": data}
    redis_client.rpush("products_queue", json.dumps(message))
    return jsonify({"msg": "Produto enfileirado para criação"}), 202


@products_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    data = request.get_json()

    # Validação
    nome = data.get("nome", "").strip()
    marca = data.get("marca", "").strip()
    valor = data.get("valor")

    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400
    if not marca:
        return jsonify({"error": "Marca é obrigatória"}), 400
    if valor is None or str(valor).strip() == "":
        return jsonify({"error": "Valor é obrigatório"}), 400

    message = {"operation": "update", "id": id, "data": data}
    redis_client.rpush("products_queue", json.dumps(message))
    return jsonify({"msg": "Produto enfileirado para atualização"}), 202


@products_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    message = {"operation": "delete", "id": id}
    redis_client.rpush("products_queue", json.dumps(message))
    return jsonify({"msg": "Produto enfileirado para remoção"}), 202
