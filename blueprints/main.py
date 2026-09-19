from flask import Blueprint, flash, redirect, render_template, url_for

from forms import ContatoForm, data_science_mental
from models import Educacao, Experiencia, Mensagem, Projeto, db
import joblib
import pandas as pd
import sklearn
#print(sklearn.__version__)

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


@main_bp.route("/data_science_mental", methods=["GET", "POST"])
def data_science_metal():
    # Carregando o modelo de volta
    clf_carregado = joblib.load("classificador.pkl")
    dados = {
    'age': 31,
    'gender': 'Female',
    'occupation':'Full-time employed',
    'region':'Asia',
    'most_used_platform':'Instagram',
    'platforms_used_count':4,
    'daily_screen_hours':2.9,
    'daily_notifications':70,
    'night_time_use':'Often',
    'minutes_to_first_check_after_waking':44,
    'primary_purpose':'Entertainment',
    'avg_sleep_hours':6.9,
    'anxiety_score_0to27':14,
    'low_mood_score_0to27':6,
    'life_satisfaction_1to10':8,
    'loneliness_1to10':9,
    'self_esteem_1to10':6,
    'fomo_1to10':1,
    'social_comparison_1to10':6,
    'physical_activity_days_per_week':4,
    'uses_screen_time_limits':'No',
    'attempted_digital_detox':'Yes, succeeded',
    'seeks_mental_health_support':'Yes',
        }
    df = pd.DataFrame(dados,index=[0])
    # print("tudo feito com sucesso no data science!!!!!!")
    # print(clf_carregado.predict(df))
    form = data_science_mental()
    if form.validate_on_submit():
            flash("Dados enviada com sucesso!", "success")
            return redirect(url_for("main.index"))
    return render_template("data_science_mental.html", form=form, contato=contato_info)
