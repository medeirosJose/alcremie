from models.customer import Customer
from dao.customer_dao import CustomerDAO

class CustomerController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.__customers = CustomerDAO()

    def create_new_customer(self, cpf, name, contact):
        new_customer = Customer(cpf, name, contact)
        self.__customers.add(new_customer)

    def update_customer(self, cpf, new_cpf, name, contact):
        customer = self.__customers.get(cpf)
        if cpf != new_cpf: # se alterar a key no dao: remove o antigo e adiciona com a key nova
            self.__customers.remove(cpf) 
            customer.cpf = new_cpf
            customer.name = name
            customer.contact = contact
            self.__customers.add(customer)
        else:
            customer.name = name
            customer.contact = contact
            self.__customers.update(customer)
    
    def get_customer(self, cpf):
        return self.__customers.get(cpf)

    def get_all_customers(self):
        return self.__customers.get_all()

    def remove_customer(self, cpf):
        customer = self.get_customer(cpf)
        if (isinstance(customer, Customer))==True:
            self.__customers.remove(cpf)
