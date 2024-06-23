from datetime import datetime

from models.order import Order
import random
from DAO.order_dao import OrderDAO


class OrderController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.orders = []
        self.order_dao = OrderDAO()
        self.load_orders()

    # carrega os pedidos do DAO para a execucao atual
    def load_orders(self):
        self.orders = list(self.order_dao.get_all())

    # gera um ID unico para um novo pedido e checa se ja existe
    def generate_id(self):
        while True:
            new_id = random.randint(
                42000000,
                42999999,  # defini que todos os pedidos começam com id 42 só pq sim kkkk
            )
            if not self.order_dao.get(new_id):
                return new_id

    # TODO adaptar depois quando tivermos o crud de clientes
    def get_customers_list(self):
        customers = self.app_controller.get_customer_controller().get_all_customers()
        # print(customers)
        return customers

    # TODO adaptar depois quando tivermos o crud de produtos
    def get_products_list(self):
        products = self.app_controller.get_product_controller().get_products()
        # print(products)
        return products

    # cria um novo pedido e adiciona ao DAO
    def create_new_order(
        self, customer, products_with_quantities, delivery_date, observation
    ):
        new_id = self.generate_id()
        # print("pRODUTOS COM QUANTIDADES", products_with_quantities)
        order_price, descountApplied = self.calculate_total(
            products_with_quantities, customer
        )

        new_order = Order(
            order_id=new_id,
            customer=customer,
            products=products_with_quantities,
            delivery_date=delivery_date,
            observation=observation,
            total_order_price=order_price,
        )

        if new_order.total_order_price > 150:
            new_order.total_order_price, new_order.observation = (
                self.check_order_requirements(new_order.total_order_price, observation)
            )

        self.order_dao.add(new_order)
        self.load_orders()
        # print(f"Pedido com ID {new_id} criado com sucesso!")
        # print(new_order.customer.name)

        return descountApplied  # mensagem na tela avisando que o desconto do cartão fidelidade foi aplicado no valor do pedido

    #!TODO atualizar depois quando tiver o crud de produtos
    def check_order_requirements(self, total_price, observation=None):
        # print(f"Total price no check_order_requirements: {total_price}")
        if total_price > 150 and observation:
            return (
                total_price,
                f"Pedido com valor de R${total_price}. Sinal necessário! {observation}",
            )
        elif total_price > 150:
            return (
                total_price,
                f"Pedido com valor de R${total_price}. Sinal necessário!",
            )
        return total_price, None

    def calculate_total(self, products_with_quantities, customer):
        total_price = 0
        for product, quantity in products_with_quantities:
            total_price += product.price * quantity

        # testa se ele completou seu cartão de fidelidade e pode receber desconto (RN06)
        descountApplied = None
        if customer.loyalty_card == 3:
            total_price *= 85/100
            descountApplied = "Desconto do cartão fidelidade aplicado"
        print(f"Total price: {total_price}")
        return total_price, descountApplied

    # remove um pedido do DAO com base no ID unico
    def remove_order(self, order_id):
        order_id = int(order_id)
        if self.order_dao.get(order_id):
            self.order_dao.remove(order_id)
            self.load_orders()
            # print(f"C - Pedido com ID {order_id} removido com sucesso!")
            return
        # print(f"C - Pedido com ID {order_id} não encontrado.")

    # atualiza um pedido no DAO e atualiza a lista de pedidos
    def update_order(self, order_id, customer, products, delivery_date, observation):
        # # print(f"Pedido ID: {type(order_id)}")
        self.load_orders()
        order = next(
            (order for order in self.orders if order.order_id == int(order_id)), None
        )
        if order:
            order.customer = customer
            order.products = products
            order.delivery_date = delivery_date
            order.observation = observation
            order.total_order_price, x = self.calculate_total(products, customer)

            if order.total_order_price > 150:
                order.total_order_price, order.observation = (
                    self.check_order_requirements(
                        order.total_order_price, order.observation
                    )
                )
            self.order_dao.update(order)
            self.load_orders()
            # print(f"Pedido com ID {order_id} atualizado com sucesso!")
            return
        # print(f"Pedido com ID {order_id} não encontrado.")

    # retorna todas as informacoes de um pedido com base no ID
    def get_order_details(self, order_id):
        # # print(f"Pedido ID: {type(order_id), order_id}")
        return self.order_dao.get(order_id)

    def get_all_orders(self):
        return self.order_dao.get_all()

    def refresh_orders_from_dao(self):
        self.orders = list(self.order_dao.get_all())

    def validate_date_interval(self, initial_date, end_date):
        initial_datetime = datetime.strptime(initial_date, "%d/%m/%Y")
        end_datetime = datetime.strptime(end_date, "%d/%m/%Y")
        if end_datetime >= initial_datetime:
            return True
        else:
            return False

    def get_products_sold_between_period(self, initial_date, end_date):
        period_orders = self.get_orders_in_period(initial_date, end_date)
        ordered_products = []
        for order in period_orders:
            ordered_products.append(order.products)
        return ordered_products

    def get_products_not_sold_between_period(self, initial_date, end_date):
        period_orders = self.get_orders_in_period(initial_date, end_date)
        ordered_products = []
        for order in period_orders:
            for order_product, quantity in order.products:
                ordered_products.append(order_product)
        products = self.app_controller.product_controller.get_products()
        for product in products:
            if any(ordered_product.name == product.name for ordered_product in ordered_products):
                products.remove(product)
        return products

    def get_orders_in_period(self, initial_date, end_date):
        orders = self.get_all_orders()
        period_orders = []
        initial_datetime = datetime.strptime(initial_date, "%d/%m/%Y")
        end_datetime = datetime.strptime(end_date, "%d/%m/%Y")
        # seleciona somente pedidos dentro do período
        for order in orders:
            order_datetime = datetime.strptime(order.delivery_date, "%d/%m/%Y")
            if initial_datetime <= order_datetime <= end_datetime:
                period_orders.append(order)
        return period_orders

    def calculate_period_profit(self, initial_date, end_date):
        period_orders = self.get_orders_in_period(initial_date, end_date)
        profit = 0
        for order in period_orders:
            for order_product, quantity in order.products:
                for i in range(quantity):
                    profit += order_product.price
        return profit

    def create_report(self, initial_date, end_date):
        if self.get_orders_in_period(initial_date, end_date):
            products_sold_between_period = self.get_products_sold_between_period(initial_date, end_date)
            products_not_sold_between_period = self.get_products_not_sold_between_period(initial_date, end_date)
            profit = self.calculate_period_profit(initial_date, end_date)
            return products_sold_between_period, products_not_sold_between_period, profit
        else:
            return False
