from flask import Flask, render_template
from webapp.model import db, BDConnector


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        news_list = BDConnector.query.order_by(BDConnector.published.desc()).all()
        return render_template('index.html', news_list=news_list)


    @app.route('/about')
    def about():
        return render_template('about.html')

    return app
