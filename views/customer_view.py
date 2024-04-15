import tkinter as tk
from tkinter import messagebox, ttk


class AskCpf:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Buscar por Cliente")
        self.result = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 400
        window_height = 300

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("400x100")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        # Input CPF
        entry_label_cpf = tk.Label(input_frame, text="CPF do Cliente:")
        entry_label_cpf.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.entry_cpf = tk.Entry(input_frame, width=30)
        self.entry_cpf.grid(row=0, column=1, sticky="ew")

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)
 
    def confirm(self):
        cpf = self.entry_cpf.get()

        self.result = (cpf)
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result


class NewCustomerPopup:
    def __init__(self, parent, controller, customer=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Editar Dados do Cliente" if customer else "Novo Cliente")
        self.controller = controller
        self.customer = customer
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

        # Input CPF
        entry_label_cpf = tk.Label(input_frame, text="CPF do Cliente:")
        entry_label_cpf.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.entry_cpf = tk.Entry(input_frame, width=30)
        self.entry_cpf.grid(row=0, column=1, sticky="ew")

        # Input Nome
        entry_label_name = tk.Label(input_frame, text="Nome do Cliente:")
        entry_label_name.grid(row=1, column=0, sticky="w", padx=(0, 5))

        self.entry_name = tk.Entry(input_frame, width=30)
        self.entry_name.grid(row=1, column=1, sticky="ew")        
        
        # Input Contato
        entry_label_contact = tk.Label(input_frame, text="Contato:")
        entry_label_contact.grid(row=2, column=0, sticky="w", padx=(0, 5))

        self.entry_contact = tk.Entry(input_frame, width=30)
        self.entry_contact.grid(row=2, column=1, sticky="ew")

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)
 
    def confirm(self):
        cpf = self.entry_cpf.get()
        name = self.entry_name.get()
        contact = self.entry_contact.get()

        self.result = (cpf, name, contact)
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result


class CustomersView(tk.Frame):
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

        self.customers_table = ttk.Treeview(
            self,
            columns=("CPF", "Nome do Cliente", "Contato"),
            show="headings",
        )

        self.customers_table.heading("CPF", text="CPF", anchor=tk.CENTER)
        self.customers_table.heading("Nome do Cliente", text="Nome do Cliente")
        self.customers_table.heading(
            "Contato", text="Contato", anchor=tk.CENTER
        )

        self.customers_table.column("CPF", width=25, anchor=tk.CENTER)  # Pequeno
        self.customers_table.column("Contato", width=25)  # Pequeno
        self.customers_table.column("Nome do Cliente", width=100)  # Médio

        self.customers_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)

        #BOTÕES
        
        # Adicionar cliente
        self.create_customer_button = tk.Button(
            buttons_frame, text="Adicionar Novo Cliente", command=self.create_new_customer
        )
        self.create_customer_button.pack(side=tk.LEFT, padx=5)
        
        # Editar dados de um cliente
        self.edit_customer_button = tk.Button(
            buttons_frame, text="Editar Dados de um Cliente", command=self.update_customer
        )
        self.edit_customer_button.pack(side=tk.LEFT, padx=5)

        # Buscar por cliente
        self.search_customer_button = tk.Button(
            buttons_frame, text="Buscar por Cliente", command=self.search_customer
        )
        self.search_customer_button.pack(side=tk.LEFT, padx=5)
        
        # Excluir cliente desse sistema
        self.remove_customer_button = tk.Button(
            buttons_frame, text="Excluir Cliente", command=self.remove_customer
        )
        self.remove_customer_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_customers_list()

    def refresh_customers_list(self):
        # Primeiro, limpa a tabela atual removendo todos os itens
        for item in self.customers_table.get_children():
            self.customers_table.delete(item)

        # Busca todos os pedidos existentes através do customerController
        customers = self.controller.get_all_customers()

        # Itera sobre os pedidos e insere-os na Treeview
        for customer in customers:
            self.customers_table.insert(
                "",
                "end",
                values=(
                    customer.cpf,
                    customer.name,
                    customer.contact,
                ),
            )

    def create_new_customer(self):
        popup = NewCustomerPopup(self, self.controller)
        result = popup.show()
        if result:
            cpf, name, contact = result
            self.controller.create_new_customer(cpf, name, contact)
            self.refresh_customers_list()

    # não está funcionando para alterar cpf
    def update_customer(self): 
        selected_items = self.customers_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return
        selected_item = selected_items[0]
        customer_details = self.customers_table.item(selected_item, "values")
        cpf = customer_details[0]
        customer = self.controller.get_customer(cpf)
        if customer:
            popup = NewCustomerPopup(
                self, self.controller, customer
            )  # Assuma que você ajustará o NewCustomerPopup para aceitar um pedido existente
            result = popup.show()
            if result:
                new_cpf, name, contact = result
                self.controller.update_customer(
                    cpf, new_cpf, name, contact # passar ainda o antigo cpf pois é a key
                )
                self.refresh_customers_list()

    def search_customer(self):
        popup = AskCpf(self)
        cpf_result = popup.show()
        if cpf_result==None: # no caso de apertar o botão cancelar 
            return
        try:
            customer = self.controller.get_customer(cpf_result)
            messagebox.showinfo("Cliente encontrado", f"    Nome: {customer.name}    Contato: {customer.contact}")
        except:
            messagebox.showwarning("Aviso", "Cliente não encontrado")

    def remove_customer(self):
        selected_items = self.customers_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        selected_item = selected_items[0]
        customer_details = self.customers_table.item(selected_item, "values")
        cpf = customer_details[0]
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente?"):
            print(f"Removendo cliente de CPF: {cpf}")
            self.controller.remove_customer(cpf)
            self.refresh_customers_list()
