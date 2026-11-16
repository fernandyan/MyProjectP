from flask import Blueprint, flash, redirect, render_template, url_for

import joblib
import pandas as pd

from forms import ContatoForm, DepressionForm, data_science_mental
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

ROTULOS_MENTAL = {
    "age": "Idade",
    "gender": "Gênero",
    "occupation": "Ocupação",
    "region": "Região",
    "most_used_platform": "Plataforma mais usada",
    "platforms_used_count": "Plataformas usadas",
    "daily_screen_hours": "Horas de tela por dia",
    "daily_notifications": "Notificações por dia",
    "night_time_use": "Uso noturno",
    "minutes_to_first_check_after_waking": "Minutos até a 1ª checagem",
    "primary_purpose": "Objetivo principal",
    "avg_sleep_hours": "Horas de sono",
    "anxiety_score_0to27": "Ansiedade (0–27)",
    "low_mood_score_0to27": "Humor baixo (0–27)",
    "life_satisfaction_1to10": "Satisfação com a vida (1–10)",
    "loneliness_1to10": "Solidão (1–10)",
    "self_esteem_1to10": "Autoestima (1–10)",
    "fomo_1to10": "FOMO (1–10)",
    "social_comparison_1to10": "Comparação social (1–10)",
    "physical_activity_days_per_week": "Dias de atividade física",
    "uses_screen_time_limits": "Limite de tempo de tela",
    "attempted_digital_detox": "Já tentou detox digital",
    "seeks_mental_health_support": "Busca apoio psicológico",
}

RESUMO_MENTAL = [
    "age",
    "gender",
    "most_used_platform",
    "daily_screen_hours",
    "avg_sleep_hours",
    "anxiety_score_0to27",
    "low_mood_score_0to27",
    "life_satisfaction_1to10",
    "loneliness_1to10",
    "seeks_mental_health_support",
]

ROTULOS_DEPRESSAO = {
    "gender": "Gênero",
    "age": "Idade",
    "family_background": "Classe familiar",
    "relationship_status": "Relacionamento",
    "marital_status": "Estado civil",
    "living_style": "Estilo de vida",
    "current_semester": "Semestre atual",
    "cgpa": "CGPA (média acadêmica)",
    "friend_circle": "Círculo de amizades",
    "health_condition": "Condição de saúde",
    "cost_without_study": "Custo sem estudo",
    "home_division": "Divisão residencial",
}

RESUMO_DEPRESSAO = [
    "age",
    "gender",
    "current_semester",
    "cgpa",
    "friend_circle",
    "health_condition",
    "family_background",
    "living_style",
]


VALORES_LEGIVEIS = {
    "Female": "Feminino",
    "Male": "Masculino",
    "Yes": "Sim",
    "No": "Não",
    "Yes, failed": "Sim, sem sucesso",
    "Yes, succeeded": "Sim, com sucesso",
    "Considering it": "Considerando",
    "Every night": "Todas as noites",
}


def _valor_legivel(form, campo):
    field = getattr(form, campo)
    valor = field.data
    if valor in VALORES_LEGIVEIS:
        return VALORES_LEGIVEIS[valor]
    opcoes = dict(getattr(field, "choices", []) or [])
    if valor in opcoes:
        return str(opcoes[valor])
    if valor is None:
        return "—"
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def _montar_resumo(form, rotulos, campos):
    return [
        {"rotulo": rotulos[campo], "valor": _valor_legivel(form, campo)}
        for campo in campos
        if hasattr(form, campo)
    ]


def _montar_detalhes(form, rotulos):
    return [
        {"rotulo": rotulo, "valor": _valor_legivel(form, campo)}
        for campo, rotulo in rotulos.items()
        if hasattr(form, campo)
    ]


def _calcular_probabilidades(modelo, df, pred):
    try:
        probabilidades = modelo.predict_proba(df)[0]
        classes = list(modelo.classes_)
    except (AttributeError, NotImplementedError, ValueError):
        return [], None

    itens = [
        {"label": str(classe), "pct": round(float(prob) * 100)}
        for classe, prob in zip(classes, probabilidades)
    ]
    itens.sort(key=lambda item: item["pct"], reverse=True)
    confianca = next(
        (item["pct"] for item in itens if item["label"] == str(pred)),
        itens[0]["pct"] if itens else None,
    )
    return itens, confianca


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


# my make its
@main_bp.route("/data", methods=["GET", "POST"])
def data():
    form = ContatoForm()
    return render_template("data/data.html")

# my make its 2
@main_bp.route("/data_science_mental", methods=["GET", "POST"])
def data_science_metal():

    form = data_science_mental()
    if form.validate_on_submit():
        clf_carregado = joblib.load("classificador.pkl")
        dados = {
            "age": form.age.data,
            "gender": form.gender.data,
            "occupation": form.occupation.data,
            "region": form.region.data,
            "most_used_platform": form.most_used_platform.data,
            "platforms_used_count": form.platforms_used_count.data,
            "daily_screen_hours": form.daily_screen_hours.data,
            "daily_notifications": form.daily_notifications.data,
            "night_time_use": form.night_time_use.data,
            "minutes_to_first_check_after_waking": form.minutes_to_first_check_after_waking.data,
            "primary_purpose": form.primary_purpose.data,
            "avg_sleep_hours": form.avg_sleep_hours.data,
            "anxiety_score_0to27": form.anxiety_score_0to27.data,
            "low_mood_score_0to27": form.low_mood_score_0to27.data,
            "life_satisfaction_1to10": form.life_satisfaction_1to10.data,
            "loneliness_1to10": form.loneliness_1to10.data,
            "self_esteem_1to10": form.self_esteem_1to10.data,
            "fomo_1to10": form.fomo_1to10.data,
            "social_comparison_1to10": form.social_comparison_1to10.data,
            "physical_activity_days_per_week": form.physical_activity_days_per_week.data,
            "uses_screen_time_limits": form.uses_screen_time_limits.data,
            "attempted_digital_detox": form.attempted_digital_detox.data,
            "seeks_mental_health_support": form.seeks_mental_health_support.data,
        }
        df = pd.DataFrame(dados, index=[0])
        pred = str(clf_carregado.predict(df)[0])
        probabilidades, confianca = _calcular_probabilidades(clf_carregado, df, pred)

        flash("Análise concluída com sucesso.", "success")
        return render_template(
            "data/data_science_mental_result.html",
            pred=pred,
            confianca=confianca,
            probabilidades=probabilidades,
            resumo=_montar_resumo(form, ROTULOS_MENTAL, RESUMO_MENTAL),
            detalhes=_montar_detalhes(form, ROTULOS_MENTAL),
        )
    return render_template("data/data_science_mental.html", form=form, contato=contato_info)


@main_bp.route("/student_depression", methods=["GET", "POST"])
def student_depression():

    form = DepressionForm()
    if form.validate_on_submit():
        clf_carregado = joblib.load("student_depression01.pkl")
        dados = {
            "Gender": form.gender.data,
            "Age": form.age.data,
            "Family_background": form.family_background.data,
            "Relationship_status": form.relationship_status.data,
            "Marital_status": form.marital_status.data,
            "Living_style": form.living_style.data,
            "Current_semester": form.current_semester.data,
            "CGPA": form.cgpa.data,
            "friend_circle": form.friend_circle.data,
            "Health_condition": form.health_condition.data,
            "Cost_without_study": form.cost_without_study.data,
            "Home_division": form.home_division.data,
        }
        df = pd.DataFrame(dados, index=[0])
        pred = str(clf_carregado.predict(df)[0])
        probabilidades, confianca = _calcular_probabilidades(clf_carregado, df, pred)

        flash("Análise concluída com sucesso.", "success")
        return render_template(
            "data/depression_result.html",
            pred=pred,
            confianca=confianca,
            probabilidades=probabilidades,
            resumo=_montar_resumo(form, ROTULOS_DEPRESSAO, RESUMO_DEPRESSAO),
            detalhes=_montar_detalhes(form, ROTULOS_DEPRESSAO),
        )
    return render_template("data/depression.html", form=form, contato=contato_info)
