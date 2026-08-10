from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from forms import LoginForm, RegistroForm
from models import User, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistroForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Nome de usuário já está em uso.", "danger")
            return render_template("auth/registro.html", form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash("Email já cadastrado.", "danger")
            return render_template("auth/registro.html", form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/registro.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login realizado com sucesso.", "success")
            destino = "admin.admin_dashboard" if user.is_admin else "main.index"
            return redirect(url_for(destino))
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("main.index"))
