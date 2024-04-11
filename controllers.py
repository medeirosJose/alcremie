from model import User, Order


class AppController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
            # Inicialização dos controladores específicos
            cls.user_controller = UserController(cls)
            cls.order_controller = OrderController(cls)
            cls.products_controller = ProductsController(cls)
            cls.customer_controller = CustomerController(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        if AppController._instance is None:
            AppController()
        return AppController._instance

    # Métodos para acessar os controladores específicos
    def get_user_controller(self):
        return self.user_controller

    def get_order_controller(self):
        return self.order_controller

    def get_products_controller(self):
        return self.products_controller

    def get_customer_controller(self):
        return self.customer_controller


class UserController:
    def __init__(self, app_controller):
        self.__app_controller = app_controller
        self.users = []

    def get_all_users(self):
        return self.users

    def add_user(self, name, email):
        user = User(name, email)
        self.users.append(user)

    def update_user(self, index, new_name, new_email):
        if index < len(self.users):
            self.users[index].name = new_name
            self.users[index].email = new_email

    def delete_user(self, index):
        if index < len(self.users):
            del self.users[index]


class OrderController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.orders = []  # Armazena os pedidos
        self.next_order_id = 1  # Simples contador para gerar IDs de pedidos

    def get_clients_list(self):
        # Retorna uma lista de nomes de clientes fictícios
        return ["Cliente A", "Cliente B", "Cliente C"]

    def get_products_list(self):
        # Retorna uma lista de produtos fictícios
        return [
            "Bolo de Chocolate",
            "Cupcake de Baunilha",
            "Torta de Limão",
            "Cookies de Aveia",
        ]

    def create_new_order(self, client, products, delivery_date):
        order_id = len(self.orders) + 1
        new_order = Order(
            order_id=order_id,
            client=client,
            products=products,
            delivery_date=delivery_date,
        )
        self.orders.append(new_order)

    def get_all_orders(self):
        # Retorna todos os pedidos existentes
        return self.orders

    def get_order_details(self, order_id):
        for order in self.orders:
            if str(order.order_id) == str(order_id):
                return order
        return None

    # Adicione outros métodos conforme necessário, como criar novos pedidos, atualizar o status de pagamento, etc


class ProductsController:
    def __init__(self, app_controller):
        self.__app_controller = app_controller

    # Adicione métodos de controle de configurações, se necessário


class CustomerController:
    def __init__(self, app_controller):
        self.app_controller = app_controller

    # Adicione métodos de controle de informações sobre a aplicação, se necessário
