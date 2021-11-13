from webapp import create_app
from webapp.news.parser import zoj

app = create_app()
with app.app_context():
    zoj.get_meal_news()
    zoj.get_train_news()
    zoj.get_news_content()
