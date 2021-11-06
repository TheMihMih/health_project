from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import current_user
from datetime import date

from flask_login.utils import login_required
from webapp.db import db

from webapp.food.forms import FoodForm, UserFood
from webapp.food.models import BDFood, DailyConsumption


blueprint = Blueprint("food", __name__, url_prefix="/food")


@blueprint.route("/process_adding_food", methods=["POST"])
@login_required
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
            return redirect(url_for("food.food_count"))

    flash("Заполните название и калорийность поля")
    return redirect(url_for("food.add_food"))


@blueprint.route("/add_food")
def add_food():
    title = "Добавление продуктов"
    form = FoodForm()
    return render_template(
        "food/add_food.html", page_title=title, form=form, user=current_user
    )


@blueprint.route("/food_count")
def food_count():
    title = "Счетчик калорий"
    form = UserFood()
    today = date.today().strftime("%d/%m/%Y")
    daily_consumption = daily_counter(today)
    return render_template(
        "food/food_count.html", page_title=title, form=form, daily_consumption=daily_consumption, user=current_user
    )



@blueprint.route("/process_adding_calories", methods=['GET'])
@login_required
def process_adding_calories():
    form = UserFood()
    today = date.today().strftime("%d/%m/%Y")
    #if form.validate_on_submit():
    food_consumed = BDFood.query.filter(BDFood.name_food == request.values[form.food_name.name]).first()
    weight_consumed = float(request.values[form.food_weight.name])
    if food_consumed:
        product_consumed = food_consumed.name_food
        сalories_consumed = weight_consumed * float(food_consumed.calories) * 0.01
        proteins_consumed = weight_consumed * float(food_consumed.proteins) * 0.01
        fats_consumed = weight_consumed * float(food_consumed.fats) * 0.01
        carbohydrates_consumed = weight_consumed * float(food_consumed.carbohydrates) * 0.01
        consumption_date = today

        new_consumption = DailyConsumption(
            user_cons=current_user.id,
            cons_product=product_consumed,
            cons_calories=сalories_consumed,
            cons_prots=proteins_consumed,
            cons_fats=fats_consumed,
            cons_carbos=carbohydrates_consumed,
            cons_weight=weight_consumed,
            cons_day=consumption_date
        )
        db.session.add(new_consumption)
        db.session.commit()
        daily_consumption = daily_counter(today)

        flash(f"Сегодня Вы покушали на {daily_consumption[0]} калорий")
        return redirect(url_for("food.food_count"))
    else:
        flash(
            f"Вы ввели: {request.values[form.food_name.name]}"
            f"Данный продукт отсутствует в базе. Попробуйте изменить запрос или добавьте продукт в базу"
        )
        return redirect(url_for("food.food_count"))
    #flash('form not validate')
    #return redirect(url_for("food.food_count"))


def daily_counter(today):

    daily_consumption = DailyConsumption.query.filter(
    DailyConsumption.user_cons == current_user.id,
    DailyConsumption.cons_day == today
    ).all()
    daily_consumption_cals = 0
    daily_consumption_prots = 0
    daily_consumption_fats = 0
    daily_consumption_carbos = 0
    for i in daily_consumption:
        daily_consumption_cals += i.cons_calories
        daily_consumption_prots += i.cons_prots
        daily_consumption_fats += i.cons_fats
        daily_consumption_carbos += i.cons_carbos
    return daily_consumption_cals, daily_consumption_prots, daily_consumption_fats, daily_consumption_carbos

