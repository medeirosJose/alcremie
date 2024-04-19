from models.product import Product
from views.product_view import ProductView
from DAO.product_dao import ProductDAO


class ProductController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.__product_dao = ProductDAO()

    def create_new_product(self, name: str, price: float, description: str, weight: float, ingredients, recipe: str,):
        products = self.get_products()
        if products:
            new_id = int(max(product.id for product in products) + 1)
        else:
            new_id = int(1)
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

    def find_product_by_id(self):
        return

    def get_product_details(self, product_id):
        products = self.get_products()
        for product in products:
            if product.id == product_id:
                return product