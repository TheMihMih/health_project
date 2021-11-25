from webapp import create_app
from webapp.food.parsers import parser
from webapp.news.parsers import zoj
from celery import Celery
from celery.schedules import crontab


celery_app = Celery('tasks', broker='redis://localhost:6379/0')

flask_app = create_app()

@celery_app.task
def get_snippets_meal():
    with flask_app.app_context():
        zoj.get_meal_news()

@celery_app.task
def get_snippets_train():
    with flask_app.app_context():
        zoj.get_train_news()

@celery_app.task
def get_content():
    with flask_app.app_context():
        zoj.get_news_content()

@celery_app.task
def get_food():
    with flask_app.app_context():
        parser.page_changer()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, get_snippets_meal.s()) # выполняет каждую минуту или каждые 60 секунд
    sender.add_periodic_task(61, get_snippets_train.s())
    sender.add_periodic_task(70, get_content.s())
    sender.add_periodic_task(crontab(hour=10, minute=10, day_of_week=1), get_food.s())
    #sender.add_periodic_task(crontab(hour=7, minute=30, day_of_week=1), get_content.s())    # выполняет каждый понедельник в 7:30 утра