import tkinter as tk

# isso aqui é só pra poder colocar o icon na janela
from PIL import Image, ImageTk


class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()

        # Define o título da janela
        self.root.title("Confeitaria Alcremie")

        icon = Image.open("alcremie.ico")
        icon = ImageTk.PhotoImage(icon)

        # Define o ícone da janela
        self.root.iconphoto(True, icon)

        # Maximiza a janela
        self.root.state("zoomed")

        # Obtenha as dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Altura da barra de tarefas
        taskbar_height = screen_height - self.root.winfo_reqheight()

        # Defina a geometria da janela para a tela menos a altura da barra de tarefas
        self.root.geometry(f"{screen_width}x{screen_height - taskbar_height}")

        self.label = tk.Label(self.root, text="")
        self.label.pack()

        # Botão para adicionar dados
        self.button = tk.Button(self.root, text="Adicionar Dado", command=self.add_data)
        self.button.pack()

    def add_data(self):
        data = "Novo Dado"
        self.controller.add_data(data)
        self.update_label()

    def update_label(self):
        # Atualiza o texto do label com os dados do modelo
        data = self.controller.get_data()
        self.label.config(text="\n".join(data))

    def run(self):
        self.root.mainloop()
