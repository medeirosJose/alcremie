import tkinter as tk
from PIL import Image, ImageTk
from views.order_view import OrderView
from views.products_view import ProductsView
from views.customer_view import CustomersView
from controllers.app_controller import (
    AppController,
)


class Main(tk.Tk):
    def __init__(self, app_controller):
        super().__init__()
        self.title("Confeitaria Alcremie")
        self.state("zoomed")  # garante que a janela inicie maximizada

        # cria a barra lateral
        self.sidebar = tk.Frame(self, width=400, bg="gray")
        self.sidebar.pack(fill="y", side="left")

        self.load_and_display_logo()

        # cria o container para as views
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # cria a imagem de logo
        image = Image.open("logo.png")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.container, image=photo)
        label.image = photo
        # centraliza a imagem no centro da view do container
        label.place(relx=0.5, rely=0.5, anchor="center")

        # cria o controller principal (singleton)
        self.app_controller = app_controller
        self.user_controller = self.app_controller.get_user_controller()

        #! Aqui tem q adicionar as demais views e seus controllers atraves do self.app_controller
        self.views = {
            "Pedido": (OrderView, self.app_controller.get_order_controller()),
            "Produtos": (ProductsView, self.app_controller.get_products_controller()),
            "Clientes": (CustomersView, self.app_controller.get_customer_controller()),
            # placeholder
            "Relatórios": (OrderView, self.app_controller.get_order_controller()),
            "Configurações": (OrderView, self.app_controller.get_order_controller()),
            "Sair": (OrderView, self.app_controller.get_order_controller()),
        }

        self.current_view = None
        self.buttons = {}
        self.active_button = None
        self.create_sidebar_buttons()

    def load_and_display_logo(self):
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((150, 150), Image.LANCZOS)

        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.sidebar, image=logo_photo, bg="gray")
        logo_label.image = logo_photo
        logo_label.pack(pady=20)

        # divisória
        divider = tk.Frame(
            self.sidebar,
            height=1,
        )
        divider.pack(fill="x", padx=50, pady=10)

    # funcao que cria os botoes da barra lateral e associa a visualizacao correspondente
    def create_sidebar_buttons(self):
        for view_name in self.views:
            button = tk.Button(
                self.sidebar,
                text=view_name,
                command=lambda name=view_name: self.show_view(name),
                relief="ridge",
                bg="white",
                width=20,
            )
            button.pack(padx=10, pady=10, fill="x")
            self.buttons[view_name] = button

    # funcao que exibe a visualizacao clicada
    def show_view(self, view_name):
        if self.current_view:
            # se houver, destroi a visualização atual
            self.current_view[0].destroy()

        if self.active_button:
            self.active_button.config(bg="white")

        # recupera a classe e o controlador da visualização selecionada
        view_class, controller = self.views[view_name]

        # instancia a view selecionada, passando o container e o controlador
        view = view_class(self.container, controller)

        view.pack(fill="both", expand=True)

        self.current_view = (view, controller)

        # atualiza o botão ativo
        self.active_button = self.buttons[view_name]
        self.active_button.config(bg="#faebd8")


if __name__ == "__main__":
    app_controller = AppController.get_instance()
    app = Main(app_controller)
    app.mainloop()
