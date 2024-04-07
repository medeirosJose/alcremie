class Product:
    def __init__(self, id: int, name: str, price: float, description: str, measure: str, ingredients=None):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__measure = measure
        self.__ingredients = ingredients or []

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
    def measure(self):
        return self.__measure

    @measure.setter
    def measure(self, measure: str):
        self.__measure = measure


    def get_ingredients(self):
        return self.__ingredients

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients
