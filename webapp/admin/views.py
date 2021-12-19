from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import current_user

from webapp.admin.forms import EditForm
from webapp.db import db

from webapp.news.forms import NewsForm
from webapp.news.models import News
from webapp.news.views import news

from webapp.user.decorators import admin_required

from datetime import datetime

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
@admin_required
def admin():
    page_title = "Панель управления"
    text = "Контент админки"
    title = "Редактирование"
    form = EditForm()
    news_edit = News.query.all()
    return render_template(
        "admin/index.html",
        page_title=page_title,
        text=text,
        user=current_user,
        form=form,
        title=title,
        news_edit=news_edit,
    )


@blueprint.route("/news/<int:news_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(news_id):
    form = EditForm()
    news_edit = News.query.filter(News.id == news_id).first()
    if request.method == "GET":
        form.edit_title.data = news_edit.title
        form.edit_text.data = news_edit.text
        form.edit_category.data = news_edit.category
    if form.validate_on_submit():
        news_edit.title = form.edit_title.data
        news_edit.text = form.edit_text.data
        news_edit.category = form.edit_category.data
        db.session.commit()
        flash("Вы успешно отредактировали новость в базе")
        return redirect(url_for("news.index"))
    return render_template(
        "admin/editnews.html", form=form, news_edit=news_edit, user=current_user
    )


@blueprint.route("/process_creating_news", methods=["POST"])
@admin_required
def process_creating_news():
    form = NewsForm()
    if form.validate_on_submit():
        news_exists = News.query.filter(
            News.title == form.news_title.data
        ).count()
        if news_exists:
            flash("Данная новость уже существует в базе")
            return redirect(url_for("admin.create_news"))
        else:
            image_data = request.files[form.news_image.name].read()
            new_news = News(
                title=form.news_title.data,
                category=form.news_category.data,
                text=form.news_text.data,
                image=image_data,
                published=datetime.now(),
            )
            db.session.add(new_news)
            db.session.commit()
            flash("Вы успешно добавили новость в базу")
            return redirect(url_for("news.index"))

    flash("Заполните все поля")
    return redirect(url_for("admin.create_news"))


@blueprint.route("/create_news")
@admin_required
def create_news():
    title = "Добавление новостей"
    form = NewsForm()
    return render_template(
        "admin/create_news.html", page_title=title, form=form, user=current_user
    )
