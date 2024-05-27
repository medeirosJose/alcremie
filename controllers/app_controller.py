from controllers.customer_controller import CustomerController
from controllers.order_controller import OrderController
from controllers.product_controller import ProductController
from controllers.product_controller import ProductController
from controllers.supplier_controller import SupplierController


class AppController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
            cls._instance.order_controller = OrderController(cls._instance)
            cls._instance.product_controller = ProductController(cls._instance)
            cls._instance.customer_controller = CustomerController(cls._instance)
            cls._instance.supplier_controller = SupplierController(cls._instance)
        return cls._instance

    @staticmethod
    def get_instance():
        if AppController._instance is None:
            AppController()
        return AppController._instance

    def get_order_controller(self):
        return self.order_controller

    def get_product_controller(self):
        return self.product_controller

    def get_customer_controller(self):
        return self.customer_controller

    def get_supplier_controller(self):
        return self.supplier_controller
