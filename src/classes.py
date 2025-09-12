import json
import os

from dotenv import load_dotenv

load_dotenv()


class Product:
    """Класс, создающий объект с информацией о продукте"""
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс, создающий объект с информацией о категориях списка продкутов класса Product"""
    total_categories = 0
    total_products = 0
    name: str
    descriprion: str
    products: list[Product]

    def __init__(self, name, decription, products):
        self.name = name
        self.descriprion = decription
        self.products = products
        Category.total_categories += 1
        Category.total_products += len(self.products)


def json_to_classes_object(path=os.getenv("PATH_TO_JSON")):
    """Функция считывает информацию из json-файла, формирует список продуктов с помощью Product
    и возвращает информацию о категориях этих продуктов с помощью класса Category"""
    with open(path, encoding="utf-8") as json_file:
        data = json.load(json_file)
        categories = []
        for category_data in data:
            products = [
                Product(p["name"], p["description"], p["price"], p["quantity"])
                for p in category_data["products"]
            ]
            category = Category(
                category_data["name"], category_data["description"], products
            )
            categories.append(category)
        return categories
