import datetime
import requests

from webapp.db import db
from webapp.news.models import BDConnector

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
        }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False

def save_news(title, text, category, url):
    news_exist = BDConnector.query.filter(BDConnector.title == title).count()
    if not news_exist:
        new_news = BDConnector(title=title, text=text, publised=datetime.now(), category=category, url=url)
        db.session.add(new_news)
        db.session.commit()