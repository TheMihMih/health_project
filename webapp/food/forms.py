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
    food_proteins = StringField(
        "Содержание белка, г.",
        render_kw={"class": "form-control"},
    )
    food_fats = StringField(
        "Содержание жира, г.",
        render_kw={"class": "form-control"},
    )   
    food_carbohydrates = StringField(
        "Содержание углеводов, г.",
        render_kw={"class": "form-control"},
    )   
        
    food_submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class UserFood(FlaskForm):
    food_name = StringField(
        "Название продукта",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    food_weight = StringField(
        "Вес продукта, г.",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField(
        "Отправить",
        render_kw={"class": "btn btn-secondary"}
    )
