import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime


class MenuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Container principal
        main_frame = ttk.Frame(self, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Nome do Cardápio
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))  # Espaçamento inferior

        ttk.Label(name_frame, text="Nome do Cardápio:", width=15).pack(side=tk.LEFT)
        self.menu_name_entry = ttk.Entry(name_frame)
        self.menu_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Categoria
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=(0, 20))  # Espaçamento inferior

        ttk.Label(category_frame, text="Categoria:", width=15).pack(side=tk.LEFT)
        self.menu_category_entry = ttk.Entry(category_frame)
        self.menu_category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Lista de Produtos
        products_frame = ttk.Frame(main_frame)
        products_frame.pack(fill=tk.BOTH, expand=True)

        # Simulando a estrutura da imagem
        for product in self.controller.get_products():
            product_frame = ttk.Frame(products_frame, relief="solid", borderwidth=1)
            product_frame.pack(fill=tk.X, pady=(0, 10))  # Espaçamento inferior

            ttk.Label(product_frame, text=product.name, width=15).pack(
                side=tk.LEFT, padx=10
            )
            ttk.Label(product_frame, text=product.description).pack(
                side=tk.LEFT, fill=tk.X, expand=True
            )

            # Botões (simulação)
            ttk.Button(product_frame, text="Add", width=3).pack(side=tk.RIGHT, padx=5)

        # Botão Salvar
        save_button = ttk.Button(
            main_frame, text="Salvar Cardápio", command=self.save_menu
        )
        save_button.pack()

    def populate_product_listbox(self):
        """Preenche a Listbox com os produtos."""
        products = self.controller.get_products()
        for product in products:
            self.product_listbox.insert(tk.END, product.name)  # Exibe o nome do produto

    def save_menu(self):
        selected_indices = self.product_listbox.curselection()
        selected_products = [
            self.controller.get_products()[i] for i in selected_indices
        ]
        menu_name = self.menu_name_entry.get()
        menu_category = self.menu_category_entry.get()
        self.controller.create_menu(selected_products, menu_name, menu_category)
