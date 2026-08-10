from datetime import datetime
from functools import wraps

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from forms import (
    ContatoForm,
    EducacaoForm,
    ExperienciaForm,
    LoginForm,
    PostForm,
    ProjetoForm,
    RegistroForm,
)
from models import Educacao, Experiencia, Mensagem, Post, Projeto, User, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return wrapper


perfil = {
    "nome": "Seu Nome",
    "titulo": "Desenvolvedor Python",
    "tagline": "Construo aplicações web modernas e eficientes com Python e Flask.",
    "bio": "Olá! Sou um desenvolvedor apaixonado por tecnologia, focado em criar "
           "soluções limpas, escaláveis e com boa experiência para o usuário. "
           "Tenho experiência com backend, APIs e ferramentas de automação.",
    "localizacao": "Brasil",
    "email": "seuemail@exemplo.com",
}

habilidades = [
    "Python",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Git",
    "Docker",
]

contato = {
    "email": "seuemail@exemplo.com",
    "github": "https://github.com/seu-usuario",
    "linkedin": "https://linkedin.com/in/seu-usuario",
}


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year, "perfil": perfil}


@app.route("/")
def index():
    projetos = Projeto.query.order_by(Projeto.id).all()
    experiencias = Experiencia.query.order_by(Experiencia.id).all()
    educacao = Educacao.query.order_by(Educacao.id).all()
    return render_template(
        "index.html",
        habilidades=habilidades,
        projetos=projetos,
        experiencias=experiencias,
        educacao=educacao,
        contato=contato,
    )


@app.route("/blog")
def blog():
    posts = Post.query.order_by(Post.criado_em.desc()).all()
    return render_template("blog.html", posts=posts)


@app.route("/blog/<int:post_id>")
def post_detalhe(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash("Postagem não encontrada.", "danger")
        return redirect(url_for("blog"))
    return render_template("post.html", post=post)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        mensagem = Mensagem(
            nome=form.nome.data,
            email=form.email.data,
            mensagem=form.mensagem.data,
        )
        db.session.add(mensagem)
        db.session.commit()
        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for("contato"))
    return render_template("contato.html", form=form, contato=contato)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistroForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Nome de usuário já está em uso.", "danger")
            return render_template("auth/registro.html", form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash("Email já cadastrado.", "danger")
            return render_template("auth/registro.html", form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("index"))
    return render_template("auth/registro.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login realizado com sucesso.", "success")
            destino = "admin_dashboard" if user.is_admin else "index"
            return redirect(url_for(destino))
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("auth/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    projetos = Projeto.query.order_by(Projeto.id).all()
    experiencias = Experiencia.query.order_by(Experiencia.id).all()
    educacao = Educacao.query.order_by(Educacao.id).all()
    posts = Post.query.order_by(Post.criado_em.desc()).all()
    mensagens = Mensagem.query.order_by(Mensagem.criada_em.desc()).all()
    return render_template(
        "admin/dashboard.html",
        projetos=projetos,
        experiencias=experiencias,
        educacao=educacao,
        posts=posts,
        mensagens=mensagens,
    )


CAMPOS_ITEM = [
    "titulo",
    "descricao",
    "conteudo",
    "tecnologias",
    "link",
    "github",
    "cargo",
    "empresa",
    "periodo",
    "curso",
    "instituicao",
]


def _processar_item(model, item_id, form, nome_rotulo):
    if item_id:
        item = db.session.get(model, item_id)
        if not item:
            flash(f"{nome_rotulo} não encontrado.", "danger")
            return redirect(url_for("admin_dashboard"))
    else:
        item = model()

    if form.validate_on_submit():
        for campo in CAMPOS_ITEM:
            if hasattr(form, campo) and hasattr(item, campo):
                setattr(item, campo, getattr(form, campo).data)
        db.session.add(item)
        db.session.commit()
        flash(f"{nome_rotulo} salvo com sucesso.", "success")
        return redirect(url_for("admin_dashboard"))

    if item_id:
        for campo in CAMPOS_ITEM:
            if hasattr(form, campo) and hasattr(item, campo):
                getattr(form, campo).data = getattr(item, campo)

    return render_template(
        "admin/item_form.html",
        titulo_pagina=nome_rotulo,
        form=form,
        acao="editar" if item_id else "novo",
    )


def _excluir_item(model, item_id, nome_rotulo):
    item = db.session.get(model, item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f"{nome_rotulo} excluído.", "success")
    else:
        flash(f"{nome_rotulo} não encontrado.", "danger")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/projetos/novo", methods=["GET", "POST"])
@admin_required
def projeto_novo():
    return _processar_item(Projeto, None, ProjetoForm(), "Projeto")


@app.route("/admin/projetos/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def projeto_editar(item_id):
    return _processar_item(Projeto, item_id, ProjetoForm(), "Projeto")


@app.route("/admin/projetos/<int:item_id>/excluir")
@admin_required
def projeto_excluir(item_id):
    return _excluir_item(Projeto, item_id, "Projeto")


@app.route("/admin/experiencias/novo", methods=["GET", "POST"])
@admin_required
def experiencia_novo():
    return _processar_item(Experiencia, None, ExperienciaForm(), "Experiência")


@app.route("/admin/experiencias/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def experiencia_editar(item_id):
    return _processar_item(Experiencia, item_id, ExperienciaForm(), "Experiência")


@app.route("/admin/experiencias/<int:item_id>/excluir")
@admin_required
def experiencia_excluir(item_id):
    return _excluir_item(Experiencia, item_id, "Experiência")


@app.route("/admin/educacao/novo", methods=["GET", "POST"])
@admin_required
def educacao_novo():
    return _processar_item(Educacao, None, EducacaoForm(), "Educação")


@app.route("/admin/educacao/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def educacao_editar(item_id):
    return _processar_item(Educacao, item_id, EducacaoForm(), "Educação")


@app.route("/admin/educacao/<int:item_id>/excluir")
@admin_required
def educacao_excluir(item_id):
    return _excluir_item(Educacao, item_id, "Educação")


@app.route("/admin/mensagens/<int:item_id>/excluir")
@admin_required
def mensagem_excluir(item_id):
    return _excluir_item(Mensagem, item_id, "Mensagem")


@app.route("/admin/posts/novo", methods=["GET", "POST"])
@admin_required
def post_novo():
    return _processar_item(Post, None, PostForm(), "Postagem")


@app.route("/admin/posts/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def post_editar(item_id):
    return _processar_item(Post, item_id, PostForm(), "Postagem")


@app.route("/admin/posts/<int:item_id>/excluir")
@admin_required
def post_excluir(item_id):
    return _excluir_item(Post, item_id, "Postagem")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
