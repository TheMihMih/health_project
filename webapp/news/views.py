from flask import abort, Blueprint, render_template, Response, flash, request
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.utils import redirect
from webapp.news.forms import SearchForm, CommentForm
from webapp.news.models import Comment, News
from PIL import Image
from io import BytesIO
from fuzzywuzzy import fuzz
from webapp.food.views import graph_maker
from webapp.db import db
from webapp.utils import get_redirect_target

blueprint = Blueprint("news", __name__)


@blueprint.route("/")
@blueprint.route("/index")
def index():
    page_title = "Главная страница"
    text = """Мы рады Вас приветствовать на нашем сайте """
    text2 = """Здесь будет интересный блок """
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.id.desc()).limit(5)
    if current_user.is_authenticated:
        script, div, data_check = graph_maker(3)
        return render_template(
            "news/index.html",
            page_title=page_title,
            text=text,
            text2=text2,
            user=current_user,
            news_list=news_list,
            the_script=script,
            the_div=div,
            data_check=data_check,
        )
    return render_template(
        "news/index.html",
        page_title=page_title,
        text=text,
        text2=text2,
        user=current_user,
        news_list=news_list,
    )


@blueprint.route("/about")
def about():
    page_title = "Наш проект"
    return render_template("news/about.html", page_title=page_title, user=current_user)


@blueprint.route("/news")
def display_news():
    form = SearchForm()
    title = "Новости"
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.id.desc()).all()
    return render_template(
        "news/news.html",
        page_title=title,
        form=form,
        news_list=news_list,
        user=current_user,
    )


@blueprint.route("/process_searching_news", methods=["GET"])
def process_searching_news():
    form = SearchForm()
    title = "Новости Python"
    search_title = request.values[form.search_news.name]
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.id.desc()).all()
    news_exists = []
    if form.validate_on_submit:
        for news in news_list:
            Ratio = fuzz.token_sort_ratio(news.title, search_title)
            if Ratio >= 50:
                news_exists += News.query.filter(
                    News.title == news.title
                ).all()
        if news_exists:
            return render_template(
                "news/news.html",
                page_title=title,
                form=form,
                news_list=news_exists,
                user=current_user,
            )
        flash("Новость не найдена, попробуйте изменить запрос")
        return render_template(
            "news/news.html",
            page_title=title,
            form=form,
            news_list=news_list,
            user=current_user,
        )


@blueprint.route("/news/<int:news_id>", methods=["GET"])
def news(news_id):
    news_context = News.query.filter(News.id == news_id).first()
    if not news_context:
        abort(404)
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.id.desc()).limit(5)
    comment_form = CommentForm(news_id=news_context.id)
    return render_template(
        "news/news_id.html",
        page_title=news_context.title,
        news_context=news_context,
        news_list=news_list,
        user=current_user,
        comment_form=comment_form,
    )


@blueprint.route("/news/comment", methods=["POST"])
@login_required
def add_comment():
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            text=comment_form.comment_text.data, 
            news_id=comment_form.news_id.data, 
            user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash("Спасибо за Ваш комментарий")
    else:
        for field, errors in comment_form.errors.items():
            for error in errors:
                flash(f"Ошибка в {getattr(comment_form, field).label.text}: {error}")
    return redirect(get_redirect_target())


@blueprint.route("/img/<int:img_id>")
def get_image(img_id):
    news_img = News.query.filter(News.id == img_id).first()
    if news_img.image:

        image = Image.open(BytesIO(news_img.image))
        output = BytesIO()
        image.save(output, "PNG")
        contents = output.getvalue()
        output.close()

        return Response(contents, mimetype="image/png")


@blueprint.route("/category/<url>", methods=["GET"])
def category(url):
    if url == "meal":
        category_list = News.query.filter(
            News.category == "Питание"
        ).all()
        page_title = "Новости про питание"
    elif url == "train":
        category_list = News.query.filter(
            News.category == "Тренировки"
        ).all()
        page_title = "Новости про тренировки"

    return render_template(
        "news/category.html",
        category_list=category_list,
        page_title=page_title,
        user=current_user,
    )
