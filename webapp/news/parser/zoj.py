import platform
import locale
import urllib.request

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from webapp.news.parser.utils import get_html, save_news
from webapp.news.models import BDConnector
from webapp import db

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


def parse_date(date_str):
    if "сегодня" in date_str:
        today = datetime.now()
        date_str = date_str.replace("сегодня", today.strftime("%d %B %Y"))
    elif "вчера" in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace("вчера", yesterday.strftime("%d %B %Y"))
    try:
        return datetime.strptime(date_str, "%d/%B/%Y")
    except ValueError:
        return datetime.now()


def get_meal_news():
    html = get_html(
        "https://www.fontanka.ru/cgi-bin/search.scgi?query=%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5&rubric=family&fdate=2000-01-01&tdate=2021-11-13&sortt=date"
    )
    soup = BeautifulSoup(html, "html.parser")
    if html:
        all_news = soup.find_all("li", class_="B5kp GRb5")
        for news in all_news:
            title = news.find("a", class_="B5i7")["title"]
            published = (
                news.find("div", class_="B5kr B5br").find("time").find("span").text
            )
            published = parse_date(published)
            category = "Питание"
            url = f"https://www.fontanka.ru{news.find('a', class_='B5i7')['href']}"
            save_news(title, published, category, url)


def get_train_news():
    html = get_html(
        "https://www.fontanka.ru/cgi-bin/search.scgi?query=%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8&rubric=family&fdate=2000-01-01&tdate=2021-11-13&sortt=weight"
    )
    soup = BeautifulSoup(html, "html.parser")
    if html:
        all_news = soup.find_all("li", class_="B5kp GRb5")
        for news in all_news:
            title = news.find("a", class_="B5i7")["title"]
            published = (
                news.find("div", class_="B5kr B5br").find("time").find("span").text
            )
            published = parse_date(published)
            category = "Тренировки"
            url = f"https://www.fontanka.ru{news.find('a', class_='B5i7')['href']}"
            save_news(title, published, category, url)


def get_news_content():
    news_without_text = BDConnector.query.filter(BDConnector.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            paragraph = soup.find("div", class_="F3h C1b5").text
            if paragraph:
                news.text = paragraph
            try:
                news_image = soup.find("picture", class_="Nbb GJmr")["data-flickity-lazyload"]
                image_bytes = urllib.request.urlopen(news_image).read()
                news.image = image_bytes
                db.session.add(news)
                db.session.commit()
                
            except TypeError:
                print("Нет картинки")
