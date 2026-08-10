from functools import wraps

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from forms import (
    EducacaoForm,
    ExperienciaForm,
    PostForm,
    ProjetoForm,
)
from models import Educacao, Experiencia, Mensagem, Post, Projeto, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)

    return wrapper


@admin_bp.route("/")
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
            return redirect(url_for("admin.admin_dashboard"))
    else:
        item = model()
        if isinstance(item, Post):
            item.author = current_user

    if form.validate_on_submit():
        for campo in CAMPOS_ITEM:
            if hasattr(form, campo) and hasattr(item, campo):
                setattr(item, campo, getattr(form, campo).data)
        db.session.add(item)
        db.session.commit()
        flash(f"{nome_rotulo} salvo com sucesso.", "success")
        return redirect(url_for("admin.admin_dashboard"))

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
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/projetos/novo", methods=["GET", "POST"])
@admin_required
def projeto_novo():
    return _processar_item(Projeto, None, ProjetoForm(), "Projeto")


@admin_bp.route("/projetos/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def projeto_editar(item_id):
    return _processar_item(Projeto, item_id, ProjetoForm(), "Projeto")


@admin_bp.route("/projetos/<int:item_id>/excluir")
@admin_required
def projeto_excluir(item_id):
    return _excluir_item(Projeto, item_id, "Projeto")


@admin_bp.route("/experiencias/novo", methods=["GET", "POST"])
@admin_required
def experiencia_novo():
    return _processar_item(Experiencia, None, ExperienciaForm(), "Experiência")


@admin_bp.route("/experiencias/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def experiencia_editar(item_id):
    return _processar_item(Experiencia, item_id, ExperienciaForm(), "Experiência")


@admin_bp.route("/experiencias/<int:item_id>/excluir")
@admin_required
def experiencia_excluir(item_id):
    return _excluir_item(Experiencia, item_id, "Experiência")


@admin_bp.route("/educacao/novo", methods=["GET", "POST"])
@admin_required
def educacao_novo():
    return _processar_item(Educacao, None, EducacaoForm(), "Educação")


@admin_bp.route("/educacao/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def educacao_editar(item_id):
    return _processar_item(Educacao, item_id, EducacaoForm(), "Educação")


@admin_bp.route("/educacao/<int:item_id>/excluir")
@admin_required
def educacao_excluir(item_id):
    return _excluir_item(Educacao, item_id, "Educação")


@admin_bp.route("/mensagens/<int:item_id>/excluir")
@admin_required
def mensagem_excluir(item_id):
    return _excluir_item(Mensagem, item_id, "Mensagem")


@admin_bp.route("/posts/novo", methods=["GET", "POST"])
@admin_required
def post_novo():
    return _processar_item(Post, None, PostForm(), "Postagem")


@admin_bp.route("/posts/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def post_editar(item_id):
    return _processar_item(Post, item_id, PostForm(), "Postagem")


@admin_bp.route("/posts/<int:item_id>/excluir")
@admin_required
def post_excluir(item_id):
    return _excluir_item(Post, item_id, "Postagem")
