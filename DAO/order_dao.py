from DAO.dao import DAO
from models.order import Order


class OrderDAO(DAO):
    def __init__(self):
        super().__init__("orders.pkl")

    def add(self, order: Order):
        if (
            (order is not None)
            and isinstance(order, Order)
            and isinstance(order.order_id, int)
        ):
            super().add(order.order_id, order)

    def update(self, order: Order):
        if (
            (order is not None)
            and isinstance(order, Order)
            and isinstance(order.order_id, int)
        ):
            super().update(order.order_id, order)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
