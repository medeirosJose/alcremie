# RN 03 - Pedidos devem ter 1 dia de antecedencia       OK
# RN 05 - Não aceita pedidos para segundas e terças     OK
# RN 06 - Fidelidade - Após 3 pedidos com um valor mínimo de 75 reais,
# o cliente ganha um desconto de 15% no próximo pedido


class Order:
    def __init__(
        self,
        order_id,
        customer,
        products,
        delivery_date,
        observation,
        total_order_price,
    ):
        self.__order_id = order_id
        self.__customer = customer
        self.__products = products
        self.__delivery_date = delivery_date
        self.__payment_status = "Pendente"
        self.__payment_date = None
        self.__observation = observation
        self.__total_order_price = total_order_price

    @property
    def order_id(self):
        return self.__order_id

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value):
        self.__customer = value

    @property
    def products(self):
        return self.__products

    @products.setter
    def products(self, value):
        self.__products = value
        self.calculate_order_price()

    @property
    def delivery_date(self):
        return self.__delivery_date

    @delivery_date.setter
    def delivery_date(self, value):
        self.__delivery_date = value

    @property
    def payment_status(self):
        return self.__payment_status

    @payment_status.setter
    def payment_status(self, value):
        self.__payment_status = value

    @property
    def payment_date(self):
        return self.__payment_date

    @payment_date.setter
    def payment_date(self, value):
        self.__payment_date = value

    @property
    def observation(self):
        return self.__observation

    @observation.setter
    def observation(self, value):
        self.__observation = value

    @property
    def total_order_price(self):
        return self.__total_order_price

    @total_order_price.setter
    def total_order_price(self, value):
        self.__total_order_price = value

    def add_product(self, product):
        self.__products.append(product)
        self.calculate_order_price()

    def remove_product(self, product):
        self.__products.remove(product)
        self.calculate_order_price()

    def calculate_order_price(self):
        # self._total_order_price = sum(product.price for product in self.__products)
        print(
            # f"\n\n\nTotal do pedido {self._order_id}: R$ {self.__total_order_price}\n\n\n"
            "teste"
        )

    def __str__(self):
        # pedido, cliente, produtos e total
        return f"Pedido: {self.__order_id} - Cliente: {self.__customer} - Produtos: {self.__products} - Total: {self.__total_order_price}"
