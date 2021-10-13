from typing import Text
from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, PasswordField, SubmitField, BooleanField
=======
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
>>>>>>> b527cc67422bd78f321ba4e43de9f2ec3d51f904
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    email = StringField(
        "Email", validators=[DataRequired()], render_kw={"class": "form-control"}
    )

    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )

    remember_me = BooleanField("Remember Me")

    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


<<<<<<< HEAD
class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    email = StringField(
        "Email", validators=[DataRequired()], render_kw={"class": "form-control"}
    )

    password1 = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )

    password2 = PasswordField(
        "Повторите Пароль",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
=======
    submit = SubmitField("Отправить", render_kw={'class': 'btn btn-primary'})


class NewsForm(FlaskForm):
    news_title = StringField("Заголовок статьи", validators=[DataRequired()], render_kw={'class': 'form-control'})
    news_text = TextAreaField("Текст статьи", validators=[DataRequired()], render_kw={'class': 'form-control'}) 
    news_category = StringField("Категория новости", validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField("Отправить", render_kw={'class': 'btn btn-primary'})
>>>>>>> b527cc67422bd78f321ba4e43de9f2ec3d51f904
