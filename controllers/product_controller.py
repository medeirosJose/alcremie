from models.product import Product
from views.product_view import ProductView
from DAO.product_dao import ProductDAO
import random
from datetime import datetime

class ProductController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.__product_dao = ProductDAO()

    # gera um ID unico para um novo pedido e checa se ja existe
    def generate_id(self):
        while True:
            new_id = random.randint(
                19000000,
                19999999,
            )
            if not self.__product_dao.get(new_id):
                return new_id

    def create_new_product(
        self,
        name: str,
        price: float,
        description: str,
        weight: float,
        recipe: str,
        ingredients,
    ):
        products = self.get_products()
        if products:
            new_id = self.generate_id()
        else:
            new_id = self.generate_id()
        new_product = Product(
            new_id,
            name,
            price,
            description,
            weight,
            recipe,
            ingredients,
        )
        self.__product_dao.add(new_product)
        print(self.get_products())
        print(f"Produto {new_id} criado com sucesso!")

    def remove_product(self, id: int):
        self.__product_dao.remove(id)

    def update_product(self, id, name, price, description, weight, recipe, ingredients):
        product = Product(
            id,
            name,
            price,
            description,
            weight,
            recipe,
            ingredients,
        )
        self.__product_dao.update(product)

    def get_products(self):
        products = []
        for product in self.__product_dao.get_all():
            products.append(product)
        return products

    def get_product_details(self, product_id):
        products = self.get_products()
        for product in products:
            if product.id == product_id:
                return product

    def get_products_sold_between_period(self, initial_date, end_date):
        orders = self.app_controller.order_controller.get_all_orders()
        period_orders = []
        initial_datetime = datetime.strptime(initial_date, "%d/%m/%Y")
        end_datetime = datetime.strptime(end_date, "%d/%m/%Y")
        # seleciona somente pedidos dentro do período
        for order in orders:
            order_datetime = datetime.strptime(order.delivery_date, "%d/%m/%Y")
            if initial_datetime <= order_datetime <= end_datetime:
                period_orders.append(order)
        ordered_products = []
        for order in period_orders:
            for order_product, quantity in order.products:
                for i in range(quantity):
                    ordered_products.append(order_product)
        return ordered_products

    def calculate_bigger_seller(self, initial_date, end_date):
        count_total = 0
        count = 0
        bigger_seller = ""
        bigger_seller_quantity = 0
        ordered_products = self.get_products_sold_between_period(initial_date, end_date)
        products = self.get_products()
        for product in products:
            for ordered_product in ordered_products:
                if ordered_product.id == product.id:
                    count += 1
            if count > count_total:
                bigger_seller = product
                bigger_seller_quantity = count
            count = 0
        return bigger_seller, bigger_seller_quantity

    def get_products_not_sold(self, initial_date, end_date):
        products = self.get_products()
        ordered_products = self.get_products_sold_between_period(initial_date, end_date)
        for product in products:
            if any(ordered_product.name == product.name for ordered_product in ordered_products):
                products.remove(product)
        return products

    def calculate_minor_seller(self, initial_date, end_date):
        x, count_total = self.calculate_bigger_seller(initial_date, end_date)
        count = 0
        minor_seller = ""
        minor_seller_quantity = 0
        ordered_products = self.get_products_sold_between_period(initial_date, end_date)
        products = self.get_products()
        for product in products:
            for ordered_product in ordered_products:
                if ordered_product.id == product.id:
                    count += 1
            if count < count_total and count != 0:
                minor_seller = product
                minor_seller_quantity = count
            count = 0
        return minor_seller, minor_seller_quantity

    def calculate_higher_price(self):
        higher_price_id = 0
        higher_price = 0
        for index, product in enumerate(self.__product_dao.get_all()):
            if index == 0:
                higher_price_id = product.id
                higher_price = product.price
            elif product.price > higher_price:
                higher_price_id = product.id
                higher_price = product.price
        higher_price_product = self.get_product_details(higher_price_id)
        return higher_price_product

    def calculate_lower_price(self):
        lower_price_id = 0
        lower_price = 0
        for index, product in enumerate(self.__product_dao.get_all()):
            if index == 0:
                lower_price_id = product.id
                lower_price = product.price
            elif product.price < lower_price:
                lower_price_id = product.id
                lower_price = product.price
        lower_price_product = self.get_product_details(lower_price_id)
        return lower_price_product

    def create_report(self, initial_date, end_date):
        bigger_seller, bigger_seller_quantity = self.calculate_bigger_seller(initial_date, end_date)
        if bigger_seller:
            lower_price = self.calculate_lower_price()
            higher_price = self.calculate_higher_price()
            minor_seller, minor_seller_quantity = self.calculate_minor_seller(initial_date, end_date)
            not_sold = self.get_products_not_sold(initial_date, end_date)
            return (lower_price, higher_price, bigger_seller, bigger_seller_quantity,
                    minor_seller, minor_seller_quantity, not_sold)
        else:
            return False

    def validate_date_interval(self, initial_date, end_date):
        initial_datetime = datetime.strptime(initial_date, "%d/%m/%Y")
        end_datetime = datetime.strptime(end_date, "%d/%m/%Y")
        if initial_datetime <= end_datetime:
            return True
        else:
            return False