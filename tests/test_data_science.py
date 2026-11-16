import blueprints.main as main_module

from .conftest import csrf_para

PAYLOAD_MENTAL = {
    "age": "25",
    "gender": "Female",
    "occupation": "Student",
    "region": "Europe",
    "most_used_platform": "Instagram",
    "platforms_used_count": "3",
    "daily_screen_hours": "6.5",
    "daily_notifications": "80",
    "night_time_use": "Often",
    "minutes_to_first_check_after_waking": "5",
    "primary_purpose": "Entertainment",
    "avg_sleep_hours": "7",
    "anxiety_score_0to27": "10",
    "low_mood_score_0to27": "8",
    "life_satisfaction_1to10": "7",
    "loneliness_1to10": "4",
    "self_esteem_1to10": "8",
    "fomo_1to10": "5",
    "social_comparison_1to10": "4",
    "physical_activity_days_per_week": "3",
    "uses_screen_time_limits": "Yes",
    "attempted_digital_detox": "No",
    "seeks_mental_health_support": "Considering it",
}

PAYLOAD_DEPRESSAO = {
    "gender": "Female",
    "age": "21",
    "family_background": "Middle class",
    "relationship_status": "Single",
    "marital_status": "Unmarried",
    "living_style": "Bachelor",
    "current_semester": "6",
    "cgpa": "3.5",
    "friend_circle": "Yes",
    "health_condition": "Normal",
    "cost_without_study": "5000",
    "home_division": "Dhaka",
}


class ModeloMentalFake:
    classes_ = ["At-risk", "Good", "Moderate"]

    def predict(self, df):
        return ["Moderate"]

    def predict_proba(self, df):
        return [[0.2, 0.3, 0.5]]


class ModeloDepressaoFake:
    classes_ = ["No", "Yes"]

    def predict(self, df):
        return ["Yes"]

    def predict_proba(self, df):
        return [[0.3, 0.7]]


def test_resultado_mental_exibe_probabilidade_e_resumo(client, monkeypatch):
    monkeypatch.setattr(main_module.joblib, "load", lambda caminho: ModeloMentalFake())
    token = csrf_para(client, "/data_science_mental")

    response = client.post(
        "/data_science_mental",
        data={**PAYLOAD_MENTAL, "csrf_token": token},
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Risco moderado" in html
    assert "Classificação original" in html and "Moderate" in html
    assert "Confiança do modelo" in html and "50%" in html
    assert "Distribuição estimada" in html
    assert "Resumo das suas respostas" in html
    assert "Ver todas as respostas" in html
    assert "Idade" in html and "25" in html
    assert "Feminino" in html


def test_resultado_depressao_exibe_resultado_apoio_e_resumo(client, monkeypatch):
    monkeypatch.setattr(
        main_module.joblib, "load", lambda caminho: ModeloDepressaoFake()
    )
    token = csrf_para(client, "/student_depression")

    response = client.post(
        "/student_depression",
        data={**PAYLOAD_DEPRESSAO, "csrf_token": token},
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Sinais de depressão identificados" in html
    assert "Confiança do modelo" in html and "70%" in html
    assert "Precisa conversar?" in html
    assert "tel:188" in html
    assert "cvv.org.br" in html
    assert "Resumo das suas respostas" in html
    assert "Ver todas as respostas" in html
    assert "Idade" in html and "21" in html


def test_payload_invalido_volta_para_o_formulario(client, monkeypatch):
    monkeypatch.setattr(main_module.joblib, "load", lambda caminho: ModeloMentalFake())
    token = csrf_para(client, "/data_science_mental")

    response = client.post("/data_science_mental", data={"csrf_token": token})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Análise de Impacto Digital" in html
    assert "Risco moderado" not in html
