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

    def test_new_product_classmethod(self):
        """Тестируем создание объекта через класс-метод из словаря"""
        product_data = {
            "name": "Smartphone",
            "description": "Smart",
            "price": 10000.0,
            "quantity": 5
        }
        product = classes.Product.new_product(product_data)

        assert product.name == "Smartphone"
        assert product.description == "Smart"
        assert product.price == 10000.0
        assert product.quantity == 5

class TestCategory:
    def setup_method(self):
        # Сбрасываем счётчики перед каждым тестом
        classes.Category.category_count = 0
        classes.Category.product_count = 0

    def test_initialisation(self):
        category = classes.Category("Laptop", "Portable Computer", [])
        assert category.name == "Laptop"
        assert category.description == "Portable Computer"
        assert category.products == []

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

    def test_add_product(self):
        """Тестируем метод добавления продукта и увеличение счетчика"""
        category = classes.Category("Electronics", "Tech", [])
        product = classes.Product("Laptop", "MacBook", 150000.0, 3)

        initial_product_count = classes.Category.product_count
        category.add_product(product)

        # Проверяем, что товар добавился (длина списка стала 1)
        assert len(category.products) == 1
        # Проверяем, что счетчик всех продуктов увеличился
        assert classes.Category.product_count == initial_product_count + 1

    def test_products_getter_format(self):
        """Тестируем, что геттер возвращает правильную f-строку"""
        product = classes.Product("Laptop", "MacBook", 150000.0, 3)
        category = classes.Category("Electronics", "Tech", [product])

        expected_string = "Laptop, 150000.0 руб. Остаток: 3 шт.\n"

        # Берем первый элемент из списка строк, который вернул геттер
        assert category.products[0] == expected_string