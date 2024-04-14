from models.user import User


class UserController:
    def __init__(self, app_controller):
        self.__app_controller = app_controller
        self.users = []

    def get_all_users(self):
        return self.users

    def add_user(self, name, email):
        user = User(name, email)
        self.users.append(user)

    def update_user(self, index, new_name, new_email):
        if index < len(self.users):
            self.users[index].name = new_name
            self.users[index].email = new_email

    def delete_user(self, index):
        if index < len(self.users):
            del self.users[index]
