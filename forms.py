from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Usuário", validators=[DataRequired(message="Informe o usuário.")]
    )
    password = PasswordField(
        "Senha", validators=[DataRequired(message="Informe a senha.")]
    )
    submit = SubmitField("Entrar")


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
