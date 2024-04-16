class Order:
    def __init__(self, order_id, client, products, delivery_date):
        self.order_id = order_id
        self.client = client
        self.products = products
        self.delivery_date = delivery_date
        self.payment_status = "Pendente"
        self.observation = ""
        self.total_order_price = self.calculate_order_price()

    def add_product(self, product):
        self.products.append(product)
        self.calculate_order_price()

    def remove_product(self, product):
        self.products.remove(product)
        self.calculate_order_price()

    def calculate_order_price(self):
        # self.total_order_price = sum(product.price for product in self.products)
        print(f"\n\n\nTotal do pedido {self.order_id}: \n\n\n")

    def __str__(self):
        product_details = ", ".join(str(product) for product in self.products)
        return f"Pedido {self.order_id} - Cliente: {self.client}, Produtos: {product_details}, Data de Entrega: {self.delivery_date}, Total: R$ {self.total_order_price}"
