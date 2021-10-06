from flask import Flask, render_template, flash, redirect, url_for, request
from create_user import create_and_add_user
from webapp.config import SECRET_KEY
from webapp.model import db, User
from webapp.forms import LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = SECRET_KEY
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/index')
    def index():
        page_title = "Главная страница"
        text = """Здесь будет какой-то текст! """
        text2 = """Здесь будет еще какой-то текст! """
        return render_template(
            'index.html', page_title=page_title, text=text, text2=text2
        )
        
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        page_title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=page_title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            email = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data) and email:
                login_user(user)
                flash("Вы успешно вошли на сайт")
                return redirect(url_for('index'))
            
        flash("Неправильные имя или пароль")
        return redirect(url_for('login'))
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash("Вы успешно вышли с сайта")
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @login_required
    def admin():
        if current_user.is_admin:
            return "Привет, Админ"
        
        else:
            return "У Вас нет прав доступа"

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        username = request.args.get("usernamesignup")
        email = request.args.get("emailsignup")
        password1 = request.args.get("passwordsignup")
        password2 = request.args.get("passwordsignup_confirm")
        if password1 == password2:
            password = password2
        create_and_add_user(username, email, password)
        return render_template('register.html')

    return app
