from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from webapp.news.models import News


class NewsForm(FlaskForm):
    news_title = StringField(
        "Заголовок статьи",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    news_text = TextAreaField(
        "Текст статьи", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    news_category = SelectField(
        "Выберите категорию",
        choices=[("Питание"), ("Тренировки"), ("Новости")],
        render_kw={"class": "form-select"},
    )
    news_image = FileField(
        "Добавьте изображение",
        validators=[FileAllowed(["jpg", "png"])],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})


class SearchForm(FlaskForm):
    search_news = StringField(
        "Поиск новостей",
        render_kw={"class": "form-control", "placeholder": "Поиск новостей"},
    )
    submit = SubmitField("Поиск", render_kw={"class": "btn btn-outline-secondary"})

class CommentForm(FlaskForm):
    news_id = HiddenField(
        'ID новости', 
        validators=[DataRequired()]
        )
    comment_text = StringField(
        'Ваш комментарий', 
        validators=[DataRequired()], 
        render_kw={"class": "form-control"}
        )
    submit = SubmitField("Комментировать", render_kw={"class": "btn btn-primary"})

    def validate_news_id(self, news_id):
        if not News.query.get(news_id.data):
            raise ValidationError("Вы пытаетесь прокомментировать новость с несуществующим ID")