import tkinter as tk
from PIL import Image, ImageTk
from views.order_view import OrderView
from views.product_view import ProductView
from views.customer_view import CustomersView
from views.pending_orders_view import PendingOrdersView
from views.supplier_view import SupplierView
from views.price_simulator_view import PriceSimulatorPopup

from views.menu_view import MenuView
from views.product_report_view import NewReportPopup

from controllers.app_controller import AppController


class Main(tk.Tk):
    def __init__(self, app_controller):
        super().__init__()
        self.title("Confeitaria Alcremie")
        self.state("zoomed")

        self.sidebar = tk.Frame(self, width=100, bg="gray")
        self.sidebar.pack(
            fill="y",
            side="left",
        )

        self.load_and_display_logo()
        self.load_icons()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.app_controller = app_controller

        #! Aqui tem q adicionar as demais views e seus controllers atraves do self.app_controller
        self.views = {
            "Pedidos": (
                OrderView,
                self.app_controller.get_order_controller(),
                self.icons["order"],
            ),
            "Produtos": (
                ProductView,
                self.app_controller.get_product_controller(),
                self.icons["products"],
            ),
            "Clientes": (
                CustomersView,
                self.app_controller.get_customer_controller(),
                self.icons["customers"],
            ),
            "Fornecedores": (
                SupplierView,
                self.app_controller.get_supplier_controller(),
                self.icons["customers"],
            ),
            "Cardapio": (
                MenuView,
                self.app_controller.get_menu_controller(),
                self.icons["menu"],
            ),
            "Relatório Produtos": (
                NewReportPopup,
                self.app_controller.get_product_controller(),
                self.icons["product_report"],
            ),
            "Relatório Lucros": (
                NewReportPopup,
                self.app_controller.get_product_controller(),
                self.icons["profit_report"],
            ),
            "Pagamentos": (
                PendingOrdersView,
                self.app_controller.get_pending_orders_controller(),
                self.icons["money"],
            ),
            "Simulador de Preço": (
                PriceSimulatorPopup,
                self.app_controller.get_product_controller(),
                self.icons["money"],
            ),
            "Sair": (
                OrderView,
                self.app_controller.get_order_controller(),
                self.icons["order"],
            ),
        }

        self.current_view = None
        self.buttons = {}
        self.create_sidebar_buttons()

    def load_icons(self):
        self.icons = {
            "order": ImageTk.PhotoImage(
                Image.open("icons/order2.png").resize((24, 24))
            ),
            "products": ImageTk.PhotoImage(
                Image.open("icons/product2.png").resize((24, 24))
            ),
            "customers": ImageTk.PhotoImage(
                Image.open("icons/customer2.png").resize((24, 24))
            ),
            "menu": ImageTk.PhotoImage(
                Image.open("icons/menu(4).png").resize((24, 24))
            ),
            "product_report": ImageTk.PhotoImage(
                Image.open("icons/reports2.png").resize((24, 24))
            ),
            "profit_report": ImageTk.PhotoImage(
                Image.open("icons/reports2.png").resize((24, 24))
            ),
            "money": ImageTk.PhotoImage(
                Image.open("icons/payment.png").resize((24, 24))
            ),
        }

    def load_and_display_logo(self):
        logo_image = ImageTk.PhotoImage(Image.open("icons/logo.png").resize((150, 150)))
        logo_label = tk.Label(self.sidebar, image=logo_image, bg="gray")
        logo_label.image = logo_image
        logo_label.pack(pady=10)
        tk.Frame(self.sidebar, height=1, bg="WHITE").pack(fill="x", padx=10, pady=10)

    def create_sidebar_buttons(self):
        for view_name, (view_class, controller, icon) in self.views.items():
            button = tk.Button(
                self.sidebar,
                image=icon,
                text=view_name,
                font=("Roboto", 10),
                compound="left",
                command=lambda name=view_name: self.show_view(name),
                relief="flat",
                anchor="w",
                width=150,
                height=30,
                padx=20,
            )
            button.pack(pady=10, padx=10, fill="x")
            self.buttons[view_name] = button

    def show_view(self, view_name):
        if self.current_view:
            self.current_view[0].destroy()

        view_class, controller, _ = self.views[view_name]
        view = view_class(self.container, controller)

        view.pack(fill="both", expand=True)
        self.current_view = (view, controller)

        for btn in self.buttons.values():
            btn.config(bg="white")
        self.buttons[view_name].config(bg="#faebd8")


if __name__ == "__main__":
    app_controller = AppController.get_instance()
    app = Main(app_controller)
    app.mainloop()
