import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk  # Importe o Pillow (PIL fork)


class MenuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_products = []

        # Container principal
        main_frame = ttk.Frame(self, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Nome do Cardápio
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(name_frame, text="Nome do Cardápio:*", width=30).pack(side=tk.LEFT)
        self.menu_name_entry = ttk.Entry(name_frame)
        self.menu_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Categoria
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(category_frame, text="Categoria:*", width=30).pack(side=tk.LEFT)
        self.menu_category_entry = ttk.Entry(category_frame)
        self.menu_category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Lista de produtos para seleção
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        canvas = tk.Canvas(canvas_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        products_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=products_frame, anchor=tk.NW)
        products_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        for product in self.controller.get_products():
            product_frame = ttk.Frame(products_frame, relief="solid", borderwidth=1)
            product_frame.pack(fill=tk.X, pady=(0, 20))

            checkbutton_frame = ttk.Frame(product_frame, padding=(20, 10, 20, 10))
            checkbutton_frame.pack(side=tk.LEFT)

            var = tk.BooleanVar()
            checkbutton = ttk.Checkbutton(
                checkbutton_frame,
                text=product.name,
                variable=var,
                command=lambda p=product, v=var: self.toggle_product(p, v),
            )

            checkbutton.pack()

            separator = ttk.Separator(product_frame, orient=tk.VERTICAL)
            separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

            # Descrição do produto
            ttk.Label(product_frame, text=product.description).pack(
                side=tk.LEFT, fill=tk.X, expand=True
            )

            # Imagem do produto
            if product.image:
                try:
                    image = Image.open(product.image)
                    image = image.resize((150, 150))  # Aumenta o tamanho para 150x150
                    photo = ImageTk.PhotoImage(image)
                    image_label = ttk.Label(product_frame, image=photo)
                    image_label.image = photo
                    image_label.pack(side=tk.RIGHT)  # Espaçamento à direita
                except FileNotFoundError:
                    ttk.Label(
                        product_frame, text="Imagem não encontrada", width=20
                    ).pack(side=tk.RIGHT)
            else:
                ttk.Label(product_frame, text="Sem imagem", width=10).pack(
                    side=tk.RIGHT
                )

        products_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        save_button = ttk.Button(
            button_frame, text="Montar Cardápio", command=self.save_menu
        )
        save_button.pack()

    def toggle_product(self, product, var):
        if var.get():
            self.selected_products.append(product)
        else:
            self.selected_products.remove(product)

    def save_menu(self):
        menu_name = self.menu_name_entry.get()
        menu_category = self.menu_category_entry.get()

        if not menu_name or not menu_category:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        # Verifica se self.selected_products está vazio
        if not self.selected_products:
            messagebox.showerror("Erro", "Selecione ao menos um produto!")
            return

        print("Produtos selecionados:")
        for product in self.selected_products:
            print(product)
        self.controller.create_menu(self.selected_products, menu_name, menu_category)
        # messagebox.showinfo("Sucesso", "Cardápio criado com sucesso!")
