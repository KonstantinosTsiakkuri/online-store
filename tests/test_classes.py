import pytest

from src import classes


class TestProduct:
    def test_initialisation(self):
        product = classes.Product("Laptop", "Portable computer", 1500.0, 10)
        assert product.name == "Laptop"
        assert product.description == "Portable computer"
        assert product.price == 1500
        assert product.quantity == 10

    def test_price_setter_positive(self):
        product = classes.Product("Laptop", "Portable computer", 1500.0, 10)
        product.price = 2000
        assert product.price == 2000

    def test_price_setter_negative(self, capsys):
        product = classes.Product("Laptop", "Portable computer", 1500.0, 10)
        product.price = -1000
        captured = capsys.readouterr()
        assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
        assert product.price == 1500  # цена не должна измениться


class TestCategory:
    def setup_method(self):
        # Сбрасываем счётчики перед каждым тестом
        classes.Category.category_count = 0
        classes.Category.product_count = 0

    def test_initialisation(self):
        category = classes.Category("Laptop", "Portable Computer", [])
        assert category.name == "Laptop"
        assert category.description == "Portable Computer"
        assert category.products[0] == []

    def test_total_categories_and_products(self):
        # Создание категорий с продуктами
        category1 = classes.Category(
            "Electronics", "Devices", [classes.Product("Phone", "Smartphone", 700, 5)]
        )
        category2 = classes.Category(
            "Furniture", "Home", [classes.Product("Chair", "Office chair", 150, 20)]
        )

        assert classes.Category.category_count == 2
        assert (
            classes.Category.product_count == 2
        )  # Поскольку в каждой категории один продукт
