import re
from datetime import datetime
from pathlib import Path

import pytest
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import generate_csrf
from sqlalchemy.pool import StaticPool

from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.blog import blog_bp
from blueprints.main import main_bp, perfil
from models import User, db

PROJETO_ROOT = Path(__file__).resolve().parent.parent

CSRF_RE = re.compile(
    r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"[^>]*>'
    r"|<input[^>]*value=\"([^\"]+)\"[^>]*name=\"csrf_token\"[^>]*>"
)


def _criar_usuario(username, password, email, is_admin=False):
    user = User(username=username, email=email, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def _montar_app():
    test_app = Flask(
        __name__,
        template_folder=str(PROJETO_ROOT / "templates"),
        static_folder=str(PROJETO_ROOT / "static"),
    )
    test_app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_ENGINE_OPTIONS={
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        },
        WTF_CSRF_ENABLED=True,
    )

    db.init_app(test_app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(test_app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @test_app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year, "perfil": perfil, "csrf_token": generate_csrf}

    test_app.register_blueprint(main_bp)
    test_app.register_blueprint(auth_bp)
    test_app.register_blueprint(blog_bp)
    test_app.register_blueprint(admin_bp)

    return test_app


@pytest.fixture()
def app():
    flask_app = _montar_app()
    with flask_app.app_context():
        db.create_all()
        _criar_usuario("admin", "admin123", "admin@example.com", is_admin=True)
        _criar_usuario("alice", "alice123", "alice@example.com")
        _criar_usuario("bob", "bob123", "bob@example.com")
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username, password):
    response = client.get("/login")
    token = _csrf(client, response.data)
    return client.post(
        "/login",
        data={
            "username": username,
            "password": password,
            "csrf_token": token,
        },
        follow_redirects=True,
    )


def _csrf(client, html):
    match = CSRF_RE.search(html.decode())
    assert match, "csrf_token não encontrado no HTML"
    return match.group(1) or match.group(2)


def csrf_para(client, path):
    response = client.get(path)
    assert response.status_code == 200, f"GET {path} retornou {response.status_code}"
    return _csrf(client, response.data)
