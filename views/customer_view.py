import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry


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
        self.entry_cpf.bind("<KeyRelease>", self.format_cpf_entry)

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

    def format_cpf_entry(self, event):
        # Obtém o texto atual do campo de entrada do CPF
        cpf = self.entry_cpf.get()

        # Remove todos os caracteres não numéricos
        cpf = "".join(filter(str.isdigit, cpf))

        # Limita o comprimento do CPF a 11 caracteres
        cpf = cpf[:11]

        # Formata o CPF
        formatted_cpf = ""
        for i in range(len(cpf)):
            if i in [3, 6]:
                formatted_cpf += "."
            elif i == 9:
                formatted_cpf += "-"
            formatted_cpf += cpf[i]

        # Define o texto formatado de volta ao campo de entrada
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, formatted_cpf)

    def confirm(self):
        cpf = self.entry_cpf.get()

        if len(cpf) < 14:
            messagebox.showerror(
                "Erro",
                "   CPF incompleto!",
            )
            return

        self.result = cpf
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
        entry_label_cpf = tk.Label(input_frame, text="CPF do Cliente: *")
        entry_label_cpf.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=3)

        self.entry_cpf = tk.Entry(input_frame, width=30)
        self.entry_cpf.grid(row=0, column=1, sticky="ew")
        self.entry_cpf.bind("<KeyRelease>", self.format_cpf_entry)

        # Input Nome
        entry_label_name = tk.Label(input_frame, text="Nome do Cliente: *")
        entry_label_name.grid(row=1, column=0, sticky="w", padx=(0, 5), pady=3)

        self.entry_name = tk.Entry(input_frame, width=30)
        self.entry_name.grid(row=1, column=1, sticky="ew")

        # Input Contato
        entry_label_contact = tk.Label(input_frame, text="Contato: *")
        entry_label_contact.grid(row=2, column=0, sticky="w", padx=(0, 5), pady=3)

        self.entry_contact = tk.Entry(input_frame, width=30)
        self.entry_contact.grid(row=2, column=1, sticky="ew")

        # Radio Button Gênero
        self.gender_var = tk.StringVar()
        self.gender_var.set("Feminino")  # Valor padrão

        gender_frame = tk.Frame(input_frame)
        gender_frame.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=(0, 5), pady=3
        )

        tk.Label(gender_frame, text="Gênero: *").pack(side=tk.LEFT)

        radio_female = tk.Radiobutton(
            gender_frame, text="Feminino", variable=self.gender_var, value="Feminino"
        )
        radio_female.pack(side=tk.LEFT)

        radio_male = tk.Radiobutton(
            gender_frame, text="Masculino", variable=self.gender_var, value="Masculino"
        )
        radio_male.pack(side=tk.LEFT)

        # Calendário Data de Nascimento
        tk.Label(input_frame, text="Data de Nascimento: *").grid(
            row=4, column=0, sticky="w", padx=(0, 5)
        )
        self.date_birth_entry = DateEntry(input_frame, date_pattern="dd/mm/yyyy")
        self.date_birth_entry.grid(row=4, column=1, sticky="ew", pady=3)

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

        if customer:
            self.entry_cpf.insert(0, customer.cpf)
            self.entry_name.insert(0, customer.name)
            self.entry_contact.insert(0, customer.contact)
            self.gender_var.set(customer.gender)
            self.date_birth_entry.set_date(customer.date_birth)

    def format_cpf_entry(self, event):
        # Obtém o texto atual do campo de entrada do CPF
        cpf = self.entry_cpf.get()

        # Remove todos os caracteres não numéricos
        cpf = "".join(filter(str.isdigit, cpf))

        # Limita o comprimento do CPF a 11 caracteres
        cpf = cpf[:11]

        # Formata o CPF
        formatted_cpf = ""
        for i in range(len(cpf)):
            if i in [3, 6]:
                formatted_cpf += "."
            elif i == 9:
                formatted_cpf += "-"
            formatted_cpf += cpf[i]

        # Define o texto formatado de volta ao campo de entrada
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, formatted_cpf)

    def confirm(self):

        cpf = self.entry_cpf.get()
        name = self.entry_name.get().title()
        contact = self.entry_contact.get()
        gender = self.gender_var.get()
        date_birth = self.date_birth_entry.get()

        if not cpf or not name or not contact or not gender or not date_birth:
            messagebox.showerror(
                "Erro",
                "Todos os campos são obrigatórios",
            )
            return

        if len(cpf) < 14:
            messagebox.showerror(
                "Erro",
                "   CPF incompleto!",
            )
            return

        # Verifica se o nome contém apenas espaços
        if all(caractere.isspace() for caractere in name):
            messagebox.showerror(
                "Erro",
                "   Nome inválido. O nome não pode conter apenas espaços",
            )
            return
        # Verifica se o nome contém apenas letras e espaços, não aceita símbolos
        if not all(caractere.isalpha() or caractere.isspace() for caractere in name):
            messagebox.showerror(
                "Erro",
                "   Nome inválido. O nome deve conter apenas letras e espaços",
            )
            return

        self.result = (cpf, name, contact, gender, date_birth)
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
        self.customers_table.heading("Contato", text="Contato", anchor=tk.CENTER)

        self.customers_table.column("CPF", width=25, anchor=tk.CENTER)  # Pequeno
        self.customers_table.column("Contato", width=25)  # Pequeno
        self.customers_table.column("Nome do Cliente", width=100)  # Médio

        self.customers_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)

        # BOTÕES

        # Adicionar cliente
        self.create_customer_button = tk.Button(
            buttons_frame,
            text="Adicionar Novo Cliente",
            command=self.create_new_customer,
        )
        self.create_customer_button.pack(side=tk.LEFT, padx=5)

        # Editar dados de um cliente
        self.edit_customer_button = tk.Button(
            buttons_frame,
            text="Editar Dados de um Cliente",
            command=self.update_customer,
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

        # Ver detalhes do cliente
        self.view_details_button = tk.Button(
            buttons_frame,
            text="Ver Detalhes do Cliente",
            command=self.customers_list_details,
        )
        self.view_details_button.pack(side=tk.LEFT, padx=5)

        # Frame para detalhes do cliente
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
            cpf, name, contact, gender, date_birth = result
            repeated_cpf_msg = self.controller.create_new_customer(
                cpf, name, contact, gender, date_birth
            )
            if repeated_cpf_msg != None:
                messagebox.showwarning("Aviso", repeated_cpf_msg)
                self.create_new_customer()
            else:
                self.refresh_customers_list()

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
            popup = NewCustomerPopup(self, self.controller, customer)
            result = popup.show()
            if result:
                new_cpf, name, contact, gender, date_birth = result
                repeated_cpf_msg = self.controller.update_customer(
                    cpf,
                    new_cpf,
                    name,
                    contact,
                    gender,
                    date_birth,  # passar ainda o antigo cpf pois é a key
                )
                if repeated_cpf_msg != None:
                    messagebox.showwarning("Aviso", repeated_cpf_msg)
                    self.update_customer()
                else:
                    self.refresh_customers_list()

    def search_customer(self):
        popup = AskCpf(self)
        cpf_result = popup.show()
        if cpf_result == None:  # no caso de apertar o botão cancelar
            return
        try:
            customer = self.controller.get_customer(cpf_result)
            messagebox.showinfo(
                "Cliente encontrado",
                f"    CPF: {customer.cpf}\n    Nome: {customer.name}\n    Contato: {customer.contact}\n    Gênero: {customer.gender}\n    Data de nascimento: {customer.date_birth}",
            )
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

    def customers_list_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_items = self.customers_table.selection()
        if selected_items:
            selected_item = selected_items[0]  # Primeiro item selecionado
            customer_details = self.customers_table.item(selected_item, "values")
            customer_cpf = customer_details[0]  # CPF do cliente

            customer = self.controller.get_customer(customer_cpf)

            if customer:
                # Frames para cada seção
                cpf_frame = tk.Frame(self.details_frame)
                cpf_frame.pack(fill=tk.X, pady=2)
                name = tk.Frame(self.details_frame)
                name.pack(fill=tk.X, pady=2)
                contact = tk.Frame(self.details_frame)
                contact.pack(fill=tk.X, pady=2)
                gender = tk.Frame(self.details_frame)
                gender.pack(fill=tk.X, pady=2)
                date_birth = tk.Frame(self.details_frame)
                date_birth.pack(fill=tk.X, pady=2)
                loyalty_card = tk.Frame(self.details_frame)
                loyalty_card.pack(fill=tk.X, pady=2)

                # cpf
                tk.Label(cpf_frame, text="CPF:", font=("Arial", 10, "bold")).pack(
                    side=tk.LEFT
                )
                tk.Label(cpf_frame, text=f"{customer.cpf}").pack(side=tk.LEFT, padx=5)

                # nome
                tk.Label(
                    name,
                    text="Nome:",
                    font=("Arial", 10, "bold"),
                ).pack(side=tk.LEFT)
                tk.Label(name, text=f"{customer.name}").pack(side=tk.LEFT, padx=5)

                # contato
                tk.Label(contact, text="Contato:", font=("Arial", 10, "bold")).pack(
                    side=tk.LEFT
                )
                tk.Label(contact, text=f"{customer.contact}").pack(side=tk.LEFT, padx=5)

                # gênero
                tk.Label(gender, text="Gênero:", font=("Arial", 10, "bold")).pack(
                    side=tk.LEFT
                )
                tk.Label(gender, text=f"{customer.gender}").pack(side=tk.LEFT, padx=5)

                # data de nascimento
                tk.Label(
                    date_birth, text="Data de Nascimento:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT)
                tk.Label(date_birth, text=f"{customer.date_birth}").pack(
                    side=tk.LEFT, padx=5
                )

                # cartão de fidelidade
                tk.Label(
                    loyalty_card,
                    text="Progresso Cartão Fidelidade:",
                    font=("Arial", 10, "bold"),
                ).pack(side=tk.LEFT)
                tk.Label(loyalty_card, text=f"{customer.loyalty_card} pedido(s)").pack(
                    side=tk.LEFT, padx=5
                )
