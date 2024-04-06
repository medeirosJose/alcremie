from models.model import Model


class Controller:
    def __init__(self):
        self.model = Model()

    def add_data(self, data):
        self.model.add_data(data)

    def get_data(self):
        return self.model.get_data()
