from webapp.db import db


class BDConnector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)
    image = db.Column(db.BLOB, nullable=True)

    published = db.Column(db.DateTime, nullable=False)

    category = db.Column(
        db.String, nullable=True
    ) 

    def __repr__(self):
        return f"<News {self.title} {self.category}>"
