class Product:
    def __init__(self, id: int, name: str, price: float, description: str, weight: float, recipe: str, ingredients=None):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__weight = weight
        self.__recipe = recipe
        self.__ingredients = ingredients or []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price: float):
        self.__price = price

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description = description

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight: str):
        self.__weight = weight

    @property
    def recipe(self):
        return self.__recipe

    @recipe.setter
    def recipe(self, recipe: str):
        self.__recipe = recipe

    def get_ingredients(self):
        return self.__ingredients

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients
