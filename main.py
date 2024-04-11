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
        self.state("zoomed")

        self.sidebar = tk.Frame(self, width=400, bg="gray")
        self.sidebar.pack(fill="y", side="left")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        image = Image.open("logo.png")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.container, image=photo)
        label.image = photo
        label.place(x=600, y=200)

        self.app_controller = (
            app_controller  # Armazena app_controller para uso posterior
        )
        self.user_controller = self.app_controller.get_user_controller()

        #! Aqui tem q adicionar as demais views e seus controllers atraves do self.app_controller
        self.views = {
            "Pedido": (OrderView, self.app_controller.get_order_controller()),
            "Produtos": (ProductsView, self.app_controller.get_products_controller()),
            "Clientes": (CustomersView, self.app_controller.get_customer_controller()),
        }

        self.current_view = None
        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        for view_name in self.views:
            button = tk.Button(
                self.sidebar,
                text=view_name,
                command=lambda name=view_name: self.show_view(name),
                width=10,
            )
            button.pack(padx=40, ipadx=50, ipady=5, pady=8)

    def show_view(self, view_name):
        # Verifica se já existe uma visualização atual
        if self.current_view:
            # Se houver, destroi a visualização atual
            self.current_view[0].destroy()

        view_class, controller = self.views[
            view_name
        ]  # controller já é instância, não classe

        # Instancia a visualização selecionada, passando o container e o controlador
        view = view_class(self.container, controller)

        view.pack(fill="both", expand=True)

        self.current_view = (view, controller)


if __name__ == "__main__":
    app_controller = AppController.get_instance()
    app = Main(app_controller)
    app.mainloop()
