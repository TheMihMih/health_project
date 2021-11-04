from datetime import date, datetime

from bs4 import BeautifulSoup

from webapp.news.parser.utils import get_html, save_news

def get_snippets():
    html = get_html('https://food.ru/search?query=%D0%B7%D0%BE%D0%B6&material=article')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find_all('div', class_='grid_container__1uSKI')
        for news in all_news:
            #title = news.find('div', class_='')
            url = news.find('a')
            if url != None:
                print(url)
            #text = news.find('div', class_='markdown_p__1f4Us').text
            #category="Питание"

            #save_news(title, text, category, url)
