from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    news_title = StringField(
        "Заголовок статьи",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    news_text = TextAreaField(
        "Текст статьи", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    news_category = StringField(
        "Категория новости",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
