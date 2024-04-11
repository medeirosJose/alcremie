import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as sd
from tkcalendar import DateEntry


class NewOrderPopup:
    def __init__(self, parent, controller, order=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Editar Pedido" if order else "Novo Pedido")
        self.controller = controller
        self.order = order
        self.result = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 400
        window_height = 300

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("400x300")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        # Cliente
        tk.Label(input_frame, text="Cliente:").grid(row=0, column=0, sticky="e")
        self.client_combobox = ttk.Combobox(
            input_frame,
            values=self.controller.get_clients_list(),
            state="readonly",
            width=40,
        )
        self.client_combobox.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        # Produto
        product_frame = tk.Frame(input_frame)
        product_frame.grid(row=1, column=1, sticky="ew", pady=5)
        self.product_listbox = tk.Listbox(
            product_frame, selectmode="extended", exportselection=0, height=6, width=30
        )
        self.product_scrollbar = tk.Scrollbar(
            product_frame, orient="vertical", command=self.product_listbox.yview
        )
        self.product_listbox.configure(yscrollcommand=self.product_scrollbar.set)

        self.product_listbox.pack(side="left", fill="both", expand=True)
        self.product_scrollbar.pack(side="right", fill="y")

        for product in self.controller.get_products_list():
            self.product_listbox.insert(tk.END, product)

        # Data de Entrega
        tk.Label(input_frame, text="Data de Entrega:").grid(
            row=2, column=0, sticky="e", padx=5
        )
        self.delivery_date_entry = DateEntry(input_frame, date_pattern="dd/mm/yyyy")
        self.delivery_date_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

        if order:
            self.client_combobox.set(order.client)

            for product in order.products:
                idx = self.controller.get_products_list().index(product)
                self.product_listbox.selection_set(idx)
            self.delivery_date_entry.set_date(order.delivery_date)

    def confirm(self):
        client = self.client_combobox.get()
        selected_indices = self.product_listbox.curselection()
        selected_products = [self.product_listbox.get(i) for i in selected_indices]
        delivery_date = self.delivery_date_entry.get()

        self.result = (client, selected_products, delivery_date)
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
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

        # Ver detalhes do pedido
        self.view_details_button = tk.Button(
            buttons_frame,
            text="Ver Detalhes do Pedido",
            command=self.refresh_order_details,
        )
        self.view_details_button.pack(side=tk.LEFT, padx=5)

        # Frame para detalhes do pedido
        self.details_frame = tk.Frame(self, borderwidth=2, relief="groove", height=200)
        self.details_frame.pack(fill=tk.X, expand=False, pady=5)
        self.details_frame.pack_propagate(
            False
        )  # Impede o frame de alterar seu tamanho

        # Canvas e Scrollbar dentro do details_frame
        self.details_canvas = tk.Canvas(self.details_frame)
        self.details_scrollbar = tk.Scrollbar(
            self.details_frame, orient="vertical", command=self.details_canvas.yview
        )
        self.details_scrollable_frame = tk.Frame(self.details_canvas)

        # Configura o frame scrollável para ser o conteúdo do Canvas
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

        # Empacota o Canvas e a Scrollbar no details_frame
        self.details_canvas.pack(side="left", fill="both", expand=True)
        self.details_scrollbar.pack(side="right", fill="y")

        self.refresh_orders_list()

    def open_new_order_popup(self):
        popup = NewOrderPopup(self, self.controller)
        result = popup.show()
        if result:
            client, selected_products, delivery_date = result
            self.controller.create_new_order(client, selected_products, delivery_date)
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
                    client_frame, text="Cliente:", font=("Arial", 10, "bold")
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
                for product in order.products:
                    products_listbox.insert(tk.END, f"- {product}")

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
            popup = NewOrderPopup(
                self, self.controller, order
            )  # Assuma que você ajustará o NewOrderPopup para aceitar um pedido existente
            result = popup.show()
            if result:
                client, selected_products, delivery_date = result
                self.controller.update_order(
                    order_id, client, selected_products, delivery_date
                )
                self.refresh_orders_list()

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
