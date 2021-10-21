
from flask import Flask, render_template, flash, redirect, url_for, request, Response
from flask_login.utils import encode_cookie
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from create_user import create_and_add_user
from webapp.model import db, User
from webapp.forms import LoginForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp.model import db, User, BDConnector
from webapp.forms import LoginForm, NewsForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy_imageattach.context import store_context
from werkzeug.utils import secure_filename
from PIL import Image 
from io import BytesIO



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    @app.route('/index')
    def index():
        
        page_title = "Главная страница"
        text = """Мы рады Вас приветствовать на нашем сайте """
        text2 = """Здесь будет интересный блок """
        return render_template(
            'index.html', page_title=page_title, text=text, text2=text2
        )
        
    @app.route('/about')
    def about():
        page_title = "Наш проект"
        return render_template('about.html', page_title=page_title)


    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вы успешно авторизировались')
                return redirect(url_for('index'))
            
        flash('Неправильные имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @login_required
    def admin():
        if current_user.is_admin:
            return "Привет, Админ"
        
        else:
            return "У Вас нет прав доступа"

    @app.route('/registr', methods=['POST', 'GET'])
    def registr():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        reg_form = RegistrationForm()
        username = request.args.get("usernamesignup")
        email = request.args.get("emailsignup")
        password1 = request.args.get("passwordsignup")
        password2 = request.args.get("passwordsignup_confirm")
        if password1 == password2:
            password = password2
        if username and password and email:
            create_and_add_user(username, email, password)
        return render_template("registr.html", form=reg_form)

    

    @app.route('/create_news')
    def create_news():
        title ='Добавление новостей'
        form = NewsForm()
        return render_template('create_news.html', page_title=title, form=form)



    
    @app.route('/process_creating_news', methods=['POST'])
    def process_creating_news():
        form = NewsForm()
        if form.validate_on_submit():
            image_data = request.files[form.news_image.name].read()
            news_exists = BDConnector.query.filter(BDConnector.title == form.news_title.data).count()
            if news_exists:
                flash("Новость уже в базе")
                return redirect(url_for('create_news')) 
            else:
                new_news = BDConnector(title=form.news_title.data, category=form.news_category.data, text=form.news_text.data, image = image_data)
                db.session.add(new_news)
                db.session.commit()
                flash("Вы успешно добавили новость в базу")
                return redirect(url_for('index'))

        flash("Заполните все поля")
        return redirect(url_for('create_news'))

    
    @app.route('/news')
    def display_news():
        title = "Новости Python"
        news_list = BDConnector.query.order_by(BDConnector.id.desc()).all()
        return render_template('news.html', page_title=title, news_list=news_list)




    @app.route('/news/<int:news_id>', methods=['GET'])
    def news(news_id):
        news_context = BDConnector.query.filter(BDConnector.id == news_id).first()
        page_title = news_context.title
        return render_template('news_id.html', page_title=page_title, news_context=news_context)

    @app.route('/img/<int:img_id>')
    def get_image(img_id):
        news_img = BDConnector.query.filter(BDConnector.id == img_id).first()
        if news_img.image:
            image = Image.open(BytesIO(news_img.image))
            output = BytesIO()
            image.save(output, "PNG")
            contents = output.getvalue()
            output.close()

            return Response(contents, mimetype='image/png')

    

    return app
