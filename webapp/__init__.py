<<<<<<< HEAD
from flask import Flask, render_template, flash, redirect, url_for
from webapp.config import SECRET_KEY
from webapp.model import db, User
from webapp.forms import LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user
=======
from flask import Flask, render_template
from webapp.model import db, BDConnector
>>>>>>> aafe73ee198626047798ed04836a4120b329e4f8


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
<<<<<<< HEAD
    app.secret_key = SECRET_KEY
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        page_title = "Главная страница"
        text = """Здесь будет какой-то текст! """
        text2 = """Здесь будет еще какой-то текст! """
        return render_template(
            'index.html', page_title=page_title, text=text, text2=text2
        )
        
=======
    db.init_app(app)

    @app.route('/')
    def index():
        news_list = BDConnector.query.order_by(BDConnector.published.desc()).all()
        return render_template('index.html', news_list=news_list)


>>>>>>> aafe73ee198626047798ed04836a4120b329e4f8
    @app.route('/about')
    def about():
        return render_template('about.html')

<<<<<<< HEAD
    @app.route('/login')
    def login():
        if current_user.is_authenticated():
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

=======
>>>>>>> aafe73ee198626047798ed04836a4120b329e4f8
    return app
