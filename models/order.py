class Order:
    def __init__(self, order_id, client, products, delivery_date):
        self.order_id = order_id
        self.client = client
        self.products = products
        self.delivery_date = delivery_date
        self.payment_status = "Pendente"
        self.observation = ""
        self.total_order_price = 0

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)


    # def get_total(self):
    #    return sum(product.price for product in self.products)

    def __str__(self):
        return f"Pedido {self.order_id} - Cliente: {self.client}"
