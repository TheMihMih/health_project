from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user

from webapp.user.models import User
from webapp.user.forms import RegistrationForm, LoginForm

from create_user import create_and_add_user

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно авторизировались')
            return redirect(url_for('news.index'))
        
    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index'))

@blueprint.route('/registr', methods=['POST', 'GET'])
def registr():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    reg_form = RegistrationForm()
    username = request.args.get("usernamesignup")
    email = request.args.get("emailsignup")
    password1 = request.args.get("passwordsignup")
    password2 = request.args.get("passwordsignup_confirm")
    if password1 == password2:
        password = password2
    if username and password and email:
        create_and_add_user(username, email, password)
    return render_template("user/registr.html", form=reg_form)