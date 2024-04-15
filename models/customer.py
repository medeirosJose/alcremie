class Customer:
    def __init__(self, cpf, name, contact):
        self.__cpf = cpf
        self.__name = name
        self.__contact = contact

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        if isinstance(cpf, str):
            self.__cpf = cpf

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self.__name = name

    @property
    def contact(self):
        return self.__contact

    @contact.setter
    def contact(self, contact: str):
        if isinstance(contact, str):
            self.__contact = contact
