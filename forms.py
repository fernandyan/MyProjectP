from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
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
