from models.order import Order


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
