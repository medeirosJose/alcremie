from DAO.dict_dao import DictDAO
from models.customer import Customer


class CustomerDAO(DictDAO):
    def __init__(self):
        super().__init__("customers.pkl")

    def add(self, customer: Customer):
        if (customer is not None) and isinstance(customer, Customer):
            super().add(customer.cpf, customer)

    def update(self, customer: Customer):
        if (customer is not None) and isinstance(customer, Customer):
            super().update(customer.cpf, customer)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
