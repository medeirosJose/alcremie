from DAO.order_dao import OrderDAO
from datetime import datetime, timedelta


class PendingOrdersController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.pending_orders = []
        self.order_in_loyalty_card = []
        self.order_dao = OrderDAO()
        self.load_pending_orders()

    # carrega os pedidos do DAO e filtra os que estão pendentes
    def load_pending_orders(self):
        # limpa os anteriores para não armazenar repetidos
        self.pending_orders = []
        all_orders = list(self.order_dao.get_all())

        for order in all_orders:
            # Converte string para um objeto de data
            delivery_date = datetime.strptime(order.delivery_date, "%d/%m/%Y").date()
            
            # Altera automaticamente o estado dos pedidos que já passaram da data de entrega para pagos
            if delivery_date < datetime.now().date() and order.payment_status == 'Pendente':
                order.payment_status = "Pago"
                self.order_dao.update(order)

            # para atender a RN06 - Após 3 pedidos com um valor mínimo de 75 reais realizados por um
            # mesmo cliente, no próxmo pedido é aplicado um desconto
            # é feito aqui para garantir que pedidos cancelados não são válidos
            if delivery_date < datetime.now().date() and order.payment_status == 'Pago' and order.total_order_price >= 75:
            # use a linha seguinte para testes e demonstrações:
            # elif delivery_date <= datetime.now().date() and order.payment_status == 'Pago' or delivery_date==datetime.now().date()+ timedelta(days=1):
                # Salva os pedidos já contabilizados para que ao atualizar a lista de pedidos não 
                # seja adicionado várias vezes o mesmo
                if order.order_id not in self.order_in_loyalty_card:
                    self.order_in_loyalty_card.append(order.order_id)
                    self.app_controller.customer_controller.change_loyalty_card(order.customer)
                    print(order.customer.loyalty_card)

            # Adiciona apenas aqueles que ainda faltam ser entregues e não foram cancelados
            elif delivery_date >= datetime.now().date() and order.payment_status != "Cancelado": 
                self.pending_orders.append(order)

    # atualiza um pedido no DAO e atualiza a lista de pedidos
    def update_order(self, order_id, payment_status, payment_date=None):
        # print(f"Pedido ID: {type(order_id)}")
        order = next(
            (order for order in self.pending_orders if order.order_id == int(order_id)), None
        )
        if order:
            order.payment_status = payment_status
            order.payment_date = payment_date

            self.order_dao.update(order)
            self.load_pending_orders()

    # retorna todas as informacoes de um pedido com base no ID
    def get_order_details(self, id_searched):
        for order in self.pending_orders:
            if order.order_id == id_searched:
                return order

    def get_all_orders(self):
        # garante que está atualizado
        self.load_pending_orders() 
        return self.pending_orders
