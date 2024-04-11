from controllers.customer_controller import CustomerController
from controllers.order_controller import OrderController
from controllers.products_controller import ProductsController
from controllers.user_controller import UserController


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
