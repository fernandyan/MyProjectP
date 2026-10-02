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
    
    form = data_science_mental()
    if form.validate_on_submit():
            # Carregando o modelo de volta
            clf_carregado = joblib.load("classificador.pkl")
            dados = {
                'age': form.age.data,
                'gender': form.gender.data,
                'occupation': form.occupation.data,
                'region': form.region.data,
                'most_used_platform': form.most_used_platform.data,
                'platforms_used_count': form.platforms_used_count.data,
                'daily_screen_hours': form.daily_screen_hours.data,
                'daily_notifications': form.daily_notifications.data,
                'night_time_use': form.night_time_use.data,
                'minutes_to_first_check_after_waking': form.minutes_to_first_check_after_waking.data,
                'primary_purpose': form.primary_purpose.data,
                'avg_sleep_hours': form.avg_sleep_hours.data,
                'anxiety_score_0to27': form.anxiety_score_0to27.data,
                'low_mood_score_0to27':form.low_mood_score_0to27.data,
                'life_satisfaction_1to10': form.life_satisfaction_1to10.data,
                'loneliness_1to10': form.loneliness_1to10.data,
                'self_esteem_1to10': form.self_esteem_1to10.data,
                'fomo_1to10': form.fomo_1to10.data,
                'social_comparison_1to10': form.social_comparison_1to10.data,
                'physical_activity_days_per_week': form.physical_activity_days_per_week.data,
                'uses_screen_time_limits': form.uses_screen_time_limits.data,
                'attempted_digital_detox': form.attempted_digital_detox.data,
                'seeks_mental_health_support': form.seeks_mental_health_support.data,
                    }
            df = pd.DataFrame(dados,index=[0])
            print(clf_carregado.predict(df))

            flash("Dados enviada com sucesso!", "success")
            return redirect(url_for("main.index"))
    return render_template("data_science_mental.html", form=form, contato=contato_info)
