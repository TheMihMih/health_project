from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    password = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )

    remember_me = BooleanField(
        "Запомнить меня", default=True, render_kw={"class": "form-check-input"}
    )

    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"},
    )

    password1 = PasswordField(
        "Пароль", validators=[DataRequired()], render_kw={"class": "form-control"}
    )

    password2 = PasswordField(
        "Повторите Пароль",
        validators=[DataRequired(), EqualTo("password1")],
        render_kw={"class": "form-control"},
    )

    submit = SubmitField("Зарегистрироваться", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError("Пользователь с таким именем уже существует!!!")

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError("Пользователь с такой почтой уже существует!!!")


class Personal_Data(FlaskForm):
    user_weight = IntegerField(
        "Вес",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    user_height = IntegerField(
        "Рост",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )   
    gender = RadioField(
        "Пол",
        choices=["Мужской", "Женский"],
        render_kw={"class": "form-control"},
    )
    purpouse = SelectField(
        "Пол",
        choices=["Набрать вес", "Набрать мышечную массу", "Похудеть", "Еще какой-то вариант"],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Сохранить", render_kw={"class": "btn btn-primary"})