from webapp.db import db


class BDFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_food = db.Column(db.String, nullable=False)
    calories = db.Column(db.String, nullable=True)
    joules = db.Column(db.String, nullable=True)
    proteins = db.Column(db.String, nullable=True)
    fats = db.Column(db.String, nullable=True)
    carbohydrates = db.Column(db.String, nullable=True)


    def __repr__(self):
        return f"<Food {self.name_food} {self.calories}kcal>"
