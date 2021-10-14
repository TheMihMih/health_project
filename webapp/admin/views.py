from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from webapp.db import db

from webapp.news.forms import NewsForm
from webapp.news.models import BDConnector

from datetime import datetime

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
@login_required
def admin():
    if current_user.is_admin:
        page_title = "Администратор"
        text = "Привет, Админ"
        return render_template("index.html", page_title=page_title, text=text)


@blueprint.route("/process_creating_news", methods=["POST"])
def process_creating_news():
    if current_user.is_admin:
        form = NewsForm()
        if form.validate_on_submit():
            news_exists = BDConnector.query.filter(
                BDConnector.title == form.news_title.data
            ).count()
            if news_exists:
                flash("Данная новость уже существует в базе")
                return redirect(url_for("admin.create_news"))
            else:
                new_news = BDConnector(
                    title=form.news_title.data,
                    category=form.news_category.data,
                    text=form.news_text.data,
                    published=datetime.now(),
                )
                db.session.add(new_news)
                db.session.commit()
                flash("Вы успешно добавили новость в базу")
                return redirect(url_for("news.index"))
    else:
        return redirect(url_for("news.index"))

    flash("Заполните все поля")
    return redirect(url_for("create_news"))


@blueprint.route("/create_news")
def create_news():
    if current_user.is_admin:
        title = "Добавление новостей"
        form = NewsForm()
        return render_template("create_news.html", page_title=title, form=form)

    else:
        return redirect(url_for("news.index"))
