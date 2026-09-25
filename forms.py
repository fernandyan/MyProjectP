from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    FloatField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField(
        "Usuário", validators=[DataRequired(message="Informe o usuário.")]
    )
    password = PasswordField(
        "Senha", validators=[DataRequired(message="Informe a senha.")]
    )
    submit = SubmitField("Entrar")


class RegistroForm(FlaskForm):
    username = StringField(
        "Usuário",
        validators=[
            DataRequired(message="Informe o usuário."),
            Length(min=3, max=80, message="O usuário deve ter entre 3 e 80 caracteres."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Informe seu email."),
            Email(message="Email inválido."),
        ],
    )
    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Informe a senha."),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(message="Confirme a senha."),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Cadastrar")


class ContatoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[DataRequired(message="Informe seu nome.")]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Informe seu email."),
            Email(message="Email inválido."),
        ],
    )
    mensagem = TextAreaField(
        "Mensagem",
        validators=[
            DataRequired(message="Escreva sua mensagem."),
            Length(max=2000, message="Mensagem muito longa."),
        ],
    )
    submit = SubmitField("Enviar")


class ProjetoForm(FlaskForm):
    titulo = StringField(
        "Título", validators=[DataRequired(message="Informe o título.")]
    )
    descricao = TextAreaField(
        "Descrição",
        validators=[DataRequired(message="Informe a descrição.")],
    )
    tecnologias = StringField(
        "Tecnologias (separadas por vírgula)"
    )
    link = StringField("Link da demo")
    github = StringField("Link do repositório")
    submit = SubmitField("Salvar")


class ExperienciaForm(FlaskForm):
    cargo = StringField(
        "Cargo", validators=[DataRequired(message="Informe o cargo.")]
    )
    empresa = StringField(
        "Empresa", validators=[DataRequired(message="Informe a empresa.")]
    )
    periodo = StringField(
        "Período", validators=[DataRequired(message="Informe o período.")]
    )
    descricao = TextAreaField("Descrição")
    submit = SubmitField("Salvar")


class PostForm(FlaskForm):
    titulo = StringField(
        "Título", validators=[DataRequired(message="Informe o título.")]
    )
    conteudo = TextAreaField(
        "Conteúdo",
        validators=[
            DataRequired(message="Escreva o conteúdo."),
            Length(max=10000, message="Conteúdo muito longo."),
        ],
    )
    submit = SubmitField("Salvar")


class EducacaoForm(FlaskForm):
    curso = StringField(
        "Curso", validators=[DataRequired(message="Informe o curso.")]
    )
    instituicao = StringField(
        "Instituição", validators=[DataRequired(message="Informe a instituição.")]
    )
    periodo = StringField(
        "Período", validators=[DataRequired(message="Informe o período.")]
    )
    submit = SubmitField("Salvar")


class ProdutoForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[DataRequired(message="Informe o nome.")]
    )
    descricao = TextAreaField("Descrição")
    preco_centavos = IntegerField(
        "Preço (em centavos de US$)",
        validators=[
            DataRequired(message="Informe o preço."),
            NumberRange(min=0, message="O preço não pode ser negativo."),
        ],
    )
    disponivel = BooleanField("Disponível para venda", default=True)
    submit = SubmitField("Salvar")

# minha class
class data_science_mental(FlaskForm):
    age = IntegerField("Informe a sua idade por favor!",validators=[DataRequired(message="Informe o idade."),NumberRange(min=0, message="O idade nao pode ser negativo."),],)
    gender = SelectField('Sexo!', choices=[('Female', 'Femenino'), ('Male', 'Masculino')])
    occupation = SelectField('Ocupacao', choices=[
        ('Student', 'Estudante'), 
        ('Full-time employed', 'Empregado em tempo integral'),
        ('Part-time employed', 'Empregado em tempo parcial'),
        ('Self-employed', 'Trabalhadores por conta própria'),
        ('Unemployed', 'Desempregada'),
        ('Retired', 'Aposentada'),
        ])
    region = SelectField('Regiao!', choices=[
        ('Latin America', 'America Latina'), 
        ('Oceania', 'Oceania'),
        ('Africa', 'Africa'),
        ('Europe', 'Europa'),
        ('Asia', 'Asia'),
        ('North America', 'Norte Americana'),
        ])
    most_used_platform = SelectField('Plataforma mais ultilizada!', choices=[
        ('TikTok', 'TikTok'), 
        ('Instagram', 'Instagram'),
        ('YouTube', 'YouTube'),
        ('LinkedIn', 'LinkedIn'),
        ('X/Twitter', 'X/Twitter'),
        ('Facebook', 'Facebook'),
        ('Snapchat', 'Snapchat'),
        ('Reddit', 'Reddit'),
        ])
    platforms_used_count = SelectField('Quantos horas na plataformas utilizadas!', choices=[
        (1, 1), 
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        ])
    daily_screen_hours = FloatField("Informe a sua valor quanto horas voces passa em um plataforma:",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    daily_notifications = IntegerField("Informe a sua quantas notificavao voce recebe por dia:",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    night_time_use = SelectField('Qual e frequncia horas por noite:', choices=[
            ('Never', 'Nunca'), 
            ('Often', 'Frequentemente'),
            ('Every night', 'todos as noite'),
            ('Sometimes', 'As vezes'),
            ])
    minutes_to_first_check_after_waking = IntegerField("Minutos ate a primeira verificacao apos acordar:",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    primary_purpose = SelectField('Plataforma objetivo principal!', choices=[
            ('Entertainment', 'Entretenimento'), 
            ('News/information', 'Noticias/informacoes'),
            ('Work/career', 'Trabalho/carreira'),
            ('Connection with friends', 'Conectar com amigos'),
            ('Passing time/boredom', 'Passar o tempo/tedio'),
            ('Content creation', 'Criacao de conteudo'),
            ])
    avg_sleep_hours = FloatField("Informe media de horas de sono:",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)  
    anxiety_score_0to27 = IntegerField("Digite o numero de assiedade de 0 a 27 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    low_mood_score_0to27 = IntegerField("Digite um escala de mal humor 0 a 27 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    life_satisfaction_1to10 = IntegerField("Digite um escala de vida satifeita 1 a 10 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    loneliness_1to10 = IntegerField("Digite um escala de solidao 1 a 10 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    self_esteem_1to10 = IntegerField("Digite um escala de autoestima 1 a 10 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    fomo_1to10 = IntegerField("Digite um escala de medo nao socilizacao 1 a 10 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    social_comparison_1to10 = IntegerField("Digite um escala de comparacao social 1 a 10 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    physical_activity_days_per_week = IntegerField("atividade social por semana 0 a 7 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    physical_activity_days_per_week = IntegerField("atividade social por semana 0 a 7 :",validators=[DataRequired(message="Informe o valor."),NumberRange(min=0, message="O valor nao pode ser negativo."),],)
    uses_screen_time_limits = SelectField('Voce tem um limeite de tempo de uso de rede social?:', choices=[
            ('No', 'Nao'), 
            ('Yes', 'Sim'),
            ])
    attempted_digital_detox = SelectField('Voce ja buscou com ajuda psicologica?:', choices=[
                ('No', 'Nao'), 
                ('Yes, failed', 'Sim, com frcasso!'),
                ('Yes, succeeded', 'Sim, com sucesso!'), 
                ])
    seeks_mental_health_support = SelectField('Voce ja buscou com ajuda psicologica?:', choices=[
            ('No', 'Nao'), 
            ('Yes', 'Sim'),
            ('Considering it', 'Considerado isso'), 
            ])
    
    submit = SubmitField('Submit')