from DAO.dao import DAO
from models.product import Product


class ProductDAO(DAO):
    def __init__(self):
        super().__init__("products.pkl")

    def add(self, product: Product):
        if (
            (product is not None)
            and isinstance(product, Product)
            and isinstance(product.id, int)
        ):
            super().add(product.id, product)

    def update(self, product: Product):
        if (
            (product is not None)
            and isinstance(product, Product)
            and isinstance(product.id, int)
        ):
            super().update(product.id, product)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
