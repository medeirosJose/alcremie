from controllers.customer_controller import CustomerController
from controllers.order_controller import OrderController
from controllers.product_controller import ProductController


class AppController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
            # Inicialização dos controladores específicos
            cls.order_controller = OrderController(cls)
            cls.products_controller = ProductController(cls)
            cls.customer_controller = CustomerController(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        if AppController._instance is None:
            AppController()
        return AppController._instance

    def get_order_controller(self):
        return self.order_controller

    def get_products_controller(self):
        return self.products_controller

    def get_customer_controller(self):
        return self.customer_controller
