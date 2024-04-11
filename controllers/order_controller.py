from models.order import Order


class OrderController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.orders = []
        self.next_order_id = 1

    def get_clients_list(self):
        return [
            "José Eduardo Medeiros Jochem",
            "Victória Duarte Eleutério dos Santos",
            "Luana Ronau Mattos",
            "Fabiane Barreto Vavassori Benitti",
        ]

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
        if self.orders:
            new_id = int(max(order.order_id for order in self.orders) + 1)
        else:
            new_id = int(1)
        new_order = Order(
            order_id=new_id,
            client=client,
            products=products,
            delivery_date=delivery_date,
        )
        self.orders.append(new_order)
        print(f"Pedido {new_id} criado com sucesso!")

    def remove_order(self, order_id):
        print("Estou dentro do remove_order do order_controller")
        print(f"order_id: {order_id}")
        print(f"orders: {self.orders}")
        order_id = int(order_id)
        for order in self.orders:
            print("Percorrendo o orders")
            if order.order_id == order_id:
                self.orders.remove(order)
                print(f"Pedido {order_id} removido com sucesso!")
                break

    def update_order(self, order_id, client, products, delivery_date):
        for order in self.orders:
            if order.order_id == order_id:
                order.client = client
                order.products = products
                order.delivery_date = delivery_date
                break

    def get_all_orders(self):
        # Retorna todos os pedidos existentes
        return self.orders

    def get_order_details(self, order_id):
        for order in self.orders:
            if str(order.order_id) == str(order_id):
                return order
        return None
