# classe menu tem um id, nome categoria, e uma serie de Produtos


class Menu:
    def __init__(self, menu_id, name, category, products):
        self.menu_id = menu_id
        self.name = name
        self.category = category
        self.products = products

    def __str__(self):
        return f"Menu ID: {self.menu_id}, Nome: {self.name}, Categoria: {self.category}, Produtos: {self.products}"
