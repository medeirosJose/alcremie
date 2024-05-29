import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as sd
from tkcalendar import DateEntry
from datetime import datetime, timedelta


# https://www.youtube.com/watch?v=0CXQ3bbBLVk
# popup para criar um novo pedido
class PaymtStatusManager(tk.Toplevel):
    def __init__(self, parent, order):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Pedido {order.order_id}")
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

        # Radio Button estado de pagamento
        self.payment_var = tk.StringVar()
        self.payment_var.set("Pendente")  # Valor padrão

        payment_frame = tk.Frame(input_frame)
        payment_frame.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=(0, 5), pady=3
        )

        tk.Label(payment_frame, text="Estado de Pagamento: ").grid(row=0, column=0, sticky="w")
        
        # evita que o usuário mude de pago para pagamento pendente
        if order.payment_status != "Pago":
            radio_pending = tk.Radiobutton(
                payment_frame, text="Pendente", variable=self.payment_var, value="Pendente"
            )
            radio_pending.grid(row=1, column=2, sticky="w")

        radio_paid = tk.Radiobutton(
            payment_frame, text="Pago", variable=self.payment_var, value="Pago"
        )
        radio_paid.grid(row=2, column=2, sticky="w")

        radio_canceled = tk.Radiobutton(
            payment_frame, text="Cancelado", variable=self.payment_var, value="Cancelado"
        )
        radio_canceled.grid(row=3, column=2, sticky="w")

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

        if order:
            self.payment_var.set(order.payment_status)


    def confirm(self):
        payment_status = self.payment_var.get()
        print(type(self.payment_var))
        print(type(self.order))

        self.result = payment_status
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result


# view principal dos pedidos pendentes
class PendingOrdersView(tk.Frame):
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
            columns=("ID", "Cliente", "Produto", "Preço", "Pagamento", "Data de Entrega"),
            show="headings",
        )

        self.orders_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.orders_table.heading("Cliente", text="Cliente")
        self.orders_table.heading("Produto", text="Produto")
        self.orders_table.heading("Preço", text="Preço", anchor=tk.CENTER)
        self.orders_table.heading("Pagamento", text="Pagamento", anchor=tk.CENTER)
        self.orders_table.heading(
            "Data de Entrega", text="Data de Entrega", anchor=tk.CENTER
        )

        # altera o tamanho das colunas pra ficar mais bonito e organizado
        self.orders_table.column("ID", width=50, anchor=tk.CENTER)
        self.orders_table.column("Cliente", width=300)
        self.orders_table.column("Produto", width=300)
        self.orders_table.column("Preço", width=25)
        self.orders_table.column("Pagamento", width=25)
        self.orders_table.column("Data de Entrega", width=25, anchor=tk.CENTER)

        self.orders_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)
        print(type(tk.X))
        print(type(tk.TOP))

        # botão para ver detalhes do pedido
        self.view_details_button = tk.Button(
            buttons_frame, text="Ver Detalhes do Pedido", command=self.refresh_order_details,
        )
        self.view_details_button.pack(side=tk.LEFT, padx=5)

        # botão para alterar entre os três estados de pagamento
        self.create_order_button = tk.Button(
            buttons_frame, text="Gerenciar Estado de Pagamento", command=self.manage_paymt_status
        )
        self.create_order_button.pack(side=tk.LEFT, padx=5)

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

        self.refresh_pending_orders_list() #if not selected_items

    # atualiza os detalhes do pedido selecionado e exibe no frame de detalhes
    def refresh_order_details(self):
        # TODO Adicionar valor total dos produtos, eventual Observação do pedido

        # se ja tiver algo no frame de detalhes, limpa
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_items = self.orders_table.selection()

        if not selected_items:
            self.show_warning_popup("Aviso", "Selecione um pedido para ver seus detalhes.")
        else:
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
                    tk.Label(payment_frame, text=order.payment_status+', '+payment_date_str).pack(
                        side=tk.LEFT, padx=padx_value
                )

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

    # atualiza a lista de pedidos na treeview
    def refresh_pending_orders_list(self):
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
                    order.total_order_price,
                    order.payment_status,
                    order.delivery_date,
                ),
            )

    # abre o pop up para o gerenciamento do estado de pagamento do pedido
    def manage_paymt_status(self):
        selected_items = self.orders_table.selection()
        
        if not selected_items:
            self.show_warning_popup("Aviso", "Selecione um pedido para gerenciar o estado de pagamento.")

        else:
            selected_item = selected_items[0]
            order_details = self.orders_table.item(selected_item, "values")
            order_id = int(order_details[0])  # ID do pedido forçado pra int

            order = self.controller.get_order_details(order_id)

            if order:
                popup = PaymtStatusManager(self, order)
                payment_status = popup.show()
                if payment_status == None: # no caso de apertar o botão cancelar
                    return
                #RN02 - Se o pedido for cancelado com menos de dois dias de antecedência o sinal não é devolvido
                # para cumprir esse requisito salvamos o dia em que esse ajuste no estado de pagamento é feito 
                # para posterior uso no relatório de lucros
                if payment_status != "Pendente": # Aqui salva a data de pagamento/ cancelamento no pedido
                    self.controller.update_order(order_id, payment_status, datetime.now().date())

                    delivery_date = datetime.strptime(order.delivery_date, "%d/%m/%Y").date()
                    if payment_status == "Cancelado" and order.total_order_price > 150:
                        if (delivery_date - datetime.now().date() >= timedelta(days=2)):
                            self.show_warning_popup("Aviso", f"Devolva o sinal de R${order.total_order_price*35/100} ao cliente.")
                        else:
                            self.show_info_popup("Aviso", "Sinal não deve ser devolvido pois o pedido foi cancelado com menos de dois dias de antecedência")
                    self.refresh_pending_orders_list()  

    def show_info_popup(self, title, message):
        messagebox.showinfo(title, message)

    def show_warning_popup(self, title, message):
        messagebox.showwarning(title, message)
