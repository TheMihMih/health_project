from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField
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
    news_category = SelectField(
        'Выберите категорию',
         choices=[('Питание'), ('Тренировки'), ('Новости')],
         render_kw={"class": "form-select"}
    )
    news_image = FileField(
        'Добавьте изображение',
        validators=[FileAllowed(['jpg', 'png'])],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})
