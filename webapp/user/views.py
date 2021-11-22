from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from webapp.db import db
from webapp.user.models import User
from webapp.user.forms import RegistrationForm, LoginForm

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("news.index"))
    title = "Авторизация"
    login_form = LoginForm()

    return render_template(
        "user/login.html", page_title=title, form=login_form, user=current_user
    )


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно авторизировались")
            return redirect(url_for("news.index"))

    flash("Неправильные имя или пароль")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("news.index"))


@blueprint.route("/registr", methods=["POST", "GET"])
def registr():
    if current_user.is_authenticated:
        return redirect(url_for("news.index"))
    reg_form = RegistrationForm()
    title = "Регистрация"
    return render_template(
        "user/registr.html", form=reg_form, user=current_user, page_title=title
    )


@blueprint.route("/process_reg", methods=["POST"])
def process_reg():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        new_user = User(username=reg_form.username.data, email=reg_form.email.data)
        new_user.set_password(reg_form.password2.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Успешная регистрация пользователя с именем - {reg_form.username.data}")
        return redirect(url_for("user.login"))
    else:
        for field, errors in reg_form.errors.items():
            for error in errors:
                flash(f"Ошибка в {getattr(reg_form, field).label.text}: {error}")
        return redirect(url_for("user.registr"))
