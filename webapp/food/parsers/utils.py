import requests

from webapp.food.models import db, BDFood


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def save_food(food_name, food_calories, food_proteins, food_fats, food_carbohydrates):
    food_exists = BDFood.query.filter(BDFood.name_food == food_name).count()
    if not food_exists:
        new_food = BDFood(
            name_food=food_name,
            calories=food_calories,
            proteins=food_proteins,
            fats=food_fats,
            carbohydrates=food_carbohydrates,
        )
        db.session.add(new_food)
        db.session.commit()
