from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired 


class FoodForm(FlaskForm):
    food_name = StringField(
        "Название продукта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    food_calories = StringField(
        "Калорийность продукта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    food_joules = StringField(
        "Название продукта",
        render_kw={"class": "form-control"},
    )
    food_proteins = StringField(
        "Содержание белков",
        render_kw={"class": "form-control"},
    )
    food_fats = StringField(
        "Содержание жиров",
        render_kw={"class": "form-control"},
    )   
    food_carbohydrates = StringField(
        "Содержание углеводов",
        render_kw={"class": "form-control"},
    )   
        
    food_submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class UserFood(FlaskForm):
    name = StringField(
        "Название продукта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    food_weight = StringField(
        "Вес продукта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )

    submit = SubmitField(
        "Отправить",
        render_kw={"class": "btn btn-primary"}
    )
