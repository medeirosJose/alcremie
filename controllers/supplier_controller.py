from models.supplier import Supplier
from DAO.supplier_dao import SupplierDAO
from views.supplier_view import SupplierView


class SupplierController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.suppliers_dao = SupplierDAO()

    def create_new_supplier(self, cnpj, company, contact, ingredients):

        if self.get_supplier(cnpj):
            return "CNPJ já cadastrado no sistema!"

        new_supplier = Supplier(cnpj, company, contact, ingredients)
        # print("\n\n[!] Fornecedor criado com sucesso.")
        self.suppliers_dao.add(new_supplier)

    def validate_supplier_fields(self, cnpj, company, contact, ingredients):
        if not cnpj or not company or not contact or not ingredients:
            return "Todos os campos devem ser preenchidos!"
        if len(cnpj) != 18:  # CNPJ: 00.000.000/0000-00 (18 caracteres)
            return "CNPJ deve conter 14 dígitos!"
        return True

    def update_supplier(self, cnpj, new_cnpj, company, contact, ingredients):
        supplier = self.suppliers_dao.get(cnpj)
        supplier.company = company
        supplier.contact = contact
        supplier.ingredients = ingredients

        if cnpj != new_cnpj: 
            if self.get_supplier(new_cnpj):
                return "CNPJ já cadastrado no sistema!"
            else:
                self.suppliers_dao.remove(cnpj)
                supplier.cnpj = new_cnpj
                self.suppliers_dao.add(supplier)

        self.suppliers_dao.update(supplier)

    def get_supplier(self, cnpj):
        return self.suppliers_dao.get(cnpj)

    def get_all_suppliers(self):
        return self.suppliers_dao.get_all()

    def remove_supplier(self, cnpj):
        self.suppliers_dao.remove(cnpj)

    def get_supplier_details(self, cnpj):
        supplier = self.get_supplier(cnpj)
        return supplier
