from models.supply import Supply
from DAO.supply_dao import SupplyDAO
import random


# class Supply:
#     def __init__(self, id, name, price):
#         self.__id = id
#         self.__name = name
#         self.__price = price


class SupplyController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.supplies_dao = SupplyDAO()
        self.supplies = []
        self.load_supplies()

    def load_supplies(self):
        self.supplies = list(self.supplies_dao.get_all())

    def generate_id(self):
        while True:
            new_id = random.randint(
                42000000,
                42999999,  # defini que todos os pedidos começam com id 42 só pq sim kkkk
            )
            if not self.supply_dao.get(new_id):
                return new_id

    def create_new_supply(self, id, name, price):
        new_id = self.generate_id()

        new_supply = Supply(id=new_id, name=name, price=price)

        self.supplies_dao.add(new_supply)
        self.load_supplies()

    def remove_supply(self, id):
        self.supplies_dao.remove(id)
        self.load_supplies()
