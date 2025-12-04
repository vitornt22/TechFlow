import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    # Passa config de teste para SQLite em memória
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "testsecret"
    })

    with app.app_context():
        db.create_all()
        # Cria usuário de teste
        admin = User(email="admin@test.com")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()

    yield app

    # Limpa banco após o teste
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
