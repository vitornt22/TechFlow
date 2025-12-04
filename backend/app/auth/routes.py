from flask import Blueprint, request, jsonify
from app.models import User, db, bcrypt
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200
