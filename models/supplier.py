class Supplier:
    def __init__(self, cnpj, company, contact, ingredients):
        self.__cnpj = cnpj
        self.__company = company
        self.__contact = contact
        self.__ingredients = ingredients

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        self.__cnpj = cnpj

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, company):
        self.__company = company

    @property
    def contact(self):
        return self.__contact

    @contact.setter
    def contact(self, contact):
        self.__contact = contact

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        self.__ingredients = ingredients
