from DAO.dao import DAO
from models.menu import Menu


class MenuDAO(DAO):
    def __init__(self):
        super().__init__("menus.pkl")

    def add(self, menu: Menu):
        if (
            (menu is not None)
            and isinstance(menu, Menu)
            and isinstance(menu.menu_id, int)
        ):
            super().add(menu.menu_id, menu)

    def update(self, menu: Menu):
        if (
            (menu is not None)
            and isinstance(menu, Menu)
            and isinstance(menu.menu_id, int)
        ):
            super().update(menu.menu_id, menu)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
