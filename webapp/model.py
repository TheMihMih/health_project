from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BDConnector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    text = db.Column(db.Text, nullable=True)
    category = db.Column(db.Integer, nullable=True) #Какие категории? Спорт, питание... Возможно стоит сделать не Int, а String
    published = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)

