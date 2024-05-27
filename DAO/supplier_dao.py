from DAO.dao import DAO
from models.supplier import Supplier


class SupplierDAO(DAO):
    def __init__(self):
        super().__init__("suppliers.pkl")

    def add(self, supplier: Supplier):
        if (
            (supplier is not None)
            and isinstance(supplier, Supplier)
            and isinstance(supplier.cnpj, str)
        ):
            print("salvou...", supplier)
            super().add(supplier.cnpj, supplier)

    def update(self, supplier: Supplier):
        if (
            (supplier is not None)
            and isinstance(supplier, Supplier)
            and isinstance(supplier.cnpj, str)
        ):
            super().update(supplier.cnpj, supplier)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        print("removendo...", key)
        if isinstance(key, str):
            return super().remove(key)
