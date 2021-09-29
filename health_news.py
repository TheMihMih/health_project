from flask import app
from webapp import create_app
from webapp.find_health_news import find_health_news

app = create_app()
with app.app_context():
    find_health_news()
    