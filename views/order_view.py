import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as sd
from tkcalendar import DateEntry
from datetime import datetime


# https://www.youtube.com/watch?v=0CXQ3bbBLVk
class NewOrderPopup(tk.Toplevel):
    def __init__(self, parent, controller, order=None):
        super().__init__(parent)
        self.controller = controller
        window_width = 600
        window_height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2) - 30

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.title("Pedido" if not order else f"Editar Pedido: {order.order_id}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.order_items = []

        # Frames Principais
        top_frame = tk.Frame(self, pady=10)
        top_frame.pack(fill=tk.X)

        middle_frame = tk.Frame(self)
        middle_frame.pack(
            fill=tk.BOTH,
        )

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X)

        # Cliente e Data
        ttk.Label(top_frame, text="Cliente:", style="TLabel").grid(
            row=0, column=0, padx=10, sticky="e"
        )
        self.client_combobox = ttk.Combobox(
            top_frame,
            values=controller.get_clients_list(),
            state="readonly",
            width=50,
        )
        self.client_combobox.grid(row=0, column=1, padx=10, sticky="w")

        ttk.Label(top_frame, text="Data de Entrega:", style="TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.delivery_date_entry = DateEntry(
            top_frame,
            width=25,
            date_pattern="dd/mm/yy",
            state="readonly",
        )
        self.delivery_date_entry.grid(row=1, column=1, padx=10, sticky="w")

        # Pesquisa e Adição de Produtos
        ttk.Label(middle_frame, text="Pesquisar Produto:", style="TLabel").pack(
            anchor="w", padx=10
        )
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            middle_frame, textvariable=self.search_var, width=40
        )
        self.search_entry.pack(padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.products_listbox = tk.Listbox(middle_frame, height=5, width=50)
        self.products_listbox.pack(padx=10, pady=5, fill=tk.X)

        ttk.Label(middle_frame, text="Quantidade:", style="TLabel").pack(
            anchor="w", padx=10
        )
        self.quantity_entry = tk.Entry(middle_frame, width=15)
        self.quantity_entry.pack(padx=10, pady=5)

        add_product_button = ttk.Button(
            middle_frame, text="Adicionar Produto", command=self.add_product_to_order
        )
        add_product_button.pack(pady=10)

        # Label e Listbox para itens do pedido
        ttk.Label(bottom_frame, text="Itens do Pedido:", style="TLabel").pack(
            anchor="w", padx=10
        )
        self.order_items_listbox = tk.Listbox(bottom_frame, height=10, width=70)
        self.order_items_listbox.pack(padx=10, pady=5, fill=tk.X)

        # Botão para remover o produto selecionado
        remove_product_button = ttk.Button(
            bottom_frame,
            text="Remover Produto Selecionado",
            command=self.remove_selected_product,
        )
        remove_product_button.pack(pady=5, padx=10)

        # Botão Confirmar
        confirm_button = ttk.Button(
            bottom_frame, text="Confirmar Pedido", command=self.confirm_order
        )
        confirm_button.pack(pady=10)

        if order:
            self.client_combobox.set(order.client)
            self.delivery_date_entry.set_date(
                datetime.strptime(order.delivery_date, "%d/%m/%Y").date()
            )
            for product, quantity in order.products:
                self.order_items.append((product, quantity))
                self.order_items_listbox.insert(
                    tk.END, f"{product} - Quantidade: {quantity}"
                )

    def on_search(self, event=None):
        search_text = self.search_var.get().lower()
        matching_products = [
            product
            for product in self.controller.get_products_list()
            if search_text in product.lower()
        ]
        self.products_listbox.delete(0, tk.END)
        for product in matching_products:
            self.products_listbox.insert(tk.END, product)

    def add_product_to_order(self):
        product = self.products_listbox.get(self.products_listbox.curselection())
        quantity = self.quantity_entry.get()
        if product and quantity.isdigit():
            self.order_items.append((product, int(quantity)))
            self.order_items_listbox.insert(
                tk.END, f"{product} - Quantidade: {quantity}"
            )
            self.quantity_entry.delete(0, tk.END)

    def remove_selected_product(self):
        selected_indices = self.order_items_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Selecione um produto para remover.")
            return

        for index in selected_indices[::-1]:
            del self.order_items[index]

        self.order_items_listbox.delete(selected_indices[0])

    def confirm_order(self):
        client = self.client_combobox.get()
        delivery_date = self.delivery_date_entry.get_date()
        formatted_date = delivery_date.strftime("%d/%m/%Y")

        if not self.order_items or not client:
            messagebox.showerror("Erro", "Pedido incompleto.")
            return
        self.result = {
            "client": client,
            "delivery_date": str(formatted_date),
            "order_items": self.order_items,
        }
        print("result", self.result)
        self.destroy()

    def show(self):
        self.wait_window(self)  # Espera a janela ser destruída
        # Você pode querer retornar algum valor aqui, por exemplo:
        return self.result


class OrderView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3",
        )
        style.configure("Treeview.Heading", font=("Calibri", 10, "bold"))

        self.orders_table = ttk.Treeview(
            self,
            columns=("ID", "Cliente", "Produto", "Data de Entrega"),
            show="headings",
        )

        self.orders_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.orders_table.heading("Cliente", text="Cliente")
        self.orders_table.heading("Produto", text="Produto")
        self.orders_table.heading(
            "Data de Entrega", text="Data de Entrega", anchor=tk.CENTER
        )

        self.orders_table.column("ID", width=25, anchor=tk.CENTER)  # Pequeno
        self.orders_table.column(
            "Data de Entrega", width=25, anchor=tk.CENTER
        )  # Pequeno
        self.orders_table.column("Cliente", width=100)  # Médio
        self.orders_table.column("Produto", width=400)  # Grande

        self.orders_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)

        # Criar um novo pedido
        self.create_order_button = tk.Button(
            buttons_frame, text="Criar Novo Pedido", command=self.open_new_order_popup
        )
        self.create_order_button.pack(side=tk.LEFT, padx=5)

        # Editar um pedido existente
        self.edit_order_button = tk.Button(
            buttons_frame, text="Editar Pedido", command=self.edit_order
        )
        self.edit_order_button.pack(side=tk.LEFT, padx=5)

        # Remover um pedido selecionado
        self.remove_order_button = tk.Button(
            buttons_frame, text="Remover Pedido", command=self.remove_order
        )
        self.remove_order_button.pack(side=tk.LEFT, padx=5)

        # Botão para ver detalhes do pedido
        self.view_details_button = tk.Button(
            buttons_frame,
            text="Ver Detalhes do Pedido",
            command=self.refresh_order_details,
        )
        self.view_details_button.pack(side=tk.LEFT, padx=5)

        # Frame para detalhes do pedido
        self.details_frame = tk.Frame(self, borderwidth=2, relief="groove", height=200)
        self.details_frame.pack(fill=tk.X, expand=False, pady=5)
        self.details_frame.pack_propagate(False)  # faz o tamanho do frame ficar fixo

        self.details_canvas = tk.Canvas(self.details_frame)
        self.details_scrollbar = tk.Scrollbar(
            self.details_frame, orient="vertical", command=self.details_canvas.yview
        )
        self.details_scrollable_frame = tk.Frame(self.details_canvas)

        # faz o frame dentro do canvas ser um scrollavel
        self.details_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.details_canvas.configure(
                scrollregion=self.details_canvas.bbox("all")
            ),
        )

        self.details_canvas.create_window(
            (0, 0), window=self.details_scrollable_frame, anchor="nw"
        )
        self.details_canvas.configure(yscrollcommand=self.details_scrollbar.set)

        self.details_canvas.pack(side="left", fill="both", expand=True)
        self.details_scrollbar.pack(side="right", fill="y")

        self.refresh_orders_list()

    def open_new_order_popup(self):
        popup = NewOrderPopup(self, self.controller)
        result = popup.show()
        if result:
            # Extrai os valores do dicionário result
            client = result["client"]
            delivery_date = result["delivery_date"]
            order_items = result["order_items"]
            print("1")
            self.controller.create_new_order(client, order_items, delivery_date)
            self.refresh_orders_list()

    def refresh_order_details(self):
        # TODO Adicionar valor total dos produtos, eventual Observação do pedido

        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_items = self.orders_table.selection()
        if selected_items:
            selected_item = selected_items[0]  # Primeiro item selecionado
            order_details = self.orders_table.item(selected_item, "values")
            order_id = order_details[0]  # ID do pedido

            order = self.controller.get_order_details(order_id)

            if order:
                # Frames para cada seção
                client_frame = tk.Frame(self.details_frame)
                client_frame.pack(fill=tk.X, pady=2)
                payment_frame = tk.Frame(self.details_frame)
                payment_frame.pack(fill=tk.X, pady=2)
                date_frame = tk.Frame(self.details_frame)
                date_frame.pack(fill=tk.X, pady=2)
                products_frame = tk.Frame(self.details_frame)
                products_frame.pack(fill=tk.X, pady=2)

                # Cliente
                tk.Label(
                    client_frame,
                    text="Cliente:",
                    font=("Arial", 10, "bold"),
                ).pack(side=tk.LEFT)
                tk.Label(client_frame, text=f"{order.client}").pack(
                    side=tk.LEFT, padx=5
                )

                # Status de Pagamento
                tk.Label(
                    payment_frame,
                    text="Status de Pagamento:",
                    font=("Arial", 10, "bold"),
                ).pack(side=tk.LEFT)
                tk.Label(payment_frame, text=f"{order.payment_status}").pack(
                    side=tk.LEFT, padx=5
                )
                # Data
                tk.Label(
                    date_frame, text="Data de Entrega:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT)
                tk.Label(date_frame, text=f"{order.delivery_date}").pack(
                    side=tk.LEFT, padx=5
                )

                # # Preço Total
                # tk.Label(
                #     date_frame, text="Preço Total:", font=("Arial", 10, "bold")
                # ).pack(side=tk.LEFT)
                # tk.Label(date_frame, text=f"{order.total_order_price}").pack(
                #     side=tk.LEFT, padx=5
                # )

                # # Observação
                # tk.Label(
                #     date_frame, text="Observação:", font=("Arial", 10, "bold")
                # ).pack(side=tk.LEFT)
                # tk.Label(date_frame, text=f"{order.observation}").pack(
                #     side=tk.LEFT, padx=5
                # )

                # Produtos
                tk.Label(
                    products_frame, text="Produtos:", font=("Arial", 10, "bold")
                ).pack(anchor="w")
                products_listbox = tk.Listbox(
                    products_frame, height=min(4, len(order.products))
                )
                products_listbox.pack(fill=tk.X, pady=5)
                for product, quantity in order.products:
                    products_listbox.insert(tk.END, f"{quantity}x {product}")

    def create_new_order(self):
        self.controller.create_new_order()
        self.refresh_orders_list()
        messagebox.showinfo("Sucesso", "Novo pedido criado com sucesso!")

    def remove_order(self):
        selected_items = self.orders_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um pedido para remover.")
            return
        selected_item = selected_items[0]
        order_details = self.orders_table.item(selected_item, "values")
        order_id = order_details[0]
        if messagebox.askyesno("Confirmar", "Deseja realmente remover este pedido?"):
            print(f"Removendo pedido {order_id}")
            self.controller.remove_order(order_id)
            self.refresh_orders_list()

    def edit_order(self):
        selected_items = self.orders_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um pedido para editar.")
            return
        selected_item = selected_items[0]
        order_details = self.orders_table.item(selected_item, "values")
        order_id = int(order_details[0])
        order = self.controller.get_order_details(order_id)
        if order:
            popup = NewOrderPopup(self, self.controller, order)
            result = popup.show()
            if result:
                # Atualiza o pedido existente com os novos dados
                self.controller.update_order(
                    order.order_id,
                    result["client"],
                    result["order_items"],
                    result["delivery_date"],
                )
                self.refresh_orders_list()

    def refresh_orders_list(self):
        self.orders_table.delete(*self.orders_table.get_children())  # Limpa a TreeView
        for order in self.controller.get_all_orders():
            print("Order do Refresh List", order)
            # Assume que 'order.products' é uma lista de tuplas (nome_do_produto, quantidade)
            # ou uma lista de dicionários com chaves 'product' e 'quantity'
            products_string = ", ".join(
                [f"{quantity}x {product}" for product, quantity in order.products]
            )

            self.orders_table.insert(
                "",
                "end",
                values=(
                    order.order_id,
                    order.client,
                    products_string,
                    order.delivery_date,
                ),
            )
