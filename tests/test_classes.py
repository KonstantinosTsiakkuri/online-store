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

        # Считываем и выбрасываем лог от миксина, очищая буфер консоли
        capsys.readouterr()

        # Теперь срабатывает только принты от сеттера цены
        product.price = -1000
        captured = capsys.readouterr()

        # Теперь тут только одна нужная нам строка
        assert captured.out == "Цена не должна быть нулевая или отрицательная\n"
        assert product.price == 1500  # цена не должна измениться

    def test_new_product_classmethod(self):
        """Тестируем создание объекта через класс-метод из словаря"""
        product_data = {
            "name": "Smartphone",
            "description": "Smart",
            "price": 10000.0,
            "quantity": 5,
        }
        product = classes.Product.new_product(product_data)

        assert product.name == "Smartphone"
        assert product.description == "Smart"
        assert product.price == 10000.0
        assert product.quantity == 5

    def test_product_str(self):
        """Тестируем магический метод __str__ для продукта"""
        product = classes.Product("Smartphone", "Smart", 10000.0, 5)
        expected_str = "Smartphone, 10000.0 руб. Остаток: 5 шт."
        assert str(product) == expected_str

    def test_product_add(self):
        """Тестируем магический метод __add__ (сложение продуктов)"""
        product1 = classes.Product(
            "Laptop", "Mac", 100000.0, 2
        )  # Общая стоимость: 200 000
        product2 = classes.Product(
            "Phone", "iPhone", 50000.0, 3
        )  # Общая стоимость: 150 000
        # 200000 + 150000 = 350000
        assert product1 + product2 == 350000.0

    def test_add_different_types_error(self):
        """Тестируем ошибку при сложении разных классов"""
        phone = classes.Smartphone(
            "iPhone", "Apple", 100000.0, 10, "High", "Pro", 256, "Black"
        )
        grass = classes.LawnGrass(
            "Газон", "Густой", 1000.0, 20, "Россия", "14 дней", "Зеленый"
        )

        # Вот как работает pytest.raises: мы говорим, что следующий блок кода ДОЛЖЕН вызвать TypeError
        with pytest.raises(TypeError):
            # Если сложение разных типов вызовет TypeError, тест будет считаться УСПЕШНЫМ (зеленым)
            phone + grass


class TestCategory:
    def setup_method(self):
        # Сбрасываем счётчики перед каждым тестом
        classes.Category.category_count = 0
        classes.Category.product_count = 0

    def test_initialisation(self):
        category = classes.Category("Laptop", "Portable Computer", [])
        assert category.name == "Laptop"
        assert category.description == "Portable Computer"
        # Геттер теперь возвращает пустую строку, если товаров нет
        assert category.products == ""

    def test_total_categories_and_products(self):

        # Создание категорий с продуктами только ради увеличения счетчиков класса
        classes.Category(
            "Electronics", "Devices", [classes.Product("Phone", "Smartphone", 700, 5)]
        )
        classes.Category(
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

        # Проверяем, что название товара появилось в итоговой строке
        assert "Laptop" in category.products
        # Проверяем, что счетчик всех продуктов увеличился
        assert classes.Category.product_count == initial_product_count + 1

    def test_products_getter_format(self):
        """Тестируем, что геттер возвращает правильную f-строку"""
        product = classes.Product("Laptop", "MacBook", 150000.0, 3)
        category = classes.Category("Electronics", "Tech", [product])

        expected_string = "Laptop, 150000.0 руб. Остаток: 3 шт.\n"

        # Теперь геттер возвращает саму строку целиком, индексы [0] больше не нужны
        assert category.products == expected_string

    def test_category_str(self):
        """Тестируем магический метод __str__ для категории"""
        product1 = classes.Product("Laptop", "Mac", 100000.0, 2)
        product2 = classes.Product("Phone", "iPhone", 50000.0, 3)
        category = classes.Category("Electronics", "Tech", [product1, product2])
        expected_str = "Electronics, количество продуктов: 5 шт."
        assert str(category) == expected_str


class TestCategoryIter:
    def test_category_iteration(self):
        """Тестируем ручной проход по итератору"""
        product1 = classes.Product("Laptop", "Mac", 100000.0, 2)
        product2 = classes.Product("Phone", "iPhone", 50000.0, 3)
        category = classes.Category("Electronics", "Tech", [product1, product2])

        # Создаем экземпляр нашего итератора
        iterator = classes.CategoryIter(category)

        products_list = list(iterator)

        assert len(products_list) == 2
        assert products_list[0].name == "Laptop"
        assert products_list[1].name == "Phone"


class TestInheritance:
    def test_smartphone_initialization(self):
        """Тестируем создание смартфона и его уникальные атрибуты"""
        phone = classes.Smartphone(
            "iPhone 15", "Apple", 100000.0, 10, "High", "Pro", 256, "Black"
        )
        assert phone.name == "iPhone 15"
        assert phone.efficiency == "High"
        assert phone.model == "Pro"
        assert phone.memory == 256

    def test_lawngrass_initialization(self):
        """Тестируем создание газонной травы"""
        grass = classes.LawnGrass(
            "Газон", "Густой", 1000.0, 20, "Россия", "14 дней", "Зеленый"
        )
        assert grass.name == "Газон"
        assert grass.country == "Россия"
        assert grass.germination_period == "14 дней"

    def test_add_product_type_error(self):
        """Тестируем ошибку при добавлении в категорию не продукта"""
        category = classes.Category("Electronics", "Tech", [])

        # Ожидаем ошибку TypeError
        with pytest.raises(TypeError):
            # Пытаемся добавить обычное число 5 (или строку "Привет") вместо объекта продукта
            category.add_product(5)


class TestAdvancedArchitecture:
    def test_base_product_instantiation(self):
        """Тестируем, что абстрактный класс BaseProduct нельзя инстанцировать напрямую"""
        # Ожидаем ошибку TypeError при попытке создать абстрактный продукт
        with pytest.raises(TypeError):
            classes.BaseProduct()

    def test_mixin_log_output(self, capsys):
        """Тестируем работу миксина (вывод в консоль при создании объекта)"""
        # Создаем продукт. В этот момент миксин должен сработать и напечатать текст
        classes.Product("Laptop", "MacBook", 150000.0, 3)

        # Перехватываем то, что попало в консоль
        captured = capsys.readouterr()

        # Проверяем, что вывод содержит ожидаемую строку от метода __repr__
        assert "Product(Laptop, MacBook, 150000.0, 3)" in captured.out

    def test_mixin_log_output_smartphone(self, capsys):
        """Тестируем работу миксина для наследников (Смартфон)"""
        classes.Smartphone("iPhone", "Apple", 100000.0, 10, "High", "Pro", 256, "Black")
        captured = capsys.readouterr()

        # Миксин должен динамически определить, что это Smartphone
        assert "Smartphone(iPhone, Apple, 100000.0, 10)" in captured.out


class TestOrder:
    def test_order_initialization(self):
        """Тестируем создание заказа и автоматический расчет итоговой стоимости"""
        phone = classes.Smartphone(
            "iPhone 15", "Apple", 100000.0, 10, "High", "Pro", 256, "Black"
        )
        order = classes.Order(phone, 2)

        # Проверяем, что атрибуты сохранились верно
        assert order.product == phone
        assert order.quantity == 2
        # 100 000 * 2 = 200 000
        assert order.total_cost == 200000.0

    def test_order_add_product(self):
        """Тестируем замену товара в заказе и перерасчет стоимости"""
        phone = classes.Smartphone(
            "iPhone 15", "Apple", 100000.0, 10, "High", "Pro", 256, "Black"
        )
        grass = classes.LawnGrass(
            "Газон", "Густой", 1000.0, 20, "Россия", "14 дней", "Зеленый"
        )

        # Создаем заказ с телефоном
        order = classes.Order(phone, 2)
        assert order.total_cost == 200000.0

        # Меняем телефон на газонную траву
        order.add_product(grass)

        # Проверяем, что товар заменился
        assert order.product == grass
        # Проверяем, что стоимость пересчиталась: 1000 * 2 = 2000
        assert order.total_cost == 2000.0

    def test_order_str(self):
        """Тестируем строковое отображение заказа"""
        phone = classes.Smartphone(
            "iPhone 15", "Apple", 100000.0, 10, "High", "Pro", 256, "Black"
        )
        order = classes.Order(phone, 2)

        expected_str = "Заказ: iPhone 15, количество: 2, итог: 200000.0 руб."
        assert str(order) == expected_str
