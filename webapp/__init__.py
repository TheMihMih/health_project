from flask import Flask, render_template, flash, redirect, url_for

from webapp.model import db, User, BDConnector
from webapp.forms import LoginForm, NewsForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


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


    @app.route('/login')
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
                login_user(user)
                flash('Вы успешно авторизировались')
                return redirect(url_for('index'))
            
        flash('Неправильные имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/create_news')
    def create_news():
        title ='Добавление новостей'
        form = NewsForm()
        return render_template('create_news.html', page_title=title, form=form)

    
    @app.route('/process_creating_news', methods=['POST'])
    def process_creating_news():
            form = NewsForm()
            if form.validate_on_submit():
                news_exists = BDConnector.query.filter(BDConnector.title == form.news_title.data).count()
                if news_exists:
                    flash("Новость уже в базе")
                    return redirect(url_for('create_news'))
                else:
                    new_news = BDConnector(title=form.news_title.data, category=form.news_category.data, text=form.news_text.data)
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

    

    return app
