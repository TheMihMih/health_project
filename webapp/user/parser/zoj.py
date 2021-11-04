import datetime
import requests
from requests.api import request

from webapp.db import db
from webapp.news.models import BDConnector

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False

def save_news(title, text, category):
    news_exist = BDConnector.query.filter(BDConnector.title == title).count()
    if not news_exist:
        new_news = BDConnector(title=title, text=text, publised=datetime.now(), category=category)
        db.session.add(new_news)
        db.session.commit()