from flask import Blueprint, render_template, Response, flash, request
from flask_login import current_user
from webapp.news.forms import SearchForm
from webapp.news.models import BDConnector
from PIL import Image 
from io import BytesIO
from fuzzywuzzy import fuzz

blueprint = Blueprint("news", __name__)


@blueprint.route("/")
@blueprint.route("/index")
def index():
    page_title = "Главная страница"
    text = """ Мы рады Вас приветствовать на нашем сайте """
    text2 = """ Вы найдете много интересных новостей на нашем сайте """
    return render_template(
        "news/index.html",
        page_title=page_title,
        text=text,
        text2=text2,
        user=current_user
    )


@blueprint.route("/about")
def about():
    page_title = "Наш проект"
    return render_template("news/about.html", page_title=page_title, user=current_user)


@blueprint.route("/news")
def display_news():
    form = SearchForm()
    title = "Новости Python"
    news_list = BDConnector.query.order_by(BDConnector.id.desc()).all()
    return render_template(
        "news/news.html", page_title=title, form=form, news_list=news_list, user=current_user
    )


@blueprint.route("/process_searching_news", methods=["GET"])
def process_searching_news():
    form = SearchForm()
    title = "Новости Python"
    search_title = request.values[form.search_news.name]
    news_list = BDConnector.query.order_by(BDConnector.id.desc()).all()
    news_exists = []
    if form.validate_on_submit:
        for news in news_list:
            Ratio = fuzz.token_sort_ratio(news.title, search_title)
            if Ratio >= 50:
                news_exists += BDConnector.query.filter(BDConnector.title == news.title).all()
        if news_exists:
            return render_template(
                "news/news.html", page_title=title, form=form, news_list=news_exists, user=current_user
            )
        flash('Новость не найдена, попробуйте изменить запрос')
        return render_template(
            "news/news.html", page_title=title, form=form, news_list=news_list, user=current_user
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
