import tkinter as tk
from tkinter import messagebox, ttk


class NewSupplierPopup:
    def __init__(self, parent, controller, supplier=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Novo Fornecedor" if not supplier else "Editar Fornecedor")
        self.controller = controller
        self.supplier = supplier
        self.result = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 400
        window_height = 250

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        # colocao a janela no centro da tela
        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.top.geometry("350x200")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        # CNPJ
        cnpj_label = tk.Label(input_frame, text="CNPJ:")
        cnpj_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=3)

        self.cnpj_entry = tk.Entry(input_frame, width=30)
        self.cnpj_entry.grid(row=0, column=1, sticky="ew")
        self.cnpj_entry.bind("<KeyRelease>", self.format_cnpj_entry)

        # Company
        company_label = tk.Label(input_frame, text="Empresa:")
        company_label.grid(row=1, column=0, sticky="w", pady=5)
        self.company_entry = tk.Entry(input_frame)
        self.company_entry.grid(row=1, column=1, sticky="ew", pady=5)

        # Contact
        contact_label = tk.Label(input_frame, text="Contato:")
        contact_label.grid(row=2, column=0, sticky="w", pady=5)
        self.contact_entry = tk.Entry(input_frame)
        self.contact_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # Ingredients
        ingredients_label = tk.Label(input_frame, text="Insumo:")
        ingredients_label.grid(row=3, column=0, sticky="w", pady=5)
        self.ingredients_entry = tk.Entry(input_frame)
        self.ingredients_entry.grid(row=3, column=1, sticky="ew", pady=5)

        # Botões
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        # Botão de salvar
        save_button = tk.Button(
            buttons_frame, text="Salvar", command=self.save_supplier
        )
        save_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Botão de cancelar
        cancel_button = tk.Button(
            buttons_frame, text="Cancelar", command=self.top.destroy
        )
        cancel_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        if supplier:
            self.cnpj_entry.insert(0, supplier.cnpj)
            self.company_entry.insert(0, supplier.company)
            self.contact_entry.insert(0, supplier.contact)
            self.ingredients_entry.insert(0, supplier.ingredients)

    def format_cnpj_entry(self, event):
        cnpj = self.cnpj_entry.get()
        cnpj = "".join(c for c in cnpj if c.isdigit())
        if len(cnpj) > 14:
            cnpj = cnpj[:14]

        formatted_cnpj = "{}.{}.{}/{}-{}".format(
            cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:]
        )
        self.cnpj_entry.delete(0, tk.END)
        self.cnpj_entry.insert(0, formatted_cnpj)

    def save_supplier(self):
        cnpj = self.cnpj_entry.get()
        company = self.company_entry.get().capitalize()
        contact = self.contact_entry.get()
        ingredients = self.ingredients_entry.get()

        # valida os campos
        validate_supplier = self.controller.validate_supplier_fields(
            cnpj, company, contact, ingredients
        )

        if validate_supplier != True:
            self.show_popup("Aviso", validate_supplier)
            return

        self.result = {
            "cnpj": cnpj,
            "company": company,
            "contact": contact,
            "ingredients": ingredients,
        }

        self.top.destroy()

    # def validate_supplier(self, cnpj, company, contact, ingredients):
    #     if self.controller.get_supplier(cnpj):
    #         messagebox.showwarning("Aviso", "CNPJ já cadastrado!")
    #         return False

    #     if (
    #         not cnpj
    #         or not company
    #         or not contact
    #         or not ingredients
    #         and len(cnpj) != 14
    #     ):
    #         messagebox.showwarning("Aviso", "Preencha todos os campos!")
    #         return False

    #     return True

    def show_popup(self, title, message):
        messagebox.showwarning(title, message)

    def show(self):
        if self.top.winfo_exists():  # Check if window exists
            self.top.grab_set()  # Make popup modal
            self.top.wait_window()
            self.top.grab_release()
        return self.result


class SupplierView(ttk.Frame):
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

        self.suppliers_table = ttk.Treeview(
            self,
            columns=("cnpj", "company", "contact", "ingredients"),
            show="headings",
            height=10,
        )
        self.suppliers_table.heading("cnpj", text="CNPJ", anchor=tk.CENTER)
        self.suppliers_table.heading("company", text="Empresa")
        self.suppliers_table.heading("contact", text="Contato")
        self.suppliers_table.heading("ingredients", text="Insumos")

        self.suppliers_table.column("cnpj", width=100, anchor=tk.CENTER)
        self.suppliers_table.column("company", width=200, anchor=tk.CENTER)
        self.suppliers_table.column("contact", width=200)
        self.suppliers_table.column("ingredients", width=200)

        self.suppliers_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)

        # criar novo fornecedor
        self.create_supplier_button = tk.Button(
            buttons_frame,
            text="Adicionar fornecedor",
            command=self.open_create_supplier_popup,
        )
        self.create_supplier_button.pack(side="left", padx=5)

        # editar fornecedor
        self.update_supplier_button = tk.Button(
            buttons_frame, text="Editar fornecedor", command=self.update_supplier
        )
        self.update_supplier_button.pack(side="left", padx=5)

        # remover fornecedor
        self.remove_supplier_button = tk.Button(
            buttons_frame, text="Remover fornecedor", command=self.remove_supplier
        )
        self.remove_supplier_button.pack(side="left", padx=5)

        # ver detalhes do fornecedor
        self.view_supplier_button = tk.Button(
            buttons_frame,
            text="Ver detalhes do fornecedor",
            command=self.refresh_supplier_details,
        )
        self.view_supplier_button.pack(side="left", padx=5)

        # frame para detalhes do fornecedor
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

        self.refresh_supplier_table()

    def refresh_supplier_table(self):
        for item in self.suppliers_table.get_children():
            self.suppliers_table.delete(item)

        suppliers = self.controller.get_all_suppliers()
        # # print("os suppliers", suppliers)

        for supplier in suppliers:
            self.suppliers_table.insert(
                "",
                "end",
                values=(
                    supplier.cnpj,
                    supplier.company,
                    supplier.contact,
                    supplier.ingredients,
                ),
            )

    def update_supplier(self):
        selected_supplier = self.suppliers_table.selection()
        if not selected_supplier:
            messagebox.showwarning("Aviso", "Selecione um fornecedor!")
            return
        else:
            selected_supplier = selected_supplier[0]
            supplier_details = self.suppliers_table.item(selected_supplier, "values")
            supplier_cpnj = supplier_details[0]

            supplier = self.controller.get_supplier_details(supplier_cpnj)
            if supplier:
                popup = NewSupplierPopup(self, self.controller, supplier)
                result = popup.show()
                if result:
                    # # print("result", result)
                    company = result["company"]
                    contact = result["contact"]
                    ingredients = result["ingredients"]
                    cnpj = result["cnpj"]
                    repeated_cpf_msg = self.controller.update_supplier(
                        supplier_cpnj, cnpj, company, contact, ingredients
                    )
                    if repeated_cpf_msg:
                        messagebox.showwarning("Aviso", repeated_cpf_msg)
                        self.update_supplier()
                    else:
                        self.refresh_supplier_table()

    def remove_supplier(self):
        selected_supplier = self.suppliers_table.selection()
        if not selected_supplier:
            messagebox.showwarning("Aviso", "Selecione um fornecedor!")
            return
        else:
            selected_supplier = selected_supplier[0]
            supplier_details = self.suppliers_table.item(selected_supplier, "values")
            supplier_cpnj = supplier_details[0]

            self.controller.remove_supplier(supplier_cpnj)
            self.refresh_supplier_table()

    # metodo que faz a atualizacao dos detalhes do fornecedor na view
    def refresh_supplier_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_supplier = self.suppliers_table.selection()
        if not selected_supplier:
            messagebox.showwarning("Aviso", "Selecione um fornecedor!")
            return
        else:
            selected_supplier = selected_supplier[0]
            supplier_details = self.suppliers_table.item(selected_supplier, "values")
            supplier_cpnj = supplier_details[0]

            supplier = self.controller.get_supplier_details(supplier_cpnj)

            self.update_details_frame(supplier)

    def update_details_frame(self, supplier):
        cnpj_frame = tk.Frame(self.details_frame)
        cnpj_frame.pack(fill=tk.X, pady=2)
        company_frame = tk.Frame(self.details_frame)
        company_frame.pack(fill=tk.X, pady=2)
        contact_frame = tk.Frame(self.details_frame)
        contact_frame.pack(fill=tk.X, pady=2)
        ingredients_frame = tk.Frame(self.details_frame)
        ingredients_frame.pack(fill=tk.X, pady=2)

        # CNPJ
        tk.Label(cnpj_frame, text="CNPJ:", font=("Arial", 10, "bold")).pack(
            side=tk.LEFT
        )
        tk.Label(cnpj_frame, text=supplier.cnpj).pack(side=tk.LEFT)

        # Company
        tk.Label(company_frame, text="Company:", font=("Arial", 10, "bold")).pack(
            side=tk.LEFT
        )
        tk.Label(company_frame, text=supplier.company).pack(side=tk.LEFT)

        # Contact
        tk.Label(contact_frame, text="Contact:", font=("Arial", 10, "bold")).pack(
            side=tk.LEFT
        )
        tk.Label(contact_frame, text=supplier.contact).pack(side=tk.LEFT)

        # Ingredients
        tk.Label(
            ingredients_frame, text="Ingredients:", font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT)
        tk.Label(ingredients_frame, text=supplier.ingredients).pack(side=tk.LEFT)

    def open_create_supplier_popup(self):
        while True:
            popup = NewSupplierPopup(self, self.controller)
            result = popup.show()
            if result:
                cnpj = result["cnpj"]
                company = result["company"]
                contact = result["contact"]
                ingredients = result["ingredients"]
                msg = self.controller.create_new_supplier(
                    cnpj, company, contact, ingredients
                )
                if msg:
                    messagebox.showwarning("Aviso", msg)
                else:
                    self.refresh_supplier_table()
                    break  # Se a criação for bem sucedida, saia do loop
            else:
                break  # Se o usuário cancelar, saia do loop
