from controllers.controller import Controller
from views.view import View


def main():
    controller = Controller()
    view = View(controller)
    view.run()

if __name__ == "__main__":
    main()
