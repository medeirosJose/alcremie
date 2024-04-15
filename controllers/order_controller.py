from models.order import Order
import random


class OrderController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.orders = []
        self.next_order_id = 1

    def generate_id(self):
        while True:
            new_id = random.randint(
                42000000,
                42999999,  # defini que todos os pedidos começam com id 42 só pq sim kkkk
            )
            if all(new_id != order.order_id for order in self.orders):
                return new_id

    # adaptar depois quando tivermos o crud de clientes
    def get_clients_list(self):
        return [
            "José Eduardo Medeiros Jochem",
            "Victória Duarte Eleutério dos Santos",
            "Luana Ronau Mattos",
            "Fabiane Barreto Vavassori Benitti",
        ]

    # adaptar depois quando tivermos o crud de produtos
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

    def create_new_order(self, client, products, delivery_date):
        new_id = self.generate_id()
        new_order = Order(
            order_id=new_id,
            client=client,
            products=products,
            delivery_date=delivery_date,
        )
        self.orders.append(new_order)
        print(f"Pedido {new_id} criado com sucesso!")

    def remove_order(self, order_id):
        order_id = int(order_id)
        for index, order in enumerate(self.orders):
            if order.order_id == order_id:
                del self.orders[index]
                print(f"Pedido {order_id} removido com sucesso!")
                return
        print(f"Pedido com ID {order_id} não encontrado.")

    def update_order(self, order_id, client, products, delivery_date):
        order = next(
            (order for order in self.orders if order.order_id == order_id), None
        )
        if order:
            order.client = client
            order.products = products
            order.delivery_date = delivery_date
            print(f"Pedido {order_id} atualizado com sucesso!")

    def get_all_orders(self):
        return self.orders

    def get_order_details(self, order_id):
        return next(
            (order for order in self.orders if str(order.order_id) == str(order_id)),
            None,
        )
