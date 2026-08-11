from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.blog import blog_bp
from blueprints.loja import loja_bp
from blueprints.main import main_bp

from .conftest import login


def test_blueprints_registrados(app):
    for bp in (main_bp, auth_bp, blog_bp, loja_bp, admin_bp):
        assert bp.name in app.blueprints


def test_rotas_publicas(client):
    for caminho in ["/", "/contato", "/blog", "/loja"]:
        response = client.get(caminho)
        assert response.status_code == 200, f"{caminho} -> {response.status_code}"


def test_login_administrativo_redirect(client):
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_novo_post_requer_login(client):
    response = client.get("/blog/novo")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_com_admin(client):
    response = login(client, "admin", "admin123")
    assert response.status_code == 200
    assert "Dashboard" in response.get_data(as_text=True)


def test_admin_dashboard_disponivel_para_admin(client):
    login(client, "admin", "admin123")
    response = client.get("/admin/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    for texto in ["Dashboard", "Projetos", "Experiências", "Educação", "Blog", "Mensagens de contato"]:
        assert texto in html


def test_admin_bloqueado_para_usuario_comum(client):
    login(client, "alice", "alice123")
    response = client.get("/admin/")
    assert response.status_code == 302


def test_formularios_contem_csrf(client):
    for caminho in ["/login", "/registro", "/contato"]:
        response = client.get(caminho)
        assert response.status_code == 200
        assert b"csrf_token" in response.data, f"{caminho} sem csrf_token"


def test_formulario_blog_novo_contem_csrf(client):
    login(client, "admin", "admin123")
    response = client.get("/blog/novo")
    assert response.status_code == 200
    assert b"csrf_token" in response.data


def test_rotas_blog(client):
    login(client, "admin", "admin123")
    assert client.get("/blog/novo").status_code == 200
    assert client.get("/blog/1").status_code in (200, 302)


def test_rotas_admin_crud(client):
    login(client, "admin", "admin123")
    for caminho in [
        "/admin/projetos/novo",
        "/admin/experiencias/novo",
        "/admin/educacao/novo",
        "/admin/posts/novo",
        "/admin/produtos/novo",
    ]:
        assert client.get(caminho).status_code == 200, caminho


def test_logout(client):
    login(client, "alice", "alice123")
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
