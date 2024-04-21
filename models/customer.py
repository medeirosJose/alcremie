class Customer:
    def __init__(self, cpf, name, contact, gender, date_birth):
        self.__cpf = cpf
        self.__name = name
        self.__contact = contact
        self.__gender = gender
        self.__date_birth = date_birth
        self.__loyalty_card = 0

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

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender: str):
        if isinstance(gender, str):
            self.__gender = gender

    @property
    def date_birth(self):
        return self.__date_birth

    @date_birth.setter
    def date_birth(self, date_birth: str):
        if isinstance(date_birth, str):
            self.__date_birth = date_birth

    @property
    def loyalty_card(self):
        return self.__loyalty_card

    @loyalty_card.setter
    def loyalty_card(self, loyalty_card: int):
        if isinstance(loyalty_card, int):
            self.__loyalty_card = loyalty_card