import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as sd


class NewOrderPopup(sd.Dialog):
    def __init__(self, parent, controller):
        # Primeiro, defina o atributo controller
        self.controller = controller
        # Agora, chame __init__ da classe base
        super().__init__(parent, title="Novo Pedido")

    def body(self, frame):
        tk.Label(frame, text="Cliente:").grid(row=0, column=0)
        # Supondo que get_clients_list retorna uma lista de clientes
        self.client_combobox = ttk.Combobox(
            frame, values=self.controller.get_clients_list()
        )
        self.client_combobox.grid(row=0, column=1)

        tk.Label(frame, text="Produto:").grid(row=1, column=0)
        # Supondo que get_products_list retorna uma lista de produtos
        self.product_listbox = tk.Listbox(
            frame, selectmode="extended", exportselection=0
        )
        for product in self.controller.get_products_list():
            self.product_listbox.insert(tk.END, product)
        self.product_listbox.grid(row=1, column=1)

        tk.Label(frame, text="Data de Entrega:").grid(row=2, column=0)
        self.delivery_date_entry = tk.Entry(frame)
        self.delivery_date_entry.grid(row=2, column=1)

        return self.client_combobox  # Para foco inicial

    def apply(self):
        client = self.client_combobox.get()
        selected_indices = self.product_listbox.curselection()
        selected_products = [self.product_listbox.get(i) for i in selected_indices]
        delivery_date = self.delivery_date_entry.get()
        self.controller.create_new_order(client, selected_products, delivery_date)


class OrderView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Alterando a cor de fundo dos itens
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3",
        )
        style.configure("Treeview.Heading", font=("Calibri", 10, "bold"))

        # Create the Treeview with columns and headings
        self.orders_table = ttk.Treeview(
            self,
            columns=("ID", "Cliente", "Produto", "Data de Entrega"),
            show="headings",
        )

        # Set heading text and specify width for "ID" and "Data de Entrega"
        self.orders_table.heading(
            "ID", text="ID", anchor=tk.CENTER
        )  # Center alignment (optional)
        self.orders_table.heading("Cliente", text="Cliente")
        self.orders_table.heading("Produto", text="Produto")
        self.orders_table.heading(
            "Data de Entrega", text="Data de Entrega", anchor=tk.CENTER
        )  # Center alignment (optional)

        # Set column widths for "ID" and "Data de Entrega" to 50 pixels
        self.orders_table.column(
            "ID", width=50, anchor=tk.CENTER
        )  # Align content to center (optional)
        self.orders_table.column(
            "Data de Entrega", width=50, anchor=tk.CENTER
        )  # Align content to center (optional)
        self.orders_table.pack(side="top", fill="both", expand=True, pady=10)
        # Botão para criar um novo pedido
        self.create_order_button = tk.Button(
            self, text="Criar Novo Pedido", command=self.open_new_order_popup
        )
        self.create_order_button.pack(pady=5)

        # Frame para detalhes do pedido
        self.details_frame = tk.Frame(self, borderwidth=2, relief="groove")
        self.details_frame.pack(fill="both", expand=True, pady=5)

        # Botão para ver detalhes do pedido
        self.view_details_button = tk.Button(
            self, text="Ver Detalhes do Pedido", command=self.refresh_order_details
        )
        self.view_details_button.pack(pady=5)

        # Inicializa e atualiza a lista de pedidos
        self.refresh_orders_list()

    def open_new_order_popup(self):
        NewOrderPopup(self, self.controller)
        # Atualiza a lista de pedidos após fechar o popup, mas não recria o frame de detalhes ou o botão de visualização
        self.refresh_orders_list()

    def refresh_order_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_items = self.orders_table.selection()
        if selected_items:
            selected_item = selected_items[0]  # Primeiro item selecionado
            order_details = self.orders_table.item(selected_item, "values")
            order_id = order_details[0]  # ID do pedido

            # Busca os detalhes do pedido usando o ID
            order = self.controller.get_order_details(order_id)

            if order:  # Se um pedido válido for retornado
                # Exibe os detalhes do pedido
                tk.Label(self.details_frame, text=f"Cliente: {order.client}").pack(
                    pady=2
                )
                tk.Label(
                    self.details_frame,
                    text=f"Status de Pagamento: {order.payment_status}",
                ).pack(pady=2)
                tk.Label(self.details_frame, text="Produtos:").pack(pady=2)

                for product in order.products:
                    tk.Label(self.details_frame, text=f"- {product}").pack(pady=1)

    def create_new_order(self):
        self.controller.create_new_order()
        self.refresh_orders_list()
        messagebox.showinfo("Sucesso", "Novo pedido criado com sucesso!")

    def refresh_orders_list(self):
        # Primeiro, limpa a tabela atual removendo todos os itens
        for item in self.orders_table.get_children():
            self.orders_table.delete(item)

        # Busca todos os pedidos existentes através do OrderController
        orders = self.controller.get_all_orders()

        # Itera sobre os pedidos e insere-os na Treeview
        for order in orders:
            # Supondo que 'order.products' seja uma lista de strings representando produtos
            # e que order.order_id, order.client e order.delivery_date sejam strings ou tipos que podem ser
            # convertidos facilmente para strings.
            self.orders_table.insert(
                "",
                "end",
                values=(
                    order.order_id,
                    order.client,
                    ", ".join(
                        order.products
                    ),  # Junta todos os produtos em uma string única
                    order.delivery_date,
                ),
            )
