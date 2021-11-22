import requests

from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def save_news(title, published, category, url):
    news_exist = News.query.filter(News.title == title).count()
    if not news_exist:
        new_news = News(
            title=title, published=published, category=category, url=url
        )
        db.session.add(new_news)
        db.session.commit()
