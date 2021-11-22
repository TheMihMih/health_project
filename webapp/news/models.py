from datetime import datetime
from webapp.db import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)
    url = db.Column(db.String, nullable=True)
    image = db.Column(db.BLOB, nullable=True)

    published = db.Column(db.DateTime, nullable=False)

    category = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<News {self.title} {self.category}>"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )

    def __repr__(self):
        return f"<Comment {self.id}>"