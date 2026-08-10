from models import Post, User, db

from .conftest import csrf_para, login


def _criar_post(titulo, conteudo, author):
    post = Post(titulo=titulo, conteudo=conteudo, author=author)
    db.session.add(post)
    db.session.commit()
    return post


def test_usuario_cria_post(client, app):
    login(client, "alice", "alice123")
    token = csrf_para(client, "/blog/novo")
    response = client.post(
        "/blog/novo",
        data={
            "titulo": "Post da Alice",
            "conteudo": "Conteúdo da Alice",
            "csrf_token": token,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        post = Post.query.filter_by(titulo="Post da Alice").first()
        assert post is not None
        assert post.author.username == "alice"
        assert post.author_id == post.author.id


def test_usuario_edita_proprio_post(client, app):
    login(client, "alice", "alice123")
    with app.app_context():
        alice = User.query.filter_by(username="alice").first()
        post = _criar_post("Post editável", "Conteúdo original", alice)
        post_id = post.id
    token = csrf_para(client, f"/blog/{post_id}/editar")
    response = client.post(
        f"/blog/{post_id}/editar",
        data={
            "titulo": "Post editado",
            "conteudo": "Conteúdo editado",
            "csrf_token": token,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        post = db.session.get(Post, post_id)
        assert post.titulo == "Post editado"
        assert post.conteudo == "Conteúdo editado"


def test_usuario_nao_edita_post_alheio(client, app):
    login(client, "alice", "alice123")
    with app.app_context():
        bob = User.query.filter_by(username="bob").first()
        post = _criar_post("Post do Bob", "Conteúdo do Bob", bob)
        post_id = post.id
    response = client.get(f"/blog/{post_id}/editar")
    assert response.status_code == 302
    token = csrf_para(client, "/blog/novo")
    response = client.post(
        f"/blog/{post_id}/editar",
        data={
            "titulo": "Post do Bob alterado",
            "conteudo": "alterado",
            "csrf_token": token,
        },
    )
    assert response.status_code == 302
    with app.app_context():
        post = db.session.get(Post, post_id)
        assert post.titulo == "Post do Bob"


def test_admin_cria_post(client, app):
    login(client, "admin", "admin123")
    token = csrf_para(client, "/admin/posts/novo")
    response = client.post(
        "/admin/posts/novo",
        data={
            "titulo": "Post do Admin",
            "conteudo": "Conteúdo do Admin",
            "csrf_token": token,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        post = Post.query.filter_by(titulo="Post do Admin").first()
        assert post is not None
        assert post.author.username == "admin"


def test_admin_edita_post_alheio(client, app):
    login(client, "admin", "admin123")
    with app.app_context():
        alice = User.query.filter_by(username="alice").first()
        post = _criar_post("Post da Alice p/ admin", "Conteúdo", alice)
        post_id = post.id
    token = csrf_para(client, f"/admin/posts/{post_id}/editar")
    response = client.post(
        f"/admin/posts/{post_id}/editar",
        data={
            "titulo": "Editado pelo admin",
            "conteudo": "Conteúdo editado",
            "csrf_token": token,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Post, post_id).titulo == "Editado pelo admin"


def test_delete_post_apenas_post(client, app):
    login(client, "alice", "alice123")
    with app.app_context():
        alice = User.query.filter_by(username="alice").first()
        post = _criar_post("Post so post", "Conteúdo", alice)
        post_id = post.id
    response = client.get(f"/blog/{post_id}/excluir")
    assert response.status_code == 405
    with app.app_context():
        assert db.session.get(Post, post_id) is not None


def test_usuario_exclui_proprio_post(client, app):
    login(client, "alice", "alice123")
    with app.app_context():
        alice = User.query.filter_by(username="alice").first()
        post = _criar_post("Post a excluir", "Conteúdo", alice)
        post_id = post.id
    token = csrf_para(client, f"/blog/{post_id}")
    response = client.post(
        f"/blog/{post_id}/excluir",
        data={"csrf_token": token},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Post, post_id) is None


def test_post_inexistente_redireciona(client):
    response = client.get("/blog/99999", follow_redirects=True)
    assert response.status_code == 200


def test_post_detalhe_exibe_titulo(client, app):
    with app.app_context():
        alice = User.query.filter_by(username="alice").first()
        post = _criar_post("Post visível", "Conteúdo visível", alice)
        post_id = post.id
    response = client.get(f"/blog/{post_id}")
    assert response.status_code == 200
    assert "Post visível" in response.get_data(as_text=True)
