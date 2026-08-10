from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Projeto(db.Model):
    __tablename__ = "projetos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tecnologias = db.Column(db.String(255), nullable=False, default="")
    link = db.Column(db.String(255), default="")
    github = db.Column(db.String(255), default="")

    @property
    def tecnologias_lista(self):
        return [t.strip() for t in self.tecnologias.split(",") if t.strip()]


class Experiencia(db.Model):
    __tablename__ = "experiencias"

    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(120), nullable=False)
    empresa = db.Column(db.String(120), nullable=False)
    periodo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=False, default="")


class Educacao(db.Model):
    __tablename__ = "educacao"

    id = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.String(120), nullable=False)
    instituicao = db.Column(db.String(120), nullable=False)
    periodo = db.Column(db.String(80), nullable=False)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    author = db.relationship("User", backref=db.backref("posts", lazy=True))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Mensagem(db.Model):
    __tablename__ = "mensagens"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)
