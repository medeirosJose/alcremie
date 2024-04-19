import tkinter as tk
from PIL import Image, ImageTk
from views.order_view import OrderView
from views.product_view import ProductView
from views.customer_view import CustomersView
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
                ProductsView,
                self.app_controller.get_products_controller(),
                self.icons["products"],
            ),
            "Clientes": (
                CustomersView,
                self.app_controller.get_customer_controller(),
                self.icons["customers"],
            ),
            # placeholder
            "Relatórios": (
                OrderView,
                self.app_controller.get_order_controller(),
                self.icons["reports"],
            ),
            "Pagamentos": (
                OrderView,
                self.app_controller.get_order_controller(),
                self.icons["settings"],
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
            "reports": ImageTk.PhotoImage(
                Image.open("icons/reports2.png").resize((24, 24))
            ),
            "settings": ImageTk.PhotoImage(
                Image.open("icons/payment.png").resize((24, 24))
            ),
        }

    # serve para carregar a logo da aplicacao acima dos botoes da sidebar
    def load_and_display_logo(self):
        logo_image = ImageTk.PhotoImage(Image.open("icons/logo.png").resize((150, 150)))
        logo_label = tk.Label(self.sidebar, image=logo_image, bg="gray")
        logo_label.image = logo_image
        logo_label.pack(pady=10)
        tk.Frame(self.sidebar, height=1, bg="WHITE").pack(fill="x", padx=10, pady=10)

    # funcao que cria os botoes da barra lateral e associa a visualizacao correspondente
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

    # funcao que exibe a visualizacao clicada
    def show_view(self, view_name):
        if self.current_view:
            # se houver, destroi a visualização atual
            self.current_view[0].destroy()

        # recupera a classe e o controlador da visualização selecionada
        view_class, controller, _ = self.views[view_name]

        # instancia a view selecionada, passando o container e o controlador
        view = view_class(self.container, controller)

        view.pack(fill="both", expand=True)
        self.current_view = (view, controller)

        # muda a cor do botão clicado
        for btn in self.buttons.values():
            btn.config(bg="white")
        self.buttons[view_name].config(bg="#faebd8")


if __name__ == "__main__":
    app_controller = AppController.get_instance()
    app = Main(app_controller)
    app.mainloop()
