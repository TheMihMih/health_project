from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from webapp.db import db
from webapp.user.models import User, PersonalData
from webapp.user.forms import Personal_Data, RegistrationForm, LoginForm
from webapp.utils import get_redirect_target

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
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
            return redirect(get_redirect_target())

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


@blueprint.route("/personaldata_edit", methods=["GET", "POST"])
def process_personaldata_edit():
    form = Personal_Data()
    data_edit = PersonalData.query.filter(PersonalData.user_id == current_user.id).first()
    if data_edit:
        if request.method == "GET":
            form.user_weight.data = data_edit.user_weight
            form.user_height.data = data_edit.user_height
            form.gender.data = data_edit.gender
            form.purpouse.data = data_edit.purpouse
        if form.validate_on_submit():
            data_edit.user_weight = form.user_weight.data
            data_edit.user_height = form.user_height.data
            data_edit.gender = form.gender.data
            data_edit.purpouse = form.purpouse.data
            db.session.commit()
            flash("Вы успешно отредактировали личные данные")
            return redirect(url_for("user.personaldata"))
    else:
        new_data = PersonalData(
            user_weight = form.user_weight.data,
            user_height = form.user_height.data,
            gender = form.gender.data,
            purpouse = form.purpouse.data,
            user_id = current_user.id
        )
        db.session.add(new_data)
        db.session.commit()
        return render_template(
            "user/personaldata_edit.html",
            form=form,
            data_edit=data_edit,
            user=current_user
        )
    return render_template(
        "user/personaldata_edit.html", form=form, data_edit=data_edit, user=current_user
    )


@blueprint.route("/personaldata", methods=["GET"])
def personaldata():
    page_title = "Личный кабинет"
    data = PersonalData.query.filter(PersonalData.user_id == current_user.id).first()
    if not data:
        data = None
    return render_template(
        "user/personaldata.html", data=data, user=current_user, page_title=page_title
    )