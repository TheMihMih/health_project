from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user
from datetime import date
from webapp.db import db

from webapp.food.forms import FoodForm, UserFood
from webapp.food.models import BDFood


blueprint = Blueprint("food", __name__, url_prefix="/food")

@blueprint.route("/process_adding_food", methods=["POST"])
def process_adding_food():
    form = FoodForm()
    if form.validate_on_submit():
        food_ex = BDFood.query.filter(
            BDFood.name_food == form.food_name.data
        ).count()
        if food_ex:
            flash("Данный продукт существует в базе")
            return redirect(url_for("news.index"))
        else:
            new_food = BDFood(
                name_food=form.food_name.data,
                calories=form.food_calories.data,
                joules=form.food_joules.data,
                proteins=form.food_proteins.data,
                fats=form.food_fats.data,
                carbohydrates=form.food_carbohydrates.data
            )
            db.session.add(new_food)
            db.session.commit()
            flash("Вы успешно добавили продукт в базу")
            return redirect(url_for("news.index"))

    flash("Заполните название и калорийность поля")
    return redirect(url_for("news.index"))


@blueprint.route("/add_food")
def add_food():
    title = "Добавление продуктов"
    form = FoodForm()
    return render_template(
        "food/add_food.html", page_title=title, form=form, user=current_user
    )


@blueprint.route("/food_count")
def counter():
    title = "Счетчик калорий"
    form = UserFood()
    return render_template(
        "food/food_count.html", page_title=title, form=form, user=current_user
    )

TODAY = date.today()

@blueprint.route("/process_addind_calories")
def process_addind_calories():
    title = "Счетчик калорий"
    form = UserFood()

    if form.validate_on_submit():
        product_consumed = BDFood.query.filter(BDFood.name_food == form.food_name.data).first()
        weight_consumed = float(form.food_weight.data)
        if product_consumed:
            сalories_consumed = weight_consumed * float(product_consumed.calories)
            proteins_consumed = weight_consumed * float(product_consumed.proteins)
            fats_consumed = weight_consumed * float(product_consumed.fats)
            сarbohydrates_consumed = weight_consumed * float(product_consumed.сarbohydrates)
            

            


    return render_template(
        "food/food_count.html", page_title=title, form=form, user=current_user
    )