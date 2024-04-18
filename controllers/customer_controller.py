from models.customer import Customer
from dao.customer_dao import CustomerDAO

class CustomerController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.__customers = CustomerDAO()

    def create_new_customer(self, cpf, name, contact, gender, date_birth):
        new_customer = Customer(cpf, name, contact, gender, date_birth)
        self.__customers.add(new_customer)

    def update_customer(self, cpf, new_cpf, name, contact, gender, date_birth):
        customer = self.__customers.get(cpf)

        customer.name = name
        customer.contact = contact
        customer.gender = gender
        customer.date_birth = date_birth

        if cpf != new_cpf: # se alterar a key no dao: remove o antigo e adiciona com a key nova
            self.__customers.remove(cpf) 
            customer.cpf = new_cpf
            self.__customers.add(customer)
        else:
            self.__customers.update(customer)
    
    def get_customer(self, cpf):
        return self.__customers.get(cpf)

    def get_all_customers(self):
        return self.__customers.get_all()

    def remove_customer(self, cpf):
        customer = self.get_customer(cpf)
        if (isinstance(customer, Customer))==True:
            self.__customers.remove(cpf)

    def change_loyalty_card(self, customer):
        if customer.loyalty_card < 3:
            customer.loyalty_card += 1
        else: # Caso já possua três pedidos e esteja fazendo o pedido com desconto seu cartão volta a ficar zerado
            customer.loyalty_card = 0
        self.__customers.update(customer)
