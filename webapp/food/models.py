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


class DailyConsumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_cons = db.Column(db.Integer, nullable=False)
    cons_product = db.Column(db.String, nullable=False)
    cons_calories = db.Column(db.Float, nullable=False)
    cons_prots = db.Column(db.Float, nullable=True)
    cons_fats = db.Column(db.Float, nullable=True)
    cons_carbos = db.Column(db.Float, nullable=True)
    cons_weight = db.Column(db.Float, nullable=False)
    cons_day = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Consumed {self.cons_weight} {self.cons_product}kcal>"
