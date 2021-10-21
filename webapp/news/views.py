from flask import Blueprint, render_template, Response, flash
from flask_login import current_user
from webapp.news.models import BDConnector
from PIL import Image 
from io import BytesIO

blueprint = Blueprint("news", __name__)


@blueprint.route("/")
@blueprint.route("/index")
def index():
    page_title = "Главная страница"
    text = """Мы рады Вас приветствовать на нашем сайте """
    text2 = """Здесь будет интересный блок """
    return render_template(
        "news/index.html",
        page_title=page_title,
        text=text,
        text2=text2,
        user=current_user,
    )


@blueprint.route("/about")
def about():
    page_title = "Наш проект"
    return render_template("news/about.html", page_title=page_title, user=current_user)


@blueprint.route("/news")
def display_news():
    title = "Новости Python"
    news_list = BDConnector.query.order_by(BDConnector.id.desc()).all()
    return render_template(
        "news/news.html", page_title=title, news_list=news_list, user=current_user
    )


@blueprint.route("/news/<int:news_id>", methods=["GET"])
def news(news_id):
    news_context = BDConnector.query.filter(BDConnector.id == news_id).first()
    page_title = news_context.title
    return render_template(
        "news/news_id.html",
        page_title=page_title,
        news_context=news_context,
        user=current_user,
    )


@blueprint.route('/img/<int:img_id>')
def get_image(img_id):
    news_img = BDConnector.query.filter(BDConnector.id == img_id).first()
    if news_img.image:

        image = Image.open(BytesIO(news_img.image))
        output = BytesIO()
        image.save(output, "PNG")
        contents = output.getvalue()
        output.close()

        return Response(
            contents,
            mimetype='image/png'
        )
