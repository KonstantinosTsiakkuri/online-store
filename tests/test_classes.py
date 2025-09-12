import pytest

from src import classes


class TestProduct:
    def test_initialisation(self):
        product = classes.Product("Laptop", "Portable computer", 1500.0, 10)
        assert product.name == "Laptop"
        assert product.description == "Portable computer"
        assert product.price == 1500
        assert product.quantity == 10


class TestCategory:
    def setup_method(self):
        # Сбрасываем счётчики перед каждым тестом
        classes.Category.total_categories = 0
        classes.Category.total_products = 0

    def test_initialisation(self):
        category = classes.Category("Laptop", "Portable Computer", [])
        assert category.name == "Laptop"
        assert category.descriprion == "Portable Computer"
        assert category.products == []

    def test_total_categories_and_products(self):
        # Создание категорий с продуктами
        category1 = classes.Category(
            "Electronics", "Devices", [classes.Product("Phone", "Smartphone", 700, 5)]
        )
        category2 = classes.Category(
            "Furniture", "Home", [classes.Product("Chair", "Office chair", 150, 20)]
        )

        assert classes.Category.total_categories == 2
        assert (
            classes.Category.total_products == 2
        )  # Поскольку в каждой категории один продукт
