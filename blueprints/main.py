from flask import Blueprint, flash, redirect, render_template, url_for

from forms import ContatoForm
from models import Educacao, Experiencia, Mensagem, Projeto, db

main_bp = Blueprint("main", __name__)

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

contato_info = {
    "email": "seuemail@exemplo.com",
    "github": "https://github.com/seu-usuario",
    "linkedin": "https://linkedin.com/in/seu-usuario",
}


@main_bp.route("/")
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
        contato=contato_info,
    )


@main_bp.route("/contato", methods=["GET", "POST"])
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
        return redirect(url_for("main.contato"))
    return render_template("contato.html", form=form, contato=contato_info)
