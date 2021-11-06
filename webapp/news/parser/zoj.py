import platform
import locale

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from webapp.news.parser.utils import get_html, save_news

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


def parse_date(date_str):
    if "сегодня" in date_str:
        today = datetime.now()
        date_str = date_str.replace("сегодня", today.strftime('%d %B %Y'))
    elif "вчера" in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace("вчера", yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%H:%M %d %B %Y')
    except ValueError:
        return datetime.now()


def get_meal_news():
    html = get_html('https://tolknews.ru/search?q=%D0%9F%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5')
    soup = BeautifulSoup(html, 'html.parser')
    if html:
        all_news = soup.find_all('div', class_='news--simple')
        for news in all_news:
            title = news.find('a')['title']
            #text = news.find('div', class_='news__content').find('a').text
            published = news.find('time').text
            published = parse_date(published)
            category = "Питание"
            url = (f"https://tolknews.ru/{news.find('a')['href']}")
            save_news(title, published, category, url)


def get_train_news():
    html = get_html('https://tolknews.ru/search?q=%D0%A2%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8')
    soup = BeautifulSoup(html, 'html.parser')
    if html:
        all_news = soup.find_all('div', class_='news--simple')
        for news in all_news:
            title = news.find('a')['title']
            #text = news.find('div', class_='news__content').find('a').text
            published = news.find('time').text
            published = parse_date(published)
            category = "Тренировки"
            url = (f"https://tolknews.ru/{news.find('a')['href']}")
            save_news(title, published, category, url)
