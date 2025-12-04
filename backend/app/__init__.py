from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from redis import Redis
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # <-- ADICIONAR AQUI
from datetime import timedelta


load_dotenv()

# instâncias únicas
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
redis_client = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))


def create_app(config: dict = None):
    app = Flask(__name__)

    # Config padrão
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://postgres:123456@db:5432/testdb"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "supersecretkey"
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    # Sobrescreve com config passada (para testes)
    if config:
        app.config.update(config)

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}},
         supports_credentials=True, expose_headers="Authorization")

    # Blueprints
    from app.auth.routes import auth_bp
    from app.routes.products import products_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")

    return app
