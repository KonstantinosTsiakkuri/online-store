import json
import os

from dotenv import load_dotenv

load_dotenv()


class Product:
    """Класс, создающий объект с информацией о продукте"""

    name: str
    description: str
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, products):
        """Класс метод для создания продукта из словаря."""
        if isinstance(products, list):
            product_dict = products[0]
        else:
            product_dict = products
        return cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = price

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Ошибка сложения разных товаров")
        else:
            product1 = self.quantity * self.price
            product2 = other.quantity * other.price
            return product1 + product2


class Smartphone(Product):
    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)

        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)

        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс, создающий объект с информацией о категориях списка продкутов класса Product"""

    category_count = 0
    product_count = 0
    name: str
    description: str

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только продукты или их наследников")

    @property
    def products(self):
        result_string = ""
        for product in self.__products:
            result_string += f"{str(product)}\n"
        return result_string

    def __str__(self):
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class CategoryIter:
    """Класс для итерации по продуктам категории"""

    def __init__(self, category):
        self.category = category
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.category._Category__products):
            current_product = self.category._Category__products[self.index]
            self.index += 1
            return current_product
        else:
            raise StopIteration


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
