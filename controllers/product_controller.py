from models.product import Product
from views.product_view import ProductView


class ProductController:
    def __init__(self, system_controller):
        self.__products = []
        self.__product_screen = ProductView()
        self.__system_controller = system_controller

    def add_product(self):
        return

    def del_product(self):
       return

    def update_product(self):
        return

    def list_products(self):
        return

    def find_product_by_id(self):
        return

    def return_to_controller(self):
        self.__system_controller.open_view()

    def open_screen(self):
        return