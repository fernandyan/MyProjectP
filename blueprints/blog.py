from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from forms import PostForm
from models import Post, db

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")


@blog_bp.route("")
def blog():
    posts = Post.query.order_by(Post.criado_em.desc()).all()
    return render_template("blog.html", posts=posts)


@blog_bp.route("/<int:post_id>")
def post_detalhe(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash("Postagem não encontrada.", "danger")
        return redirect(url_for("blog.blog"))
    return render_template("post.html", post=post)


def _pode_gerenciar_post(post):
    return current_user.is_admin or post.author_id == current_user.id


@blog_bp.route("/novo", methods=["GET", "POST"])
@login_required
def blog_novo():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Postagem criada com sucesso!", "success")
        return redirect(url_for("blog.post_detalhe", post_id=post.id))
    return render_template(
        "blog/post_form.html", form=form, acao="novo", post=None
    )


@blog_bp.route("/<int:post_id>/editar", methods=["GET", "POST"])
@login_required
def blog_editar(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash("Postagem não encontrada.", "danger")
        return redirect(url_for("blog.blog"))
    if not _pode_gerenciar_post(post):
        flash("Acesso restrito: você só pode gerenciar suas próprias postagens.", "danger")
        return redirect(url_for("blog.post_detalhe", post_id=post.id))
    form = PostForm()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.conteudo = form.conteudo.data
        db.session.commit()
        flash("Postagem atualizada com sucesso.", "success")
        return redirect(url_for("blog.post_detalhe", post_id=post.id))
    form.titulo.data = post.titulo
    form.conteudo.data = post.conteudo
    return render_template(
        "blog/post_form.html", form=form, acao="editar", post=post
    )


@blog_bp.route("/<int:post_id>/excluir", methods=["POST"])
@login_required
def blog_excluir(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash("Postagem não encontrada.", "danger")
        return redirect(url_for("blog.blog"))
    if not _pode_gerenciar_post(post):
        flash("Acesso restrito: você só pode gerenciar suas próprias postagens.", "danger")
        return redirect(url_for("blog.post_detalhe", post_id=post.id))
    db.session.delete(post)
    db.session.commit()
    flash("Postagem excluída.", "success")
    return redirect(url_for("blog.blog"))
