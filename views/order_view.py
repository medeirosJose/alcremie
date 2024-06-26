import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as sd
from tkcalendar import DateEntry
from datetime import datetime, timedelta


# https://www.youtube.com/watch?v=0CXQ3bbBLVk
# popup para criar um novo pedido
class NewOrderPopup(tk.Toplevel):
    def __init__(self, parent, controller, order=None):
        super().__init__(parent)
        self.controller = controller

        window_width = 600
        window_height = 750

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2) - 30

        # colocao a janela no centro da tela
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.title("Pedido" if not order else f"Pedido {order.order_id}")
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

        self.client_combobox = ttk.Combobox(
            top_frame,
            values=[
                customer.name for customer in controller.get_customers_list()
            ],  # nomes dos clientes
            state="readonly",
            width=50,
        )
        self.client_combobox.grid(row=0, column=1, padx=10, sticky="w")

        # Armazenando referências aos objetos Customer para uso posterior
        self.clients = {
            customer.name: customer for customer in controller.get_customers_list()
        }

        self.populate_customers()

        ttk.Label(top_frame, text="Data de Entrega:*", style="TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.delivery_date_entry = DateEntry(
            top_frame,
            width=25,
            mindate=datetime.now()
            + timedelta(days=1),  #! RN 03 - Pedidos devem ter 1 dia de antecedencia
            date_pattern="dd/mm/yy",
            state="readonly",
        )
        self.delivery_date_entry.grid(row=1, column=1, padx=10, sticky="w")
        self.delivery_date_entry.bind("<<DateEntrySelected>>", self.check_date)

        # Pesquisa e Adição de Produtos
        ttk.Label(middle_frame, text="Pesquisar Produto:*", style="TLabel").pack(
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

        self.load_products()  # tive que colocar aqui para chamar depois de criar o listbox

        ttk.Label(middle_frame, text="Quantidade:*", style="TLabel").pack(
            anchor="w", padx=10
        )
        self.quantity_entry = ttk.Entry(middle_frame, width=5)
        self.quantity_entry.pack(padx=10, pady=5, fill="x")
        self.quantity_entry.bind("<KeyRelease>", self.format_quantity_entry)

        add_product_button = ttk.Button(
            middle_frame, text="Adicionar Produto", command=self.add_product_to_order
        )
        add_product_button.pack(pady=10)

        # Observação
        obs_label = ttk.Label(middle_frame, text="Observação:", style="TLabel")
        obs_label.pack(anchor="w", padx=10, pady=10, after=add_product_button)
        self.obs_entry = tk.Text(middle_frame, width=50, height=5)
        self.obs_entry.pack(padx=10, pady=5, fill="x", after=obs_label)

        # Listbox para itens do pedido
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

        # preenche os campos com os dados do pedido a ser editado
        if order:
            self.client_combobox.set(order.customer.name)
            self.delivery_date_entry.set_date(order.delivery_date)
            self.obs_entry.insert(tk.END, order.observation)
            self.order_items_listbox.delete(0, tk.END)
            self.order_items.clear()

            # Adiciona os produtos ao listbox
            for product, quantity in order.products:
                self.order_items.append((product, quantity))
                product_details = (
                    f"{quantity}x {product.name} - R$ {product.price:.2f}"
                    if hasattr(product, "name")
                    else "Produto não identificado"
                )
                self.order_items_listbox.insert(tk.END, product_details)

    # funcao que preenche o combobox de clientes e armazena os objetos Customer
    def populate_customers(self):
        customers = self.controller.get_customers_list()
        self.client_combobox["values"] = [customer.name for customer in customers]
        self.clients = {customer.name: customer for customer in customers}

    # semelhante a funcao de cpf da luana
    def format_quantity_entry(self, event=None):
        quantity = self.quantity_entry.get()
        if not quantity.isdigit():
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, "".join(filter(str.isdigit, quantity)))

    #! RN 05 - Não aceita pedidos para segundas e terças
    def check_date(self, event=None):
        # verifica se o dia selecionado é segunda ou terça-feira
        date = self.delivery_date_entry.get_date()
        if date.weekday() == 0 or date.weekday() == 1:
            messagebox.showerror(
                "Erro",
                "A confeitaria não abre às segundas e terças-feiras.\nMarcando para o dia seguinte.",
            )
            # redefine para o próximo dia válido
            next_valid_date = date + timedelta(days=2 if date.weekday() == 0 else 1)
            self.delivery_date_entry.set_date(next_valid_date)

    # funcao que filtra os produtos de acordo com o texto digitado
    # baseado no video https://www.youtube.com/watch?v=0CXQ3bbBLVk
    def on_search(self, event=None):
        search_text = self.search_var.get().lower()
        matching_products = [
            product
            for product in self.controller.get_products_list()
            if search_text
            in product.name.lower()  # Access the name attribute of Product
        ]
        self.products_listbox.delete(0, tk.END)
        for product in matching_products:
            self.products_listbox.insert(tk.END, product.name)
            # print(product.price)

    # carrega a lista de produtos do controller
    def load_products(self):
        self.products = {
            product.name: product for product in self.controller.get_products_list()
        }
        self.update_product_listbox()

    # atualiza a lista de produtos no listbox
    def update_product_listbox(self):
        self.products_listbox.delete(0, tk.END)
        for product_name in self.products:
            self.products_listbox.insert(tk.END, product_name)

    # adiciona um produto ao pedido
    def add_product_to_order(self):
        selected_index = self.products_listbox.curselection()
        if selected_index:
            selected_product_name = self.products_listbox.get(selected_index[0])
            selected_product = self.products[selected_product_name]
            try:
                quantity = int(self.quantity_entry.get())
                if quantity > 0:
                    self.order_items.append((selected_product, quantity))

                    self.order_items_listbox.insert(
                        tk.END,
                        f"{quantity}x {selected_product.name} - {selected_product.price * quantity:.2f}",
                    )

                    self.quantity_entry.delete(0, tk.END)
                else:
                    messagebox.showerror(
                        "Error", "Quantidade deve ser um número maior que 0."
                    )
            except ValueError:
                messagebox.showerror("Error", "Por favor digite uma quantidade válida.")

    # remove um produto do pedido
    def remove_selected_product(self):
        selected_indices = self.order_items_listbox.curselection()
        # se nao tiver nenhum selecionado, exibe um aviso
        if not selected_indices:
            messagebox.showwarning("Aviso", "Selecione um produto para remover.")
            return

        # remove os produtos selecionados da lista de itens do pedido
        for index in selected_indices[::-1]:
            del self.order_items[index]

        self.order_items_listbox.delete(selected_indices[0])

    # confirma o pedido, fecha a janela e retorna os dados do pedido para o controller
    def confirm_order(self):
        selected_customer_name = self.client_combobox.get()
        if selected_customer_name in self.clients:
            selected_customer = self.clients[selected_customer_name]

            delivery_date = self.delivery_date_entry.get_date()
            formatted_date = delivery_date.strftime("%d/%m/%Y") if delivery_date else ""

            # Checa se os campos obrigatórios estão vazios
            if not selected_customer_name or not formatted_date or not self.order_items:
                messagebox.showerror(
                    "Erro",
                    "Todos os campos são obrigatórios e deve haver pelo menos um item no pedido.",
                )
                return

            total_price, descountApplied = self.controller.calculate_total(
                self.order_items, selected_customer
            )

            total_price, message = self.controller.check_order_requirements(total_price)

            # RN X - Avisa ao usuário que há um sinal necessário no pedido
            # print("message: ", message)
            if message:
                response = messagebox.showinfo("Aviso", message)
                if not response:
                    return
            else:
                message = ""
                
            user_observation = self.obs_entry.get("1.0", tk.END).strip().split(" | ")

            print(len(user_observation))
            if len(user_observation) > 1:
                user_observation = user_observation[1]
            else:
                user_observation = user_observation[0]

            self.result = {
                "client": selected_customer,  # Armazena a instância do cliente
                "delivery_date": formatted_date,
                "order_items": self.order_items,  # Lista de tuplas (Product, quantity)
                "total_price": total_price,
                "observation": message
                + " | "
                + user_observation,  # Observação do pedido
            }
            self.destroy()
        else:
            messagebox.showerror("Erro", "Cliente selecionado não encontrado.")

    def show(self):
        self.wait_window(self)
        return self.result


# view principal dos pedidos
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

        # cria a TreeView para exibir os pedidos com 4 colunas
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

        # altera o tamanho das colunas pra ficar mais bonito e organizado
        self.orders_table.column("ID", width=25, anchor=tk.CENTER)
        self.orders_table.column("Data de Entrega", width=25, anchor=tk.CENTER)
        self.orders_table.column("Cliente", width=100)
        self.orders_table.column("Produto", width=400)

        self.orders_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)

        # criar um novo pedido
        self.create_order_button = tk.Button(
            buttons_frame, text="Criar Novo Pedido", command=self.open_new_order_popup
        )
        self.create_order_button.pack(side=tk.LEFT, padx=5)

        # editar um pedido existente
        self.edit_order_button = tk.Button(
            buttons_frame, text="Editar Pedido", command=self.edit_order
        )
        self.edit_order_button.pack(side=tk.LEFT, padx=5)

        # remover um pedido selecionado
        self.remove_order_button = tk.Button(
            buttons_frame, text="Remover Pedido", command=self.remove_order
        )
        self.remove_order_button.pack(side=tk.LEFT, padx=5)

        # botão para ver detalhes do pedido
        self.view_details_button = tk.Button(
            buttons_frame,
            text="Ver Detalhes do Pedido",
            command=self.refresh_order_details,
        )
        self.view_details_button.pack(side=tk.LEFT, padx=5)

        # frame para detalhes do pedido
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

    # abre o popup para criar um novo pedido
    def open_new_order_popup(self):
        popup = NewOrderPopup(self, self.controller)
        result = popup.show()
        if result:
            client = result["client"]
            delivery_date = result["delivery_date"]
            order_items = result["order_items"]
            observation = result["observation"]
            #  # print("1")
            descountApplied = self.controller.create_new_order(
                client,
                order_items,
                delivery_date,
                observation,
            )

            if descountApplied:
                messagebox.showinfo("Aviso", descountApplied)

            self.refresh_orders_list()

    # atualiza os detalhes do pedido selecionado e exibe no frame de detalhes
    def refresh_order_details(self):
        # TODO Adicionar valor total dos produtos, eventual Observação do pedido

        # se ja tiver algo no frame de detalhes, limpa
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_items = self.orders_table.selection()
        if selected_items:
            selected_item = selected_items[0]
            order_details = self.orders_table.item(selected_item, "values")
            order_id = int(order_details[0])  # ID do pedido forçado pra int

            order = self.controller.get_order_details(order_id)

            if order:
                # Defina as larguras máximas para os labels e os valores
                label_width = 20
                value_width = 30

                # Use padx para espaçamento consistente
                padx_value = 5

                # Frame para Cliente e Data
                top_frame1 = tk.Frame(self.details_frame)
                top_frame1.pack(fill=tk.X, pady=2)

                client_frame = tk.Frame(top_frame1)
                client_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

                date_frame = tk.Frame(top_frame1)
                date_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

                # Frame para Status de Pagamento e Preço Total
                top_frame2 = tk.Frame(self.details_frame)
                top_frame2.pack(fill=tk.X, pady=2)

                payment_frame = tk.Frame(top_frame2)
                payment_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

                total_price_frame = tk.Frame(top_frame2)
                total_price_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

                # Labels e Listbox
                tk.Label(
                    client_frame, text="Cliente:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=padx_value)
                tk.Label(client_frame, text=order.customer.name).pack(
                    side=tk.LEFT, padx=padx_value
                )

                tk.Label(
                    date_frame, text="Data de Entrega:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=padx_value)
                tk.Label(date_frame, text=order.delivery_date).pack(
                    side=tk.LEFT, padx=padx_value
                )

                if order.payment_date is None:
                    tk.Label(
                        payment_frame,
                        text="Status de Pagamento:",
                        font=("Arial", 10, "bold"),
                    ).pack(side=tk.LEFT, padx=padx_value)
                    tk.Label(payment_frame, text=order.payment_status).pack(
                        side=tk.LEFT, padx=padx_value
                    )
                else:
                    payment_date_str = order.payment_date.strftime("%d/%m/%Y")
                    tk.Label(
                        payment_frame,
                        text="Status de Pagamento:",
                        font=("Arial", 10, "bold"),
                    ).pack(side=tk.LEFT, padx=padx_value)
                    tk.Label(
                        payment_frame,
                        text=order.payment_status + ", " + payment_date_str,
                    ).pack(side=tk.LEFT, padx=padx_value)

                tk.Label(
                    total_price_frame, text="Preço Total:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=padx_value)
                tk.Label(total_price_frame, text=f"R$ {order.total_order_price}").pack(
                    side=tk.LEFT, padx=padx_value
                )

                obs_frame = tk.Frame(self.details_frame)
                obs_frame.pack(fill=tk.X, pady=2)
                tk.Label(
                    obs_frame, text="Observação:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=padx_value)
                tk.Label(obs_frame, text=order.observation).pack(
                    side=tk.LEFT, fill=tk.X, padx=padx_value
                )

                products_frame = tk.Frame(self.details_frame)
                products_frame.pack(fill=tk.X, pady=2)
                products_label = tk.Label(
                    products_frame,
                    text="Produtos",
                    font=("Arial", 10, "bold"),
                    anchor="w",
                )
                products_label.pack(side=tk.TOP, anchor="w", padx=padx_value)

                products_listbox = tk.Listbox(products_frame, height=6)
                products_listbox.pack(
                    side=tk.LEFT, fill=tk.BOTH, expand=True, padx=padx_value, pady=2
                )

                for product, quantity in order.products:
                    products_listbox.insert(
                        tk.END,
                        f"{quantity}x {product.name} - R$ {product.price:.2f} a unidade",
                    )

                self.details_frame.mainloop()

    # remove o pedido selecionado
    def remove_order(self):
        selected_items = self.orders_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um pedido para remover.")
            return
        selected_item = selected_items[0]
        order_details = self.orders_table.item(selected_item, "values")
        order_id = order_details[0]

        # pede confirmação antes de remover, RNF
        if messagebox.askyesno("Confirmar", "Deseja realmente remover este pedido?"):
            # print(f"VIEW - Removendo pedido {order_id}")
            self.controller.remove_order(order_id)
            self.refresh_orders_list()

    # abre o popup para editar o pedido selecionado
    def edit_order(self):
        selected_items = self.orders_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um pedido para editar.")
            return
        selected_item = selected_items[0]
        order_details = self.orders_table.item(selected_item, "values")
        order_id = int(order_details[0])

        order = self.controller.get_order_details(order_id)
        popup = NewOrderPopup(self, self.controller, order)
        result = popup.show()
        print("\n\nRESULTADO: ", result)
        if result:
            client = result["client"]
            delivery_date = result["delivery_date"]
            order_items = result["order_items"]
            observation = result["observation"]
            self.controller.update_order(
                order_id, client, order_items, delivery_date, observation
            )
            self.refresh_orders_list()

    # atualiza a lista de pedidos na treeview
    def refresh_orders_list(self):
        self.orders_table.delete(*self.orders_table.get_children())
        for order in self.controller.get_all_orders():
            products_string = ", ".join(
                [f"{quantity}x {product.name}" for product, quantity in order.products]
            )

            # insere os dados do pedido na treeview
            self.orders_table.insert(
                "",
                "end",
                values=(
                    order.order_id,
                    order.customer.name,
                    products_string,
                    order.delivery_date,
                ),
            )
