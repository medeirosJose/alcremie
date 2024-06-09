import tkinter
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import random


class NewProductPopup:
    def __init__(self, parent, controller, product=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Editar produto" if product else "Novo produto")
        self.controller = controller
        self.product = product
        self.result = None
        self.image = None
        self.file_path = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 450
        window_height = 550

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("450x550")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        # input de nome do produto
        tk.Label(input_frame, text="Nome do produto: *").grid(
            row=0, column=0, sticky="e", padx=5
        )
        self.name_input = ttk.Entry(
            input_frame,
            width=40,
        )
        self.name_input.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        # input de preço
        tk.Label(input_frame, text="Preço: *").grid(row=1, column=0, sticky="e", padx=5)
        tk.Label(input_frame, text="Preço (R$): *").grid(
            row=1, column=0, sticky="e", padx=5
        )
        self.price_input = ttk.Entry(
            input_frame,
            width=40,
        )
        self.price_input.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        # input de descrição
        tk.Label(input_frame, text="Descrição: *").grid(
            row=2, column=0, sticky="e", padx=5
        )
        self.description_input = ttk.Entry(
            input_frame,
            width=40,
        )
        self.description_input.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        # input de peso
        tk.Label(input_frame, text="Peso (gramas):").grid(
            row=3, column=0, sticky="e", padx=5
        )
        self.weight_input = ttk.Entry(
            input_frame,
            width=40,
        )
        self.weight_input.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        # input de ingredientes
        tk.Label(input_frame, text="Ingredientes:").grid(
            row=4, column=0, sticky="e", padx=5
        )
        self.ingredients_input = ttk.Entry(
            input_frame,
            width=40,
        )
        self.ingredients_input.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

        # input de receita
        tk.Label(input_frame, text="Receita:").grid(row=5, column=0, sticky="e", padx=5)
        self.recipe_input = tk.Text(
            input_frame,
            width=20,
            height=5,
        )
        self.recipe_input.grid(row=5, column=1, sticky="ew", pady=5, padx=5)

        # input de imagem

        image_label = tk.Label(input_frame)
        image_label.grid(row=7, column=1, sticky="e", padx=5)

        def upload_image():
            # Abrir o diálogo de seleção de arquivo
            self.file_path = tkinter.filedialog.askopenfilename(title="Selecionar Imagem")

            # Verificar se um arquivo foi selecionado
            if self.file_path:
                try:
                    # Abrir a imagem com o Pillow
                    self.image = Image.open(self.file_path)

                    # Redimensionar a imagem para caber no label
                    resized_image = self.image.resize((200, 200))

                    # Converter a imagem para o formato Tkinter
                    img = ImageTk.PhotoImage(resized_image)

                    # Atualizar o label com a nova imagem
                    image_label.configure(image=img)
                    image_label.image = img

                except Exception as e:
                    # Exibir mensagem de erro caso a imagem não possa ser aberta
                    tk.messagebox.showerror("Erro", f"Erro ao abrir a imagem: {e}")

        upload_image_button = tk.Button(input_frame, text="Selecionar Imagem", command=upload_image)
        upload_image_button.grid(row=6, column=1, sticky="ew", padx=5)

        # coloca os valores atuais dos atributos de produto em cada input
        if product:
            price = str(product.price).replace(".", ",")
            weight = str(product.weight).replace(".", ",")
            self.name_input.insert(0, product.name)
            self.price_input.insert(0, price)
            self.description_input.insert(0, product.description)
            self.weight_input.insert(0, weight)
            self.recipe_input.insert("1.0", product.recipe)
            self.ingredients_input.insert(0, product.ingredients)

        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

    def confirm(self):
        name = self.name_input.get()
        price = self.price_input.get()
        description = self.description_input.get()
        weight = self.weight_input.get()
        recipe = self.recipe_input.get("1.0", "end-1c")
        ingredients = self.ingredients_input.get()

        if not name or not price or not description:
            messagebox.showerror(
                "Erro",
                "Os campos nome, preço e descrição são obrigatórios",
            )
            return

        if price:
            try:
                float(price.replace(",", "."))
            except ValueError:
                messagebox.showerror(
                    "Erro",
                    "O campo de preço deve ser um número",
                )
                return
            price = float(price.replace(",", "."))

        if weight:
            try:
                float(weight.replace(",", "."))
            except ValueError:
                messagebox.showerror(
                    "Erro",
                    "O campo de peso deve ser um número",
                )
                return
            weight = float(weight.replace(",", "."))

        if self.image:
            # Definir o caminho para salvar a imagem no repositório
            repository_path = './images/'
            # Extrair o nome do arquivo e a extensão da imagem
            filename, file_extension = os.path.splitext(self.file_path)

            # Criar o nome do arquivo salvo (incluindo data e hora)
            new_filename = f"{name}_{random.randint(1,99999)}{file_extension}"
            print(new_filename)

            # Salvar a imagem no repositório
            path = os.path.join(repository_path, new_filename)
            self.image.save(path)
            self.file_path = path

            # Mensagem de sucesso
            tk.messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")

        image = self.file_path
        self.result = (name, price, description, weight, recipe, ingredients, image)
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result


class ProductView(tk.Frame):
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

        self.products_table = ttk.Treeview(
            self,
            columns=("ID", "Nome", "Preço (R$)", "Descrição"),
            show="headings",
        )

        self.products_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.products_table.heading("Nome", text="Nome")
        self.products_table.heading("Preço (R$)", text="Preço (R$)")
        self.products_table.heading("Descrição", text="Descrição", anchor=tk.CENTER)

        self.products_table.column("ID", width=25, anchor=tk.CENTER)  # Pequeno
        self.products_table.column("Nome", width=25, anchor=tk.CENTER)  # Pequeno
        self.products_table.column("Preço (R$)", width=100, anchor=tk.CENTER)  # Médio
        self.products_table.column("Descrição", width=400, anchor=tk.CENTER)  # Médio

        self.products_table.pack(side="top", fill="both", expand=True, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10, padx=10, fill=tk.X, side=tk.TOP)

        # Criar um novo produto
        self.create_product_button = tk.Button(
            buttons_frame,
            text="Criar Novo Produto",
            command=self.open_new_product_popup,
        )
        self.create_product_button.pack(side=tk.LEFT, padx=5)

        # Editar um produto existente
        self.edit_product_button = tk.Button(
            buttons_frame, text="Editar produto", command=self.edit_product
        )
        self.edit_product_button.pack(side=tk.LEFT, padx=5)

        # Remover um produto selecionado
        self.remove_product_button = tk.Button(
            buttons_frame, text="Remover produto", command=self.remove_product
        )
        self.remove_product_button.pack(side=tk.LEFT, padx=5)

        # Ver detalhes do produto
        self.view_details_button = tk.Button(
            buttons_frame,
            text="Ver detalhes do produto",
            command=self.refresh_product_details,
        )
        self.view_details_button.pack(side=tk.LEFT, padx=5)

        # Frame para detalhes do produto
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

        self.refresh_products_list()

    def open_new_product_popup(self):
        popup = NewProductPopup(self, self.controller)
        result = popup.show()
        if result:
            name, price, description, weight, recipe, ingredients = result
            self.controller.create_new_product(name, price, description, weight, recipe, ingredients)
            self.refresh_products_list()

    def edit_product(self):
        selected_items = self.products_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")
            return
        selected_item = selected_items[0]
        product_details = self.products_table.item(selected_item, "values")
        product_id = int(product_details[0])
        product = self.controller.get_product_details(product_id)
        if product:
            popup = NewProductPopup(
                self, self.controller, product
            )  # Assuma que você ajustará o NewProductPopup para aceitar um pedido existente
            result = popup.show()
            if result:
                name, price, description, weight, recipe, ingredients = result
                self.controller.update_product(
                    product_id, name, price, description, weight, recipe, ingredients
                )
                self.refresh_products_list()

    def remove_product(self):
        selected_items = self.products_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um produto para remover.")
            return
        selected_item = selected_items[0]
        product_details = self.products_table.item(selected_item, "values")
        product_id = int(product_details[0])
        product_name = product_details[1]
        if messagebox.askyesno("Confirmar", "Deseja realmente remover este produto?"):
            print(f"Removendo o produto {product_name}")
            self.controller.remove_product(product_id)
            self.refresh_products_list()

    def refresh_products_list(self):
        # Primeiro, limpa a tabela atual removendo todos os itens
        for item in self.products_table.get_children():
            self.products_table.delete(item)

        # Busca todos os produtos existentes através do ProductController
        products = self.controller.get_products()

        # Itera sobre os produtos e insere-os na Treeview
        for product in products:
            price = str(product.price).replace(".", ",")
            self.products_table.insert(
                "",
                "end",
                values=(
                    product.id,
                    product.name,
                    price,
                    product.description,
                ),
            )

    def refresh_product_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_items = self.products_table.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        else:
            selected_item = selected_items[0]  # Primeiro item selecionado
            product_details = self.products_table.item(selected_item, "values")
            product_id = int(product_details[0])  # ID do pedido

            product = self.controller.get_product_details(product_id)

            if product:
                # Frames para cada seção
                name_frame = tk.Frame(self.details_frame)
                name_frame.pack(fill=tk.X, pady=2)
                price_frame = tk.Frame(self.details_frame)
                price_frame.pack(fill=tk.X, pady=2)
                description_frame = tk.Frame(self.details_frame)
                description_frame.pack(fill=tk.X, pady=2)
                weight_frame = tk.Frame(self.details_frame)
                weight_frame.pack(fill=tk.X, pady=2)
                recipe_frame = tk.Frame(self.details_frame)
                recipe_frame.pack(fill=tk.X, pady=2)
                ingredients_frame = tk.Frame(self.details_frame)
                ingredients_frame.pack(fill=tk.X, pady=2)

                # Nome
                tk.Label(name_frame, text="Nome:", font=("Arial", 10, "bold")).pack(
                    side=tk.LEFT
                )
                tk.Label(name_frame, text=f"{product.name}").pack(side=tk.LEFT, padx=5)

                # Preço
                price = str(product.price).replace(".", ",")
                tk.Label(
                    price_frame,
                    text="Preço (R$):",
                    font=("Arial", 10, "bold"),
                ).pack(side=tk.LEFT)
                tk.Label(price_frame, text=f"{price}").pack(
                    side=tk.LEFT, padx=5
                )

                # Descrição
                tk.Label(
                    description_frame, text="Descrição:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT)
                tk.Label(description_frame, text=f"{product.description}").pack(
                    side=tk.LEFT, padx=5
                )

                # Peso
                weight = str(product.weight).replace(".", ",")
                tk.Label(
                    weight_frame, text="Peso:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT)
                tk.Label(weight_frame, text=f"{weight}").pack(
                    side=tk.LEFT, padx=5
                )

                # Receita
                tk.Label(
                    recipe_frame, text="Receita:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT)
                tk.Label(recipe_frame, text=f"{product.recipe}").pack(
                    side=tk.LEFT, padx=5
                )

                # Ingredientes
                tk.Label(
                    ingredients_frame, text="Ingredientes:", font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT)
                tk.Label(ingredients_frame, text=f"{product.ingredients}").pack(
                    side=tk.LEFT, padx=5
                )
