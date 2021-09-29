from os import times
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, BDConnector

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def find_health_news():
    html = get_html('ТУТ БУДУТ АДРЕСА ДЛЯ НОВОСТЕЙ') #Возможно стоит делать это в цикле 
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, "%Y-%m-%d")
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)

def save_news(title, url, published):
    news_exists = BDConnector.query.filter(BDConnector.url == url).count()
    print(news_exists)
    if not news_exists:
        new_news = BDConnector(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()
