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
    def get_clients_list(self):
        return [
            "José Eduardo Medeiros Jochem",
            "Victória Duarte Eleutério dos Santos",
            "Luana Ronau Mattos",
            "Fabiane Barreto Vavassori Benitti",
        ]

    # TODO adaptar depois quando tivermos o crud de produtos
    def get_products_list(self):
        return [
            "Bolo de Chocolate",
            "Cupcake de Baunilha",
            "Torta de Limão",
            "Cookies de Aveia",
            "Pão de Mel",
            "Brownie",
            "Bolo de Cenoura",
            "Cupcake de Chocolate",
            "Torta de Morango",
            "Cookies de Chocolate",
        ]

    # cria um novo pedido e adiciona ao DAO
    def create_new_order(self, client, products, delivery_date):
        new_id = self.generate_id()
        new_order = Order(
            order_id=new_id,
            client=client,
            products=products,
            delivery_date=delivery_date,
        )
        self.order_dao.add(new_order)
        self.load_orders()
        print(f"C - Pedido com ID {new_id} criado com sucesso!")

    #!TODO atualizar depois quando tiver o crud de produtos
    def check_order_requirements(self, order_items):
        # total_price = self.calculate_total(order_items)
        total_price = order_items
        if total_price > 150:
            return total_price, f"Pedido com valor de {total_price}. Sinal necessário!"
        return total_price, None
    
    def calculate_total(self, order_items):
        total_price = 0
        for item in order_items:
            total_price += item.price

        return total_price

    # remove um pedido do DAO com base no ID unico
    def remove_order(self, order_id):
        order_id = int(order_id)
        if self.order_dao.get(order_id):
            self.order_dao.remove(order_id)
            self.load_orders()
            print(f"C - Pedido com ID {order_id} removido com sucesso!")
            return
        print(f"C - Pedido com ID {order_id} não encontrado.")

    # atualiza um pedido no DAO e atualiza a lista de pedidos
    def update_order(self, order_id, client, products, delivery_date):
        order = next(
            (order for order in self.orders if order.order_id == order_id), None
        )
        if order:
            order.client = client
            order.products = products
            order.delivery_date = delivery_date
            self.order_dao.update(order)
            self.load_orders()
            print(f"C - Pedido {order_id} atualizado com sucesso!")
        else:
            print(f"C - Pedido com ID {order_id} não encontrado.")

    # retorna todas as informacoes de um pedido com base no ID
    def get_order_details(self, order_id):
        return self.order_dao.get(order_id)

    def get_all_orders(self):
        return self.order_dao.get_all()

    def refresh_orders_from_dao(self):
        self.orders = list(self.order_dao.get_all())
