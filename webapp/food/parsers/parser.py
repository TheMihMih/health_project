from bs4 import BeautifulSoup
import requests
from webapp.food.parsers.utils import get_html, save_food


def page_counter(url):
    soup = BeautifulSoup(get_html(url), "html.parser")
    page_number = int(soup.find("ul", class_="pager-long").find_all("li")[-2].text)

    return page_number


def page_changer():
    url = "https://calorizator.ru/product/all"
    pages = page_counter(url)
    for page in range(pages):
        if page == 0:
            html = get_html(url)
        else:
            url = f"https://calorizator.ru/product/all&page={page}"
            html = get_html(url)
        page += 1
        if html:
            soup = BeautifulSoup(html, "html.parser")
            all_food_even = soup.find("div", class_="view-product-all").findAll(
                "tr", class_="even"
            )
            food_finder(all_food_even)
            all_food_odd = soup.find("div", class_="view-product-all").findAll(
                "tr", class_="odd"
            )
            food_finder(all_food_odd)


def food_finder(all_food):
    for food in all_food:
        food_name = food.find("td", class_="views-field-title").text
        food_calories = food.find("td", class_="views-field-field-kcal-value").text
        food_fats = food.find("td", class_="views-field-field-fat-value").text
        food_proteins = food.find("td", class_="views-field-field-protein-value").text
        food_carbohydrates = food.find(
            "td", class_="views-field-field-carbohydrate-value"
        ).text

        food_name = food_name.strip()
        food_calories = food_calories.strip()
        food_fats = food_fats.strip()
        food_proteins = food_proteins.strip()
        food_carbohydrates = food_carbohydrates.strip()

        save_food(
            food_name, food_calories, food_fats, food_proteins, food_carbohydrates
        )
